#!/usr/bin/env python3
"""Receituário de suplementação (prescritor: o nutricionista RT da consultoria Souto Treinador): JSON → HTML → PDF A4,
no Chrome local, sem token.

Uso:
  python montar_receita.py receita-sono.json [--saida PASTA]

Entrada (JSON): `paciente` (nome e nascimento; em branco = linha para preencher à mão), `data`, `formulas`
(composição, forma, quantidade, posologia, observação para a farmácia), `orientacoes` ao paciente, `base_legal`
e `fontes` (as notas de rodapé). O prescritor (nome, CRN, contato) vem de prescritor.json: primeiro o da pasta privada
(%USERPROFILE%/SoutoTreinador/privado/prescritor.json, com o contato profissional do RT, fora do repositório),
senão o modelo desta pasta (sem contato).
Usa as fontes, o logo e a impressão do template do plano alimentar (../template).
Saída: "Receituário - {primeiro nome ou 'em branco'} - AAAA-MM-DD" em .pdf e .html.
"""
import argparse
import json
import os
import sys

sys.dont_write_bytecode = True  # zero lixo: sem __pycache__
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "template"))
from montar_plano import LOGO, contar_paginas, data_br, data_uri, esc, fontes_css, imprimir  # noqa: E402
import config_st  # noqa: E402  (o montar_plano já pôs ../../comum no caminho)


def linha_ou_texto(valor, largura="100%"):
    return esc(valor) if valor else f"<span class='preencher' style='width:{largura}'></span>"


def cabecalho(Pr, logo):
    selo = f"<div class='selo'><span style=\"background-image:url('{logo}')\"></span></div>" if logo else ""
    contato = " · ".join(esc(c) for c in Pr.get("contato", []) if c)
    endereco = f"<div class='pr-end'>{esc(Pr['endereco'])}</div>" if Pr.get("endereco") else ""
    return (f"<header class='topo'>{selo}<div class='pr'><div class='pr-nome'>{esc(Pr['nome'])}</div>"
            f"<div class='pr-prof'>{esc(Pr['profissao'])} · <b>{esc(Pr['crn'])}</b></div>"
            f"<div class='pr-contato'>{contato}</div>{endereco}</div>"
            f"<div class='doc-tipo'><span class='rot'>Receituário</span><b>Prescrição de suplementação</b></div></header>")


def paciente(Pa, data):
    """Nome e endereço do paciente (obrigatórios: Res. CFN 656/2020 e RDC 67/2007); em branco = linha para preencher à mão."""
    return (f"<section class='paciente'><div class='campo'><span class='rot'>Paciente</span><div>{linha_ou_texto(Pa.get('nome'))}</div></div>"
            f"<div class='campo'><span class='rot'>Endereço do paciente</span><div>{linha_ou_texto(Pa.get('endereco'))}</div></div></section>")


def formula(F, i):
    comp = ""
    for c in F["componentes"]:
        det = f"<small>{esc(c['detalhe'])}</small>" if c.get("detalhe") else ""
        comp += (f"<li><span class='ativo'>{esc(c['ativo'])}{det}</span><span class='pontos'></span>"
                 f"<span class='dose'>{esc(c['dose'])}</span></li>")
    if F.get("excipiente"):
        comp += (f"<li class='exc'><span class='ativo'>{esc(F['excipiente']['nome'])}</span><span class='pontos'></span>"
                 f"<span class='dose'>{esc(F['excipiente']['quantidade'])}</span></li>")
    obs = f"<p><span class='rot'>Para a farmácia</span>{esc(F['obs_farmacia'])}</p>" if F.get("obs_farmacia") else ""
    # condições para contraindicação ou não uso: sempre no condicional ("Em caso de..."), sem supor que o paciente usa algo
    contra = ""
    if F.get("contraindicacoes"):
        itens = "".join(f"<li>{esc(c)}</li>" for c in F["contraindicacoes"])
        contra = f"<div class='contra'><span class='rot'>Condições para contraindicação ou não uso</span><ul>{itens}</ul></div>"
    return (f"<article class='formula'><div class='f-topo'><span class='f-n'>{i}</span><div><span class='rot'>{esc(F.get('uso', 'Uso oral'))}</span>"
            f"<h2>{esc(F['forma'])}</h2></div><span class='chip'>{esc(F.get('publico', 'Uso adulto'))}</span></div>"
            f"<ul class='comp'>{comp}</ul>"
            f"<div class='f-linhas'><p><span class='rot'>Mande</span>{esc(F['quantidade'])}</p>"
            f"<p><span class='rot'>Como tomar</span><b>{esc(F['posologia'])}</b></p>"
            + (f"<p><span class='rot'>Duração</span>{esc(F['duracao'])}</p>" if F.get("duracao") else "")
            + f"{obs}</div>{contra}</article>")


def orientacoes(itens):
    if not itens:
        return ""
    lis = "".join(f"<li>{esc(t)}</li>" for t in itens)
    return f"<section class='orient'><span class='rot'>Orientações para você</span><ul class='lista'>{lis}</ul></section>"


def assinatura(Pr, R):
    local = R.get("local") or ""
    data = data_br(R["data"]) if R.get("data") else ""
    local_data = ", ".join(x for x in (local, data) if x)
    digital = ("<div class='dig'><span class='rot'>Assinatura digital</span><p>Na receita enviada em PDF: certificado ICP-Brasil ou gov.br.</p></div>") if R.get("assinatura_digital", True) else "<div></div>"
    ld = esc(local_data) if local_data else "<span class='preencher' style='width:52mm'></span>"
    return (f"<section class='assina'><div class='esq'><p class='ld'><span class='rot'>Local e data</span>{ld}</p>{digital}</div>"
            f"<div class='mao'><span class='rot'>Assinatura e carimbo</span><div class='linha-ass'></div>"
            f"<strong>{esc(Pr['nome'])}</strong><span>Nutricionista · {esc(Pr['crn'])}</span></div></section>{rodape_legal(R)}")


def rodape_legal(R):
    partes = []
    if R.get("base_legal"):
        partes.append(f"<p class='legal'>{esc(R['base_legal'])}</p>")
    if R.get("fontes"):
        partes.append("".join(f"<p class='legal'>{esc(f)}</p>" for f in R["fontes"]))
    return f"<section class='rodape-legal'>{''.join(partes)}</section>" if partes else ""  # base legal | fontes, em 2 colunas


def css_pagina(Pr, primeiro):
    esq = f"Prescrição: {Pr['nome']} · Nutricionista · {Pr['crn']}\\A Consultoria {config_st.rodape_profissional()}"
    dir_ = (f"Receituário de {primeiro} · página " if primeiro else "Receituário · página ")
    q = lambda s: '"' + s.replace('"', '\\"') + '"'  # noqa: E731
    caixa = "font-family:'Inter Tight','Segoe UI',Arial,sans-serif;font-size:7.5pt;line-height:1.35;color:#5A6075;white-space:pre;"
    return (f"@page {{ size: A4; margin: 10mm 16mm 16mm 16mm; @bottom-left {{ content: {q(esq)}; {caixa} }} "
            f"@bottom-right {{ content: {q(dir_)} counter(page) \" de \" counter(pages); {caixa} }} }}")


def montar(R):
    privado = os.path.join(config_st.pasta_privada(), "prescritor.json")
    with open(privado if os.path.isfile(privado) else os.path.join(AQUI, "prescritor.json"), encoding="utf-8") as f:
        Pr = json.load(f)
    with open(os.path.join(AQUI, "receita.css"), encoding="utf-8") as f:
        css = f.read()
    logo = data_uri(LOGO, "image/png") if LOGO else ""
    Pa = R.get("paciente") or {}
    primeiro = (Pa.get("nome") or "").split(" ")[0]
    corpo = (cabecalho(Pr, logo) + paciente(Pa, R.get("data"))
             + "".join(formula(F, i) for i, F in enumerate(R["formulas"], 1))
             + orientacoes(R.get("orientacoes")) + assinatura(Pr, R))
    link_fontes, faces = fontes_css()
    nome = f"Receituário - {primeiro or 'em branco'} - {R.get('data') or 'sem data'}"
    return (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{esc(nome)}</title>{link_fontes}<style>{faces}\n{css}\n{css_pagina(Pr, primeiro)}</style></head>"
            f"<body><main class='doc'>{corpo}</main></body></html>"), nome


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--saida", help="pasta de saída (padrão: a pasta do JSON)")
    a = ap.parse_args()
    with open(a.json, encoding="utf-8") as f:
        R = json.load(f)
    doc, nome = montar(R)
    saida = os.path.abspath(a.saida or os.path.dirname(os.path.abspath(a.json)))
    os.makedirs(saida, exist_ok=True)
    h, pdf = os.path.join(saida, nome + ".html"), os.path.join(saida, nome + ".pdf")
    with open(h, "w", encoding="utf-8") as f:
        f.write(doc)
    imprimir(h, pdf)
    print("HTML:", h)
    print(f"PDF:  {pdf} ({contar_paginas(pdf)} páginas)")


if __name__ == "__main__":
    main()
