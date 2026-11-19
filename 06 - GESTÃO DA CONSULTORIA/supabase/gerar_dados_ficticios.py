#!/usr/bin/env python3
"""Gera os DADOS FICTÍCIOS de demonstração, numa fonte só, em dois formatos:
  - supabase/seed_ficticio.sql          (para carregar num projeto Supabase de TESTE, pelo SQL Editor)
  - Painel ST/demo/dados-demo.json      (para o `painel_st.py --demo`, sem Supabase)

Todos os nomes são inventados e marcados (Exemplo, Fictício, Teste...). Telefones usam o prefixo 55 00 9 0000-…,
que não existe. As datas são relativas a hoje (no SQL: current_date + n; no JSON: "@hoje+n"), então a demonstração
nunca envelhece.

Uso: python gerar_dados_ficticios.py
"""
import datetime
import json
import os
import sys
import uuid

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA_SQL = os.path.join(AQUI, "seed_ficticio.sql")
SAIDA_JSON = os.path.join(os.path.dirname(AQUI), "Painel ST", "demo", "dados-demo.json")
NS = uuid.UUID("5a0f0000-0000-4000-8000-00000000f1c7")


def uid(*partes):
    return str(uuid.uuid5(NS, "/".join(map(str, partes))))


class Dia:
    """Data relativa a hoje (n dias), com hora opcional."""
    def __init__(self, n, hora=None):
        self.n, self.hora = n, hora

    def json(self):
        return f"@hoje{self.n:+d}" + (f"T{self.hora}" if self.hora else "")

    def sql(self):
        base = f"(current_date {'+' if self.n >= 0 else '-'} {abs(self.n)})"
        return f"(({base} + time '{self.hora}') at time zone 'America/Sao_Paulo')" if self.hora else base


class SDia(Dia):
    """Data relativa à segunda-feira desta semana (n dias): check-ins e semanas de treino caem sempre numa segunda."""
    def json(self):
        return f"@semana{self.n:+d}"

    def sql(self):
        return f"(date_trunc('week', current_date)::date {'+' if self.n >= 0 else '-'} {abs(self.n)})"


def segunda(n):
    """Deslocamento (em dias) da segunda-feira de "n dias atrás", contado a partir da segunda desta semana."""
    return -7 * ((-n + 6) // 7)


T = {}  # tabela -> linhas


def add(tabela, linha, so_json=None):
    """so_json: campos calculados pelo banco (colunas geradas) que a demo precisa já prontos."""
    T.setdefault(tabela, []).append((linha, so_json or {}))
    return linha


# ------------------------------------------------------------------ base
add("configuracoes", {"id": uid("cfg", 1), "chave": "demo", "valor": "sim", "descricao": "Dados fictícios de demonstração"})
META = add("metas", {"id": uid("meta"), "nome": "100 alunos ativos", "alvo": 100})["id"]
PRECOS = [add("tabela_precos", {"id": uid("preco", i), "nome": n, "periodicidade": p, "valor": v, "duracao_dias": d, "inclui_dieta": dieta})["id"]
          for i, (n, p, v, d, dieta) in enumerate([("Treino online · mensal", "mensal", 297, 30, False),
                                                   ("Treino + dieta (RT) · trimestral", "trimestral", 1290, 90, True),
                                                   ("Treino + dieta (RT) · semestral", "semestral", 2340, 180, True)])]

# ------------------------------------------------------------------ alunos (todos inventados)
ALUNOS = [
    # chave, nome, sexo, linha, status, tem_dieta, tem_treino, objetivo, dia_checkin
    ("ana", "Ana Exemplo", "F", "emagrecimento", "ativo", True, True, "Perder gordura mantendo a força no treino", "segunda"),
    ("bruno", "Bruno Fictício", "M", "hipertrofia", "ativo", False, True, "Ganhar massa muscular", "segunda"),
    ("carla", "Carla Demonstração", "F", "emagrecimento", "renovacao", True, True, "Emagrecer e melhorar o condicionamento", "terça"),
    ("diego", "Diego Teste", "M", "performance", "ativo", True, True, "Melhorar o tempo na corrida de 10 km", "segunda"),
    ("elisa", "Elisa Modelo", "F", "saude", "entrada", False, True, "Começar a treinar com segurança", None),
    ("fabio", "Fábio Simulado", "M", "emagrecimento", "pausado", False, True, "Voltar à rotina de treino", "quarta"),
]
A = {}
for i, (k, nome, sexo, linha, status, dieta, treino, obj, dia) in enumerate(ALUNOS, 1):
    A[k] = add("alunos", {
        "id": uid("aluno", k), "nome": nome, "primeiro_nome": nome.split()[0], "telefone": f"550090000{i:04d}",
        "email": f"{k}@exemplo.invalid", "sexo": sexo, "nascimento": f"{1984 + i}-0{i}-1{i}", "altura_cm": 160 + i * 3,
        "cidade": "Cidade Exemplo/UF", "status": status, "etapa_entrada": "plano_enviado" if status != "entrada" else "anamnese",
        "linha": linha, "objetivo": obj, "tem_dieta": dieta, "tem_treino": treino, "dia_checkin": dia,
        "mostrar_numeros_pdf": True, "modelo_pdf": "a", "meta_id": META, "anamnese_recebida_em": Dia(-70 + i).json() and None,
        "consentimento_lgpd_em": None, "consentimento_versao": "v1-ficticio", "observacoes": "DADO FICTÍCIO DE DEMONSTRAÇÃO",
    }, {"codigo": f"AL-{i}", "numero": i})
    A[k]["_consent"] = Dia(-80 + i, "10:00")
    A[k]["_anamnese"] = Dia(-75 + i)

# ------------------------------------------------------------------ leads
for i, (nome, etapa, temp, origem, problema, fu) in enumerate([
        ("Gabriela Exemplo", "novo", "quente", "Instagram", "Quer treino em casa com pouco equipamento", 0),
        ("Henrique Fictício", "em_conversa", "morno", "Indicação", "Dor nas costas ao treinar", 1),
        ("Íris Teste", "proposta", "quente", "Instagram", "Quer treino + dieta para emagrecer", -1),
        ("João Modelo", "fechou", "quente", "Indicação", "Hipertrofia", None),
        ("Karina Simulada", "perdido", "frio", "Anúncio", "Achou caro", None)], 1):
    add("leads", {"id": uid("lead", i), "nome": nome, "telefone": f"550090001{i:04d}", "perfil": f"@exemplo_{i}",
                  "entrou_em": Dia(-3 * i), "origem": origem, "temperatura": temp, "problema": problema,
                  "linha_provavel": "emagrecimento", "etapa": etapa, "proximo_followup": Dia(fu) if fu is not None else None,
                  "valor_fechado": 1290 if etapa == "fechou" else None, "observacao": "fictício"})

# ------------------------------------------------------------------ contratos e pagamentos
pag_n = 0
for k, preco, inicio in (("ana", 1, -100), ("bruno", 0, -20), ("carla", 1, -85), ("diego", 2, -60)):
    dur = [30, 90, 180][preco]
    cid = add("contratos", {"id": uid("contrato", k), "aluno_id": A[k]["id"], "plano_id": PRECOS[preco],
                            "valor": [297, 1290, 2340][preco], "inicio": Dia(inicio), "duracao_dias": dur,
                            "status": "em_renovacao" if k == "carla" else "vigente", "forma_cobranca": "Pix", "parcelas": 3 if preco else 1},
              {"fim": Dia(inicio + dur)})["id"]
    parcelas = 3 if preco else 1
    for p in range(parcelas):
        pag_n += 1
        venc = inicio + p * 30
        pago = venc <= -5
        valor = round([297, 1290, 2340][preco] / parcelas, 2)
        add("pagamentos", {"id": uid("pag", pag_n), "contrato_id": cid, "aluno_id": A[k]["id"],
                           "descricao": f"{A[k]['primeiro_nome']} · parcela {p + 1}/{parcelas}",
                           "situacao": "pago" if pago else ("vencido" if venc < 0 else "previsto"),
                           "vencimento": Dia(venc), "pago_em": Dia(venc) if pago else None, "valor_bruto": valor,
                           "taxa": round(valor * 0.03, 2), "forma": "Pix", "parcela": f"{p + 1}/{parcelas}"},
            {"valor_liquido": round(valor - round(valor * 0.03, 2), 2)})
# um pagamento deste mês e um vencido (para os números do financeiro)
for pag_n, (k, desc, venc, sit, valor) in enumerate([("elisa", "Elisa · avaliação inicial", -1, "pago", 150),
                                                     ("fabio", "Fábio · mensalidade", -6, "vencido", 297)], pag_n + 1):
    add("pagamentos", {"id": uid("pag", pag_n), "aluno_id": A[k]["id"], "descricao": desc, "situacao": sit, "vencimento": Dia(venc),
                       "pago_em": Dia(venc) if sit == "pago" else None, "valor_bruto": valor, "taxa": 0, "forma": "Pix"},
        {"valor_liquido": valor})
# meses anteriores (para as barras do financeiro)
for m in range(1, 6):
    for j in range(2):
        pag_n += 1
        add("pagamentos", {"id": uid("pag", pag_n), "aluno_id": A["bruno" if j else "diego"]["id"],
                           "descricao": f"Mensalidade antiga {m}.{j}", "situacao": "pago", "vencimento": Dia(-30 * m - 2),
                           "pago_em": Dia(-30 * m - 2), "valor_bruto": 297 + 120 * j + 40 * m, "taxa": 9, "forma": "Pix"},
            {"valor_liquido": 297 + 120 * j + 40 * m - 9})

# ------------------------------------------------------------------ agenda
for i, (k, n, hora, tipo, alerta) in enumerate([
        ("carla", 0, "18:00", "renovacao", "Renovação: levar a evolução das cargas"),
        ("elisa", 1, "07:30", "avaliacao", "Sem anamnese ainda: confirmar antes"),
        ("bruno", 3, "19:00", "retorno", "")], 1):
    add("consultas", {"id": uid("consulta", i), "aluno_id": A[k]["id"], "titulo": f"{tipo.capitalize()} · {A[k]['primeiro_nome']}",
                      "data_hora": Dia(n, hora), "duracao_min": 45, "tipo": tipo, "status": "confirmada" if n == 0 else "agendada",
                      "link_reuniao": "https://meet.exemplo.invalid/abc-defg-hij", "alerta": alerta})

# ------------------------------------------------------------------ medidas, check-ins
PESOS = {"ana": [82.4, 81.9, 81.6, 81.0, 80.7, 80.1, 79.8, 79.3, 79.0, 78.6],
         "carla": [74.0, 73.8, 73.1, 72.9, 72.5, 72.6, 72.0, 71.7],
         "bruno": [70.2, 70.4, 70.9, 71.1, 71.4, 71.8],
         "diego": [76.5, 76.2, 76.4, 76.0, 75.8, 75.9]}
DIAS = {"ana": [5, 6, 5, 7, 4, 6, 6, 5, 6, 6], "carla": [4, 5, 3, 5, 4, 5, 3, 4], "bruno": [6, 6, 5, 7, 6, 6], "diego": [5, 5, 6, 6, 5, 5]}
for k, pesos in PESOS.items():
    n = len(pesos)
    for i, kg in enumerate(pesos):
        sem = segunda(-7 * (n - i))
        no_plano = DIAS[k][i]
        leve = 1 if no_plano < 7 else 0
        grande = 7 - no_plano - leve
        ck = add("checkins", {
            "id": uid("ck", k, i), "aluno_id": A[k]["id"], "semana_inicio": SDia(sem), "quinzenal": False,
            "peso_semana": kg, "dias_no_plano": no_plano, "dias_leve": leve, "dias_grande": grande, "dias_nao_lembro": 0,
            "treinos_feitos": 3 if k != "carla" else 2, "fome": 4, "saciedade": 7, "sono_horas": 7, "sono_qualidade": 7,
            "estresse": 4, "agua_l": 2.2, "dor_lesao_nova": False, "nivel": "ok",
            "troca_pedida": "Trocar o pão do café por cuscuz" if (k == "ana" and i == n - 1) else None,
            "dificuldade": "Semana corrida no trabalho" if (k == "carla" and i == n - 1) else None,
        }, {"score": round((no_plano * 100 + leve * 50) / (no_plano + leve + grande))})
        add("medidas", {"id": uid("med", k, i), "aluno_id": A[k]["id"], "checkin_id": ck["id"], "data": SDia(sem + 6),
                        "peso_kg": kg, "cintura_cm": None, "origem": "checkin"})

# ------------------------------------------------------------------ recebidos (o que chegou do Tally)
for i, (k, tipo, n, status) in enumerate([("ana", "checkin_semanal", -1, "NOVO"), ("carla", "checkin_semanal", -2, "EM_ANALISE"),
                                          ("bruno", "checkin_cargas", -1, "NOVO")], 1):
    add("recebidos", {"id": uid("rec", i), "aluno_id": A[k]["id"], "tipo": tipo, "status": status, "origem": "tally",
                      "titulo": f"{ {'checkin_semanal': 'Check-in semanal', 'checkin_cargas': 'Check-in de cargas'}[tipo]} · {A[k]['primeiro_nome']}", "recebido_em": Dia(n, "08:15"),
                      "tally_resposta_id": f"demo-{i}", "urgente": False, "respostas": {"demo": True}, "respostas_texto": "Respostas fictícias."},
        {"prazo": Dia(n + 2, "08:15")})

# ------------------------------------------------------------------ diário
add("diario", {"id": uid("diario", 1), "aluno_id": A["carla"]["id"], "data": Dia(-1), "tipo": "Análise do check-in", "status": "RASCUNHO",
               "conduta_proposta": "Manter o treino e reforçar o lanche pré-treino", "envolve_dieta": False,
               "texto_proposto": "Oi, Carla! Semana corrida, mas você manteve 2 treinos. Vamos deixar o lanche pré-treino pronto na véspera e seguir com as mesmas cargas."})
add("diario", {"id": uid("diario", 2), "aluno_id": A["ana"]["id"], "data": Dia(-1), "tipo": "Análise do check-in", "status": "EM_REVISAO",
               "conduta_proposta": "Trocar o pão do café por cuscuz (pedido da aluna)", "envolve_dieta": True,
               "texto_proposto": "Oi, Ana! Recebi o seu pedido de trocar o pão por cuscuz. Como mexe na dieta, o nosso nutricionista responsável confere e te respondo até amanhã."})

# ------------------------------------------------------------------ dietas e entregas
def dieta(k, v, tipo, fase, kcal, p, c, g, status, inicio, aprovado_rt):
    did, eid = uid("dieta", k, v), uid("entrega", "dieta", k, v)
    add("dietas", {"id": did, "aluno_id": A[k]["id"], "versao": v, "tipo_versao": tipo, "fase": fase,
                   "plano_anterior_id": uid("dieta", k, v - 1) if v > 1 else None,
                   "get_kcal": kcal + 450, "get_metodo": "mifflin_fa", "fator_atividade": 1.375, "peso_usado_kg": PESOS[k][-1],
                   "kcal_dia": kcal, "proteina_g": p, "carboidrato_g": c, "gordura_g": g, "fibra_g": 25, "meta_agua_l": 2.8,
                   "livre_prevista": True, "livre_por_semana": 1, "conferencia": "ok", "mensagens_conferencia": "sem avisos",
                   "mostrar_numeros": True, "entrega_id": eid, "gerado_por": "exemplo fictício"})
    for o, (nome, hora, kc) in enumerate([("Café da manhã", "07:00", 380), ("Almoço", "12:30", 520),
                                          ("Lanche da tarde (pré-treino)", "16:30", 260), ("Jantar", "20:00", 430)], 1):
        add("refeicoes", {"id": uid("ref", k, v, o), "dieta_id": did, "ordem": o, "nome_exibicao": nome, "horario": hora,
                          "kcal": kc, "itens": "itens fictícios", "tipo_dia": "todos"})
    pdf = f"Plano alimentar v{v} - {A[k]['primeiro_nome']} - demo.pdf"
    ent = {"id": eid, "aluno_id": A[k]["id"], "tipo": "dieta", "status": status, "titulo": f"Dieta v{v} · {A[k]['primeiro_nome']}",
           "versao": v, "dieta_id": did, "inicio": Dia(inicio), "dias_validade": 30, "pdf_path": f"demo/{did}.pdf", "pdf_nome": pdf,
           "pdf_sha256": "demo" + "0" * 60, "origem": "agente de dieta", "pdf_gerado_em": Dia(-2, "10:00"),
           "texto_envio": f"Oi, {A[k]['primeiro_nome']}! Seu plano alimentar novo está pronto e vale de "
                          f"{(datetime.date.today() + datetime.timedelta(days=inicio)).strftime('%d/%m')} por 30 dias. "
                          "Ele foi prescrito pelo nosso nutricionista responsável técnico. Qualquer dúvida, me chama aqui.",
           "link_whatsapp": None, "aprovado_em": Dia(-2, "11:00") if status != "RASCUNHO" else None,
           "aprovado_por": "Jorge Souto" if status != "RASCUNHO" else None,
           "rt_aprovado_em": Dia(inicio - 1, "09:00") if aprovado_rt else None,
           "rt_aprovado_por": "Lucas Melo (CRN6 - 50479-P) · demo" if aprovado_rt else None,
           "rt_pdf_sha256": ("demo" + "0" * 60) if aprovado_rt else None,
           "enviado_em": Dia(inicio, "09:30") if status == "ENVIADO" else None}
    add("entregas", ent, {"validade": Dia(inicio + 30)})
    if aprovado_rt:
        add("aprovacoes_rt", {"id": uid("aprov", k, v), "entrega_id": eid, "decisao": "aprovado",
                              "por": "Lucas Melo (CRN6 - 50479-P) · demo", "em": Dia(inicio - 1, "09:00"), "pdf_sha256": "demo" + "0" * 60})
    return did, eid


ana1, ana1e = dieta("ana", 1, "primeiro", "deficit", 1650, 135, 160, 52, "ENVIADO", -28, True)
ana2, _ = dieta("ana", 2, "ajuste", "deficit", 1600, 140, 148, 50, "APROVACAO_RT", 2, False)
carla1, carla1e = dieta("carla", 1, "primeiro", "deficit", 1500, 120, 140, 50, "ENVIADO", -25, True)
carla2, _ = dieta("carla", 2, "ajuste", "deficit", 1500, 125, 135, 48, "RASCUNHO", 5, False)
diego1, diego1e = dieta("diego", 1, "primeiro", "manutencao", 2500, 150, 320, 70, "ENVIADO", -20, True)
EM_USO = {"ana": ana1, "carla": carla1, "diego": diego1}

# ------------------------------------------------------------------ treino: exercícios, prescrições, semanas, sessões, séries
EXS = [("Agachamento livre", "kg total", "Pernas"), ("Supino reto com barra", "kg total", "Peito"),
       ("Remada curvada", "kg total", "Costas"), ("Elevação pélvica", "kg total", "Glúteos"), ("Barra fixa", "peso do corpo", "Costas")]
EX = {n: add("exercicios", {"id": uid("ex", n), "nome_tecnico": n, "nome_aluno": n, "grupo": g, "unidade_padrao": u})["id"]
      for n, u, g in EXS}
PRESC = {}
CARGAS = {"ana": {"Agachamento livre": 36, "Elevação pélvica": 50, "Remada curvada": 25},
          "bruno": {"Agachamento livre": 60, "Supino reto com barra": 50, "Barra fixa": None},
          "carla": {"Agachamento livre": 30, "Elevação pélvica": 40},
          "diego": {"Agachamento livre": 55, "Remada curvada": 35}}
for k, exs in CARGAS.items():
    pid = uid("presc", k)
    eid = uid("entrega", "treino", k)
    PRESC[k] = pid
    add("prescricoes_treino", {"id": pid, "aluno_id": A[k]["id"], "versao": 2 if k == "bruno" else 1, "objetivo": A[k]["objetivo"],
                               "nivel": "intermediário", "local_treino": "academia", "sessoes_por_semana": 3,
                               "inicio": Dia(-42), "validade": Dia(-42 + 60), "entrega_id": eid})
    for o, n in enumerate(exs, 1):
        add("itens_prescricao", {"id": uid("item", k, o), "prescricao_id": pid, "dia": "A", "ordem": o, "exercicio_id": EX[n],
                                 "series": 4, "repeticoes": "8 a 12", "descanso_s": 90})
    status = "ENVIAR" if k == "bruno" else "ENVIADO"
    add("entregas", {"id": eid, "aluno_id": A[k]["id"], "tipo": "treino", "status": status, "titulo": f"Treino v{2 if k == 'bruno' else 1} · {A[k]['primeiro_nome']}",
                     "versao": 2 if k == "bruno" else 1, "prescricao_treino_id": pid, "inicio": Dia(1 if k == "bruno" else -42), "dias_validade": 60,
                     "pdf_nome": f"Treino - {A[k]['primeiro_nome']} - demo.pdf", "origem": "manual",
                     "texto_envio": f"Oi, {A[k]['primeiro_nome']}! Seu treino novo está pronto. Bora!",
                     "aprovado_em": Dia(-1, "10:00"), "aprovado_por": "Jorge Souto",
                     "enviado_em": Dia(-42, "09:00") if status == "ENVIADO" else None},
        {"validade": Dia((1 if k == "bruno" else -42) + 60)})
    for w in range(6):
        sem = segunda(-7 * (6 - w))
        sid = add("semanas_treino", {"id": uid("sem", k, w), "aluno_id": A[k]["id"], "prescricao_id": pid, "semana_inicio": SDia(sem),
                                     "planejadas": 3, "completas": 2 if w % 3 else 3, "parciais": 1 if w % 3 else 0, "esforco": 7,
                                     "leitura": "semana fictícia"}, {"adesao_pct": 100})["id"]
        ses = add("sessoes", {"id": uid("ses", k, w), "aluno_id": A[k]["id"], "prescricao_id": pid, "semana_id": sid,
                              "data": SDia(sem + 1), "dia_treino": "A", "status": "completa", "origem": "lançado depois"})["id"]
        for n, base in exs.items():
            if base is None:  # peso do corpo: repetições
                reps = [8 + w // 2, 7 + w // 2, 6 + w // 2]
                linha = {f"s{i}_rep": r for i, r in enumerate(reps, 1)}
                extra = {"maior_carga": None, "reps_total": sum(reps)}
            else:
                carga = base + w * (2.5 if base >= 40 else 2)
                linha = {"s1_rep": 10, "s2_rep": 9, "s3_rep": 8, "s1_carga": carga, "s2_carga": carga, "s3_carga": carga}
                extra = {"maior_carga": carga, "reps_total": 27}
            add("series", {"id": uid("serie", k, w, n), "sessao_id": ses, "aluno_id": A[k]["id"], "exercicio_id": EX[n],
                           "exercicio_nome": n, "unidade": "peso do corpo" if base is None else "kg total", **linha}, extra)

# ------------------------------------------------------------------ comunicação e lembretes
add("mensagens_prontas", {"id": uid("msg", 1), "codigo": "D1", "nome": "Envio do plano alimentar", "dono": "Dieta", "status": "APROVADO",
                          "texto": "Oi, {primeiro_nome}! Seu plano alimentar novo está pronto e vale até {validade}. Ele foi prescrito pelo nosso nutricionista responsável técnico. Qualquer dúvida, me chama aqui."})
add("envios", {"id": uid("envio", 1), "aluno_id": A["fabio"]["id"], "titulo": "Convite para voltar · Fábio", "status": "PARA_APROVAR",
               "texto_final": "Oi, Fábio! Sentimos sua falta nos treinos. Quer marcar uma conversa rápida esta semana para recomeçar no seu ritmo?",
               "telefone": A["fabio"]["telefone"], "origem": "manual"})
add("envios", {"id": uid("envio", 2), "aluno_id": A["diego"]["id"], "titulo": "Lembrete do check-in · Diego", "status": "APROVADO",
               "texto_final": "Oi, Diego! Lembrete do check-in de segunda: leva 3 minutos. Valeu!", "telefone": A["diego"]["telefone"],
               "aprovado_em": Dia(-1, "18:00"), "origem": "manual"})
for i, (k, titulo, secao, prazo, motivo, minutos, texto) in enumerate([
        ("ana", "Aluna relatou dor no joelho no agachamento", "urgente", 0, "Dor no treino", 10,
         "Oi, Ana! Vi que o joelho incomodou no agachamento. Me conta como está hoje e vamos ajustar o exercício."),
        ("bruno", "Mandar o treino v2", "para_hoje", 0, "Entrega", 5, None),
        ("carla", "Preparar a renovação", "para_hoje", 0, "Renovação", 20, None),
        ("diego", "Conferir a planilha de corrida", "proximos_dias", 2, "Treino", 15, None),
        ("elisa", "Cobrar a anamnese", "proximos_dias", 1, "Anamnese", 3, "Oi, Elisa! Consegue responder a anamnese até amanhã?")], 1):
    add("lembretes", {"id": uid("lem", i), "aluno_id": A[k]["id"], "titulo": titulo, "secao": secao, "prazo": Dia(prazo),
                      "motivo": motivo, "minutos_estimados": minutos, "texto_pronto": texto, "feito": False, "origem": "demo"})


# ------------------------------------------------------------------ saída
def para_json(v):
    if isinstance(v, Dia):
        return v.json()
    return v


def para_sql(v):
    if v is None:
        return "null"
    if isinstance(v, Dia):
        return v.sql()
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (dict, list)):
        return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"


def main():
    # alunos: consentimento e anamnese são Dias guardados à parte
    for linha, _ in T["alunos"]:
        linha["consentimento_lgpd_em"] = linha.pop("_consent")
        linha["anamnese_recebida_em"] = linha.pop("_anamnese")
    ordem = ["configuracoes", "metas", "tabela_precos", "leads", "alunos", "contratos", "pagamentos", "consultas", "checkins",
             "medidas", "recebidos", "diario", "dietas", "refeicoes", "exercicios", "prescricoes_treino", "itens_prescricao",
             "entregas", "aprovacoes_rt", "semanas_treino", "sessoes", "series", "mensagens_prontas", "envios", "lembretes"]
    assert set(ordem) == set(T), set(T) ^ set(ordem)
    sql = ["-- =====================================================================================================",
           "-- DADOS FICTÍCIOS de demonstração (gerado por gerar_dados_ficticios.py; não edite à mão).",
           "-- Use SÓ num projeto de TESTE. Nenhuma pessoa real: nomes inventados, telefones inexistentes (55 0090000…),",
           "-- e-mails no domínio reservado .invalid. Para apagar tudo: rode o bloco 'limpar' no fim deste arquivo.",
           "-- =====================================================================================================",
           "begin;",
           "-- entregas: o seed grava direto o status final; a trava de transição só vale para UPDATE"]
    adiadas = []  # chaves "em círculo" gravadas depois
    for t in ordem:
        for linha, _ in T[t]:
            l = dict(linha)
            if t == "dietas" and l.get("entrega_id"):
                adiadas.append(f"update public.dietas set entrega_id = '{l['entrega_id']}' where id = '{l['id']}';")
                l["entrega_id"] = None
            if t == "prescricoes_treino" and l.get("entrega_id"):
                adiadas.append(f"update public.prescricoes_treino set entrega_id = '{l['entrega_id']}' where id = '{l['id']}';")
                l["entrega_id"] = None
            if t == "dietas" and l.get("plano_anterior_id"):
                adiadas.append(f"update public.dietas set plano_anterior_id = '{l['plano_anterior_id']}' where id = '{l['id']}';")
                l["plano_anterior_id"] = None
            cols = [c for c in l if l[c] is not None]
            sql.append(f"insert into public.{t} ({', '.join(cols)}) values ({', '.join(para_sql(l[c]) for c in cols)});")
    sql += adiadas
    for k, did in EM_USO.items():
        sql.append(f"update public.alunos set dieta_em_uso_id = '{did}' where id = '{A[k]['id']}';")
    for k, pid in PRESC.items():
        sql.append(f"update public.alunos set treino_em_uso_id = '{pid}' where id = '{A[k]['id']}';")
    sql += ["commit;", "",
            "-- ---------------------------------------------------------------- limpar (apaga SÓ os fictícios)",
            "-- begin;",
            "-- delete from public.leads where observacao = 'fictício';",
            "-- delete from public.pagamentos where aluno_id in (select id from public.alunos where observacoes = 'DADO FICTÍCIO DE DEMONSTRAÇÃO');",
            "-- delete from public.alunos where observacoes = 'DADO FICTÍCIO DE DEMONSTRAÇÃO';",
            "-- delete from public.exercicios where id in (" + ", ".join(f"'{v}'" for v in EX.values()) + ");",
            "-- delete from public.mensagens_prontas where codigo = 'D1' and nome = 'Envio do plano alimentar';",
            "-- delete from public.tabela_precos where id in (" + ", ".join(f"'{v}'" for v in PRECOS) + ");",
            "-- delete from public.metas where id = '" + META + "';",
            "-- delete from public.configuracoes where chave = 'demo';",
            "-- commit;"]
    with open(SAIDA_SQL, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sql) + "\n")

    tabelas = {}
    for t in ordem:
        tabelas[t] = []
        for linha, extra in T[t]:
            tabelas[t].append({k: para_json(v) for k, v in {**linha, **extra}.items()})
    for linha in tabelas["alunos"]:
        k = next(c for c, v in A.items() if v["id"] == linha["id"])
        linha["dieta_em_uso_id"] = EM_USO.get(k)
        linha["treino_em_uso_id"] = PRESC.get(k)
    os.makedirs(os.path.dirname(SAIDA_JSON), exist_ok=True)
    with open(SAIDA_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"_aviso": "DADOS FICTÍCIOS de demonstração (gerado por supabase/gerar_dados_ficticios.py). Datas '@hoje+n' são relativas ao dia em que o painel abre.",
                   "tabelas": tabelas}, f, ensure_ascii=False, indent=1)
    print(f"SQL:  {SAIDA_SQL} ({sum(len(v) for v in T.values())} linhas)")
    print(f"JSON: {SAIDA_JSON}")


if __name__ == "__main__":
    main()
