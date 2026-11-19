#!/usr/bin/env python3
"""Contas do agente de dieta, sem token: gasto do dia, macros e a conferência automática do plano
(contrato 1.7.4 do plano.json + regras do RT em "Método do RT (Lucas Melo).md").

Uso:
  python calcular_plano.py energia --sexo F --idade 36 --altura 165 --peso 81.1 --fa 1.375
         [--deficit 500] [--proteina 1.6] [--gordura 0.9]
      gasto em repouso (Mifflin-St Jeor; Harris-Benedict só para comparar), gasto do dia e, com --deficit,
      as kcal e os macros (proteína e gordura em g/kg, carboidrato fecha as calorias, fibra 15 g por 1.000 kcal)
  python calcular_plano.py conferir plano.json [--gravar]
      calcula cada item pelo banco de alimentos (campo "ref"), soma refeições e dia, confere tudo e,
      com --gravar, escreve os números e o resultado da conferência no próprio JSON

Resultado da conferência: ok · aviso (deixa salvar) · erro (não deixa) · trava (só com plano.justificativa_rt).
"""
import argparse
import datetime
import json
import math
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
import alimentos  # noqa: E402

REFEICOES_PADRAO = ["Café da manhã", "Lanche da manhã", "Almoço", "Lanche da tarde", "Jantar", "Ceia ou depois do jantar"]
NUTRI = ["kcal", "proteina_g", "carboidrato_g", "gordura_g", "fibra_g", "saturada_g"]
SIGLAS_OK = {"CRN", "PDF", "OK"}
MORAIS = ["falhou", "trapaceou", "jacou", "sem força de vontade", "preguiços", "gulos", "cheat", "lixo", "proibid",
          "inflamatório"]
PROMESSA = [r"garant", r"vai perder", r"perca \d", r"perder \d+ ?(kg|quilo)", r"resultado certo", r"emagre\w+ \d+ ?kg"]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")


def br(v, casas=0):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------- energia ----------------
def energia(a):
    s = a.sexo.upper()[0]
    mifflin = 10 * a.peso + 6.25 * a.altura - 5 * a.idade + (5 if s == "M" else -161)
    hb = (66.473 + 13.7516 * a.peso + 5.0033 * a.altura - 6.755 * a.idade) if s == "M" else \
         (655.0955 + 9.5634 * a.peso + 1.8496 * a.altura - 4.6756 * a.idade)
    get = mifflin * a.fa
    print(f"Gasto em repouso · Mifflin-St Jeor: {br(mifflin)} kcal  (Harris-Benedict, só para comparar: {br(hb)})")
    print(f"Gasto do dia (GET) = {br(mifflin)} × {a.fa} = {br(get)} kcal   [com fator um degrau abaixo: "
          f"{br(mifflin * max(1.2, a.fa - 0.175))}]")
    print(f"IMC: {br(a.peso / (a.altura / 100) ** 2, 1)}")
    if a.deficit is None:
        return
    kcal = math.ceil((get - a.deficit) / 50) * 50  # arredonda para cima: o déficit nunca passa do escolhido
    print(f"\nkcal do plano: {br(get)} − {br(a.deficit)} = {br(get - a.deficit)} → {br(kcal)} kcal/dia "
          f"(de 50 em 50; déficit real {br(get - kcal)})")
    if a.proteina and a.gordura:
        p, g = round(a.proteina * a.peso), round(a.gordura * a.peso)
        c = round((kcal - 4 * p - 9 * g) / 4)
        print(f"Proteína {p} g ({br(a.proteina, 1)} g/kg · {round(400 * p / kcal)}%) · Gordura {g} g ({br(a.gordura, 1)} g/kg · "
              f"{round(900 * g / kcal)}%) · Carboidrato {c} g ({round(400 * c / kcal)}%)")
        print(f"Fibra: {round(15 * kcal / 1000)} g (15 g por 1.000 kcal) · Saturada: até {round(0.10 * kcal / 9)} g (10% das kcal)")
        if c < 0:
            print("ATENÇÃO: proteína e gordura já passam das calorias; baixe uma delas.")


# ---------------- cálculo dos itens ----------------
def calcular_item(it, banco, msgs, onde):
    g = it.get("gramas")
    if it.get("ref"):
        a = banco.get(it["ref"])
        if not a:
            msgs.append(("erro", f"{onde}: '{it['ref']}' não existe no banco de alimentos"))
            return {k: 0 for k in NUTRI}
        if g in (None, ""):
            msgs.append(("erro", f"{onde}: {it['alimento']} tem ref mas não tem gramas"))
            return {k: 0 for k in NUTRI}
        v = {k: (a["por_100g"].get(k) or 0) * float(g) / 100 for k in NUTRI}
        if a["por_100g"].get("saturada_g") is None and a["por_100g"].get("gordura_g", 0) > 1:
            it["_sem_saturada"] = True
        for k in NUTRI:
            it[k] = round(v[k], 1)
        return v
    if g not in (None, ""):
        msgs.append(("erro", f"{onde}: {it['alimento']} ({g} g) sem 'ref' no banco: busque com alimentos.py buscar"))
    return {k: 0 for k in NUTRI}


def soma(lista):
    return {k: sum(x[k] for x in lista) for k in NUTRI}


def texto_leigo(campo, txt, msgs):
    if not txt:
        return
    t = str(txt)
    for s in re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,6}\b", t):
        if s not in SIGLAS_OK:
            msgs.append(("erro", f"{campo}: sigla '{s}' no texto do aluno (escreva por extenso)"))
    low = sem_acento(t)
    for m in MORAIS:
        if sem_acento(m) in low:
            msgs.append(("erro", f"{campo}: termo moral '{m}' (Diretrizes do RT 6.1)"))
    for p in PROMESSA:
        if re.search(p, low):
            msgs.append(("erro", f"{campo}: parece promessa de resultado ('{p}') — ética do CFN"))


def conferir(dados, gravar=False):
    """Calcula e confere o plano. Devolve (resultado, mensagens, resumo)."""
    banco = alimentos.por_id()
    D, P, R = dados.get("documento", {}), dados.get("plano", {}), dados.get("relatorio", {}) or {}
    msgs = []

    obrig = ["aluno_id", "versao", "tipo_versao", "fase", "dias_validade", "get_kcal", "get_metodo", "peso_usado_kg",
             "data_peso", "kcal_dia", "proteina_g", "carboidrato_g", "gordura_g", "refeicoes", "meta_agua_l",
             "gerado_por", "gerado_em"]
    for k in obrig:
        if P.get(k) in (None, "", []):
            msgs.append(("erro", f"falta plano.{k}"))
    if "livre_prevista" not in P:
        msgs.append(("erro", "falta plano.livre_prevista (true ou false)"))
    for k in ("aluno_nome", "primeiro_nome", "linha", "inicio", "validade", "sexo"):
        if not D.get(k):
            msgs.append(("erro", f"falta documento.{k}"))
    if P.get("tipo_versao") not in ("primeiro", "ajuste", "repeticao", "pausa", "mudanca_fase"):
        msgs.append(("erro", f"tipo_versao '{P.get('tipo_versao')}' fora da lista"))
    if (P.get("versao") or 1) > 1 and P.get("tipo_versao") != "primeiro" and not P.get("o_que_muda"):
        msgs.append(("erro", "da v2 em diante, plano.o_que_muda é obrigatório (até 3 frases leigas)"))
    if len(P.get("o_que_muda") or []) > 3:
        msgs.append(("aviso", "o_que_muda passa de 3 frases"))
    if any(msgs) and any(m[0] == "erro" and m[1].startswith("falta plano.refeicoes") for m in msgs):
        return fechar(msgs, {}, P, gravar)

    # --- itens e refeições
    por_tipo = {}
    for i, r in enumerate(P["refeicoes"]):
        onde = r.get("nome_exibicao") or f"refeição {i + 1}"
        if r.get("refeicao_padrao") not in REFEICOES_PADRAO:
            msgs.append(("erro", f"{onde}: refeicao_padrao '{r.get('refeicao_padrao')}' não é uma das 6 do check-in"))
        tot = soma([calcular_item(it, banco, msgs, onde) for it in r.get("itens", [])])
        for k in ("kcal", "proteina_g", "carboidrato_g", "gordura_g"):
            r[k] = round(tot[k])
        r["_fibra_g"], r["_saturada_g"] = round(tot["fibra_g"], 1), round(tot["saturada_g"], 1)
        por_tipo.setdefault(r.get("tipo_dia") or "todos", []).append((r, tot))
        sem_sat = [it["alimento"] for it in r.get("itens", []) if it.pop("_sem_saturada", False)]
        if sem_sat:
            msgs.append(("info", f"{onde}: sem dado de gordura saturada na tabela para {', '.join(sem_sat)}"))
        # regras do RT: legumes e folhas no almoço e no jantar, sem "salada livre"
        if r.get("refeicao_padrao") in ("Almoço", "Jantar"):
            veg = [it for it in r.get("itens", []) if re.search(r"legume|folha|verdura|salada|vegeta", sem_acento(
                (it.get("categoria") or "") + " " + (it.get("grupo_substituicao") or "")))]
            gramas_veg = sum(float(it.get("gramas") or 0) for it in veg)
            if gramas_veg < 150:
                msgs.append(("aviso", f"{onde}: legumes e folhas somam {br(gramas_veg)} g (o RT pede no mínimo 150 g)"))
            if any(it.get("gramas") in (None, "") or "livre" in sem_acento(it.get("alimento", "")) for it in veg):
                msgs.append(("aviso", f"{onde}: legume ou folha sem quantidade ou 'livre' (especifique um por um)"))

    # --- substituições
    grupos = {}
    for g in P.get("substituicoes", []):
        grupos[g["grupo"]] = g
        base = calcular_item(g["base"], banco, msgs, f"troca {g['grupo']} (base)")
        g["base"]["kcal"] = round(base["kcal"])
        for e in g.get("equivalentes", []):
            v = calcular_item(e, banco, msgs, f"troca {g['grupo']}")
            e["kcal"] = round(v["kcal"])
            if base["kcal"] and abs(v["kcal"] - base["kcal"]) > 0.10 * base["kcal"]:
                msgs.append(("aviso", f"troca {g['grupo']}: {e['alimento']} tem {br(v['kcal'])} kcal e a base "
                                      f"{g['base']['alimento']} {br(base['kcal'])} (fora de ±10%)"))
            # o macro que mais dá calorias à porção base (proteína, carboidrato ou gordura) também precisa bater
            chave = max((("proteina_g", 4), ("carboidrato_g", 4), ("gordura_g", 9)), key=lambda m: base[m[0]] * m[1])[0]
            if base[chave] > 5 and abs(v[chave] - base[chave]) > 0.20 * base[chave]:
                nome = {"proteina_g": "proteína", "carboidrato_g": "carboidrato", "gordura_g": "gordura"}[chave]
                msgs.append(("aviso", f"troca {g['grupo']}: {e['alimento']} tem {br(v[chave], 1)} g de {nome} e a base "
                                      f"{br(base[chave], 1)} g (fora de ±20%)"))
    for r in P["refeicoes"]:
        for it in r.get("itens", []):
            gs = it.get("grupo_substituicao")
            if gs and gs not in grupos:
                msgs.append(("aviso", f"{r['nome_exibicao']}: grupo '{gs}' não existe em substituicoes"))
        if r.get("refeicao_padrao") in ("Almoço", "Jantar"):
            for alvo, nome in (("prote", "proteína"), ("carbo", "carboidrato")):
                ops = [1 + len(grupos[it["grupo_substituicao"]].get("equivalentes", []))
                       for it in r.get("itens", []) if it.get("grupo_substituicao") in grupos and alvo in sem_acento(
                           (grupos[it["grupo_substituicao"]].get("nome_exibicao") or "") + it["grupo_substituicao"])]
                if ops and max(ops) < 3:
                    msgs.append(("aviso", f"{r['nome_exibicao']}: só {max(ops)} opção(ões) de {nome} (o RT usa 3 a 4)"))

    # --- dia e semana
    kcal = float(P.get("kcal_dia") or 0)
    todos = soma([t for _, t in por_tipo.get("todos", [])])
    dias = []  # (rótulo, totais, nº de dias na semana, kcal alvo)
    if P.get("tipos_de_dia"):
        for td in P["tipos_de_dia"]:
            extra = soma([t for _, t in por_tipo.get(td["tipo"], [])])
            dias.append((td["tipo"], {k: todos[k] + extra[k] for k in NUTRI}, len(td.get("dias", [])), td.get("kcal")))
        if sum(d[2] for d in dias) != 7:
            msgs.append(("erro", "tipos_de_dia: os dias da semana não somam 7"))
    else:
        dias.append(("dia comum", todos, 7, None))
    semana = sum(t["kcal"] * n for _, t, n, _ in dias)
    livre_txt = ""
    if P.get("livre_prevista"):
        L, n = P.get("livre_teto_kcal"), P.get("livre_por_semana") or 1
        J = sum(r["kcal"] for r in P["refeicoes"] if r.get("refeicao_padrao") == P.get("livre_substitui")
                and (r.get("tipo_dia") or "todos") == "todos")
        if not P.get("livre_substitui"):
            msgs.append(("erro", "refeição livre prevista sem livre_substitui (qual refeição ela troca)"))
        if not L:
            msgs.append(("aviso", "refeição livre sem teto de kcal: a média da semana não a inclui"))
        else:
            semana += n * (L - J)
            livre_txt = f" · com {n} refeição(ões) livre(s) de até {br(L)} kcal no lugar de {br(J)} kcal"
        if not P.get("livre_teto_texto"):
            msgs.append(("aviso", "refeição livre sem teto em linguagem leiga (livre_teto_texto)"))
        if str(D.get("linha")) == "gastro":
            msgs.append(("aviso", "refeição livre em aluno da linha gastro (o RT não costuma usar: confirme)"))
    media = semana / 7
    if kcal and abs(media - kcal) > 0.03 * kcal:
        msgs.append(("erro", f"refeições somam {br(media)} kcal na média da semana{livre_txt}; o plano diz {br(kcal)} (±3%)"))
    for rot, t, n, alvo in dias:
        if alvo and abs(t["kcal"] - alvo) > 0.03 * alvo:
            msgs.append(("erro", f"{rot}: refeições somam {br(t['kcal'])} kcal e o tipo de dia diz {br(alvo)} (±3%)"))

    # --- macros, fibra e saturada
    p, c, g = (float(P.get(k) or 0) for k in ("proteina_g", "carboidrato_g", "gordura_g"))
    conta = 4 * p + 4 * c + 9 * g
    if kcal and abs(conta - kcal) > 0.05 * kcal:
        msgs.append(("erro", f"4P + 4C + 9G = {br(conta)} kcal e o plano diz {br(kcal)} (±5%)"))
    base_dia = dias[0][1]
    for k, nome, tol in (("proteina_g", "proteína", 0.10), ("carboidrato_g", "carboidrato", 0.15), ("gordura_g", "gordura", 0.15)):
        alvo = float(P.get(k) or 0)
        if alvo and abs(base_dia[k] - alvo) > tol * alvo:
            msgs.append(("aviso", f"{nome}: refeições do {dias[0][0]} somam {br(base_dia[k])} g e a meta é {br(alvo)} g"))
    fibra_meta = (P.get("fibra_g_por_1000kcal") or 15) * base_dia["kcal"] / 1000
    if base_dia["kcal"] and base_dia["fibra_g"] < 0.95 * fibra_meta:
        nota = " (linha gastro: a meta depende da fase; confirme com o RT)" if D.get("linha") == "gastro" else ""
        msgs.append(("aviso", f"fibra: {br(base_dia['fibra_g'], 1)} g no {dias[0][0]}, abaixo de "
                              f"{br(fibra_meta)} g ({P.get('fibra_g_por_1000kcal') or 15} g por 1.000 kcal){nota}"))
    limite = P.get("limite_saturada_pct") or 10
    sat_pct = 900 * base_dia["saturada_g"] / base_dia["kcal"] if base_dia["kcal"] else 0
    if sat_pct > limite:
        msgs.append(("aviso", f"gordura saturada: {br(sat_pct, 1)}% das kcal (limite {limite}%)"))

    # --- fase, déficit e travas
    get = float(P.get("get_calibrado_kcal") or P.get("get_kcal") or 0)
    fase, treino = P.get("fase"), bool(D.get("tem_treino"))
    if get and kcal:
        deficit = get - kcal
        if fase == "deficit" and deficit <= 0:
            msgs.append(("erro", f"fase déficit, mas as kcal ({br(kcal)}) não ficam abaixo do gasto ({br(get)})"))
        if fase in ("manutencao", "pausa") and abs(deficit) > 0.05 * get:
            msgs.append(("erro", f"fase {fase} com kcal {br(kcal)} longe do gasto {br(get)} (±5%)"))
        if fase == "superavit" and deficit >= 0:
            msgs.append(("erro", f"fase superávit, mas as kcal ({br(kcal)}) não passam do gasto ({br(get)})"))
        teto = 500 if treino else 750
        if fase == "deficit" and deficit > teto:
            msgs.append(("aviso", f"déficit de {br(deficit)} kcal/dia passa do teto de {teto} (só com o ok do RT)"))
    sexo = str(D.get("sexo") or "").upper()[:1]
    if kcal and kcal < 800:
        if P.get("justificativa_rt"):
            msgs.append(("trava", f"{br(kcal)} kcal: abaixo de 800 (justificativa do RT registrada)"))
        else:
            msgs.append(("trava", f"{br(kcal)} kcal: abaixo de 800, dieta de muito baixa caloria; só com justificativa escrita do RT"))
    elif kcal and kcal < (1500 if sexo == "M" else 1200):
        msgs.append(("aviso", f"{br(kcal)} kcal: abaixo da faixa típica ({'1.500 homem' if sexo == 'M' else '1.200 mulher'})"))
    peso = float(P.get("peso_usado_kg") or 0)
    if treino and peso and p / peso < 1.6:
        msgs.append(("aviso", f"proteína {br(p / peso, 2)} g/kg com treino, abaixo de 1,6 (ok se for a regra da gordura corporal alta)"))
    if D.get("linha") == "gastro" and not P.get("fodmap"):
        msgs.append(("erro", "linha gastro sem plano.fodmap (nao, fase1, fase2, fase3)"))
    dv = P.get("dias_validade") or 0
    if fase == "pausa" and not 7 <= dv <= 14:
        msgs.append(("aviso", f"pausa com {dv} dias de validade (o combinado é 7 a 14)"))
    elif fase != "pausa" and dv != 30:
        msgs.append(("aviso", f"{dv} dias de validade (o padrão é 30)"))

    # --- textos que o aluno lê
    for i, t in enumerate(P.get("o_que_muda") or []):
        texto_leigo(f"o_que_muda[{i + 1}]", t, msgs)
    for k in ("livre_teto_texto", "fator_atividade_texto"):
        texto_leigo(k, P.get(k), msgs)
    for i, t in enumerate(P.get("avisos") or []):
        texto_leigo(f"avisos[{i + 1}]", t, msgs)
    for s in P.get("suplementacao") or []:
        texto_leigo(f"suplemento {s.get('suplemento')}", f"{s.get('para_que', '')} {s.get('quando', '')}", msgs)
    for k in ("acertos", "atencao", "melhorar"):
        for i, t in enumerate(R.get(k) or []):
            texto_leigo(f"relatorio.{k}[{i + 1}]", t, msgs)
    for m in R.get("metas") or []:
        texto_leigo("relatorio.metas", m.get("texto"), msgs)
    rec = R.get("recapitulacao") or {}
    for t in (rec.get("feito") or []) + (rec.get("nao_atingido") or []):
        texto_leigo("relatorio.recapitulacao", t, msgs)

    resumo = {"dias": [(rot, round(t["kcal"]), round(t["proteina_g"]), round(t["carboidrato_g"]), round(t["gordura_g"]),
                        round(t["fibra_g"], 1), round(t["saturada_g"], 1), n) for rot, t, n, _ in dias],
              "media_semana": round(media), "livre": livre_txt, "sat_pct": round(sat_pct, 1), "fibra_meta": round(fibra_meta)}
    if gravar and not P.get("fibra_g"):
        P["fibra_g"] = round(base_dia["fibra_g"])
    return fechar(msgs, resumo, P, gravar)


def fechar(msgs, resumo, P, gravar):
    niveis = [m[0] for m in msgs]
    resultado = "trava" if "trava" in niveis else "erro" if "erro" in niveis else "aviso" if "aviso" in niveis else "ok"
    if gravar:
        P["conferencia"] = {"resultado": resultado, "mensagens": [f"{n}: {t}" for n, t in msgs if n != "info"],
                            "em": datetime.datetime.now().isoformat(timespec="seconds")}
    return resultado, msgs, resumo


def imprimir(resultado, msgs, resumo, P):
    for rot, k, p, c, g, f, s, n in resumo.get("dias", []):
        print(f"{rot} ({n} dia(s) na semana): {br(k)} kcal · P {p} g · C {c} g · G {g} g · fibra {br(f, 1)} g · saturada {br(s, 1)} g")
    if resumo:
        print(f"Média da semana: {br(resumo['media_semana'])} kcal{resumo['livre']} · plano: {br(float(P.get('kcal_dia') or 0))} kcal")
        print(f"Meta de fibra: {resumo['fibra_meta']} g · saturada: {br(resumo['sat_pct'], 1)}% das kcal")
        for r in P.get("refeicoes", []):
            print(f"  {r.get('horario', ''):>5} {r.get('nome_exibicao', '')[:34]:<34} {r.get('kcal', 0):>5} kcal · "
                  f"P {r.get('proteina_g', 0)} · C {r.get('carboidrato_g', 0)} · G {r.get('gordura_g', 0)} · fibra {br(r.get('_fibra_g', 0), 1)}")
    print(f"\nCONFERÊNCIA: {resultado.upper()}")
    for n, t in msgs:
        print(f"  [{n}] {t}")


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("energia")
    e.add_argument("--sexo", required=True)
    e.add_argument("--idade", type=float, required=True)
    e.add_argument("--altura", type=float, required=True, help="cm")
    e.add_argument("--peso", type=float, required=True, help="kg (peso de tendência)")
    e.add_argument("--fa", type=float, required=True, help="fator de atividade")
    e.add_argument("--deficit", type=float)
    e.add_argument("--proteina", type=float, help="g/kg")
    e.add_argument("--gordura", type=float, help="g/kg")
    c = sub.add_parser("conferir")
    c.add_argument("json")
    c.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    if a.cmd == "energia":
        energia(a)
    elif a.cmd == "conferir":
        dados = json.load(open(a.json, encoding="utf-8"))
        res, msgs, resumo = conferir(dados, a.gravar)
        imprimir(res, msgs, resumo, dados["plano"])
        if a.gravar:
            for r in dados["plano"].get("refeicoes", []):
                r.pop("_fibra_g", None), r.pop("_saturada_g", None)
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=1)
            print("\n(números e conferência gravados no JSON)")
        sys.exit({"ok": 0, "aviso": 0, "erro": 1, "trava": 0 if dados["plano"].get("justificativa_rt") else 2}[res])
    else:
        ap.print_help()
