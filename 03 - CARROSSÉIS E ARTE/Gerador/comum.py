"""Peças compartilhadas pelos modelos (M1 a M4): grão, ajuste automático de texto e recorte de fundo."""
import os

GRAO = """<svg class="grao" xmlns="http://www.w3.org/2000/svg"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""

# data-fitw: a linha cresce/encolhe até ocupar a largura do pai · data-max="px": só encolhe se passar da largura
# data-fith="px": encolhe a fonte até a altura caber
AJUSTE_JS = """<script>
document.fonts.ready.then(function(){
  document.querySelectorAll('[data-fitw]').forEach(function(el){
    var alvo = el.parentElement.clientWidth, lo = 10, hi = 700;
    for (var k = 0; k < 22; k++) { var m = (lo + hi) / 2; el.style.fontSize = m + 'px'; if (el.getBoundingClientRect().width <= alvo) lo = m; else hi = m; }
    el.style.fontSize = lo + 'px';
  });
  document.querySelectorAll('[data-max]').forEach(function(el){
    var max = +el.dataset.max, s = parseFloat(getComputedStyle(el).fontSize);
    while (el.getBoundingClientRect().width > max && s > 20) { s -= 2; el.style.fontSize = s + 'px'; }
  });
  document.querySelectorAll('[data-fith]').forEach(function(el){
    var max = +el.dataset.fith, s = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollHeight > max && s > 20) { s -= 2; el.style.fontSize = s + 'px'; }
  });
  document.body.classList.add('pronto');
});
</script>"""


def caminho(c, base):
    if not c:
        return ""
    return c if os.path.isabs(c) else os.path.join(base, c)


def url(p):
    """Endereço file:/// codificado (apóstrofo, espaço e acento no caminho não quebram o HTML; o render relativiza depois)."""
    import urllib.parse
    return "file:///" + urllib.parse.quote(os.path.abspath(p).replace("\\", "/"), safe="/:") if p else ""


def recortar(origem, modo="borda", tol=None, base=False, erosao=3, buracos=False):
    """Isola o personagem/objeto de uma arte gerada em fundo liso (PRETO ou BRANCO puro) e grava <arte>_recorte.png
    com transparência, do mesmo tamanho da arte. O fundo (preto ou branco) é detectado pelos cantos.
    modo "borda": apaga só o fundo ligado às bordas (fotos e objetos realistas: o miolo do objeto fica opaco).
                  tol automático: 14 no preto (não come cabelo/roupa escura), 34 no branco.
    modo "tinta": cor-para-alfa (objeto luminoso sobre preto): o objeto fica opaco e o fundo some por inteiro,
                  inclusive nos vãos fechados; as cores são preservadas. Em foto realista sobre branco, use "borda".
    base=True também semeia a borda de baixo (objeto que não encosta embaixo). buracos=True também tira o fundo preso dentro do
    sujeito (vão entre tubos, alça, braço na cintura); desligado por padrão para não comer clara de ovo, papel ou camisa clara.
    No fundo claro, uma 2ª passada tira a sombra do chão (metade de baixo) e um matte suave limpa o contorno (cabelo).
    Reaproveita o recorte se ele for mais novo que a arte e tiver sido feito com os mesmos parâmetros."""
    from PIL import Image, ImageDraw, ImageFilter, PngImagePlugin
    import numpy as np
    assinatura = f"{modo}|{tol}|{base}|{erosao}|{int(buracos)}|v14"
    saida = os.path.splitext(origem)[0] + "_recorte.png"
    if os.path.exists(saida) and os.path.getmtime(saida) >= os.path.getmtime(origem):
        try:
            if Image.open(saida).info.get("recorte") == assinatura:
                return saida
        except OSError:
            pass
    im = Image.open(origem).convert("RGB")
    w, h = im.size
    a = np.asarray(im, dtype=np.float32)
    cantos = [a[2, 2], a[2, w - 3]] + ([a[h - 3, 2], a[h - 3, w - 3]] if base else [])
    ref = np.mean(cantos, axis=0)
    escuro = ref.mean() < 128
    if modo == "tinta":
        B = np.zeros(3, np.float32) if escuro else np.full(3, 255, np.float32)
        d = np.where(a >= B, (a - B) / np.maximum(255 - B, 1), (B - a) / np.maximum(B, 1))
        bruto = d.max(axis=2)
        cor = np.clip((a - B) / np.maximum(bruto, 1e-3)[..., None] + B, 0, 255)
        alfa = np.clip((bruto - 0.06) / 0.94, 0, 1)
        rgba = Image.fromarray(np.dstack([cor, alfa * 255]).astype("uint8"), "RGBA")
    else:
        tol = tol or (14 if escuro else 34)
        marca = im.copy()
        MAG = (255, 0, 254)
        passo_x, passo_y = max(1, w // 40), max(1, h // 40)
        sementes = [(x, 0) for x in range(0, w, passo_x)] + [(0, y) for y in range(0, h, passo_y)] + [(w - 1, y) for y in range(0, h, passo_y)]
        if base:
            sementes += [(x, h - 1) for x in range(0, w, passo_x)]
        for x, y in sementes:
            p = marca.getpixel((x, y))
            if p == MAG or np.abs(np.array(p, dtype=float) - ref).max() > tol:
                continue
            ImageDraw.floodfill(marca, (x, y), MAG, thresh=tol)
        m = np.array(marca)
        fundo = (m[:, :, 0] == 255) & (m[:, :, 1] == 0) & (m[:, :, 2] == 254)
        if not escuro:
            # 2ª passada, só na metade de baixo: sombra suave no chão (cinza neutro e claro, ligada ao fundo) também é fundo.
            # Cor viva e tom escuro barram o preenchimento; na metade de cima nada muda (cabelo grisalho fica).
            arr = np.asarray(im, np.int16)
            # contorno vira barreira: a sombra clareia devagar; a borda do objeto muda de repente
            lz = np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(1.5)), np.float32)
            grad = np.zeros_like(lz)
            grad[:, 1:-1] = np.abs(lz[:, 2:] - lz[:, :-2])
            grad[1:-1, :] = np.maximum(grad[1:-1, :], np.abs(lz[2:, :] - lz[:-2, :]))
            barra = ((arr.max(axis=2) - arr.min(axis=2)) > 24) | (arr.mean(axis=2) < 60) | (grad > 14)
            barra = np.asarray(Image.fromarray((barra * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))) > 0
            barra[: int(h * 0.45)] = True
            copia = np.where(fundo[..., None], 255, np.where(barra[..., None], 0, arr)).astype("uint8")
            sombra = Image.fromarray(copia)
            MARCA2 = (1, 2, 3)  # longe do branco (o PIL não preenche se a cor de marcação couber na tolerância)
            for x, y in sementes:
                if sombra.getpixel((x, y)) == (255, 255, 255):
                    # thresh do floodfill do PIL = soma das diferenças nos 3 canais: 3 × (255 − 60) aceita cinza até a luz 60
                    ImageDraw.floodfill(sombra, (x, y), MARCA2, thresh=585)
            s2 = np.array(sombra)
            fundo = fundo | ((s2[:, :, 0] == 1) & (s2[:, :, 1] == 2) & (s2[:, :, 2] == 3))
        try:
            from scipy import ndimage
            if buracos:
                # buracos (só quando pedido: "recorte_buracos": true no slide): fundo preso dentro do sujeito (vão entre
                # tubos, alça de caneca, entre braço e corpo). Sai a região grande, da cor do fundo e quase chapada.
                # Desligado por padrão: clara de ovo, papel e camisa clara podem ter trechos iguais ao fundo.
                perto = (np.abs(a - ref).sum(axis=2) < 40) & ~fundo
                rot_b, nb = ndimage.label(perto)
                if nb:
                    lum_b = a.mean(axis=2)
                    area_b = ndimage.sum(np.ones_like(rot_b), rot_b, index=np.arange(1, nb + 1))
                    desvio = ndimage.standard_deviation(lum_b, rot_b, index=np.arange(1, nb + 1))
                    sai = np.flatnonzero((area_b > 0.0005 * w * h) & (desvio < 8)) + 1
                    fundo = fundo | np.isin(rot_b, sai)
            # ilhas soltas no fundo (pontinhos, ruído) somem; o sujeito e o que encosta nele ficam
            rot, n = ndimage.label(~fundo)
            if n > 1:
                areas = ndimage.sum(np.ones_like(rot), rot, index=np.arange(1, n + 1))
                pequenas = np.flatnonzero(areas < max(400, 0.0004 * w * h)) + 1
                fundo = fundo | np.isin(rot, pequenas)
        except ImportError:
            pass
        alfa = Image.fromarray(np.where(fundo, 0, 255).astype("uint8"))
        if erosao > 1:
            alfa = alfa.filter(ImageFilter.MinFilter(erosao))
        # Matte suave junto do contorno (faixa de ~30 px para dentro): o quanto o pixel ainda é fundo sai da cor dele,
        # comparada com a cor do miolo vizinho (cor-para-alfa local). Fio de cabelo escuro fica, resto de fundo branco entre
        # os fios some, e a cor do fundo que vazou é tirada (unmix). Sem halo claro no slide escuro nem escuro no claro.
        m = np.asarray(alfa, np.float32) / 255
        # miolo = máscara erodida ~30 px (feito na imagem reduzida a 1/4, para ser rápido): a faixa cobre o cabelo ralo
        red = alfa.resize((max(1, w // 4), max(1, h // 4)), Image.BILINEAR).point(lambda v: 255 if v > 250 else 0)
        miolo = np.asarray(red.filter(ImageFilter.MinFilter(13)).resize((w, h), Image.BILINEAR), np.float32) / 255
        def espalhar(raio):  # cor do miolo espalhada para fora (média ponderada pelo miolo) e o peso dela
            pre = Image.fromarray((a * miolo[..., None]).astype("uint8")).filter(ImageFilter.GaussianBlur(raio))
            pz = np.asarray(Image.fromarray((miolo * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(raio)), np.float32) / 255
            return np.asarray(pre, np.float32) / np.maximum(pz, 1e-3)[..., None], pz
        fg, peso = espalhar(16)
        fg2, peso2 = espalhar(60)  # tufos longe do miolo: estimativa mais larga; sem nada perto, a cor média do miolo
        media = (a * miolo[..., None]).sum(axis=(0, 1)) / max(miolo.sum(), 1)
        fg = np.where((peso > 0.05)[..., None], fg, np.where((peso2 > 0.01)[..., None], fg2, media))
        B = 0.0 if escuro else 255.0
        lum, lum_fg = a.mean(axis=2), fg.mean(axis=2)
        k = np.clip(np.abs(lum - B) / np.maximum(np.abs(lum_fg - B), 30), 0, 1)
        # cor viva é sujeito, não mistura com o fundo: o aro vermelho do balde e a pele ficam sólidos; o matte só age no
        # que é neutro (fio de cabelo, resto de fundo branco entre os fios)
        viva = np.clip(((a.max(axis=2) - a.min(axis=2)) - 18) / 20, 0, 1)
        k = k * (1 - viva) + viva
        banda = (m > 0.5) & (miolo < 0.5)
        suave = np.asarray(alfa.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
        af = np.where(banda, np.minimum(suave, k), suave)
        kk = np.maximum(af, 0.05)[..., None]
        cor = np.where((af < 0.98)[..., None], np.clip((a - (1 - kk) * B) / kk, 0, 255), a)
        cor = np.where((m <= 0.5)[..., None], fg, cor)  # só aparece pelo desfoque do alfa: cor do miolo
        rgba = Image.fromarray(np.dstack([cor, af * 255]).clip(0, 255).astype("uint8"), "RGBA")
    info = PngImagePlugin.PngInfo()
    info.add_text("recorte", assinatura)
    rgba.save(saida, pnginfo=info)
    return saida


ANCORAS = {"baixo": "base-centro", "direita": "base-dir", "esquerda": "base-esq", "centro": "meio-centro"}


def modo_pelo_fundo(arq):
    """Modo de recorte pelo fundo da arte (cantos de cima): fundo escuro = "tinta" (objeto luminoso sobre preto);
    fundo claro = "borda" (foto realista sobre branco, o padrão desde 2026-10-14)."""
    from PIL import Image
    im = Image.open(arq).convert("L")
    w, h = im.size
    return "tinta" if (im.getpixel((2, 2)) + im.getpixel((w - 3, 2))) / 2 < 128 else "borda"


def arte_posicionada(arq, area, ancora="base-centro", modo="tinta", recorte=True, rotulo="Arte (recorte)",
                     classe="arte", encaixe="", folga=0, extra="", buracos=False):
    """Recorta, apara e devolve um <img> com caixa justa no personagem, encaixado (sem distorcer) na área
    [x, y, largura, altura] do slide e ancorado em ancora = "<base|meio|topo>-<esq|centro|dir>" (ou baixo/direita/esquerda/centro).
    A área pode passar da borda do slide (a arte sangra). encaixe="<seletor css>": no navegador, a arte encolhe
    (mantendo a âncora) se invadir o bloco de texto indicado. data-original guarda a arte bruta para o editor refazer o recorte.
    modo="auto": "borda" se a arte veio em fundo branco, "tinta" se veio em fundo preto (modo_pelo_fundo)."""
    from PIL import Image
    import html as _html
    if not arq:
        return ""
    if modo == "auto":
        modo = modo_pelo_fundo(arq)
    p = aparar(recortar(arq, modo=modo, buracos=buracos)) if recorte else arq
    iw, ih = Image.open(p).size
    x, y, aw, ah = area
    k = min(aw / iw, ah / ih)
    w, h = round(iw * k), round(ih * k)
    anc = ANCORAS.get(ancora, ancora)
    left = x if "esq" in anc else x + aw - w if "dir" in anc else x + (aw - w) / 2
    top = y if "topo" in anc else y + (ah - h) / 2 if "meio" in anc else y + ah - h
    enc = f" data-encaixe='{_html.escape(encaixe)}' data-folga='{folga}'" if encaixe else ""
    return (f"<img class='{classe}' data-arte='1' data-el='{_html.escape(rotulo)}' data-ancora='{anc}' data-modo='{modo}'{enc}"
            f" data-original='{url(arq)}' src='{url(p)}' style='left:{left:.0f}px;top:{top:.0f}px;width:{w}px;height:{h}px;{extra}'>")


# Arte com data-encaixe encolhe (mantendo a âncora) só o necessário para não ficar embaixo de nenhuma LINHA de texto do bloco
# indicado: mede as linhas de verdade (não a caixa do bloco), então a arte pode crescer ao lado de linhas curtas ou do outro
# lado do slide (diagonal do M1, peixe da capa do M2). Busca binária na altura. O editor tira o data-encaixe quando a arte é
# movida à mão, para respeitar a posição escolhida.
ENCAIXE_JS = """<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){
  function linhas(alvo){
    var out = [], tw = document.createTreeWalker(alvo, NodeFilter.SHOW_TEXT, null);
    while (tw.nextNode()) { if (!tw.currentNode.textContent.trim()) continue;
      var rg = document.createRange(); rg.selectNodeContents(tw.currentNode);
      [].slice.call(rg.getClientRects()).forEach(function(x){ if (x.width > 2 && x.height > 2) out.push(x); }); }
    return out;
  }
  document.querySelectorAll('[data-encaixe]').forEach(function(img){
    var alvo = document.querySelector(img.dataset.encaixe); if (!alvo) return;
    var ls = linhas(alvo), folga = +img.dataset.folga || 0, r0 = img.getBoundingClientRect(), a = img.dataset.ancora || '';
    function caixa(h){ var w = r0.width * h / r0.height;
      var left = a.indexOf('dir') >= 0 ? r0.right - w : a.indexOf('esq') >= 0 ? r0.left : r0.left + (r0.width - w) / 2;
      return {left: left, right: left + w, top: r0.bottom - h, w: w, h: h}; }
    function cabe(c){ return ls.every(function(x){ return Math.min(x.right, c.right) - Math.max(x.left, c.left) <= 4 || c.top >= x.bottom + folga; }); }
    if (cabe(caixa(r0.height))) return;
    var lo = Math.min(260, r0.height), hi = r0.height;
    for (var k = 0; k < 14; k++) { var m = (lo + hi) / 2; if (cabe(caixa(m))) lo = m; else hi = m; }
    var c = caixa(lo);
    img.style.left = c.left + 'px'; img.style.top = c.top + 'px'; img.style.width = c.w + 'px'; img.style.height = c.h + 'px';
  });
});
</script>"""


# ---------- tratamento da arte (decisão de 2026-10-14: escolhido na hora, por peça e por slide) ----------
# "cena"    = foto inteira cobrindo o slide, sem recorte, com um degradê de leitura do lado do texto.
# "recorte" = o sujeito recortado (arte_posicionada) sobre um fundo:
#             "liso" (cor do tema) · "branco" / "preto" (forçam o tema claro / escuro) · "quadriculado" (grade fina na cor do
#             tema) · "blend" (foto de elementos do tema, desfocada atrás do recorte, com véu da cor do tema).
# Não há caixa fixa para o sujeito (cada silhueta é diferente): cada formato define só a zona aproximada onde ele fica.
TRATAMENTOS = ("cena", "recorte")
FUNDOS = ("liso", "branco", "preto", "quadriculado", "blend")

TRATAMENTO_CSS = """
.blend{position:absolute;inset:-60px;z-index:2;background-size:cover;background-position:center;filter:blur(11px) saturate(.9);transform:scale(1.06)}
.veu{position:absolute;inset:0;z-index:3}
.quad{position:absolute;inset:0;z-index:2;background-size:54px 54px;background-position:-1px -1px}
.leitura{position:absolute;inset:0;z-index:4;pointer-events:none}
.cena{position:absolute;inset:0;z-index:1;background-size:cover;background-position:center}
.guia{position:absolute;z-index:45;border:3px dashed #ff00c8;pointer-events:none}
.guia span{position:absolute;left:8px;top:6px;font:600 20px/1 Arial,sans-serif;color:#ff00c8;background:rgba(255,255,255,.85);padding:4px 8px}
"""


def _rgba(hexcor):
    """'#0B0B0E' → 'rgba(11,11,14,' (o JS e o CSS completam com a opacidade e o parêntese)."""
    h = hexcor.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},"


def tema_do_fundo(fundo, tema):
    """Fundo branco força o tema claro; preto força o escuro; os outros seguem o tema do slide."""
    return {"branco": "claro", "preto": "escuro"}.get(fundo, tema)


def camadas_fundo(tratamento, fundo, cor_tema, claro, url_cena="", url_blend="", enquadramento="center",
                  leitura="topo", alvo=".bloco"):
    """HTML das camadas de fundo do slide conforme o tratamento da arte (o recorte em si vem de arte_posicionada).
    cor_tema = cor de fundo do tema ('#0B0B0E' ou '#F2F4F8'); claro = True no tema claro.
    leitura = lado do texto ("topo", "esquerda", "direita" ou "" para nenhum): o degradê de leitura cobre o bloco `alvo`
    (medido no navegador pelo LEITURA_JS) e some depois dele, para a foto ou o fundo desfocado não brigarem com o texto."""
    c = _rgba(cor_tema)
    out = ""
    if tratamento == "cena":
        if url_cena:
            out += (f"<div class='cena' data-el='Foto de fundo (cena inteira)' "
                    f"style=\"background-image:url('{url_cena}');background-position:{enquadramento}\"></div>")
    elif fundo == "quadriculado":
        linha = "rgba(0,0,0,.15)" if claro else "rgba(255,255,255,.14)"  # visível sem brigar com o texto 
        out += (f"<div class='quad' data-el='Fundo quadriculado' style=\"background-image:linear-gradient({linha} 2px,transparent 2px),"
                f"linear-gradient(90deg,{linha} 2px,transparent 2px)\"></div>")
    elif fundo == "blend" and url_blend:
        out += (f"<div class='blend' data-el='Fundo desfocado (elementos do tema)' style=\"background-image:url('{url_blend}')\"></div>"
                f"<div class='veu' data-el='Véu do fundo desfocado' style='background:{c}{.3 if claro else .35})'></div>")
    if leitura and (tratamento == "cena" or fundo == "blend"):
        out += f"<div class='leitura' data-el='Degradê de leitura' data-lado='{leitura}' data-alvo='{alvo}' data-cor='{c}'></div>"
    return out


def guia_zona(area, rotulo="zona do sujeito"):
    """Contorno tracejado da zona aproximada do sujeito (só com --guias, para a revisão do layout; não vai para publicação)."""
    x, y, w, h = area
    return (f"<div class='guia' data-livre='1' data-el='Guia (zona do sujeito)' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px'>"
            f"<span>{rotulo}</span></div>")


# Degradê de leitura: sólido até o fim do bloco de texto (com folga) e some em 260 px. Roda depois do ajuste das fontes.
LEITURA_JS = """<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){
  document.querySelectorAll('.leitura').forEach(function(el){
    var alvo = document.querySelector(el.dataset.alvo), c = el.dataset.cor, lado = el.dataset.lado;
    if (!alvo) return;
    var r = alvo.getBoundingClientRect(), g;
    if (lado == 'topo') { var y = Math.min(1350, r.bottom + 40);
      g = 'linear-gradient(180deg,' + c + '.92) 0px,' + c + '.84) ' + y + 'px,' + c + '0) ' + (y + 260) + 'px)'; }
    else if (lado == 'esquerda') { var x = Math.min(1080, r.right + 30);
      g = 'linear-gradient(90deg,' + c + '.92) 0px,' + c + '.82) ' + x + 'px,' + c + '0) ' + (x + 240) + 'px)'; }
    else if (lado == 'direita') { var x2 = Math.max(0, r.left - 30);
      g = 'linear-gradient(270deg,' + c + '.92) 0px,' + c + '.82) ' + (1080 - x2) + 'px,' + c + '0) ' + (1080 - x2 + 240) + 'px)'; }
    if (g) el.style.background = g;
  });
});
</script>"""


def aparar(png):
    """Corta as margens transparentes de um recorte (caixa justa no personagem), para ele virar um elemento
    que se posiciona e redimensiona sozinho no layout. Gera <png>_aparado.png; reaproveita se já existir e for mais novo."""
    from PIL import Image
    saida = os.path.splitext(png)[0] + "_aparado.png"
    if os.path.exists(saida) and os.path.getmtime(saida) >= os.path.getmtime(png):
        return saida
    im = Image.open(png).convert("RGBA")
    caixa = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    (im.crop(caixa) if caixa else im).save(saida)
    return saida


def fracao_transparente(png):
    """Fração de pixels transparentes de um recorte (para acusar recorte que falhou ou comeu o personagem)."""
    from PIL import Image
    a = Image.open(png).convert("RGBA").getchannel("A")
    hist = a.histogram()
    return sum(hist[:128]) / max(1, a.width * a.height)
