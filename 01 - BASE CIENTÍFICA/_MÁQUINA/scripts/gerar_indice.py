"""Gera "01 - BASE CIENTÍFICA/00 - ÍNDICE.md": o mapa da base por área (Condição | Protocolo | Ficha | Fontes) e o resumo
do catálogo de artigos e da fila. Só biblioteca padrão. Não edite o índice à mão: este script o refaz.

Uso (de qualquer pasta):  python gerar_indice.py
Também é chamado no fim de `biblioteca.py catalogar`.
"""
import collections
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MAQ = AQUI.parent
BASE = MAQ.parent
SAIDA = BASE / "00 - ÍNDICE.md"
AREAS = ["Treino de força", "Composição corporal e emagrecimento", "Nutrição esportiva", "Populações especiais", "Transversais"]
PROCESSADAS = MAQ / "fontes-processadas"


def nfc(t):
    return unicodedata.normalize("NFC", t or "")


def sa(t):
    return "".join(c for c in unicodedata.normalize("NFD", (t or "").lower()) if unicodedata.category(c) != "Mn")


def frontmatter(texto):
    texto = texto.replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n?", texto, re.S)
    fm = {}
    for l in (m.group(1).splitlines() if m else []):
        k, sep, v = l.partition(":")
        if sep and re.fullmatch(r"[\w-]+", k.strip()):
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, texto[m.end():] if m else texto


def n_afirmacoes(corpo):
    """(n, rótulo): linhas numeradas de '## Afirmações prontas'; Ficha conceitual (sem essa seção): itens da 1ª tabela numerada."""
    m = re.search(r"(?ms)^##\s+Afirma[çc][õo]es prontas[^\n]*\n(.*?)(?=^##\s|\Z)", corpo)
    if m:
        return sum(1 for l in m.group(1).splitlines() if re.match(r"^\s*\|\s*\d+\s*\|", l)), "afirmações"
    for sec in re.split(r"(?m)^##\s", corpo)[1:]:
        n = sum(1 for l in sec.splitlines() if re.match(r"^\s*\|\s*\d+\s*\|", l))
        if n:
            return n, "itens"
    return 0, "afirmações"


def ler_jsonl(p):
    if not p.exists():
        return None
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def linhas_da_area(pasta):
    """{condição: {'protocolo': (stem, fm), 'ficha': (stem, fm, n, fontes, quebradas)}} das notas '<Condição> - Protocolo/Ficha.md'."""
    out = {}
    if not pasta.exists():
        return out
    existentes = {sa(nfc(p.stem)) for p in PROCESSADAS.glob("*.md")}
    for p in sorted(pasta.glob("*.md")):
        stem = nfc(p.stem)
        for sufixo, chave in ((" - Protocolo", "protocolo"), (" - Ficha", "ficha")):
            if stem.endswith(sufixo):
                cond = stem[:-len(sufixo)]
                fm, corpo = frontmatter(p.read_text(encoding="utf-8-sig", errors="replace"))
                item = {"stem": stem, "fm": fm}
                if chave == "ficha":
                    item["n"], item["rotulo"] = n_afirmacoes(corpo)
                    notas = [nfc(x).split("#")[0].strip() for x in re.findall(r"\[\[([^\]|]+)", fm.get("notas_base", ""))]
                    item["fontes"] = sum(1 for n in notas if sa(n) in existentes)
                    item["quebradas"] = [n for n in notas if sa(n) not in existentes and not n.endswith(" - Protocolo")]
                out.setdefault(cond, {})[chave] = item
    return out


def celula_protocolo(it):
    if not it:
        return "—"
    fm = it["fm"]
    status = fm.get("status_protocolo") or fm.get("status") or "sem status"
    data = fm.get("atualizado_em") or fm.get("atualizada") or "sem data"
    return f"[[{it['stem']}]] ({status}, {data})"


def celula_ficha(it):
    if not it:
        return "—"
    fm = it["fm"]
    return f"[[{it['stem']}]] ({fm.get('status') or 'sem status'}, {fm.get('atualizada') or 'sem data'}, {it['n']} {it['rotulo']})"


def celula_fontes(it):
    if not it:
        return "—"
    txt = f"{it['fontes']} em fontes-processadas"
    if it["quebradas"]:
        txt += f" · {len(it['quebradas'])} sem nota"
    return txt


def gerar():
    hoje = time.strftime("%Y-%m-%d")
    out = ["---", "tipo: indice", f"atualizada: {hoje}", "---", "# Base científica: índice", "",
           "> Gerado por `_MÁQUINA/scripts/gerar_indice.py` (roda no fim do `biblioteca.py catalogar`). Não edite à mão.", "",
           "## Como usar",
           "1. Solte os PDFs novos em `ENTRADA/` (qualquer nome); o `biblioteca.py catalogar` lê, cataloga e guarda em `_MÁQUINA/pdf`.",
           "2. `/montar-condicao <condição ou tema>` monta o Protocolo e a Ficha (o Jorge aprova de 3 a 10 fontes antes).",
           "3. `/roteiro` e `/carrossel` leem só a **Ficha**; o validador confere cada `[#n]` contra ela.",
           "4. Para evidência fora da Ficha: `biblioteca.py buscar \"tema\"`, depois `ver` e `trecho` (nunca abrir PDF inteiro).",
           "5. Este índice mostra o que já existe, por área, e o tamanho do catálogo e da fila.", ""]
    for area in AREAS:
        out += [f"## {area}", "", "| Condição | Protocolo (status, atualizada) | Ficha (status, atualizada, nº de afirmações) | Fontes |",
                "|---|---|---|---|"]
        linhas = linhas_da_area(BASE / area)
        if not linhas:
            out.append("| _(nenhuma ainda)_ | — | — | — |")
        for cond in sorted(linhas, key=sa):
            L = linhas[cond]
            out.append(f"| {cond} | {celula_protocolo(L.get('protocolo'))} | {celula_ficha(L.get('ficha'))} | {celula_fontes(L.get('ficha'))} |")
        out.append("")

    cat = ler_jsonl(MAQ / "catalogo.jsonl")
    out += ["## Catálogo de artigos", ""]
    if cat is None:
        out += ["_Catálogo ainda não existe: rode `biblioteca.py catalogar`._", ""]
    else:
        tipos = collections.Counter(c.get("tipo") or "?" for c in cat)
        out += [f"**{len(cat)} artigos** em `_MÁQUINA/artigos` (busca: `biblioteca.py buscar \"tema\"`).", "",
                "| Tipo de estudo | Artigos |", "|---|---|"]
        out += [f"| {t} | {n} |" for t, n in sorted(tipos.items(), key=lambda x: (-x[1], x[0]))]
        out.append("")
    fila = ler_jsonl(MAQ / "fila.jsonl")
    out += ["## Fila de fontes", ""]
    if fila is None:
        out += ["_Sem `fila.jsonl`._", ""]
    else:
        eixos = collections.Counter(f.get("eixo_principal") or "?" for f in fila)
        out += [f"**{len(fila)} fontes** na fila (`_MÁQUINA/fila.jsonl`): candidatas, **não são evidência** até serem processadas.", "",
                "| Eixo | Na fila |", "|---|---|"]
        out += [f"| {e} | {n} |" for e, n in sorted(eixos.items(), key=lambda x: (-x[1], x[0]))]
        out.append("")
    SAIDA.write_text("\n".join(out), encoding="utf-8", newline="\n")
    return SAIDA


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("Índice gerado:", gerar())
