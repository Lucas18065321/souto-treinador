"""Motor de prescrição de treino de força e controle volume × desempenho do SOUTO TREINADOR.

Só biblioteca padrão do Python (3.10+). Toda decisão cita a linha do Protocolo que a sustenta:
    01 - BASE CIENTÍFICA/Treino de força/Hipertrofia e força - Protocolo.md   (códigos [A1], [V1], [P1], [D1]...)

Comandos (rode da raiz do repositório; `python "05 - TREINO/calcular_treino.py" <comando> -h` explica cada um):
    1rm        estima a carga máxima (1RM) a partir de carga × repetições (+ RIR)
    tabela     monta a tabela de cargas por exercício a partir do 1RM e do RIR alvo
    volume     séries por grupo muscular e volume load (séries × repetições × kg) por semana, do registro de cargas
    decidir    PROGREDIR / MANTER / REDUZIR VOLUME / DELOAD por exercício e por grupo (registro + check-in)
    mesociclo  gera o mesociclo (linear, ondulatória ou blocos) com rampa de volume e semana de deload
    regras     lista as regras do motor e a linha do Protocolo de cada uma

Estimativas são estimativas: a tabela de repetições × %1RM é média de grupo (Nuzzo 2024) e cada pessoa varia (Richens 2014).
Dado de aluno nunca fica no repositório: as saídas vão para %USERPROFILE%\\SoutoTreinador\\Alunos\\<nome>\\Treinos\\.
"""
import argparse
import csv
import datetime
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
PROTOCOLO = "01 - BASE CIENTÍFICA/Treino de força/Hipertrofia e força - Protocolo.md"

# ===================================================================================================== REGRAS
# Cada número aqui tem uma linha no Protocolo. "operacional" = sem fonte direta na base (está nas Lacunas do Protocolo);
# o Jorge pode trocar. Mudou aqui? Mude no Protocolo também.
REGRAS = {
    # [M2] tendência do 1RM estimado em 2 semanas (%): >= +1 subindo; <= -2 caindo; entre os dois, estável (operacional)
    "tendencia_sobe_pct": 1.0,
    "tendencia_cai_pct": -2.0,
    # [M3] margem de RIR (repetições) para "ficou fácil" / "ficou pesado" (operacional)
    "margem_rir": 1,
    # [M4] prontidão 0-10 (média de sono, 10-fadiga, 10-dor muscular, 10-estresse): >=6 boa; <4 ruim (operacional)
    "prontidao_boa": 6.0,
    "prontidao_ruim": 4.0,
    # [D2] deload reativo: prontidão < 4 por 2 semanas, ou < 5 com metade+ dos principais caindo (operacional)
    "deload_prontidao_moderada": 5.0,
    "deload_fracao_caindo": 0.5,
    # [P2] passo de volume quando estagna com recuperação boa (séries por grupo por semana; operacional)
    "passo_series": 2,
    # [P3] bloco de baixo volume e alta tensão: corte de séries (Travis 2020: ~30 a <=50%)
    "reducao_volume": 0.4,
    "bloco_baixo_volume_semanas": "2 a 4",
    # [D1] deload: séries x0,5 (operacional) e RIR alvo +2 (afastar da falha: Bell 2023)
    "deload_fator_series": 0.5,
    "deload_rir_extra": 2,
    # [V1]-[V3] séries/grupo/semana: ponto de partida e teto por nível
    "inicio_series": {"iniciante": 6, "intermediario": 10, "avancado": 12},
    "teto_series": {"iniciante": 10, "intermediario": 20, "avancado": 20},
    # [M1] série de trabalho = RIR <= 4; grupo secundário conta 0,5 (operacional)
    "rir_serie_trabalho": 4,
    "peso_secundario": 0.5,
    # [E1] dor durante o treino >= 5/10 ou lesão nova: pausar progressão e encaminhar
    "dor_alerta": 5,
    # teto de séries de um exercício numa sessão (operacional; o banco também guarda até 6): acima disso, outro exercício
    "max_series_exercicio": 6,
    # [P5] semanas mínimas de registro para decidir
    "semanas_minimas": 2,
}

# Linha do Protocolo de cada código (para a decisão citar em uma linha)
CITA = {
    "A1": "[A1] 1RM estimado pela tabela repetições × %1RM (Nuzzo 2024; Grgic 2020)",
    "A4": "[A4] em iniciante o RIR só acompanha (Helms 2016)",
    "M1": "[M1] volume load só se compara no mesmo exercício e faixa (Schoenfeld 2016; Currier 2026)",
    "M2": "[M2] tendência do 1RM estimado em 2 semanas (cortes operacionais)",
    "M3": "[M3] RIR relatado × alvo (Helms 2016; margem operacional)",
    "M4": "[M4] prontidão subjetiva (Saw 2016; cortes operacionais)",
    "P1": "[P1] dupla progressão: repetições, depois carga pela tabela (Plotkin 2022; Nuzzo 2024)",
    "P2": "[P2] estagnou com recuperação boa: +2 séries/grupo/semana até o teto (Currier 2026; Baz-Valle 2022)",
    "P3": "[P3] bloco de baixo volume e alta tensão: -30 a -50% das séries, carga mantida (Schoenfeld 2019; Travis 2020)",
    "P4": "[P4] desempenho subindo e RIR no alvo: manter (Currier 2026)",
    "P5": "[P5] menos de 2 semanas de registro: manter e registrar",
    "D1": "[D1] deload planejado na última semana do mesociclo (Bell 2023)",
    "D2": "[D2] deload reativo por cansaço acumulado (Bell 2023; Saw 2016)",
    "E1": "[E1] dor ≥5/10 ou lesão nova: pausar progressão e encaminhar",
    "V": "[V1]-[V3] faixa de séries por nível (Currier 2026; Baz-Valle 2022; Iversen 2021)",
}

# ===================================================================================================== TABELA %1RM × REPETIÇÕES
# Nuzzo 2024 (meta-regressão, ~7000 pessoas), seç. Discussion: só os pontos escritos no texto do artigo.
#   geral (todos os exercícios menos supino e leg press): ~5 rep a 90% e ~15 a 70%
#   supino: ~4 a 90%, 8,8 a 80%, 14,1 a 70%      leg press: ~9 a 90%, 13,1 a 80%, 19,0 a 70%
# 100% = 1 repetição (definição de 1RM). Entre os pontos: interpolação no logaritmo das repetições (o artigo modelou o log).
# Abaixo de 70% é extrapolação (a tabela completa está numa figura que não temos em texto): o motor avisa.
TABELAS = {
    "geral": [(100.0, 1.0), (90.0, 5.0), (70.0, 15.0)],
    "supino": [(100.0, 1.0), (90.0, 4.0), (80.0, 8.8), (70.0, 14.1)],
    "legpress": [(100.0, 1.0), (90.0, 9.0), (80.0, 13.1), (70.0, 19.0)],
}
# Desvio-padrão entre pessoas (repetições), Nuzzo 2024: 2,51 a 80% e 4,36 a 60% (interpolado no log)
DP_ANCORAS = [(80.0, 2.51), (60.0, 4.36)]
PCT_MIN_ANCORADO = 70.0


def _tab(nome):
    n = (nome or "geral").lower().replace(" ", "").replace("-", "")
    if n in ("supino", "supinoreto", "benchpress", "bench"):
        return "supino"
    if n in ("legpress", "leg", "legpress45"):
        return "legpress"
    return "geral"


def reps_maximas(pct, tabela="geral"):
    """Repetições máximas esperadas (média) a uma %1RM. Devolve (reps, extrapolado)."""
    pts = TABELAS[_tab(tabela)]
    pct = max(1.0, min(100.0, float(pct)))
    for (p1, r1), (p2, r2) in zip(pts, pts[1:]):
        if p2 <= pct <= p1:
            f = (p1 - pct) / (p1 - p2)
            return math.exp(math.log(r1) + f * (math.log(r2) - math.log(r1))), False
    (p1, r1), (p2, r2) = pts[-2], pts[-1]  # extrapola com a última inclinação
    inc = (math.log(r2) - math.log(r1)) / (p1 - p2)
    return math.exp(math.log(r2) + (p2 - pct) * inc), True


def pct_para_reps(reps, tabela="geral"):
    """%1RM em que a média faz `reps` repetições máximas (inverso da tabela). Devolve (pct, extrapolado)."""
    pts = TABELAS[_tab(tabela)]
    reps = max(1.0, float(reps))
    for (p1, r1), (p2, r2) in zip(pts, pts[1:]):
        if r1 <= reps <= r2:
            f = (math.log(reps) - math.log(r1)) / (math.log(r2) - math.log(r1))
            return p1 - f * (p1 - p2), False
    (p1, r1), (p2, r2) = pts[-2], pts[-1]
    inc = (math.log(r2) - math.log(r1)) / (p1 - p2)
    return p2 - (math.log(reps) - math.log(r2)) / inc, True


def dp_reps(pct):
    (p1, d1), (p2, d2) = DP_ANCORAS
    f = (p1 - pct) / (p1 - p2)
    return math.exp(math.log(d1) + f * (math.log(d2) - math.log(d1)))


def epley(carga, reps):
    return carga * (1 + reps / 30.0)


def brzycki(carga, reps):
    return carga * 36.0 / (37.0 - reps) if reps < 37 else float("nan")


def estimar_1rm(carga, reps, rir=0, tabela="geral"):
    """1RM estimado. Repetições até a falha = feitas + RIR. Devolve dict com a estimativa principal (Nuzzo) e as de conferência."""
    carga, reps = float(carga), float(reps)
    rir = float(rir or 0)
    rf = reps + rir
    pct, extrap = pct_para_reps(rf, tabela)
    e = carga / (pct / 100.0)
    dp = dp_reps(pct)
    pct_lo, _ = pct_para_reps(max(1.0, rf - dp), tabela)  # quem faz menos repetições que a média: 1RM maior
    pct_hi, _ = pct_para_reps(rf + dp, tabela)
    avisos = []
    if extrap:
        avisos.append("acima das repetições ancoradas na tabela (abaixo de 70% 1RM): extrapolação, confiança menor")
    if rf > 12:
        avisos.append("mais de 12 repetições até a falha: a dispersão entre pessoas cresce (Nuzzo 2024); prefira 3 a 10")
    if rir > 4:
        avisos.append("RIR acima de 4: série longe da falha, a estimativa piora")
    return {
        "carga": carga, "reps": reps, "rir": rir, "reps_ate_falha": rf, "tabela": _tab(tabela),
        "pct_1rm": round(pct, 1), "1rm": round(e, 1),
        "faixa_1rm": sorted([round(carga / (pct_hi / 100.0), 1), round(carga / (pct_lo / 100.0), 1)]),
        "epley": round(epley(carga, rf), 1), "brzycki": round(brzycki(carga, rf), 1) if rf < 37 else None,
        "avisos": avisos,
    }


def arredonda_carga(kg, incremento=1.0, para_baixo=True):
    inc = float(incremento or 1.0)
    q = kg / inc
    q = math.floor(q + 1e-9) if para_baixo else round(q)
    return round(q * inc, 2)


def carga_para(e1rm, reps, rir, tabela="geral", incremento=1.0):
    """Carga para fazer `reps` deixando `rir` na reserva: %1RM da tabela para reps+rir."""
    pct, extrap = pct_para_reps(float(reps) + float(rir), tabela)
    return arredonda_carga(e1rm * pct / 100.0, incremento), round(pct, 1), extrap

# ===================================================================================================== ARQUIVOS


def ler_json(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        return json.load(f)


def gravar_json(obj, caminho):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def pasta_alunos():
    base = os.environ.get("ST_ALUNOS") or os.path.join(os.path.expanduser("~"), "SoutoTreinador", "Alunos")
    return os.path.normpath(base)


def nome_de_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*]', "", str(nome)).strip(" .")


def pasta_treinos(nome_aluno, criar=True):
    p = os.path.join(pasta_alunos(), nome_de_arquivo(nome_aluno), "Treinos")
    if criar:
        os.makedirs(p, exist_ok=True)
    return p


def ler_registro(caminho):
    """Registro de cargas em JSON {"sessoes":[{"semana","data","dia","exercicios":[{"nome","series":[{carga,reps,rir}]}]}]}
    ou CSV com colunas semana,data,dia,exercicio,serie,carga,reps,rir. Devolve a lista de sessões."""
    if caminho.lower().endswith(".csv"):
        sess = {}
        with open(caminho, encoding="utf-8-sig", newline="") as f:
            amostra = f.read(2048)
            f.seek(0)
            dial = csv.Sniffer().sniff(amostra, delimiters=",;\t")
            for l in csv.DictReader(f, dialect=dial):
                l = {k.strip().lower(): (v or "").strip() for k, v in l.items() if k}
                chave = (int(l["semana"]), l.get("data", ""), l.get("dia", "A"))
                s = sess.setdefault(chave, {"semana": chave[0], "data": chave[1], "dia": chave[2], "exercicios": []})
                ex = next((e for e in s["exercicios"] if e["nome"] == l["exercicio"]), None)
                if not ex:
                    ex = {"nome": l["exercicio"], "series": []}
                    s["exercicios"].append(ex)
                num = lambda x: float(x.replace(",", ".")) if x not in ("", None) else None
                ex["series"].append({"carga": num(l.get("carga", "")), "reps": num(l.get("reps", "")), "rir": num(l.get("rir", ""))})
        return [sess[k] for k in sorted(sess)]
    d = ler_json(caminho)
    return d["sessoes"] if isinstance(d, dict) else d


def ler_checkin(caminho):
    if not caminho:
        return {}
    d = ler_json(caminho)
    lst = d.get("semanas", d) if isinstance(d, dict) else d
    return {int(x["semana"]): x for x in lst}


def mapa_exercicios(plano):
    """nome → {grupo, secundarios, tabela, principal, incremento_kg, reps, rir}, do arquivo do aluno ou do plano gerado."""
    m = {}
    for e in (plano or {}).get("exercicios", []):
        m[e["nome"].lower()] = e
    return m

# ===================================================================================================== VOLUME


def prontidao(c):
    """[M4] média de sono, 10-fadiga, 10-dor muscular, 10-estresse (só as que vieram). None se nada veio."""
    if not c:
        return None
    partes = []
    if c.get("sono") is not None:
        partes.append(float(c["sono"]))
    for k in ("fadiga", "dor_muscular", "estresse"):
        if c.get(k) is not None:
            partes.append(10.0 - float(c[k]))
    return round(sum(partes) / len(partes), 1) if partes else None


def resumo_semanal(sessoes, exmap):
    """Por semana: séries de trabalho por grupo, volume load por exercício e grupo, melhor 1RM estimado por exercício."""
    lim = REGRAS["rir_serie_trabalho"]
    out = {}
    for s in sessoes:
        w = int(s["semana"])
        W = out.setdefault(w, {"grupos": {}, "vl_grupo": {}, "exercicios": {}, "series_sem_rir": 0})
        for e in s.get("exercicios", []):
            info = exmap.get(e["nome"].lower(), {})
            g = info.get("grupo", "outros")
            sec = info.get("secundarios", [])
            tab = info.get("tabela", "geral")
            X = W["exercicios"].setdefault(e["nome"], {"grupo": g, "series": 0, "vl": 0.0, "e1rm": None, "sessoes": []})
            reg = []
            for sr in e.get("series", []):
                carga, reps, rir = sr.get("carga"), sr.get("reps"), sr.get("rir")
                if reps is None:
                    continue
                carga = float(carga or 0)
                if rir is None:
                    W["series_sem_rir"] += 1
                trabalho = rir is None or float(rir) <= lim
                if trabalho:
                    X["series"] += 1
                    W["grupos"][g] = W["grupos"].get(g, 0) + 1
                    for g2 in sec:
                        W["grupos"][g2] = W["grupos"].get(g2, 0) + REGRAS["peso_secundario"]
                vl = carga * float(reps)
                X["vl"] += vl
                W["vl_grupo"][g] = W["vl_grupo"].get(g, 0.0) + vl
                if carga > 0 and reps >= 1:
                    est = estimar_1rm(carga, reps, rir or 0, tab)["1rm"]
                    X["e1rm"] = max(X["e1rm"] or 0, est)
                reg.append({"carga": carga, "reps": reps, "rir": rir})
            X["sessoes"].append(reg)
    for W in out.values():
        for X in W["exercicios"].values():
            X["vl"] = round(X["vl"], 1)
        W["vl_grupo"] = {k: round(v, 1) for k, v in W["vl_grupo"].items()}
    return dict(sorted(out.items()))

# ===================================================================================================== DECISÃO


def _tendencia(serie_e1rm, w):
    """[M2] variação % do 1RM estimado da semana w contra a melhor das 2 anteriores (ou a anterior)."""
    ant = [serie_e1rm[k] for k in (w - 2, w - 1) if serie_e1rm.get(k)]
    if not serie_e1rm.get(w) or not ant:
        return None
    ref = max(ant)
    return round((serie_e1rm[w] - ref) / ref * 100.0, 1)


def _classe(t):
    if t is None:
        return "sem dados"
    if t >= REGRAS["tendencia_sobe_pct"]:
        return "subindo"
    if t <= REGRAS["tendencia_cai_pct"]:
        return "caindo"
    return "estável"


def alvo_da_semana(plano, nome, semana):
    for s in plano.get("semanas", []):
        if s["semana"] == semana:
            for lst in s["sessoes"].values():
                for l in lst:
                    if l["exercicio"].lower() == nome.lower():
                        return {"reps": [l["reps_min"], l["reps_max"]], "rir": l["rir"]}
    return None


def decidir(plano, sessoes, checkins, semana=None, nivel=None, proxima_semana_deload=None):
    exmap = mapa_exercicios(plano)
    nivel = (nivel or plano.get("aluno", {}).get("nivel") or "intermediario").lower()
    nivel = "intermediario" if nivel.startswith("inter") else ("iniciante" if nivel.startswith("inic") else ("avancado" if nivel.startswith("avan") else nivel))
    res = resumo_semanal(sessoes, exmap)
    if not res:
        sys.exit("Registro vazio.")
    w = int(semana or max(res))
    c_w, c_ant = checkins.get(w, {}), checkins.get(w - 1, {})
    pr_w, pr_ant = prontidao(c_w), prontidao(c_ant)
    alertas, decisoes = [], []

    # ---- [E1] dor / lesão
    dor = c_w.get("dor_treino")
    dor_flag = bool(c_w.get("lesao_nova")) or (dor is not None and float(dor) >= REGRAS["dor_alerta"])
    if dor_flag:
        onde = c_w.get("dor_local") or "local não informado"
        alertas.append(f"ENCAMINHAR: dor {dor if dor is not None else '?'}/10 ou lesão nova ({onde}). Pausar a progressão do que dói e falar com o aluno; médico/fisioterapeuta se persistir. {CITA['E1']}")

    # ---- séries por exercício
    serie = {}
    for k, W in res.items():
        for nome, X in W["exercicios"].items():
            serie.setdefault(nome, {})[k] = X["e1rm"]
    principais = [n for n in res[w]["exercicios"] if exmap.get(n.lower(), {}).get("principal")] or list(res[w]["exercicios"])
    tend = {n: _tendencia(serie.get(n, {}), w) for n in res[w]["exercicios"]}
    caindo = [n for n in principais if _classe(tend.get(n)) == "caindo"]

    # ---- [D1]/[D2] deload (vale para o aluno todo)
    deload_motivo = None
    if pr_w is not None and pr_ant is not None and pr_w < REGRAS["prontidao_ruim"] and pr_ant < REGRAS["prontidao_ruim"]:
        deload_motivo = f"prontidão {pr_ant} e {pr_w}/10 (abaixo de {REGRAS['prontidao_ruim']:g}) duas semanas seguidas. {CITA['D2']}"
    elif pr_w is not None and pr_w < REGRAS["deload_prontidao_moderada"] and principais and len(caindo) / len(principais) >= REGRAS["deload_fracao_caindo"]:
        deload_motivo = (f"prontidão {pr_w}/10 e desempenho caindo em {len(caindo)} de {len(principais)} exercícios principais "
                         f"({', '.join(caindo)}). {CITA['D2']}")
    elif proxima_semana_deload:
        deload_motivo = f"semana de deload planejada no mesociclo. {CITA['D1']}"

    grupos_dec = {}
    for nome, X in res[w]["exercicios"].items():
        info = dict(exmap.get(nome.lower(), {}))
        alvo_sem = alvo_da_semana(plano, nome, w)  # alvo da própria semana no mesociclo, se houver
        if alvo_sem:
            info.update(alvo_sem)
        alvo_rir = float(info.get("rir", plano.get("rir_padrao", 2)))
        faixa = info.get("reps") or [8, 12]
        rmin, rmax = (faixa[0], faixa[-1]) if isinstance(faixa, list) else (int(faixa), int(faixa))
        ult = X["sessoes"][-1] if X["sessoes"] else []
        reps_feitas = [s["reps"] for s in ult if s["reps"] is not None]
        rirs = [s["rir"] for s in ult if s["rir"] is not None]
        rir_ult = rirs[-1] if rirs else None
        completou = bool(reps_feitas) and min(reps_feitas) >= rmin
        no_topo = bool(reps_feitas) and min(reps_feitas) >= rmax
        semanas_dados = sum(1 for k in serie.get(nome, {}) if k <= w and serie[nome][k])
        t = tend.get(nome)
        cl = _classe(t)
        estagnou = cl in ("estável", "caindo") and semanas_dados >= 3
        fac = rir_ult is not None and rir_ult >= alvo_rir + REGRAS["margem_rir"]
        pesado = rir_ult is not None and rir_ult <= alvo_rir - REGRAS["margem_rir"] and not completou
        confia_rir = nivel != "iniciante"
        carga_atual = max((s["carga"] for s in ult), default=0)
        tab, inc = info.get("tabela", "geral"), info.get("incremento_kg", 1.0)
        desc_t = f"1RM est. {X['e1rm'] or '-'} kg, tendência {t:+.1f}% ({cl})" if t is not None else f"1RM est. {X['e1rm'] or '-'} kg"
        sug = ""
        if dor_flag and (c_w.get("dor_local") or "").lower() and (c_w.get("dor_local") or "").lower() in (nome.lower() + " " + X["grupo"].lower()):
            dec, regra, motivo = "MANTER", "E1", f"dor relatada neste exercício/grupo: não progredir até conversar. {CITA['E1']}"
        elif deload_motivo:
            dec, regra, motivo = "DELOAD", ("D1" if "planejada" in deload_motivo else "D2"), deload_motivo
            if X["e1rm"]:
                cg, pct, _ = carga_para(X["e1rm"], rmin, alvo_rir + REGRAS["deload_rir_extra"], tab, inc)
                cg = min(cg, carga_atual) if carga_atual else cg  # deload nunca sobe a carga
                sug = f"séries ×{REGRAS['deload_fator_series']:g}, {rmin} reps com RIR {alvo_rir + REGRAS['deload_rir_extra']:g} (~{cg:g} kg, {pct:g}% 1RM)"
        elif semanas_dados < REGRAS["semanas_minimas"]:
            dec, regra, motivo = "MANTER", "P5", f"só {semanas_dados} semana(s) de registro. {CITA['P5']}"
        elif estagnou and (pr_w is not None and pr_w < REGRAS["prontidao_boa"] or (pesado and confia_rir)):
            dec, regra = "REDUZIR VOLUME", "P3"
            por = f"prontidão {pr_w}/10" if pr_w is not None and pr_w < REGRAS["prontidao_boa"] else f"RIR {rir_ult:g} abaixo do alvo {alvo_rir:g} sem completar as repetições"
            motivo = f"{desc_t} há 2+ semanas com {por}. {CITA['P3']}"
            sug = f"bloco de {REGRAS['bloco_baixo_volume_semanas']} semanas: séries -{int(REGRAS['reducao_volume'] * 100)}%, mesma carga ({carga_atual:g} kg) e mesmo RIR alvo"
        elif completou and (cl != "caindo") and ((fac and confia_rir) or no_topo):
            dec, regra = "PROGREDIR", "P1"
            if no_topo and X["e1rm"]:
                cg, pct, _ = carga_para(X["e1rm"], rmin, alvo_rir, tab, inc)
                if cg <= carga_atual:
                    cg = arredonda_carga(carga_atual + float(inc), inc)
                sug = f"carga {carga_atual:g} → {cg:g} kg e volta a {rmin} reps (RIR {alvo_rir:g})"
            else:
                nr = min(rmax, (min(reps_feitas) if reps_feitas else rmin) + 1)
                sug = f"mesma carga ({carga_atual:g} kg), +1 repetição por série (alvo {nr:g})"
            why = f"fez todas as repetições ({'topo da faixa' if no_topo else 'dentro da faixa'})" + (f" com RIR {rir_ult:g} ≥ alvo {alvo_rir:g}+{REGRAS['margem_rir']}" if fac and confia_rir else "")
            motivo = f"{why}; {desc_t}. {CITA['P1']}" + ("" if confia_rir else f" {CITA['A4']}")
        elif estagnou and cl == "estável" and (pr_w is None or pr_w >= REGRAS["prontidao_boa"]):
            dec, regra = "PROGREDIR", "P2"
            motivo = f"{desc_t} há 2+ semanas com prontidão boa ({pr_w if pr_w is not None else 'sem check-in'}). {CITA['P2']}"
            sug = f"+{REGRAS['passo_series']} séries/semana no grupo {X['grupo']} (sem passar de {REGRAS['teto_series'].get(nivel, 20)})"
        else:
            dec, regra = "MANTER", "P4"
            extra = f"; RIR {rir_ult:g} pesado para o alvo {alvo_rir:g}: confira a carga pela tabela" if pesado else ""
            if cl == "caindo":
                extra += "; queda com recuperação boa: repita a semana e confira execução, sono da véspera e a carga [M2]"
            motivo = f"{desc_t}, RIR {rir_ult if rir_ult is not None else '-'} (alvo {alvo_rir:g}){extra}. {CITA['P4']}"
        decisoes.append({"exercicio": nome, "grupo": X["grupo"], "decisao": dec, "regra": regra, "motivo": motivo,
                         "sugestao": sug, "e1rm": X["e1rm"], "tendencia_pct": t, "rir_ultima": rir_ult, "vl_semana": X["vl"]})
        grupos_dec.setdefault(X["grupo"], []).append(dec if regra != "P1" else "PROGREDIR-carga")

    # ---- decisão por grupo (volume)
    grupos = []
    teto = REGRAS["teto_series"].get(nivel, 20)
    for g, decs in grupos_dec.items():
        series = res[w]["grupos"].get(g, 0)
        if "DELOAD" in decs:
            d, why = "DELOAD", f"semana leve: ~{math.ceil(series * REGRAS['deload_fator_series'])} séries. {CITA['D1'] if 'planejada' in (deload_motivo or '') else CITA['D2']}"
        elif decs.count("REDUZIR VOLUME") * 2 >= len(decs):
            d, why = "REDUZIR VOLUME", f"{series:g} → ~{math.ceil(series * (1 - REGRAS['reducao_volume']))} séries/semana. {CITA['P3']}"
        elif "PROGREDIR" in decs and "REDUZIR VOLUME" not in decs:
            novo = min(teto, series + REGRAS["passo_series"])
            d, why = ("PROGREDIR", f"{series:g} → {novo:g} séries/semana (teto {teto}). {CITA['P2']}") if novo > series else ("MANTER", f"já no teto de {teto} séries. {CITA['V']}")
        else:
            d, why = "MANTER", f"{series:g} séries/semana. {CITA['P4']}"
        grupos.append({"grupo": g, "series_semana": series, "decisao": d, "motivo": why})

    return {
        "semana": w, "nivel": nivel, "prontidao": pr_w, "prontidao_anterior": pr_ant,
        "alertas": alertas, "exercicios": decisoes, "grupos": grupos,
        "fonte": PROTOCOLO, "gerado_em": datetime.date.today().isoformat(),
        "aviso": "Proposta do motor: o Jorge aprova antes de mudar a ficha. Estimativas de 1RM são médias de grupo.",
    }

# ===================================================================================================== MESOCICLO
# Esquemas de repetições/RIR por semana normal (a carga sai da tabela de Nuzzo para repetições + RIR).
# Os números do esquema são exemplos operacionais dentro das faixas do Protocolo [I1]/[I2]/[Z1]-[Z3].


def _esquema(modelo, objetivo, n):
    """Lista com n semanas normais; cada uma: {fase, zonas: [(reps_min, reps_max, rir)...] por sessão (ciclo)}."""
    forca = objetivo.startswith("for")
    def lin(a, b):
        return [round(a + (b - a) * i / max(1, n - 1)) for i in range(n)]
    if modelo == "linear":  # [Z1]
        rr = lin(8, 4) if forca else lin(12, 8)
        rir = lin(3, 1)
        return [{"fase": "linear", "zonas": [(r, r if forca else r + 2, q)]} for r, q in zip(rr, rir)]
    if modelo in ("ondulatoria", "ondulatória", "dup"):  # [Z2]
        rir = lin(3, 1)
        z = [(4, 6, None), (8, 10, None), (12, 15, None)] if not forca else [(3, 5, None), (6, 8, None), (8, 10, None)]
        return [{"fase": "ondulatória", "zonas": [(a, b, q) for a, b, _ in z]} for q in rir]
    if modelo == "blocos":  # [Z3] acumulação 50-70% → transmutação 75-90% → realização ≥90% (Lorenz 2015)
        na = max(1, round(n * 0.5))
        nt = max(1, n - na - 1) if n >= 3 else 0
        nr = n - na - nt
        out = [{"fase": "acumulação", "zonas": [(12, 15, 3 if i == 0 else 2)], "volume": 1.0} for i in range(na)]
        out += [{"fase": "transmutação", "zonas": [(5, 6, 2 if i == 0 else 1)], "volume": 0.8} for i in range(nt)]
        out += [{"fase": "realização", "zonas": [(2, 3, 1)], "volume": 0.6} for _ in range(nr)]  # volume -40% (Travis 2020)
        return out
    sys.exit(f"Modelo desconhecido: {modelo} (use linear, ondulatoria ou blocos)")


def gerar_mesociclo(aluno, modelo="linear", semanas=6, deload=True, inicio=None):
    A = aluno["aluno"]
    nivel = A.get("nivel", "intermediario").lower()
    nivel = "intermediario" if nivel.startswith("inter") else ("iniciante" if nivel.startswith("inic") else "avancado")
    objetivo = A.get("objetivo", "hipertrofia").lower()
    exs = {e["nome"]: dict(e) for e in aluno["exercicios"]}
    # 1RM de cada exercício: dado direto, ou estimado do teste (carga × reps + RIR) [A1]
    testes = {t["exercicio"]: t for t in aluno.get("testes", [])}
    for nome, e in exs.items():
        if not e.get("1rm") and nome in testes:
            t = testes[nome]
            e["1rm"] = estimar_1rm(t["carga"], t["reps"], t.get("rir", 0), e.get("tabela", "geral"))["1rm"]
            e["1rm_origem"] = f"estimado ({t['carga']} kg × {t['reps']} + RIR {t.get('rir', 0)}), tabela {_tab(e.get('tabela'))}"
        elif e.get("1rm"):
            e["1rm_origem"] = "informado"
    n_norm = semanas - 1 if deload else semanas
    esq = _esquema(modelo, objetivo, n_norm)
    divisao = aluno["divisao"]  # {"A": [nomes], "B": [...]}
    # séries por grupo: começo do nível [V1]-[V3]; rampa até metade da distância ao teto (operacional), máx +2/semana
    ini, teto = REGRAS["inicio_series"][nivel], REGRAS["teto_series"][nivel]
    fim = ini + (teto - ini) / 2.0
    vol_ini = aluno.get("volume_inicial", {})
    grupo_ex = {}
    for d, lst in divisao.items():
        for nome in lst:
            grupo_ex.setdefault(exs[nome]["grupo"], []).append((d, nome))
    plano_sem = []
    avisos = {}  # grupo → (maior alvo que não coube, nº de exercícios)
    hoje = datetime.date.fromisoformat(inicio) if inicio else datetime.date.today()
    seg = hoje - datetime.timedelta(days=hoje.weekday())
    for i in range(semanas):
        is_del = deload and i == semanas - 1
        e_s = esq[min(i, n_norm - 1)]
        vol_fator = e_s.get("volume", 1.0)
        alvo_grupo = ini + min((fim - ini) * i / max(1, n_norm - 1), 2 * i) if not is_del else None
        sessoes = {}
        series_grupo = {}
        for g, lista in grupo_ex.items():
            ini_g = float(vol_ini.get(g, ini))  # grupo pequeno recebe séries indiretas dos compostos (0,5 cada) [M1]
            alvo = (alvo_grupo * ini_g / ini) * vol_fator if not is_del else None
            n_ex = len(lista)
            for j, (d, nome) in enumerate(lista):
                if is_del:
                    base = plano_sem[0]["series_por_exercicio"][nome]
                    s = max(1, math.ceil(base * REGRAS["deload_fator_series"]))
                else:
                    tot = int(round(alvo))
                    s = max(2, tot // n_ex + (1 if j < tot % n_ex else 0))  # pelo menos 2 séries por exercício [V2]
                    s = min(s, REGRAS["max_series_exercicio"])
                series_grupo[g] = series_grupo.get(g, 0) + s
                sessoes.setdefault(d, {})[nome] = s
            if not is_del and series_grupo[g] < int(round(alvo)) - 1:
                avisos[g] = (max(avisos.get(g, (0, 0))[0], int(round(alvo))), n_ex)
        linhas = {}
        spe = {}
        for k, (d, lst) in enumerate(divisao.items()):
            linhas[d] = []
            for nome in lst:
                e = exs[nome]
                zonas = e_s["zonas"]
                rmin, rmax, rir = zonas[k % len(zonas)]
                if e.get("isolado") and rmax <= 6:  # isolado não vai a 2-6 repetições (opção operacional)
                    rmin, rmax = 8, 10
                if is_del:
                    z0 = esq[0]["zonas"][k % len(esq[0]["zonas"])]
                    rmin, rmax = z0[0], z0[1]
                    rir = (z0[2] if z0[2] is not None else 3) + REGRAS["deload_rir_extra"]
                s = sessoes[d][nome]
                spe[nome] = s
                carga, pct, ext = (None, None, False)
                if e.get("1rm"):
                    carga, pct, ext = carga_para(e["1rm"], rmin, rir, e.get("tabela", "geral"), e.get("incremento_kg", 1.0))
                else:
                    pct, ext = pct_para_reps(rmin + rir, e.get("tabela", "geral"))
                    pct = round(pct, 1)
                desc = e.get("descanso_s") or (180 if e.get("principal") and rmax <= 6 else (120 if e.get("principal") else 90))
                linhas[d].append({
                    "exercicio": nome, "grupo": e["grupo"], "series": s,
                    "reps": f"{rmin}" if rmin == rmax else f"{rmin} a {rmax}",
                    "reps_min": rmin, "reps_max": rmax, "rir": rir, "pct_1rm": pct, "carga_kg": carga,
                    "descanso_s": desc, "obs": e.get("obs", ""), "extrapolado": ext,
                })
        plano_sem.append({
            "semana": i + 1, "inicio": (seg + datetime.timedelta(weeks=i)).isoformat(),
            "tipo": "deload" if is_del else "normal", "fase": "deload" if is_del else e_s["fase"],
            "series_por_grupo": series_grupo, "series_por_exercicio": spe, "sessoes": linhas,
        })
    # exercícios com faixa/RIR da semana 1 (o "decidir" usa como alvo)
    s1 = {l["exercicio"]: l for d in plano_sem[0]["sessoes"].values() for l in d}
    exercicios = []
    for nome, e in exs.items():
        l = s1.get(nome, {})
        exercicios.append({**e, "reps": [l.get("reps_min", 8), l.get("reps_max", 12)], "rir": l.get("rir", 2)})
    return {
        "aluno": A, "modelo": modelo, "objetivo": objetivo, "nivel": nivel, "semanas": plano_sem,
        "exercicios": exercicios, "divisao": divisao, "nomes_dias": aluno.get("nomes_dias", {}), "rir_padrao": 2,
        "volume_alvo": {"inicio": ini, "teto": teto, "regra": CITA["V"]},
        "check_in_cargas_url": aluno.get("check_in_cargas_url", ""), "avisos": [f"{g}: a rampa pede até {v} séries/semana, mas {n} exercício(s) com até {REGRAS['max_series_exercicio']} séries não comportam; acrescente um exercício para esse grupo" for g, (v, n) in sorted(avisos.items())],
        "fonte": PROTOCOLO, "gerado_em": datetime.date.today().isoformat(),
    }

# ===================================================================================================== SAÍDA


def _t(linhas, cab):
    larg = [max(len(str(c)) for c in col) for col in zip(cab, *linhas)] if linhas else [len(c) for c in cab]
    f = lambda r: "  ".join(str(c).ljust(w) for c, w in zip(r, larg))
    return "\n".join([f(cab), f(["-" * w for w in larg])] + [f(r) for r in linhas])


def cmd_1rm(a):
    r = estimar_1rm(a.carga, a.reps, a.rir, a.tabela)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    print(f"Carga {r['carga']:g} kg × {r['reps']:g} repetições + RIR {r['rir']:g} = {r['reps_ate_falha']:g} até a falha (tabela '{r['tabela']}')")
    print(f"  1RM estimado (Nuzzo 2024, média de grupo): {r['1rm']} kg  (≈ {r['pct_1rm']}% do 1RM nessa série)")
    print(f"  faixa entre pessoas (±1 desvio-padrão de repetições): {r['faixa_1rm'][0]} a {r['faixa_1rm'][1]} kg")
    print(f"  conferência (fórmulas clássicas, sem fonte na base): Epley {r['epley']} kg · Brzycki {r['brzycki']} kg")
    for av in r["avisos"]:
        print("  AVISO:", av)
    print("  Estimativa, não teste: confira na 1ª semana pelo RIR relatado. [A1] [A2]")


def cmd_tabela(a):
    if a.aluno:
        d = ler_json(a.aluno)
        testes = {t["exercicio"]: t for t in d.get("testes", [])}
        linhas = []
        for e in d["exercicios"]:
            rm = e.get("1rm")
            if not rm and e["nome"] in testes:
                t = testes[e["nome"]]
                rm = estimar_1rm(t["carga"], t["reps"], t.get("rir", 0), e.get("tabela"))["1rm"]
            if not rm:
                continue
            faixa = e.get("reps") or [8, 12]
            rir = e.get("rir", 2)
            cg, pct, ext = carga_para(rm, faixa[0], rir, e.get("tabela"), e.get("incremento_kg", 1))
            linhas.append([e["nome"], f"{rm:g}", f"{faixa[0]}-{faixa[-1]}", rir, f"{pct:g}%", f"{cg:g}" + (" *" if ext else "")])
        print(_t(linhas, ["Exercício", "1RM est.", "Reps", "RIR", "%1RM", "Carga kg"]))
        print("\n* abaixo de 70% 1RM: extrapolação da tabela. Carga = %1RM para (reps mínimas + RIR) [A1] [I1]/[I2].")
        return
    if not a.rm:
        sys.exit("Informe --rm (1RM em kg) ou --aluno <arquivo.json>.")
    linhas = []
    for reps in range(a.reps_de, a.reps_ate + 1):
        cg, pct, ext = carga_para(a.rm, reps, a.rir, a.tabela, a.incremento)
        linhas.append([reps, a.rir, f"{pct:g}%", f"{cg:g}" + (" *" if ext else "")])
    print(f"1RM {a.rm:g} kg · tabela '{_tab(a.tabela)}' · incremento {a.incremento:g} kg\n")
    print(_t(linhas, ["Reps", "RIR alvo", "%1RM", "Carga kg"]))
    print("\n* extrapolação (abaixo de 70% 1RM). [A1] Nuzzo 2024")


def cmd_volume(a):
    plano = ler_json(a.plano) if a.plano else {}
    res = resumo_semanal(ler_registro(a.registro), mapa_exercicios(plano))
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    grupos = sorted({g for W in res.values() for g in W["grupos"]})
    print("Séries de trabalho por grupo e semana (RIR ≤ 4; grupo secundário conta 0,5) [M1]\n")
    print(_t([[g] + [f"{res[w]['grupos'].get(g, 0):g}" for w in res] for g in grupos], ["Grupo"] + [f"S{w}" for w in res]))
    exs = sorted({n for W in res.values() for n in W["exercicios"]})
    print("\nVolume load (kg) e 1RM estimado por exercício [M1] [M2]\n")
    print(_t([[n] + [(f"{res[w]['exercicios'][n]['vl']:g} / {res[w]['exercicios'][n]['e1rm'] or '-'}" if n in res[w]["exercicios"] else "-") for w in res] for n in exs],
             ["Exercício (VL / 1RM est.)"] + [f"S{w}" for w in res]))
    sem = sum(W["series_sem_rir"] for W in res.values())
    if sem:
        print(f"\nAVISO: {sem} série(s) sem RIR registrado contadas como série de trabalho.")
    print("\nCompare volume load só no mesmo exercício e na mesma faixa de repetições (Schoenfeld 2016). [M1]")


def cmd_decidir(a):
    plano = ler_json(a.plano)
    prox_del = None
    if a.semana_plano:
        sems = plano.get("semanas", [])
        nxt = next((s for s in sems if s["semana"] == a.semana_plano + 1), None)
        prox_del = bool(nxt and nxt.get("tipo") == "deload")
    r = decidir(plano, ler_registro(a.registro), ler_checkin(a.checkin), a.semana, a.nivel, prox_del)
    if a.saida:
        gravar_json(r, a.saida)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    print(f"Semana {r['semana']} · nível {r['nivel']} · prontidão {r['prontidao']} (anterior {r['prontidao_anterior']})\n")
    for al in r["alertas"]:
        print("!!", al, "\n")
    for d in r["exercicios"]:
        print(f"{d['decisao']:<15} {d['exercicio']}  — {d['motivo']}")
        if d["sugestao"]:
            print(f"{'':<15} → {d['sugestao']}")
    print("\nPor grupo muscular (volume semanal):")
    for g in r["grupos"]:
        print(f"{g['decisao']:<15} {g['grupo']}  — {g['motivo']}")
    print("\n" + r["aviso"])
    if a.saida:
        print(f"\nGravado: {a.saida}")


def cmd_mesociclo(a):
    aluno = ler_json(a.aluno)
    p = gerar_mesociclo(aluno, a.modelo, a.semanas, not a.sem_deload, a.inicio)
    nome = p["aluno"].get("nome", "aluno")
    saida = a.saida or os.path.join(pasta_treinos(nome), f"mesociclo-{a.modelo}-{p['gerado_em']}.json")
    gravar_json(p, saida)
    print(f"Mesociclo {a.modelo} · {a.semanas} semanas · nível {p['nivel']} · objetivo {p['objetivo']}\n")
    grupos = sorted({g for s in p["semanas"] for g in s["series_por_grupo"]})
    print(_t([[f"S{s['semana']}", s["fase"]] + [s["series_por_grupo"].get(g, 0) for g in grupos] for s in p["semanas"]], ["Sem", "Fase"] + grupos))
    print("\nSemana 1 (cargas pela tabela de Nuzzo para reps mínimas + RIR):")
    for d, lst in p["semanas"][0]["sessoes"].items():
        print(f"\n  Treino {d}")
        for l in lst:
            print(f"    {l['exercicio']:<32} {l['series']}× {l['reps']:<7} RIR {l['rir']}  {l['pct_1rm']}%  {l['carga_kg'] if l['carga_kg'] is not None else '-'} kg  desc {l['descanso_s']}s")
    for av in p["avisos"]:
        print("AVISO:", av)
    print(f"\nGravado: {saida}")


def cmd_regras(_a):
    print(f"Regras do motor — cada uma tem a linha no Protocolo:\n  {PROTOCOLO}\n")
    for k, v in CITA.items():
        print(f"  {v}")
    print("\nConstantes (mude aqui e no Protocolo):")
    for k, v in REGRAS.items():
        print(f"  {k} = {v}")


def main():
    ap = argparse.ArgumentParser(description="Motor de treino do SOUTO TREINADOR (prescrição e volume × desempenho).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("1rm", help="estima o 1RM de carga × repetições (+ RIR)")
    p.add_argument("--carga", type=float, required=True)
    p.add_argument("--reps", type=float, required=True)
    p.add_argument("--rir", type=float, default=0, help="repetições que ainda sobravam (0 = falha)")
    p.add_argument("--tabela", default="geral", help="geral | supino | legpress")
    p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_1rm)
    p = sub.add_parser("tabela", help="tabela de cargas por repetição e RIR, ou por exercício do arquivo do aluno")
    p.add_argument("--rm", type=float)
    p.add_argument("--aluno")
    p.add_argument("--rir", type=float, default=2)
    p.add_argument("--reps-de", type=int, default=3)
    p.add_argument("--reps-ate", type=int, default=15)
    p.add_argument("--tabela", default="geral")
    p.add_argument("--incremento", type=float, default=1.0)
    p.set_defaults(f=cmd_tabela)
    p = sub.add_parser("volume", help="séries por grupo e volume load por semana")
    p.add_argument("--registro", required=True, help="registro de cargas (.json ou .csv)")
    p.add_argument("--plano", help="mesociclo ou arquivo do aluno (para saber o grupo de cada exercício)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_volume)
    p = sub.add_parser("decidir", help="PROGREDIR / MANTER / REDUZIR VOLUME / DELOAD")
    p.add_argument("--plano", required=True)
    p.add_argument("--registro", required=True)
    p.add_argument("--checkin")
    p.add_argument("--semana", type=int, help="semana a decidir (padrão: a última do registro)")
    p.add_argument("--semana-plano", type=int, help="semana do mesociclo correspondente (para saber se a próxima é deload)")
    p.add_argument("--nivel")
    p.add_argument("--saida", help="grava a decisão em JSON")
    p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_decidir)
    p = sub.add_parser("mesociclo", help="gera o mesociclo com rampa de volume e deload")
    p.add_argument("--aluno", required=True)
    p.add_argument("--modelo", default="linear", choices=["linear", "ondulatoria", "blocos"])
    p.add_argument("--semanas", type=int, default=6)
    p.add_argument("--sem-deload", action="store_true")
    p.add_argument("--inicio", help="AAAA-MM-DD (segunda da semana 1)")
    p.add_argument("--saida", help="padrão: %%USERPROFILE%%/SoutoTreinador/Alunos/<nome>/Treinos/")
    p.set_defaults(f=cmd_mesociclo)
    p = sub.add_parser("regras", help="lista as regras e as linhas do Protocolo")
    p.set_defaults(f=cmd_regras)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
