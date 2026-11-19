#!/usr/bin/env python3
"""Painel ST: o painel da consultoria Souto Treinador rodando no seu PC, lendo e gravando no Supabase.

Uso: duplo clique no atalho "Painel ST" da área de trabalho (criado por criar_atalho.ps1), que roda
  pythonw painel_st.py --app : servidor sem janela, o painel abre numa janela de aplicativo (Chrome ou Edge) e o
  servidor desliga sozinho ~1,5 min depois de a última janela fechar.
  Para testes: python painel_st.py [--porta 8787] [--sem-abrir]  (fica ligado até fechar o console)
  Demonstração sem Supabase: python painel_st.py --demo   (dados fictícios de demo/dados-demo.json; nada é gravado)
  PIN do RT (o RT digita, uma vez): python painel_st.py --definir-pin-rt

Regras:
- Só escuta no próprio PC (127.0.0.1): ninguém de fora acessa. Os pedidos que gravam exigem o cabeçalho X-Painel.
- Dado de aluno só passa pela memória (1 minuto de cache); não vai para arquivo nem para o console. A única exceção é
  o PDF da entrega, que fica na pasta do aluno (%USERPROFILE%\\SoutoTreinador\\Alunos\\<nome>), fora do repositório.
- O painel não decide nada clínico: os botões só fazem as transições combinadas, com segundo toque para confirmar.
- Dieta, suplementação e receituário só vão para ENVIAR depois da APROVAÇÃO DO RT (nutricionista). O banco também trava.
- A chave service_role vem de %USERPROFILE%\\SoutoTreinador\\privado\\supabase.env e nunca vai para o navegador.
"""
import concurrent.futures
import datetime
import hashlib
import hmac
import http.server
import json
import os
import re
import socket
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import webbrowser

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
GESTAO = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(GESTAO, "comum"))
import config_st  # noqa: E402
import supabase_st  # noqa: E402

WEB = os.path.join(AQUI, "web")
FONTES = os.path.join(GESTAO, "Agente de dieta", "template", "fontes")
DEMO_JSON = os.path.join(AQUI, "demo", "dados-demo.json")
TTL = 60
CACHE, TRAVA = {}, threading.Lock()
VIDA = {"ultimo": time.time(), "fechou": 0.0}
FECHAR_APOS = 90
DB = None  # Supabase ou Demo (main)
REQUER_RT = {"dieta", "suplementacao", "receituario"}
TIPOS = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".woff2": "font/woff2", ".png": "image/png", ".svg": "image/svg+xml", ".json": "application/json", ".pdf": "application/pdf"}
ROT_STATUS_ALUNO = {"entrada": "Entrada", "ativo": "Ativo", "pausado": "Pausado", "renovacao": "Renovação", "encerrado": "Encerrado"}
ROT_LINHA = {"emagrecimento": "Emagrecimento", "hipertrofia": "Hipertrofia", "saude": "Saúde", "performance": "Performance", "gastro": "Gastro"}
ROT_ETAPA_LEAD = {"novo": "Novo", "em_conversa": "Em conversa", "proposta": "Proposta", "fechou": "Fechou", "perdido": "Perdido"}
ROT_SECAO = {"urgente": "Urgente", "para_hoje": "Para hoje", "proximos_dias": "Próximos dias"}
ROT_TIPO_ENTREGA = {"dieta": "Dieta", "treino": "Treino", "suplementacao": "Suplementação", "receituario": "Receituário",
                    "relatorio": "Relatório", "material": "Material", "recibo": "Recibo", "outro": "Outro"}
ROT_STATUS_REC = {"NOVO": "NOVO", "SEM_DONO": "SEM DONO", "EM_ANALISE": "EM ANÁLISE", "PARA_REVISAO": "PARA REVISÃO"}
ROT_RECEBIDO = {"anamnese": "Anamnese", "anamnese_treino": "Anamnese de treino", "checkin_semanal": "Check-in semanal",
                "checkin_quinzenal": "Check-in quinzenal", "checkin_cargas": "Check-in de cargas", "exame": "Exame",
                "foto": "Foto", "mensagem": "Mensagem", "outro": "Outro"}


# ---------------- leitura (com cache) ----------------
def agora():
    return datetime.datetime.now().astimezone()


def hoje():
    return agora().date()


def d(iso):
    try:
        return datetime.date.fromisoformat(str(iso)[:10]) if iso else None
    except ValueError:
        return None


def lista(tabela, params=None, fresco=False):
    chave = (tabela, json.dumps(params or {}, sort_keys=True))
    with TRAVA:
        if not fresco and chave in CACHE and time.time() - CACHE[chave][0] < TTL:
            return CACHE[chave][1]
    linhas = DB.select(tabela, params)
    with TRAVA:
        CACHE[chave] = (time.time(), linhas)
    return linhas


def limpar_cache():
    with TRAVA:
        CACHE.clear()


def varios(pedidos, fresco=False):
    """Busca várias tabelas em paralelo (4 de cada vez)."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futuros = {k: ex.submit(lista, *args, fresco=fresco) for k, args in pedidos.items()}
        return {k: f.result() for k, f in futuros.items()}


def iniciais(nome):
    partes = [p for p in re.split(r"\s+", nome or "") if p and p[0].isalpha()]
    return ((partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")) if partes else "?").upper()


def mapa_alunos(alunos):
    return {a["id"]: {"id": a["id"], "nome": a.get("nome") or "Sem nome", "codigo": a.get("codigo"),
                      "primeiro": a.get("primeiro_nome") or (a.get("nome") or "").split(" ")[0],
                      "iniciais": iniciais(a.get("nome"))} for a in alunos}


def quem(aid, mp):
    return mp.get(aid, {"id": aid, "nome": "—", "codigo": None, "primeiro": "—", "iniciais": "?"}) if aid else None


def score_de(c):
    if c.get("score") is not None:
        return c["score"]
    no, lv, gr = (c.get("dias_no_plano") or 0), (c.get("dias_leve") or 0), (c.get("dias_grande") or 0)
    return round((no * 100 + lv * 50) / (no + lv + gr)) if no + lv + gr else None


def validade_de(e):
    if e.get("validade"):
        return e["validade"]
    ini = d(e.get("inicio"))
    return (ini + datetime.timedelta(days=e.get("dias_validade") or 30)).isoformat() if ini else None


def etiqueta(e):
    if e.get("status") != "ENVIADO":
        return ""
    if e.get("fim_real"):
        return "substituído"
    v = d(validade_de(e))
    if not v:
        return ""
    return "vencido" if v < hoje() else "vencendo" if (v - hoje()).days <= 5 else "vigente"


def wa(fone, texto):
    fone = re.sub(r"\D", "", str(fone or ""))
    return f"https://wa.me/{fone}?text={urllib.parse.quote(texto or '', safe='')}" if fone else None


def faltando(a, ultimo):
    if a.get("status") not in ("ativo", "renovacao"):
        return None
    u = d(ultimo)
    if not u or (hoje() - u).days > 14:
        return "check-in há mais de 14 dias"
    if (hoje() - u).days > 8:
        return "check-in há mais de 8 dias"
    return None


# ---------------- telas ----------------
ABERTOS_ENTREGA = "in.(RASCUNHO,APROVACAO_RT,ENVIAR)"
ABERTOS_RECEBIDO = "in.(NOVO,SEM_DONO,EM_ANALISE,PARA_REVISAO)"


def tela_inicio(fresco=False):
    ontem = (hoje() - datetime.timedelta(days=1)).isoformat()
    b = varios({
        "alu": ("alunos",), "lem": ("lembretes", {"feito": "eq.false"}),
        "dia": ("diario", {"status": "in.(RASCUNHO,EM_REVISAO)"}),
        "ent": ("entregas", {"status": ABERTOS_ENTREGA}),
        "env": ("envios", {"status": "in.(PARA_APROVAR,APROVADO)"}),
        "rec": ("recebidos", {"status": ABERTOS_RECEBIDO}),
        "ck": ("checkins", {"order": "semana_inicio.desc"}),
        "med": ("medidas", {"order": "data.asc"}),
        "con": ("consultas", {"data_hora": f"gte.{ontem}", "order": "data_hora.asc"}),
        "pag": ("pagamentos",), "lead": ("leads",), "ctr": ("contratos",), "meta": ("metas",),
    }, fresco)
    mp = mapa_alunos(b["alu"])
    aprovar = aprov_itens(b, mp)
    urg = [l for l in b["lem"] if l.get("secao") == "urgente"]
    rec_urg = [r for r in b["rec"] if r.get("urgente")]
    if urg:
        l = urg[0]
        destaque = {"tipo": "urgente", "titulo": l.get("titulo"), "texto": l.get("texto_pronto") or "Fale com o aluno ainda hoje e registre o contato.",
                    "aluno": quem(l.get("aluno_id"), mp), "acao": {"acao": "lembrete_feito", "id": l["id"], "rotulo": "Registrar contato"}}
    elif rec_urg:
        r = rec_urg[0]
        destaque = {"tipo": "urgente", "titulo": r.get("titulo"), "texto": "Chegou com sinal de alerta. Abra a ficha e fale com o aluno ainda hoje.",
                    "aluno": quem(r.get("aluno_id"), mp), "acao": None}
    else:
        prox = proximas_consultas(b["con"], mp)[:1]
        destaque = ({"tipo": "consulta", "titulo": f"Próximo horário: {prox[0]['tipo_txt']} · {prox[0]['aluno']['primeiro'] if prox[0]['aluno'] else ''}",
                     "texto": f"{prox[0]['quando_txt']}. {prox[0]['alerta'] or 'Tudo pronto.'}", "aluno": prox[0]["aluno"], "acao": None}
                    if prox else {"tipo": "calmo", "titulo": "Nada urgente agora", "texto": "Nenhum alarme aberto. Bom momento para revisar as aprovações e os leads.",
                                  "aluno": None, "acao": None})
    pesos = {}
    for m in b["med"]:
        if m.get("aluno_id") and m.get("peso_kg") is not None:
            pesos.setdefault(m["aluno_id"], []).append(float(m["peso_kg"]))
    vistos, cks = set(), []
    for c in b["ck"]:
        aid = c.get("aluno_id")
        if not aid or aid in vistos:
            continue
        vistos.add(aid)
        a = next((x for x in b["alu"] if x["id"] == aid), {})
        cks.append({"aluno": quem(aid, mp), "semana": c.get("semana_inicio"), "score": score_de(c),
                    "dias": [c.get("dias_no_plano") or 0, c.get("dias_leve") or 0, c.get("dias_grande") or 0],
                    "peso": c.get("peso_semana"), "linha": ROT_LINHA.get(a.get("linha"), ""), "nivel": c.get("nivel"),
                    "treinos": c.get("treinos_feitos"), "pesos": (pesos.get(aid) or [])[-8:]})
    limite = hoje() - datetime.timedelta(days=14)
    scores = [score_de(c) for c in b["ck"] if score_de(c) is not None and (d(c.get("semana_inicio")) or limite) >= limite]
    ativos = [a for a in b["alu"] if a.get("status") in ("ativo", "renovacao")]
    meta = b["meta"][0] if b["meta"] else {}
    ultimo_ck = {}
    for c in b["ck"]:
        ultimo_ck.setdefault(c.get("aluno_id"), c.get("semana_inicio"))
    lem_por = {}
    for l in b["lem"]:
        lem_por.setdefault(l.get("aluno_id"), []).append(l.get("secao"))
    gente = []
    for a in b["alu"]:
        if a.get("status") == "encerrado":
            continue
        estado = "urg" if "urgente" in lem_por.get(a["id"], []) else ("rev" if faltando(a, ultimo_ck.get(a["id"])) else "ok")
        gente.append({**mp[a["id"]], "estado": estado, "status": ROT_STATUS_ALUNO.get(a.get("status"))})
    quentes = [l for l in b["lead"] if l.get("etapa") in ("novo", "em_conversa", "proposta")]
    rt = [x for x in aprovar if x["tipo"] == "rt"]
    return {
        "hora": agora().hour,
        "contadores": {"aprovar": len(aprovar), "rt": len(rt), "urgentes": len(urg) + len(rec_urg),
                       "hoje": len([l for l in b["lem"] if l.get("secao") in ("urgente", "para_hoje")]), "recebidos": len(b["rec"])},
        "destaque": destaque, "aprovar": aprovar[:5], "checkins": cks[:6],
        "operacao": {"adesao": round(sum(scores) / len(scores)) if scores else None, "ativos": len(ativos), "alunos": len(b["alu"]),
                     "leads": len(quentes), "renovacoes": len([c for c in b["ctr"] if c.get("status") == "em_renovacao"]),
                     "meta_alvo": meta.get("alvo")},
        "agenda": proximas_consultas(b["con"], mp)[:3], "financeiro": financeiro(b["pag"], resumo=True),
        "gente": {"alunos": gente[:8], "leads": [{"id": l["id"], "nome": l.get("nome"), "iniciais": iniciais(l.get("nome")),
                                                   "etapa": ROT_ETAPA_LEAD.get(l.get("etapa"))} for l in quentes][:4]},
    }


def aprov_itens(b, mp):
    itens = []
    for x in b["dia"]:
        rt = bool(x.get("envolve_dieta"))
        itens.append({"tipo": "rt" if rt else "diario", "id": x["id"], "titulo": f"Diário · {x.get('tipo') or 'análise'}",
                      "aluno": quem(x.get("aluno_id"), mp), "status": x.get("status"), "status_txt": status_txt(x.get("status")),
                      "sub": f"conduta proposta: {x.get('conduta_proposta') or '—'}" + (" · mexe na dieta: decisão do RT" if rt else ""),
                      "texto": x.get("texto_final") or x.get("texto_proposto") or "",
                      "acoes": ["diario_aprovar_rt" if rt else "diario_aprovar"]})
    alunos = {a["id"]: a for a in b.get("alu", [])}
    for x in b["ent"]:
        st, tipo = x.get("status"), x.get("tipo")
        requer = tipo in REQUER_RT
        a = alunos.get(x.get("aluno_id"), {})
        link = x.get("link_whatsapp") or wa(a.get("telefone"), x.get("texto_envio"))
        if st == "RASCUNHO":
            acoes = ["entrega_para_rt" if requer else "entrega_aprovar"]
        elif st == "APROVACAO_RT":
            acoes = ["entrega_aprovar_rt", "entrega_devolver_rt"]
        else:
            acoes = ["entrega_enviada"]
        sub = f"{ROT_TIPO_ENTREGA.get(tipo, tipo)} · {status_txt(st)}"
        if requer and x.get("rt_aprovado_em"):
            sub += f" · RT aprovou em {str(x['rt_aprovado_em'])[8:10]}/{str(x['rt_aprovado_em'])[5:7]}"
        itens.append({"tipo": "rt" if st == "APROVACAO_RT" else "entrega", "id": x["id"], "titulo": x.get("titulo") or "Entrega",
                      "aluno": quem(x.get("aluno_id"), mp), "sub": sub, "status": st, "status_txt": status_txt(st),
                      "texto": x.get("texto_envio") or "", "whatsapp": link, "tem_pdf": bool(x.get("pdf_path") or x.get("pdf_nome")),
                      "requer_rt": requer, "acoes": acoes})
    for x in b["env"]:
        st = x.get("status")
        itens.append({"tipo": "envio", "id": x["id"], "titulo": x.get("titulo") or "Mensagem", "aluno": quem(x.get("aluno_id"), mp),
                      "sub": f"mensagem · {status_txt(st)}", "status": st, "status_txt": status_txt(st), "texto": x.get("texto_final") or "",
                      "whatsapp": wa(x.get("telefone"), x.get("texto_final")),
                      "acoes": ["envio_aprovar" if st == "PARA_APROVAR" else "envio_enviado"]})
    ordem = {"rt": 0, "entrega": 1, "diario": 2, "envio": 3}
    return sorted(itens, key=lambda i: (ordem.get(i["tipo"], 9), 0 if "requer_rt" in i else 1))


def status_txt(st):
    return {"APROVACAO_RT": "APROVAÇÃO DO RT", "PARA_APROVAR": "PARA APROVAR", "EM_REVISAO": "EM REVISÃO"}.get(st, st or "")


def proximas_consultas(cons, mp):
    saida = []
    for c in cons:
        if c.get("status") in ("cancelada", "remarcada", "realizada", "faltou"):
            continue
        try:
            dt = datetime.datetime.fromisoformat(str(c.get("data_hora")).replace("Z", "+00:00")).astimezone() if c.get("data_hora") else None
        except ValueError:
            dt = None
        dias = (dt.date() - hoje()).days if dt else None
        if dias is not None and dias < 0:
            continue
        rot = "hoje" if dias == 0 else "amanhã" if dias == 1 else (dt.strftime("%d/%m") if dt else "")
        tipo_txt = {"primeira": "Primeira consulta", "retorno": "Retorno", "renovacao": "Renovação", "avaliacao": "Avaliação",
                    "treino_presencial": "Treino presencial"}.get(c.get("tipo"), "Consulta")
        saida.append({"id": c["id"], "titulo": c.get("titulo"), "tipo_txt": tipo_txt, "status": (c.get("status") or "").capitalize(),
                      "aluno": quem(c.get("aluno_id"), mp), "hora": dt.strftime("%Hh%M") if dt else "", "dia": rot,
                      "data": dt.date().isoformat() if dt else None, "quando_txt": f"{rot} às {dt.strftime('%Hh%M')}" if dt else "",
                      "link": c.get("link_reuniao"), "alerta": c.get("alerta") or ""})
    return saida


def financeiro(pags, resumo=False):
    h = hoje()
    mes = h.strftime("%Y-%m")
    val = lambda p: float(p.get("valor_bruto") or 0)  # noqa: E731
    rec_mes = sum(val(p) for p in pags if p.get("situacao") == "pago" and str(p.get("pago_em") or "")[:7] == mes)
    a_receber = sum(val(p) for p in pags if p.get("situacao") == "previsto" and d(p.get("vencimento"))
                    and h <= d(p.get("vencimento")) <= h + datetime.timedelta(days=7))
    vencidos = [p for p in pags if p.get("situacao") == "vencido" or (p.get("situacao") == "previsto" and d(p.get("vencimento")) and d(p.get("vencimento")) < h)]
    meses = []
    for i in range(5, -1, -1):
        ano, m = h.year, h.month - i
        while m <= 0:
            ano, m = ano - 1, m + 12
        chave = f"{ano}-{m:02d}"
        meses.append({"mes": chave, "valor": sum(val(p) for p in pags if p.get("situacao") == "pago" and str(p.get("pago_em") or "")[:7] == chave)})
    saida = {"recebido_mes": rec_mes, "a_receber_7d": a_receber, "vencidos": sum(val(p) for p in vencidos), "meses": meses}
    if not resumo:
        def linha(p):
            return {"id": p["id"], "titulo": p.get("descricao"), "valor": val(p), "situacao": (p.get("situacao") or "").capitalize(),
                    "vencimento": p.get("vencimento"), "pago_em": p.get("pago_em"), "forma": p.get("forma")}
        saida["vencidos_lista"] = [linha(p) for p in vencidos]
        saida["proximos"] = sorted([linha(p) for p in pags if p.get("situacao") == "previsto" and d(p.get("vencimento")) and d(p.get("vencimento")) >= h],
                                   key=lambda x: x["vencimento"] or "")[:12]
        saida["pagos"] = sorted([linha(p) for p in pags if p.get("situacao") == "pago"], key=lambda x: x["pago_em"] or "", reverse=True)[:12]
    return saida


def tela_hoje(fresco=False):
    b = varios({"alu": ("alunos",), "lem": ("lembretes", {"feito": "eq.false", "order": "prazo.asc"}),
                "rec": ("recebidos", {"status": ABERTOS_RECEBIDO, "order": "recebido_em.desc"}),
                "con": ("consultas", {"data_hora": f"gte.{hoje().isoformat()}", "order": "data_hora.asc"})}, fresco)
    mp = mapa_alunos(b["alu"])
    secoes = {"Urgente": [], "Para hoje": [], "Próximos dias": []}
    for l in b["lem"]:
        secoes.setdefault(ROT_SECAO.get(l.get("secao"), "Próximos dias"), []).append({
            "id": l["id"], "titulo": l.get("titulo"), "motivo": l.get("motivo"), "prazo": l.get("prazo"),
            "atrasado": bool(d(l.get("prazo")) and d(l.get("prazo")) < hoje()), "minutos": l.get("minutos_estimados"),
            "texto": l.get("texto_pronto"), "aluno": quem(l.get("aluno_id"), mp)})
    recs = []
    for r in b["rec"]:
        prazo = None
        try:
            prazo = (datetime.datetime.fromisoformat(str(r.get("recebido_em")).replace("Z", "+00:00")) + datetime.timedelta(hours=48)).astimezone()
        except ValueError:
            pass
        recs.append({"id": r["id"], "titulo": r.get("titulo"), "tipo": ROT_RECEBIDO.get(r.get("tipo"), r.get("tipo")),
                     "status": ROT_STATUS_REC.get(r.get("status"), r.get("status") or ""), "prazo": prazo.date().isoformat() if prazo else None,
                     "atrasado": bool(prazo and prazo < agora()), "aluno": quem(r.get("aluno_id"), mp)})
    return {"secoes": secoes, "recebidos": recs, "consultas": [c for c in proximas_consultas(b["con"], mp) if c["dia"] == "hoje"]}


def tela_aprovacoes(fresco=False):
    b = varios({"alu": ("alunos",), "dia": ("diario", {"status": "in.(RASCUNHO,EM_REVISAO)"}),
                "ent": ("entregas", {"status": ABERTOS_ENTREGA}), "env": ("envios", {"status": "in.(PARA_APROVAR,APROVADO)"})}, fresco)
    return {"itens": aprov_itens(b, mapa_alunos(b["alu"])), "pin_rt": bool(DB.rt_pin_hash), "rt": config_st.RT}


def tela_alunos(fresco=False):
    b = varios({"alu": ("alunos", {"order": "nome.asc"}), "ck": ("checkins", {"order": "semana_inicio.desc"})}, fresco)
    ultimo = {}
    for c in b["ck"]:
        ultimo.setdefault(c.get("aluno_id"), c)
    saida = []
    for a in b["alu"]:
        c = ultimo.get(a["id"], {})
        saida.append({"id": a["id"], "nome": a.get("nome"), "codigo": a.get("codigo"), "iniciais": iniciais(a.get("nome")),
                      "status": ROT_STATUS_ALUNO.get(a.get("status")), "linha": ROT_LINHA.get(a.get("linha")),
                      "faltando": faltando(a, c.get("semana_inicio")), "ultimo_checkin": c.get("semana_inicio"),
                      "score": score_de(c) if c else None, "peso": c.get("peso_semana"), "tem_dieta": a.get("tem_dieta")})
    return {"alunos": saida}


def tela_aluno(aid, fresco=False):
    a = DB.um("alunos", aid)
    if not a:
        raise ValueError("aluno não encontrado")
    f = {"aluno_id": f"eq.{aid}"}
    b = varios({"med": ("medidas", {**f, "order": "data.asc"}), "ck": ("checkins", {**f, "order": "semana_inicio.desc"}),
                "die": ("dietas", {**f, "order": "versao.desc"}), "ent": ("entregas", {**f, "order": "criado_em.desc"}),
                "lem": ("lembretes", {**f, "feito": "eq.false"}), "dia": ("diario", {**f, "order": "data.desc"}),
                "con": ("consultas", {**f, "order": "data_hora.desc"}), "ses": ("sessoes", f), "ser": ("series", f)}, fresco)
    ents = {e["id"]: e for e in b["ent"]}
    return {
        "id": aid, "nome": a.get("nome"), "codigo": a.get("codigo"), "iniciais": iniciais(a.get("nome")),
        "status": ROT_STATUS_ALUNO.get(a.get("status")), "linha": ROT_LINHA.get(a.get("linha")), "objetivo": a.get("objetivo"),
        "tem_treino": a.get("tem_treino"), "tem_dieta": a.get("tem_dieta"), "dia_checkin": a.get("dia_checkin"),
        "consentimento": bool(a.get("consentimento_lgpd_em")), "whatsapp": wa(a.get("telefone"), ""),
        "medidas": [{"data": m.get("data"), "peso": float(m["peso_kg"]) if m.get("peso_kg") is not None else None,
                     "cintura": m.get("cintura_cm")} for m in b["med"] if m.get("data")],
        "checkins": [{"semana": c.get("semana_inicio"), "score": score_de(c), "dias_no_plano": c.get("dias_no_plano"),
                      "treinos": c.get("treinos_feitos"), "peso": c.get("peso_semana"), "nivel": c.get("nivel")} for c in b["ck"][:10]],
        "dietas": [{"id": x["id"], "versao": x.get("versao"), "fase": {"deficit": "déficit", "manutencao": "manutenção", "pausa": "pausa",
                                                                        "superavit": "superávit"}.get(x.get("fase"), x.get("fase")),
                    "kcal": x.get("kcal_dia"), "p": x.get("proteina_g"), "c": x.get("carboidrato_g"), "g": x.get("gordura_g"),
                    "status": status_txt((ents.get(x.get("entrega_id")) or {}).get("status")),
                    "inicio": (ents.get(x.get("entrega_id")) or {}).get("inicio"), "validade": validade_de(ents.get(x.get("entrega_id")) or {}),
                    "em_uso": x["id"] == a.get("dieta_em_uso_id")} for x in b["die"]],
        "entregas": [{"id": x["id"], "titulo": x.get("titulo"), "tipo": ROT_TIPO_ENTREGA.get(x.get("tipo")), "status": x.get("status"),
                      "status_txt": status_txt(x.get("status")), "tem_pdf": bool(x.get("pdf_path") or x.get("pdf_nome")), "etiqueta": etiqueta(x),
                      "whatsapp": x.get("link_whatsapp") or wa(a.get("telefone"), x.get("texto_envio")), "texto": x.get("texto_envio") or "",
                      "rt": bool(x.get("rt_aprovado_em"))} for x in b["ent"][:12]],
        "lembretes": [{"id": l["id"], "titulo": l.get("titulo"), "secao": ROT_SECAO.get(l.get("secao")), "prazo": l.get("prazo")} for l in b["lem"]],
        "diario": [{"data": x.get("data"), "tipo": x.get("tipo"), "status": status_txt(x.get("status")),
                    "conduta": x.get("conduta_decidida") or x.get("conduta_proposta")} for x in b["dia"][:6]],
        "cargas": cargas(b["ses"], b["ser"]),
    }


def cargas(sessoes, series):
    """Evolução por exercício: a maior carga de cada semana (ou o total de repetições, nos de peso do corpo)."""
    datas = {s["id"]: s.get("data") for s in sessoes}
    out = {}
    for s in series:
        data = datas.get(s.get("sessao_id"))
        if not data:
            continue
        cs = [float(s[f"s{i}_carga"]) for i in range(1, 7) if s.get(f"s{i}_carga") is not None]
        rs = [int(s[f"s{i}_rep"]) for i in range(1, 7) if s.get(f"s{i}_rep") is not None]
        ponto = {"data": data, "valor": max(cs) if cs else sum(rs), "un": "kg" if cs else "rep", "reps": " ".join(map(str, rs))}
        semanas = out.setdefault(s.get("exercicio_nome") or "", {})
        if data not in semanas or ponto["valor"] > semanas[data]["valor"]:
            semanas[data] = ponto
    return {n: [v[k] for k in sorted(v)] for n, v in out.items() if n}


def tela_leads(fresco=False):
    leads = lista("leads", {"order": "entrou_em.desc"}, fresco)
    etapas = {v: [] for v in ROT_ETAPA_LEAD.values()}
    for l in leads:
        fu = d(l.get("proximo_followup"))
        etapas.setdefault(ROT_ETAPA_LEAD.get(l.get("etapa"), "Novo"), []).append({
            "id": l["id"], "nome": l.get("nome"), "iniciais": iniciais(l.get("nome")), "origem": l.get("origem"),
            "temperatura": (l.get("temperatura") or "").capitalize() or None, "problema": l.get("problema"),
            "linha": ROT_LINHA.get(l.get("linha_provavel")), "followup": l.get("proximo_followup"),
            "atrasado": bool(fu and fu < hoje() and l.get("etapa") not in ("fechou", "perdido")),
            "valor": l.get("valor_fechado"), "whatsapp": wa(l.get("telefone"), "")})
    return {"etapas": etapas}


def tela_financeiro(fresco=False):
    return financeiro(lista("pagamentos", None, fresco))


def tela_agenda(fresco=False):
    b = varios({"alu": ("alunos",), "con": ("consultas", {"data_hora": f"gte.{hoje().isoformat()}", "order": "data_hora.asc"})}, fresco)
    return {"consultas": proximas_consultas(b["con"], mapa_alunos(b["alu"]))[:40]}


def tela_sistema(fresco=False):
    ok, erro, ultimo = True, "", None
    try:
        DB.saude()
        r = DB.select("recebidos", {"origem": "eq.tally", "order": "recebido_em.desc", "limit": "1"})
        ultimo = r[0]["recebido_em"] if r else None
    except Exception as e:  # sem rede ou chave: o painel diz, não quebra
        ok, erro = False, str(e)[:200]
    return {"modo": DB.modo, "supabase_ok": ok, "erro": erro, "projeto": DB.url if DB.modo == "demo" else re.sub(r"^https://([a-z0-9]{4})[a-z0-9]*", r"https://\1…", DB.url),
            "ultimo_tally": ultimo, "assinatura_rt": bool(config_st.assinatura_rt()), "pin_rt": bool(DB.rt_pin_hash),
            "pasta_alunos": config_st.pasta_alunos().replace(os.path.expanduser("~"), "%USERPROFILE%"), "cache_s": TTL, "rt": config_st.RT, "agora": agora().isoformat(timespec="minutes")}


def tela_config(fresco=False):
    return {"saudacao": config_st.CFG.get("painel", {}).get("saudacao") or config_st.PROF["nome"].split()[0].upper(),
            "marca": config_st.MARCA["nome"], "modo": DB.modo, "rt": config_st.RT, "pin_rt": bool(DB.rt_pin_hash)}


# ---------------- ações (as únicas transições que o painel faz) ----------------
def conferir_pin(pin):
    """Com RT_PIN_HASH no supabase.env, a aprovação do RT pede o PIN dele (SHA-256 do PIN). Sem ele, vale o segundo toque."""
    if not DB.rt_pin_hash:
        return
    dado = hashlib.sha256(str(pin or "").encode("utf-8")).hexdigest()
    if not hmac.compare_digest(dado, DB.rt_pin_hash.lower()):
        raise ValueError("PIN do RT incorreto: nada foi aprovado")


def pdf_confere(e):
    """Se o PDF já está na pasta do aluno, a impressão digital tem que bater com a que foi salva."""
    if DB.modo == "demo" or not e.get("pdf_sha256"):
        return
    caminho = caminho_pdf_local(e)
    if caminho and os.path.isfile(caminho):
        with open(caminho, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h != e["pdf_sha256"]:
            raise ValueError("o PDF na pasta do aluno é diferente do que foi salvo: gere e salve de novo antes de aprovar")


def um_ou_erro(tabela, eid):
    x = DB.um(tabela, eid) if eid else None
    if not x:
        raise ValueError("registro não encontrado (atualize a tela)")
    return x


def acao(nome, eid, extra=None):
    extra = extra or {}
    agora_iso, hoje_iso = agora().isoformat(timespec="minutes"), hoje().isoformat()
    jorge = config_st.PROF["nome"]
    rt_nome = f"{config_st.RT['nome']} ({config_st.RT['registro']}) · Painel ST"
    if nome == "lembrete_feito":
        l = um_ou_erro("lembretes", eid)
        if l.get("feito"):
            return "já estava feito"
        DB.atualizar("lembretes", eid, {"feito": True, "feito_em": agora_iso})
        return "lembrete marcado como feito"
    if nome in ("diario_aprovar", "diario_aprovar_rt"):
        x = um_ou_erro("diario", eid)
        if x.get("status") not in ("RASCUNHO", "EM_REVISAO"):
            return f"nada feito: o diário está {status_txt(x.get('status'))}"
        if x.get("envolve_dieta") and nome != "diario_aprovar_rt":
            return "nada feito: esta conduta mexe na dieta e é aprovada pelo RT"
        if nome == "diario_aprovar_rt":
            conferir_pin(extra.get("pin"))
        DB.atualizar("diario", eid, {"status": "APROVADO", "aprovado_em": agora_iso, "aprovado_por": rt_nome if nome == "diario_aprovar_rt" else jorge})
        return "diário aprovado"
    if nome.startswith("entrega_"):
        e = um_ou_erro("entregas", eid)
        st, requer = e.get("status"), e.get("tipo") in REQUER_RT
        if nome == "entrega_para_rt":
            if st != "RASCUNHO" or not requer:
                return f"nada feito: a entrega está {status_txt(st)}"
            DB.atualizar("entregas", eid, {"status": "APROVACAO_RT", "aprovado_em": agora_iso, "aprovado_por": jorge})
            return "revisado: agora a entrega espera a APROVAÇÃO DO RT"
        if nome == "entrega_aprovar":
            if st != "RASCUNHO" or requer:
                return f"nada feito: {'esta entrega precisa do RT' if requer else 'a entrega está ' + status_txt(st)}"
            DB.atualizar("entregas", eid, {"status": "ENVIAR", "aprovado_em": agora_iso, "aprovado_por": jorge})
            return "aprovada: agora é só enviar"
        if nome == "entrega_aprovar_rt":
            if st != "APROVACAO_RT":
                return f"nada feito: a entrega está {status_txt(st)}"
            conferir_pin(extra.get("pin"))
            pdf_confere(e)
            DB.atualizar("entregas", eid, {"status": "ENVIAR", "rt_aprovado_em": agora_iso, "rt_aprovado_por": rt_nome,
                                           "rt_pdf_sha256": e.get("pdf_sha256"), "rt_observacao": extra.get("nota") or None})
            DB.inserir("aprovacoes_rt", {"entrega_id": eid, "decisao": "aprovado", "por": rt_nome, "pdf_sha256": e.get("pdf_sha256"),
                                         "observacao": extra.get("nota") or None})
            return "aprovada pelo RT: agora é só enviar"
        if nome == "entrega_devolver_rt":
            if st != "APROVACAO_RT":
                return f"nada feito: a entrega está {status_txt(st)}"
            conferir_pin(extra.get("pin"))
            DB.atualizar("entregas", eid, {"status": "RASCUNHO", "rt_observacao": extra.get("nota") or "devolvido pelo RT",
                                           "rt_aprovado_em": None, "rt_aprovado_por": None, "rt_pdf_sha256": None})
            DB.inserir("aprovacoes_rt", {"entrega_id": eid, "decisao": "devolvido", "por": rt_nome, "pdf_sha256": e.get("pdf_sha256"),
                                         "observacao": extra.get("nota") or None})
            return "devolvida pelo RT: volta para RASCUNHO (refazer e salvar de novo)"
        if nome == "entrega_enviada":
            if st != "ENVIAR":
                return f"nada feito: a entrega está {status_txt(st)}"
            if requer and not e.get("rt_aprovado_em"):
                return "nada feito: falta a aprovação do RT"
            inicio = e.get("inicio") or hoje_iso
            DB.atualizar("entregas", eid, {"status": "ENVIADO", "enviado_em": agora_iso, "inicio": inicio})
            a = DB.um("alunos", e["aluno_id"]) or {}
            campo, novo = ("dieta_em_uso_id", e.get("dieta_id")) if e.get("tipo") == "dieta" else \
                ("treino_em_uso_id", e.get("prescricao_treino_id")) if e.get("tipo") == "treino" else (None, None)
            if campo and novo:
                anterior = a.get(campo)
                if anterior and anterior != novo:
                    tabela = "dietas" if campo == "dieta_em_uso_id" else "prescricoes_treino"
                    ent_ant = (DB.um(tabela, anterior) or {}).get("entrega_id")
                    if ent_ant:
                        DB.atualizar("entregas", ent_ant, {"fim_real": inicio})
                DB.atualizar("alunos", a["id"], {campo: novo})
                return "enviado: o plano em uso foi trocado e o anterior foi fechado"
            return "marcado como enviado"
    if nome in ("envio_aprovar", "envio_enviado"):
        x = um_ou_erro("envios", eid)
        if nome == "envio_aprovar":
            if x.get("status") != "PARA_APROVAR":
                return f"nada feito: a mensagem está {status_txt(x.get('status'))}"
            DB.atualizar("envios", eid, {"status": "APROVADO", "aprovado_em": agora_iso})
            return "mensagem aprovada"
        if x.get("status") != "APROVADO":
            return f"nada feito: a mensagem está {status_txt(x.get('status'))}"
        DB.atualizar("envios", eid, {"status": "ENVIADO", "enviado_em": agora_iso})
        return "mensagem marcada como enviada"
    raise ValueError(f"ação desconhecida: {nome}")


def caminho_pdf_local(e):
    a = DB.um("alunos", e.get("aluno_id")) or {}
    sub = "Treino" if e.get("tipo") == "treino" else None
    pasta = config_st.pasta_do_aluno(a.get("nome") or "Sem aluno", sub, criar=False)
    nome = config_st.nome_de_arquivo(e.get("pdf_nome") or f"{e.get('titulo') or 'entrega'}.pdf")
    return os.path.join(pasta, nome if nome.lower().endswith(".pdf") else nome + ".pdf")


def pdf_local(eid):
    """O PDF da entrega na pasta do aluno no PC. Se ainda não estiver lá, baixa do bucket privado do Supabase."""
    e = um_ou_erro("entregas", eid)
    if not e or not (e.get("pdf_path") or e.get("pdf_nome")):
        raise ValueError("esta entrega não tem PDF")
    caminho = caminho_pdf_local(e)
    if not os.path.isfile(caminho) or not os.path.getsize(caminho):
        if DB.modo == "demo":
            raise ValueError("na demonstração não há PDF de verdade (os dados são fictícios)")
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        corpo = DB.baixar(e["pdf_path"])
        with open(caminho, "wb") as f:
            f.write(corpo)
    return caminho


def abrir_pasta(eid):
    subprocess.Popen(f'explorer /select,"{pdf_local(eid)}"')
    return "pasta aberta com o PDF selecionado: arraste para a conversa do WhatsApp"


def copiar_pdf(eid):
    caminho = pdf_local(eid)
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command",
                        f"Set-Clipboard -LiteralPath '{caminho.replace(chr(39), chr(39) * 2)}'"],
                       capture_output=True, timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode:
        raise RuntimeError("não consegui pôr o PDF na área de transferência")
    return "PDF copiado: na conversa do WhatsApp, aperte Ctrl+V para anexar"


TELAS = {"inicio": tela_inicio, "hoje": tela_hoje, "aprovacoes": tela_aprovacoes, "alunos": tela_alunos, "leads": tela_leads,
         "financeiro": tela_financeiro, "agenda": tela_agenda, "sistema": tela_sistema, "config": tela_config}


# ---------------- servidor ----------------
class Painel(http.server.BaseHTTPRequestHandler):
    server_version = "PainelST/1.0"

    def log_message(self, fmt, *args):  # sem log: nenhum dado de aluno vai para o console
        pass

    def _host_ok(self):
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        return host in ("127.0.0.1", "localhost") and self.client_address[0] == "127.0.0.1"

    def _json(self, codigo, dados):
        corpo = json.dumps(dados, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _arquivo(self, caminho, cache="no-cache"):
        if not os.path.isfile(caminho):
            self.send_error(404)
            return
        with open(caminho, "rb") as f:
            corpo = f.read()
        self.send_response(200)
        self.send_header("Content-Type", TIPOS.get(os.path.splitext(caminho)[1].lower(), "application/octet-stream"))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if not self._host_ok():
            return self.send_error(403)
        VIDA["ultimo"] = time.time()
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        fresco = q.get("fresco", ["0"])[0] == "1"
        try:
            if u.path.startswith("/api/"):
                nome = u.path[5:]
                if nome == "vivo":
                    return self._json(200, {"ok": True})
                if nome == "aluno":
                    return self._json(200, tela_aluno(q["id"][0], fresco))
                if nome == "pdf":  # o PDF da pasta do aluno, ou um link assinado de 10 min do bucket privado
                    eid = (q.get("id") or [""])[0]
                    e = (DB.um("entregas", eid) if eid else None) or {}
                    local = caminho_pdf_local(e) if e else None
                    if local and os.path.isfile(local):
                        return self._arquivo(local, "no-store")
                    url = DB.url_assinada(e["pdf_path"]) if e.get("pdf_path") else None
                    if not url:
                        return self._json(404, {"erro": "PDF não disponível" + (" na demonstração" if DB.modo == "demo" else "")})
                    self.send_response(302)
                    self.send_header("Location", url)
                    self.end_headers()
                    return
                if nome in TELAS:
                    return self._json(200, TELAS[nome](fresco))
                return self._json(404, {"erro": "rota desconhecida"})
            if u.path.startswith("/fontes/"):
                return self._arquivo(os.path.join(FONTES, os.path.basename(u.path)))
            if u.path == "/logo.png":
                return self._arquivo(config_st.logo("branco") or "")
            arq = os.path.basename(u.path) or "index.html"
            return self._arquivo(os.path.join(WEB, arq))
        except Exception as e:
            return self._json(500, {"erro": str(e)[:300]})

    def do_POST(self):
        if not self._host_ok() or self.headers.get("X-Painel") != "1":
            return self.send_error(403)
        if self.path == "/api/fechei":
            VIDA["fechou"] = time.time()
            return self._json(200, {"ok": True})
        VIDA["ultimo"] = time.time()
        try:
            tam = int(self.headers.get("Content-Length") or 0)
            if tam > 100_000:
                return self._json(413, {"ok": False, "erro": "pedido grande demais"})
            corpo = json.loads(self.rfile.read(tam) or b"{}")
            if self.path == "/api/acao":
                msg = acao(corpo.get("acao"), corpo.get("id"), {"pin": corpo.get("pin"), "nota": (corpo.get("nota") or "")[:500]})
                limpar_cache()
                return self._json(200, {"ok": not msg.startswith("nada feito"), "mensagem": msg, "erro": msg if msg.startswith("nada feito") else None})
            if self.path == "/api/atualizar":
                limpar_cache()
                return self._json(200, {"ok": True})
            if self.path in ("/api/abrir_pasta", "/api/copiar_pdf"):
                feito = abrir_pasta if self.path == "/api/abrir_pasta" else copiar_pdf
                return self._json(200, {"ok": True, "mensagem": feito(corpo.get("id"))})
            return self._json(404, {"erro": "rota desconhecida"})
        except Exception as e:
            return self._json(500, {"ok": False, "erro": str(e)[:300]})


class Servidor(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = sys.platform != "win32"

    def server_bind(self):
        if sys.platform == "win32":  # porta exclusiva: o segundo clique no atalho cai no "já está aberto"
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


def abrir_janela(endereco):
    """Janela de aplicativo (Chrome ou Edge com --app, no perfil de sempre: o WhatsApp Web segue logado)."""
    exe = config_st.chrome()
    if exe:
        subprocess.Popen([exe, f"--app={endereco}", "--window-size=1440,900"])
    else:
        webbrowser.open(endereco)


def vigiar(srv):
    while True:
        time.sleep(5)
        if VIDA["fechou"] > VIDA["ultimo"] and time.time() - VIDA["fechou"] > FECHAR_APOS:
            srv.shutdown()
            return


def avisar(msg):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, msg, "Painel ST", 0x10)
    except Exception:
        pass


def definir_pin_rt():
    """O RT digita o PIN dele (duas vezes, sem aparecer na tela); só o SHA-256 vai para o supabase.env."""
    import getpass
    env = config_st.ler_env()
    caminho = env["_arquivo"]
    if not os.path.isfile(caminho):
        sys.exit(f"Crie antes o {caminho} (guia 05, passo 4).")
    pin = getpass.getpass("PIN do RT (4 a 12 números; não aparece na tela): ")
    if not re.fullmatch(r"\d{4,12}", pin or ""):
        sys.exit("O PIN precisa ter de 4 a 12 números. Nada foi gravado.")
    if getpass.getpass("Repita o PIN: ") != pin:
        sys.exit("Os dois PINs não batem. Nada foi gravado.")
    linha = "RT_PIN_HASH=" + hashlib.sha256(pin.encode("utf-8")).hexdigest()
    with open(caminho, encoding="utf-8-sig") as f:
        linhas = [l.rstrip("\n") for l in f if not l.startswith("RT_PIN_HASH=")]
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas + [linha]) + "\n")
    print("PIN do RT gravado (só a impressão digital dele). Feche e abra o Painel ST de novo.")


def main():
    global DB
    if "--definir-pin-rt" in sys.argv:
        return definir_pin_rt()
    porta = int(config_st.CFG.get("painel", {}).get("porta") or 8787)
    if "--porta" in sys.argv:
        porta = int(sys.argv[sys.argv.index("--porta") + 1])
    demo = "--demo" in sys.argv
    DB = supabase_st.Demo(DEMO_JSON) if demo else supabase_st.Supabase()
    endereco = f"http://127.0.0.1:{porta}/"
    app = "--app" in sys.argv
    abrir = abrir_janela if app else webbrowser.open
    try:
        srv = Servidor(("127.0.0.1", porta), Painel)
    except OSError:  # já está aberto: só abre outra janela
        if "--sem-abrir" not in sys.argv:
            abrir(endereco)
        return
    threading.Thread(target=lambda: tela_inicio(), daemon=True).start()  # aquece o cache
    if app:
        threading.Thread(target=vigiar, args=(srv,), daemon=True).start()
    if "--sem-abrir" not in sys.argv:
        threading.Timer(0.8, lambda: abrir(endereco)).start()
    if sys.stdout:
        print(f"Painel ST {'(DEMONSTRAÇÃO, dados fictícios) ' if demo else ''}aberto em {endereco}  (feche esta janela para desligar)")
    srv.serve_forever()


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except Exception as e:
        if not sys.stdout:
            avisar(f"O Painel ST não abriu: {e}")
        else:
            print(f"O Painel ST não abriu: {e}")
        sys.exit(1)
