"""Modelo 3 — Dossiê (estudo de caso: manchetes condensadas em caixa-alta, foto emoldurada, fundos azul/preto/branco,
texto sobre foto). Importado por render_carrossel.py quando "modelo": "dossie".

Cores: todo elemento gráfico (texto, tarja, etiqueta, pílula, fundo liso, ícone) só com as cores da marca (2026-10-15): o azul da marca em degradê (aço, elétrico, royal e noite), branco e preto, lidos do marca.json (paleta, gradiente, fundo_escuro,
fundo_claro). Sem vinho, creme ou marrom. As fotos não precisam ficar na paleta (o tema pode pedir outras cores). Os nomes antigos "vinho" e "creme"
ainda funcionam (viram preto e branco) e o render avisa.

Cabeçalho (opcional no topo do JSON): "cabecalho": ["DOSSIÊ TREINO", "JORGE SOUTO", "<@ do marca.json>"] (padrão: profissional e @ do marca.json)

Regra das referências para as artes do Flow:
  · personagem/objeto sobre fundo liso (capa A, capa B) = RECORTE: foto realista (decisão de 2026-10-14: sem anime,
    sem ilustração) em fundo BRANCO puro (PRETO só para objeto luminoso, com "recorte_modo":"tinta"); o gerador recorta
    (comum.recortar), apara na caixa do personagem e posiciona como elemento próprio do layout;
  · cenário atrás do texto (foto, cta) ou dentro da moldura (manchete) = UMA imagem inteira, sem recorte (cena cheia).

Slides:
  {"tipo":"capa","fundo":"cor|foto|preto|branco|#RRGGBB","cor_titulo":"preto|branco (opcional)","fade":"auto|nenhum|cima|baixo|ambos",
   "imagem":"x.png","topo":"O FIM DA","base":"**FALHA**:","sub":"Linha 1\\nLinha 2\\nLinha 3","tag":"DOSSIÊ DO TREINO",
   "posicao_sub":"esquerda|direita","sub_topo":830,
   "cena":false,"imagem_area":[x,y,larg,alt],"ancora":"base-centro","recorte":true,"recorte_modo":"borda"}
     · capa A (2026-10-15: capa chamativa sem poluir; o fundo não precisa ser azul): "fundo" = "cor" (azul da
       marca, padrão), "preto", "branco" ou outra cor "#RRGGBB" que converse com a foto, sempre com o recorte; ou "foto" (a própria
       foto com o fundo dela, cena cheia; "cena":true é sinônimo), quando o cenário ajuda (ex.: o jogador no estádio).
     · leitura automática (leitura_capa; o render imprime a escolha): títulos, subtítulo e cabeçalho em preto ou branco pelo
       contraste com o que fica atrás; uma cor para os dois títulos ou, se nenhuma servir, uma por título; onde nem preto nem
       branco leem, entra o degradê preto (feedout) em cima e/ou embaixo; se nem assim ler, o render dá ALERTA (a conta usa a
       altura que o título vai ter: título curto fica gigante). "cor_titulo" força a cor dos títulos (o preto nunca ganha
       degradê preto embaixo dele); "fade" força o degradê ("nenhum" desliga). A variação escura/P&B ("fundo":"escuro", "pb":true) saiu na revisão do design
       (2026-10-15): continua aqui só para peças antigas, e o render avisa.
     · texto normal = condensada leve; **x** = condensada pesada. Cada linha (topo/base) ocupa a largura toda.
     · A arte é RECORTE por padrão ("profundidade":true continua valendo como sinônimo). Ela vira um elemento com caixa
       própria: capa azul = ~860x1075 ancorado embaixo (sangra; sobe até entrar ~17% no título), na frente do título de cima e atrás do de baixo;
       capa escura = ~1020x680 com o topo fixo (y≈470) entre os dois títulos. "imagem_area" e "ancora"
       (base|meio|topo + -esq|-centro|-dir) sobrescrevem; "recorte":false usa a arte como veio; "recorte_modo":"tinta"
       só para objeto luminoso sobre preto. Só vira foto de fundo inteira (cena cheia, atrás de tudo) com "fundo":"foto".
  {"tipo":"capa2","pre":"INVESTIGANDO A ACADEMIA:","titulo_topo":"O TREINO ATÉ A FALHA","tag":"...","imagem":"x.png",
   "titulo":"Por que o {{cansaço}}\\nparece medir\\no resultado?"}      (capa B, branco; {{x}} = tarja azul)
     · a arte é RECORTE em fundo branco puro: caixa ~700x560 no meio, fade só na base, sem multiply.
     · opcionais: "imagem_area", "ancora", "recorte", "recorte_modo" (como na capa).
  {"tipo":"manchete","fundo":"(vazio = automático)|cor|noite|branco|preto","cor_titulo":"branco|preto (só no fundo cor)",
   "titulo":"**PARTE PESADA.** parte leve",
   "imagem":"x.png","posicao_imagem":"center","proporcao":"auto|16/9|3/2|4/3","texto":"**negrito.** resto leve"}
     · foto emoldurada com proporção FIXA por slide: "auto" (padrão) escolhe 3/2 (slides 6 e 7 da referência) e cai para
       16/9 (slides 2 e 4) quando o título é longo e não sobra altura; "16/9", "3/2" ou "4/3" travam a proporção. A arte é
       cena cheia, sem recorte (cover corta laterais ou cima/baixo: peça 16:9 com o sujeito no centro). Título, moldura e texto
       ficam juntos no meio do slide; a sobra de altura vai para cima e para baixo do bloco.
     · cores (2026-10-15): sem "fundo", as manchetes se revezam sozinhas na paleta (ROTACAO_MANCHETE: azul,
       noite, branco), confortável para a vista: nunca a mesma família do slide de antes (azul e noite são da mesma família e
       não ficam colados, nem logo depois da capa azul) e os dois tons de azul se alternam. Com a capa azul e a anatomia de 9
       slides: branco, noite, branco, azul; com a capa B: azul, noite, branco, azul. Azul = título e texto brancos
       ("cor_titulo":"preto" põe o título em preto); noite = título e texto brancos; branco = título em degradê noite e texto
       preto; preto (só fixando "fundo") = título em degradê azul e texto branco. O cabeçalho acompanha o texto.
  {"tipo":"foto","imagem":"x.png","posicao_imagem":"center top","texto":["parágrafo leve","**parágrafo em negrito**"]}
  {"tipo":"cta","imagem":"x.png","posicao_imagem":"center top","tag":"Consultoria individualizada",
   "titulo":"**Quer um treino para a sua rotina?** _A dose certa_ **para o seu momento.**","caixa":"**Link na bio** · Jorge Souto, treinador · <registro do marca.json>"}
     · foto e cta: cena cheia 4:5 atrás do texto, com o ponto focal no terço de cima (o texto ocupa a metade de baixo); no cta, sem pessoa; degradê
       preto de 50% a 94% da altura, que fica mais forte sozinho quando a foto é clara atrás do texto, e cabeçalho preto ou
       branco pelo topo da foto (leitura_foto; "fade": "normal"|"forte" força o degradê).
Marcação: **negrito/pesado**, _itálico leve_, {{tarja}} (capa2), <br>.

Todo elemento visível tem data-el="Nome em português" (o editor visual lista e edita cada um). Recortes que passam por
trás/na frente do título de propósito (capa A) levam data-frente em vez de data-arte, para a verificação de "texto sobre
a arte recortada" não acusar a sobreposição intencional.
"""
import html
import os
import re

from comum import (ANCORAS, AJUSTE_JS, ENCAIXE_JS, GRAO, aparar, arte_posicionada, caminho, fracao_transparente,
                   recortar, url)

W, H = 1080, 1350
# nomes de cor que saíram com a regra das cores da marca (2026-10-15) → o equivalente da marca
CORES_ANTIGAS = {"vinho": "preto", "creme": "branco", "azul": "cor"}  # "azul" = sinônimo de "cor" (o azul da marca)
SETA = "<svg data-el='Seta' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h13M13 6l6 6-6 6'/></svg>"
GRAO_EL = GRAO.replace("<svg ", "<svg data-el='Grão (textura)' ", 1)

# degradê preto das fotos de fundo (slides de foto e cta), em (posição 0–1 na altura, opacidade): o "normal" é o da referência
# (slides 3, 5, 8, 9: de 50% a preto sólido em 94%); o "forte" sobe e escurece mais, para foto clara atrás do texto
# (o "normal" sobe junto com o texto do slide de foto, que ficou mais alto e mais estreito em 2026-10-15)
SOMBRAS = {"normal": [(.42, 0), (.64, .55), (.88, 1), (1, 1)], "forte": [(.26, 0), (.5, .62), (.72, .93), (.88, 1), (1, 1)]}
# onde fica o texto, [x0, y0, x1, y1]: no slide de foto, o bloco mais alto e estreito ("gordinho"); no cta, o título e a pílula
FAIXA_TEXTO_FOTO = {"foto": (36, 730, 740, 1220), "cta": (36, 860, 1000, 1314)}
CONTRASTE_TEXTO = 4.5  # texto leve de 40 px: pede mais contraste que o título
# fade linear só na base do recorte da capa B (a cabeça "afunda" no fundo branco)
FADE_BASE = "-webkit-mask-image:linear-gradient(180deg,#000 84%,transparent 100%);mask-image:linear-gradient(180deg,#000 84%,transparent 100%)"

# áreas [x, y, largura, altura] medidas nas referências (1080x1350)
AREA_CAPA_COR = [40, 295, 1000, 1075]    # slide-1: personagem x100–940 (840 de largura), y295–1350 (sangra embaixo); folga lateral p/ INVADE_JS
AREA_CAPA_ESCURA = [30, 470, 1020, 680]  # variação escura: jogador x35–1015, y490–1095, topo fixo entre os títulos
AREA_CAPA_B = [190, 355, 700, 560]       # capa B: cabeça+disco x215–865, y365–915


def cor_marca(v, padrao):
    """Valor de cor do JSON com os nomes antigos convertidos (vinho → preto, creme → branco)."""
    if not isinstance(v, str) or not v:  # vazio ou de outro tipo (lista, número): o padrão; o render avisa
        return padrao
    return CORES_ANTIGAS.get(v, v)


def fmt(t):
    t = html.escape(t).replace("&lt;br&gt;", "<br>")
    t = re.sub(r"(CREF\s*\d+(?:-[A-Z])?(?:/[A-Z]{2})?)", r"<span style='white-space:nowrap'>\1</span>", t)  # registro inteiro numa linha
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\{\{(.+?)\}\}", r"<span class='mk' data-el='Tarja azul'>\1</span>", t)
    t = re.sub(r"(?<![\w/])_(.+?)_(?!\w)", r"<i>\1</i>", t)
    return t


def paleta(M):
    """Cores do M3, todas da identidade da marca (marca.json): fundo azul em degradê (a 172°, como na referência), o degradê
    da marca (texto, etiqueta, tarja), o destaque, o preto e o branco."""
    p = M.get("paleta") or {}
    s, v, a = p.get("clara", "#445DB4"), p.get("principal", "#2E49CE"), p.get("media", "#1F33A3")
    azul = [(0, s), (.48, v), (1, a)]
    t = p.get("profunda", "#141A3D")
    return {"azul": css_degrade(azul), "azul_paradas": azul, "noite": css_degrade([(0, a), (1, t)]),
            "grad_escuro": f"linear-gradient(100deg,{v} 0%,{a} 50%,{t} 100%)",  # título sobre o branco (a ponta clara lia pouco)
            "grad": M.get("gradiente") or f"linear-gradient(100deg,{s} 0%,{v} 48%,{a} 100%)",
            "grad_texto_escuro": M.get("gradiente_escuro") or M.get("gradiente") or f"linear-gradient(100deg,{s} 0%,{v} 48%,{a} 100%)",
            "destaque": M.get("cor_destaque") or v, "preto": M.get("fundo_escuro") or "#0B0B0E",
            "branco": M.get("fundo_claro") or "#F2F4F8"}


def css(K):
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Antonio:wght@500;600;700&family=Inter+Tight:ital,wght@0,300;0,400;0,500;0,600;0,800;1,300;1,400&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:'Inter Tight',sans-serif;position:relative;-webkit-font-smoothing:antialiased;background:{K['preto']};color:{K['branco']}}}
.grao{{position:absolute;inset:0;width:100%;height:100%;z-index:90;opacity:.10;mix-blend-mode:overlay;pointer-events:none}}
.cab{{position:absolute;top:26px;left:36px;right:36px;height:16px;z-index:80;font:600 12px/16px 'Inter Tight';letter-spacing:.01em;text-transform:uppercase}}
.cab span{{position:absolute;top:0}} .cab .c1{{left:0}} .cab .c2{{left:64%}} .cab .c3{{right:0}}
.cor{{background:{K['azul']}}} .noite{{background:{K['noite']}}} .preto{{background:{K['preto']}}} .branco{{background:{K['branco']}}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center;z-index:1}}
.fade{{position:absolute;inset:0;pointer-events:none}}
.pb{{filter:grayscale(1) contrast(1.08) brightness(.92)}}
/* capa */
.cond{{display:inline-block;white-space:nowrap;padding-top:.13em;font-family:'Antonio';font-weight:600;line-height:.8;letter-spacing:-.01em;text-transform:uppercase}}
.cond b{{font-family:'Anton';font-weight:400;letter-spacing:0}}
.linha{{position:absolute;left:34px;right:34px;text-align:center}}
.topo{{top:34px;z-index:2}} .base{{bottom:26px;z-index:4}}
.recorte{{position:absolute;z-index:3;max-width:none}}
.tx-preto{{color:{K['preto']}}} .tx-branco{{color:{K['branco']}}}
.tx-azul{{background:{K['grad_texto_escuro']};-webkit-background-clip:text;background-clip:text;color:transparent}}
.tx-noite{{background:{K['grad_escuro']};-webkit-background-clip:text;background-clip:text;color:transparent}}
/* texto em degradê só aparece dentro da caixa do elemento: com line-height .8 a base das letras do Antonio passava da
   caixa e sumia (o "L" perdia o pé na capa escura); folga embaixo, compensada na margem */
.cond.tx-azul{{padding-bottom:.3em;margin-bottom:-.3em}}
.sub{{position:absolute;z-index:5;width:440px}}
.sub span{{display:inline-block;font-weight:800;font-size:35px;line-height:1.12;letter-spacing:-.025em;border-bottom:2px solid currentColor;padding-bottom:3px;margin-bottom:7px}}
.tag{{display:inline-block;margin-top:24px;padding:7px 15px 6px;font:500 21px/1 'Inter Tight';text-transform:uppercase;letter-spacing:.01em;color:{K['branco']}}}
.tag.t-azul{{background:{K['grad']}}} .tag.t-preto{{background:{K['preto']}}}
/* capa B */
.topo-b{{position:absolute;left:60px;right:60px;top:150px;text-align:center;z-index:5}}
.pre{{font-family:'Antonio';font-weight:600;font-size:60px;line-height:1;text-transform:uppercase;letter-spacing:-.01em;color:{K['preto']}}}
.pre b{{font-family:'Anton';font-weight:400;display:block;font-size:64px;margin-top:20px}} /* respiro: a cedilha de cima batia no acento de baixo */
.pilula{{display:inline-block;margin-top:24px;border:2px solid {K['destaque']};border-radius:999px;padding:11px 28px;font:600 19px/1 'Inter Tight';text-transform:uppercase;color:{K['destaque']}}}
.arte-b{{position:absolute;z-index:2;max-width:none}}
.tit-b{{position:absolute;left:40px;right:40px;bottom:105px;text-align:center;z-index:5;font-weight:400;font-size:94px;line-height:1.02;letter-spacing:-.055em;color:{K['preto']}}}
.tit-b .ln{{display:inline-block;border-bottom:3px solid {K['preto']};padding:0 8px 2px;margin-bottom:8px}}
.mk{{display:inline-block;position:relative;z-index:6;padding:0 16px 6px;margin:0 2px;color:{K['branco']};background:{K['grad']};transform:rotate(-2.2deg) translateY(-8px);letter-spacing:-.05em}}
/* manchete: título, moldura de proporção fixa e texto juntos no meio do slide (2026-10-15: título e texto
   perto da foto); a sobra de altura vai para cima e para baixo do bloco, com o bloco ~40 px acima do centro (mais embaixo do que
   em cima no padding) */
.mold{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:34px;padding:60px 36px 110px;z-index:5}}
.mt{{flex:none;padding-top:.1em;font-family:'Antonio';font-weight:600;font-size:84px;line-height:.9;letter-spacing:-.005em;text-transform:uppercase}}
.mt b{{font-family:'Anton';font-weight:400}}
.ft{{flex:none;width:100%;aspect-ratio:16/9;border-radius:9px;background-size:cover;background-position:center}}
.tx{{flex:none;font-weight:400;font-size:38px;line-height:1.14;letter-spacing:-.032em}} .tx b{{font-weight:800;letter-spacing:-.028em}}
/* foto e cta */
.sombra{{position:absolute;inset:0;z-index:2;background:{sombra_css('normal')}}}
.bloco{{position:absolute;left:36px;right:150px;bottom:64px;z-index:5;color:{K['branco']}}}
/* slide de foto: texto mais alto e linha mais curta, bloco "gordinho" (2026-10-15) */
.bloco.b-foto{{right:340px;bottom:130px}}
.bloco p{{font-weight:300;font-size:40px;line-height:1.2;letter-spacing:-.035em;margin-top:46px}} .bloco p b{{font-weight:800;letter-spacing:-.03em}}
.circ{{width:46px;height:46px;border-radius:50%;background:{K['grad']};color:{K['branco']};display:flex;align-items:center;justify-content:center;margin-bottom:12px}}
.circ svg{{width:26px;height:26px}}
.cta-t{{font-weight:800;font-size:70px;line-height:1.0;letter-spacing:-.038em;margin-top:30px}} .cta-t i{{font-weight:300;font-style:italic}} .cta-t b{{font-weight:800}}
.cta-tag{{display:inline-block;border-radius:999px;padding:12px 26px;font:500 25px/1 'Inter Tight';text-transform:uppercase;background:{K['grad']};color:{K['branco']}}}
.caixa{{position:absolute;left:36px;right:46px;bottom:36px;z-index:5;border:3px solid {K['branco']};border-radius:999px;padding:15px 30px;text-align:center;font-size:30px;letter-spacing:-.03em;color:{K['branco']}}}
.caixa b{{font-weight:800}}
"""


NOMES_CAB = ["esquerda", "centro", "direita"]


def cabecalho(C, cor, M=None):
    """cor = uma cor para os 3 textos, ou uma lista com a cor de cada um (foto com topo misto: madeira escura e pão claro)."""
    c = C.get("cabecalho") or ["DOSSIÊ TREINO", (M or {}).get("profissional", "").upper(), (M or {}).get("nome", "").upper()]
    cores = cor if isinstance(cor, (list, tuple)) else [None] * 3
    spans = "".join(f"<span class='c{i}' data-el='Cabeçalho · {NOMES_CAB[i - 1]}'"
                    f"{f' style={chr(39)}color:{cores[i - 1]}{chr(39)}' if cores[i - 1] else ''}>{html.escape(t)}</span>"
                    for i, t in enumerate(c[:3], 1))
    base = cor if isinstance(cor, str) else cores[0]
    return f"<div class='cab' data-el='Cabeçalho' style='color:{base}'>{spans}</div>"


def proporcao(v):
    """'16/9', '16:9', '3/2'… → valor CSS de aspect-ratio. Vazio, "auto" ou algo estranho → None (o JS escolhe 3/2 ou 16/9)."""
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*[/:x]\s*(\d+(?:\.\d+)?)\s*", str(v or ""))
    return f"{m.group(1)}/{m.group(2)}" if m else None


# Proporção automática da moldura da manchete: 3/2 se couber (título curto), senão 16/9. Roda depois do AJUSTE_JS (fontes já
# ajustadas) e tira o data-prop-auto, então o valor escolhido fica gravado no HTML (o editor não recalcula por cima).
PROP_JS = """<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){
  document.querySelectorAll('[data-prop-auto]').forEach(function(ft){
    var col = ft.parentElement, cs = getComputedStyle(col), gap = parseFloat(cs.rowGap) || 0, outros = 0;
    [].slice.call(col.children).forEach(function(c){ if (c !== ft) outros += c.getBoundingClientRect().height; });
    var livre = col.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom) - outros - 2 * gap;
    var prop = ft.getBoundingClientRect().width * 2 / 3 <= livre ? '3/2' : '16/9';
    ft.style.aspectRatio = prop; ft.setAttribute('data-proporcao', prop); ft.removeAttribute('data-prop-auto');
  });
});
</script>"""


# Capa A (azul): o recorte cresce para cima, mantendo a base (sangra embaixo) e a âncora, até invadir ~17% da altura do título de
# cima, como na referência (saco sobre "LUCRO"). Só cresce (nunca abaixo da área medida), só com a área padrão (sem imagem_area/ancora
# no slide) e tira o data-invade depois de aplicar, então o valor fica gravado no HTML (o editor não recalcula por cima).
INVADE_JS = """<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){
  document.querySelectorAll('[data-invade]').forEach(function(im){
    function ajusta(){
      var alvo = document.querySelector(im.dataset.invade), a = (im.dataset.area || '').split(',').map(Number);
      im.removeAttribute('data-invade');
      if (!alvo || a.length < 4 || !im.naturalWidth) return;
      var r = alvo.getBoundingClientRect(), fundo = a[1] + a[3], topo = Math.max(150, r.bottom - 0.17 * r.height), ah = fundo - topo;
      if (ah <= a[3]) return;
      var k = Math.min(a[2] / im.naturalWidth, ah / im.naturalHeight), w = im.naturalWidth * k, h = im.naturalHeight * k;
      im.style.width = w + 'px'; im.style.height = h + 'px'; im.style.left = (a[0] + (a[2] - w) / 2) + 'px'; im.style.top = (fundo - h) + 'px';
    }
    if (im.complete) ajusta(); else im.addEventListener('load', ajusta);
  });
});
</script>"""


def alerta_recorte(arq, modo, onde, buracos=False):
    """Recorte suspeito: quase nada transparente (o fundo não saiu), quase nada opaco (o recorte comeu o personagem) ou
    muito furado dentro da própria caixa. Marcadores do gerador não contam. Por ora imprime no terminal; o
    render_carrossel pode drenar uma lista ALERTAS se preferir."""
    if not arq or "_marcadores" in arq.replace("\\", "/"):
        return
    try:
        rec = recortar(arq, modo=modo, buracos=buracos)
        f = fracao_transparente(rec)
        f_caixa = fracao_transparente(aparar(rec))
    except Exception as e:  # noqa: BLE001
        print(f"   ALERTA {onde}: não consegui conferir o recorte ({e})")
        return
    if f < 0.05:
        print(f"   ALERTA {onde}: recorte suspeito ({f:.0%} transparente) — o fundo não saiu; gere a arte em fundo branco ou preto puro")
    elif 1 - f < 0.04:
        print(f"   ALERTA {onde}: recorte suspeito (só {1 - f:.0%} opaco) — o recorte comeu o personagem")
    elif f_caixa > 0.60:
        print(f"   ALERTA {onde}: recorte suspeito ({f_caixa:.0%} da caixa do personagem está transparente) — o recorte pode estar furado")


def arte_recorte(s, arq, area, ancora, rotulo, classe, **kw):
    """<img> do recorte (caixa justa no personagem, encaixado na área, sem distorcer). Overrides do slide: imagem_area, ancora,
    recorte (false = arte como veio), recorte_modo (borda|tinta)."""
    modo = s.get("recorte_modo", "borda")
    usar = s.get("recorte", True)
    if usar:
        alerta_recorte(arq, modo, rotulo, buracos=bool(s.get("recorte_buracos")))
    return arte_posicionada(arq, s.get("imagem_area") or area, ancora=s.get("ancora") or ancora, modo=modo,
                            recorte=usar, rotulo=rotulo, classe=classe, buracos=bool(s.get("recorte_buracos")), **kw)


# Capa A: o contraste mínimo no pior 10% dos pontos atrás do texto. Abaixo dele, com "fade": "auto", entra o degradê preto
# (feedout) do lado que falhou; se nem assim ler, o render dá ALERTA.
FAIXA_CAB = (20, 48)
CONTRASTE_MIN = 2.5
# degradês pretos de leitura da capa A: (posição 0–1 na altura, opacidade)
FADES = {"cima": [(0, .8), (.13, .55), (.3, 0)], "baixo": [(.45, 0), (.68, .55), (1, .88)]}
FADES_PEDIDOS = {"nenhum": set(), "cima": {"cima"}, "baixo": {"baixo"}, "ambos": {"cima", "baixo"}}
# títulos da capa A: o data-fitw faz cada linha ocupar a largura toda, então a altura depende do texto ("SAL" fica gigante).
# Largura média de cada letra em em (Antonio 600 no leve, Anton no **pesado**), medida no Chrome: "O COLESTEROL" = 218 px,
# "DIETA" = 557 px, "SAL" = 700 px de fonte.
LARG_TITULO = W - 68
EM_LETRA = {False: (.40, .20, .55), True: (.47, .24, .62)}  # (letra comum, estreita, larga)


def _luminancia(rgb):
    import numpy as np
    c = np.asarray(rgb, float) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return c @ np.array([0.2126, 0.7152, 0.0722])


def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def _int(v, padrao):
    try:
        return int(round(float(v)))
    except (TypeError, ValueError):
        return padrao


def _centro(pos):
    """background-position do CSS → centering do ImageOps.fit (0 = esquerda/topo, .5 = centro, 1 = direita/base)."""
    x = y = None
    for i, t in enumerate(str(pos or "center").lower().split()[:2]):
        if t in ("top", "bottom"):
            y = 0.0 if t == "top" else 1.0
        elif t in ("left", "right"):
            x = 0.0 if t == "left" else 1.0
        elif t.endswith("%"):
            try:
                v = min(1.0, max(0.0, float(t[:-1]) / 100))
            except ValueError:
                continue
            if i == 0 and x is None:
                x = v
            else:
                y = v
    return (.5 if x is None else x, .5 if y is None else y)


def foto_cheia(arq, pos):
    """A foto como o CSS a mostra de fundo (cover + background-position), em array W x H."""
    import numpy as np
    from PIL import Image, ImageOps
    return np.asarray(ImageOps.fit(Image.open(arq).convert("RGB"), (W, H), centering=_centro(pos)), float)


def faixa_titulo(texto, cima):
    """[y0, y1] estimado do título de cima (topo 34) ou de baixo (base 1324), pela largura do texto."""
    em = 0.0
    for parte in re.split(r"(\*\*.+?\*\*)", str(texto or "").replace("<br>", " ")):
        pesado = parte.startswith("**")
        comum_, estreita, larga = EM_LETRA[pesado]
        for ch in parte.strip("*").upper():
            em += (.2 if ch == " " else estreita if ch in "IÍÌÎÏJ1!.,:;'|" else larga if ch in "MWÆ" else comum_)
    alt = LARG_TITULO / max(em, .4) * .93  # line-height .8 + padding-top .13em
    return (34, min(H, round(34 + alt))) if cima else (max(0, round(1324 - alt)), 1324)


def css_degrade(paradas):
    return "linear-gradient(172deg," + ",".join(f"{c} {round(p * 100)}%" for p, c in paradas) + ")"


def paradas_fundo(s, K):
    """Degradê vertical [(posição, "#hex")] do fundo liso da capa A: o azul da marca (padrão), preto, branco ou outra cor
    "#RRGGBB" (liberado em 2026-10-15, quando a cor conversa com a foto). None = a própria foto é o fundo."""
    f = cor_marca(s.get("fundo"), "cor")
    if f == "foto" or s.get("cena"):
        return None
    if f in ("preto", "branco"):
        return [(0, K[f]), (1, K[f])]
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", f):
        return [(0, f.upper()), (1, "#%02X%02X%02X" % tuple(round(c * .72) for c in _rgb(f)))]
    return K["azul_paradas"]


def _fade_css(lado, K):
    r, g, b = _rgb(K["preto"])
    return "linear-gradient(180deg," + ",".join(f"rgba({r},{g},{b},{a}) {round(p * 100)}%" for p, a in FADES[lado]) + ")"


def leitura_capa(s, K, arq, paradas, caixa_sub, forcada=""):
    """Legibilidade da capa A (2026-10-15: o fundo pode ser azul, outra cor ou a própria foto, desde que o
    texto se leia; degradê preto quando precisar). Monta uma prévia aproximada do que fica atrás do texto (fundo + recorte onde
    o layout o põe, ou a foto inteira na posição do CSS), com os títulos na altura que o texto vai ter, escolhe preto ou branco
    para os títulos (forcada = "cor_titulo"), o subtítulo e o cabeçalho pelo pior contraste (10º percentil) e, com "fade":
    "auto" (padrão), liga o degradê preto do lado em que a cor escolhida não passa de CONTRASTE_MIN. caixa_sub None = sem
    subtítulo nem etiqueta. Devolve {"cima", "baixo", "sub", "cab", "fades", "contraste", "alertas"}."""
    import numpy as np
    from PIL import Image
    ys = np.linspace(0, 1, H)

    def perfil(pontos):
        return np.interp(ys, [p for p, _ in pontos], [v for _, v in pontos])

    faixas = {"cima": faixa_titulo(s.get("topo"), True), "baixo": faixa_titulo(s.get("base"), False)}
    preto = np.array(_rgb(K["preto"]), float)
    tem_arte = bool(arq) and os.path.isfile(arq)
    rec_rgb = rec_a = None
    if paradas is None:  # a foto é o fundo: o texto fica sobre ela em todo lugar (sem foto, o body preto)
        base = foto_cheia(arq, s.get("posicao_imagem")) if tem_arte else np.tile(preto, (H, W, 1))
    else:
        linha = np.stack([perfil([(p, _rgb(c)[i]) for p, c in paradas]) for i in range(3)], axis=1)
        base = np.repeat(linha[:, None, :], W, axis=1)
        if tem_arte:  # o recorte como o arte_posicionada e o INVADE_JS o põem
            usar = s.get("recorte", True)
            rec = Image.open(aparar(recortar(arq, modo=s.get("recorte_modo", "borda"), buracos=bool(s.get("recorte_buracos"))))
                             if usar else arq).convert("RGBA")
            x, y, aw, ah = s.get("imagem_area") or AREA_CAPA_COR
            anc = ANCORAS.get(s.get("ancora") or "base-centro", s.get("ancora") or "base-centro")
            if usar and not s.get("imagem_area") and not s.get("ancora"):  # cresce até entrar ~17% no título de cima
                c0, c1 = faixas["cima"]
                topo = max(150, c1 - .17 * (c1 - c0))
                ah, y = max(ah, y + ah - topo), min(y, topo)
            k = min(aw / rec.width, ah / rec.height)
            rec = rec.resize((max(1, round(rec.width * k)), max(1, round(rec.height * k))))
            left = x if "esq" in anc else x + aw - rec.width if "dir" in anc else x + (aw - rec.width) / 2
            top = y if "topo" in anc else y + (ah - rec.height) / 2 if "meio" in anc else y + ah - rec.height
            camada = Image.new("RGBA", (W, H))
            camada.paste(rec, (round(left), round(top)))
            a = np.asarray(camada, float)
            rec_rgb, rec_a = a[..., :3], a[..., 3:] / 255
    lb, lp = _luminancia(_rgb(K["branco"])), _luminancia(_rgb(K["preto"]))

    def compor(fades):
        f = base
        if "cima" in fades:  # atrás do recorte
            a = perfil(FADES["cima"])[:, None, None]
            f = f * (1 - a) + preto * a
        if rec_a is not None:
            f = f * (1 - rec_a) + rec_rgb * rec_a
        if "baixo" in fades:  # na frente do recorte
            a = perfil(FADES["baixo"])[:, None, None]
            f = f * (1 - a) + preto * a
        return f

    def pior(lum):  # contraste (branco, preto) no pior 10% dos pontos; sem ponto visível, qualquer cor serve
        if not lum.size:
            return 99.0, 99.0
        return float(np.percentile((lb + .05) / (lum + .05), 10)), float(np.percentile((lum + .05) / (lp + .05), 10))

    def medir(f):
        (c0, c1), (b0, b1), (h0, h1) = faixas["cima"], faixas["baixo"], FAIXA_CAB
        cima = _luminancia(f[c0:c1, 34:W - 34])
        if rec_a is not None:  # o título de cima só aparece onde o recorte não passa na frente
            cima = cima[rec_a[c0:c1, 34:W - 34, 0] < .5]
        m = {"cima": cima.ravel(), "baixo": _luminancia(f[b0:b1, 34:W - 34]).ravel()}
        if caixa_sub:
            sx0, sy0, sx1, sy1 = caixa_sub
            m["sub"] = _luminancia(f[sy0:sy1, sx0:sx1]).ravel()
        return m

    def melhor(par):
        return "branco" if par[0] >= par[1] else "preto"

    def idx(cor):
        return 0 if cor == "branco" else 1

    pedido = s.get("fade") or "auto"
    pedido = pedido if isinstance(pedido, str) else "?"  # lista ou número: sem degradê (o render avisa)
    fades = set(FADES_PEDIDOS.get(pedido, set()))
    pode = {"cima", "baixo"} if pedido == "auto" else fades  # lados em que o degradê preto pode entrar

    def escolher(m):
        """Cor dos títulos (cima, baixo) e os lados sem leitura. Cor forçada: fica, e só o branco pode pedir degradê preto
        (preto sobre degradê preto não lê). Senão: 1º uma cor só para os dois (se ela ler em CADA título); senão uma por título;
        o título em que nem preto nem branco leem fica branco e pede o degradê (sem degradê possível, a melhor das duas)."""
        pares = {lado: pior(m[lado]) for lado in ("cima", "baixo")}
        if forcada in ("preto", "branco"):
            falta = {l for l, par in pares.items() if par[idx(forcada)] < CONTRASTE_MIN} if forcada == "branco" else set()
            return forcada, forcada, falta
        tit = tuple(min(pares["cima"][i], pares["baixo"][i]) for i in (0, 1))
        if max(tit) >= CONTRASTE_MIN:
            return melhor(tit), melhor(tit), set()
        cores = {l: melhor(par) if max(par) >= CONTRASTE_MIN or l not in pode else "branco" for l, par in pares.items()}
        return cores["cima"], cores["baixo"], {l for l, par in pares.items() if max(par) < CONTRASTE_MIN}

    def lado_do_sub():  # o degradê que de fato cobre a caixa do subtítulo (o de cima some em ~30% da altura)
        sy0, sy1 = caixa_sub[1], caixa_sub[3]
        cob = {l: float(perfil(FADES[l])[sy0:sy1].mean()) if sy1 > sy0 else 0.0 for l in FADES}
        lado = max(cob, key=cob.get)
        return lado if cob[lado] >= .3 else None

    for _ in range(3):
        m = medir(compor(fades))
        cima, baixo, falta = escolher(m)
        novos = falta & pode
        cor_sub = "branco"
        if caixa_sub:
            sub = pior(m["sub"])  # branco por padrão (o estilo aprovado); preto só se o branco não ler e o preto ler
            cor_sub = "branco" if sub[0] >= CONTRASTE_MIN or sub[1] < CONTRASTE_MIN else "preto"
            if max(sub) < CONTRASTE_MIN and lado_do_sub() in pode:
                novos.add(lado_do_sub())
        if novos <= fades:
            break
        fades |= novos
    final = {"cima": pior(m["cima"])[idx(cima)], "baixo": pior(m["baixo"])[idx(baixo)]}
    alertas = [f"capa: o título de {lado} lê pouco ({v:.1f}:1, mínimo {CONTRASTE_MIN}) — troque a foto, o fundo ou a cor do título"
               for lado, v in final.items() if v < CONTRASTE_MIN]
    if caixa_sub and pior(m["sub"])[idx(cor_sub)] < CONTRASTE_MIN:
        alertas.append(f"capa: o subtítulo lê pouco ({pior(m['sub'])[idx(cor_sub)]:.1f}:1) — mude \"sub_topo\"/\"posicao_sub\" "
                       "ou a foto")
    return {"cima": cima, "baixo": baixo, "sub": cor_sub, "cab": cores_cabecalho(compor(fades), K), "fades": fades, "contraste": final,
            "alertas": alertas}


# o cabeçalho tem 3 textos (esquerda, 64% e direita): cada um escolhe preto ou branco pelo pedaço da foto atrás dele
CAB_X = ((36, 300), (680, 860), (840, W - 36))


def cores_cabecalho(f, K):
    """Preto ou branco para cada texto do cabeçalho, pelo pior contraste (10º percentil) na faixa FAIXA_CAB."""
    import numpy as np
    lb, lp = _luminancia(_rgb(K["branco"])), _luminancia(_rgb(K["preto"]))
    out = []
    for x0, x1 in CAB_X:
        lum = _luminancia(f[FAIXA_CAB[0]:FAIXA_CAB[1], x0:x1]).ravel()
        out.append("branco" if np.percentile((lb + .05) / (lum + .05), 10) >= np.percentile((lum + .05) / (lp + .05), 10) else "preto")
    return out


def sombra_css(nome):
    return "linear-gradient(180deg," + ",".join(f"rgba(0,0,0,{a}) {round(p * 100)}%" for p, a in SOMBRAS[nome]) + ")"


def leitura_foto(s, K, arq):
    """Slides de foto e cta (texto branco sobre a foto, no degradê preto): usa o degradê "normal" da referência e passa para o
    "forte" se o texto não chegar a CONTRASTE_TEXTO no pior 10% da faixa do texto (foto clara embaixo); o cabeçalho fica preto
    ou branco pelo topo da foto (some no branco sobre parede clara). "fade": "normal"|"forte" força o degradê.
    Devolve (degradê, cor do cabeçalho)."""
    fade = s.get("fade") if isinstance(s.get("fade"), str) else ""
    if not arq or not os.path.isfile(arq):
        return fade if fade in SOMBRAS else "normal", ["branco"] * 3
    import numpy as np
    f = foto_cheia(arq, s.get("posicao_imagem"))
    lb, lp = _luminancia(_rgb(K["branco"])), _luminancia(_rgb(K["preto"]))
    cab = cores_cabecalho(f, K)
    if fade in SOMBRAS:
        return fade, cab
    x0, y0, x1, y1 = FAIXA_TEXTO_FOTO.get(s.get("tipo"), FAIXA_TEXTO_FOTO["foto"])
    ys = np.linspace(0, 1, H)[y0:y1]
    for nome in ("normal", "forte"):
        a = np.interp(ys, [p for p, _ in SOMBRAS[nome]], [v for _, v in SOMBRAS[nome]])[:, None, None]
        lum = _luminancia(f[y0:y1, x0:x1] * (1 - a)).ravel()
        if np.percentile((lb + .05) / (lum + .05), 10) >= CONTRASTE_TEXTO:
            return nome, cab
    return "forte", cab


# Manchete: as cores se revezam dentro da paleta (2026-10-15: o azul não é a única cor), numa ordem
# confortável para a vista: cada manchete pega a próxima cor do rodízio que não é da mesma família do slide de antes (azul
# e noite são da mesma família: nunca ficam coladas, nem logo depois da capa azul). "fundo" no slide fixa a cor
# ("preto" só assim: os slides de foto já são escuros). (classe do título, cor do texto e do cabeçalho)
ROTACAO_MANCHETE = ("cor", "noite", "branco")
CORES_MANCHETE = {"cor": ("tx-branco", "branco"), "noite": ("tx-branco", "branco"),
                  "branco": ("tx-noite", "preto"), "preto": ("tx-azul", "branco")}
FAMILIA = {"cor": "marca", "noite": "marca", "branco": "claro", "preto": "escuro"}


def _familia(x, cores):
    """Família de cor de um slide já decidido (para a manchete seguinte não repetir)."""
    tipo = x.get("tipo")
    if tipo == "manchete":
        return FAMILIA.get(cores.get(id(x)), "marca")
    if tipo == "capa2":
        return "claro"
    if tipo == "capa":
        f = cor_marca(x.get("fundo"), "cor")
        return "foto" if x.get("cena") or f == "foto" else "escuro" if f == "escuro" else FAMILIA.get(f, "outra")
    return "escuro" if tipo in ("foto", "cta") else None


def fundo_manchete(s, C):
    if s.get("fundo"):
        f = cor_marca(s["fundo"], "cor")
        return f if f in CORES_MANCHETE else "cor"  # desconhecido: azul (classe sem CSS deixaria o título sumir)
    slides = C.get("slides") or []
    n = s.get("_n")
    if not isinstance(n, int) or not 1 <= n <= len(slides):
        return ROTACAO_MANCHETE[0]
    cores, k, anterior, ultimo_quente = {}, 0, None, None
    for x in slides[:n]:
        if x.get("tipo") == "manchete":
            if x.get("fundo"):
                cores[id(x)] = cor_marca(x["fundo"], "cor")
            else:
                cands = [ROTACAO_MANCHETE[(k + p) % len(ROTACAO_MANCHETE)] for p in range(len(ROTACAO_MANCHETE))]
                cands = [c for c in cands if FAMILIA[c] != anterior] or cands
                # azul e noite se revezam entre si (o noite não some quando as manchetes vêm seguidas)
                cor = ([c for c in cands if not (FAMILIA[c] == "marca" and c == ultimo_quente)] or cands)[0]
                cores[id(x)] = cor
                k = (ROTACAO_MANCHETE.index(cor) + 1) % len(ROTACAO_MANCHETE)
        elif x.get("tipo") == "capa" and cor_marca(x.get("fundo"), "cor") == "cor" and not x.get("cena"):
            ultimo_quente = "cor"
        if FAMILIA.get(cores.get(id(x))) == "marca":
            ultimo_quente = cores[id(x)]
        anterior = _familia(x, cores)
    return cores.get(id(slides[n - 1]), ROTACAO_MANCHETE[0])


def slide(s, M, base, C):
    tipo = s["tipo"]
    arq = caminho(s.get("imagem"), base)
    img = url(arq)
    pos = s.get("posicao_imagem", "center")
    K = paleta(M)
    corpo, classe, cab, estilo = "", "", K["branco"], ""
    alertas_slide = []  # vão no HTML como <meta name='alerta'> e o render conta como ALERTA
    if tipo == "capa":
        escuro = s.get("fundo") == "escuro"  # variação escura/P&B: saiu em 2026-10-15, fica só para peças antigas
        paradas = None if escuro else paradas_fundo(s, K)
        cena = bool(arq) and not escuro and paradas is None
        if escuro:
            classe = ""
        elif paradas == K["azul_paradas"]:
            classe = "cor"
        elif paradas:  # preto, branco ou outra cor
            estilo = f" style='background:{css_degrade(paradas)}'"
        direita = s.get("posicao_sub", "esquerda") == "direita"
        lado = "right:36px" if direita else "left:36px"
        topo_sub = max(0, min(H - 60, _int(s.get("sub_topo"), 500 if direita else 830)))
        subs = [x for x in str(s.get("sub") or "").split("\n") if x]
        x_sub = W - 36 - 440 if direita else 36
        caixa_sub = ((x_sub, topo_sub, x_sub + 440, min(H, topo_sub + 51 * len(subs) + (70 if s.get("tag") else 0)))
                     if subs or s.get("tag") else None)
        fades, cor_sub = set(), "branco"
        if escuro:
            tit_cima = tit_baixo = "tx-azul"
        else:  # preto ou branco pelo contraste com o que fica atrás; "cor_titulo" força; degradê preto se nenhum dos dois ler
            forcada = cor_marca(s.get("cor_titulo"), "")
            L = leitura_capa(s, K, arq, paradas, caixa_sub, forcada)
            cima, baixo = L["cima"], L["baixo"]
            fades, cor_sub, cab = L["fades"], L["sub"], [K[c] for c in L["cab"]]
            alertas_slide += L["alertas"]
            print(f"   capa A: título {cima if cima == baixo else cima + ' em cima e ' + baixo + ' embaixo'}"
                  f"{' (forçado)' if cima == forcada else ''}, subtítulo {cor_sub}"
                  f"{', degradê preto ' + ' e '.join(sorted(fades)) if fades else ''} (contraste no pior trecho: "
                  f"cima {L['contraste']['cima']:.1f}:1, baixo {L['contraste']['baixo']:.1f}:1)")
            tit_cima, tit_baixo = f"tx-{cima}", f"tx-{baixo}"
        pb = " pb" if s.get("pb") else ""
        fade_cima = (f"<div class='fade' data-el='Degradê preto (cima)' style='z-index:1;background:{_fade_css('cima', K)}'></div>"
                     if "cima" in fades else "")
        fade_baixo = (f"<div class='fade' data-el='Degradê preto (baixo)' style='z-index:3;background:{_fade_css('baixo', K)}'></div>"
                      if "baixo" in fades else "")
        camadas = ""
        if cena:  # a foto é o fundo (cena cheia, atrás de tudo); os títulos ficam sobre ela
            camadas = f"<div class='bg{pb}' data-el='Foto de fundo (cena cheia)' style=\"background-image:url('{img}');background-position:{pos}\"></div>"
        elif arq:  # recorte com caixa própria, na frente do título de cima e atrás do de baixo
            tag_img = arte_recorte(s, arq, AREA_CAPA_ESCURA if escuro else AREA_CAPA_COR, "topo-centro" if escuro else "base-centro",
                                   "Personagem (recorte)", "recorte" + pb)
            # o recorte passa na frente do título de propósito: data-frente no lugar de data-arte (sem alerta de sobreposição)
            camadas = tag_img.replace(" data-arte='1'", " data-frente='1'", 1)
            if not escuro and not s.get("imagem_area") and not s.get("ancora") and s.get("recorte", True):
                camadas = camadas.replace("<img ", f"<img data-invade='.linha.topo' data-area='{','.join(map(str, AREA_CAPA_COR))}' ", 1)
        camadas = (camadas + fade_cima + fade_baixo) if cena else (fade_cima + camadas + fade_baixo)
        linhas_sub = "<br>".join(f"<span data-el='Subtítulo · linha {k}'>{fmt(l)}</span>" for k, l in enumerate(subs, 1))
        tag = f"<br><div class='tag {'t-azul' if escuro else 't-preto'}' data-el='Etiqueta'>{fmt(s['tag'])}</div>" if s.get("tag") else ""
        corpo = f"""{camadas}
<div class='linha topo' data-el='Título de cima'><div class='cond {tit_cima}' data-fitw data-el='Título de cima · texto'>{fmt(s.get('topo',''))}</div></div>
<div class='linha base' data-el='Título de baixo'><div class='cond {tit_baixo}' data-fitw data-el='Título de baixo · texto'>{fmt(s.get('base',''))}</div></div>
<div class='sub' data-el='Subtítulo' style='{lado};top:{topo_sub}px;color:{K[cor_sub]}'>{linhas_sub}{tag}</div>"""
    elif tipo == "capa2":
        classe, cab = "branco", K["destaque"]
        pre = fmt(s.get("pre", "")) + (f"<b data-el='Pré-título · destaque'>{fmt(s['titulo_topo'])}</b>" if s.get("titulo_topo") else "")
        pil = f"<div class='pilula' data-el='Pílula'>{fmt(s['tag'])}</div>" if s.get("tag") else ""
        arte = arte_recorte(s, arq, AREA_CAPA_B, "meio-centro", "Arte da capa (recorte)", "arte-b",
                            encaixe=".topo-b", extra=FADE_BASE) if arq else ""
        linhas = "<br>".join(f"<span class='ln' data-el='Título · linha {k}'>{fmt(l)}</span>"
                         for k, l in enumerate(s.get("titulo", "").split("\n"), 1))
        corpo = f"""<div class='topo-b' data-el='Pré-título e pílula'><div class='pre' data-el='Pré-título'>{pre}</div>{pil}</div>
{arte}<div class='tit-b' data-el='Título (pergunta)' data-fith='330'>{linhas}</div>"""
    elif tipo == "manchete":
        fundo = fundo_manchete(s, C)
        classe = fundo
        cor_tit, tx = CORES_MANCHETE[fundo]
        if fundo == "cor" and cor_marca(s.get("cor_titulo"), "") == "preto":  # azul com o título preto (o texto vira branco)
            cor_tit, tx = "tx-preto", "branco"
        cor_tx, cab = f"color:{K[tx]}", K[tx]  # o cabeçalho acompanha o texto
        prop = proporcao(s.get("proporcao"))
        fundo_img = f"background-image:url('{img}');background-position:{pos};" if img else ""
        foto = (f"<div class='ft' data-el='Foto emoldurada' data-proporcao='{prop}' style=\"{fundo_img}aspect-ratio:{prop}\"></div>" if prop else
                f"<div class='ft' data-el='Foto emoldurada' data-prop-auto='1' style=\"{fundo_img}\"></div>")
        corpo = f"""<div class='mold' data-el='Coluna (manchete, foto e texto)'><div class='mt {cor_tit}' data-el='Manchete' data-fith='{s.get('altura_titulo', 380)}'>{fmt(s.get('titulo',''))}</div>{foto}
<div class='tx' data-el='Texto' style='{cor_tx}' data-fith='260'>{fmt(s.get('texto',''))}</div></div>"""
    elif tipo in ("foto", "cta"):
        sombra, cor_cab = leitura_foto(s, K, arq)
        cab = [K[c] for c in cor_cab]
        sombra_el = f"<div class='sombra' data-el='Sombra (degradê preto)' style='background:{sombra_css(sombra)}'></div>"
    if tipo == "foto":
        paras = "".join(f"<p data-el='Parágrafo {k}'>{fmt(p)}</p>" for k, p in enumerate(s.get("texto", []), 1))
        corpo = f"""<div class='bg' data-el='Foto de fundo (cena cheia)' style="background-image:url('{img}');background-position:{pos}"></div>{sombra_el}
<div class='bloco b-foto' data-el='Bloco de texto'><div class='circ' data-el='Seta (círculo)'>{SETA}</div>{paras}</div>"""
    elif tipo == "cta":
        tag = f"<div class='cta-tag' data-el='Tag'>{fmt(s['tag'])}</div>" if s.get("tag") else ""
        corpo = f"""<div class='bg' data-el='Foto de fundo (cena cheia)' style="background-image:url('{img}');background-position:{pos}"></div>
{sombra_el}
<div class='bloco' data-el='Bloco (tag e título)' style='bottom:190px;right:80px'>{tag}<div class='cta-t' data-el='Título'>{fmt(s.get('titulo',''))}</div></div>
<div class='caixa' data-el='Pílula (CTA)'>{fmt(s.get('caixa',''))}</div>"""
    metas = "".join(f"<meta name='alerta' content='{html.escape(a, quote=True)}'>" for a in alertas_slide)
    return (f"<!doctype html><html><head><meta charset='utf-8'>{metas}<style>{css(K)}</style></head>"
            f"<body class='{classe}'{estilo}>{cabecalho(C, cab, M)}{corpo}{GRAO_EL}{AJUSTE_JS}{PROP_JS if tipo == 'manchete' else ''}{ENCAIXE_JS}{INVADE_JS if tipo == 'capa' else ''}</body></html>")
