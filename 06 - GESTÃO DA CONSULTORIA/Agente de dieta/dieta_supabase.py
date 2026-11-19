#!/usr/bin/env python3
"""Ponte do agente de dieta com o Supabase (sem pacote externo; chave service_role lida da pasta privada).

Uso:
  python dieta_supabase.py pacote "Ana Exemplo"      (ou AL-3) lê do Supabase tudo o que o agente precisa e grava
                                                    pacote.json na pasta do aluno (fora do repositório e do OneDrive)
  python dieta_supabase.py salvar "<plano.json>" [--refazer] [--sem-assinatura]
      confere o plano (calcular_plano.py) e grava no Supabase: a Dieta v{n} (kcal, macros, fase, gasto e o resto),
      as Refeições, os Itens de suplementação, o Relatório de abertura (da v2 em diante) e a Entrega em RASCUNHO,
      com o PDF e o JSON no bucket privado "entregas", a impressão digital (SHA-256) do PDF, o texto de envio e o
      link do WhatsApp.
      --refazer: a versão já existe e ainda não foi aprovada pelo RT: apaga a antiga e grava de novo.
      --sem-assinatura: deixa salvar um PDF sem a imagem da assinatura do RT (só para teste; não envie assim).

Depois de salvar, o caminho é sempre: RASCUNHO → (Jorge revisa) → APROVAÇÃO DO RT → (o RT aprova) → ENVIAR → ENVIADO,
no Painel ST. O banco não deixa uma dieta ir para ENVIAR sem a aprovação do RT.

Pasta dos alunos: %USERPROFILE%\\SoutoTreinador\\Alunos\\<nome do aluno> (dado de aluno nunca entra no repositório).
Chave: %USERPROFILE%\\SoutoTreinador\\privado\\supabase.env (o Claude nunca lê nem mostra).
"""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.parse

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "comum"))
sys.path.insert(0, AQUI)
import calcular_plano  # noqa: E402
import config_st  # noqa: E402
import supabase_st  # noqa: E402

FASE_TXT = {"deficit": "déficit", "manutencao": "manutenção", "pausa": "pausa planejada", "superavit": "superávit"}
DIA_CK = {"segunda": "segunda-feira", "terça": "terça-feira", "quarta": "quarta-feira", "quinta": "quinta-feira",
          "sexta": "sexta-feira", "sábado": "sábado", "domingo": "domingo"}
TEXTOS_ENVIO = {  # usados enquanto não houver texto APROVADO em mensagens_prontas (dono = Dieta)
    "primeiro": "Oi, {primeiro_nome}! Seu primeiro plano alimentar está aqui, prescrito pelo nosso nutricionista responsável "
                "técnico. Comece pela página 'Como usar o seu plano'. Ele vale até {validade}, e o seu check-in chega toda "
                "{dia_checkin}. Qualquer dúvida, me chama aqui.",
    "novo": "Oi, {primeiro_nome}! Seu plano alimentar novo está pronto, vale de {inicio} a {validade}. Na primeira página tem "
            "o resumo do último mês e as metas que combinamos. Qualquer dúvida, me chama aqui.",
    "repeticao": "Oi, {primeiro_nome}! Vamos seguir com o mesmo cardápio até {validade}. Na primeira página está explicado o "
                 "porquê e o que vamos focar agora. Se quiser trocar algum alimento, me fala.",
}
_DB = None


def db():
    global _DB
    if _DB is None:
        try:
            _DB = supabase_st.Supabase()
        except supabase_st.ErroSupabase as e:
            sys.exit(str(e))
    return _DB


def hoje():
    return datetime.date.today()


def idade(nasc):
    if not nasc:
        return None
    n, h = datetime.date.fromisoformat(str(nasc)[:10]), hoje()
    return h.year - n.year - ((h.month, h.day) < (n.month, n.day))


def data_br(iso):
    return datetime.date.fromisoformat(str(iso)[:10]).strftime("%d/%m")


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def achar(quem):
    quem = quem.strip()
    if re.fullmatch(r"(?i)al-?\d+", quem):
        r = db().select("alunos", {"codigo": f"eq.AL-{re.sub(r'\D', '', quem)}"})
    else:
        r = db().select("alunos", {"nome": f"ilike.*{quem}*"})
    if not r:
        sys.exit(f"Não achei aluno com '{quem}'.")
    if len(r) > 1:
        sys.exit("Mais de um aluno com esse nome: " + " · ".join(f"{a['codigo']} {a['nome']}" for a in r))
    return r[0]


# ---------------- pacote (leitura) ----------------
def pacote(quem):
    a = achar(quem)
    aid = a["id"]
    por_aluno = {"aluno_id": f"eq.{aid}"}
    anam = {}
    for r in db().select("recebidos", {**por_aluno, "tipo": "in.(anamnese,anamnese_treino)", "order": "recebido_em.desc"}):
        anam.setdefault(r["tipo"], {"recebido_em": r["recebido_em"], "texto": r.get("respostas_texto") or "",
                                    "respostas": (r.get("respostas") or {}).get("respostas")})
    cks = db().select("checkins", {**por_aluno, "order": "semana_inicio.desc"})
    campos_ck = ["semana_inicio", "quinzenal", "peso_semana", "dias_no_plano", "dias_leve", "dias_grande", "dias_nao_lembro",
                 "score", "fome", "saciedade", "sono_horas", "sono_qualidade", "estresse", "agua_l", "treinos_feitos",
                 "cintura_cm", "quadril_cm", "dor_lesao_nova", "troca_pedida", "dificuldade", "pergunta", "nivel", "alertas"]
    checkins = [{k: c.get(k) for k in campos_ck if c.get(k) not in (None, "", [], False)} for c in cks]
    fotos = next(({"semana": c["semana_inicio"], **{k: v for k, v in (c.get("respostas") or {}).items() if str(k).lower().startswith("foto") and v}}
                  for c in cks if any(str(k).lower().startswith("foto") and v for k, v in (c.get("respostas") or {}).items())), None)
    medidas = [{"data": m["data"], "peso": m.get("peso_kg"), "cintura": m.get("cintura_cm"), "quadril": m.get("quadril_cm"),
                "origem": m.get("origem")} for m in db().select("medidas", {**por_aluno, "order": "data.asc"})]
    marc = {}
    for m in db().select("marcadores", {**por_aluno, "order": "data_coleta.asc"}):
        marc.setdefault(m["nome"], []).append({"data": m.get("data_coleta"), "valor": m.get("valor"), "unidade": m.get("unidade"),
                                               "faixa": m.get("faixa_texto"), "situacao": m.get("situacao")})
    marc = {k: v[-3:] for k, v in marc.items()}
    entregas = {e["id"]: e for e in db().select("entregas", {**por_aluno, "tipo": "eq.dieta"})}
    dietas = []
    for d in db().select("dietas", {**por_aluno, "order": "versao.asc"}):
        e = entregas.get(d.get("entrega_id")) or {}
        dietas.append({"id": d["id"], "versao": d["versao"], "tipo": d["tipo_versao"], "status": e.get("status"),
                       "inicio": e.get("inicio"), "validade": e.get("validade") or (
                           (datetime.date.fromisoformat(e["inicio"]) + datetime.timedelta(days=e.get("dias_validade") or 30)).isoformat()
                           if e.get("inicio") else None),
                       "fase": d["fase"], "kcal_dia": d["kcal_dia"], "proteina_g": d["proteina_g"], "carboidrato_g": d["carboidrato_g"],
                       "gordura_g": d["gordura_g"], "get": d.get("get_kcal"), "get_calibrado": d.get("get_calibrado_kcal"),
                       "agua_ml_por_kg": d.get("agua_ml_por_kg")})
    em_uso = None
    if a.get("dieta_em_uso_id"):
        d = db().um("dietas", a["dieta_em_uso_id"])
        if d:
            em_uso = {k: v for k, v in d.items() if v not in (None, "", []) and k != "plano_json"}
            em_uso["refeicoes"] = db().select("refeicoes", {"dieta_id": f"eq.{d['id']}", "order": "ordem.asc"})
            em_uso["suplementos"] = db().select("itens_suplementacao", {"dieta_id": f"eq.{d['id']}"})
            em_uso["plano_json"] = d.get("plano_json")
    diario = [{"id": x["id"], "data": x["data"], "tipo": x["tipo"], "status": x["status"], "conduta_proposta": x.get("conduta_proposta"),
               "conduta_decidida": x.get("conduta_decidida"), "envolve_dieta": x.get("envolve_dieta"),
               "texto": (x.get("texto_final") or x.get("texto_proposto") or "")[:1500]}
              for x in db().select("diario", {**por_aluno, "order": "data.desc", "limit": "3"})]
    msgs = {m.get("codigo") or m["nome"]: m["texto"] for m in db().select("mensagens_prontas", {"dono": "eq.Dieta", "status": "eq.APROVADO"})}

    # blocos prontos para o montar_plano.py
    validade_uso = next((d["validade"] for d in dietas if em_uso and d["id"] == em_uso["id"]), None)
    inicio = max(hoje() + datetime.timedelta(days=1), datetime.date.fromisoformat(validade_uso[:10])) if validade_uso \
        else hoje() + datetime.timedelta(days=1)
    anterior_json = (em_uso or {}).get("plano_json") if isinstance((em_uso or {}).get("plano_json"), dict) else {}
    documento = {
        "ficticio": "FICTÍCIO" in (a.get("observacoes") or "").upper(),
        "aluno_nome": a["nome"], "primeiro_nome": a.get("primeiro_nome") or a["nome"].split(" ")[0],
        "sexo": a.get("sexo") or "", "linha": "gastro" if a.get("linha") == "gastro" else "emagrecimento",
        "tem_treino": bool(a.get("tem_treino")),
        "treino": (anterior_json.get("documento") or {}).get("treino") or {"dias": [], "horario": ""},
        "inicio": inicio.isoformat(), "validade": (inicio + datetime.timedelta(days=30)).isoformat(),
        "dia_checkin": DIA_CK.get(a.get("dia_checkin") or "", ""), "mostrar_numeros": bool(a.get("mostrar_numeros_pdf")),
        "modelo": a.get("modelo_pdf") or "a", "data_assinatura": hoje().isoformat(),
    }
    enviados = [d for d in dietas if d["status"] == "ENVIADO" and d["inicio"]]
    planos_evol = [{"versao": d["versao"], "inicio": d["inicio"][:10],
                    "fim": enviados[i + 1]["inicio"][:10] if i + 1 < len(enviados) else None, "fase": d["fase"],
                    "kcal_dia": d["kcal_dia"], "proteina_g": d["proteina_g"], "carboidrato_g": d["carboidrato_g"], "gordura_g": d["gordura_g"]}
                   for i, d in enumerate(enviados)]
    por_semana = {}
    for c in reversed(checkins):
        if c.get("semana_inicio"):
            por_semana[c["semana_inicio"][:10]] = c
    cks_asc = [por_semana[k] for k in sorted(por_semana)]
    pesos = [{"data": m["data"][:10], "kg": float(m["peso"])} for m in medidas if m.get("peso")]
    esperados = None
    if enviados:
        semanas = max(1, (hoje() - datetime.date.fromisoformat(enviados[0]["inicio"][:10])).days // 7)
        esperados = semanas // 2 if cks_asc and cks_asc[-1].get("quinzenal") else semanas
    evolucao = {
        "periodo": {"inicio": pesos[0]["data"] if pesos else None, "fim": pesos[-1]["data"] if pesos else None},
        "peso_inicial_kg": pesos[0]["kg"] if pesos else None,
        "constancia": {"checkins": {"feitos": len(cks_asc), "esperados": max(esperados or 0, len(cks_asc))}} if cks_asc else {},
        "planos": planos_evol, "peso": pesos,
        "adesao": [{"semana": c["semana_inicio"][:10], "dias_no_plano": c.get("dias_no_plano"), "score": c.get("score")}
                   for c in cks_asc if c.get("score") is not None],
    }
    if a.get("tem_treino"):  # cargas: a maior de cada semana, nos exercícios com carga
        sessoes = {s["id"]: s["data"] for s in db().select("sessoes", por_aluno)}
        series = {}
        for s in db().select("series", por_aluno):
            data, carga = sessoes.get(s["sessao_id"]), s.get("maior_carga")
            if data and carga is not None:
                p = series.setdefault(s["exercicio_nome"], {})
                p[data] = max(float(carga), p.get(data, 0))
        series = sorted(series.items(), key=lambda kv: -len(kv[1]))[:4]
        if series:
            evolucao["treino"] = {"unidade": "kg", "series": [{"nome": n, "pontos": [{"data": d, "valor": v} for d, v in sorted(p.items())]}
                                                              for n, p in series if len(p) >= 2]}
            semanas_t = db().select("semanas_treino", {**por_aluno, "order": "semana_inicio.asc"})
            if semanas_t:
                evolucao.setdefault("constancia", {})["treinos"] = {
                    "feitos": sum((w.get("completas") or 0) + (w.get("parciais") or 0) for w in semanas_t),
                    "planejados": sum(w.get("planejadas") or 0 for w in semanas_t)}
    altura = a.get("altura_cm")
    ficha = {k: a.get(k) for k in ("nome", "codigo", "status", "etapa_entrada", "linha", "objetivo", "cidade", "sexo", "nascimento",
                                   "tem_treino", "dia_checkin", "mostrar_numeros_pdf", "modelo_pdf", "observacoes")
             if a.get(k) not in (None, "", [], False)}
    ficha.update({"id": aid, "idade": idade(a.get("nascimento")), "altura_cm": altura, "telefone": a.get("telefone")})
    peso_atual = pesos[-1]["kg"] if pesos else None
    tendencia = round(sum(p["kg"] for p in pesos[-2:]) / len(pesos[-2:]), 1) if pesos else None
    saida = {
        "_aviso": "Dado de aluno (LGPD, dado de saúde). Fica só nesta pasta, fora do repositório e do OneDrive. Não copie para o projeto.",
        "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
        "ficha": ficha, "peso_atual_kg": peso_atual, "peso_tendencia_kg": tendencia,
        "anamnese": anam.get("anamnese"), "anamnese_treino": anam.get("anamnese_treino"),
        "checkins_recentes": checkins[:8], "fotos_mais_recentes": fotos, "medidas": medidas, "marcadores": marc,
        "dietas": dietas, "dieta_em_uso": em_uso, "diario_recente": diario,
        "proxima_versao": max([d["versao"] or 0 for d in dietas] or [0]) + 1,
        "textos_de_envio_aprovados": msgs, "documento": documento, "evolucao": evolucao,
    }
    caminho = os.path.join(config_st.pasta_do_aluno(a["nome"]), "pacote.json")
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(saida, fh, ensure_ascii=False, indent=1, default=str)
    print(f"{a['nome']} · {a.get('linha')} · {a.get('sexo') or '?'} · {ficha['idade']} anos · altura {altura or '— (sem anamnese)'} cm"
          f" · peso atual {peso_atual} kg (tendência {tendencia})")
    print(f"Anamnese: {'sim' if anam.get('anamnese') else 'NÃO'} · check-ins: {len(checkins)} · medidas: {len(medidas)}"
          f" · marcadores: {', '.join(marc) or '—'}")
    print("Dietas: " + (" · ".join(f"v{d['versao']} {d['status']} {d['kcal_dia']} kcal" for d in dietas) or "nenhuma"))
    print(f"Próxima versão: v{saida['proxima_versao']} · início sugerido {documento['inicio']}")
    print("Pacote:", caminho)


# ---------------- salvar (gravação) ----------------
def linha_item(i):
    partes = [i["alimento"], i.get("medida_caseira") or "",
              f"{i['gramas']:g} {i.get('unidade', 'g')}" if i.get("gramas") not in (None, "") else "",
              i.get("preparo") or "", i.get("grupo_substituicao") or i.get("categoria") or ""]
    return " · ".join(p for p in partes if p)


def salvar(caminho, refazer=False, sem_assinatura=False):
    with open(caminho, encoding="utf-8") as fh:
        dados = json.load(fh)
    json_mudou_em = os.path.getmtime(caminho)
    res, msgs, _ = calcular_plano.conferir(dados, gravar=True)
    for r in dados["plano"].get("refeicoes", []):
        r.pop("_fibra_g", None), r.pop("_saturada_g", None)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)
    if res == "erro" or (res == "trava" and not dados["plano"].get("justificativa_rt")):
        calcular_plano.imprimir(res, msgs, {}, dados["plano"])
        sys.exit("\nNão salvei: corrija os erros (ou, na trava, registre a justificativa escrita do RT) e rode de novo.")
    D, P, R = dados["documento"], dados["plano"], dados.get("relatorio") or {}
    n = P["versao"]
    a = achar(P["aluno_id"])
    aid = a["id"]

    ja = db().select("dietas", {"aluno_id": f"eq.{aid}", "versao": f"eq.{n}"})
    if ja:
        ent = db().um("entregas", ja[0]["entrega_id"]) if ja[0].get("entrega_id") else None
        status = (ent or {}).get("status")
        if not refazer:
            sys.exit(f"A Dieta v{n} de {a['nome']} já existe ({status}). Use --refazer para trocar uma que ainda não foi aprovada pelo RT.")
        if status not in ("RASCUNHO", "APROVACAO_RT", "DESCARTADO", None):
            sys.exit(f"A Dieta v{n} já está {status}: aprovada pelo RT ou enviada não é trocada. Faça a v{n + 1}.")
        if ent:
            db().apagar("entregas", ent["id"])
        db().apagar("dietas", ja[0]["id"])
        print(f"v{n} antiga ({status}) apagada.")

    pasta_aluno = os.path.dirname(os.path.abspath(caminho))
    base = f"Plano alimentar v{n} - {D['primeiro_nome']} - {D['inicio']}"
    pdf, html_doc = os.path.join(pasta_aluno, base + ".pdf"), os.path.join(pasta_aluno, base + ".html")
    if not os.path.exists(pdf):
        sys.exit(f"Falta o PDF: {pdf}\nGere antes: python template/montar_plano.py \"{caminho}\"")
    if os.path.getmtime(pdf) < json_mudou_em - 5:
        print("aviso: o PDF é mais velho que o JSON; se mudou número depois do PDF, gere o PDF de novo.")
    if os.path.exists(html_doc):
        with open(html_doc, encoding="utf-8") as fh:
            sem_img = "class='assinatura-falta'" in fh.read()
        if sem_img and not sem_assinatura:
            sys.exit("O PDF saiu SEM a imagem da assinatura do RT (falta assinatura-rt.png na pasta privada).\n"
                     "Ponha a imagem lá, gere o PDF de novo e salve. (Só para teste: --sem-assinatura.)")
    nome_json = f"Plano v{n} - {config_st.nome_de_arquivo(D['aluno_nome'])} - {D['inicio']}.json"
    copia_json = os.path.join(pasta_aluno, nome_json)
    if os.path.abspath(copia_json) != os.path.abspath(caminho):
        with open(copia_json, "w", encoding="utf-8") as fh:
            json.dump(dados, fh, ensure_ascii=False, indent=1)
    destino = f"alunos/{aid}/dieta-v{n}-{D['inicio']}"
    db().enviar_arquivo(pdf, destino + ".pdf", "application/pdf")
    db().enviar_arquivo(copia_json, destino + ".json", "application/json")
    impressao = sha256(pdf)

    conf = P.get("conferencia") or {}
    dieta = db().inserir("dietas", {
        "aluno_id": aid, "versao": n, "tipo_versao": P["tipo_versao"], "plano_anterior_id": P.get("plano_anterior_id"),
        "fase": P["fase"], "get_kcal": P.get("get_kcal"), "get_metodo": P.get("get_metodo"),
        "get_calibrado_kcal": P.get("get_calibrado_kcal"), "fator_atividade": P.get("fator_atividade"),
        "peso_usado_kg": P.get("peso_usado_kg"), "data_peso": P.get("data_peso"), "kcal_dia": P["kcal_dia"],
        "proteina_g": P["proteina_g"], "carboidrato_g": P["carboidrato_g"], "gordura_g": P["gordura_g"],
        "fibra_g": P.get("fibra_g"), "meta_agua_l": P.get("meta_agua_l"), "agua_ml_por_kg": P.get("agua_ml_por_kg"),
        "livre_prevista": bool(P.get("livre_prevista")), "livre_por_semana": P.get("livre_por_semana") if P.get("livre_prevista") else None,
        "livre_teto_kcal": P.get("livre_teto_kcal") if P.get("livre_prevista") else None,
        "o_que_muda": "\n".join(P.get("o_que_muda") or []) or ("Primeiro plano." if n == 1 else None),
        "conferencia": conf.get("resultado"), "mensagens_conferencia": "\n".join(conf.get("mensagens") or []) or "sem avisos",
        "justificativa_rt": P.get("justificativa_rt"), "mostrar_numeros": bool(D.get("mostrar_numeros")),
        "plano_json": dados, "json_path": destino + ".json", "diario_id": P.get("diario_id"),
        "gerado_por": P.get("gerado_por") or "Claude (/montar-dieta)",
    })
    did = dieta["id"]
    grupos = {g["grupo"]: g for g in P.get("substituicoes", [])}
    refs = []
    for i, r in enumerate(P["refeicoes"], 1):
        usados = [grupos[g] for g in dict.fromkeys(it.get("grupo_substituicao") for it in r["itens"]) if g in grupos]
        trocas = "\n".join(f"{g.get('nome_exibicao') or g['grupo']}: " + " | ".join(linha_item(o) for o in [g["base"]] + g.get("equivalentes", []))
                           for g in usados)
        refs.append({"dieta_id": did, "ordem": i, "nome_exibicao": r["nome_exibicao"], "refeicao_padrao": r.get("refeicao_padrao"),
                     "horario": r.get("horario"), "kcal": r.get("kcal"), "proteina_g": r.get("proteina_g"),
                     "carboidrato_g": r.get("carboidrato_g"), "gordura_g": r.get("gordura_g"),
                     "itens": "\n".join(linha_item(it) for it in r["itens"]), "substituicoes": trocas,
                     "tipo_dia": r.get("tipo_dia") or "todos"})
    if refs:
        db().inserir("refeicoes", refs)
    supl = [{"dieta_id": did, "suplemento": s["suplemento"], "dose": s.get("dose"), "unidade": s.get("unidade"),
             "medida_caseira": s.get("medida_caseira"), "quando": s.get("quando"), "para_que": s.get("para_que"),
             "motivo_tecnico": s.get("motivo_tecnico"), "situacao": s.get("situacao"),
             "desde": D["inicio"] if s.get("situacao") == "novo" else s.get("desde"), "cuidados": s.get("cuidados")}
            for s in P.get("suplementacao") or []]
    supl_ids = [x["id"] for x in db().inserir("itens_suplementacao", supl)] if supl else []

    rel_id = None
    if any(R.get(k) for k in ("acertos", "atencao", "melhorar", "metas", "por_que_manter")):
        rec = R.get("recapitulacao") or {}
        rel_id = db().inserir("relatorios", {
            "aluno_id": aid, "dieta_id": did, "tipo": "Abertura do plano", "status": "RASCUNHO",
            "titulo": f"Abertura do plano · {D['primeiro_nome']} · {D['inicio'][:7]}",
            "acertos": "\n".join(R.get("acertos") or []), "atencao": "\n".join(R.get("atencao") or []),
            "melhorar": "\n".join(R.get("melhorar") or [R.get("por_que_manter") or ""]),
            "resumo": "\n".join((rec.get("feito") or []) + [("Não atingido: " + t) for t in rec.get("nao_atingido") or []]),
            "proximos_passos": "\n".join(f"{m.get('tipo', '')}: {m.get('texto', '')}" for m in R.get("metas") or []),
            "numeros": dados.get("evolucao") or {}})["id"]

    tipo_txt = "primeiro" if P["tipo_versao"] == "primeiro" else "repeticao" if P["tipo_versao"] == "repeticao" else "novo"
    texto = P.get("texto_envio") or TEXTOS_ENVIO[tipo_txt].format(
        primeiro_nome=D["primeiro_nome"], inicio=data_br(D["inicio"]), validade=data_br(D["validade"]),
        dia_checkin=D.get("dia_checkin") or "semana")
    fone = re.sub(r"\D", "", str(a.get("telefone") or ""))
    link = f"https://wa.me/{fone}?text={urllib.parse.quote(texto, safe='')}" if fone else None
    if not fone:
        print("aviso: a ficha não tem telefone; a Entrega sai sem o link do WhatsApp.")
    agora = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    ent = db().inserir("entregas", {
        "aluno_id": aid, "tipo": "dieta", "status": "RASCUNHO", "titulo": f"Dieta v{n} · {D['primeiro_nome']}", "versao": n,
        "dieta_id": did, "relatorio_id": rel_id, "inicio": D["inicio"], "dias_validade": P.get("dias_validade") or 30,
        "pdf_path": destino + ".pdf", "pdf_nome": base + ".pdf", "pdf_sha256": impressao, "json_path": destino + ".json",
        "texto_envio": texto, "link_whatsapp": link, "origem": "agente de dieta", "pdf_gerado_em": agora,
    })
    db().atualizar("dietas", did, {"entrega_id": ent["id"]})
    for s in supl_ids:
        db().atualizar("itens_suplementacao", s, {"entrega_id": ent["id"]})
    print(f"Salvo no Supabase · {D['aluno_nome']} · Dieta v{n} ({FASE_TXT[P['fase']]}, {P['kcal_dia']} kcal, P {P['proteina_g']} · "
          f"C {P['carboidrato_g']} · G {P['gordura_g']}) · conferência: {conf.get('resultado')}")
    print(f"  Entrega em RASCUNHO (início previsto {data_br(D['inicio'])}, validade {data_br(D['validade'])}); "
          f"PDF no bucket privado, impressão digital {impressao[:12]}…")
    print(f"  {len(P['refeicoes'])} refeições · {len(supl)} suplemento(s)" + (" · relatório de abertura em RASCUNHO" if rel_id else ""))
    print("  Próximo passo, no Painel ST → Aprovações: Jorge revisa e manda para o RT; o RT aprova; aí ENVIAR → ENVIADO.")


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 3 and sys.argv[1] == "pacote":
        pacote(" ".join(sys.argv[2:]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "salvar":
        salvar(sys.argv[2], "--refazer" in sys.argv, "--sem-assinatura" in sys.argv)
    else:
        print(__doc__)
