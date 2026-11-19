"""Conversores de texto aberto (JATS/XML da Europe PMC e HTML da PMC) para texto limpo, usados por
`biblioteca.py importar-fila --baixar`. Só biblioteca padrão. Código tirado de obter_textos.py/base_lib.py
(01 - BASE CIENTÍFICA/_SISTEMA/Scripts, antigo) para que a Biblioteca não dependa mais daquela pasta."""
import html
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SoutoTreinador-base/1.0"


def limpar(txt):
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t ]+", " ", txt)
    txt = re.sub(r" *\n *", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


def baixar(url, tentativas=3, espera=1.0):
    ultimo = None
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(espera * (i + 1))
    raise ultimo


TITULO_SEMPRE = re.compile(r"(abstract|summary|resumo|recommend|recomenda|conclus|key points|pontos-chave|executive|take.?home|"
                           r"what is new|o que há de novo|funding|financiamento|conflict|competing|disclosure|conflito)", re.I)


# ---------- conversores ----------
def _txt(el, pular=("table-wrap", "fig", "xref-skip")):
    partes = []
    def rec(e):
        tag = e.tag.split("}")[-1]
        if tag in pular:
            return
        if e.text:
            partes.append(e.text)
        for c in e:
            rec(c)
            if c.tail:
                partes.append(c.tail)
    rec(el)
    return re.sub(r"\s+", " ", "".join(partes)).strip()


def _tabela(tw, out):
    label = _txt(tw.find("label")) if tw.find("label") is not None else "Tabela"
    cap = tw.find("caption")
    out.append(f"\n**{label}.** {_txt(cap) if cap is not None else ''}")
    for tr in tw.iter():
        if tr.tag.split("}")[-1] == "tr":
            cel = [_txt(c, pular=()) for c in tr if c.tag.split("}")[-1] in ("td", "th")]
            if any(cel):
                out.append("| " + " | ".join(x.replace("|", "/") for x in cel) + " |")
    foot = tw.find("table-wrap-foot")
    if foot is not None:
        out.append("_Nota da tabela:_ " + " ".join(_txt(foot, pular=()).split()[:120]))
    out.append("")


def _bloco(el, nivel, out):
    for c in el:
        tag = c.tag.split("}")[-1]
        if tag == "sec":
            t = c.find("title")
            if t is not None and _txt(t):
                out.append("\n" + "#" * min(nivel, 5) + " " + _txt(t))
            _bloco(c, nivel + 1, out)
        elif tag == "p":
            t = _txt(c)
            if t:
                out.append(t + "\n")
            for sub in c:
                st = sub.tag.split("}")[-1]
                if st == "table-wrap":
                    _tabela(sub, out)
                elif st in ("list", "boxed-text", "disp-quote"):
                    _bloco(sub, nivel, out)
        elif tag == "list":
            for li in c:
                if li.tag.split("}")[-1] == "list-item":
                    out.append("- " + _txt(li, pular=("table-wrap",)))
            out.append("")
        elif tag == "table-wrap":
            _tabela(c, out)
        elif tag == "fig":
            lab = c.find("label")
            cap = c.find("caption")
            out.append(f"[Figura] {_txt(lab) if lab is not None else ''} " + " ".join((_txt(cap, pular=()) if cap is not None else "").split()[:120]) + "\n")
        elif tag in ("boxed-text", "disp-quote", "statement", "def-list", "table-wrap-group"):
            _bloco(c, nivel, out)
        elif tag in ("title", "label", "ref-list", "ack"):
            continue


def jats_para_texto(xml_bytes):
    raiz = ET.fromstring(xml_bytes)
    out = []
    for ab in raiz.iter():
        if ab.tag.split("}")[-1] == "abstract":
            out.append("\n## Resumo")
            _bloco(ab, 3, out)
            t = _txt(ab)
            if t and len(out) < 3:
                out.append(t)
    for parte in ("body", "floats-group"):
        for b in raiz.iter():
            if b.tag.split("}")[-1] == parte:
                _bloco(b, 2, out)
    for b in raiz.iter():  # financiamento e conflitos (curto)
        tag = b.tag.split("}")[-1]
        if tag in ("fn-group", "notes", "funding-group") or (tag == "sec" and TITULO_SEMPRE.search(_txt(b.find("title")) if b.find("title") is not None else "") and b in list(raiz.iter("back"))):
            t = _txt(b, pular=())
            if re.search(r"fund|financ|conflict|compet|disclos|conflito", t, re.I):
                out.append("\n## Financiamento / conflitos (resumo)\n" + " ".join(t.split()[:150]))
    return cortar_lixo(limpar("\n".join(out)))


class _HTML(HTMLParser):
    PULAR = {"script", "style", "nav", "header", "footer", "aside", "button", "svg", "noscript", "form", "math"}
    VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
    CLASSE_PULAR = re.compile(r"ref-list|references|front-matter|author-notes|affiliation|fig-panel|related|"
                              r"permissions|copyright|license|pmc-sidebar|in-this-article|cite-this", re.I)

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.pilha, self.pular_em, self.celulas = [], [], None, None

    def handle_starttag(self, tag, attrs):
        if tag in self.VAZIOS:
            if tag == "br" and self.pular_em is None:
                self.out.append("\n")
            return
        self.pilha.append(tag)
        a = dict(attrs)
        if self.pular_em is None and (tag in self.PULAR or self.CLASSE_PULAR.search((a.get("class") or "") + " " + (a.get("id") or ""))):
            self.pular_em = len(self.pilha)
        if self.pular_em is not None:
            return
        if re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n" + "#" * max(2, int(tag[1])) + " ")
        elif tag in ("p", "div", "section"):
            self.out.append("\n")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag == "tr":
            self.celulas = []
        elif tag in ("td", "th") and self.celulas is not None:
            self.celulas.append("")
        elif tag == "caption":
            self.out.append("\n**")

    def handle_endtag(self, tag):
        if tag in self.VAZIOS or tag not in self.pilha:
            return
        pulando = self.pular_em is not None
        while self.pilha:
            t = self.pilha.pop()
            if self.pular_em is not None and len(self.pilha) < self.pular_em:
                self.pular_em = None
            if t == tag:
                break
        if pulando:
            return
        if tag == "tr" and self.celulas is not None:
            if any(c.strip() for c in self.celulas):
                self.out.append("\n| " + " | ".join(re.sub(r"\s+", " ", c).strip().replace("|", "/") for c in self.celulas) + " |")
            self.celulas = None
        elif tag == "caption":
            self.out.append("**\n")
        elif tag in ("p", "table", "h2", "h3", "h4", "h5", "h6"):
            self.out.append("\n")

    def handle_data(self, data):
        if self.pular_em is not None:
            return
        if self.celulas and "td" in self.pilha[-3:] or self.celulas and "th" in self.pilha[-3:]:
            self.celulas[-1] += data
        else:
            self.out.append(data)


def pmc_html_para_texto(html_bytes):
    h = html_bytes.decode("utf-8", errors="replace")
    ini = h.find('class="abstract')
    if ini == -1:
        ini = h.find('main-article-body')
    fim = min([i for i in (h.find('class="ref-list'), h.find('id="ref-list'), h.find("</article>")) if i != -1] or [len(h)])
    trecho = h[max(h.rfind("<", 0, ini), 0):fim] if ini != -1 else h
    p = _HTML()
    p.feed(trecho)
    return cortar_lixo(limpar("".join(p.out)))


LIXO = re.compile(r"^(#{2,6}) *(references|referências|associated data|supplementary|data availability|author information|"
                  r"contributor information|footnotes|article information|acknowledg|agradecimentos|author contributions|"
                  r"abbreviations|ethics statement|peer review)", re.I)


def cortar_lixo(texto):
    """Remove seções sem valor para a extração (referências, afiliações, material suplementar…)."""
    out, pular = [], None
    for ln in texto.splitlines():
        m = re.match(r"^(#{2,6}) ", ln)
        if m:
            nivel = len(m.group(1))
            if pular is not None and nivel <= pular:
                pular = None
            if pular is None and LIXO.match(ln):
                pular = nivel
                continue
        if pular is None:
            out.append(ln)
    return limpar("\n".join(out))
