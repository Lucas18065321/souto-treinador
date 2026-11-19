#!/usr/bin/env python3
"""Banco de alimentos do agente de dieta: composição por 100 g do alimento como está descrito (cru, cozido,
grelhado...). Base: TACO 4ª ed. (NEPA/UNICAMP); a TBCA entra com `tbca`, e os rótulos de marca com `adicionar`. Sem token.

Uso:
  python alimentos.py importar-taco alimentos/taco_4ed.xlsx   (re)gera as linhas da TACO em alimentos/alimentos.json
  python alimentos.py buscar frango grelhado                   id, nome e kcal/P/C/G/fibra por 100 g (todas as palavras)
  python alimentos.py ver taco:3 taco:4                        a linha inteira de cada id
  python alimentos.py tbca peixe assado                        busca no site da TBCA (todas as palavras) e numera os achados;
                                                               no terminal, pergunta quais gravar
  python alimentos.py tbca peixe assado --gravar 1 3           grava os achados 1 e 3 (ou códigos BRC..., ou "todos")
  python alimentos.py tbca BRC0022E BRC0065J --gravar todos    grava pelos códigos da TBCA
  python alimentos.py adicionar novos.json                     acrescenta ou atualiza itens de TBCA, rótulo ou receita
  python alimentos.py conferir novos.json                      as mesmas checagens do adicionar, sem gravar nada

Formato de cada item (o mesmo em `novos.json`, numa lista):
  {"id": "tbca:BRC0001A" | "marca:rap10-integral" | "receita:sorvete-de-morango", "nome": "...",
   "grupo": "...", "fonte": "TBCA 7.3 (USP/FoRC) | rótulo do fabricante, conferido em AAAA-MM-DD | receita do RT",
   "por_100g": {"kcal": 0, "proteina_g": 0, "carboidrato_g": 0, "gordura_g": 0, "fibra_g": 0,
                "saturada_g": 0, "sodio_mg": 0}, "porcao": {"medida_caseira": "1 unidade", "gramas": 40}, "obs": "",
   "url": "página do fabricante ou foto do rótulo (só nos itens de marca)"}
Rótulo: os valores por 100 g copiados da tabela. Líquido: por 100 mL (porcao.gramas = mL; o plano conta 1 mL = 1 g,
anotado em obs). Tabela só com a porção: por 100 g = valor da porção × 100 ÷ gramas da porção, anotado em obs.
carboidrato_g é sempre o TOTAL, com a fibra (como na TACO). A TBCA e o rótulo trazem também o disponível, sem a
fibra: ele vai em carboidrato_disponivel_g (no rótulo, é o "Carboidratos" impresso; o total = esse + fibra).
Valores da TACO: "Tr" (traço) e "NA" (não se aplica) viram 0; "*" (não analisado) fica vazio (null).
Valores da TBCA: "tr" vira 0; "NA" e "-" (sem dado) ficam vazios.
"""
import datetime
import html
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(AQUI, "alimentos", "alimentos.json")
FONTE_TACO = "TACO 4ª ed. rev. e ampl. (NEPA/UNICAMP, 2011)"
NUTRIENTES = ["kcal", "proteina_g", "carboidrato_g", "gordura_g", "fibra_g", "saturada_g", "mono_g", "poli_g",
              "colesterol_mg", "sodio_mg"]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn")


def carregar():
    if not os.path.exists(BANCO):
        sys.exit("Banco vazio: rode  python alimentos.py importar-taco alimentos/taco_4ed.xlsx")
    return json.load(open(BANCO, encoding="utf-8"))


def gravar(itens):
    itens.sort(key=lambda x: (x["id"].split(":")[0] != "taco", x["id"].split(":")[0],
                              int(x["id"].split(":")[1]) if x["id"].startswith("taco:") else 0, x["nome"]))
    with open(BANCO, "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(i, ensure_ascii=False) for i in itens) + "\n]\n")


def por_id():
    return {i["id"]: i for i in carregar()}


# ---------------- TACO (xlsx lido só com a biblioteca padrão) ----------------
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def ler_xlsx(caminho):
    z = zipfile.ZipFile(caminho)
    ss = [("".join(t.text or "" for t in si.iter(NS + "t")))
          for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")]
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    folhas = {}
    for s in ET.fromstring(z.read("xl/workbook.xml")).find(NS + "sheets"):
        alvo = rels[s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")].lstrip("/")
        alvo = alvo if alvo.startswith("xl/") else "xl/" + alvo
        linhas = []
        for row in ET.fromstring(z.read(alvo)).iter(NS + "row"):
            lin = {}
            for c in row.findall(NS + "c"):
                v = c.find(NS + "v")
                if v is None:
                    continue
                lin[re.match(r"[A-Z]+", c.get("r")).group(0)] = ss[int(v.text)] if c.get("t") == "s" else v.text
            linhas.append(lin)
        folhas[s.get("name")] = linhas
    return folhas


def valor(v):
    v = (v or "").strip()
    if v in ("Tr", "NA", "tr"):
        return 0.0
    try:
        return round(float(v), 3)
    except ValueError:
        return None  # "*" = não analisado, ou vazio


def importar_taco(caminho):
    folhas = ler_xlsx(caminho)
    cmv = next(v for k, v in folhas.items() if k.lower().startswith("cmv"))
    ag = next(v for k, v in folhas.items() if k.lower().startswith("ag"))
    graxos = {l["A"]: l for l in ag if l.get("A", "").isdigit()}
    novos, grupo = [], ""
    for l in cmv:
        a = l.get("A", "").strip()
        if a and not a.isdigit() and len(l) == 1:
            grupo = a
            continue
        if not a.isdigit() or not l.get("B"):
            continue
        g = graxos.get(a, {})
        novos.append({"id": f"taco:{a}", "nome": l["B"].strip(), "grupo": grupo, "fonte": FONTE_TACO, "por_100g": {
            "kcal": valor(l.get("D")), "proteina_g": valor(l.get("F")), "carboidrato_g": valor(l.get("I")),
            "gordura_g": valor(l.get("G")), "fibra_g": valor(l.get("J")), "saturada_g": valor(g.get("C")),
            "mono_g": valor(g.get("D")), "poli_g": valor(g.get("E")), "colesterol_mg": valor(l.get("H")),
            "sodio_mg": valor(l.get("R"))}})
    outros = [i for i in carregar() if not i["id"].startswith("taco:")] if os.path.exists(BANCO) else []
    gravar(novos + outros)
    print(f"TACO: {len(novos)} alimentos gravados em {os.path.relpath(BANCO, AQUI)} (+ {len(outros)} de outras fontes)")


# ---------------- consulta ----------------
def linha(i):
    p = i["por_100g"]
    f = lambda k: "—" if p.get(k) is None else f"{p[k]:.1f}".replace(".", ",")
    return f"{i['id']:<24} {i['nome'][:58]:<58} {f('kcal'):>6} kcal · P {f('proteina_g'):>5} · C {f('carboidrato_g'):>5} · G {f('gordura_g'):>5} · fibra {f('fibra_g'):>4} · sat {f('saturada_g'):>4}"


def buscar(termos):
    chaves = [sem_acento(t) for t in termos]
    achados = [i for i in carregar() if all(c in sem_acento(i["nome"] + " " + i.get("grupo", "")) for c in chaves)]
    print(f"{len(achados)} achado(s), valores por 100 g:")
    for i in achados[:40]:
        print(" ", linha(i))
    if len(achados) > 40:
        print("  ... (refine a busca)")


def ver(ids):
    banco = por_id()
    for x in ids:
        print(json.dumps(banco.get(x, {"id": x, "erro": "não existe no banco"}), ensure_ascii=False, indent=1))


def adicionar(caminho, salvar=True):
    incluir(json.load(open(caminho, encoding="utf-8")), salvar)


def incluir(novos, salvar=True):
    banco, ids = por_id(), set()
    for n in novos:
        if not re.match(r"^(tbca|marca|receita|rt):[\w.-]+$", n.get("id", "")):
            sys.exit(f"id inválido: {n.get('id')} (use tbca:, marca:, receita: ou rt:)")
        if n["id"] in ids:
            sys.exit(f"{n['id']}: id repetido na lista")
        ids.add(n["id"])
        if not n.get("fonte") or not n.get("nome") or "por_100g" not in n:
            sys.exit(f"{n['id']}: faltam nome, fonte ou por_100g")
        p = n["por_100g"]
        if any(v is not None and not isinstance(v, (int, float)) for v in p.values()):
            sys.exit(f"{n['id']}: por_100g só aceita número ou null")
        if n["id"].startswith("marca:") and not (n.get("porcao") or {}).get("gramas"):
            print(f"  aviso: {n['id']} sem a porção do rótulo (porcao.gramas)")
        if (p.get("carboidrato_disponivel_g") or 0) > (p.get("carboidrato_g") or 0) + 0.05:
            print(f"  aviso: {n['id']} tem carboidrato disponível maior que o total (o total leva a fibra)")
        # o rótulo e a TBCA dão à fibra de 0 a 4 kcal/g: vale qualquer conta entre as duas pontas
        fibra = p.get("fibra_g") or 0
        disp = p.get("carboidrato_disponivel_g")
        disp = max((p.get("carboidrato_g") or 0) - fibra, 0) if disp is None else disp
        sem_fibra = 4 * (p.get("proteina_g") or 0) + 4 * disp + 9 * (p.get("gordura_g") or 0)
        folga = 0.15 * (p.get("kcal") or 0) + 5
        if p.get("kcal") and not sem_fibra - folga <= p["kcal"] <= sem_fibra + 4 * fibra + folga:
            print(f"  aviso: {n['id']} diz {p['kcal']} kcal e os macros somam {sem_fibra:.0f} a {sem_fibra + 4 * fibra:.0f}"
                  " (confira na fonte)")
        print(("atualizado " if n["id"] in banco else "novo ") + linha(n))
        banco[n["id"]] = n
    if salvar:
        gravar(list(banco.values()))
    else:
        print(f"{len(novos)} item(ns) conferido(s); nada gravado")


# ---------------- TBCA (site tbca.net.br, lido só com a biblioteca padrão) ----------------
TBCA = "https://www.tbca.net.br/base-dados/"
FONTE_TBCA = "TBCA 7.3 (USP/FoRC)"
TAGS_TBCA = {"PROCNT": "proteina_g", "CHOCDF": "carboidrato_g", "CHOAVLDF": "carboidrato_disponivel_g",
             "FAT": "gordura_g", "FIBTG": "fibra_g", "FASAT": "saturada_g", "FAMS": "mono_g", "FAPU": "poli_g",
             "CHOLE": "colesterol_mg", "NA": "sodio_mg"}
ORDEM_TBCA = ["kcal", "proteina_g", "carboidrato_g", "carboidrato_disponivel_g", "gordura_g", "fibra_g", "saturada_g",
              "mono_g", "poli_g", "colesterol_mg", "sodio_mg"]


def tbca_pagina(caminho, dados=None):
    req = urllib.request.Request(TBCA + caminho, headers={"User-Agent": "Mozilla/5.0"},
                                 data=urllib.parse.urlencode(dados).encode() if dados else None)
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def sem_tags(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def tbca_linhas(h):
    achados = []
    for link, cod, resto in re.findall(r"<tr><td><a href='(int_composicao_estatistica\.php\?[^']+)'>(\w+)</a></td>(.*?)</tr>",
                                       h, re.S):
        cel = [sem_tags(c) for c in re.findall(r"<td>(.*?)</td>", resto, re.S)] + [""] * 4
        achados.append({"codigo": cod, "nome": cel[0], "grupo": cel[2], "marca": cel[3], "link": html.unescape(link)})
    return achados


def tbca_buscar(termos):
    """O site busca um termo por vez (parte do nome ou do código, sem ligar para acento) e pagina de 100 em 100:
    busca pelo termo com menos páginas e filtra aqui pelos outros."""
    primeiras = {}
    for t in termos:
        h = tbca_pagina("composicao_estatistica.php", {"guarda": "tomo1", "produto": t, "cmb_grupo": "", "cmb_tipo_alimento": ""})
        m = re.search(r"gina 1 de (\d+)", h)
        primeiras[t] = (int(m.group(1)) if m else 1, h)
    termo = min(termos, key=lambda t: primeiras[t][0])
    paginas, h = primeiras[termo]
    achados = tbca_linhas(h)
    for pag in range(2, min(paginas, 30) + 1):
        achados += tbca_linhas(tbca_pagina(f"composicao_estatistica.php?pagina={pag}&atuald={(pag - 1) // 10 + 1}"
                                           f"&produto={urllib.parse.quote(termo)}"))
    return [a for a in achados if all(sem_acento(t) in sem_acento(a["codigo"] + " " + a["nome"] + " " + a["marca"])
                                      for t in termos)]


def tbca_valor(v):
    v = v.strip().lower()
    if v == "tr":
        return 0.0
    try:
        return round(float(v.replace(",", ".")), 3)
    except ValueError:
        return None  # "NA" ou "-" = sem dado


def tbca_item(a):
    h = tbca_pagina(a["link"])
    p = dict.fromkeys(ORDEM_TBCA)
    for lin in re.findall(r"<tr>(.*?)</tr>", h, re.S):
        cel = [sem_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", lin, re.S)]
        if len(cel) < 4:
            continue
        if cel[1] == "ENERC" and cel[2] == "kcal":
            p["kcal"] = tbca_valor(cel[3])
        elif cel[1] in TAGS_TBCA:
            p[TAGS_TBCA[cel[1]]] = tbca_valor(cel[3])
    if p["kcal"] is None:
        sys.exit(f"{a['codigo']}: a página da TBCA veio sem a tabela de composição")
    tipo = re.search(r"Tipo de Alimento:\s*(?:\w+ - )?(.*?)\s*(?:Nome Cient|Descri)", sem_tags(h))
    return {"id": "tbca:" + a["codigo"], "nome": a["nome"] + (f" ({a['marca']})" if a["marca"] else ""),
            "grupo": a["grupo"], "fonte": FONTE_TBCA, "por_100g": p,
            "obs": (tipo.group(1) + "; " if tipo else "") + f"consultada em {datetime.date.today()}"}


def tbca(args):
    termos, escolha = (args[:args.index("--gravar")], args[args.index("--gravar") + 1:]) if "--gravar" in args else (args, None)
    if not termos:
        sys.exit("diga o que buscar:  python alimentos.py tbca peixe assado")
    try:
        codigos = [t.upper() for t in termos if re.match(r"^BRC\w+$", t, re.I)]
        if codigos:  # códigos valem cada um por si
            achados = [a for c in codigos for a in tbca_buscar([c]) if a["codigo"] == c]
        else:
            achados = tbca_buscar(termos)
        banco = por_id()
        print(f"{len(achados)} achado(s) na TBCA:")
        for n, a in enumerate(achados, 1):
            print(f"  {n:>3}. {a['codigo']}  {a['nome'][:90]}" + (f" ({a['marca']})" if a["marca"] else "")
                  + f" · {a['grupo']}" + (" · já no banco" if "tbca:" + a["codigo"] in banco else ""))
        if escolha is None and achados and sys.stdin and sys.stdin.isatty():
            try:
                escolha = input("Quais gravar? Números ou códigos (Enter = nenhum, 'todos' = todos): ").split()
            except EOFError:
                escolha = []
        escolha = " ".join(escolha or []).replace(",", " ").split()
        if not escolha:
            if achados:
                print("Nada gravado. Para gravar:  python alimentos.py tbca " + " ".join(termos) + " --gravar 1 2 (ou todos)")
            return
        if [e.lower() for e in escolha] == ["todos"]:
            sel = achados
        else:
            sel = []
            for e in escolha:
                if e.isdigit() and 1 <= int(e) <= len(achados):
                    sel.append(achados[int(e) - 1])
                    continue
                a = (next((a for a in achados if a["codigo"] == e.upper()), None)
                     or next((a for a in tbca_buscar([e]) if a["codigo"] == e.upper()), None))
                if not a:
                    sys.exit(f"não achei {e} nos achados nem na TBCA")
                sel.append(a)
        incluir([tbca_item(a) for a in sel])
    except urllib.error.URLError as erro:
        sys.exit(f"Não consegui falar com o site da TBCA ({erro}). Confira a internet e tente de novo.")


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "importar-taco" and args:
        importar_taco(args[0])
    elif cmd == "buscar" and args:
        buscar(args)
    elif cmd == "ver" and args:
        ver(args)
    elif cmd == "adicionar" and args:
        adicionar(args[0])
    elif cmd == "conferir" and args:
        adicionar(args[0], salvar=False)
    elif cmd == "tbca" and args:
        tbca(args)
    else:
        print(__doc__)
