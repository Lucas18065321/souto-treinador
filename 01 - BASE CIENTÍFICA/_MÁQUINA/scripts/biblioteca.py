"""Biblioteca de artigos da base científica (motor JSON): transforma os PDFs de artigos e diretrizes em JSON leve
para Fichas, roteiro e carrossel. Zero token: só biblioteca padrão do Python + pdftotext (vem com o Git) +
Europe PMC/Crossref (metadados públicos, sem chave, com cache).

Tudo da máquina mora em "01 - BASE CIENTÍFICA/_MÁQUINA/" (o Jorge não precisa abrir):
  pdf/                    todos os PDFs catalogados (sem duplicata exata)
  artigos/<id>.json       ficha automática: referência Vancouver, resumo, conclusão, achados com número e
                          página, limitações, financiamento, teto de certeza pelo desenho do estudo
  texto/<id>.txt          texto completo limpo com [p. N] (só para 'trecho'; nunca ler inteiro)
  texto-fontes/           texto limpo (.txt) de fontes já processadas (localizador "seç.")
  fontes_fila/            texto de acesso aberto baixado pelo importar-fila
  fontes-processadas/     notas de fonte já processadas que as Fichas citam
  catalogo.jsonl  fora_do_catalogo.json  fila.jsonl  para-baixar.md  cache/
O Jorge solta PDFs novos em "01 - BASE CIENTÍFICA/ENTRADA/": o catalogar cataloga e move para _MÁQUINA/pdf
(duplicata exata: só remove a cópia da ENTRADA). As pastas lidas estão em biblioteca_fontes.json; as palavras
dos eixos, em biblioteca_eixos.json. O índice "01 - BASE CIENTÍFICA/00 - ÍNDICE.md" é gerado por gerar_indice.py
(chamado no fim do catalogar).

Fontes do catálogo: os PDFs de ENTRADA e de _MÁQUINA/pdf + da fila (fila.jsonl) só o de maior grau (diretriz,
consenso, posicionamento) e o que veio das Reviews do Igor Eckert + as notas já processadas (fontes-processadas).

Uso (de qualquer pasta; S = "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/biblioteca.py"):
  python S importar-fila [--baixar] [--sem-rede]   plano (e download do acesso aberto) das diretrizes/Reviews da fila
  python S catalogar [--forcar] [--limite N] [--sem-rede]
  python S buscar "creatina cognição" [--eixo X] [--tipo meta-analise] [--desde 2018] [--n 12]
  python S ver "<id ou parte do id>" [--completo]
  python S trecho "<id>" "termo" [--n 5]
  python S conferir-ficha "<Tema> - Ficha"         (ou o caminho da Ficha .md)
  python S panorama
"""
import argparse
import collections
import concurrent.futures as cf
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = Path(__file__).resolve().parent      # .../_MÁQUINA/scripts
MAQ = AQUI.parent                           # .../01 - BASE CIENTÍFICA/_MÁQUINA
BASE = MAQ.parent                           # .../01 - BASE CIENTÍFICA
RAIZ = BASE.parent
PDFS = MAQ / "pdf"
DUPLICATAS = PDFS / "_duplicatas"           # ENTRADA com o mesmo artigo mas arquivo diferente (nunca apagado)
ENTRADA = BASE / "ENTRADA"                  # o Jorge solta PDFs aqui
ARTS = MAQ / "artigos"
TXT = MAQ / "texto"
CATALOGO = MAQ / "catalogo.jsonl"
FORA = MAQ / "fora_do_catalogo.json"
FILA_JSONL = MAQ / "fila.jsonl"
CACHE = MAQ / "cache"
ESTADO = CACHE / "_estado.json"
BUSCA = CACHE / "_indice_busca.json"
CONF = AQUI / "biblioteca_fontes.json"
EIXOS = AQUI / "biblioteca_eixos.json"
PROCESSADAS = MAQ / "fontes-processadas"    # notas de fonte já processadas (as Fichas citam)
TEXTO_FONTES = MAQ / "texto-fontes"         # .txt de fontes processadas (localizador "seç.")
FONTES_FILA = MAQ / "fontes_fila"           # texto completo (acesso aberto) das diretrizes da fila, baixado por 'importar-fila'
PARA_BAIXAR = MAQ / "para-baixar.md"
# Da fila entram só as fontes de maior grau (diretriz, consenso, posicionamento) e as que vieram das Reviews (Igor Eckert)
SUBTIPOS_ALTOS = ("diretriz", "consenso", "posicionamento")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SoutoTreinador-biblioteca/1.0"
VERSAO = 2
SEM_REDE = False
NUVEM = "só na nuvem (OneDrive): clique com o botão direito na pasta > 'Sempre manter neste dispositivo' e rode catalogar de novo"
# motivos que não ficam em cache: o arquivo pode mudar de estado sem mudar tamanho/data
REPETIR = ("só na nuvem", "sem texto", "erro")


# ---------------------------------------------------------------- utilidades
def sa(t):
    """sem acento, minúsculo"""
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def nfc(t):
    return unicodedata.normalize("NFC", t or "")


TAG = re.compile(r"</?[a-zA-Z][\w-]*(\s[^<>]{0,200})?/?>")  # só tag de verdade: "P < 0·001" fica


def limpa_html(t):
    t = t or ""
    for _ in range(2):  # a Europe PMC às vezes manda as tags escapadas (&lt;i&gt;)
        t = re.sub(r"<h\d[^>]*>\s*(.*?)\s*:?\s*</h\d>", r"\n\1: ", t, flags=re.S | re.I)
        t = re.sub(r"<b>\s*([A-Z][^<]{2,40}?)\s*:?\s*</b>\s*:?", r"\n\1: ", t)
        t = TAG.sub("", t)
        t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*", "\n", t).strip()


def pdftotext_bin():
    for c in (shutil.which("pdftotext"), r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"):
        if c and os.path.exists(c):
            return c
    sys.exit("pdftotext não encontrado (vem com o Git for Windows).")


def http_json(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / (hashlib.sha1(url.encode()).hexdigest()[:20] + ".json")
    if c.exists():
        return json.loads(c.read_text(encoding="utf-8"))
    if SEM_REDE:
        return None
    for tent in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode("utf-8"))
            c.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.15)
            return d
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                c.write_text("null", encoding="utf-8")
                return None
            time.sleep(1.5 * (tent + 1))
        except Exception:
            time.sleep(1.5 * (tent + 1))
    return None


# ---------------------------------------------------------------- texto do PDF
def extrair_paginas(pdf):
    exe = pdftotext_bin()

    def roda(caminho):
        r = subprocess.run([exe, "-enc", "UTF-8", str(caminho), "-"], capture_output=True, timeout=240)
        return r.stdout.decode("utf-8", "replace")

    try:
        t = roda(pdf)
    except subprocess.TimeoutExpired:
        t = ""
    if len(t.strip()) < 200:  # caminho com acento às vezes falha no pdftotext do Git: tenta cópia temporária
        tmp = Path(tempfile.gettempdir()) / f"bib_{hashlib.sha1(str(pdf).encode()).hexdigest()[:12]}.pdf"
        try:
            shutil.copyfile(pdf, tmp)
            t = roda(tmp)
        except Exception:
            pass
        finally:
            try:
                tmp.unlink()
            except OSError:
                pass
    paginas = t.split("\f")
    if paginas and not paginas[-1].strip():
        paginas = paginas[:-1]
    return paginas


def paragrafos(pagina):
    t = unicodedata.normalize("NFKC", pagina).replace("\u00ad", "")
    t = re.sub(r"(?<=[a-z])-\n(?=[a-z])", "", t)
    paras, atual = [], []
    for l in t.splitlines():
        l = l.strip()
        if not l:
            if atual:
                paras.append(" ".join(atual))
                atual = []
        else:
            atual.append(l)
    if atual:
        paras.append(" ".join(atual))
    return [re.sub(r"\s+", " ", p) for p in paras]


def tirar_repetidos(pags):
    cont = collections.Counter()
    for paras in pags:
        for p in set(paras):
            if len(p) < 140:
                cont[re.sub(r"\d+", "#", p)] += 1
    lim = max(3, int(len(pags) * 0.3))
    rep = {k for k, v in cont.items() if v >= lim}
    return [[p for p in paras if re.sub(r"\d+", "#", p) not in rep and not re.fullmatch(r"[\d\s\-–/|.]+", p)]
            for paras in pags]


RE_REFS = re.compile(r"^(\d+\.?\s*)?(references?( and notes)?|bibliography|refer[eê]ncias( bibliogr[aá]ficas)?|literature cited|works cited)\s*:?$", re.I)


def cortar_referencias(pags):
    n = len(pags)
    for i in range(int(n * 0.4), n):
        for k, p in enumerate(pags[i]):
            if RE_REFS.match(p.strip()):
                return pags[:i] + [pags[i][:k]]
    return pags


RE_ABREV = re.compile(r"\b(et al|vs|v|Fig|Figs|e\.g|i\.e|approx|No|Ref|Eq|Suppl|Tab|cf|ca|Dr|ref|sd|SD)\.")


def frases(p):
    p = RE_ABREV.sub(lambda m: m.group(0).replace(".", "§"), p)
    partes = re.split(r"(?<=[.!?])\s+(?=[A-Z\[(“\"])", p)
    return [x.replace("§", ".").strip() for x in partes if x.strip()]


# ---------------------------------------------------------------- metadados
RE_DOI = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>,;]+)", re.I)


def dois_candidatos(pags_brutas, stem=""):
    vistos = []

    def poe(d):
        d = re.sub(r"(?i)(\.pdf|/abstract|/full|/epdf|\.)$", "", d.rstrip(".)]}"))
        m = re.search(r"(annurev-[a-z]+-)(\d{6})(\d{6})$", d)  # Annual Reviews: o PDF às vezes perde o hífen
        if m:
            d = d[:m.start()] + m.group(1) + m.group(2) + "-" + m.group(3)
        if d.lower() not in [v.lower() for v in vistos]:
            vistos.append(d)

    # DOI pelo nome do arquivo (Annual Reviews, Springer/BMC)
    if re.fullmatch(r"annurev-[a-z]+-\d{6}-\d{6}", stem):
        poe("10.1146/" + stem)
    if re.fullmatch(r"s\d{5}-\d{3}-\d{5}-[0-9a-z]", stem):
        poe("10.1007/" + stem)
        poe("10.1186/" + stem)
    for p in pags_brutas[:2]:
        # hífen de quebra de linha e hífen invisível (soft hyphen) partem o DOI
        for variante in (re.sub(r"\u00ad\s*", "-", re.sub(r"-\s*\n\s*", "-", p)), p.replace("\u00ad", "")):
            for m in RE_DOI.finditer(variante):
                poe(m.group(1))
    return vistos[:6]


def palavras_titulo(t):
    return [w for w in re.findall(r"[a-z0-9]+", sa(t)) if len(w) > 3]


def confere_titulo(titulo, texto_inicio):
    ws = palavras_titulo(titulo)
    if not ws:
        return False
    alvo = " ".join(re.findall(r"[a-z0-9]+", sa(texto_inicio)))
    return sum(1 for w in ws if w in alvo) / len(ws) >= 0.6


def epmc(query, n=1):
    q = urllib.parse.quote(query)
    d = http_json(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&resultType=core&format=json&pageSize={n}")
    return (d or {}).get("resultList", {}).get("result", []) or []


def lista(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def meta_epmc(r):
    autores = lista((r.get("authorList") or {}).get("author"))
    ji = r.get("journalInfo") or {}
    j = ji.get("journal") or {}
    ano = r.get("pubYear") or ji.get("yearOfPublication")
    return {
        "titulo": limpa_html(r.get("title", "")).rstrip("."),
        "autores": (r.get("authorString") or "").rstrip("."),
        "primeiro_autor": (autores[0].get("lastName") or autores[0].get("collectiveName") or "") if autores else "",
        "revista": j.get("isoabbreviation") or j.get("medlineAbbreviation") or j.get("title") or "",
        "ano": int(ano) if str(ano or "").isdigit() else None,
        "volume": ji.get("volume") or "", "numero": ji.get("issue") or "", "paginas": r.get("pageInfo") or "",
        "doi": r.get("doi") or "", "pmid": r.get("pmid") or "", "pmcid": r.get("pmcid") or "",
        "resumo": limpa_html(r.get("abstractText", "")),
        "tipos_pub": lista((r.get("pubTypeList") or {}).get("pubType")),
        "palavras_chave": lista((r.get("keywordList") or {}).get("keyword"))[:12],
        "mesh": [m.get("descriptorName") for m in lista((r.get("meshHeadingList") or {}).get("meshHeading"))][:15],
        "fonte_metadados": "europepmc",
    }


def meta_crossref(m):
    aut = m.get("author") or []
    nomes = []
    for a in aut:
        fam = a.get("family") or a.get("name") or ""
        ini = "".join(p[0] for p in re.split(r"[\s\-.]+", a.get("given", "")) if p)
        nomes.append(f"{fam} {ini}".strip())
    ano = None
    for k in ("published-print", "published-online", "issued", "created"):
        dp = (m.get(k) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            ano = dp[0][0]
            break
    return {
        "titulo": limpa_html(" ".join(m.get("title") or [""])).rstrip("."),
        "autores": ", ".join(nomes), "primeiro_autor": (aut[0].get("family") or aut[0].get("name") or "") if aut else "",
        "revista": (m.get("short-container-title") or m.get("container-title") or [""])[0],
        "ano": ano, "volume": m.get("volume", ""), "numero": m.get("issue", ""), "paginas": m.get("page", ""),
        "doi": m.get("DOI", ""), "pmid": "", "pmcid": "", "resumo": limpa_html(m.get("abstract", "")),
        "tipos_pub": [m.get("type", "")], "palavras_chave": (m.get("subject") or [])[:12], "mesh": [],
        "fonte_metadados": "crossref",
    }


def titulo_do_arquivo(stem):
    """Nome de arquivo descritivo (ex.: NOETIKON) vira título; códigos (s00394-024-…) não."""
    s = re.sub(r"[_+]+", " ", stem)
    s = re.sub(r"\s*\(\d+\)$", "", s).strip()
    s = re.sub(r"^[A-ZÀ-Ý][\wÀ-ÿ' -]+ \d{4} - ", "", s)  # "Sobrenome 2025 - Título" da base
    palavras = re.findall(r"[A-Za-zÀ-ÿ]{3,}", s)
    if len(palavras) < 4:
        return ""
    if "-" in s and " " not in s:
        s = s.replace("-", " ")
    return s


def titulo_da_pagina(paras):
    for p in paras[:25]:
        w = p.split()
        if 5 <= len(w) <= 30 and not re.search(r"(?i)(journal|doi|http|©|copyright|received|accepted|vol\.|issn|open access|licen[cs]e|university|department|correspond)", p) \
                and sum(c.isalpha() for c in p) > 0.75 * len(p.replace(" ", "")):
            return p.rstrip(".")
    return ""


def ano_do_texto(texto, stem):
    for pad in (r"©\s*(?:\w+\s+)?((?:19|20)\d\d)", r"(?i)published(?: online)?[^.\n]{0,40}?((?:19|20)\d\d)",
                r"(?i)accepted[^.\n]{0,40}?((?:19|20)\d\d)", r"(?i)received[^.\n]{0,40}?((?:19|20)\d\d)"):
        m = re.search(pad, texto)
        if m and 1980 <= int(m.group(1)) <= 2027:
            return int(m.group(1))
    m = re.search(r"\b((?:19[89]|20[0-2])\d)\b", stem)
    return int(m.group(1)) if m else None


def obter_metadados(pags_brutas, paras1, stem):
    inicio = " ".join(pags_brutas[:2])
    for doi in dois_candidatos(pags_brutas, stem):
        r = epmc(f'DOI:"{doi}"')
        if r:
            m = meta_epmc(r[0])
            if confere_titulo(m["titulo"], inicio):
                return m, "doi"
        c = (http_json("https://api.crossref.org/works/" + urllib.parse.quote(doi)) or {}).get("message")
        if c:
            m = meta_crossref(c)
            if m["titulo"] and confere_titulo(m["titulo"], inicio):
                # a Europe PMC às vezes indexa com o DOI em maiúsculas/diferente: tenta pelo título para pegar resumo
                if not m["resumo"]:
                    r2 = epmc(f'TITLE:"{m["titulo"][:180]}"', 3)
                    for x in r2:
                        if sa(x.get("title", ""))[:60] == sa(m["titulo"])[:60]:
                            m2 = meta_epmc(x)
                            m2["doi"] = m2["doi"] or m["doi"]
                            return m2, "doi+titulo"
                return m, "doi"
    titulo = titulo_do_arquivo(stem) or titulo_da_pagina(paras1)
    if titulo and len(titulo) >= 25:
        for x in epmc(f'TITLE:"{titulo[:160]}"', 3):
            t = sa(x.get("title", ""))
            if t.startswith(sa(titulo)[:50]) and confere_titulo(x.get("title", ""), inicio):
                return meta_epmc(x), "titulo"
    return {"titulo": titulo or stem, "autores": "", "primeiro_autor": "", "revista": "", "ano": ano_do_texto(inicio, stem),
            "volume": "", "numero": "", "paginas": "", "doi": "",  # DOI não confirmado pelo título pode ser de uma referência
            "pmid": "", "pmcid": "", "resumo": "", "tipos_pub": [], "palavras_chave": [], "mesh": [],
            "fonte_metadados": "pdf"}, "pdf"


def vancouver(m):
    aut = [a.strip() for a in (m.get("autores") or "").split(",") if a.strip()]
    partes = []
    if aut:
        partes.append(", ".join(aut[:6]) + (", et al." if len(aut) > 6 else "."))
    partes.append((m.get("titulo") or "").rstrip(".") + ".")
    if m.get("revista"):
        s = m["revista"].rstrip(".") + ". " + str(m.get("ano") or "")
        if m.get("volume"):
            s += f";{m['volume']}" + (f"({m['numero']})" if m.get("numero") else "")
        if m.get("paginas"):
            s += f":{m['paginas']}"
        partes.append(s + ".")
    elif m.get("ano"):
        partes.append(f"{m['ano']}.")
    if m.get("doi"):
        partes.append(f"doi:{m['doi']}")
    return " ".join(partes)


# ---------------------------------------------------------------- classificação e extração
TIPOS = [
    ("errata", r"^(correction|erratum|corrigendum|retraction|retracted|expression of concern)\b"),
    ("diretriz", r"\bguidelines?\b|\bdiretriz|clinical practice recommendations|\bguidance\b"),
    ("consenso", r"\bconsensus|position (stand|statement|paper)|scientific statement|presidential advisory|expert (panel|opinion)|\bposicionamento"),
    ("umbrella", r"umbrella review|overview of (systematic )?reviews|review of (systematic )?reviews|review of meta-analyses"),
    ("meta-analise", r"meta-?analys[ie]s|metan[aá]lise|meta-regression|pooled analysis"),
    ("revisao-sistematica", r"systematic (literature )?review|revis[aã]o sistem[aá]tica|scoping review"),
    ("mendeliana", r"mendelian randomi[sz]ation"),
    ("ensaio-clinico", r"randomi[sz]ed|controlled trial|cross-?over (trial|study|design)|placebo-controlled|\brct\b|clinical trial|feeding study|pilot trial|ensaio cl[ií]nico"),
    ("pre-clinico", r"\b(mice|mouse|murine|rats?|rodents?|in vitro|cell lines?|zebrafish|animal models?|drosophila)\b"),
    ("coorte", r"\bcohort|prospective (study|analysis)|longitudinal|follow-up study|coorte"),
    ("caso-controle", r"case-control"),
    ("transversal", r"cross-sectional|transversal|national survey|diagnostic accuracy|sensitivity and specificity|validation study"),
    ("revisao-narrativa", r"\breview\b|revis[aã]o|perspective|commentary|editorial|narrative|viewpoint|\bupdate\b|^introduction$"),
]
PUBTYPE = [("Retracted", "errata"), ("Erratum", "errata"), ("Published Erratum", "errata"), ("Practice Guideline", "diretriz"),
           ("Guideline", "diretriz"), ("Consensus", "consenso"), ("Meta-Analysis", "meta-analise"),
           ("Systematic Review", "revisao-sistematica"), ("Randomized Controlled Trial", "ensaio-clinico"),
           ("Clinical Trial", "ensaio-clinico"), ("Observational Study", "coorte")]
TETO = {
    "diretriz": ("conforme a diretriz", "use a força e a certeza que a própria diretriz declara em cada recomendação"),
    "consenso": ("baixa a moderada", "opinião organizada de especialistas: cite como posição, não como prova"),
    "umbrella": ("moderada", "depende da certeza (GRADE) das meta-análises incluídas"),
    "meta-analise": ("moderada", "teto alto só se a própria meta-análise declarar GRADE alta"),
    "revisao-sistematica": ("moderada", "sem meta-análise a conclusão é qualitativa"),
    "ensaio-clinico": ("baixa", "um ensaio isolado: 'pode'; amostra pequena, curta duração ou desfecho substituto rebaixam"),
    "mendeliana": ("baixa", "sugere causalidade genética, não testa intervenção"),
    "coorte": ("baixa", "associação, não causa: 'está associado a'"),
    "caso-controle": ("muito baixa", "associação retrospectiva, sujeita a viés de memória"),
    "transversal": ("muito baixa", "retrato de um momento: não mostra causa nem direção"),
    "pre-clinico": ("muito baixa", "animal ou célula: só mecanismo; nunca afirmar efeito em humanos"),
    "revisao-narrativa": ("muito baixa", "opinião dos autores: use para achar as fontes primárias"),
    "errata": ("—", "correção de outro artigo"),
    "outro": ("indefinida", "classifique lendo o resumo"),
    "posicionamento": ("baixa a moderada", "posição de sociedade: cite como posição; a certeza é a que o documento declara"),
    "revisao-cochrane": ("moderada", "use o GRADE da tabela 'Summary of findings'"),
    "documento-regulatorio": ("conforme o documento", "norma ou parecer: diz o que é permitido, não o que funciona"),
    "relatorio-epidemiologico": ("dado descritivo", "mostra frequência e tendência, não causa"),
}
PESO_TIPO = {"diretriz": 3, "consenso": 2, "posicionamento": 2, "revisao-cochrane": 3, "documento-regulatorio": 1,
             "relatorio-epidemiologico": 0.5, "umbrella": 3, "meta-analise": 3, "revisao-sistematica": 2, "ensaio-clinico": 1.5,
             "mendeliana": 1, "coorte": 1, "caso-controle": 0.5, "transversal": 0.3, "revisao-narrativa": 0.5,
             "pre-clinico": -1, "errata": -6, "outro": -0.5}


def classificar(titulo, tipos_pub, resumo):
    t = sa(titulo)
    for nome, pad in TIPOS:
        if re.search(pad, t, re.I):
            if nome == "revisao-narrativa" and re.search(TIPOS[5][1] + "|" + TIPOS[4][1], sa(resumo[:1500]), re.I):
                break  # "review" no título, mas o resumo diz que é sistemática/meta-análise
            return nome
    for pt, nome in PUBTYPE:
        if any(pt.lower() == (x or "").lower() for x in tipos_pub):
            return nome
    r = sa(resumo[:1500])
    if any((x or "").lower() in ("review", "review-article") for x in tipos_pub):
        for nome, pad in TIPOS[3:6]:
            if re.search(pad, r, re.I):
                return nome
        return "revisao-narrativa"
    for nome, pad in TIPOS[2:]:
        if nome == "pre-clinico" and not re.search(pad, r[:500], re.I):
            continue
        if re.search(pad, r, re.I):
            return nome
    if any((x or "").lower() == "review" for x in tipos_pub):
        return "revisao-narrativa"
    return "outro"


def teto_certeza(tipo, resumo):
    nivel, porque = TETO.get(tipo, TETO["outro"])
    r = sa(resumo)
    if tipo in ("meta-analise", "revisao-sistematica", "umbrella") and re.search(r"observational|cohort|prospective stud|case-control|cross-sectional", r) \
            and not re.search(r"randomi[sz]ed", r):
        nivel, porque = "baixa", "síntese de estudos observacionais: associação, não causa"
    grade = sorted(set(m.group(0) for m in re.finditer(r"\b(high|moderate|low|very low)[- ](certainty|quality)( of (the )?evidence)?", r)))
    return {"nivel": nivel, "porque": porque, "grade_declarado": grade}


RE_EST = re.compile(r"95\s*%\s*(CI|confidence intervals?|IC|CrI)\s*[:,=]?\s*[\[(]?\s*[-−–]?\d"
                    r"|[\[(]\s*[-−–]?\d+(?:[.,·]\d+)?\s*(?:to|–|-|,|;)\s*[-−–]?\d+[.,·]\d+\s*[\])]"
                    r"|[\[(]\s*[-−–]?\d+[.,·]\d+\s*(?:to|–|-|,|;)\s*[-−–]?\d+(?:[.,·]\d+)?\s*[\])]"
                    r"|\b(RR|HR|OR|SMD|WMD|MD|IRR|aOR|aHR|RD)\b\s*[=:,]?\s*[-−–]?\d"
                    r"|\b[pP]\s*[<=≤]\s*0?[.,·]\d|\d+[.,·]?\d*\s*%", re.I)
RE_METODO = re.compile(r"(presented as|expressed as|data are|values are|were calculated|was calculated|was used|were used|"
                       r"we (used|calculated|performed|assessed)|statistical(ly)? (analys|signific)|analyses (were|are)|"
                       r"defined as|power calculation|sample size calculation|indicates EM|e\.g\.|abbreviations|"
                       r"inclusion criteria|search strategy|was set at|were set at)", re.I)
RE_EFEITO = re.compile(r"(reduc|increas|decreas|improv|associat|lower|higher|risk|benefit|no (significant )?(effect|difference)|"
                       r"did not|was not|were not|changed|attenuat|elevat|declin)", re.I)


def _pontua(f, pg):
    if not (50 <= len(f) <= 480) or not RE_EST.search(f) or RE_METODO.search(f):
        return None
    if f.count(";") > 4 or re.search(r"doi:|https?://", f) or sum(c.isdigit() for c in f) > 0.3 * len(f):
        return None
    s = 0
    if re.search(r"95\s*%\s*(CI|confidence|IC)\s*[:,=]?\s*[\[(]?\s*[-−–]?\d|[\[(]\s*[-−–]?\d+[.,·]\d+\s*(to|–|,)\s*[-−–]?\d", f, re.I):
        s += 3
    if re.search(r"\b(RR|HR|OR|SMD|WMD|MD|IRR)\b", f):
        s += 2
    if RE_EFEITO.search(f):
        s += 2
    if re.search(r"(table|fig\.|figure|supplementa)", f, re.I):
        s -= 2
    if pg == "resumo":
        s += 2
    return s


def achados(pags, resumo="", n=10):
    cand, vistos = [], set()
    fontes = [("resumo", [resumo.replace("\n", " ")])] if resumo else []
    fontes += [(pg, paras) for pg, paras in enumerate(pags, 1)]
    for pg, paras in fontes:
        for p in paras:
            if len(p) < 60:
                continue
            for f in frases(p):
                s = _pontua(f, pg)
                if s is None or s < 2:
                    continue
                chave = sa(f)[:70]
                if chave in vistos:
                    continue
                vistos.add(chave)
                cand.append((s, 0 if pg == "resumo" else pg, pg, f))
    melhores = sorted(cand, key=lambda x: -x[0])[:n]
    return [{"p": pg, "frase": f} for _, _, pg, f in sorted(melhores, key=lambda x: x[1])]


def frases_com(pags, pad, n, desde=0.0):
    out = []
    ini = int(len(pags) * desde)
    for pg, paras in enumerate(pags[ini:], ini + 1):
        for p in paras:
            for f in frases(p):
                if re.search(pad, f, re.I) and 60 <= len(f) <= 450 and sum(c.isupper() for c in f) < 0.3 * len(f):
                    out.append({"p": pg, "frase": f})
                    if len(out) >= n:
                        return out
    return out


RE_INDUSTRIA = r"\b(Inc\.?|Ltd\.?|GmbH|S\.A\.|Nestl|Danone|Abbott|Herbalife|Coca-Cola|PepsiCo|Unilever|Mars,|Kellogg|Bayer|Pfizer|Novo Nordisk|Eli Lilly|Lilly|DSM|Yakult|Glanbia|Nutricia|AstraZeneca|Sanofi|Amgen|Merck|Novartis|industry)\b"


def conclusao_do_resumo(resumo):
    m = re.search(r"(?:^|\n)\s*(conclusions?(?: and relevance)?|interpretation|implications|conclus(?:ao|oes|ão|ões)|significance)\s*:\s*(.+?)(?=\n[A-Z][\w ,&/-]{2,45}:|\Z)", resumo, re.I | re.S)
    if m:
        return re.sub(r"\s+", " ", m.group(2)).strip()
    fs = frases(resumo.replace("\n", " "))
    concl = [f for f in fs if re.search(r"(?i)\b(in conclusion|we conclude|these (findings|results) (suggest|indicate|show)|our (findings|results) (suggest|indicate|show)|overall,)", f)]
    return " ".join(concl[:2]) if concl else (" ".join(fs[-2:]) if len(fs) >= 4 else "")


def conclusao_do_texto(pags):
    for pg in range(len(pags) - 1, -1, -1):
        paras = pags[pg]
        for k, p in enumerate(paras):
            m = re.match(r"^(\d+\.?\s*)?(conclusions?|concluding remarks|conclus[aã]o|conclus[oõ]es)\s*:?\s*(.*)$", p, re.I)
            if m and len(p) < 2000:
                corpo = m.group(3).strip()
                seguinte = paras[k + 1:k + 4] + (pags[pg + 1][:2] if pg + 1 < len(pags) else [])
                for q in seguinte:
                    if len(corpo.split()) > 140 or re.match(r"(?i)^(\d+\.?\s*)?(acknowledg|funding|author|conflict|declaration|data availab|abbreviations|references)", q):
                        break
                    corpo += " " + q
                corpo = " ".join(corpo.split()[:170])
                if len(corpo) > 80:
                    return {"p": pg + 1, "texto": corpo}
    return None


def resumo_do_pdf(paras1):
    t = "\n".join(paras1)
    m = re.search(r"(?is)\b(abstract|summary|resumo)\b\s*:?\s*(.+?)(?=\n\s*(keywords?|key words|palavras-chave|introduction|1\.?\s+introduction|background\n))", t)
    if not m:
        return ""
    return " ".join(m.group(2).split()[:380])


def tamanho_amostra(texto):
    out = {}
    m = re.search(r"(\d{1,3}(?:[,.]\d{3})+|\d+)\s+(randomi[sz]ed (controlled )?trials|RCTs|studies|trials|cohorts|articles|publications)\b[^.]{0,40}?\b(were |was )?(included|identified|eligible|met|comprising|involving)", texto, re.I)
    if m:
        out["n_estudos"] = m.group(0)[:90]
    m = re.search(r"(\d{1,3}(?:[,.]\d{3})+|\d{2,})\s+(participants|patients|subjects|adults|children|adolescents|women|men|individuals|volunteers|athletes|people|persons)\b", texto, re.I)
    if m:
        out["n"] = m.group(0)[:60]
    return out


def eixos_de(m, resumo, regras):
    titulo = " " + sa(m.get("titulo", "")) + " "
    resto = " " + sa(" ".join(m.get("palavras_chave", []) + m.get("mesh", [])) + " " + resumo) + " "
    pont = []
    for eixo, termos in regras.items():
        s = 0
        for termo in termos:
            partes = [sa(x) for x in termo.split("&")]
            def tem(alvo):
                return all(re.search(r"(?<![a-z0-9])" + re.escape(x), alvo) for x in partes)
            if tem(titulo):
                s += 3
            elif tem(resto):
                s += 1
        if s >= 2:
            pont.append((s, eixo))
    return [e for _, e in sorted(pont, reverse=True)[:3]]


# ---------------------------------------------------------------- processamento de um PDF
def processar(pdf, origem, conf, regras):
    st = pdf.stat()
    info = {"arquivo": str(pdf), "origem": origem, "tamanho": st.st_size, "mtime": int(st.st_mtime)}
    if getattr(st, "st_file_attributes", 0) & (0x400000 | 0x1000):  # RECALL_ON_DATA_ACCESS | OFFLINE
        return {**info, "fora": NUVEM}
    if st.st_size > conf.get("limite_mb", 40) * 1024 * 1024:
        return {**info, "fora": "arquivo grande demais (provável livro)"}
    brutas = extrair_paginas(pdf)
    total = sum(len(p) for p in brutas)
    if total < 1500:
        return {**info, "fora": "sem texto extraível (PDF escaneado ou imagem)"}
    pags = tirar_repetidos([paragrafos(p) for p in brutas])
    m, como = obter_metadados(brutas, pags[0] if pags else [], pdf.stem)
    if len(brutas) > conf.get("limite_paginas_livro", 160) and not re.search(r"(?i)guideline|diretriz|consensus|report", m["titulo"] + pdf.stem):
        return {**info, "fora": f"{len(brutas)} páginas (livro)", "titulo": m["titulo"]}
    resumo = m["resumo"] or resumo_do_pdf(pags[0] if pags else [])
    funding = frases_com(pags, r"(funded by|funding|financial support|supported by (a |an )?(grant|research)|conflicts? of interest|competing interests?|declaration of interest|disclosure)", 3)
    corpo = cortar_referencias(pags)
    tipo = classificar(m["titulo"], m["tipos_pub"], resumo)
    texto_corpo = " ".join(" ".join(p) for p in corpo)
    amostra = tamanho_amostra(resumo + " " + texto_corpo[:20000])
    concl_txt = conclusao_do_texto(corpo)
    art = {
        "versao": VERSAO,
        "titulo": m["titulo"],
        "referencia": {"vancouver": vancouver(m), "autores": m["autores"], "primeiro_autor": m["primeiro_autor"],
                       "ano": m["ano"], "revista": m["revista"], "doi": m["doi"], "pmid": m["pmid"],
                       "link": f"https://doi.org/{m['doi']}" if m["doi"] else (f"https://pubmed.ncbi.nlm.nih.gov/{m['pmid']}/" if m["pmid"] else "")},
        "tipo": tipo,
        "certeza_teto": teto_certeza(tipo, resumo),
        "eixos": eixos_de(m, resumo, regras),
        "palavras_chave": [k for k in (m["palavras_chave"] + m["mesh"]) if k][:16],
        **amostra,
        "resumo": resumo,
        "conclusao_autores": conclusao_do_resumo(resumo) if resumo else "",
        "conclusao_texto": concl_txt,
        "achados": achados(corpo, resumo),
        "limitacoes": frases_com(corpo, r"\blimitations?\b|\blimited by\b|interpreted with caution|should be interpreted|\bweakness|\bcaveat", 3, desde=0.3),
        "financiamento": funding,
        "industria": bool(any(re.search(RE_INDUSTRIA, f["frase"]) for f in funding)),
        "paginas": len(brutas),
        "metadados": f"{m['fonte_metadados']} ({como})",
    }
    if m["fonte_metadados"] == "pdf":
        art["aviso"] = "metadados tirados só do PDF (sem DOI reconhecido): confira autor, ano e revista antes de citar"
    if tipo == "errata":
        art["aviso"] = "errata/correção: não é evidência por si; procure o artigo original"
    return {**info, "art": art, "texto": [(f"p. {i + 1}", paras) for i, paras in enumerate(corpo)]}


# ---------------------------------------------------------------- fontes da fila (diretrizes, consensos, Reviews) e do cofre
def ler_fm(p):
    t = p.read_text(encoding="utf-8-sig", errors="replace")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", t, re.S)
    fm = {}
    for l in (m.group(1).splitlines() if m else []):
        k, sep, v = l.partition(":")
        if not sep or not re.fullmatch(r"[\w-]+", k.strip()):
            continue
        v = v.strip()
        try:
            fm[k.strip()] = json.loads(v) if v[:1] in "[\"" else v
        except ValueError:  # lista no estilo YAML sem aspas: [a, b]
            fm[k.strip()] = [x.strip(" '\"") for x in v.strip("[]").split(",") if x.strip()] if v[:1] == "[" else v.strip('"')
    return fm, (m.group(2) if m else t)


def _vancouver_da_nota(corpo):
    m = re.search(r"(?m)^(?:\*\*)?Vancouver(?:\*\*)?\s*:\s*(.+)$", corpo) or re.search(r"## Refer[êe]ncia\n+(.+)", corpo)
    return m.group(1).strip() if m else ""


def fichas_da_base():
    """Todas as Fichas: 01 - BASE CIENTÍFICA/**/<Tema> - Ficha.md (fora de _MÁQUINA)."""
    out = []
    for d, dirs, arqs in os.walk(BASE):
        dirs[:] = [x for x in dirs if x != "_MÁQUINA" and not x.startswith(".")]
        out += [Path(d) / a for a in arqs if nfc(a).endswith(" - Ficha.md")]
    return sorted(out, key=lambda p: sa(nfc(p.stem)))


def selecao_fila():
    """Diretrizes/consensos/posicionamentos e fontes das Reviews (fila.jsonl) + notas de artigo já processadas (fontes-processadas)."""
    sel = []
    if FILA_JSONL.exists():
        for l in FILA_JSONL.read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            fm = json.loads(l)
            cur = " ".join(str(x) for x in lista(fm.get("curadoria")))
            if fm.get("subtipo") in SUBTIPOS_ALTOS or "Reviews" in cur or "Treino de força" in cur:
                origem = "fila/" + ("Reviews Igor Eckert" if "Reviews" in cur else
                                    "treino de força" if "Treino de força" in cur else "diretrizes")
                sel.append({"nome": nfc(fm["titulo"]), "fm": fm, "vancouver": fm.get("vancouver", ""),
                            "links": fm.get("links", []), "origem": origem, "nota": None})
    for p in sorted(PROCESSADAS.glob("*.md")):
        fm, corpo = ler_fm(p)
        if fm.get("tipo") != "artigo":  # conceitos de avaliação (Motor 1) servem à Ficha, não são artigos do catálogo
            continue
        links = sorted(set(re.findall(r"https?://[^\s)>\]]+", corpo)))[:2]
        sel.append({"nome": nfc(p.stem), "fm": fm, "vancouver": _vancouver_da_nota(corpo), "links": links,
                    "origem": "cofre/processado", "nota": p, "processado": True})
    return sel


def texto_da_fila(it):
    """Onde está o texto: baixado pelo importar-fila, texto limpo de fonte processada ou (processado) a própria nota."""
    for pasta in (FONTES_FILA, TEXTO_FONTES):
        p = pasta / f"{it['nome']}.txt"
        if p.exists():
            return p
    return it["nota"] if it.get("processado") else None


def secoes_de_texto(t):
    """Texto em markdown (## Seção) → [(título, [parágrafos])]. Pula o cabeçalho da fila, se houver."""
    if "=" * 30 + " TEXTO " in t:
        t = t.split("=" * 30 + " TEXTO ", 1)[1].split("\n", 1)[-1]
    t = re.sub(r"(?s)^---\n.*?\n---\n", "", t)
    secs, titulo, buf = [], "início", []
    for l in t.splitlines():
        m = re.match(r"^#{1,4}\s+(.+)$", l)
        if m:
            if buf:
                secs.append((titulo, buf))
            titulo, buf = re.sub(r"[*_`\[\]]", "", m.group(1)).strip()[:80], []
        elif l.strip():
            buf.append(re.sub(r"\s+", " ", l.strip()))
    if buf:
        secs.append((titulo, buf))
    return secs


def processar_fila(it, tp, regras):
    st = tp.stat()
    info = {"arquivo": str(tp), "origem": it["origem"], "tamanho": st.st_size, "mtime": int(st.st_mtime)}
    fm = it["fm"]
    doi = str(fm.get("doi") or "").strip()
    m = None
    if doi:
        r = epmc(f'DOI:"{doi}"')
        m = meta_epmc(r[0]) if r else None
        if not m:
            c = (http_json("https://api.crossref.org/works/" + urllib.parse.quote(doi)) or {}).get("message")
            m = meta_crossref(c) if c else None
    if not m:
        m = {"titulo": fm.get("titulo_original") or it["nome"], "autores": "", "primeiro_autor": fm.get("primeiro_autor", ""),
             "revista": fm.get("periodico", ""), "ano": int(fm["ano"]) if str(fm.get("ano", "")).isdigit() else None,
             "volume": "", "numero": "", "paginas": "", "doi": doi, "pmid": str(fm.get("pmid") or ""), "pmcid": "",
             "resumo": "", "tipos_pub": [], "palavras_chave": [], "mesh": [], "fonte_metadados": "fila"}
    if fm.get("primeiro_autor") and re.search(r"(?i)committee|group|members|panel|consortium|working|task force", m["primeiro_autor"] or "x"):
        m["primeiro_autor"] = fm["primeiro_autor"]  # autor coletivo: usa o nome da fila (ex.: Blumenthal)
    ref_fila = it.get("vancouver") or ""
    secs = [s for s in secoes_de_texto(tp.read_text(encoding="utf-8-sig", errors="replace")) if s[1]]
    if not secs:
        return {**info, "fora": "sem texto (arquivo vazio)"}
    titulos, pags = [s[0] for s in secs], [s[1] for s in secs]
    resumo = m["resumo"] or " ".join(next((p for t, p in secs if re.search(r"(?i)^(resumo|abstract|summary)", t)), []))[:3000]
    tipo = fm.get("subtipo") if fm.get("subtipo") in TETO else classificar(m["titulo"], m["tipos_pub"], resumo)

    def sec(lst):
        for x in lst:
            if isinstance(x.get("p"), int):
                x["sec"] = titulos[x.pop("p") - 1]
            elif "p" in x:
                x["sec"] = x.pop("p")
        return lst

    concl = conclusao_do_texto(pags)
    if concl:
        concl = {"sec": titulos[concl["p"] - 1], "texto": concl["texto"]}
    funding = sec(frases_com(pags, r"(funded by|funding|financial support|conflicts? of interest|competing interests?|disclosure|financiamento|conflito)", 3))
    art = {
        "versao": VERSAO,
        "titulo": m["titulo"],
        "referencia": {"vancouver": vancouver(m) if m["fonte_metadados"] != "fila" or not ref_fila else ref_fila,
                       "autores": m["autores"], "primeiro_autor": m["primeiro_autor"], "ano": m["ano"], "revista": m["revista"],
                       "doi": m["doi"] or doi, "pmid": m["pmid"],
                       "link": f"https://doi.org/{m['doi'] or doi}" if (m["doi"] or doi) else str(fm.get("link") or "")},
        "tipo": tipo,
        "certeza_teto": teto_certeza(tipo, resumo),
        "eixos": [e for e in lista(fm.get("eixos")) if e] or eixos_de(m, resumo, regras),
        "palavras_chave": [k for k in (m["palavras_chave"] + m["mesh"] + lista(fm.get("subtemas"))) if k][:16],
        **tamanho_amostra(resumo + " " + " ".join(" ".join(p) for p in pags)[:20000]),
        "resumo": resumo,
        "conclusao_autores": conclusao_do_resumo(resumo) if resumo else "",
        "conclusao_texto": concl,
        "recomendacoes": sec(frases_com(pags, r"\b(we recommend|is recommended|are recommended|we suggest|is suggested|should (be|not)|"
                                              r"recomenda|recomendad[ao]s?|sugere-se|deve(m)? ser|não deve|class (I|IIa|IIb|III)\b|"
                                              r"grade [ABC]\b|(strong|conditional|weak) recommendation|level of evidence|nível de evidência|"
                                              r"grau de recomendação|força da recomendação)", 15)),
        "achados": sec(achados(pags, resumo)),
        "limitacoes": sec(frases_com(pags, r"\blimitations?\b|\blimited by\b|interpreted with caution|\bweakness|\blimitaç", 3, desde=0.3)),
        "financiamento": funding,
        "industria": bool(any(re.search(RE_INDUSTRIA, f["frase"]) for f in funding)),
        "localizador": "seção",
        "metadados": f"{m['fonte_metadados']} (fila: {it['nome']})",
    }
    if it.get("processado"):
        art["aviso"] = "fonte já processada no cofre: para afirmar, prefira a nota processada e a Ficha de conteúdo"
    elif "## [Trechos omitidos pelo filtro" in tp.read_text(encoding="utf-8-sig", errors="replace"):
        art["aviso"] = "texto reduzido pelo filtro temático do /processar-tema: partes da diretriz ficaram de fora"
    return {**info, "art": art, "texto": [(f"seç. {t}", p) for t, p in secs]}


def importar_fila(args):
    """Planeja (e com --baixar, baixa) o texto completo de acesso aberto das diretrizes/consensos/Reviews da fila (fila.jsonl)."""
    global SEM_REDE
    SEM_REDE = args.sem_rede
    sel = [it for it in selecao_fila() if not it.get("processado")]
    dois_cat = set()
    if CATALOGO.exists():
        dois_cat = {(json.loads(l).get("doi") or "").lower() for l in CATALOGO.read_text(encoding="utf-8").splitlines() if l.strip()}
    if args.baixar:
        sys.path.insert(0, str(AQUI))
        from texto_aberto import baixar, jats_para_texto, pmc_html_para_texto  # noqa: E402
    FONTES_FILA.mkdir(parents=True, exist_ok=True)
    plano, manual, por_eixo = collections.Counter(), [], collections.defaultdict(collections.Counter)
    for k, it in enumerate(sel, 1):
        fm = it["fm"]
        doi = str(fm.get("doi") or "").lower()
        pmcid = str(fm.get("pmcid") or "")
        if doi and doi in dois_cat:
            rota = "já no catálogo (PDF)"
        elif texto_da_fila(it):
            rota = "texto pronto"
        else:
            if not pmcid and doi:
                r = epmc(f'DOI:"{doi}"')
                pmcid = (r[0].get("pmcid") or "") if r else ""
            rota = "acesso aberto (PMC)" if pmcid else "baixar à mão"
            if pmcid and args.baixar:
                bruto = ""
                try:
                    bruto = jats_para_texto(baixar(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"))
                except Exception:  # noqa: BLE001
                    pass
                if len(bruto.split()) < 800:
                    try:
                        bruto = pmc_html_para_texto(baixar(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"))
                    except Exception:  # noqa: BLE001
                        bruto = ""
                if len(bruto.split()) >= 800:
                    (FONTES_FILA / f"{it['nome']}.txt").write_text(f"# {it['nome']}\n# origem: {pmcid}\n" + bruto, encoding="utf-8")
                    rota = "baixado agora"
                else:
                    rota = "baixar à mão"
                time.sleep(0.6)
        plano[rota] += 1
        por_eixo[fm.get("eixo_principal") or "?"][rota] += 1
        if rota == "baixar à mão":
            manual.append(it)
        if args.baixar and k % 20 == 0:
            print(f"  {k}/{len(sel)}", flush=True)
    print(f"\nFila selecionada (diretriz/consenso/posicionamento + Reviews): {len(sel)} fontes")
    for rota, n in plano.most_common():
        print(f"  {rota}: {n}")
    print("\nPor eixo (pronto+aberto / à mão):")
    print("  " + " · ".join(f"{e} {c['texto pronto'] + c['baixado agora'] + c['já no catálogo (PDF)'] + c['acesso aberto (PMC)']}/{c['baixar à mão']}"
                           for e, c in sorted(por_eixo.items())))
    with open(PARA_BAIXAR, "w", encoding="utf-8") as fh:
        fh.write("---\ntipo: lista-download\n---\n# Para baixar: diretrizes, consensos e fontes das Reviews\n\n"
                 "Sem acesso aberto pela PMC. Baixe o PDF (site da sociedade, SciELO, revista ou o seu acesso) e solte em "
                 "`01 - BASE CIENTÍFICA/ENTRADA/` com **qualquer nome**: o `catalogar` reconhece pelo DOI e guarda em `_MÁQUINA/pdf`.\n\n")
        for eixo in sorted({it["fm"].get("eixo_principal") or "?" for it in manual}):
            fh.write(f"\n## {eixo}\n")
            for it in [x for x in manual if (x["fm"].get("eixo_principal") or "?") == eixo]:
                fm = it["fm"]
                fh.write(f"- [ ] **{it['nome']}** · {fm.get('subtipo', '')} · acesso: {fm.get('acesso', '?')}"
                         + (f" · DOI {fm['doi']}" if fm.get("doi") else "") + "\n" + "".join(f"  - {l}\n" for l in it["links"]))
    print(f"\nLista do que baixar à mão: {PARA_BAIXAR}")
    if not args.baixar and plano["acesso aberto (PMC)"]:
        print(f"Para baixar os {plano['acesso aberto (PMC)']} de acesso aberto: python biblioteca.py importar-fila --baixar")


# ---------------------------------------------------------------- catálogo
def listar_pdfs(conf):
    pdfs = []
    for item in conf["incluir"]:
        if "arquivo" in item:
            p = Path(item["arquivo"])
            p = p if p.is_absolute() else BASE / p
            if p.exists():
                pdfs.append((p, item["origem"]))
            continue
        raiz = Path(item["pasta"])
        raiz = raiz if raiz.is_absolute() else BASE / raiz  # pastas do JSON são relativas a "01 - BASE CIENTÍFICA"
        if not raiz.exists():
            continue
        it = raiz.rglob("*") if item.get("recursivo") else raiz.glob("*")
        for p in it:
            if p.is_file() and p.suffix.lower() == ".pdf":
                rel = p.relative_to(raiz)
                if any(any(sa(x) in sa(seg) for x in conf["ignorar_subpastas_com"]) for seg in rel.parts[:-1]):
                    continue
                sub = rel.parts[0] if len(rel.parts) > 1 else ""
                pdfs.append((p, item["origem"] + (f"/{sub}" if sub else "")))
    return pdfs


def nome_seguro(t):
    t = nfc(t)
    t = re.sub(r"[\\/:*?\"<>|\[\]#^{}]", " ", t)
    return re.sub(r"\s+", " ", t).strip(" .-,")


def fazer_id(art, stem, usados):
    r = art["referencia"]
    sob = nome_seguro(r.get("primeiro_autor") or "")
    ano = r.get("ano") or ""
    tit = nome_seguro(art["titulo"] or stem)
    curto = " ".join(tit.split()[:9])
    base = f"{sob} {ano} - {curto}" if sob else (f"{ano} - {curto}" if ano else curto)
    base = re.sub(r"\s+", " ", base)[:95].rstrip(" -.,")
    nid, k = base, 2
    while sa(nid) in usados:
        nid, k = f"{base} ({k})", k + 1
    usados.add(sa(nid))
    return nid


def mapa_notas_processadas():
    """DOI → nota processada (fontes-processadas) ou título na fila (fila.jsonl); e nota → Ficha que a usa."""
    doi_nota, nota_ficha = {}, {}
    if FILA_JSONL.exists():
        for l in FILA_JSONL.read_text(encoding="utf-8").splitlines():
            if l.strip():
                fm = json.loads(l)
                d = str(fm.get("doi") or "").lower()
                if d.startswith("10."):
                    doi_nota.setdefault(d, (nfc(fm["titulo"]), True))
    for p in PROCESSADAS.glob("*.md"):  # nota processada vence a da fila
        try:
            cab = p.read_text(encoding="utf-8-sig", errors="replace")[:2500]
        except OSError:
            continue
        m = re.search(r"(?im)^doi:\s*\"?([^\"\s]+)", cab)
        if m and m.group(1).lower().startswith("10.") and re.search(r"(?m)^tipo:\s*artigo", cab):
            doi_nota[m.group(1).lower()] = (nfc(p.stem), False)
    for f in fichas_da_base():
        cab = f.read_text(encoding="utf-8-sig", errors="replace")[:4000]
        for n in re.findall(r"\[\[([^\]|]+)", cab):
            nota_ficha.setdefault(nfc(n), nfc(f.stem))
    return doi_nota, nota_ficha


def _sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def so_na_nuvem(p):
    return bool(getattr(p.stat(), "st_file_attributes", 0) & (0x400000 | 0x1000))


def descartar_copias_exatas(pdfs):
    """PDF da ENTRADA idêntico (hash) a um de _MÁQUINA/pdf, ou a outro da própria ENTRADA: só remove a cópia da ENTRADA."""
    na_entrada = [p for p, _ in pdfs if ENTRADA in p.parents and not so_na_nuvem(p)]
    if not na_entrada:
        return pdfs
    vistos = {_sha1(p) for p in PDFS.glob("*.pdf")}
    removidos = set()
    for p in sorted(na_entrada):
        h = _sha1(p)
        if h in vistos:
            p.unlink()
            removidos.add(p)
            print(f"  cópia exata já catalogada: removi {p.name} da ENTRADA")
        else:
            vistos.add(h)
    return [(p, o) for p, o in pdfs if p not in removidos]


def organizar_entrada(resultados, artigos, novo_estado):
    """PDF que veio da ENTRADA: catalogado → vai para _MÁQUINA/pdf; duplicata do mesmo artigo (arquivo diferente) → _MÁQUINA/pdf/_duplicatas
    (nunca apaga o que não é cópia exata); falhas (sem texto, nuvem, livro, erro) ficam na ENTRADA."""
    ficaram, movidos, dups = [], 0, 0
    PDFS.mkdir(parents=True, exist_ok=True)

    def livre(pasta, nome):
        dest, k = pasta / nome, 2
        while dest.exists():
            dest = pasta / f"{Path(nome).stem} ({k}){Path(nome).suffix}"
            k += 1
        return dest

    entrada = [r for r in resultados if ENTRADA in Path(r["arquivo"]).parents and Path(r["arquivo"]).exists()]
    for r in sorted(entrada, key=lambda x: (str(novo_estado.get(x["arquivo"], {}).get("fora", "")).startswith("duplicata"), x["arquivo"])):
        p = Path(r["arquivo"])
        e = novo_estado.get(r["arquivo"])
        if e is None:
            continue
        if e.get("id"):  # artigo novo
            dest = livre(PDFS, p.name)
            shutil.move(str(p), str(dest))
            art = artigos[e["id"]]
            art["arquivos"] = [str(dest) if x == r["arquivo"] else x for x in art["arquivos"]]
            novo_estado[str(dest)] = novo_estado.pop(r["arquivo"])
            movidos += 1
        elif str(e.get("fora", "")).startswith("duplicata de "):
            alvo = artigos.get(e["fora"][len("duplicata de "):])
            h = _sha1(p)
            iguais = [x for x in (alvo["arquivos"] if alvo else []) if x != r["arquivo"] and Path(x).exists() and _sha1(x) == h]
            if alvo:
                alvo["arquivos"] = [x for x in alvo["arquivos"] if x != r["arquivo"]]
            if iguais:
                p.unlink()
                print(f"  duplicata exata de {Path(iguais[0]).name}: removi {p.name} da ENTRADA")
            else:
                DUPLICATAS.mkdir(parents=True, exist_ok=True)
                dest = livre(DUPLICATAS, p.name)
                shutil.move(str(p), str(dest))
                print(f"  mesmo artigo, arquivo diferente: {p.name} → {dest.relative_to(MAQ)} (confira e apague à mão se quiser)")
            novo_estado.pop(r["arquivo"], None)
            dups += 1
        else:
            ficaram.append((p.name, e.get("fora", "")))
    if movidos or dups:
        print(f"ENTRADA: {movidos} PDF(s) catalogado(s) e movido(s) para _MÁQUINA/pdf · {dups} duplicata(s) tratada(s).")
    for nome, motivo in ficaram:
        print(f"  ficou na ENTRADA: {nome}: {motivo}")


def catalogar(args):
    global SEM_REDE
    SEM_REDE = args.sem_rede
    conf = json.loads(CONF.read_text(encoding="utf-8"))
    regras = json.loads(EIXOS.read_text(encoding="utf-8"))["eixos"]
    for d in (ARTS, TXT, PDFS, ENTRADA, CACHE):
        d.mkdir(parents=True, exist_ok=True)
    estado = json.loads(ESTADO.read_text(encoding="utf-8")) if ESTADO.exists() and not args.forcar else {}
    pdfs = descartar_copias_exatas(listar_pdfs(conf))
    if args.limite:
        pdfs = pdfs[:args.limite]
    fila = [(it, texto_da_fila(it)) for it in selecao_fila()]
    fila = [(it, tp) for it, tp in fila if tp]
    print(f"{len(pdfs)} PDFs (ENTRADA + _MÁQUINA/pdf) · {len(fila)} textos da fila e das fontes processadas (diretrizes, consensos, Reviews, processados).")
    fontes = [("pdf", p, origem, p) for p, origem in pdfs] + [("fila", (it, tp), it["origem"], tp) for it, tp in fila]

    pendentes, reaproveitados = [], []
    for tipo_f, obj, origem, p in fontes:
        st = p.stat()
        e = estado.get(str(p))
        if e and e.get("tamanho") == st.st_size and e.get("mtime") == int(st.st_mtime) and e.get("versao") == VERSAO \
                and not (e.get("fora") or "").startswith(REPETIR) \
                and (e.get("fora") or (ARTS / f"{e['id']}.json").exists()):
            reaproveitados.append((p, origem, e))
        else:
            pendentes.append((tipo_f, obj, origem, p))
    print(f"{len(reaproveitados)} sem mudança (reaproveitados) · {len(pendentes)} para processar.")

    def roda(tipo_f, obj, origem):
        return processar(obj, origem, conf, regras) if tipo_f == "pdf" else processar_fila(obj[0], obj[1], regras)

    resultados, t0 = [], time.time()
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futuros = {ex.submit(roda, t, ob, o): (p, o) for t, ob, o, p in pendentes}
        for k, fu in enumerate(cf.as_completed(futuros), 1):
            p, o = futuros[fu]
            try:
                resultados.append(fu.result())
            except Exception as err:  # noqa: BLE001
                st = p.stat()
                resultados.append({"arquivo": str(p), "origem": o, "tamanho": st.st_size, "mtime": int(st.st_mtime),
                                   "fora": f"erro: {type(err).__name__}: {str(err)[:120]}"})
            if k % 25 == 0 or k == len(pendentes):
                print(f"  {k}/{len(pendentes)} ({time.time() - t0:.0f} s)", flush=True)

    # ids e duplicatas: primeiro os reaproveitados (mantêm o id), depois os novos em ordem de caminho
    usados, por_doi, por_titulo, novo_estado, fora = set(), {}, {}, {}, []
    artigos = {}
    for p, origem, e in reaproveitados:
        if e.get("fora"):
            fora.append({"arquivo": str(p), "origem": origem, "motivo": e["fora"]})
            novo_estado[str(p)] = e
            continue
        art = json.loads((ARTS / f"{e['id']}.json").read_text(encoding="utf-8"))
        usados.add(sa(e["id"]))
        artigos[e["id"]] = art
        if art["referencia"].get("doi"):
            por_doi[art["referencia"]["doi"].lower()] = e["id"]
        por_titulo[sa(art["titulo"])[:80]] = e["id"]
        novo_estado[str(p)] = e
    for r in sorted(resultados, key=lambda x: (x["origem"].startswith(("fila", "cofre")), x["arquivo"])):  # PDF primeiro
        base_e = {"tamanho": r["tamanho"], "mtime": r["mtime"], "versao": VERSAO}
        if r.get("fora"):
            fora.append({"arquivo": r["arquivo"], "origem": r["origem"], "motivo": r["fora"]})
            novo_estado[r["arquivo"]] = {**base_e, "fora": r["fora"]}
            continue
        art = r["art"]
        doi = (art["referencia"].get("doi") or "").lower()
        chave_t = sa(art["titulo"])[:80]
        dup = por_doi.get(doi) if doi else None
        dup = dup or (por_titulo.get(chave_t) if len(chave_t) > 30 else None)
        if dup:
            alvo = artigos[dup]
            if r["arquivo"] not in alvo["arquivos"] and ENTRADA not in Path(r["arquivo"]).parents:  # cópia da ENTRADA não fica registrada
                alvo["arquivos"].append(r["arquivo"])
                alvo["origens"] = sorted(set(alvo.get("origens", []) + [r["origem"]]))
            fora.append({"arquivo": r["arquivo"], "origem": r["origem"], "motivo": f"duplicata de {dup}"})
            novo_estado[r["arquivo"]] = {**base_e, "fora": f"duplicata de {dup}"}
            continue
        aid = fazer_id(art, Path(r["arquivo"]).stem, usados)
        art = {"id": aid, **art, "arquivos": [r["arquivo"]], "origens": [r["origem"]], "texto": f"texto/{aid}.txt"}
        artigos[aid] = art
        if doi:
            por_doi[doi] = aid
        por_titulo[chave_t] = aid
        with open(TXT / f"{aid}.txt", "w", encoding="utf-8") as fh:
            fh.write(f"# {art['titulo']}\n# {art['referencia']['vancouver']}\n")
            for marca, paras in r["texto"]:
                fh.write(f"\n[{marca}]\n" + "\n".join(paras) + "\n")
        novo_estado[r["arquivo"]] = {**base_e, "id": aid}

    organizar_entrada(resultados, artigos, novo_estado)
    doi_nota, nota_ficha = mapa_notas_processadas()
    for aid, art in artigos.items():
        art.pop("nota_processada", None), art.pop("na_fila", None), art.pop("ficha", None)
        nota = doi_nota.get((art["referencia"].get("doi") or "").lower())
        if nota:
            if nota[1]:
                art["na_fila"] = nota[0]
            else:
                art["nota_processada"] = nota[0]
                if nota[0] in nota_ficha:
                    art["ficha"] = nota_ficha[nota[0]]
        (ARTS / f"{aid}.json").write_text(json.dumps(art, ensure_ascii=False, indent=1), encoding="utf-8")

    for pasta, ext in ((ARTS, ".json"), (TXT, ".txt")):
        for f in pasta.glob("*" + ext):
            if f.stem not in artigos:
                f.unlink()

    # catálogo enxuto + índice de busca + índice em markdown
    linhas, busca = [], {}
    for aid in sorted(artigos, key=lambda a: sa(a)):
        a = artigos[aid]
        concl = a.get("conclusao_autores") or (a.get("conclusao_texto") or {}).get("texto", "")
        linhas.append(json.dumps({
            "id": aid, "titulo": a["titulo"], "ano": a["referencia"].get("ano"), "tipo": a["tipo"],
            "certeza_teto": a["certeza_teto"]["nivel"], "eixos": a["eixos"], "n": a.get("n") or a.get("n_estudos", ""),
            "revista": a["referencia"].get("revista"), "doi": a["referencia"].get("doi"),
            "origens": a.get("origens", []), "processado": a.get("nota_processada") or "",
            "conclusao": concl[:240]}, ensure_ascii=False))
        busca[aid] = {"t": sa(a["titulo"]), "k": sa(" ".join(a.get("palavras_chave", []) + a.get("origens", []))),
                      "r": sa(a.get("resumo", "") + " " + concl)}
    CATALOGO.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    BUSCA.write_text(json.dumps(busca, ensure_ascii=False), encoding="utf-8")
    FORA.write_text(json.dumps(sorted(fora, key=lambda x: x["motivo"]), ensure_ascii=False, indent=1), encoding="utf-8")
    ESTADO.write_text(json.dumps(novo_estado, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"\nPronto: {len(artigos)} artigos no catálogo · {len(fora)} fora (ver fora_do_catalogo.json) · {time.time() - t0:.0f} s")
    panorama(None)
    try:  # índice 01 - BASE CIENTÍFICA/00 - ÍNDICE.md (script irmão)
        if str(AQUI) not in sys.path:
            sys.path.insert(0, str(AQUI))
        import gerar_indice
        gerar_indice.gerar()
    except Exception as err:  # noqa: BLE001
        print(f"AVISO: não consegui gerar o índice ({type(err).__name__}: {err}); rode gerar_indice.py à mão.")


# ---------------------------------------------------------------- consulta
def carregar_catalogo():
    if not CATALOGO.exists():
        sys.exit("Catálogo ainda não existe: rode  python biblioteca.py catalogar")
    return [json.loads(l) for l in CATALOGO.read_text(encoding="utf-8").splitlines() if l.strip()]


def expandir(consulta, sinonimos):
    q = sa(consulta)
    grupos = []
    for chave in sorted(sinonimos, key=len, reverse=True):  # expressões de várias palavras primeiro
        if " " in chave and chave in q:
            grupos.append([chave] + [sa(x) for x in sinonimos[chave]])
            q = q.replace(chave, " ")
    for w in re.findall(r"[a-z0-9\-]+", q):
        if len(w) < 3 or w in {"de", "da", "do", "das", "dos", "e", "x", "vs", "com", "sem", "para", "no", "na", "em", "the", "and"}:
            continue
        grupos.append([w] + [sa(x) for x in sinonimos.get(w, [])])
    return grupos


def buscar(args):
    cat = {c["id"]: c for c in carregar_catalogo()}
    idx = json.loads(BUSCA.read_text(encoding="utf-8"))
    sinonimos = {sa(k): v for k, v in json.loads(EIXOS.read_text(encoding="utf-8"))["sinonimos"].items()}
    grupos = expandir(args.consulta, sinonimos)
    if not grupos:
        sys.exit("Consulta vazia.")
    minimo = len(grupos) if len(grupos) <= 2 else (len(grupos) + 1) // 2
    res = []
    for aid, c in cat.items():
        if args.eixo and args.eixo not in c["eixos"]:
            continue
        if args.tipo and c["tipo"] != args.tipo:
            continue
        if args.desde and (c["ano"] or 0) < args.desde:
            continue
        d = idx.get(aid, {})
        s, casou = 0.0, 0
        for g in grupos:
            melhor = 0
            for termo in g:
                pad = r"(?<![a-z0-9])" + re.escape(termo)
                if re.search(pad, d.get("t", "")):
                    melhor = max(melhor, 5)
                elif re.search(pad, d.get("k", "")):
                    melhor = max(melhor, 3)
                else:
                    n = len(re.findall(pad, d.get("r", "")))
                    melhor = max(melhor, min(n, 3))
            if melhor:
                casou += 1
                s += melhor
        if casou < minimo:
            continue
        s += PESO_TIPO.get(c["tipo"], 0) + max(0, min((c["ano"] or 2000) - 2015, 10)) * 0.15
        res.append((s, c))
    res.sort(key=lambda x: -x[0])
    if not res:
        print(f"Nada na biblioteca para '{args.consulta}'. Tente termos em inglês ou menos palavras.")
        return
    print(f"{len(res)} artigos para '{args.consulta}' (mostrando {min(args.n, len(res))}):\n")
    for k, (s, c) in enumerate(res[:args.n], 1):
        proc = f" · PROCESSADO: [[{c['processado']}]]" if c.get("processado") else ""
        print(f"[{k}] {c['id']}\n    {c['tipo']} (teto: {c['certeza_teto']}) · {c['revista'] or '?'} · eixos: {', '.join(c['eixos']) or '—'}"
              + (f" · {c['n']}" if c.get("n") else "") + proc)
        if c.get("conclusao"):
            print(f"    conclusão: {c['conclusao'][:220]}")
        print()


def achar_artigo(chave):
    alvo = sa(nfc(chave)).strip()
    exato = ARTS / f"{nome_seguro(chave)}.json"
    if exato.exists():
        return exato
    cands = [p for p in ARTS.glob("*.json") if alvo in sa(nfc(p.stem))]
    if len(cands) == 1:
        return cands[0]
    if not cands:
        sys.exit(f"Nenhum artigo com '{chave}'. Use 'buscar' para achar o id.")
    print("Mais de um artigo casa; seja mais específico:")
    for p in cands[:15]:
        print("  -", p.stem)
    sys.exit(1)


def ver(args):
    a = json.loads(achar_artigo(args.id).read_text(encoding="utf-8"))
    if not args.completo:
        for k in ("versao", "arquivos", "origens", "texto", "metadados"):
            a.pop(k, None)
        a["referencia"] = {k: v for k, v in a["referencia"].items() if k in ("vancouver", "link", "ano")}
    print(json.dumps(a, ensure_ascii=False, indent=1))


def trecho(args):
    p = achar_artigo(args.id)
    a = json.loads(p.read_text(encoding="utf-8"))
    linhas = (TXT / Path(a["texto"]).name).read_text(encoding="utf-8").splitlines()
    pad = re.compile(re.escape(sa(args.termo)))
    pg, achou = "?", 0
    print(f"{a['id']}  ({a['referencia']['vancouver'][:120]}…)\n")
    for l in linhas:
        m = re.match(r"^\[((?:p|seç)\. .+)\]$", l)
        if m:
            pg = m.group(1)
            continue
        if pad.search(sa(l)):
            i = pad.search(sa(l)).start()
            ini = max(0, i - args.janela // 2)
            print(f"[{pg}] …{l[ini:ini + args.janela]}…\n")
            achou += 1
            if achou >= args.n:
                break
    if not achou:
        print(f"'{args.termo}' não aparece no texto.")


# ---------------------------------------------------------------- conferência da Ficha (zero token)
def _num_norm(x):
    x = x.replace("−", "-").replace("–", "-")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", x):  # 1.234 (milhar em pt)
        return x.replace(".", "")
    return x.replace(",", ".")


def _nz(t):
    return re.sub(r"\s+", " ", re.sub(r"[/–—\-_,.()]", " ", sa(t))).strip()


def achar_ficha_arquivo(ref):
    """Caminho do .md, ou '<Tema> - Ficha' / 'Ficha - <Tema>' / '<Tema>' → arquivo em 01 - BASE CIENTÍFICA/**."""
    p = Path(ref)
    if p.exists() and p.is_file():
        return p
    n = re.sub(r"^\[\[|\]\]$|\.md$", "", ref.strip())
    tema = n[len("ficha - "):] if sa(n).startswith("ficha - ") else (n[:-len(" - ficha")] if sa(n).endswith(" - ficha") else n)
    todas = fichas_da_base()
    for p in todas:
        if sa(nfc(p.stem)[:-len(" - Ficha")]) == sa(nfc(tema)):
            return p
    sys.exit(f"Ficha '{ref}' não encontrada. Disponíveis: {', '.join(p.stem for p in todas) or '(nenhuma)'}")


def conferir_ficha(args):
    caminho = achar_ficha_arquivo(args.ficha)
    texto = caminho.read_text(encoding="utf-8-sig")
    m = re.search(r"(?ms)^---\n(.*?)\n---", texto.replace("\r\n", "\n"))
    fm = m.group(1) if m else ""
    nomes = re.findall(r"\[\[([^\]|]+)", re.search(r"(?m)^notas_base:.*$", fm).group(0)) if re.search(r"(?m)^notas_base:.*$", fm) else []
    # nota → artigo do catálogo: pelo id ou pela nota processada (campo nota_processada); o resto (Protocolo, conceitos) não é artigo
    por_nome = {}
    for pj in ARTS.glob("*.json"):
        a0 = json.loads(pj.read_text(encoding="utf-8"))
        por_nome[sa(nfc(a0["id"]))] = a0["id"]
        if a0.get("nota_processada"):
            por_nome.setdefault(sa(nfc(a0["nota_processada"])), a0["id"])
    notas_md = set()
    for d, dirs, arqs in os.walk(BASE):
        dirs[:] = [x for x in dirs if x not in ("_anexos", "ENTRADA") and not x.startswith(".") and not (x == "_MÁQUINA" and Path(d) == BASE)]
        notas_md |= {sa(nfc(a[:-3])) for a in arqs if a.endswith(".md")}
    notas_md |= {sa(nfc(p.stem)) for p in PROCESSADAS.glob("*.md")}
    erros, avisos, textos, arts, entradas = [], [], {}, {}, []   # entradas: (nome da nota, id do artigo ou None)
    for nome in nomes:
        aid = por_nome.get(sa(nfc(nome)))
        if aid:
            a = json.loads((ARTS / f"{aid}.json").read_text(encoding="utf-8"))
            arts[aid] = a
            t = (TXT / Path(a["texto"]).name).read_text(encoding="utf-8")
            textos[aid] = " " + re.sub(r"\s+", " ", t.replace("−", "-").replace("–", "-")) + " " + a.get("resumo", "")
            entradas.append((nome, aid))
        elif sa(nfc(nome)) in notas_md:
            entradas.append((nome, None))  # Protocolo ou nota de conceito: não é artigo do catálogo
        else:
            erros.append(f"notas_base: '{nome}' não existe no catálogo nem entre as notas da base (use o id exato do 'buscar')")
    if not nomes:
        erros.append("frontmatter sem notas_base: [\"[[<nota ou id do artigo>]]\", …]")
    n_prot = sum(1 for _, a in entradas if a is None)
    if n_prot:
        avisos.append(f"{n_prot} nota(s) de notas_base não são artigos do catálogo (Protocolo/conceitos): fontes que citam só elas não têm número conferido")

    def artigo_do_rotulo(rot):
        r = _nz(rot)
        for nome, aid in entradas:
            n = _nz(nome)
            if r and (n.startswith(r) or f" {r} " in f" {n} " or (aid and r in _nz(aid))):
                return nome, aid
        return None, None

    def checar(celulas_numeros, fonte, onde):
        partes = [x.strip() for x in fonte.split(";") if x.strip()]
        if not partes:
            erros.append(f"{onde}: sem fonte")
            return
        alvos, anterior = [], None
        for parte in partes:
            rot, _, loc = parte.partition(",")
            nome, aid = artigo_do_rotulo(re.sub(r"\([^)]*\)", " ", rot))  # "ESC/EAS 2025 (texto 2019)" → "ESC/EAS 2025"
            if not nome and anterior and re.match(r"(sec|tab|rec|result|sof|fig|§|p\.|\d|dados)", sa(parte)):
                (nome, aid), loc = anterior, parte  # "Hooper 2020, SoF 1; Tab. 2": mesma fonte
            if not nome:
                erros.append(f"{onde}: fonte '{rot.strip()}' não corresponde a nenhuma nota de notas_base")
                continue
            anterior = (nome, aid)
            if not aid:
                continue  # fonte = Protocolo/conceito: sem texto de artigo para conferir
            alvos.append(aid)
            mp = re.search(r"(?<![a-zç])p\.\s*(\d+)", loc)
            if mp and arts[aid].get("localizador") == "seção":
                avisos.append(f"{onde}: {aid} veio de texto sem páginas: use 'seç. <título da seção>'")
            elif mp and int(mp.group(1)) > arts[aid].get("paginas", 999):
                erros.append(f"{onde}: página {mp.group(1)} não existe em {aid} ({arts[aid]['paginas']} p.)")
            if not mp and not re.search(r"resumo|se[cç]\.|tab\.|rec\.", sa(loc)):
                avisos.append(f"{onde}: fonte sem localizador (p. N, seç. X ou 'resumo')")
        if not alvos:
            return
        for bruto, pct in re.findall(r"(?<![\w.,·])[-−–]?(\d+(?:[.,·]\d+)*)(\s*%)?", celulas_numeros):
            bruto_pt = bruto.replace("·", ".")
            n = _num_norm(bruto_pt).lstrip("-")
            if len(n.replace(".", "")) < 2 and "." not in n:
                continue  # 1 dígito: aparece em qualquer texto
            if re.fullmatch(r"\d{1,3}(\.\d{3})+", bruto_pt):  # milhar em pt (1.000, 60.716): o texto pode trazer 1,000 / 1000 / 1 000
                corpo_pad = r"[.,\s ]?".join(bruto_pt.split("."))
            else:
                corpo_pad = re.escape(n).replace(r"\.", r"[.,·]")
            pad = r"(?<![\d.,·])" + corpo_pad + r"(?![\d]|[.,·]\d)" + (r"\s*%" if pct else "")
            if not any(re.search(pad, textos.get(a, "")) for a in alvos):
                erros.append(f"{onde}: o número '{bruto}{'%' if pct else ''}' não aparece no texto de {', '.join(alvos)}")

    sec = re.split(r"(?m)^## ", texto.replace("\r\n", "\n"))
    for s_ in sec:
        titulo = sa(s_.split("\n", 1)[0])
        linhas = [l for l in s_.splitlines() if l.strip().startswith("|")]
        if titulo.startswith("afirmacoes prontas") and len(linhas) >= 3:
            cab = [sa(c.strip()) for c in linhas[0].strip().strip("|").split("|")]
            col = lambda chave: next((k for k, c in enumerate(cab) if chave in c), None)
            ci, ct, cn, cf_ = col("#"), col("afirmac"), col("numero"), col("fonte")
            for l in linhas[2:]:
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                if ci is None or ci >= len(c):
                    continue
                pega = lambda k: c[k] if k is not None and k < len(c) else ""
                checar(pega(ct) + " " + pega(cn), pega(cf_), f"#{pega(ci)}")
        elif titulo.startswith("mitos") and len(linhas) >= 3:
            cab = [sa(c.strip()) for c in linhas[0].strip().strip("|").split("|")]
            col = lambda chave: next((k for k, c in enumerate(cab) if chave in c), None)
            ce, cf_ = col("evidencia"), col("fonte")
            for k, l in enumerate(linhas[2:], 1):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                pega = lambda j: c[j] if j is not None and j < len(c) else ""
                checar(pega(ce), pega(cf_), f"M{k}")
        elif titulo.startswith("numeros de impacto"):
            k = 0
            for l in s_.splitlines():
                if re.match(r"^\s*[-*]\s+", l):
                    k += 1
                    # a fonte é a última parte "(Sobrenome Ano, seç. X; certeza alta)" com letras e ano (não "(2001–2021)"), ou fecha o
                    # item sem parênteses ("… SBC 2025, Seç. 2.1."); só contam as partes com ano
                    par = [m_ for m_ in re.finditer(r"\(([^()]*[A-Za-zÀ-ÿ]{2,}[^()]*\d{4}[^()]*)\)", l)]
                    mf = par[-1] if par else re.search(r"((?:[A-ZÀ-Ý][\wÀ-ÿ/]*\s)+\d{4}(?:,\s*[^()]*?)?)\.?\s*$", l)
                    fonte = "; ".join(x.strip() for x in mf.group(1).split(";") if re.search(r"\d{4}", x)) if mf else ""
                    corpo = l[:mf.start()] + " " + l[mf.end():] if mf else l
                    if not fonte:
                        erros.append(f"N{k}: termine o item com a fonte: (Sobrenome Ano, seç. X) ou Sobrenome Ano, seç. X")
                        continue
                    checar(corpo, fonte, f"N{k}")
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("AVISO ", a)
    print(f"\n{caminho.name}: {len(erros)} erro(s), {len(avisos)} aviso(s).")
    sys.exit(1 if erros else 0)


def panorama(_args):
    cat = carregar_catalogo()
    fora = json.loads(FORA.read_text(encoding="utf-8")) if FORA.exists() else []
    tipos = collections.Counter(c["tipo"] for c in cat)
    eixos = collections.Counter(e for c in cat for e in c["eixos"])
    origens = collections.Counter(o.split("/")[0] for c in cat for o in c.get("origens", []))
    motivos = collections.Counter(re.sub(r"duplicata de .*", "duplicata", re.sub(r"^\d+ páginas", "N páginas", f["motivo"])).split(":")[0] for f in fora)
    nuvem = collections.Counter(f["origem"].split("/")[0] for f in fora if f["motivo"] == NUVEM)
    sem_meta = sum(1 for c in cat if not c.get("doi"))
    print(f"\nBIBLIOTECA: {len(cat)} artigos · {sum(1 for c in cat if c.get('processado'))} já processados no cofre · {sem_meta} sem DOI")
    print("Tipos:   " + " · ".join(f"{k} {v}" for k, v in tipos.most_common()))
    print("Eixos:   " + " · ".join(f"{k} {v}" for k, v in eixos.most_common()))
    print("Origens: " + " · ".join(f"{k} {v}" for k, v in origens.most_common()))
    print("Fora:    " + " · ".join(f"{k} {v}" for k, v in motivos.most_common()))
    if nuvem:
        print("Só na nuvem (baixar no OneDrive e rodar catalogar): " + " · ".join(f"{k} {v}" for k, v in nuvem.most_common()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("catalogar")
    a.add_argument("--forcar", action="store_true")
    a.add_argument("--limite", type=int)
    a.add_argument("--sem-rede", action="store_true")
    a.set_defaults(f=catalogar)
    f = sub.add_parser("importar-fila")
    f.add_argument("--baixar", action="store_true")
    f.add_argument("--sem-rede", action="store_true")
    f.set_defaults(f=importar_fila)
    b = sub.add_parser("buscar")
    b.add_argument("consulta")
    b.add_argument("--eixo")
    b.add_argument("--tipo")
    b.add_argument("--desde", type=int)
    b.add_argument("--n", type=int, default=12)
    b.set_defaults(f=buscar)
    v = sub.add_parser("ver")
    v.add_argument("id")
    v.add_argument("--completo", action="store_true")
    v.set_defaults(f=ver)
    t = sub.add_parser("trecho")
    t.add_argument("id")
    t.add_argument("termo")
    t.add_argument("--n", type=int, default=5)
    t.add_argument("--janela", type=int, default=700)
    t.set_defaults(f=trecho)
    c = sub.add_parser("conferir-ficha")
    c.add_argument("ficha", help="caminho do .md ou '<Tema> - Ficha'")
    c.set_defaults(f=conferir_ficha)
    p = sub.add_parser("panorama")
    p.set_defaults(f=panorama)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
