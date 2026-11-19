"""Modelo 2 — Editorial Clean (fundo claro quadriculado, título serifado em degradê, numeral esbatido,
personagem/objeto RECORTADO que "invade" o slide). Importado por render_carrossel.py.

Slides (campos de texto):
  {"tipo":"capa","titulo":"Linha 1\\nLinha 2\\nLinha 3","sub":"texto com ~~sublinhado~~","imagem":"x.png"}
  {"tipo":"capa2","titulo":"Assim você {{destaca}}\\ntextos","sub":"(texto em caixa alta)","imagem":"x.png"}
  {"tipo":"topico","numero":"01","titulo":"Linha 1\\nLinha 2","texto":["..."],"fecho":"_itálico_ final","imagem":"x.png","imagem2":"y.png"}
  {"tipo":"resumo","titulo":"Um logotipo\\nforte|precisa passar em três testes:","itens":["...","..."],"fecho":"...","imagem":"x.png"}
  {"tipo":"cta","titulo":"Quer ajuda\\ncom o seu caso?","sub":"...","caixa":"Treino individualizado com **Jorge Souto** · <registro do marca.json> · **link na bio**"}
Marcação: **negrito**, _itálico_, ==degradê da marca==, ~~sublinhado~~, {{destaque em caixa}}. "|" separa o texto pequeno ao lado da
última linha do título.

ARTES: no Modelo 2 TODA arte é RECORTE (personagem/objeto isolado sobre o fundo quadriculado do slide, nunca cena cheia). O gerador
apaga o fundo liso (modo "borda": só o fundo ligado às bordas; o miolo do objeto fica opaco), apara a caixa no personagem e a
posiciona como elemento próprio: o texto nunca fica em cima dela (a verificação acusa) e ela "sangra" pela borda do slide.
  imagem   obrigatória em capa, capa2, topico e resumo (cta: opcional) · FUNDO BRANCO PURO no Flow (ver proporções abaixo)
  imagem2  só no topico (opcional): 2º recorte NO FLUXO do texto, entre título e fecho/texto (ex.: o logo-exemplo do slide-2)
  ("imagem" e "imagem2" são caminhos relativos ao JSON; sem "imagem" nos tipos obrigatórios entra um marcador cinza + ALERTA)
O que pedir ao Flow (sempre fundo branco puro, sem texto/logo na arte):
  capa      4:5 · plano fechado, sujeito saindo pela direita e por baixo, topo-esquerdo livre
  capa2     4:5 · busto frontal centrado, cortado na base
  topico    "lado" (padrão, coluna à direita do texto): objeto único 1:1, 4:3 ou retrato 9:16 (coluna de variações)
            "esquerda" (metade do sujeito cortada na borda esquerda, texto desloca para a direita e centraliza): 3:4
            "direita-baixo": retrato 3:4 · "centro-baixo": paisagem 4:3
  imagem2   1:1 ou 4:3 · objeto realista do tema, em fundo branco (foto realista; sem anime nem ilustração, decisão de 2026-10-14)
  resumo    3:4 ou 9:16 · sujeito alto, em pé, cortado na base (sai pelo canto inferior direito)
  cta       3:4 · mesmo personagem do resumo; só uma faixa de ~95 px da borda esquerda aparece

Posição da arte (opcional): "posicao_imagem": "lado" | "esquerda" | "direita-baixo" | "direita" | "centro-baixo" (cada tipo tem o seu
padrão e aceita só as que fazem sentido; as outras caem no padrão). Overrides finos por slide: "imagem_area": [x, y, larg, alt] (área do
slide 1080x1350 onde a arte se encaixa sem distorcer; pode passar da borda para sangrar), "ancora": "base-dir" | "base-esq" |
"base-centro" | "meio-centro" | "meio-dir" | "meio-esq" | "topo-esq" | "topo-dir" ..., "imagem2_area": [x, y, larg, alt] (relativo ao
espaço da imagem2, que ocupa o fluxo do texto), "modo_recorte": "borda" (padrão) | "tinta", "recorte": false (usa a imagem como está).
Outros: "sombra": true | "direita" | "topo" (sombra de folhagem desfocada; desligada por padrão — toda imagem vem do Flow),
"topo": px do topo do bloco de texto do topico (290), "num_x"/"num_y": põe o "#01" em posição fixa do slide.
Todo elemento visível tem data-el="Nome em português" (o editor visual lista e edita cada um).
"""
import html
import os
import re
import sys
import urllib.parse

from comum import ENCAIXE_JS, arte_posicionada

W, H = 1080, 1350
SETA = "<svg class='seta' data-el='Seta' viewBox='0 0 40 20' fill='none' stroke='currentColor' stroke-width='1.6'><path d='M2 10h34M28 3l8 7-8 7'/></svg>"

# Área [x, y, larg, alt] e âncora da arte por tipo e posição (medidas nas referências do Modelo 2; a área passa da borda do slide
# onde a arte sangra). Terceiro valor: seletor do bloco de texto que a arte não pode invadir (encolhe, mantendo a âncora).
POS = {
    "capa": {"direita-baixo": ([200, 330, 1000, 1170], "base-dir", ".txt-capa"),
             "centro-baixo": ([60, 560, 960, 850], "base-centro", ".txt-capa"),
             "esquerda": ([-80, 560, 900, 850], "base-esq", ".txt-capa")},
    "capa2": {"centro-baixo": ([100, 560, 880, 850], "base-centro", ".capb")},
    "topico": {"lado": ([640, 540, 330, 430], "meio-centro", ""),
               "esquerda": ([-90, 600, 490, 810], "base-esq", ""),
               "direita-baixo": ([720, 640, 420, 770], "base-dir", ""),
               "centro-baixo": ([60, 900, 960, 510], "base-centro", ".bt")},
    "resumo": {"direita-baixo": ([720, 650, 420, 760], "base-dir", "")},
    "cta": {"esquerda": ([-240, 620, 335, 520], "meio-dir", ""),
            "direita": ([985, 620, 335, 520], "meio-esq", "")},
}
PADRAO = {"capa": "direita-baixo", "capa2": "centro-baixo", "topico": "direita-baixo", "resumo": "direita-baixo", "cta": "esquerda"}
# Tópico: o design aprovado usa só "direita-baixo" (pessoa no canto) e "centro-baixo" (objeto largo embaixo) em 2026-10-14;
# "lado" e "esquerda" ficam só para peças antigas (o render avisa).
SINONIMO = {"direita": "direita-baixo"}  # "direita" (antigo) = canto inferior direito

# Bloco de texto do tópico por posição da arte: x, largura, tamanho do título, centralizado, largura do corpo, altura mínima do corpo,
# fim do rodapé (x1) e começo (x0, None = padrão)
TOPICO = {
    "lado": dict(x=120, w=810, tam=92, cen=False, corpo=480, minh=430, x1=885),
    "esquerda": dict(x=420, w=620, tam=68, cen=True, corpo=620, minh=0, x1=885),
    "direita-baixo": dict(x=120, w=580, tam=84, cen=False, corpo=580, minh=0, x1=870, topo=200),
    "centro-baixo": dict(x=120, w=810, tam=92, cen=False, corpo=810, minh=0, x1=885, topo=190),
    "sem": dict(x=120, w=810, tam=92, cen=False, corpo=820, minh=0, x1=885),
}


def fmt(t):
    t = html.escape(t).replace("&lt;br&gt;", "<br>")
    t = re.sub(r"(CREF\s*\d+(?:-[A-Z])?(?:/[A-Z]{2})?)", r"<span style='white-space:nowrap'>\1</span>", t)  # registro inteiro numa linha
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"==(.+?)==", r"<span class='dest'>\1</span>", t)
    t = re.sub(r"~~(.+?)~~", r"<u>\1</u>", t)
    t = re.sub(r"\{\{(.+?)\}\}", r"<span class='sel' data-el='Palavra em destaque'>\1<em class='p1' data-el='Ponto do destaque 1'></em><em class='p2' data-el='Ponto do destaque 2'></em></span>", t)
    t = re.sub(r"(?<![\w/])_(.+?)_(?!\w)", r"<i>\1</i>", t)
    return t


def _rgba(hexa, al):
    hexa = hexa.lstrip("#")
    return "rgba(%d,%d,%d,%s)" % (int(hexa[0:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16), al)


def css(M):
    """Cores do M2 lidas do marca.json: tinta (texto escuro), tinta_suave (corpo), linha (rodapé), papel (fundo), paleta e
    degradês. Os valores padrão são os do Souto Treinador."""
    pal = M.get("paleta") or {}
    P, PL, PM = pal.get("principal", "#2E49CE"), pal.get("clara", "#445DB4"), pal.get("media", "#1F33A3")
    T, TS, LN = M.get("tinta", "#141A3D"), M.get("tinta_suave", "#5A6178"), M.get("linha", "#8A90A6")
    PAPEL = M.get("papel", "#F7F8FB")
    g = M.get("gradiente_titulo", f"linear-gradient(180deg,{P} 0%,{PM} 38%,{T} 72%,#0B0B0E 100%)")
    return f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,500;1,600;1,700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:'Poppins',sans-serif;position:relative;background:{PAPEL};color:{T};-webkit-font-smoothing:antialiased;
background-image:linear-gradient({_rgba(T, .05)} 1px,transparent 1px),linear-gradient(90deg,{_rgba(T, .05)} 1px,transparent 1px);background-size:108px 108px;background-position:-2px -2px}}
.sombra{{position:absolute;z-index:1;opacity:.10;filter:blur(26px);pointer-events:none}}
.sombra.direita{{right:-120px;top:-140px;width:760px;height:760px}}
.sombra.topo{{left:0;top:-120px;width:1080px;height:700px}}
.sombra i{{position:absolute;background:{T};border-radius:50%;width:520px;height:90px;transform-origin:0 50%}}
.sombra.direita i{{left:200px;top:300px}}
.sombra.topo i{{left:540px;top:60px}}
.tit{{font-family:'DM Serif Display',serif;line-height:.98;letter-spacing:-1.5px;background:{g};-webkit-background-clip:text;background-clip:text;color:transparent;position:relative;z-index:30}}
.lado{{display:inline-block;font-family:'Poppins';font-weight:600;font-size:40px;line-height:1.05;letter-spacing:0;vertical-align:baseline;margin-left:22px;color:{T};-webkit-text-fill-color:{T};text-align:left}}
.dest{{background:{M.get('gradiente', P)};-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:700}}
b{{font-weight:700;color:{T}}} i{{font-style:italic}}
u{{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}}
.corpo{{position:relative;z-index:30;font-size:40px;line-height:1.14;color:{TS}}}
.corpo p{{margin-bottom:40px}}
.fecho{{position:relative;z-index:30;font-size:42px;line-height:1.12;font-style:italic;font-weight:600;color:{T}}}
.cen .corpo,.cen .fecho{{text-align:center}}
.num{{position:absolute;z-index:20;font-family:'DM Serif Display',serif;font-size:300px;line-height:1;background:linear-gradient(180deg,{_rgba(P, .14)},{_rgba(P, 0)} 85%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.num.no-bloco{{left:0;right:0;top:-110px;text-align:center}}
.recorte{{position:absolute;z-index:10;max-width:none;pointer-events:none}}  /* acima da linha do rodapé (z 5): a foto cobre a linha, como na referência */
.fig{{position:relative}}
.rodape{{position:absolute;bottom:62px;height:2px;background:{LN};z-index:5}}
.seta{{position:absolute;bottom:48px;width:38px;height:28px;color:{TS};z-index:5}}
.marca{{position:absolute;left:0;right:0;top:58px;text-align:center;z-index:30}}
.marca img{{height:96px;filter:invert(1) brightness(.14)}}
.caixa{{position:relative;z-index:30;border:4px dashed {T};border-radius:26px;padding:42px 48px;font-size:42px;line-height:1.18;font-style:italic;text-align:center;color:{T}}}
.caixa b{{font-style:italic;font-weight:700}}
.sel{{position:relative;display:inline-block;padding:0 18px 4px;margin:0 4px;background:{_rgba(P, .12)};border-left:3px solid {P};border-right:3px solid {P};-webkit-text-fill-color:{PM}}}
.sel em{{position:absolute;width:14px;height:14px;border-radius:50%;background:{P}}}
.sel .p1{{right:-8px;top:-10px}} .sel .p2{{left:-8px;bottom:-10px}}
.capb .sub2{{font-family:'Poppins';font-weight:500;font-size:38px;line-height:1.22;letter-spacing:.06em;text-transform:uppercase;color:{T};margin:28px auto 0;max-width:760px}}
.arraste{{display:inline-flex;align-items:stretch;margin-top:44px;border:2px solid {T};height:52px}}
.arraste span{{font-weight:700;font-size:20px;letter-spacing:.32em;padding:0 34px 0 46px;display:flex;align-items:center;color:{T}}}
.arraste b{{width:52px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,{PL},{PM});color:#fff;font-size:26px}}
.barra{{border-left:4px solid {P};padding-left:16px;font-size:44px;line-height:1.16;color:{TS}}}
.barra div{{margin-bottom:22px}}
.barra div:last-child{{margin-bottom:0}}
"""


def sombra(variante="direita"):
    v = "topo" if variante == "topo" else "direita"
    angulos = (20, 50, 80, 100, 130, 160, 10) if v == "topo" else (-160, -125, -95, -60, -30, 5, 35)
    folhas = "".join(f"<i data-el='Folha {n}' style='transform:rotate({a}deg)'></i>" for n, a in enumerate(angulos, 1))
    return f"<div class='sombra {v}' data-el='Sombra de folhagem'>{folhas}</div>"


def titulo_html(t, tam, rotulo="Título", centro=False, cabe=0):
    """cabe=px: cada linha do título fica inteira (sem quebrar) e a fonte encolhe até a linha mais longa caber nessa largura."""
    linhas = t.split("\n")
    partes = []
    for i, l in enumerate(linhas):
        if "|" in l and i == len(linhas) - 1:
            grande, peq = l.split("|", 1)
            if len(peq) > 14 and " " in peq.strip():  # quebra no espaço mais perto do meio (não depois da 1ª palavra)
                meio, esp = len(peq) / 2, [k for k, ch in enumerate(peq) if ch == " " and 0 < k < len(peq) - 1]
                k = min(esp, key=lambda e: abs(e - meio)) if esp else -1
                peq_html = fmt(peq[:k]) + "<br>" + fmt(peq[k + 1:]) if k > 0 else fmt(peq)
            else:
                peq_html = fmt(peq)
            partes.append(f"{fmt(grande)}<span class='lado' data-el='{rotulo} · texto lateral'>{peq_html}</span>")
        else:
            partes.append(fmt(l))
    al = "text-align:center;" if centro else ""
    fit = f" data-cabe='{cabe}'" if cabe else ""
    nw = "white-space:nowrap;" if cabe else ""
    return f"<div class='tit' data-el='{rotulo}'{fit} style='{al}{nw}font-size:{tam}px'>{'<br>'.join(partes)}</div>"


# Título com data-cabe: encolhe a fonte até a linha mais longa caber (roda antes do encaixe da arte).
CABE_JS = """<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){
  document.querySelectorAll('[data-cabe]').forEach(function(el){
    var max = +el.dataset.cabe, s = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > max + 1 && s > 40) { s -= 2; el.style.fontSize = s + 'px'; }
  });
});
</script>"""


def rodape(x0=150, x1=885):
    """Linha + seta do rodapé; encurta (x0/x1) quando a arte ocupa a lateral, como nas referências."""
    return (f"<div class='rodape' data-el='Linha do rodapé' style='left:{x0}px;width:{x1 - x0}px'></div>"
            + SETA.replace("<svg ", f"<svg style='left:{x1 + 30}px' ", 1))


def _arq(url):
    """file:///C:/... -> caminho local."""
    return os.path.normpath(urllib.parse.unquote(url[8:])) if url else ""


def _base(s, url_img):
    """Pasta do JSON: s["_base"] (se o render passar) ou deduzida do caminho relativo de "imagem"."""
    if s.get("_base"):
        return s["_base"]
    im = s.get("imagem")
    if url_img and im and not os.path.isabs(im):
        p, r = _arq(url_img), os.path.normpath(im)
        if p.endswith(r):
            return p[: -len(r)]
    for a in sys.argv[1:]:  # o render roda como script: o 1º argumento .json é o carrossel
        if a.lower().endswith(".json") and os.path.isfile(a):
            return os.path.dirname(os.path.abspath(a))
    return os.getcwd()


def _caixa(h):
    m = re.search(r"left:(-?\d+)px;top:(-?\d+)px;width:(\d+)px;height:(\d+)px", h or "")
    return tuple(int(v) for v in m.groups()) if m else None


def posicao(s):
    """Posição normalizada da arte (padrão do tipo se a pedida não existe para ele)."""
    tipo = s["tipo"]
    p = SINONIMO.get(s.get("posicao_imagem"), s.get("posicao_imagem"))
    if not p and tipo == "topico":
        # tópicos alternam sozinhos (2026-10-15): #01, #03, #05 = foto no canto de baixo à direita;
        # #02, #04, #06 = foto embaixo no centro. "posicao_imagem" no slide força uma delas.
        try:
            n = int(re.sub(r"\D", "", str(s.get("numero") or "")) or s.get("_n") or 1)
        except ValueError:
            n = 1
        p = "direita-baixo" if n % 2 else "centro-baixo"
    p = p or PADRAO.get(tipo, "direita-baixo")
    return p if p in POS.get(tipo, {}) else PADRAO.get(tipo, "direita-baixo")


def arte(s, url_img):
    """Arte principal recortada e posicionada. Devolve (html, caixa (x, y, larg, alt))."""
    if not url_img:
        return "", None
    tipo = s["tipo"]
    area, anc, enc = POS.get(tipo, POS["capa"])[posicao(s)]
    if s.get("imagem_area"):
        area, enc = s["imagem_area"], ""
    h = arte_posicionada(_arq(url_img), area, s.get("ancora") or anc, modo=s.get("modo_recorte", "borda"),
                         recorte=s.get("recorte", True), rotulo="Arte (recorte)", classe="recorte", encaixe=enc,
                         folga=s.get("folga", 50 if tipo == "topico" else 0),  # respiro entre o fim do texto e a foto
                         buracos=bool(s.get("recorte_buracos")))
    return h, _caixa(h)


def figura(s, url_img, largura):
    """imagem2 do tópico: recorte NO FLUXO do texto (entre título e fecho). Devolve "" sem imagem2."""
    c = s.get("imagem2")
    if not c:
        return ""
    arq = c if os.path.isabs(c) else os.path.join(_base(s, url_img), c)
    if not os.path.exists(arq):
        print(f"   AVISO: imagem2 não encontrada: {arq}")
        return ""
    area = s.get("imagem2_area") or [0, 0, largura, 300]
    img = arte_posicionada(arq, area, s.get("ancora2") or "meio-centro", modo=s.get("modo_recorte", "borda"),
                           recorte=s.get("recorte", True), rotulo="Arte 2 (recorte)", classe="recorte",
                           buracos=bool(s.get("recorte_buracos2")))
    return f"<div class='fig' data-el='Espaço da imagem 2' style='height:{area[1] + area[3]}px;margin:30px 0 0'>{img}</div>"


def sombra_do_slide(s):
    v = s.get("sombra")
    if not v:
        return ""
    if v is True:
        v = "topo" if s["tipo"] == "cta" else "direita"
    return sombra(v)


def slide(s, M, url_img, logo_url):
    tipo = s["tipo"]
    art, caixa = arte(s, url_img)
    base = sombra_do_slide(s)
    pos = posicao(s)
    if tipo == "capa":
        corpo = f"""{base}{art}<div class='txt-capa' data-el='Bloco de texto' style='position:absolute;left:66px;top:150px;width:620px;z-index:30'>{titulo_html(s.get('titulo',''), 136, cabe=620)}
<div data-el='Subtítulo' style='font-size:38px;font-weight:600;line-height:1.25;margin-top:30px;color:{M.get('tinta', '#141A3D')}'>{fmt(s.get('sub',''))}</div></div>"""
    elif tipo == "capa2":
        corpo = f"""{base}{art}<div class='capb' data-el='Bloco de texto' style='position:absolute;left:60px;right:60px;top:150px;text-align:center;z-index:30'>{titulo_html(s.get('titulo',''), 100)}
<div class='sub2' data-el='Subtítulo'>{fmt(s.get('sub',''))}</div><div class='arraste' data-el='Botão ARRASTE'><span data-el='Texto ARRASTE'>ARRASTE</span><b data-el='Seta do botão'>&rarr;</b></div></div>"""
    elif tipo == "topico":
        c = TOPICO[pos if art else "sem"]
        x1 = c["x1"]
        x0 = 150
        if pos == "esquerda" and caixa:
            x0 = max(150, caixa[0] + caixa[2] + 20)
        paras = "".join(f"<p data-el='Parágrafo {n}'>{fmt(p)}</p>" for n, p in enumerate(s.get("texto", []), 1))
        fixo = "num_x" in s or "num_y" in s
        num_t = html.escape(s.get("numero", ""))
        num = (f"<div class='num' data-el='Número (#{num_t})' style='left:{s.get('num_x', 330)}px;top:{s.get('num_y', 180)}px'>#{num_t}</div>" if fixo else "")
        num_bloco = "" if fixo else f"<div class='num no-bloco' data-el='Número (#{num_t})'>#{num_t}</div>"
        minh = f"min-height:{c['minh']}px;" if c["minh"] and paras else ""
        corpo_h = f"<div class='corpo' data-el='Texto' style='margin-top:60px;width:{c['corpo']}px;{minh}'>{paras}</div>" if paras else ""
        fig = figura(s, url_img, c["w"])
        ft = s.get("fecho", "")
        fecho = f"<div class='fecho' data-el='Fecho' style='margin-top:{10 if paras else 30}px;width:{c['w']}px'>{fmt(ft)}</div>" if ft else ""
        if not paras and not fig:
            fecho = fecho.replace("margin-top:30px", "margin-top:60px")
        corpo = f"""{base}{art}{num}<div class='bt{' cen' if c['cen'] else ''}' data-el='Bloco de texto' style='position:absolute;left:{c['x']}px;width:{c['w']}px;top:{s.get('topo', c.get('topo', 290))}px;z-index:30'>{num_bloco}{titulo_html(s.get('titulo',''), c['tam'], centro=True)}
{corpo_h}{fig}{fecho}</div>{rodape(x0, x1)}"""
    elif tipo == "resumo":
        itens = "".join(f"<div data-el='Item {n}'>{fmt(i)}</div>" for n, i in enumerate(s.get("itens", []), 1))
        corpo = f"""{base}{art}<div class='bt' data-el='Bloco de texto' style='position:absolute;left:184px;top:{s.get("topo", 230)}px;width:640px;z-index:30'>{titulo_html(s.get('titulo',''), 116)}
<div class='barra' data-el='Lista' style='margin-top:44px;width:600px'>{itens}</div>
<div class='fecho' data-el='Fecho' style='margin-top:44px;width:520px'>{fmt(s.get('fecho',''))}</div></div>{rodape(150, 870)}"""
    elif tipo == "cta":
        logo = f"<div class='marca' data-el='Logo'><img src='{logo_url}'></div>" if logo_url else ""
        corpo = f"""{base}{art}{logo}<div class='bt' data-el='Bloco de texto' style='position:absolute;left:150px;right:150px;top:360px;z-index:30;text-align:center'>{titulo_html(s.get('titulo',''), 112, cabe=780)}
<div data-el='Subtítulo' style='font-size:38px;font-weight:600;line-height:1.2;margin-top:30px'>{fmt(s.get('sub',''))}</div>
<div class='caixa' data-el='Caixa tracejada' style='margin-top:90px'>{fmt(s.get('caixa',''))}</div></div>"""
        if s.get("assinatura", True):  # nome + registro (CREF) no rodapé de todo CTA do M2
            assin = M.get("assinatura", "") + (f" · {M['registro']}" if M.get("registro") else "")
            corpo += (f"<div data-el='Assinatura' style='position:absolute;left:0;right:0;bottom:70px;text-align:center;z-index:30;"
                      f"font-size:22px;letter-spacing:.32em;color:{M.get('tinta_suave', '#5A6178')}'>{html.escape(assin)}</div>")
    else:
        corpo = base
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(M)}</style></head><body>{corpo}{CABE_JS}{ENCAIXE_JS}</body></html>"
