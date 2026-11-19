"""Ponte entre o motor de treino e o banco da consultoria (Supabase), sem pacote externo.

Mapeia o JSON do motor nas tabelas de `06 - GESTÃO DA CONSULTORIA/supabase/migrations/0001_schema.sql`:
    mesociclo (semana N)   → prescricoes_treino (1 linha) + exercicios (upsert por nome_tecnico) + itens_prescricao
    registro de cargas     → semanas_treino + sessoes + series (s1..s6: repetições e carga)
    check-in + decisão     → semanas_treino.esforco / dor / leitura / alertas
E o caminho de volta (o que o Tally grava → registro e check-in que o `calcular_treino.py decidir` lê):
    series + sessoes + semanas_treino + checkins (sono_qualidade, estresse, respostas) → registro.json + checkin.json

Por padrão NADA é enviado: os comandos imprimem as linhas e as chamadas REST (modo conferência). `--enviar` grava de verdade
(⏸ só com o OK do Jorge). A chave vem de %USERPROFILE%\\SoutoTreinador\\privado\\supabase.env (SUPABASE_URL e
SUPABASE_SERVICE_ROLE_KEY), nunca do repositório, e nunca é impressa.

Limites do esquema atual (pendências para o dono do banco):
  * `series` não tem RIR por série → o RIR vai em `sessoes.observacao`, uma linha por exercício: "RIR · <exercício>: 3,2,2";
  * `series` guarda no máximo 6 séries por exercício por sessão → séries extras ficam fora (o script avisa);
  * `checkins` não tem fadiga nem dor muscular em coluna → o script procura em `checkins.respostas` (jsonb) as chaves
    "fadiga" e "dor muscular"; sem elas, a prontidão usa só sono e estresse;
  * `itens_prescricao` não tem %1RM, carga nem RIR alvo → vão em `observacao`: "~90 kg (70% 1RM) · RIR alvo 3 · <técnica>".

    python "05 - TREINO/treino_supabase.py" prescricao --plano <mesociclo.json> --aluno-id <uuid> [--semana 1] [--versao 1] [--enviar]
    python "05 - TREINO/treino_supabase.py" registro   --registro <registro.json|csv> --aluno-id <uuid> [--plano ...] [--checkin ...] [--decisao ...] [--enviar]
    python "05 - TREINO/treino_supabase.py" baixar     --aluno-id <uuid> [--plano <mesociclo.json>] --saida <pasta>
    python "05 - TREINO/treino_supabase.py" saude      (testa a conexão, sem mostrar a chave)
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calcular_treino as ct  # noqa: E402

ENV_PADRAO = os.path.join(os.path.expanduser("~"), "SoutoTreinador", "privado", "supabase.env")
MAX_SERIES = 6


# ------------------------------------------------------------------------------------------------ conexão
def ler_env():
    caminho = os.environ.get("ST_SUPABASE_ENV") or ENV_PADRAO
    vals = {}
    if os.path.isfile(caminho):
        with open(caminho, encoding="utf-8-sig") as f:
            for l in f:
                l = l.strip()
                if l and not l.startswith("#") and "=" in l:
                    k, v = l.split("=", 1)
                    vals[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if os.environ.get(k):
            vals[k] = os.environ[k]
    vals["_arquivo"] = caminho
    return vals


class Rest:
    def __init__(self):
        env = ler_env()
        self.url = (env.get("SUPABASE_URL") or "").rstrip("/")
        self._k = env.get("SUPABASE_SERVICE_ROLE_KEY") or ""
        if not self.url or not self._k:
            sys.exit(f"Falta SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY em {env['_arquivo']} (o arquivo fica fora do repositório).")

    def __repr__(self):
        return f"Rest({self.url}, chave=***)"

    def pedir(self, metodo, rota, corpo=None, prefer="return=representation"):
        req = urllib.request.Request(f"{self.url}/rest/v1/{rota}", method=metodo,
                                     data=None if corpo is None else json.dumps(corpo).encode("utf-8"))
        req.add_header("apikey", self._k)
        req.add_header("Authorization", f"Bearer {self._k}")
        req.add_header("Content-Type", "application/json")
        if prefer:
            req.add_header("Prefer", prefer)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                txt = r.read().decode("utf-8")
                return json.loads(txt) if txt else None
        except urllib.error.HTTPError as e:
            sys.exit(f"Supabase respondeu {e.code} em {metodo} {rota.split('?')[0]}: {e.read().decode('utf-8', 'replace')[:400]}")

    def get(self, tabela, params):
        return self.pedir("GET", f"{tabela}?{urllib.parse.urlencode(params)}", prefer=None)


class Conferencia:
    """Modo padrão: mostra o que seria enviado, sem rede."""
    def pedir(self, metodo, rota, corpo=None, prefer=None):
        n = len(corpo) if isinstance(corpo, list) else 1
        print(f"\n# {metodo} /rest/v1/{rota}   ({n} linha(s))")
        print(json.dumps(corpo, ensure_ascii=False, indent=1)[:4000])
        if isinstance(corpo, list):
            return [dict(c, id=c.get("id") or f"<id de {c.get('nome_tecnico', 'linha')}>") for c in corpo]
        return [dict(corpo or {}, id=(corpo or {}).get("id") or "<id>")]


# ------------------------------------------------------------------------------------------------ montar linhas
def linhas_prescricao(plano, aluno_id, semana=1, versao=1):
    s = plano["semanas"][semana - 1]
    ini = datetime.date.fromisoformat(s["inicio"])
    validade = datetime.date.fromisoformat(plano["semanas"][-1]["inicio"]) + datetime.timedelta(days=6)
    pid = str(uuid.uuid4())
    presc = {
        "id": pid, "aluno_id": aluno_id, "versao": versao, "objetivo": plano.get("objetivo"), "nivel": plano.get("nivel"),
        "local_treino": plano.get("aluno", {}).get("local"), "sessoes_por_semana": len(s["sessoes"]),
        "inicio": ini.isoformat(), "validade": validade.isoformat(),
        "observacao": f"Mesociclo {plano.get('modelo')} · semana {semana} de {len(plano['semanas'])} ({s['fase']}) · motor 05 - TREINO",
    }
    exmap = {e["nome"]: e for e in plano.get("exercicios", [])}
    exercicios = []
    for nome, e in exmap.items():
        exercicios.append({"nome_tecnico": nome, "nome_aluno": nome, "grupo": e.get("grupo"),
                           "unidade_padrao": "kg total"})
    itens = []
    for d, lst in s["sessoes"].items():
        if not re.fullmatch(r"[A-F]", d):
            sys.exit(f"Dia '{d}' não cabe no banco (itens_prescricao.dia aceita só A a F).")
        for ordem, l in enumerate(lst, 1):
            carga = f"~{l['carga_kg']:g} kg ({l['pct_1rm']:g}% 1RM)" if l.get("carga_kg") is not None else "carga pelo RIR"
            obs = " · ".join(x for x in (carga, f"RIR alvo {l['rir']:g}", l.get("obs") or "") if x)
            itens.append({"prescricao_id": pid, "dia": d, "ordem": ordem, "_exercicio": l["exercicio"], "series": l["series"],
                          "repeticoes": l["reps"], "descanso_s": l["descanso_s"], "observacao": obs})
    return presc, exercicios, itens


def _segunda(iso):
    d = datetime.date.fromisoformat(iso)
    return (d - datetime.timedelta(days=d.weekday())).isoformat()


def linhas_registro(sessoes, aluno_id, prescricao_id=None, checkins=None, decisao=None, planejadas=None):
    checkins = checkins or {}
    semanas, sess_rows, series_rows, avisos = {}, [], [], []
    for s in sessoes:
        w = int(s["semana"])
        if w not in semanas:
            c = checkins.get(w, {})
            leitura = []
            if c:
                leitura.append(f"prontidão {ct.prontidao(c)}/10")
            if decisao and int(decisao.get("semana", -1)) == w:
                cont = {}
                for d in decisao["exercicios"]:
                    cont[d["decisao"]] = cont.get(d["decisao"], 0) + 1
                leitura.append("decisão do motor: " + ", ".join(f"{k} {v}" for k, v in cont.items()))
            semanas[w] = {
                "id": str(uuid.uuid4()), "aluno_id": aluno_id, "prescricao_id": prescricao_id,
                "semana_inicio": _segunda(s["data"]) if s.get("data") else None, "planejadas": planejadas, "completas": 0, "parciais": 0,
                "esforco": c.get("esforco"), "dor": c.get("dor_treino"), "leitura": " · ".join(leitura) or None,
                "alertas": (["Dor durante"] if (c.get("dor_treino") or 0) >= ct.REGRAS["dor_alerta"] else [])
                           + ([a.split(":")[0] for a in decisao.get("alertas", [])] if decisao and int(decisao.get("semana", -1)) == w else []),
            }
        semanas[w]["completas"] += 1
        sid = str(uuid.uuid4())
        rir_txt = []
        for e in s.get("exercicios", []):
            sr = e.get("series", [])
            if len(sr) > MAX_SERIES:
                avisos.append(f"semana {w} {s.get('dia')}: {e['nome']} tem {len(sr)} séries; o banco guarda {MAX_SERIES} (as extras ficam só no registro)")
            linha = {"sessao_id": sid, "aluno_id": aluno_id, "exercicio_nome": e["nome"], "unidade": "kg total"}
            for i, x in enumerate(sr[:MAX_SERIES], 1):
                if x.get("reps") is not None:
                    linha[f"s{i}_rep"] = int(x["reps"])
                if x.get("carga") is not None:
                    linha[f"s{i}_carga"] = float(x["carga"])
            series_rows.append(linha)
            rirs = [x.get("rir") for x in sr[:MAX_SERIES]]
            if any(r is not None for r in rirs):
                rir_txt.append(f"RIR · {e['nome']}: " + ",".join("" if r is None else f"{r:g}" for r in rirs))
        sess_rows.append({"id": sid, "aluno_id": aluno_id, "prescricao_id": prescricao_id, "semana_id": semanas[w]["id"],
                          "data": s.get("data"), "dia_treino": s.get("dia"), "status": "completa", "origem": "motor 05 - TREINO",
                          "observacao": "\n".join(rir_txt) or None})
    return list(semanas.values()), sess_rows, series_rows, avisos


# ------------------------------------------------------------------------------------------------ caminho de volta
def _num(respostas, *chaves):
    for k, v in (respostas or {}).items():
        kk = re.sub(r"\s+", " ", str(k).lower())
        if any(c in kk for c in chaves):
            try:
                return float(str(v).replace(",", "."))
            except ValueError:
                pass
    return None


def montar_registro(rest_or_dados, aluno_id, plano=None):
    """Baixa (ou recebe em dict, para teste) semanas_treino, sessoes, series e checkins e devolve (registro, checkin)."""
    if isinstance(rest_or_dados, dict):
        D = rest_or_dados
    else:
        r = rest_or_dados
        f = {"aluno_id": f"eq.{aluno_id}"}
        D = {"semanas_treino": r.get("semanas_treino", {**f, "select": "*", "order": "semana_inicio.asc"}),
             "sessoes": r.get("sessoes", {**f, "select": "*", "order": "data.asc"}),
             "series": r.get("series", {**f, "select": "*"}),
             "checkins": r.get("checkins", {**f, "select": "semana_inicio,sono_qualidade,estresse,respostas", "order": "semana_inicio.asc"})}
    inicio = plano["semanas"][0]["inicio"] if plano else None
    semanas_ord = sorted({s["semana_inicio"] for s in D["semanas_treino"] if s.get("semana_inicio")})
    def num_semana(iso):
        if inicio:
            return (datetime.date.fromisoformat(_segunda(iso)) - datetime.date.fromisoformat(inicio)).days // 7 + 1
        seg = _segunda(iso)
        return semanas_ord.index(seg) + 1 if seg in semanas_ord else len(semanas_ord) + 1
    por_sessao = {}
    for x in D["series"]:
        por_sessao.setdefault(x["sessao_id"], []).append(x)
    sessoes = []
    for s in D["sessoes"]:
        rir = {}
        for l in (s.get("observacao") or "").splitlines():
            m = re.match(r"RIR · (.+?): (.*)$", l.strip())
            if m:
                rir[m.group(1)] = [float(v) if v.strip() else None for v in m.group(2).split(",")]
        exs = []
        for x in por_sessao.get(s["id"], []):
            sr = []
            for i in range(1, MAX_SERIES + 1):
                if x.get(f"s{i}_rep") is None:
                    continue
                rr = rir.get(x["exercicio_nome"], [])
                sr.append({"carga": x.get(f"s{i}_carga") or 0, "reps": x[f"s{i}_rep"], "rir": rr[i - 1] if i - 1 < len(rr) else None})
            exs.append({"nome": x["exercicio_nome"], "series": sr})
        sessoes.append({"semana": num_semana(s["data"]), "data": s["data"], "dia": s.get("dia_treino") or "A", "exercicios": exs})
    chk = {}
    for st in D["semanas_treino"]:
        w = num_semana(st["semana_inicio"])
        chk.setdefault(w, {"semana": w})
        chk[w].update({"esforco": st.get("esforco"), "dor_treino": st.get("dor")})
    for c in D["checkins"]:
        w = num_semana(c["semana_inicio"])
        chk.setdefault(w, {"semana": w})
        chk[w].update({"sono": c.get("sono_qualidade"), "estresse": c.get("estresse"),
                       "fadiga": _num(c.get("respostas"), "fadiga", "cansa"),
                       "dor_muscular": _num(c.get("respostas"), "dor muscular")})
    registro = {"_sobre": "Baixado do Supabase por treino_supabase.py", "sessoes": sorted(sessoes, key=lambda s: (s["semana"], s["data"]))}
    checkin = {"semanas": [chk[k] for k in sorted(chk)]}
    return registro, checkin


# ------------------------------------------------------------------------------------------------ comandos
def cmd_prescricao(a):
    plano = ct.ler_json(a.plano)
    presc, exs, itens = linhas_prescricao(plano, a.aluno_id, a.semana, a.versao)
    api = Rest() if a.enviar else Conferencia()
    api.pedir("POST", "prescricoes_treino", presc)
    got = api.pedir("POST", "exercicios?on_conflict=nome_tecnico", exs, prefer="resolution=merge-duplicates,return=representation")
    ids = {g["nome_tecnico"]: g["id"] for g in (got or [])}
    for it in itens:
        it["exercicio_id"] = ids.get(it.pop("_exercicio"))
    api.pedir("POST", "itens_prescricao", itens)
    print(f"\n{'Enviado' if a.enviar else 'Conferência (nada enviado; use --enviar com o OK do Jorge)'}: "
          f"1 prescrição, {len(exs)} exercícios, {len(itens)} itens. Para usar como treino em uso: PATCH alunos.treino_em_uso_id = {presc['id']}")


def cmd_registro(a):
    plano = ct.ler_json(a.plano) if a.plano else None
    dec = ct.ler_json(a.decisao) if a.decisao else None
    plan = len(plano["semanas"][0]["sessoes"]) if plano else None
    sem, ses, ser, avisos = linhas_registro(ct.ler_registro(a.registro), a.aluno_id, a.prescricao_id, ct.ler_checkin(a.checkin), dec, plan)
    api = Rest() if a.enviar else Conferencia()
    api.pedir("POST", "semanas_treino", sem)
    api.pedir("POST", "sessoes", ses)
    api.pedir("POST", "series", ser)
    for av in avisos:
        print("AVISO:", av)
    print(f"\n{'Enviado' if a.enviar else 'Conferência (nada enviado)'}: {len(sem)} semanas, {len(ses)} sessões, {len(ser)} linhas de séries.")


def cmd_baixar(a):
    plano = ct.ler_json(a.plano) if a.plano else None
    reg, chk = montar_registro(Rest(), a.aluno_id, plano)
    os.makedirs(a.saida, exist_ok=True)
    ct.gravar_json(reg, os.path.join(a.saida, "registro-supabase.json"))
    ct.gravar_json(chk, os.path.join(a.saida, "checkin-supabase.json"))
    print(f"{len(reg['sessoes'])} sessões e {len(chk['semanas'])} semanas de check-in gravadas em {a.saida}")


def cmd_saude(_a):
    r = Rest()
    r.get("exercicios", {"select": "id", "limit": "1"})
    print(f"Conexão OK com {r.url} (chave não exibida).")


def main():
    ap = argparse.ArgumentParser(description="Motor de treino ↔ Supabase (conferência por padrão).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prescricao")
    p.add_argument("--plano", required=True)
    p.add_argument("--aluno-id", required=True)
    p.add_argument("--semana", type=int, default=1)
    p.add_argument("--versao", type=int, default=1)
    p.add_argument("--enviar", action="store_true")
    p.set_defaults(f=cmd_prescricao)
    p = sub.add_parser("registro")
    p.add_argument("--registro", required=True)
    p.add_argument("--aluno-id", required=True)
    p.add_argument("--prescricao-id")
    p.add_argument("--plano")
    p.add_argument("--checkin")
    p.add_argument("--decisao")
    p.add_argument("--enviar", action="store_true")
    p.set_defaults(f=cmd_registro)
    p = sub.add_parser("baixar")
    p.add_argument("--aluno-id", required=True)
    p.add_argument("--plano")
    p.add_argument("--saida", required=True)
    p.set_defaults(f=cmd_baixar)
    p = sub.add_parser("saude")
    p.set_defaults(f=cmd_saude)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
