"""Edison Scientific (antiga FutureHouse) como motor principal de DESCOBERTA de artigos da base científica.

O Literature (ex-Crow/Falcon) lê a literatura e devolve uma resposta com referências; o Precedent (ex-Owl) responde
"alguém já testou X em humanos?". O script manda a pergunta, guarda a resposta e entrega os artigos citados como
CANDIDATOS para o Jorge aprovar no /montar-condicao. A regra da base não muda: a Ficha cita o artigo baixado e
processado na base, nunca a resposta do agente.

Só biblioteca padrão do Python (HTTP direto, nada instalado). Endereços conferidos no código do pacote oficial
edison-client 0.18.0: POST /auth/login {api_key} -> JWT; POST /v0.1/crows {name, query} -> trajectory_id;
GET /v0.2/trajectories/{id}?lite=true (status) e ?lite=false (resposta completa).

A chave NUNCA vai para o chat nem para a pasta do OneDrive: fica em  C:\\Users\\<usuário>\\.edison-key  (ou na
variável EDISON_PLATFORM_API_KEY). O script nunca imprime a chave.

Tudo o que o script guarda fica em "01 - BASE CIENTÍFICA/_MÁQUINA/edison/":
  <tema>/AAAA-MM-DD_HHMM_<agente>.md|.json|.bruto.json.gz   resposta legível, resumo estruturado e resposta completa
  <tema>/candidatos.md|.json                                 artigos citados, no formato do /montar-condicao
  creditos.jsonl  config.json                                 registro de créditos e plano

Uso (S = "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/edison.py"):
  python S chave [--abrir] [--testar]            cria o arquivo da chave (vazio), abre no Bloco de Notas, testa o login
  python S plano [--mes N] [--literature N] [--high N] [--precedent N]   mostra/ajusta o plano de créditos
  python S creditos                              créditos gastos no mês e no total
  python S perguntar "<tema>" "<pergunta>" [--agente literature|high|precedent] [--modelo fontes|revisao|curta|
         precedente|livre] [--autorizado] [--seco] [--so-enviar]
  python S coletar "<tema>" <task_id> [--agente ...]      pega uma resposta enviada com --so-enviar (ou que passou do tempo)
  python S candidatos "<tema>" [--n 20] [--sem-rede]      DOIs/PMIDs citados + tipo, ano, tamanho e situação na base
"""
import argparse
import datetime as dt
import gzip
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = Path(__file__).resolve().parent          # .../_MÁQUINA/scripts
MAQ = AQUI.parent                               # .../01 - BASE CIENTÍFICA/_MÁQUINA
EDI = MAQ / "edison"
CREDITOS = EDI / "creditos.jsonl"
CONFIG = EDI / "config.json"
CHAVE = Path(os.path.expanduser("~")) / ".edison-key"

BASE_URL = "https://api.platform.edisonscientific.com"
UA = "base-cientifica-edison/1.0"
AGENTES = {  # nome curto -> (job da API, rótulo)
    "literature": ("job-futurehouse-paperqa3", "Literature"),
    "high": ("job-futurehouse-paperqa3-high", "Literature High"),
    "precedent": ("job-futurehouse-paperqa3-precedent", "Precedent"),
}
ALIAS = {"literature-high": "high", "literature_high": "high", "crow": "literature", "falcon": "literature",
         "owl": "precedent"}
TERMINAIS = {"success", "fail", "cancelled", "truncated"}
POLL_S = 10
TIMEOUT_S = 40 * 60
# Plano inicial = a última tabela pública (até abril de 2026): 10 créditos/mês, Literature High 5x. O custo por agente
# NÃO está na doc oficial: ajuste com `plano` depois de olhar o saldo na plataforma.
CONFIG_PADRAO = {"limite_mes": 10, "custo": {"literature": 1, "high": 5, "precedent": 1}, "confirmado": False}

MODELOS = {
    "fontes": ("Liste as melhores fontes para: {x}. Priorize diretrizes vigentes, revisões sistemáticas e meta-análises "
               "recentes e ensaios clínicos randomizados em humanos. Para cada fonte dê: citação completa, DOI, ano, tipo "
               "de estudo, número de participantes e o resultado principal com o número absoluto. Separe o que é estudo "
               "em humanos do que é estudo em célula ou animal e diga onde os estudos discordam e o que ainda não se sabe. "
               "Responda em português."),
    "revisao": ("Faça uma revisão completa sobre {x}: definição, causas conhecidas, o que já foi testado como tratamento ou "
                "solução, onde os estudos discordam e o que ainda não se sabe. Separe evidência de ensaio clínico em "
                "humanos de evidência de laboratório ou em animal, cite cada ponto com DOI e termine com as 3 perguntas "
                "em aberto mais importantes. Responda em português."),
    "curta": ("{x} Responda em até 10 linhas, com a citação, o DOI e o ano de cada afirmação, e diga quantos estudos "
              "sustentam cada ponto. Responda em português."),
    "precedente": ("Alguém já testou {x} em humanos? Se sim, liste os trabalhos com ano, DOI, tamanho do estudo, duração, "
                   "dose e resultado. Se não, diga o que existe de mais parecido e o que falta. Responda em português."),
    "livre": "{x}",
}


def sa(t):
    t = unicodedata.normalize("NFD", t or "")
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", sa(t)).strip("-")[:60] or "tema"


def agora():
    return dt.datetime.now()


# ------------------------------------------------------------------ HTTP e login
class ErroEdison(Exception):
    pass


def le_chave():
    k = os.environ.get("EDISON_PLATFORM_API_KEY") or os.environ.get("EDISON_API_KEY")
    if k:
        return k.strip()
    if CHAVE.exists():
        k = CHAVE.read_text(encoding="utf-8-sig", errors="replace").strip()
        if k:
            return k.splitlines()[0].strip()
    return None


def http(metodo, url, corpo=None, token=None, timeout=60):
    h = {"User-Agent": UA, "Accept": "application/json", "x-client": "sdk"}
    dados = None
    if corpo is not None:
        h["Content-Type"] = "application/json"
        dados = json.dumps(corpo).encode()
    if token:
        h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=dados, headers=h, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


class Sessao:
    def __init__(self):
        self.chave = le_chave()
        if not self.chave:
            raise ErroEdison("Sem chave da Edison. Rode:  python edison.py chave --abrir  (o Jorge cola a chave no Bloco de Notas).")
        self.jwt = None

    def login(self):
        st, b = http("POST", BASE_URL + "/auth/login", {"api_key": self.chave})
        if st != 200:
            raise ErroEdison(f"Login recusado (HTTP {st}): chave inválida, apagada ou sem acesso. Crie outra em Account > Profile > API Tokens.")
        self.jwt = json.loads(b)["access_token"]

    def req(self, metodo, caminho, corpo=None, tentar=3):
        if not self.jwt:
            self.login()
        ultimo = None
        for t in range(tentar):
            try:
                st, b = http(metodo, BASE_URL + caminho, corpo, self.jwt)
                if st in (401, 403) and t == 0:      # token vencido: um novo login e repete uma vez
                    self.login()
                    continue
                return st, b
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                ultimo = e
                time.sleep(2 * (t + 1))
        raise ErroEdison(f"Sem conexão com a Edison: {ultimo}")


def msg_http(st, b):
    try:
        d = json.loads(b)
        det = d.get("detail", d) if isinstance(d, dict) else d
    except Exception:
        det = b[:300].decode("utf-8", "replace")
    return f"HTTP {st}: {str(det)[:400]}"


# ------------------------------------------------------------------ créditos
def config():
    if CONFIG.exists():
        c = json.loads(CONFIG.read_text(encoding="utf-8"))
        c.setdefault("custo", {}).update({k: v for k, v in CONFIG_PADRAO["custo"].items() if k not in c["custo"]})
        return c
    return json.loads(json.dumps(CONFIG_PADRAO))


def salva_config(c):
    EDI.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")


def ledger():
    if not CREDITOS.exists():
        return []
    return [json.loads(l) for l in CREDITOS.read_text(encoding="utf-8").splitlines() if l.strip()]


def registra(**linha):
    EDI.mkdir(parents=True, exist_ok=True)
    linha = {"ts": agora().isoformat(timespec="seconds"), **linha}
    with CREDITOS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def gasto(mes=None):
    """Créditos estimados já gastos (conta no envio da tarefa). mes = 'AAAA-MM' ou None (total)."""
    return sum(l.get("creditos", 0) for l in ledger() if l.get("evento") == "enviada" and (mes is None or l["ts"][:7] == mes))


def cmd_creditos(_a):
    c = config()
    mes = agora().strftime("%Y-%m")
    L = ledger()
    env = [l for l in L if l.get("evento") == "enviada"]
    print(f"Plano: {c['limite_mes']} créditos/mês"
          + ("" if c.get("confirmado") else "  (a confirmar: tabela pública antiga; o saldo real aparece na plataforma)"))
    print(f"Custo por pergunta (estimado): Literature {c['custo']['literature']}, Literature High {c['custo']['high']}, "
          f"Precedent {c['custo']['precedent']}")
    print(f"Gasto em {mes}: {gasto(mes)} de {c['limite_mes']}  ·  total desde o início: {gasto()}  ·  perguntas: {len(env)}")
    for l in env[-8:]:
        print(f"  {l['ts'][:16]} · {l['agente']} · {l['tema']} · {l['creditos']} cr · {l.get('task_id', '')[:8]}")
    usd = [l["custo_usd"] for l in L if l.get("evento") == "resultado" and l.get("custo_usd")]
    if usd:
        print(f"Custo em dólar informado pela API nas respostas: {sum(usd):.2f} (o que a Edison gasta com o modelo, não o seu plano)")


def cmd_plano(a):
    c = config()
    mudou = False
    if a.mes is not None:
        c["limite_mes"], mudou = a.mes, True
    for chave, v in (("literature", a.literature), ("high", a.high), ("precedent", a.precedent)):
        if v is not None:
            c["custo"][chave], mudou = v, True
    if mudou:
        c["confirmado"] = True
        salva_config(c)
        print("Plano atualizado.")
    cmd_creditos(a)


# ------------------------------------------------------------------ chave
def cmd_chave(a):
    if not CHAVE.exists():
        CHAVE.write_text("", encoding="utf-8")
        print(f"Arquivo da chave criado (vazio): {CHAVE}")
    tem = bool(le_chave())
    if a.abrir and not tem:
        subprocess.Popen(["notepad.exe", str(CHAVE)])
        print("Bloco de Notas aberto. Cole a chave, aperte Ctrl+S e feche.")
        return
    if not tem:
        print(f"Chave ainda vazia. Arquivo: {CHAVE}")
        return
    print("Chave encontrada (não é mostrada).")
    if a.testar:
        try:
            Sessao().login()
            print("Login na Edison: OK.")
        except ErroEdison as e:
            sys.exit(str(e))


# ------------------------------------------------------------------ enviar e coletar
def nome_agente(x):
    x = ALIAS.get(sa(x), sa(x))
    if x not in AGENTES:
        sys.exit(f"Agente '{x}' inválido. Use: literature, high ou precedent.")
    return x


def pasta_tema(tema):
    p = EDI / slug(tema)
    p.mkdir(parents=True, exist_ok=True)
    return p


def cmd_perguntar(a):
    ag = nome_agente(a.agente)
    c = config()
    custo = c["custo"][ag]
    modelo = a.modelo or ("precedente" if ag == "precedent" else "fontes")
    texto = MODELOS[modelo].format(x=a.pergunta)
    mes = agora().strftime("%Y-%m")
    usado = gasto(mes)
    print(f"Agente: {AGENTES[ag][1]} · custo estimado: {custo} crédito(s) · mês {mes}: {usado} de {c['limite_mes']} usados"
          + ("" if c.get("confirmado") else " (plano a confirmar)"))
    if usado + custo > c["limite_mes"] and not a.autorizado:
        sys.exit(f"PARE: passaria do plano grátis ({usado}+{custo} > {c['limite_mes']}). Só com ⏸ do Jorge: rode de novo com --autorizado "
                 f"depois que ele disser sim (ou ajuste o plano real com `plano --mes N`).")
    if a.seco:
        print("[seco] Nada enviado. Pergunta que iria:\n" + texto)
        return
    s = Sessao()
    corpo = {"name": AGENTES[ag][0], "query": texto}
    st, b = s.req("POST", "/v0.1/crows", corpo)
    if st == 422:   # o cliente oficial manda o corpo completo, com campos nulos
        corpo = {"id": None, "project_id": None, "persona_id": None, **corpo, "runtime_config": None,
                 "caller_target_id": None, "caller_project_id": None, "tags": None, "workspace_id": None}
        st, b = s.req("POST", "/v0.1/crows", corpo)
    if st in (402, 429) or (st >= 400 and b"credit" in b.lower()):
        sys.exit("A Edison recusou por falta de créditos ou limite. " + msg_http(st, b))
    if st >= 400:
        sys.exit("Erro ao enviar a tarefa. " + msg_http(st, b))
    tid = json.loads(b)["trajectory_id"]
    registra(evento="enviada", tema=a.tema, agente=ag, task_id=tid, creditos=custo, modelo=modelo,
             autorizado=bool(a.autorizado), pergunta=a.pergunta[:200])
    print(f"Tarefa enviada: {tid}")
    if a.so_enviar:
        print(f"Depois: python edison.py coletar \"{a.tema}\" {tid} --agente {ag}")
        return
    coleta(s, a.tema, tid, ag, a.pergunta)


def espera(s, tid):
    """Consulta o status leve até terminar. Devolve o status final."""
    ini = time.time()
    ult = None
    while True:
        st, b = s.req("GET", f"/v0.2/trajectories/{tid}?history=false&lite=true")
        if st >= 400:
            raise ErroEdison("Erro ao consultar a tarefa. " + msg_http(st, b))
        status = json.loads(b).get("status", "?")
        if status != ult:
            print(f"  status: {status} ({int(time.time() - ini)} s)", flush=True)
            ult = status
        if status in TERMINAIS:
            return status
        if time.time() - ini > TIMEOUT_S:
            raise ErroEdison(f"Passou de {TIMEOUT_S // 60} min e a tarefa segue '{status}'. Pegue depois com: coletar \"<tema>\" {tid}")
        time.sleep(POLL_S)


def baixa_blobs(dados):
    """A resposta completa guarda o estado em arquivos assinados (download_url); busca e embute, sem o cabeçalho de login."""
    linhas = []
    if isinstance(dados.get("agent_state"), list):
        linhas += [r for r in dados["agent_state"] if isinstance(r, dict)]
    if isinstance(dados.get("environment_frame"), dict):
        linhas.append(dados["environment_frame"])
    for r in linhas:
        if r.get("state") is None and r.get("download_url"):
            req = urllib.request.Request(r["download_url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                raw = resp.read()
            if raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            r["state"] = json.loads(raw)
        r.pop("download_url", None)


def resumo_da_resposta(dados):
    ef = dados.get("environment_frame") or {}
    est = ((ef.get("state") or {}).get("state")) or {}
    resp = (est.get("response") or {}).get("answer") or {}
    uso = (est.get("info") or {}).get("usage") or {}
    return {
        "status": dados.get("status"), "agente_job": dados.get("crow"), "pergunta": dados.get("task"),
        "resposta": resp.get("answer"), "resposta_formatada": resp.get("formatted_answer"),
        "raciocinio": resp.get("answer_reasoning"), "resposta_ok": resp.get("has_successful_answer"),
        "custo_usd": uso.get("total_cost"), "consultas": uso.get("total_queries"),
    }


def coleta(s, tema, tid, ag, pergunta=""):
    status = espera(s, tid)
    st, b = s.req("GET", f"/v0.2/trajectories/{tid}?history=false&lite=false")
    if st >= 400:
        raise ErroEdison("Erro ao baixar a resposta. " + msg_http(st, b))
    dados = json.loads(b)
    baixa_blobs(dados)
    r = resumo_da_resposta(dados)
    r["task_id"] = tid
    r["agente"] = ag
    r["fontes"] = fontes_do_bruto(dados)
    p = pasta_tema(tema)
    base = p / f"{agora():%Y-%m-%d_%H%M}_{ag}"
    base.with_suffix(".json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    with gzip.open(str(base) + ".bruto.json.gz", "wt", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    md = [f"# {tema} — {AGENTES[ag][1]} ({agora():%Y-%m-%d %H:%M})", "",
          "> Resposta do agente: serve para DESCOBRIR artigos, não é evidência. A Ficha cita só o artigo baixado e processado na base.",
          "", f"**Pergunta:** {pergunta or r.get('pergunta') or ''}", f"**Status:** {status} · tarefa {tid}", "",
          "## Resposta", "", r.get("resposta_formatada") or r.get("resposta") or "(sem resposta)", ""]
    if r.get("raciocinio"):
        md += ["## Raciocínio do agente", "", r["raciocinio"], ""]
    base.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    registra(evento="resultado", tema=tema, agente=ag, task_id=tid, status=status, custo_usd=r.get("custo_usd"),
             consultas=r.get("consultas"))
    print(f"Resposta guardada: {base.with_suffix('.md')}")
    if not (r.get("resposta_formatada") or r.get("resposta")):
        print("ATENÇÃO: a resposta veio vazia (status " + status + "). Confira o .bruto.json.gz antes de gastar de novo.")
    print(f"Fontes citadas encontradas: {len(r['fontes'])}  ·  próximo: python edison.py candidatos \"{tema}\"")


def cmd_coletar(a):
    ag = nome_agente(a.agente)
    coleta(Sessao(), a.tema, a.task_id, ag)


# ------------------------------------------------------------------ extrair DOI/PMID
RE_DOI = re.compile(r"10\.\d{4,9}/[^\s<>\"',;\]]+")
RE_PMID = re.compile(r"PMID[:\s]*([0-9]{6,9})", re.I)


def limpa_doi(d):
    d = d.rstrip(".,;:")
    while d.endswith(")") and d.count("(") < d.count(")"):
        d = d[:-1].rstrip(".,;:")
    return d.lower()


def fontes_do_bruto(dados):
    """Procura, em qualquer ponto da resposta completa, blocos com metadados de artigo (doi + citação/título)."""
    achados = {}

    def anda(x):
        if isinstance(x, dict):
            doi = x.get("doi")
            if isinstance(doi, str) and RE_DOI.search(doi):
                d = limpa_doi(RE_DOI.search(doi).group(0))
                reg = achados.setdefault(d, {"doi": d})
                for k_out, ks in (("titulo", ("title", "titulo")), ("citacao", ("citation", "formatted_citation")),
                                  ("docname", ("docname",)), ("ano", ("year", "publication_year"))):
                    for k in ks:
                        if x.get(k) and not reg.get(k_out):
                            reg[k_out] = x[k]
            for v in x.values():
                anda(v)
        elif isinstance(x, list):
            for v in x:
                anda(v)
        elif isinstance(x, str) and len(x) > 20 and "10." in x:
            for m in RE_DOI.finditer(x):
                achados.setdefault(limpa_doi(m.group(0)), {"doi": limpa_doi(m.group(0))})

    anda(dados)
    return list(achados.values())


def refs_do_texto(texto):
    """DOIs e PMIDs citados no texto da resposta (a lista de referências vem no formatted_answer)."""
    dois = {limpa_doi(m.group(0)) for m in RE_DOI.finditer(texto or "")}
    pmids = set(RE_PMID.findall(texto or ""))
    return dois, pmids


# ------------------------------------------------------------------ candidatos
ORDEM = ["diretriz", "consenso", "posicionamento", "revisao-cochrane", "umbrella", "meta-analise", "revisao-sistematica",
         "ensaio-clinico", "mendeliana", "coorte", "caso-controle", "transversal", "revisao-narrativa", "pre-clinico", "outro",
         "errata"]


def indices_da_base():
    """DOI, PMID e título normalizado do catálogo e da fila: diz se o candidato já está na base."""
    idx = {"cat": {}, "fila": {}, "titulos": {}}
    cat = MAQ / "catalogo.jsonl"
    if cat.exists():
        for l in cat.read_text(encoding="utf-8").splitlines():
            if l.strip():
                c = json.loads(l)
                if c.get("doi"):
                    idx["cat"][c["doi"].lower()] = c["id"]
                idx["titulos"][re.sub(r"[^a-z0-9]+", " ", sa(c.get("titulo", "")))[:80]] = c["id"]
    fila = MAQ / "fila.jsonl"
    if fila.exists():
        for l in fila.read_text(encoding="utf-8").splitlines():
            if l.strip():
                f = json.loads(l)
                for k in ("doi", "pmid"):
                    if f.get(k):
                        idx["fila"][f[k].lower()] = f
    return idx


def cmd_candidatos(a):
    sys.path.insert(0, str(AQUI))
    import biblioteca as B  # noqa: PLC0415  (reaproveita Europe PMC, classificação e teto de certeza da base)
    B.SEM_REDE = bool(a.sem_rede)
    p = EDI / slug(a.tema)
    if not p.exists() or not list(p.glob("*.json")):
        sys.exit(f"Nenhuma resposta guardada para '{a.tema}'. Rode antes:  python edison.py perguntar \"{a.tema}\" \"<pergunta>\"")
    dois, pmids, info = set(), set(), {}
    for j in sorted(p.glob("*_*.json")):
        if j.name.startswith("candidatos"):
            continue
        r = json.loads(j.read_text(encoding="utf-8"))
        d, pm = refs_do_texto((r.get("resposta_formatada") or "") + "\n" + (r.get("resposta") or ""))
        dois |= d
        pmids |= set(pm)
        for f in r.get("fontes", []):
            dois.add(f["doi"])
            info.setdefault(f["doi"], f)
    idx = indices_da_base()
    cands = []
    for doi in sorted(dois):
        recs = B.epmc(f'DOI:"{doi}"', 1)
        cands.append(monta_candidato(B, idx, doi, "", recs[0] if recs else None, info.get(doi)))
    for pm in sorted(pmids):
        recs = B.epmc(f"EXT_ID:{pm} AND SRC:MED", 1)
        if recs and (recs[0].get("doi") or "").lower() in {c["doi"] for c in cands if c["doi"]}:
            continue
        cands.append(monta_candidato(B, idx, (recs[0].get("doi") if recs else "") or "", pm, recs[0] if recs else None, None))
    cands.sort(key=lambda c: (ORDEM.index(c["tipo"]) if c["tipo"] in ORDEM else 99, -(c["ano"] or 0)))
    saida = {"tema": a.tema, "gerado_em": agora().isoformat(timespec="seconds"), "candidatos": cands}
    (p / "candidatos.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    linhas = formata(cands, a.n)
    (p / "candidatos.md").write_text(
        f"# Candidatos: {a.tema}\n\n> Gerado de respostas da Edison por edison.py. Candidatos NÃO são evidência: o Jorge aprova, "
        f"o artigo é baixado e processado, e só então entra na Ficha.\n\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas))
    print(f"\n({len(cands)} candidatos; lista completa em {p / 'candidatos.md'})")


def monta_candidato(B, idx, doi, pmid, rec, info):
    meta = B.meta_epmc(rec) if rec else {}
    resumo = meta.get("resumo", "")
    titulo = meta.get("titulo") or (info or {}).get("titulo") or (info or {}).get("citacao") or ""
    tipo = B.classificar(titulo, meta.get("tipos_pub", []), resumo) if meta else "outro"
    teto = B.teto_certeza(tipo, resumo)["nivel"] if meta else "indefinida"
    amostra = B.tamanho_amostra(resumo) if resumo else {}
    doi = (meta.get("doi") or doi or "").lower()
    pmid = meta.get("pmid") or pmid
    pmcid = meta.get("pmcid") or ""
    na_base = idx["cat"].get(doi) if doi else None
    if not na_base:
        na_base = idx["titulos"].get(re.sub(r"[^a-z0-9]+", " ", sa(titulo))[:80]) if titulo else None
    na_fila = idx["fila"].get(doi) or idx["fila"].get((pmid or "").lower())
    aberto = bool(pmcid) or bool(rec and rec.get("isOpenAccess") == "Y")
    if na_base:
        situacao = f"JÁ NO CATÁLOGO: {na_base}"
    elif na_fila:
        situacao = f"NA FILA (acesso: {na_fila.get('acesso', '?')})"
    elif aberto:
        situacao = "novo, acesso aberto" + (f" ({pmcid})" if pmcid else "")
    else:
        situacao = "novo, provavelmente pago (Jorge baixa e solta em ENTRADA/)"
    return {"doi": doi, "pmid": pmid, "pmcid": pmcid, "titulo": titulo, "ano": meta.get("ano") or (info or {}).get("ano"),
            "revista": meta.get("revista", ""), "tipo": tipo, "teto_certeza": teto,
            "n": amostra.get("n") or amostra.get("n_estudos") or "", "situacao": situacao,
            "verificado_europepmc": bool(rec)}


def formata(cands, n):
    out = ["**Candidatos citados pela Edison** (tipo, ano, teto de certeza, tamanho do resumo, situação na base):", ""]
    for k, c in enumerate(cands[:n], 1):
        t = (c["titulo"] or "(sem título: conferir pelo DOI)")[:110]
        ids = " · ".join(x for x in (f"doi:{c['doi']}" if c["doi"] else "", f"pmid:{c['pmid']}" if c["pmid"] else "") if x)
        tam = f" · {c['n']}" if c["n"] else ""
        aviso = "" if c["verificado_europepmc"] else " · ⚠ não achado no Europe PMC (conferir se o artigo existe)"
        out.append(f"[{k}] {t}\n    {c['tipo']} (teto: {c['teto_certeza']}) · {c['ano'] or '?'} · {c['revista'] or '?'}{tam} · "
                   f"{ids}\n    → {c['situacao']}{aviso}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("chave")
    c.add_argument("--abrir", action="store_true")
    c.add_argument("--testar", action="store_true")
    c.set_defaults(f=cmd_chave)
    p = sub.add_parser("plano")
    p.add_argument("--mes", type=int)
    p.add_argument("--literature", type=int)
    p.add_argument("--high", type=int)
    p.add_argument("--precedent", type=int)
    p.set_defaults(f=cmd_plano)
    sub.add_parser("creditos").set_defaults(f=cmd_creditos)
    q = sub.add_parser("perguntar")
    q.add_argument("tema")
    q.add_argument("pergunta")
    q.add_argument("--agente", default="literature")
    q.add_argument("--modelo", choices=sorted(MODELOS))
    q.add_argument("--autorizado", action="store_true", help="o Jorge disse sim para passar do plano")
    q.add_argument("--seco", action="store_true", help="mostra o que enviaria, sem enviar nem gastar")
    q.add_argument("--so-enviar", action="store_true")
    q.set_defaults(f=cmd_perguntar)
    k = sub.add_parser("coletar")
    k.add_argument("tema")
    k.add_argument("task_id")
    k.add_argument("--agente", default="literature")
    k.set_defaults(f=cmd_coletar)
    d = sub.add_parser("candidatos")
    d.add_argument("tema")
    d.add_argument("--n", type=int, default=20)
    d.add_argument("--sem-rede", action="store_true")
    d.set_defaults(f=cmd_candidatos)
    a = ap.parse_args()
    try:
        a.f(a)
    except ErroEdison as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
