"""Renderiza carrosséis do Instagram (1080x1350, exporta em 2x) a partir de um JSON, usando o Chrome local.

Modelos ("modelo" no JSON): "manga-dark" (1, formato abaixo) · "editorial" (2, ver modelo_editorial.py) ·
"dossie" (3, ver modelo_dossie.py) · "cinema" (4, ver modelo_cinema.py) · "brandsdecoded" (5, ver modelo_brandsdecoded.py).
Marca: Gerador/marca.json (Souto Treinador: cores, logo, @, assinatura e registro CREF). Uma 2ª marca opcional
(ex.: um perfil novo) vai em Gerador/marcas/<nome>.json, por cima da marca.json: --marca=<nome> ou "marca" no topo do JSON.
Modelo 5 · BrandsDecoded (estilo Moderno, alternado claro/escuro): slides "capa" (foto cheia + headline caixa-alta),
"dark", "light", "grad" e "cta"; componentes em "componente" (card, tabela, stat, setas, cards), "imagem" (caixa de
imagem) e "imagem_fundo" (só dark). O render passa a cada slide do M5 o índice e o total (s["_n"], s["_total"]) para a
barra de progresso. Limites do M5 (tabela LIMITES): campos aninhados com ponto ("componente.texto", "cta.palavra"),
"texto" por bloco (máx. 2 blocos) e listas (setas, células da tabela, cartões) item a item.
Cada slide vira um HTML editável (pasta html/) e depois PNG. Todos os elementos podem ser ajustados no editor visual
(python editor.py → http://localhost:8765/editor). Slide salvo pelo editor fica marcado (data-editado) e NÃO é
sobrescrito por este script: ele só refotografa. Para gerar de novo a partir do JSON: --refazer.
Cada slide passa por uma verificação automática (sobreposição, texto sobre a arte, fora da arte, borda, fonte pequena,
distorção, limite de caracteres, arte ausente ou arquivo de arte que não existe) e os problemas saem como ALERTA no terminal
(só entregar com 0). AVISO = composição a conferir, não bloqueia (M5: conteúdo ocupando menos de 50% da área, sem imagem).
Folha de contato: python folha.py <pasta>.

Uso:
  python render_carrossel.py caminho/do/carrossel.json [--refazer] [--guias] [--slides=4,6] [--marca=<nome>]
  --guias desenha a zona aproximada do sujeito (tracejado rosa) para a revisão do layout; nunca publicar com guias.

JSON (Modelo 1 · Mangá Dark):
{
  "modelo": "manga-dark",
  "saida": "pasta de saída, relativa ao JSON (opcional; padrão: ao lado do JSON, com o nome do JSON)",
  "slides": [
    {"tipo": "capa", "imagem": "artes/slide-01.png", "tratamento": "cena", "enquadramento": "center 30%",
     "linha1": "entre exaustão e", "linha2": "procrastinação", "sub": "uma vida de ..."},
    {"tipo": "texto", "tema": "escuro|claro", "imagem": "artes/slide-02.png", "tratamento": "recorte", "fundo": "liso",
     "zona": "baixo|direita|esquerda", "coluna": "estreita|larga",
     "texto": ["parágrafo com **negrito** e ==destaque== e _itálico_", "> parágrafo centralizado"]},
    {"tipo": "lista", "tema": "escuro", "imagem": "artes/slide-04.png", "tratamento": "recorte", "fundo": "blend",
     "imagem_blend": "artes/slide-04-fundo.png", "titulo": "_Por que...?_ ==São 5 camadas==", "itens": ["...", "..."]},
    {"tipo": "cta", "antes": "Guarda para consultar depois:", "palavra": "SALVA", "depois": "e manda para quem precisa ler isso",
     "chamada": "frase-ponte com **negrito**", "imagem_blend": "artes/slide-09-fundo.png"}
  ]
}
Marcação no texto: **negrito**, ==destaque na cor da marca==, _itálico_, <br>.
Fotos: foto realista conceitual (regra do sistema: nenhum anime, nem mangá, nem 3D). O TRATAMENTO de cada slide
com arte é escolhido pelo Jorge na hora, por peça (a skill pergunta na etapa das artes):
  "tratamento": "cena"    → foto inteira cobrindo o slide, sem recorte; o sujeito fica na zona do slide e o lado do texto
                            ganha um degradê de leitura na cor do tema ("enquadramento" = posição CSS da foto, ex. "center top").
  "tratamento": "recorte" → o sujeito vem do Flow em FUNDO BRANCO puro, é recortado (modo "borda"; "tinta" no preto, só para
                            objeto luminoso; automático pelo fundo da arte, "modo_recorte" força) e se encaixa na zona pela própria
                            silhueta, sobre o "fundo": "liso" (cor do tema) · "branco" (força o tema claro) · "preto" (força o
                            escuro) · "quadriculado" (grade fina na cor do tema) · "blend" (a foto "imagem_blend" com elementos do
                            tema, desfocada atrás do recorte, com véu da cor do tema).
  Sem "tratamento": capa = cena; texto e lista = recorte sobre o fundo liso (o render dá AVISO para lembrar de perguntar).
  Zonas aproximadas (AREAS_M1): capa = embaixo do título · texto "baixo" (texto em cima), "direita" (texto à esquerda) ou
  "esquerda" (texto à direita) · lista = embaixo. Não é caixa fixa: cada silhueta ocupa a zona do seu jeito, e a arte encolhe
  se invadir o texto. JSON antigo: "posicao_imagem" "baixo|direita" = zona; "fundo" = cena.
Slides de texto em diagonal: o bloco alterna de lado sozinho (pares à esquerda; ímpares à direita, alinhado à direita) e o recorte vai embaixo do lado OPOSTO (zonas baixo-dir / baixo-esq); "lado": "esquerda|direita" força. Na foto inteira, o sujeito tem de vir do Flow do lado oposto ao texto. CTA (aprovado em 2026-10-14): metade clara com a chamada; metade escura com a foto do tema desfocada ("imagem_blend", obrigatória) e a assinatura com o registro (CREF) do marca.json.: [x, y, largura, altura], "ancora": "base-centro|base-dir|base-esq|meio-centro",
"recorte": false (usa a arte como veio), "recorte_buracos": true (tira o fundo preso dentro do sujeito: vão entre tubos,
alça, braço na cintura; só quando o objeto tem vãos, porque pode comer partes brancas e lisas, como clara de ovo).
Imagens: caminho relativo ao JSON ou absoluto.
"""
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse

sys.dont_write_bytecode = True  # sem __pycache__ no Gerador (regra de zero lixo)
sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from comum import (AJUSTE_JS, ENCAIXE_JS, LEITURA_JS, TRATAMENTO_CSS, arte_posicionada, camadas_fundo,  # noqa: E402
                   guia_zona, tema_do_fundo)

def _achar_chrome():
    """Google Chrome instalado: variável CHROME, se existir; senão os caminhos padrão do Windows (máquina toda e só do
    usuário), do macOS e do Linux. O render e o editor precisam dele para fotografar os slides. (O Microsoft Edge em modo
    headless NÃO gerou os PNGs no teste de 2026-11-19: use o Chrome.)"""
    import shutil
    if os.environ.get("CHROME") and os.path.isfile(os.environ["CHROME"]):
        return os.environ["CHROME"]
    cands = []
    for raiz in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")):
        if raiz:
            cands += [os.path.join(raiz, "Google", "Chrome", "Application", "chrome.exe"),
                      os.path.join(raiz, "Chromium", "Application", "chrome.exe")]
    cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in cands:
        if os.path.isfile(c):
            return c
    for nome in ("chrome", "google-chrome", "chromium", "chromium-browser"):
        if shutil.which(nome):
            return shutil.which(nome)
    return r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # padrão (o render avisa se não existir)


CHROME = _achar_chrome()
W, H, ESCALA = 1080, 1350, 2

SWIPE = """<svg class="swipe" data-el="Ícone arraste" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
<rect x="14" y="4" width="44" height="18" rx="9"/><path d="M38 13h12M46 9l4 4-4 4"/>
<path d="M24 46V20a4 4 0 0 1 8 0v16"/><path d="M32 30a4 4 0 0 1 8 0v6M40 32a4 4 0 0 1 8 0v8"/>
<path d="M24 40l-5-5a4 4 0 0 0-6 6l10 13c3 4 7 6 12 6h4c7 0 13-6 13-13V40"/></svg>"""
ICONES = """<div class="icones" data-el="Ícones (comentar, curtir, enviar, salvar)">
<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6"><path d="M24 6C13 6 6 13 6 22c0 5 2 9 6 12l-2 8 8-4c2 1 4 1 6 1 11 0 18-7 18-17S35 6 24 6z"/></svg>
<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6"><path d="M24 41S6 30 6 17a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 13-18 24-18 24z"/></svg>
<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6"><path d="M43 5L5 21l15 6 6 15z"/><path d="M43 5L20 27"/></svg>
<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6"><path d="M11 5h26v38L24 33 11 43z"/></svg></div>"""
GRAO = """<svg class="grao" data-el="Grão (textura)" xmlns="http://www.w3.org/2000/svg"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""

# Zonas aproximadas do sujeito no Modelo 1, medidas nas referências: [x, y, largura, altura] + âncora + bloco de texto a
# respeitar (a arte encolhe se invadir). Não é caixa fixa: o recorte se encaixa na zona pela própria silhueta, e a foto de
# cena inteira deve trazer o sujeito nessa região (é o que vai no prompt do Flow).
AREAS_M1 = {
    "baixo": ([0, 600, 1080, 750], "base-centro", ".bloco"),
    # diagonal (2026-10-14): texto de um lado em cima, foto do lado oposto embaixo, sangrando pela borda
    "baixo-dir": ([240, 560, 900, 790], "base-dir", ".bloco"),  # texto à esquerda → foto embaixo à direita
    "baixo-esq": ([-60, 560, 900, 790], "base-esq", ".bloco"),  # texto à direita → foto embaixo à esquerda
    "direita": ([540, 380, 560, 970], "base-dir", ""),
    "esquerda": ([-20, 380, 560, 970], "base-esq", ""),
    "lista": ([0, 660, 1080, 690], "base-centro", "ol"),
    "capa": ([0, 560, 1080, 940], "base-centro", ".titulo"),  # sangra 150 px por baixo: busto grande, rosto logo abaixo do subtítulo
}
LEITURA_M1 = {"baixo": "topo", "direita": "esquerda", "esquerda": "direita"}  # lado do texto → degradê de leitura


def _nome_marca(nome):
    """'@perfil_novo', 'Perfil.br' → nome do arquivo em marcas/ (None = a marca principal, Gerador/marca.json)."""
    n = str(nome or "").strip().lower().lstrip("@").split(".")[0].strip("_ ")
    return None if n in ("", "souto", "soutotreinador", "jorge", "marca") else n


def marcas_disponiveis():
    pasta = os.path.join(AQUI, "marcas")
    return sorted(os.path.splitext(f)[0] for f in os.listdir(pasta) if f.endswith(".json")) if os.path.isdir(pasta) else []


def marca(nome=None):
    """marca.json (Souto Treinador). Com o nome de uma 2ª marca, marcas/<nome>.json por cima: o que ela não define vem da
    marca principal, para nenhum modelo quebrar."""
    with open(os.path.join(AQUI, "marca.json"), encoding="utf-8") as fh:
        M = json.load(fh)
    n = _nome_marca(nome)
    if n:
        cam = os.path.join(AQUI, "marcas", n + ".json")
        if not os.path.isfile(cam):
            sys.exit(f"marca '{nome}' não existe — tire o \"marca\" do JSON (usa a marca.json) ou crie Gerador/marcas/{n}.json"
                     + (f" (existentes: {', '.join(marcas_disponiveis())})" if marcas_disponiveis() else ""))
        with open(cam, encoding="utf-8") as fh:
            M.update(json.load(fh))
    return M


def arg_marca(argv):
    """--marca=<nome> ou --marca <nome> (devolve o nome e os argumentos sem a flag)."""
    nome, resto, k = None, [], 0
    while k < len(argv):
        a = argv[k]
        if a.startswith("--marca="):
            nome = a.split("=", 1)[1]
        elif a == "--marca" and k + 1 < len(argv):
            nome, k = argv[k + 1], k + 1
        else:
            resto.append(a)
        k += 1
    return nome, resto


def sem_orfas(t):
    """Espaço inquebrável onde a quebra de linha fica feia: número + palavra curta ("1 em 263"), palavra curta + número
    e a última palavra de cada linha de texto (evita uma palavra sozinha na última linha)."""
    nb = " "
    t = re.sub(r"(?<=\d) (?=\w{1,3}\b)", nb, t)
    t = re.sub(r"(?<!\w)(\w{1,2}) (?=\d)", r"\1" + nb, t)
    return "&lt;br&gt;".join(re.sub(r" (?=\S+\s*$)", nb, parte) for parte in t.split("&lt;br&gt;"))


def fmt(t):
    t = sem_orfas(html.escape(t)).replace("&lt;br&gt;", "<br>")
    t = re.sub(r"(?<![\w-])(\w+(?:-\w+)+)", r"<span class='nq'>\1</span>", t)  # "baixá-la" não quebra no hífen
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"==(.+?)==", r"<span class='dest'>\1</span>", t)
    t = re.sub(r"(?<![\w/])_(.+?)_(?!\w)", r"<i>\1</i>", t)
    return t


def caminho(c, base):
    if not c:
        return ""
    return c if os.path.isabs(c) else os.path.join(base, c)


def img_url(c, base):
    p = caminho(c, base)  # endereço codificado: apóstrofo, espaço e acento no caminho não quebram o HTML
    return "file:///" + urllib.parse.quote(os.path.abspath(p).replace("\\", "/"), safe="/:") if p else ""


def css(M):
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,600;0,700;0,800;1,300;1,400&family=Anton&family=Montserrat:wght@300;500&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:'Poppins',sans-serif;position:relative;-webkit-font-smoothing:antialiased}}
.escuro{{background:{M['fundo_escuro']};color:#f4f4f2}}
.claro{{background:{M['fundo_claro']};color:#141414}}
.dest{{background:{M.get('gradiente', M['cor_destaque'])};-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:700}}
.escuro .dest{{background:{M.get('gradiente_escuro', M.get('gradiente', M['cor_destaque']))};-webkit-background-clip:text;background-clip:text}}
.assin{{font-family:'Montserrat',sans-serif;font-weight:300;letter-spacing:.42em;font-size:22px;text-transform:uppercase}}
.logo img.inv{{filter:invert(1) brightness(.15)}}
b{{font-weight:700}}
.grao{{position:absolute;inset:0;width:100%;height:100%;opacity:.16;mix-blend-mode:overlay;pointer-events:none;z-index:50}}
.claro .grao{{opacity:.22;mix-blend-mode:multiply}}
.swipe{{position:absolute;top:54px;right:66px;width:78px;height:78px;z-index:40}}
.escuro .swipe{{color:#f4f4f2}} .claro .swipe{{color:#141414}}
.logo{{position:absolute;top:56px;left:0;right:0;text-align:center;z-index:40;font-weight:800;font-size:40px;letter-spacing:-.5px}}
.logo img{{height:76px}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center;z-index:0}}
.vinheta{{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.25) 45%,rgba(0,0,0,.55) 100%)}}
.capa .titulo{{position:absolute;top:240px;left:70px;right:70px;text-align:center;z-index:30;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.6)}}
.capa .l1{{font-weight:700;font-size:84px;line-height:1;display:inline-block;white-space:nowrap}}
.capa .l2{{font-weight:800;font-size:128px;line-height:1.02;letter-spacing:-2px;display:inline-block;white-space:nowrap}}
.capa .sub{{font-weight:300;font-size:38px;margin-top:22px;text-wrap:balance}}
.nq{{white-space:nowrap}}
.texto .bloco p,.lista .q{{text-wrap:pretty}}
.selo{{position:absolute;right:56px;bottom:56px;z-index:40;width:74px;height:74px;background:{M.get('gradiente', M['cor_destaque'])};-webkit-mask:url('{img_url(M.get('logo'), AQUI)}') center/contain no-repeat;mask:url('{img_url(M.get('logo'), AQUI)}') center/contain no-repeat}}
.texto .bloco{{position:absolute;top:150px;left:100px;right:{M.get('margem_direita_texto', 380)}px;z-index:30;font-size:47px;line-height:1.08;font-weight:300}}
.texto .bloco.larga{{left:110px;right:150px}}
.texto .bloco.estreita-dir{{left:64px;right:540px;font-size:44px}}
.texto .bloco.estreita-esq{{left:540px;right:64px;font-size:44px}}
.claro.capa .titulo{{color:#141414;text-shadow:none}}
{TRATAMENTO_CSS}
.texto .bloco p{{margin-bottom:46px;text-align:left}}
.texto .bloco.lado-dir{{left:{M.get('margem_direita_texto', 380)}px;right:100px}}
.texto .bloco.lado-dir p{{text-align:right}}
.texto .bloco.justificado p{{text-align:justify;text-align-last:left}}
.texto .bloco p.centro{{text-align:center;text-align-last:center}}
.arte{{position:absolute;z-index:10;display:block;object-fit:contain}}
.lista .q{{position:absolute;top:90px;left:84px;right:330px;z-index:30;font-size:50px;line-height:1.1;font-weight:300}}
.lista ol{{position:absolute;top:340px;right:100px;width:500px;z-index:30;font-size:40px;line-height:1.08;text-align:right;list-style:none}}
.lista li{{margin-bottom:8px}}
.lista li .n{{margin-right:.45em}}
.cta .topo{{position:absolute;top:0;left:0;right:0;height:51%;background:{M['fundo_claro']};z-index:5}}
.cta .baixo{{position:absolute;bottom:0;left:0;right:0;height:49%;background:{M['fundo_cta']};z-index:5}}
.cta .baixo-foto{{position:absolute;bottom:0;left:0;right:0;height:49%;z-index:6;overflow:hidden}}
.cta .baixo-foto .ft{{position:absolute;inset:-50px;background-size:cover;background-position:center;filter:blur(10px) saturate(.9);transform:scale(1.05)}}
.cta .baixo-foto .vl{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,20,19,.62) 0%,rgba(26,20,19,.5) 60%,rgba(26,20,19,.7) 100%)}}
.cta .assin{{position:absolute;bottom:70px;left:0;right:0;text-align:center;z-index:30;color:#e9e3df;opacity:.85}}
.cta .logo{{top:120px;color:#141414}}
.cta .antes{{position:absolute;top:395px;left:0;right:0;text-align:center;z-index:30;font-size:38px;color:#222}}
.cta .palavra{{position:absolute;top:440px;left:0;right:0;text-align:center;z-index:30;font-family:'Anton',sans-serif;font-size:170px;line-height:1;background:{M.get('gradiente', '#151515')};-webkit-background-clip:text;background-clip:text;color:transparent}}
.cta .depois{{position:absolute;top:622px;left:0;right:0;text-align:center;z-index:30;font-size:34px;color:#222}}
.cta .icones{{position:absolute;top:790px;left:0;right:0;display:flex;justify-content:center;gap:70px;z-index:30;color:#f4f4f2}}
.cta .icones svg{{width:92px;height:92px}}
.cta .chamada{{position:absolute;top:930px;left:0;right:0;text-align:center;z-index:30;color:#f4f4f2;font-size:36px;line-height:1.3}}
"""


def logo_html(M, cor=None, inverter=False):
    if M.get("logo"):
        return f"<div class='logo' data-el='Logo'><img class='{'inv' if inverter else ''}' src='{img_url(M['logo'], AQUI)}'></div>"
    return f"<div class='logo' data-el='Logo' style='color:{cor or 'inherit'}'>{html.escape(M['nome'])}</div>"


def arte_m1(s, base, chave):
    """Sujeito recortado (modo pelo fundo da arte: borda no branco, tinta no preto) encaixado na zona `chave` do Modelo 1."""
    arq = caminho(s.get("imagem"), base)
    if not arq:
        return ""
    area, ancora, encaixe = AREAS_M1[chave]
    return arte_posicionada(arq, s.get("imagem_area") or area, s.get("ancora") or ancora, modo=s.get("modo_recorte", "auto"),
                            recorte=s.get("recorte", True), buracos=bool(s.get("recorte_buracos")),
                            encaixe=encaixe if not s.get("imagem_area") else "",
                            folga=0 if chave == "baixo" else 20 if chave == "capa" else 30)


def trat_m1(s):
    """(tratamento, fundo, tema) de um slide do Modelo 1. Sem "tratamento" no JSON: capa = cena inteira, texto e lista =
    recorte sobre o fundo liso do tema (JSON antigo: "posicao_imagem": "fundo" = cena)."""
    t = s.get("tratamento") or ("cena" if s.get("tipo") == "capa" or s.get("posicao_imagem") == "fundo" else "recorte")
    fundo = s.get("fundo") or "liso"
    tema = tema_do_fundo(fundo, s.get("tema", "escuro")) if t == "recorte" else s.get("tema", "escuro")
    return t, fundo, tema


def zona_m1(s):
    z = s.get("zona") or s.get("posicao_imagem")
    return z if z in ("baixo", "direita", "esquerda") else "baixo"


def slide_html(s, M, base):
    tipo = s["tipo"]
    trat, fundo, tema = trat_m1(s)
    claro = tema == "claro"
    cor_tema = M["fundo_claro"] if claro else M["fundo_escuro"]
    url, blend = img_url(s.get("imagem"), base), img_url(s.get("imagem_blend"), base)
    enq = s.get("enquadramento") or "center"
    guia = (lambda chave: guia_zona(s.get("imagem_area") or AREAS_M1[chave][0])) if s.get("_guias") else (lambda chave: "")
    corpo = ""
    if tipo == "capa":
        if trat == "cena":
            enq = s.get("enquadramento") or s.get("posicao_imagem") or "center"
            fundo_html = ((f"<div class='bg' data-el='Foto de fundo (cena inteira)' style=\"background-image:url('{url}');background-position:{enq}\"></div>" if url
                           else "<div class='bg' data-el='Fundo' style='background:radial-gradient(circle at 50% 70%,#2a2f33,#090a0b)'></div>")
                          + "<div class='vinheta' data-el='Vinheta (escurecimento)'></div>")
        else:
            fundo_html = (camadas_fundo("recorte", fundo, cor_tema, claro, url_blend=blend, leitura="topo", alvo=".titulo")
                          + arte_m1(s, base, "capa"))
        corpo = f"""{fundo_html}{guia('capa')}{logo_html(M, '#fff', inverter=claro)}{SWIPE}
<div class='titulo' data-el='Título'><div class='l1' data-el='Título · linha 1' data-max='940'>{fmt(s.get('linha1',''))}</div><br><div class='l2' data-el='Título · linha 2' data-max='940'>{fmt(s.get('linha2',''))}</div><div class='sub' data-el='Subtítulo'>{fmt(s.get('sub',''))}</div></div>
{"<div class='selo' data-el='Selo da marca'></div>" if M.get('selo') else ''}"""
        tema += " capa"
    elif tipo == "texto":
        z = zona_m1(s)
        coluna = {"direita": "estreita-dir", "esquerda": "estreita-esq"}.get(z, s.get("coluna", ""))
        # o texto alterna de lado a cada slide e a foto vai para o lado oposto, em diagonal (2026-10-14):
        # slides pares = texto à esquerda + foto embaixo à direita; ímpares = texto à direita + foto embaixo à esquerda.
        # "lado": "esquerda|direita" força o lado do texto. Na foto inteira (cena), o sujeito já vem do Flow do lado oposto.
        lado = s.get("lado") or ("esquerda" if int(s.get("_n") or 2) % 2 == 0 else "direita")
        if z == "baixo" and lado == "direita" and coluna in ("", "estreita"):
            coluna = (coluna + " lado-dir").strip()
        zf = ("baixo-dir" if lado == "esquerda" else "baixo-esq") if z == "baixo" else z
        paras = "".join(f"<p class='{'centro' if p.startswith('>') else ''}'>{fmt(p.lstrip('> '))}</p>" for p in s.get("texto", []))
        camadas = camadas_fundo(trat, fundo, cor_tema, claro, url_cena=url, url_blend=blend, enquadramento=enq,
                                leitura=LEITURA_M1[z], alvo=".bloco")
        corpo = (f"{camadas}{guia(zf)}{SWIPE}<div class='bloco {coluna}' data-el='Bloco de texto'>{paras}</div>"
                 + (arte_m1(s, base, zf) if trat == "recorte" else ""))
        tema += " texto"
    elif tipo == "lista":
        itens = "".join(f"<li><span class='n'>{k}.</span>{fmt(i)}</li>" for k, i in enumerate(s.get("itens", []), 1))
        camadas = camadas_fundo(trat, fundo, cor_tema, claro, url_cena=url, url_blend=blend, enquadramento=enq, leitura="topo", alvo="ol")
        corpo = (f"{camadas}{guia('lista')}{SWIPE}<div class='q' data-el='Título da lista'>{fmt(s.get('titulo',''))}</div><ol data-el='Lista'>{itens}</ol>"
                 + (arte_m1(s, base, "lista") if trat == "recorte" else ""))
        tema += " lista"
    elif tipo == "cta":
        foto_baixo = (f"<div class='baixo-foto' data-el='Foto desfocada (metade escura)'><div class='ft' data-el='Foto desfocada' "
                      f"style=\"background-image:url('{blend}')\"></div><div class='vl' data-el='Véu da foto'></div></div>") if blend else ""
        assin = M.get("assinatura", "") + (f" · {M['registro']}" if M.get("registro") else "")  # nome + CREF (CTA aprovado)
        corpo = f"""<div class='topo' data-el='Metade clara'></div><div class='baixo' data-el='Metade escura'></div>{foto_baixo}{logo_html(M, '#141414', inverter=True)}
<div class='antes' data-el='Texto antes'>{fmt(s.get('antes',''))}</div><div class='palavra' data-el='Palavra grande'>{html.escape(s.get('palavra',''))}</div><div class='depois' data-el='Texto depois'>{fmt(s.get('depois',''))}</div>
{ICONES}<div class='chamada' data-el='Chamada'>{fmt(s.get('chamada',''))}</div><div class='assin' data-el='Assinatura'>{html.escape(assin)}</div>"""
        tema = "claro cta"
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(M)}</style></head><body class='{tema}'>{corpo}{GRAO}{AJUSTE_JS}{ENCAIXE_JS}{LEITURA_JS}</body></html>"


def relativizar(doc, pasta_html):
    """Troca os endereços file:///C:/... por caminhos relativos à pasta html/, para o slide abrir igual no Chrome
    local (file://) e no editor (http://localhost)."""
    def troca(m):
        alvo = urllib.parse.unquote(m.group(1))
        try:
            rel = os.path.relpath(alvo, pasta_html).replace("\\", "/")
        except ValueError:
            return m.group(0)
        return urllib.parse.quote(rel, safe="/._-~")
    return re.sub(r"file:///([^'\")]+)", troca, doc)


def _chrome(h):
    return [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
            "--run-all-compositor-stages-before-draw",  # a foto só sai com a tela inteira pintada (sem retângulo em branco)
            f"--window-size={W},{H}", "--virtual-time-budget=6000"], "file:///" + os.path.abspath(h).replace("\\", "/")


def fotografar(h, png):
    """HTML do slide → PNG 2160x2700 no Chrome local. Devolve True se o PNG saiu."""
    args, u = _chrome(h)
    if os.path.exists(png):
        os.remove(png)
    try:
        subprocess.run(args + [f"--force-device-scale-factor={ESCALA}", f"--screenshot={png}", u], capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:  # Chrome travou (rede lenta nas fontes): o slide sai FALHOU e o render segue
        return False
    return os.path.exists(png)


def verificar(h, avisos=None):
    """Roda a verificação visual (VERIFICA_JS) no Chrome e devolve a lista de alertas, ou None se ela não rodou.
    Com uma lista em `avisos`, acrescenta nela os avisos de composição que não bloqueiam (ex.: M5 com pouco conteúdo)."""
    args, u = _chrome(h)
    try:
        dom = subprocess.run(args + ["--dump-dom", u], capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None  # vira "verificação visual não rodou" no relatório
    txt = dom.stdout.decode("utf-8", "ignore")
    m = re.search(r'data-alertas="([^"]*)"', txt)
    if not m:
        return None
    if avisos is not None:
        mv = re.search(r'data-avisos="([^"]*)"', txt)
        avisos += [a for a in html.unescape(mv.group(1)).split(" || ") if a] if mv else []
    return [a for a in html.unescape(m.group(1)).split(" || ") if a]


def editado(h):
    if not os.path.exists(h):
        return False
    with open(h, encoding="utf-8", errors="ignore") as fh:
        return "data-editado" in fh.read(3000)


def ponte_do_slide(modelo, s, base):
    """M4 (2026-10-15): o objeto do slide de busca ("imagem2") fica centrado na divisa e continua no slide
    seguinte, na mesma altura e no mesmo tamanho, sem emenda visível na troca de slide. Devolve o que o próximo slide precisa."""
    if modelo != "cinema" or s.get("tipo") != "busca" or not s.get("imagem2"):
        return None
    arq = caminho(s["imagem2"], base)
    if not arq or not os.path.isfile(arq):
        return None
    return {"arq": arq, "topo": s.get("ponte_topo", 320), "modo": s.get("modo_recorte2") or s.get("modo_recorte") or "auto",
            "buracos": bool(s.get("recorte_buracos"))}


def fotos_repetidas(C, base):
    """Regra de todos os formatos: nenhuma foto se repete no mesmo carrossel, nem em dois campos do mesmo slide.
    Devolve {nº do slide: [ALERTA]}. Vale só para as peças de verdade: os testes (pasta _testes, ou "revisao": true)
    podem repetir foto."""
    if C.get("revisao") or "_testes" in os.path.normpath(base).split(os.sep):
        return {}
    usos = {}
    for i, s in enumerate(C.get("slides", []), 1):
        for campo in CAMPOS_ARTE:
            v = s.get(campo)
            if isinstance(v, str) and v:
                usos.setdefault(os.path.normcase(os.path.abspath(caminho(v, base))), []).append((i, campo, v))
    out = {}
    for lista in usos.values():
        if len(lista) > 1:
            onde = ", ".join(f"slide {i} ({campo})" for i, campo, _ in lista)
            for i, campo, v in lista:
                out.setdefault(i, []).append(f"foto repetida no carrossel: {v} aparece em {onde} — cada foto entra uma vez só "
                                             "(regra do sistema)")
    return out


def main():
    nome_marca, argv = arg_marca(sys.argv[1:])  # --marca=<nome>: sobrescreve o "marca" do JSON
    pos = [a for a in argv if not a.startswith("--")]
    refazer = "--refazer" in sys.argv
    guias = "--guias" in sys.argv  # contorno da zona do sujeito (revisão de layout; não publicar com guias)
    # --slides=4,6: renderiza só esses (os outros PNGs ficam como estão); a ponte do M4 continua calculada
    so = {int(x) for a in sys.argv[1:] if a.startswith("--slides=") for x in a.split("=", 1)[1].split(",") if x.strip()}
    cam = os.path.abspath(pos[0])
    base = os.path.dirname(cam)
    with open(cam, encoding="utf-8") as fh:
        C = json.load(fh)
    modelo = C.get("modelo", "manga-dark")
    if modelo not in MODELOS:
        sys.exit(f"modelo '{modelo}' não existe — use um destes: {', '.join(MODELOS)}")
    if not os.path.isfile(CHROME):
        sys.exit("Chrome não encontrado. Instale o Google Chrome (https://www.google.com/chrome/) ou aponte a variável CHROME "
                 "para o chrome.exe (veja o guia docs/guias/03-carrossel.md, seção Problemas).")
    M = marca(nome_marca or C.get("marca"))
    lembrete_marca(M)
    chave = modelo
    saida = os.path.normpath(os.path.join(base, C["saida"])) if C.get("saida") else os.path.join(base, os.path.splitext(os.path.basename(cam))[0])
    os.makedirs(os.path.join(saida, "html"), exist_ok=True)
    total = total_av = 0
    repetidas = fotos_repetidas(C, base)
    ponte = None  # M4: objeto do slide de busca que continua no slide seguinte (a emenda some na troca de slide)
    for i, s in enumerate(C["slides"], 1):
        h = os.path.join(saida, "html", f"slide-{i:02d}.html")
        png = os.path.join(saida, f"slide-{i:02d}.png")
        alertas, avisos = list(repetidas.get(i, [])), []
        if so and i not in so:
            if not (editado(h) and not refazer):
                s2, _ = conferir_artes(chave, dict(s, _ponte=ponte) if ponte else s, base)
                ponte = ponte_do_slide(modelo, dict(s2, _base=base, _guias=guias, _n=i), base)
            continue
        if editado(h) and not refazer:
            print(f"   slide-{i:02d}: editado no editor — mantido como está (--refazer gera de novo a partir do JSON)")
        else:
            if ponte:
                s = dict(s, _ponte=ponte)
            s, faltas = conferir_artes(chave, s, base)
            alertas += faltas
            avisos += avisos_tratamento(modelo, s)
            s = dict(s, _base=base, _guias=guias, _n=i)  # pasta do JSON (imagem2 etc.) e nº do slide (M1: lado do texto; M5: progresso)
            ponte = ponte_do_slide(modelo, s, base)
            if modelo == "brandsdecoded":
                s = dict(s, _total=len(C["slides"]))  # barra de progresso N/total do M5
            if modelo == "editorial":
                import modelo_editorial as ME
                doc = ME.slide(s, M, img_url(s.get("imagem"), base), img_url(M.get("logo"), AQUI) if M.get("logo") else "")
            elif modelo in ("dossie", "cinema", "brandsdecoded"):
                import importlib
                doc = importlib.import_module("modelo_" + modelo).slide(s, M, base, C)
            else:
                doc = slide_html(s, M, base)
            with open(h, "w", encoding="utf-8") as fh:
                fh.write(relativizar(doc.replace("</body>", VERIFICA_JS + "</body>"), os.path.dirname(h)))
            alertas += limites(modelo, s)
            # alertas que o próprio modelo grava no HTML (ex.: M3, texto da capa que não lê nem com o degradê preto)
            alertas += [html.unescape(a) for a in re.findall(r"<meta name='alerta' content='([^']*)'>", doc)]
        foto_ok = fotografar(h, png)
        print(("OK " if foto_ok else "FALHOU ") + png)
        if not foto_ok:
            alertas.append("o PNG não saiu (o Chrome travou ou demorou demais) — renderize de novo")
        v = verificar(h, avisos)
        alertas += v if v is not None else ["verificação visual não rodou (confira o slide a olho)"]
        for a in alertas:
            print(f"   ALERTA slide-{i:02d}: {a}")
        for a in avisos:
            print(f"   AVISO slide-{i:02d}: {a}")
        total += len(alertas)
        total_av += len(avisos)
    print(f"\n{total} alerta(s). " + ("Corrija e renderize de novo antes de entregar." if total else "Layout aprovado na verificação automática — ainda confira a olho."))
    if total_av:
        print(f"{total_av} aviso(s) de composição (não bloqueiam; confira na folha de contato).")
    print(f"Editor visual: python \"{os.path.join(AQUI, 'editor.py')}\"  →  http://localhost:8765/editor")


MODELOS = ("manga-dark", "editorial", "dossie", "cinema", "brandsdecoded")


def lembrete_marca(M):
    """Lembrete (não conta como ALERTA): o @ e o CREF do marca.json ainda são os provisórios."""
    prov = [c for c in ("nome", "registro") if "000000" in str(M.get(c, "")) or str(M.get(c, "")) == "@soutotreinador"]
    if prov:
        nomes = {"nome": "o @ (\"nome\")", "registro": "o CREF (\"registro\")"}
        print(f"LEMBRETE: {' e '.join(nomes[c] for c in prov)} no Gerador/marca.json "
              f"{'ainda são provisórios' if len(prov) > 1 else 'ainda é provisório'} (TROCAR antes de publicar).")


# Espaços de arte obrigatórios por modelo/tipo e o fundo em que a arte deve ser gerada (Flow/Gemini ou Higgsfield; foto realista).
# Regra das referências: personagem/objeto sobre fundo liso = RECORTE (gerar em FUNDO BRANCO puro; preto só para objeto
# luminoso; o gerador recorta e posiciona como elemento próprio) · cenário atrás do texto = "foto" (cena cheia, sem recorte).
# "tratamento" (M1) = foto se o slide é cena inteira, branco se é recorte · "recorte-ou-cena" = branco, ou foto se "cena": true (M3).
# Recorte sobre fundo "blend" pede também "imagem_blend" (foto dos elementos do tema, que vai desfocada atrás do recorte).
# Nenhuma imagem de referência entra no layout: sem arte (campo vazio ou arquivo que não existe), o slide recebe um marcador
# cinza e sai ALERTA. Campos opcionais preenchidos (CAMPOS_ARTE) também são conferidos: arquivo ausente = marcador + ALERTA.
ARTES = {
    "manga-dark": {"capa": {"imagem": "tratamento"}, "texto": {"imagem": "tratamento"}, "lista": {"imagem": "tratamento"},
                   "cta": {"imagem_blend": "blend"}},  # CTA aprovado: foto do tema desfocada na metade escura
    "editorial": {"capa": {"imagem": "branco"}, "capa2": {"imagem": "branco"}, "topico": {"imagem": "branco"},
                  "resumo": {"imagem": "branco"}},
    "dossie": {"capa": {"imagem": "recorte-ou-cena"}, "capa2": {"imagem": "branco"}, "manchete": {"imagem": "foto"},
               "foto": {"imagem": "foto"}, "cta": {"imagem": "foto"}},
    "cinema": {"capa": {"imagem": "foto"}, "capa2": {"imagem": "branco"}, "busca": {"imagem": "branco"},  # imagem2 (objeto à direita) é opcional
               "lateral": {"imagem": "branco"}, "quadro": {"imagem": "branco"}, "vidro": {"imagem": "branco"},
               "texto": {"imagem": "branco"}},
    # M5: só a capa é obrigatória (foto cheia); "imagem" (caixa) e "imagem_fundo" dos slides internos são opcionais.
    "brandsdecoded": {"capa": {"imagem": "foto"}},
}
# Campos de arte conferidos sempre que preenchidos, e o marcador de cada um quando o arquivo não existe (padrão: "branco").
CAMPOS_ARTE = ("imagem", "imagem2", "imagem_fundo", "imagem_blend")
ARTES_OPCIONAIS = {"brandsdecoded": {"imagem": "foto", "imagem_fundo": "foto"}, "dossie": {"imagem": "foto"},
                   "cinema": {"imagem2": "branco"}}
TIPOS_COM_TRATAMENTO = {"manga-dark": ("capa", "texto", "lista")}  # formatos já revisados com o tratamento da arte por slide
# Tratamentos aprovados por função do slide no M1 (revisão slide a slide, 2026-10-14). (tratamento, fundo);
# fundo None = qualquer. Capa à parte; os slides internos (2 a 8) têm a mesma composição (texto em cima, foto embaixo) e
# claro/escuro livre por slide; o tratamento segue o tema (escuro como o slide 2 aprovado; claro como o slide 3). O CTA
# ainda está em revisão (vale qualquer tratamento).
TRAT_M1_PERMITIDOS = {
    "capa": {("recorte", "preto"), ("recorte", "branco"), ("recorte", "quadriculado"), ("recorte", "blend")},
    "interno-escuro": {("recorte", "blend"), ("cena", None)},
    "interno-claro": {("recorte", "quadriculado"), ("recorte", "blend"), ("cena", None)},
}
NOMES_TRAT = {("recorte", "preto"): "recorte no fundo preto", ("recorte", "branco"): "recorte no fundo branco",
              ("recorte", "quadriculado"): "recorte no quadriculado", ("recorte", "blend"): "recorte sobre fundo desfocado",
              ("cena", None): "foto inteira"}


# Tipos de slide que saíram na revisão do design (continuam no gerador só para peças antigas): o render avisa.
AVISOS_FORMATO = {
    ("manga-dark", "lista"): "slide de lista numerada saiu do M1 (2026-10-14: não serve para todo tema) — escreva como slide de texto",
    ("editorial", "capa"): "a capa 1 do M2 saiu (2026-10-14) — use \"tipo\": \"capa2\" (título central + foto embaixo)",
}


def avisos_dossie(s):
    """M3 (revisão de 2026-10-15): elementos gráficos só nas cores da marca, sem a capa A escura/P&B; a capa A aceita fundo
    azul da marca, preto, branco, outra cor "#RRGGBB" ou a própria foto ("foto"), com degradê preto automático."""
    out = []
    if s.get("tipo") == "capa" and (s.get("fundo") == "escuro" or s.get("pb")):
        out.append("a capa A escura/P&B saiu do M3 (2026-10-15) — use a capa A (\"fundo\": \"cor\", \"foto\", \"preto\", \"branco\" "
                   "ou \"#RRGGBB\") ou a capa B (\"tipo\": \"capa2\")")
    tipo = s.get("tipo")
    # (valores válidos, o que o modelo usa no lugar de um valor inválido); vinho/creme viram preto/branco onde a cor existe
    validos = {"capa": {"fundo": (("cor", "azul", "foto", "preto", "branco", "escuro"), "o azul da marca"),
                        "cor_titulo": (("preto", "branco"), "a cor escolhida pela foto"),
                        "fade": (("auto", "nenhum", "cima", "baixo", "ambos"), "nenhum degradê")},
               "manchete": {"fundo": (("cor", "azul", "noite", "preto", "branco"), "o azul da marca"), "cor_titulo": (("preto", "branco"), "o branco")},
               "foto": {"fade": (("normal", "forte"), "o degradê automático")},
               "cta": {"fade": (("normal", "forte"), "o degradê automático")}}.get(tipo, {})
    for campo, (ok, troca) in validos.items():
        v = s.get(campo)
        # o "escuro" da capa é aceito (peças antigas) mas não é sugerido; a capa também aceita outra cor "#RRGGBB"
        sugestao = ", ".join([o for o in ok if o != "escuro"] + (["#RRGGBB"] if (tipo, campo) == ("capa", "fundo") else []))
        if v is None or v == "":
            continue
        if not isinstance(v, str):
            out.append(f"{campo} precisa ser um texto ({sugestao}), não {json.dumps(v, ensure_ascii=False)} — usei {troca}")
            continue
        novo = {"vinho": "preto", "creme": "branco"}.get(v)
        if (tipo, campo) == ("capa", "fundo") and re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
            continue  # fundo de outra cor (liberado em 2026-10-15)
        if novo and novo in ok:
            out.append(f"{campo} '{v}' saiu do M3 (2026-10-15: só cores da marca) — usei '{novo}'; troque no JSON")
        elif v not in ok:
            out.append(f"{campo} '{v}' não existe na {tipo} do M3 (use {sugestao}) — usei {troca}")
    if tipo == "capa" and s.get("cena") and s.get("fundo") not in (None, "", "foto"):
        out.append(f"\"cena\": true usa a foto como fundo e ignora \"fundo\": {json.dumps(s.get('fundo'), ensure_ascii=False)} "
                   "— tire um dos dois")
    if tipo == "manchete" and s.get("cor_titulo") and isinstance(s.get("fundo"), str) and s["fundo"] in ("noite", "preto", "branco", "vinho", "creme"):
        out.append("cor_titulo só vale na manchete de fundo azul (\"fundo\": \"cor\"); nos outros fundos a cor do título é fixa")
    return out


def avisos_tratamento(modelo, s):
    """AVISO (não bloqueia): tipo de slide que saiu na revisão, ou slide com arte sem o tratamento (o Jorge escolhe na hora)."""
    out = [AVISOS_FORMATO[(modelo, s.get("tipo"))]] if (modelo, s.get("tipo")) in AVISOS_FORMATO else []
    if modelo == "editorial" and s.get("tipo") == "topico" and s.get("posicao_imagem") in ("lado", "esquerda"):
        out.append("posição de foto do tópico do M2 fora do aprovado (2026-10-14): use \"direita-baixo\" (pessoa) ou \"centro-baixo\" (objeto largo)")
    if modelo == "dossie":
        out += avisos_dossie(s)
    if modelo == "cinema" and s.get("tipo") == "vidro" and s.get("mistura") in ("cena", "clarear", "multiplicar"):
        out.append("cartões de vidro sobre foto inteira saíram do M4 (2026-10-15) — use a arte recortada entre os cartões ou \"tema\": \"claro\"")
    if (modelo == "cinema" and s.get("tipo") == "texto" and s.get("tema", "escuro") == "escuro" and not s.get("imagem2")
            and s.get("mistura") not in ("cena", "clarear", "multiplicar")):
        out.append("slide de texto do M4 no escuro só com a arte de cima saiu (2026-10-15) — use as duas artes (\"imagem2\" na base), "
                   "a foto inteira de fundo (\"mistura\": \"cena\") ou \"tema\": \"claro\"")
    if s.get("tipo") not in TIPOS_COM_TRATAMENTO.get(modelo, ()):
        return out
    if not s.get("tratamento"):
        t, fundo, _ = trat_m1(s)
        out.append(f"tratamento da arte não definido (usei '{t}'{'' if t == 'cena' else ' sobre fundo ' + fundo}) — pergunte ao "
                   "Jorge: cena inteira, ou recorte sobre fundo liso, branco, preto, quadriculado ou blend")
    elif s["tratamento"] not in ("cena", "recorte"):
        out.append(f"tratamento '{s['tratamento']}' desconhecido (use 'cena' ou 'recorte')")
    elif modelo == "manga-dark":
        t, fundo, tema = trat_m1(s)
        chave = "capa" if s.get("tipo") == "capa" else f"interno-{tema}"
        ok = TRAT_M1_PERMITIDOS.get(chave)
        if ok and (t, fundo) not in ok and (t, None) not in ok:
            out.append(f"tratamento fora do aprovado para o slide {chave} do M1 — use: "
                       + " ou ".join(sorted(NOMES_TRAT[x] for x in ok)))
    if modelo == "manga-dark" and s.get("tipo") == "texto" and zona_m1(s) != "baixo":
        out.append("recorte ao lado do texto saiu do M1 (2026-10-14: a coluna de texto fica estreita) — use \"zona\": \"baixo\"")
    if s.get("fundo") and s["fundo"] not in ("liso", "branco", "preto", "quadriculado", "blend"):
        out.append(f"fundo '{s['fundo']}' desconhecido (use liso, branco, preto, quadriculado ou blend)")
    return out


def conferir_artes(modelo, s, base):
    """Espaço de arte obrigatório vazio, ou qualquer campo de arte preenchido com um arquivo que não existe (o redator
    grava "artes/slide-NN.png" antes de a arte existir) → marcador cinza no lugar + ALERTA. Devolve (slide, alertas)."""
    alertas = []
    obrig = dict(ARTES.get(modelo, {}).get(s.get("tipo"), {}))
    if s.get("_ponte") and s.get("tipo") in ("lateral", "quadro"):  # a arte da esquerda é a metade da ponte do slide anterior
        obrig.pop("imagem", None)
    trat = trat_m1(s)[0] if modelo == "manga-dark" else (s.get("tratamento") or "recorte")
    if s.get("fundo") == "blend" and trat == "recorte":
        obrig["imagem_blend"] = "blend"
    for campo in dict.fromkeys(list(obrig) + [c for c in CAMPOS_ARTE if s.get(c)]):
        fundo = obrig.get(campo) or ARTES_OPCIONAIS.get(modelo, {}).get(campo) or ("blend" if campo == "imagem_blend" else "branco")
        if fundo == "recorte-ou-cena":
            fundo = "foto" if s.get("cena") or s.get("fundo") == "foto" else "branco"
        elif fundo == "tratamento":
            fundo = "foto" if trat_m1(s)[0] == "cena" else "branco"
        valor = s.get(campo)
        if not valor:
            s = dict(s, **{campo: marcador(fundo)})
            alertas.append(f"falta a arte em '{campo}' (marcador cinza no lugar) — gere no Flow/Gemini ou no Higgsfield; não entregar assim")
        elif not isinstance(valor, str) or not os.path.isfile(caminho(valor, base)):
            s = dict(s, **{campo: marcador(fundo)})
            alertas.append(f"arquivo da arte não encontrado em '{campo}': {valor} (marcador cinza no lugar) — gere a arte e "
                           f"salve nesse caminho, ou corrija o caminho no JSON")
    return s, alertas


MARCADOR_VERSAO = "v3-silhueta"


def _silhueta(d, cx, topo, base_y, larg, cor):
    """Busto genérico (cabeça + pescoço + ombros) que sangra pela base: o marcador do recorte tem forma de gente, para ninguém
    confundir a zona do sujeito com um círculo."""
    rc = larg * 0.2
    d.ellipse([cx - rc, topo, cx + rc, topo + rc * 2.3], fill=cor)
    d.rectangle([cx - rc * 0.5, topo + rc * 2.0, cx + rc * 0.5, topo + rc * 2.8], fill=cor)
    om = topo + rc * 2.55
    d.rounded_rectangle([cx - larg / 2, om, cx + larg / 2, base_y + 200], radius=int(larg * 0.28), fill=cor)


def marcador(fundo):
    """Marcador neutro no lugar da arte que ainda não existe: foto = cena inteira (cinza cheio, com o sujeito sugerido) ·
    branco/preto = silhueta de busto sobre o fundo em que o Flow deve gerar (vira recorte com forma de gente) ·
    blend = manchas de 'elementos do tema' que vão desfocadas atrás do recorte. Cache em _marcadores/ (refeito se mudar a versão)."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, PngImagePlugin
    pasta = os.path.join(AQUI, "_marcadores")
    os.makedirs(pasta, exist_ok=True)
    p = os.path.join(pasta, f"{fundo}.png")
    if os.path.exists(p):
        try:
            if Image.open(p).info.get("versao") == MARCADOR_VERSAO:
                return p
        except OSError:
            pass
    w, h = 1080, 1350
    try:
        fontes = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        f1 = ImageFont.truetype(os.path.join(fontes, "arialbd.ttf"), 50)
        f2 = ImageFont.truetype(os.path.join(fontes, "arial.ttf"), 32)
    except OSError:  # fora do Windows: fonte padrão do Pillow (o marcador é só um lugar reservado)
        f1 = f2 = ImageFont.load_default()
    if fundo == "foto":
        im = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(im)
        for y in range(h):
            v = int(78 - 46 * y / h)
            d.line([(0, y), (w, y)], fill=(v, v + 2, v + 4))
        _silhueta(d, w / 2, 520, h, 700, (38, 40, 43))
        textos, cor_tx, cy = ("FOTO INTEIRA · ARTE DO TEMA", "cena cheia, sem recorte"), (225, 225, 225), 980
    elif fundo == "blend":
        im = Image.new("RGB", (w, h), (120, 120, 120))
        d = ImageDraw.Draw(im)
        for k, (x, y, r, v) in enumerate([(160, 220, 170, 170), (820, 300, 210, 95), (430, 640, 150, 200), (930, 900, 190, 150),
                                          (180, 1080, 230, 85), (620, 1180, 160, 185), (560, 120, 120, 140), (40, 640, 140, 105)]):
            d.ellipse([x - r, y - r, x + r, y + r], fill=(v, v - 6, v - 12))
        im = im.filter(ImageFilter.GaussianBlur(6))
        d = ImageDraw.Draw(im)
        textos, cor_tx, cy = ("FUNDO · ELEMENTOS DO TEMA", "vai desfocado atrás do recorte"), (250, 250, 250), h / 2
    else:
        im = Image.new("RGB", (w, h), (255, 255, 255) if fundo == "branco" else (0, 0, 0))
        d = ImageDraw.Draw(im)
        _silhueta(d, w / 2, 300, h, 760, (150, 150, 150))
        textos, cor_tx, cy = ("RECORTE · ARTE DO TEMA", f"sujeito em fundo {'branco' if fundo == 'branco' else 'preto'}"), (245, 245, 245), 1010
    d.text((w / 2, cy - 26), textos[0], font=f1, fill=cor_tx, anchor="mm")
    d.text((w / 2, cy + 30), textos[1], font=f2, fill=cor_tx, anchor="mm")
    info = PngImagePlugin.PngInfo()
    info.add_text("versao", MARCADOR_VERSAO)
    im.save(p, pnginfo=info)
    return p


# Modelo 5 (BrandsDecoded): campo com ponto = aninhado ("componente.texto" = s["componente"]["texto"]); listas no caminho ou no
# fim são conferidas item a item ("texto" por bloco, "setas" por item, "componente.linhas" por célula, "componente.itens.titulo"
# por cartão). Cartões numerados (titulo 40 / texto 140), fonte da tabela (80) e instrução do CTA (50) não estão na SPEC: valores do gerador.
M5_MAX_BLOCOS = 2
_M5_INTERNO = {"tag": 32, "titulo": 70, "texto": 230, "setas": 110,
               "componente.texto": 200, "componente.cabecalho": 40, "componente.linhas": 40, "componente.fonte": 80,
               "componente.valor": 12, "componente.legenda": 90, "componente.itens": 110,
               "componente.itens.titulo": 40, "componente.itens.texto": 140}

# Limites de caracteres por campo (sem contar a marcação). Listas "itens"/"cartoes": por item; demais listas: soma (M5: ver limites_m5).
LIMITES = {
    "manga-dark": {"capa": {"linha1": 24, "linha2": 18, "sub": 60}, "texto": {"texto": 300}, "lista": {"titulo": 90, "itens": 40},
                   "cta": {"antes": 40, "palavra": 14, "depois": 80, "chamada": 90}},
    "editorial": {"capa": {"titulo": 45, "sub": 70}, "capa2": {"titulo": 50, "sub": 60}, "topico": {"titulo": 40, "texto": 260, "fecho": 80},
                  "resumo": {"titulo": 60, "itens": 40, "fecho": 80}, "cta": {"titulo": 45, "sub": 70, "caixa": 90}},
    "dossie": {"capa": {"topo": 16, "base": 13, "sub": 80, "tag": 28}, "capa2": {"pre": 30, "titulo_topo": 28, "titulo": 70, "tag": 34},
               "manchete": {"titulo": 130, "texto": 200}, "foto": {"texto": 330}, "cta": {"tag": 34, "titulo": 110, "caixa": 70}},
    "cinema": {"capa": {"linha1": 14, "linha2": 14, "script": 45, "caixa": 110}, "capa2": {"titulo": 30, "sub": 40, "nota": 40},
               "busca": {"texto": 230, "balao": 45, "fecho": 55}, "quadro": {"texto": 150, "rodape": 160}, "lateral": {"texto": 150, "rodape": 160}, "vidro": {"cartoes": 140},
               "texto": {"texto": 130, "nota": 130}, "janela": {"janela": 110, "texto": 130}, "pergunta": {"texto": 90}},
    "brandsdecoded": {"capa": {"headline": 120}, "dark": _M5_INTERNO, "light": _M5_INTERNO, "grad": _M5_INTERNO,
                      "cta": {"tag": 32, "ponte": 200, "titulo": 60, "cta.instrucao": 50, "cta.palavra": 16, "cta.beneficio": 90}},
}


def limpo(t):
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\*\*|==|!!|~~|\{\{|\}\}|(?<![\w/])_|_(?!\w)|\|", "", t).strip()


def _m5_valores(v, partes, idx=()):
    """Valores de um campo pontuado do M5, com o índice de cada lista atravessada no caminho."""
    if not partes:
        return [(idx, v)]
    if isinstance(v, list):
        return [r for k, x in enumerate(v, 1) for r in _m5_valores(x, partes, idx + (k,))]
    if isinstance(v, dict):
        return _m5_valores(v.get(partes[0]), partes[1:], idx)
    return []


def _m5_folhas(v, idx):
    if isinstance(v, str):
        yield idx, v
    elif isinstance(v, list):
        for k, x in enumerate(v, 1):
            yield from _m5_folhas(x, idx + (k,))


def limites_m5(s):
    """Limites do Modelo 5: caracteres sem marcação (**, *, <br>) por campo, bloco, item ou célula; no máximo 2 blocos de texto."""
    out = []
    for campo, maxc in LIMITES["brandsdecoded"].get(s.get("tipo"), {}).items():
        for idx0, v in _m5_valores(s, campo.split(".")):
            for idx, x in _m5_folhas(v, idx0):
                n = len(limpo(x).replace("*", ""))
                if n <= maxc:
                    continue
                if campo.endswith("linhas") and len(idx) == 2:
                    onde = f" linha {idx[0]}, coluna {idx[1]}"
                elif idx:
                    onde = (" bloco " if campo == "texto" else " item ") + ".".join(map(str, idx))
                else:
                    onde = ""
                out.append(f"'{campo}'{onde} com {n} caracteres (máx. {maxc}) — sintetize")
    txt = s.get("texto")
    if isinstance(txt, list) and len(txt) > M5_MAX_BLOCOS:
        out.append(f"'texto' com {len(txt)} blocos (máx. {M5_MAX_BLOCOS}) — junte ou corte")
    if s.get("imagem_fundo") and s.get("tipo") != "dark":
        out.append("'imagem_fundo' só vale em slide dark (no light, use 'imagem' para a caixa de imagem)")
    cta = s.get("cta") if isinstance(s.get("cta"), dict) else {}
    if s.get("tipo") == "cta" and cta.get("tipo", "palavra") == "palavra" and not cta.get("palavra"):
        out.append("CTA de palavra sem 'cta.palavra' (a caixa sairia vazia) — preencha ou use \"tipo\": \"salvar\"/\"consultoria\"")
    return out


def limites(modelo, s):
    if modelo == "brandsdecoded":
        return limites_m5(s)
    out = []
    for campo, maxc in LIMITES.get(modelo, {}).get(s.get("tipo"), {}).items():
        v = s.get(campo)
        if not v:
            continue
        if isinstance(v, list) and campo in ("itens", "cartoes"):
            for k, x in enumerate(v, 1):
                if len(limpo(x)) > maxc:
                    out.append(f"'{campo}' item {k} com {len(limpo(x))} caracteres (máx. {maxc}) — sintetize")
        else:
            n = len(limpo(" ".join(v) if isinstance(v, list) else v))
            if n > maxc:
                out.append(f"'{campo}' com {n} caracteres (máx. {maxc}) — sintetize")
    return out


# Roda dentro de cada slide depois do ajuste das fontes: acusa texto sobreposto entre blocos, texto sobre a arte recortada,
# fora da arte ou colado na borda, fonte pequena demais, texto/imagem esticados (distorção) e caixas de texto que não couberam.
VERIFICA_JS = r"""<script>
(function(){
function checar(){
  var W=1080,H=1350,al=[],blocos=[],cv=document.createElement('canvas').getContext('2d');
  function tinta(x,txt,cs){cv.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
    var m=cv.measureText(cs.textTransform=='uppercase'?txt.toUpperCase():txt);
    if(!m.fontBoundingBoxAscent) return {left:x.left,right:x.right,top:x.top,bottom:x.bottom};
    return {left:x.left,right:x.right,top:x.top+Math.max(0,m.fontBoundingBoxAscent-m.actualBoundingBoxAscent),bottom:x.bottom-Math.max(0,m.fontBoundingBoxDescent-m.actualBoundingBoxDescent)};}
  var tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null);
  while(tw.nextNode()){
    var n=tw.currentNode; if(!n.textContent.trim()) continue;
    var p=n.parentElement; if(!p||p.closest('svg,script,style,.num,.cab,.indice,[data-livre]')) continue;
    var cs=getComputedStyle(p); if(cs.display=='none'||cs.visibility=='hidden') continue;
    var r=document.createRange(); r.selectNodeContents(n);
    var fs=parseFloat(cs.fontSize), rs=[].slice.call(r.getClientRects()).filter(function(x){return x.width>2&&x.height>2;}).map(function(x){return tinta(x,n.textContent.trim(),cs);});
    var g=p; while(g&&g!==document.body&&getComputedStyle(g).position!=='absolute') g=g.parentElement;
    var nome=n.textContent.trim().slice(0,28);
    blocos.push({g:g,rs:rs,fs:fs,t:nome});
    if(fs<18) al.push('fonte pequena demais ('+Math.round(fs)+'px): "'+nome+'"');
    rs.forEach(function(x){
      if(x.left<-1||x.right>W+1||x.top<0||x.bottom>H) al.push('texto fora da arte: "'+nome+'"');
      else if(x.left<14||x.right>W-14||x.top<14||x.bottom>H-14) al.push('texto colado na borda: "'+nome+'"');
    });
    for(var e=p;e&&e!==document.body;e=e.parentElement){
      var t=getComputedStyle(e).transform;
      if(t&&t!=='none'){var v=t.match(/-?[\d.e]+/g).map(Number),sx=Math.hypot(v[0],v[1]),sy=Math.hypot(v[2],v[3]);
        if(Math.abs(sx-sy)>0.01){al.push('texto distorcido (escala desigual): "'+nome+'"');break;}}
    }
  }
  for(var a=0;a<blocos.length;a++) for(var b=a+1;b<blocos.length;b++){
    var A=blocos[a],B=blocos[b]; if(A.g===B.g) continue;
    var hit=A.rs.some(function(x){return B.rs.some(function(y){
        return Math.min(x.right,y.right)-Math.max(x.left,y.left)>2 && Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top)>2;});});
    if(hit) al.push('texto sobreposto: "'+A.t+'" x "'+B.t+'"');
  }
  document.querySelectorAll('[data-arte]').forEach(function(im){
    var c=getComputedStyle(im); if(c.display=='none'||c.visibility=='hidden'||+c.opacity<0.3) return;
    var q=im.getBoundingClientRect();
    blocos.forEach(function(B){ if(B.rs.some(function(x){
        return Math.min(x.right,q.right)-Math.max(x.left,q.left)>12 && Math.min(x.bottom,q.bottom)-Math.max(x.top,q.top)>12;}))
      al.push('texto sobre a arte recortada: "'+B.t+'" (afaste ou diminua a arte)'); });
  });
  document.querySelectorAll('*').forEach(function(e){
    var cs=getComputedStyle(e);
    if(cs.backgroundImage.indexOf('url(')>=0&&!/cover|contain|auto|px/.test(cs.backgroundSize)) al.push('imagem pode estar esticada ('+cs.backgroundSize+')');
    if(e.tagName=='IMG'&&e.naturalWidth){var rn=e.naturalWidth/e.naturalHeight,rr=e.clientWidth/e.clientHeight;
      if(cs.objectFit!='cover'&&cs.objectFit!='contain'&&Math.abs(rn-rr)/rn>0.02) al.push('imagem distorcida');}
    if(e.dataset&&e.dataset.fith&&e.scrollHeight>+e.dataset.fith+2) al.push('texto não coube na área: "'+e.textContent.trim().slice(0,28)+'"'+(e.dataset.dica?' — '+e.dataset.dica:''));
  });
  document.body.setAttribute('data-alertas',al.filter(function(x,i){return al.indexOf(x)===i;}).join(' || '));
  // avisos de composição (não bloqueiam): o M5 marca em data-preench quanto da área útil o conteúdo ocupa
  var av=[];
  if(!document.querySelector('.img-box,.bgimg')) document.querySelectorAll('[data-preench]').forEach(function(e){
    if(+e.dataset.preench<50) av.push('conteúdo ocupa só '+e.dataset.preench+'% da área útil: o BD sugere caixa de imagem ("imagem") ou um card');});
  document.body.setAttribute('data-avisos',av.join(' || '));
}
(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){setTimeout(checar,400);});
})();
</script>"""


if __name__ == "__main__":
    main()
