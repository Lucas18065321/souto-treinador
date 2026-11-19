#!/usr/bin/env python3
"""Plano alimentar da consultoria Souto Treinador (prescrição dietética do nutricionista RT):
JSON → HTML (gráficos interativos) → PDF A4, no Chrome local, sem token e sem internet.

Uso:
  python montar_plano.py exemplo-ficticio.json
  python montar_plano.py dados.json --saida PASTA [--modelo b] [--so-html] [--png] [--mostrar-numeros]

Entrada: um JSON com 4 blocos (o README diz de qual campo sai cada seção):
  documento  dados do envio: nome, linha, treino, datas, dia do check-in, chave "mostrar números"
  plano      o plano.json do agente /montar-dieta (contrato 1.7.2 de Módulos/Planos e materiais.md)
  relatorio  textos de leitura aprovados pelo RT (recapitulação, último mês, metas)
  evolucao   séries salvas no Supabase para os gráficos (planos, peso, adesão, treino, sintomas)
Textos fixos (cocção, conservação, alarmes, como usar): textos-padrao.json, nesta pasta.

Saída: "Plano alimentar v{n} - {primeiro nome} - AAAA-MM-DD" em .html (com dica ao passar o mouse nos gráficos)
e .pdf (estático). --png grava a prévia de cada página do PDF (pasta png/, descartável).
Seção sem dado some: nunca sai gráfico ou quadro vazio.

Marca, CREF, @ e o bloco do RT vêm de ../../config-st.json (um arquivo só, com os TROCAR).
A assinatura do RT é uma IMAGEM fora do repositório (%USERPROFILE%\\SoutoTreinador\\privado\\assinatura-rt.png,
ou a variável ST_ASSINATURA_RT). Sem ela, o PDF sai com a linha "assinatura do nutricionista RT" e um aviso.
"""
import argparse
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

sys.dont_write_bytecode = True  # zero lixo: sem __pycache__
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, "..", "..", "comum")))
import graficos  # noqa: E402
import config_st  # noqa: E402

LOGO = os.path.join(AQUI, "logo.png") if os.path.exists(os.path.join(AQUI, "logo.png")) else config_st.logo("branco")
FONTES_WEB = ("https://fonts.googleapis.com/css2?family=Inter+Tight:wght@100..900"
              "&family=Bricolage+Grotesque:opsz,wght@12..96,200..800&display=swap")
FONTES = [("Inter Tight", "normal", "100 900", "InterTight.woff2"),                 # texto
          ("Bricolage Grotesque", "normal", "200 800", "BricolageGrotesque.woff2")]  # capa, títulos e números
MARCA, PROF, RT = config_st.MARCA, config_st.PROF, config_st.RT
AVISOS = []   # o que o script avisa no fim (ex.: assinatura do RT ausente)
TOTAL_PAGINAS = "__TOTAL_PAGINAS__"   # trocado pelo total de páginas na 2ª passada do PDF (rodapé da capa)
DIAS_CURTOS = {"segunda": "seg", "terça": "ter", "quarta": "qua", "quinta": "qui", "sexta": "sex", "sábado": "sáb", "domingo": "dom"}


# ---------- utilitários ----------
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def data_br(iso):
    if not iso:
        return ""
    a, m, d = str(iso)[:10].split("-")
    return f"{d}/{m}/{a}"


def num(v, casas=0):
    s = f"{float(v):,.{casas}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def qtd(v):
    v = float(v)
    return num(v, 0 if v.is_integer() else 1)


def chave(s):
    s = unicodedata.normalize("NFD", str(s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def e_lista(*itens):
    itens = [i for i in itens if i]
    if len(itens) <= 1:
        return "".join(itens)
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def sem_quebra(texto):
    """Palavra com hífen não quebra no meio ("pré-treino")."""
    return re.sub(r"(\S*-\S*)", r"<span style='white-space:nowrap'>\1</span>", esc(texto))


def lista(itens, classe="lista"):
    itens = [i for i in (itens or []) if i]
    return f"<ul class='{classe}'>" + "".join(f"<li>{esc(i)}</li>" for i in itens) + "</ul>" if itens else ""


def data_uri(caminho, tipo):
    with open(caminho, "rb") as f:
        return f"data:{tipo};base64," + base64.b64encode(f.read()).decode()


class Capitulos:
    """Numera só os capítulos que existem (seção sem dado some e não deixa buraco na numeração)."""
    def __init__(self):
        self.n = 0

    def olho(self, texto):
        self.n += 1
        return f"<div class='olho'>{self.n:02d} · {esc(texto)}</div>"


def titulo(cap, olho, h2, guia=""):
    guia_html = f"<p class='guia'>{guia}</p>" if guia else ""
    return f"<div class='cabeca'>{cap.olho(olho)}<h2>{h2}</h2><div class='barra'></div>{guia_html}</div>"


# ---------- seções ----------
def capa(D, P, T, logo):
    fase = T["fases"].get(P.get("fase"), "")
    ficticio = "<div class='capa-ficticio'>Exemplo fictício</div>" if D.get("ficticio") else ""
    marca = f"<div class='capa-marca' style=\"background-image:url('{logo}')\"></div>" if logo else ""
    logo_div = f"<div class='capa-logo' style=\"background-image:url('{logo}')\"></div>" if logo else "<div></div>"
    dados = [("Versão", f"{P['versao']}"), ("Vale de", f"{data_br(D['inicio'])} a {data_br(D['validade'])}")]
    if fase:
        dados.append(("Momento", fase))
    dados_html = "".join(f"<div class='capa-dado'><span>{esc(r)}</span><b>{esc(v)}</b></div>" for r, v in dados)
    return f"""<section class='capa'>{marca}
<div class='capa-topo'>{logo_div}{ficticio}</div>
<div class='capa-miolo'>
  <div class='capa-sobre'>Consultoria {esc(MARCA['nome'])}</div>
  <h1>Seu plano<br><em>alimentar</em></h1>
  <div class='capa-nome'>{esc(D['aluno_nome'])}</div>
  <div class='capa-dados'>{dados_html}</div>
</div>
<div class='capa-rodape'><div><strong>{esc(PROF['nome'])}</strong>{esc(PROF['profissao'])} · {esc(PROF['registro'])}</div><div class='arroba'>{esc(PROF['arroba'])}</div></div>
<div class='capa-pe'><span>{esc(config_st.rodape_profissional())}<br>{esc(RT['linha_documento'])}</span><span>Documento individual de {esc(D['primeiro_nome'])}<br>página 1 de __TOTAL_PAGINAS__</span></div>
</section>"""


def evolucao(cap, D, P, E, modelo="a", mostrar=True):
    if not E:
        return ""
    blocos = graficos.todos(E, D, P, modelo, mostrar)
    if not blocos:
        return ""
    per = E.get("periodo") or {}
    sub = f"De {data_br(per.get('inicio'))} a {data_br(per.get('fim'))}. " if per.get("inicio") else ""
    guia = esc(sub + "A linha tracejada marca cada troca de plano (v1, v2…).") + (
        "<span class='so-tela'> Passe o dedo ou o mouse num ponto para ver a data, o valor e o plano daquela semana.</span>")
    return f"<section class='cap'>{titulo(cap, 'Anexos de evolução', 'Sua evolução <em>até aqui</em>', guia)}{blocos}</section>"


def recapitulacao(cap, R):
    rc = (R or {}).get("recapitulacao") or {}
    if not (rc.get("feito") or rc.get("nao_atingido")):
        return ""
    guia = f"O que fizemos juntos {esc(rc['periodo'])}." if rc.get("periodo") else ""
    feito = f"<div class='painel'><div class='rot'>O que foi feito</div><div style='height:3mm'></div>{lista(rc.get('feito'))}</div>" if rc.get("feito") else ""
    nao = (f"<div class='painel creme'><div class='rot'>O que ainda não foi atingido</div><div style='height:3mm'></div>"
           f"{lista(rc.get('nao_atingido'), 'lista neutra')}</div>") if rc.get("nao_atingido") else ""
    return f"<div class='sec'>{titulo(cap, 'Recapitulação', 'O caminho <em>até aqui</em>', guia)}<div class='duas'>{feito}{nao}</div></div>"


def ultimo_mes(cap, R, P):
    R = R or {}
    linhas = [("Pontos acertados", R.get("acertos")), ("Pontos de atenção", R.get("atencao")), ("Pontos a melhorar", R.get("melhorar"))]
    linhas = [(r, l) for r, l in linhas if l]
    if not linhas:
        return ""
    if P.get("tipo_versao") == "repeticao":
        h2, guia = "Por que vamos <em>manter o plano</em>", esc(R.get("por_que_manter", ""))
    else:
        h2, guia = "Como foi o <em>último mês</em>", ""
    corpo = "".join(f"<div class='leitura-linha'><div class='rot'>{esc(r)}</div><div>{lista(l)}</div></div>" for r, l in linhas)
    return f"<div class='sec'>{titulo(cap, 'Último mês', h2, guia)}<div class='leitura'>{corpo}</div></div>"


def como_usar(cap, T):
    return f"<div class='sec'>{titulo(cap, 'Antes de começar', 'Como usar o <em>seu plano</em>')}{lista(T['como_usar'])}</div>"


def avisos(P, primeiro):
    """Combinados e avisos só deste aluno (plano.avisos), aprovados pelo RT com o plano."""
    av = P.get("avisos") or []
    if not av:
        return ""
    return f"<div class='sec'><h3>{'Para este primeiro mês' if primeiro else 'Para este mês'}</h3>{lista(av)}</div>"


def metas(cap, D, P, R, T):
    ms = (R or {}).get("metas") or []
    muda = P.get("o_que_muda") or []
    if isinstance(muda, str):
        muda = [muda]
    if not ms and not muda:
        return ""
    out = ""
    if ms:
        def tipo(m):
            return f"<span class='chip'>{esc(m['tipo'])}</span>" if m.get("tipo") else ""

        def prazo(m):
            pr = m.get("prazo") or D["validade"]
            return "" if pr == D["validade"] else f"<b>até {data_br(pr)}</b>"
        itens = "".join(
            f"<div class='meta'><div class='meta-n'>{i}</div><div>{esc(m['texto'])}</div>"
            f"<div class='meta-tipo'>{tipo(m)}{prazo(m)}</div></div>"
            for i, m in enumerate(ms, 1))
        out += (f"<div class='sec inteira'>{titulo(cap, 'Metas do novo plano', f'Suas metas até <em>{data_br(D['validade'])}</em>')}"
                f"<div class='metas'>{itens}</div><p class='combinado'>{esc(T['frase_metas'])}</p></div>")
    if muda and P.get("versao", 1) > 1:
        out += f"<div class='sec'><h3>O que muda no plano</h3>{lista(muda[:3])}</div>"
    return out


def seu_dia(D, P):
    itens = [(r.get("horario", ""), r["nome_exibicao"], "", r.get("tipo_dia", "todos")) for r in P["refeicoes"]]
    tr = D.get("treino") or {}
    if D.get("tem_treino") and tr.get("horario"):
        dias = e_lista(*[DIAS_CURTOS.get(chave(d).replace("-feira", ""), d) for d in tr.get("dias", [])])
        itens.append((tr["horario"], "Treino", dias, "treino_marca"))
    itens.sort(key=lambda x: x[0] or "99")
    cel = []
    for hora, nome, extra, tipo in itens:
        m = re.match(r"^(.*?)\s*\((.+)\)$", nome)
        if m and not extra:
            nome, extra = m.group(1), m.group(2)
        classe = " treino" if tipo == "treino_marca" else ""
        extra_html = f"<div class='op-det'>{esc(extra)}</div>" if extra else ""
        if tipo in ("treino", "descanso"):
            extra_html = f"<div class='op-det'>{'só em dia de treino' if tipo == 'treino' else 'só em dia sem treino'}</div>"
        cel.append(f"<div class='dia-item{classe}'><div class='dia-hora'>{esc(hora.replace(':', 'h') if hora else '')}</div>"
                   f"<div class='dia-nome'>{sem_quebra(nome)}</div>{extra_html}</div>")
    return f"<div class='dia' style='--n:{len(cel)}'>{''.join(cel)}</div>"


def opcao(o, base):
    g = o.get("gramas")
    marca = "<span class='op-marca'></span>"
    if g in (None, ""):
        quanto, det = o.get("medida_caseira", ""), o.get("preparo", "")
    else:
        quanto = f"{qtd(g)} {o.get('unidade', 'g')}"
        det = " · ".join(x for x in (o.get("medida_caseira"), o.get("preparo")) if x)
    det_html = f"<span class='op-det'>{esc(det)}</span>" if det else ""
    return (f"<div class='op{' base' if base else ''}'>{marca}<span class='op-nome'>{esc(o['alimento'])}</span>"
            f"<span class='op-g'>{esc(quanto)}</span>{det_html}</div>")


def refeicao(r, grupos):
    blocos = []
    for it in r["itens"]:
        g = grupos.get(it.get("grupo_substituicao"))
        if g:
            outras = [o for o in [g["base"]] + g.get("equivalentes", []) if chave(o["alimento"]) != chave(it["alimento"])]
            blocos.append({"rot": g.get("nome_exibicao") or g["grupo"], "ops": [it] + outras, "grupo": True})
        else:
            cat = it.get("categoria", "")
            if blocos and not blocos[-1]["grupo"] and blocos[-1]["rot"] == cat:
                blocos[-1]["ops"].append(it)
            else:
                blocos.append({"rot": cat, "ops": [it], "grupo": False})
    linhas = []
    for b in blocos:
        n = len(b["ops"])
        escolha = f"<small>escolha 1 de {n}</small>" if b["grupo"] and n > 1 else ""
        ops = "".join(opcao(o, i == 0 or not b["grupo"]) for i, o in enumerate(b["ops"]))
        um = " um" if (not b["grupo"] or n == 1) else ""
        linhas.append(f"<div class='grp'><div class='grp-rot rot'>{esc(b['rot'])}{escolha}</div><div class='ops{um}'>{ops}</div></div>")
    tag = {"treino": "só em dia de treino", "descanso": "só em dia sem treino"}.get(r.get("tipo_dia"), "")
    tag_html = f"<span class='ref-tag'>{tag}</span>" if tag else ""
    hora = (r.get("horario") or "").replace(":", "h")
    return (f"<article class='ref'><div class='ref-topo'><span class='ref-hora'>{esc(hora)}</span>"
            f"<span class='ref-nome'>{esc(r['nome_exibicao'])}</span>{tag_html}</div>{''.join(linhas)}</article>")


def plano_alimentar(cap, D, P, T):
    grupos = {g["grupo"]: g for g in P.get("substituicoes", [])}
    legenda = ("<div class='legenda-ops'><span><span class='op-marca' style='border:0;background:var(--degrade)'></span>sugestão do plano</span>"
               "<span><span class='op-marca'></span>troca de mesmo valor</span></div>")
    refs = "".join(refeicao(r, grupos) for r in sorted(P["refeicoes"], key=lambda r: r.get("horario") or "99"))
    aviso = f"<div class='aviso-peso'><div class='selo'>g</div><div>{esc(T['pronto_para_consumo'])}</div></div>"
    return (f"<section class='cap'>{titulo(cap, 'Plano alimentar', 'Seu <em>dia</em>')}{seu_dia(D, P)}{aviso}"
            f"<h3>Suas refeições</h3>{legenda}{refs}</section>")


def calculo(cap, D, P, T):
    """Como montei seu plano: a conta do gasto em blocos, a divisão das calorias e a água, com notas de rodapé."""
    C, F = T["calculo"], T["fontes"]
    notas = []

    def nota(k):
        if k not in F:
            return ""
        if k not in notas:
            notas.append(k)
        return f"<sup>{notas.index(k) + 1}</sup>"

    kcal, get, fa, peso = P["kcal_dia"], P.get("get_kcal"), P.get("fator_atividade"), P.get("peso_usado_kg")
    metodo, fase = P.get("get_metodo"), P.get("fase")
    redondo = lambda v: num(round(float(v) / 10) * 10)  # noqa: E731
    itens = []
    if metodo == "mifflin_fa" and get and fa:
        tmb = P.get("tmb_kcal") or round(get / fa)
        itens += [("Gasto em repouso", num(tmb), "calorias, " + C["repouso"] + nota("mifflin_fa"), ""), "×",
                  ("Atividade", num(fa, 3).rstrip("0").rstrip(","), esc(P.get("fator_atividade_texto", "")), ""), "="]
    if get:
        itens.append(("Gasto do dia", "≈ " + redondo(get), "calorias", ""))
        dif = float(get) - float(kcal)
        if fase == "deficit" and dif > 0:
            itens += ["−", ("Ajuste", redondo(dif), "calorias a menos, para emagrecer", "")]
        elif fase == "superavit" and dif < 0:
            itens += ["+", ("Ajuste", redondo(-dif), "calorias a mais, para ganhar massa", "")]
        itens.append("=")
    itens.append(("Seu plano", num(kcal), "calorias por dia, na média da semana", " fim"))
    conta = "".join(f"<div class='conta-op'>{i}</div>" if isinstance(i, str) else
                    f"<div class='conta-item{i[3]}'><span class='rot'>{esc(i[0])}</span><b>{esc(i[1])}</b><span>{i[2]}</span></div>"
                    for i in itens)
    linhas = [esc(C["metodos"].get(metodo, "")) + (nota(metodo) if metodo in F else ""), esc(C["mesmo_metodo"])]
    if D.get("tem_treino") and fase == "deficit":
        linhas.append(esc(C["deficit_treino"]) + nota("deficit_treino"))
    soma = sum(r.get("kcal") or 0 for r in P.get("refeicoes", []) if r.get("tipo_dia", "todos") == "todos")
    if P.get("livre_prevista") and soma and abs(soma - kcal) > 20:
        linhas.append(f"Os {num(kcal)} são a média da semana, já contando a refeição livre: num dia comum, o plano soma cerca de {redondo(soma)} calorias.")
    explica = "<p>" + " ".join(l for l in linhas if l) + "</p>"   # um parágrafo só: a página cabe numa folha com as notas

    macros = [("Proteína", "proteina", P["proteina_g"], 4), ("Carboidrato", "carboidrato", P["carboidrato_g"], 4),
              ("Gordura", "gordura", P["gordura_g"], 9)]
    total = sum(g * f for _, _, g, f in macros)
    barra, cols, fr = "", "", []
    for nome, k, g, f in macros:
        pct = round(g * f / total * 100)
        fr.append(f"{g * f}fr")
        barra += f"<span style='flex:{g * f}'>{nome} {pct}%</span>"
        por_kg = f"{num(g / peso, 1)} g por kg · " if peso else ""
        sup = nota("proteina_treino") if k == "proteina" and D.get("tem_treino") else ""
        cols += (f"<div class='macro'><span class='rot'>{nome}</span><b>{qtd(g)} g</b>"
                 f"<span>{por_kg}{pct}% das calorias{sup}</span><span class='macro-faz'>{esc(C['macros'][k])}</span></div>")
    fibra = (f"<div class='painel'><span class='rot'>Fibra</span><b class='num-calc'>{qtd(P['fibra_g'])} g</b>"
             f"<p>por dia, para o intestino.</p></div>") if P.get("fibra_g") else ""

    agua = ""
    if P.get("meta_agua_l"):
        l = float(P["meta_agua_l"])
        conta_agua = (f"{qtd(P['agua_ml_por_kg'])} mL por kg × {num(peso, 1)} kg = {num(P['agua_ml_por_kg'] * peso / 1000, 2)} litros, "
                      f"arredondado para {qtd(l)}") if P.get("agua_ml_por_kg") and peso else ""
        agua = (f"<div class='painel'><span class='rot'>Água</span><b class='num-calc'>{qtd(l)} litros</b>"
                f"<p>por dia, cerca de {round(l * 1000 / 250)} copos de 250 mL.</p>"
                + (f"<p class='guia'>{esc(conta_agua)}.</p>" if conta_agua else "")
                + f"<p class='guia'>{esc(C['agua'])}</p></div>")
    rodape = ("<ol class='notas'>" + "".join(f"<li>{esc(F[k])}</li>" for k in notas) + "</ol>") if notas else ""
    return (f"<section class='cap calc'>{titulo(cap, 'Seus números', 'Como montei <em>seu plano</em>', esc(C.get('guia_fase', {}).get(fase, C['guia'])))}"
            f"<div class='sec inteira'><h3>O gasto e o plano</h3><div class='conta'>{conta}</div><div class='explica'>{explica}</div></div>"
            f"<div class='sec inteira'><h3>Como as calorias se dividem</h3><div class='macro-barra'>{barra}</div>"
            f"<div class='macros' style='--cols:{' '.join(f'minmax(44mm, {x})' for x in fr)}'>{cols}</div></div>"
            + (f"<div class='sec inteira'><div class='agua-fibra{' duas' if agua and fibra else ''}'>{agua}{fibra}</div></div>" if agua or fibra else "")
            + f"{rodape}</section>")


def extras(cap, D, P, T, mostrar):
    partes = []
    if P.get("livre_prevista"):
        n = float(P.get("livre_por_semana") or 1)  # 0,5 = 1 a cada 15 dias (2026-11-15)
        quantas = "1 a cada 15 dias" if n == 0.5 else (f"{int(n)} por semana" if n > 1 else "1 por semana")
        fatos = [("Quantas", quantas)]
        if P.get("livre_dias"):
            fatos.append(("Dia sugerido", e_lista(*P["livre_dias"])))
        if P.get("livre_substitui_texto") or P.get("livre_substitui"):  # _texto: quando troca mais de uma refeição
            fatos.append(("No lugar de", (P.get("livre_substitui_texto") or P["livre_substitui"]).lower()))
        fatos_html = "".join(f"<div class='fato'><span class='rot'>{esc(r)}</span><b>{esc(v)}</b></div>" for r, v in fatos)
        teto = f"<p><b>Até onde vai:</b> {esc(P['livre_teto_texto'])}.</p>" if P.get("livre_teto_texto") else ""
        if mostrar and P.get("livre_teto_kcal"):
            teto += f"<p class='nota-graf'>Cerca de {num(P['livre_teto_kcal'])} calorias.</p>"
        partes.append(f"<div class='sec'><h3>Refeição livre</h3><div class='painel'><div class='fatos'>{fatos_html}</div>{teto}</div></div>")
    if P.get("meta_agua_l") and not mostrar:  # com os números ligados, a água sai em "Como montei seu plano"
        l = float(P["meta_agua_l"])
        copos = round(l * 1000 / 250)
        partes.append(f"<div class='sec'><h3>Água</h3><div class='agua'><b>{qtd(l)} litros</b><span>por dia, cerca de {copos} copos de 250 mL. "
                      f"Café e chá sem açúcar contam; refrigerante e suco, não.</span></div></div>")
    sup = [s for s in P.get("suplementacao") or [] if s.get("situacao") != "suspenso"]
    if sup:
        linhas = ""
        for s in sup:
            chip = f"<span class='chip'>{esc(s['situacao'])}</span>" if s.get("situacao") in ("novo", "ajustado") else ""
            quanto = f"{qtd(s['dose'])} {s.get('unidade', '')}".strip() + (f" ({s['medida_caseira']})" if s.get("medida_caseira") else "")
            linhas += (f"<tr><td data-rot='Suplemento'>{esc(s['suplemento'])}{chip}</td><td data-rot='Quanto'>{esc(quanto)}</td>"
                       f"<td data-rot='Quando'>{esc(s.get('quando', ''))}</td><td data-rot='Para quê'>{esc(s.get('para_que', ''))}</td></tr>")
        partes.append("<div class='sec'><h3>Suplementação</h3><table class='tab tab-sup'><colgroup><col style='width:24%'>"
                      "<col style='width:22%'><col style='width:28%'><col style='width:26%'></colgroup><thead><tr><th>Suplemento</th>"
                      f"<th>Quanto</th><th>Quando</th><th>Para quê</th></tr></thead><tbody>{linhas}</tbody></table></div>")
    if not partes:
        return ""
    h2 = "Refeição livre e <em>suplementos</em>" if mostrar else "Livre, água e <em>suplementos</em>"
    return f"<section class='cap'>{titulo(cap, 'Para o dia a dia', h2)}{''.join(partes)}</section>"


def cozinha(cap, T):
    c = T["conservacao"]
    return (f"<section class='cap'>{titulo(cap, 'Na cozinha', 'Preparo e <em>marmitas</em>')}"
            f"<div class='sec'><h3>Como preparar sem gordura sobrando</h3>{lista(T['coccao'])}</div>"
            f"<div class='sec'><h3>Como guardar as marmitas</h3><div class='duas'>"
            f"<div class='painel'><div class='rot'>Na geladeira</div><div style='height:3mm'></div>{lista(c['geladeira'])}</div>"
            f"<div class='painel'><div class='rot'>No congelador</div><div style='height:3mm'></div>{lista(c['congelador'])}</div>"
            f"</div></div></section>")


def assinatura_rt_html():
    """A imagem da assinatura do RT, embutida no documento. Fica FORA do repositório; sem ela, sai a linha para assinar."""
    caminho = config_st.assinatura_rt()
    if caminho:
        tipo = "image/png" if caminho.lower().endswith(".png") else "image/jpeg"
        return f"<div class='assinatura-img'><img src='{data_uri(caminho, tipo)}' alt='Assinatura do nutricionista RT'></div>"
    AVISOS.append("assinatura do RT não encontrada (" + os.path.join(config_st.pasta_privada(), "assinatura-rt.png")
                  + "): o PDF saiu com a linha \"assinatura do nutricionista RT\". Não envie assim.")
    return "<div class='assinatura-falta'>assinatura do nutricionista RT</div>"


def fechamento(cap, D, T, logo):
    sinais = T["alarme"].get(D.get("linha"), T["alarme"]["emagrecimento"])
    checkin = T["checkin"].replace("{dia}", D.get("dia_checkin", ""))
    logo_ass = f"<div class='assinatura-selo'><span style=\"background-image:url('{logo}')\"></span></div>" if logo else ""
    data = data_br(D.get("data_assinatura") or D["inicio"])
    prof = (f"<div class='assinatura-bloco'>{logo_ass}<div class='assinatura-papel'>Acompanhamento e treino</div>"
            f"<div class='assinatura-linha'><strong>{esc(PROF['nome'])}</strong><span>{esc(PROF['profissao'])} · {esc(PROF['registro'])}</span>"
            f"<span>{esc(PROF['arroba'])}</span></div></div>")
    rt = (f"<div class='assinatura-bloco bloco-rt'><div class='assinatura-papel'>Prescrição dietética · Responsável Técnico</div>"
          f"{assinatura_rt_html()}<div class='assinatura-linha'><strong>{esc(RT['nome'])}</strong>"
          f"<span>{esc(RT['profissao'])} · {esc(RT['registro'])}</span><span>{data}</span></div></div>")
    nota = (f"<p class='nota-rt'>{esc(RT['linha_documento'])}. O plano alimentar é prescrição do nutricionista responsável técnico "
            f"(ato privativo do nutricionista, Lei 8.234/1991); o acompanhamento do treino é de {esc(PROF['nome'])}, "
            f"{esc(PROF['profissao'].lower())}.</p>")
    return (f"<section class='cap'>{titulo(cap, 'Sinais de alerta', 'Quando procurar <em>ajuda na hora</em>')}"
            f"<div class='sec alarme'><p class='acao'>{esc(T['alarme']['acao'])}</p><p>{esc(T['alarme']['intro'])}</p>{lista(sinais)}</div>"
            f"<div class='sec'><h3>Seu check-in</h3><p>{esc(checkin)}</p></div>"
            f"<div class='assinaturas'>{prof}{rt}</div>{nota}</section>")


# ---------- montagem ----------
def css_pagina(D, T, modelo="a"):
    """Rodapé de toda página: a marca e o profissional + a linha da prescrição dietética do RT (2 linhas)."""
    esq = config_st.rodape_profissional() + "\\A " + RT["linha_documento"]
    dir_ = f"Documento individual de {D['primeiro_nome']} · página "
    q = lambda s: '"' + s.replace('"', '\\"') + '"'  # noqa: E731
    cor = "#9BA3BA" if modelo == "b" else "#5A6075"
    caixa = f"font-family:'Inter Tight','Segoe UI',Arial,sans-serif;font-size:7.5pt;line-height:1.35;color:{cor};white-space:pre;"
    fundo = " background: #0B0B0E;" if modelo == "b" else ""  # modelo B: página escura de ponta a ponta
    fundo_capa = "#0B0B0E" if modelo == "b" else "#141A3D"   # cor do pé da capa: pinta o fio que sobra embaixo
    return f"""@page {{ size: A4; margin: 16mm 16mm 20mm 16mm;{fundo}
  @bottom-left {{ content: {q(esq)}; {caixa} vertical-align: middle; }}
  @bottom-right {{ content: {q(dir_)} counter(page) " de " counter(pages); {caixa} vertical-align: middle; }} }}
@page capa {{ margin: 0; background: {fundo_capa}; @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}"""


def fontes_css():
    """Fontes de fontes/ embutidas no HTML (o PDF sai igual sem internet). Faltou arquivo: puxa do Google Fonts."""
    pasta = os.path.join(AQUI, "fontes")
    if all(os.path.exists(os.path.join(pasta, a)) for *_, a in FONTES):
        faces = [f"@font-face{{font-family:'{fam}';font-style:{estilo};font-weight:{peso};font-display:block;"
                 f"src:url({data_uri(os.path.join(pasta, arq), 'font/woff2')}) format('woff2')}}"
                 for fam, estilo, peso, arq in FONTES]
        return "", "\n".join(faces)
    return f"<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin><link rel='stylesheet' href='{FONTES_WEB}'>", ""


def montar(dados, mostrar_numeros=False, modelo="a"):
    """modelo "a" = claro (padrão aprovado) · "b" = escuro (plano-b.css por cima do plano.css)."""
    with open(os.path.join(AQUI, "textos-padrao.json"), encoding="utf-8") as f:
        T = json.load(f)
    css = ""
    for arq in ("plano.css", "plano-b.css") if modelo == "b" else ("plano.css",):
        with open(os.path.join(AQUI, arq), encoding="utf-8") as f:
            css += f.read() + "\n"
    D, P, R, E = dados["documento"], dados["plano"], dados.get("relatorio") or {}, dados.get("evolucao") or {}
    mostrar = bool(mostrar_numeros or D.get("mostrar_numeros"))
    logo = data_uri(LOGO, "image/png") if LOGO else ""
    primeiro = P.get("versao", 1) == 1 or P.get("tipo_versao") == "primeiro"
    cap = Capitulos()
    partes = [capa(D, P, T, logo), evolucao(cap, D, P, E, modelo, mostrar)]
    abertura = como_usar(cap, T) if primeiro else recapitulacao(cap, R) + ultimo_mes(cap, R, P)
    abertura += avisos(P, primeiro) + metas(cap, D, P, R, T)
    if abertura:
        partes.append(f"<section class='cap'>{abertura}</section>")
    partes += [calculo(cap, D, P, T) if mostrar else "", plano_alimentar(cap, D, P, T), extras(cap, D, P, T, mostrar),
               cozinha(cap, T), fechamento(cap, D, T, logo)]
    link_fontes, faces = fontes_css()
    with open(os.path.join(AQUI, "interacao.js"), encoding="utf-8") as f:
        js = f.read()
    rodape_tela = (f"<footer class='rodape-tela'>{esc(config_st.rodape_profissional())}<br>{esc(RT['linha_documento'])}<br>"
                   f"Documento individual de {esc(D['primeiro_nome'])}</footer>")
    titulo_doc = f"Plano alimentar v{P['versao']} - {D['primeiro_nome']} - {D['inicio']}"
    classe = " class='modelo-b'" if modelo == "b" else ""
    return f"""<!doctype html>
<html lang="pt-BR"{classe}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo_doc)}</title>{link_fontes}
<style>{faces}
{css}
{css_pagina(D, T, modelo)}</style></head>
<body><main class="doc">{''.join(p for p in partes if p)}{rodape_tela}</main>
<div class="dica" id="dica"></div>
<script>{js}</script></body></html>""", titulo_doc


def chrome():
    c = config_st.chrome()
    if not c:
        sys.exit("Chrome não encontrado (defina a variável CHROME com o caminho do chrome.exe).")
    return c


def imprimir(html_path, pdf_path):
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    perfil = tempfile.mkdtemp(prefix="st-chrome-")   # perfil descartável: não mexe no Chrome do dia a dia
    args = [chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
            "--no-first-run", "--no-default-browser-check", f"--user-data-dir={perfil}",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000", f"--print-to-pdf={pdf_path}", url]
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    try:
        subprocess.run(args, capture_output=True, timeout=180)
    finally:
        shutil.rmtree(perfil, ignore_errors=True)
    if not os.path.exists(pdf_path):
        sys.exit("O Chrome não gerou o PDF.")


def contar_paginas(pdf_path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf_path).pages)
    except Exception:
        with open(pdf_path, "rb") as f:
            return len(re.findall(rb"/Type\s*/Page[^s]", f.read()))


def prevista_png(pdf_path, pasta):
    ps1 = os.path.join(AQUI, "pdf_para_png.ps1")
    subprocess.run(["powershell", "-MTA", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1, "-Pdf", pdf_path,
                    "-OutDir", pasta, "-Largura", "1240"], capture_output=True, timeout=180)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--saida", help="pasta de saída (padrão: a pasta do JSON)")
    ap.add_argument("--so-html", action="store_true", help="não gera o PDF")
    ap.add_argument("--png", action="store_true", help="grava a prévia de cada página do PDF em png/")
    ap.add_argument("--modelo", choices=["a", "b"], help="passa por cima de documento.modelo do JSON (a = claro, padrão · b = escuro)")
    ap.add_argument("--mostrar-numeros", action="store_true", help="liga 'Como montei seu plano' mesmo com a chave desligada no JSON")
    a = ap.parse_args()
    with open(a.json, encoding="utf-8") as f:
        dados = json.load(f)
    modelo = a.modelo or dados["documento"].get("modelo") or "a"   # escolha por aluno (ficha: modelo_pdf)
    doc, nome = montar(dados, a.mostrar_numeros, modelo)
    saida = os.path.abspath(a.saida or os.path.dirname(os.path.abspath(a.json)))
    os.makedirs(saida, exist_ok=True)
    h = os.path.join(saida, nome + ".html")

    def gravar(total):
        with open(h, "w", encoding="utf-8") as f:
            f.write(doc.replace(TOTAL_PAGINAS, str(total)))

    # 1ª passada conta as páginas; a 2ª escreve o total no rodapé da capa (as outras páginas contam sozinhas)
    gravar("?")
    if a.so_html:
        print("HTML:", h)
        return
    pdf = os.path.join(saida, nome + ".pdf")
    imprimir(h, pdf)
    total = contar_paginas(pdf)
    gravar(total)
    imprimir(h, pdf)
    print("HTML:", h)
    print(f"PDF:  {pdf} ({contar_paginas(pdf)} páginas)")
    if a.png:
        prevista_png(pdf, os.path.join(saida, "png"))
        print("PNG: ", os.path.join(saida, "png"))
    for av in dict.fromkeys(AVISOS):
        print("AVISO:", av)


if __name__ == "__main__":
    main()
