"""Modelo 4 — Cinema (storytelling cinematográfico: fundo escuro texturizado, artes do tema geradas no Google Flow, elementos de interface —
barra de busca, janela, caixa de seleção, vidro fosco — e fundo claro de nuvens). Importado por render_carrossel.py
quando "modelo": "cinema".

As molduras douradas da referência NÃO fazem parte do modelo: cada espaço de imagem recebe a arte do tema gerada no Flow.
REGRA DAS ARTES (igual à das referências; foto realista, decisão de 2026-10-14: nada de anime, gravura ou ilustração):
  · personagem/objeto sobre fundo liso = RECORTE: o gerador tira o fundo (PNG transparente), apara na caixa do objeto e posiciona
    como elemento próprio (pode sangrar para fora do slide). Gere no Flow sobre BRANCO PURO (foto realista); PRETO PURO só para
    objeto luminoso realista. Sem degradê, sem vinheta e sem sombra no chão. A proporção da arte quase não importa (a caixa é
    aparada no objeto), só a resolução: peça a proporção parecida com a do objeto.
  · cenário atrás do texto = FOTO INTEIRA (capa; ou "mistura":"cena" nos demais), sem recorte.
Campos opcionais em slides com arte:
  "modo_recorte":"borda|tinta" (e "modo_recorte2" para a imagem2) — "borda" = só o fundo ligado às bordas (foto realista, objeto
      sobre branco); "tinta" = cor-para-alfa (objeto luminoso sobre preto: o preto some inteiro). Padrão automático pelo fundo da arte
      (comum.modo_pelo_fundo): borda no branco, tinta no preto; nas mãos do slide vidro e na capa B, sempre borda.
  "imagem_area":[x,y,larg,alt] · "imagem2_area":[...] — caixa do slide onde a arte é encaixada (sem distorcer; pode passar da borda);
  "ancora":"base-esq|base-centro|base-dir|meio-esq|meio-centro|meio-dir|topo-esq|topo-centro|topo-dir" (e "ancora2").
  "mistura":"recorte" (padrão; "normal" = o mesmo) | "cena" (cena inteira, sem recorte; bordas esfumadas, ou tela cheia em capa/vidro/texto)
      | "clarear" | "multiplicar" (sem recorte; mistura por flag explícita) · "girar": graus · "topo"/"imagem_topo" (px) em alguns tipos.
Todo elemento visível tem data-el="Nome" (o editor visual lista e edita cada um). Artes: <img data-arte data-original=...>.

Slides (exemplos de forma; o texto segue o Método de texto do carrossel: leigo, sem "você" fora do CTA, sem fórmula de IA):
  {"tipo":"capa","imagem":"x.png","contador":"#01 / 09","linha1":"O fim","linha2":"da falha","script":"exaustão",
   "caixa":"_O que sobra_ **depois da última série**"}     (foto inteira num cartão arredondado de margem preta)
  {"tipo":"capa2","titulo":"4 → ==10==","sub":"séries por semana","cursor":"jorgesouto","imagem":"x.png","nota":"até certo\\nponto"}
       (capa B, janela clara; título: texto = condensada cinza, ==x== = itálico fino no azul da marca, _x_ = letra cursiva; imagem = recorte
        sobre BRANCO, ~800x460 em y460)
  {"tipo":"busca","busca":"volume de treino","indice":["Início","..."],"imagem":"figura.png","imagem2":"anilha.png",
   "texto":["_Sair destruído da academia_ ==parece treino bem feito.==","==Numa revisão,== texto menor"],"balao":"Será que\\né demais?","fecho":"_Só que o espelho_ ==nem sempre acompanha...=="}
       (imagem = figura sangrando embaixo-esquerda, abaixo dos parágrafos; imagem2 = PONTE: objeto centrado na divisa x=1080, metade
        aqui e a outra metade no slide seguinte, no mesmo lugar e tamanho, sem emenda na troca de slide (2026-10-15); "ponte_topo" ajusta a altura. O slide seguinte, se for lateral/quadro, usa a ponte no lugar da própria arte)
  {"tipo":"lateral","imagem":"arte.png","texto":["_A soma da semana_ ==pesa mais que um dia.==","**_Mesmo quando o treino cansa menos..._**"],
   "rodape":"**Subir a dose** aos poucos... !!pede alguém acompanhando.!!"}     ("quadro" é igual; arte sangra à esquerda)
  {"tipo":"vidro","imagem":"maos.png","cartoes":["Peso leve<br>==deu músculo parecido==<br><small>quando a série terminou perto do cansaço</small>","A falha em toda série... **não pareceu necessária.**"]}
       (imagem = recorte ~1000x520 entre e sob os cartões de vidro; "topos":[290,960]; no tema claro o vidro é claro e o texto preto)
  {"tipo":"texto","imagem":"objeto-cima.png","imagem2":"objeto-base.png","texto":"O cansaço diz muito... !!a soma da semana diz mais.!!",
   "nota":"==Dose é dose,== no treino também... **a planilha mostra.**"}     (imagem = canto superior esquerdo; imagem2 (opcional) = base)
  {"tipo":"janela","tema":"claro|escuro","barra":"A regra final","janela":"==Contar as séries.== Depois, subir aos poucos...","texto":"No treino... **a série termina perto do cansaço.**"}
  {"tipo":"pergunta","tema":"claro|escuro","texto":"**Quer um treino para a sua rotina?**<br>Jorge Souto, CREF … · ==link na bio=="}
       (é o CTA: ponte curta + ação, até 90 caracteres; o CREF vem do "registro" do marca.json)
Marcação: **negrito**, _itálico_, ==azul da marca em degradê (negrito)==, !!marca-texto!!, <br>, <small>…</small>.
Ajustes finos opcionais em qualquer slide: "topo" (px; "rodape_topo" no lateral) e "imagem_pos" (capa/cena inteira: "center", "left top"...).
"""
import html
import random
import re

from comum import AJUSTE_JS, ENCAIXE_JS, GRAO, arte_posicionada, caminho, url

W, H = 1080, 1350
# Cores: todo elemento gráfico só nas cores da marca (o azul da marca em degradê: aço, elétrico, royal e noite; branco
# e preto; cinza = preto com transparência), lidas do marca.json. As fotos podem ter qualquer cor.


def _hex(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def paleta(M):
    p = M.get("paleta") or {}
    s, v, a = p.get("clara", "#445DB4"), p.get("principal", "#2E49CE"), p.get("media", "#1F33A3")
    t = p.get("profunda", "#141A3D")
    pr, br = M.get("fundo_escuro") or "#0B0B0E", M.get("fundo_claro") or "#F2F4F8"

    def mistura(c1, c2, k):  # c1 → c2 em k (0–1)
        return "#%02X%02X%02X" % tuple(round(x + (y - x) * k) for x, y in zip(_hex(c1), _hex(c2)))

    def rgba(c, al):
        return "rgba(%d,%d,%d,%s)" % (*_hex(c), al)

    return {"grad": M.get("gradiente") or f"linear-gradient(100deg,{s} 0%,{v} 48%,{a} 100%)",
            "grad_escuro": M.get("gradiente_escuro") or M.get("gradiente") or f"linear-gradient(100deg,{s} 0%,{v} 48%,{a} 100%)", "clara": s, "principal": v,
            "media": a, "profunda": t, "preto": pr, "branco": br, "mistura": mistura, "rgba": rgba}


XIS = "<svg data-el='Ícone ×' viewBox='0 0 20 20' stroke='currentColor' stroke-width='2.2' stroke-linecap='round'><path d='M5 5l10 10M15 5L5 15'/></svg>"
GRAO_EL = GRAO.replace('<svg class="grao"', '<svg class="grao" data-el="Grão (textura)"')


def fmt(t):
    t = html.escape(t).replace("&lt;br&gt;", "<br>").replace("&lt;small&gt;", "<small>").replace("&lt;/small&gt;", "</small>")
    t = re.sub(r"(CREF\s*\d+(?:-[A-Z])?(?:/[A-Z]{2})?)", r"<span style='white-space:nowrap'>\1</span>", t)  # registro inteiro numa linha
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"==(.+?)==", r"<span class='lj'>\1</span>", t)
    t = re.sub(r"!!(.+?)!!", r"<span class='mt'>\1</span>", t)
    t = re.sub(r"(?<![\w/])_(.+?)_(?!\w)", r"<i>\1</i>", t)
    return t


def css(K):
    P, B, mix, rgba = K["preto"], K["branco"], K["mistura"], K["rgba"]
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@500;600&family=Nunito:ital,wght@0,300;0,400;0,600;0,800;0,900;1,300;1,400;1,800&family=Yellowtail&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:'Nunito',sans-serif;font-weight:300;position:relative;-webkit-font-smoothing:antialiased;color:{B}}}
body.escuro{{background:radial-gradient(ellipse 90% 60% at 50% 0%,{mix(P, B, .1)} 0%,{mix(P, B, .035)} 50%,{P} 100%)}}
body.escuro:before{{content:'';position:absolute;inset:0;z-index:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1.3px);background-size:7px 7px}}
body.claro{{background:radial-gradient(ellipse 70% 55% at 50% 50%,{B} 0%,{mix(B, P, .03)} 55%,{mix(B, P, .1)} 100%);color:{rgba(P, .58)}}}
body.claro:before{{content:'';position:absolute;inset:0;z-index:0;background-image:radial-gradient(rgba(0,0,0,.07) 1px,transparent 1.3px);background-size:7px 7px}}
body.capa{{background:{P}}} body.capa:before{{display:none}}
.grao{{position:absolute;inset:0;width:100%;height:100%;z-index:90;opacity:.13;mix-blend-mode:overlay;pointer-events:none}}
.nuvens{{position:absolute;inset:0;z-index:1;pointer-events:none}}
.nuvens i{{position:absolute;border-radius:50%;background:radial-gradient(circle,{rgba(P, .26)} 0%,{rgba(P, .14)} 35%,{rgba(P, .04)} 58%,{rgba(P, 0)} 72%)}}  /* sem filter:blur: o desfoque pesado falhava no render (faixas brancas na base) */
b{{font-weight:800}} i{{font-style:italic}} small{{font-size:.78em}}
.lj{{font-weight:800;background:{K['grad']};-webkit-background-clip:text;background-clip:text;color:transparent}}
body.escuro .lj{{background:{K['grad_escuro']};-webkit-background-clip:text;background-clip:text}}
.lj i,i .lj{{font-style:italic}}
.mt{{font-weight:800;color:{B};background:{K['grad']};padding:0 7px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.z{{position:absolute;z-index:10}}
/* artes: recorte real (PNG transparente, mistura normal). clarear/multiplicar/cena só por "mistura" explícita */
.arte{{position:absolute;z-index:3;max-width:none}}
.arte.clarear{{mix-blend-mode:lighten}} .arte.multiplicar{{mix-blend-mode:multiply}}
.arte.cena{{-webkit-mask-image:radial-gradient(ellipse 72% 72% at 50% 50%,#000 58%,transparent 100%);mask-image:radial-gradient(ellipse 72% 72% at 50% 50%,#000 58%,transparent 100%)}}
.bg{{position:absolute;inset:0;z-index:1;background-size:cover;background-position:center}}
/* capa: foto inteira num cartão arredondado com margem preta */
.bg.cartao{{inset:18px;border-radius:38px}}
.vinheta{{position:absolute;inset:18px;border-radius:38px;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 60%,rgba(0,0,0,.75) 100%)}}
.cont{{left:50%;transform:translateX(-50%);top:78px;white-space:nowrap;border:2px solid rgba(255,255,255,.75);border-radius:999px;padding:6px 20px;font:600 27px/1.1 'Nunito';color:{B}}}
.tit{{left:60px;right:60px;top:200px;text-align:center}}
.l1,.l2{{display:inline-block;font-family:'Anton';font-size:230px;line-height:.86;letter-spacing:-.01em;white-space:nowrap}}
.l1{{color:{B};text-shadow:-5px 0 0 {rgba(K['clara'], .6)},5px 0 0 {rgba(K['profunda'], .6)},0 10px 40px rgba(0,0,0,.6)}}
.l2{{padding:.1em .03em .16em;margin:-.1em 0 -.16em;background:{K['grad_escuro']};-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 10px 26px rgba(0,0,0,.55))}}
.scr{{display:block;font-family:'Yellowtail';font-size:120px;line-height:.7;color:{B};transform:rotate(-7deg);margin:-34px 0 0 260px;text-shadow:0 6px 24px rgba(0,0,0,.6)}}
.caixa-x{{left:50%;transform:translateX(-50%);bottom:225px;white-space:nowrap;display:flex;align-items:center;gap:34px;border:2px dashed rgba(255,255,255,.9);padding:16px 26px;font-size:38px;color:{B};background:rgba(0,0,0,.18)}}
.caixa-x svg{{width:22px;height:22px;flex:none}}
/* capa com texto longo (2026-10-21): cursiva em até 2 linhas e caixa em até 3 linhas, centradas */
.scr.longa{{font-size:86px;line-height:1.02;white-space:normal;max-width:900px;margin:4px auto 0;transform:rotate(-4deg);text-align:center}}
.caixa-x.longa{{bottom:150px;white-space:normal;width:900px;gap:22px;padding:20px 28px;font-size:40px;line-height:1.22;text-align:center}}
.assin{{left:56px;bottom:52px;display:flex;align-items:center;gap:18px;padding:14px 28px;border-radius:999px;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.14);backdrop-filter:blur(10px);font:400 26px/1 'Nunito';color:rgba(255,255,255,.75)}}
.assin b{{color:{B};font-weight:800}} .assin em{{width:1px;height:26px;background:rgba(255,255,255,.4)}}
/* capa B */
.janela-b{{position:absolute;left:36px;right:36px;top:38px;bottom:36px;border-radius:44px;z-index:1;background:linear-gradient(180deg,{B},{mix(B, P, .05)});overflow:hidden;
background-image:linear-gradient(rgba(0,0,0,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.035) 1px,transparent 1px),linear-gradient(180deg,{B},{mix(B, P, .055)});background-size:120px 120px,120px 120px,auto}}
.ctrl{{position:absolute;top:44px;color:{rgba(P, .42)};font:300 40px/1 'Nunito'}}
.tb{{left:40px;right:40px;top:150px;text-align:center;white-space:nowrap}}
.tb .t{{display:inline-block;font-family:'Anton';font-size:170px;line-height:1;letter-spacing:-.01em;background:linear-gradient(180deg,{rgba(P, .48)},{rgba(P, .68)});-webkit-background-clip:text;background-clip:text;color:transparent}}
.tb .t .lj{{font-family:'Nunito';font-weight:300;font-style:italic;letter-spacing:-.06em;margin-right:24px}}
.tb .t i{{font-family:'Yellowtail';font-style:normal;font-size:1.05em;margin-right:-6px}}
.sb{{left:0;right:0;top:350px;text-align:center;font-size:56px;color:{rgba(P, .42)}}} .sb b{{font-style:italic;color:{rgba(P, .58)}}}
.cursor{{right:62px;top:330px;width:170px}}
.cursor svg{{width:46px;height:52px;margin-left:-10px}}
.cursor span{{display:inline-block;margin-top:-4px;padding:6px 14px 8px;background:{K['grad']};color:{B};font:700 31px/1 'Nunito'}}
/* capa B · variante foto */
.tbf{{left:70px;right:70px;text-align:center}}
.tbf .t{{display:inline-block;white-space:nowrap;font-family:'Anton';font-size:150px;line-height:.96;letter-spacing:.005em;color:{rgba(P, .82)}}}
.tbf .t .lj{{font-family:'Anton';font-weight:400;font-style:normal;padding:0 .02em}}
.sbf{{margin-top:26px;font:600 46px/1.15 'Nunito';color:{rgba(P, .62)};letter-spacing:-.005em}} .sbf b{{color:{rgba(P, .85)};font-weight:800}}
.foto-f{{inset:auto;left:150px;right:150px;border-radius:30px;box-shadow:0 30px 60px -20px rgba(0,0,0,.45),0 0 0 1px rgba(0,0,0,.06);z-index:3}}
.cursor-f{{right:96px;z-index:12;display:flex;align-items:flex-start}}
.cursor-f svg{{width:46px;height:52px;margin-right:-6px}}
.cursor-f span{{margin-top:34px;padding:8px 16px 10px;background:{K['grad']};color:{B};font:800 32px/1 'Nunito';border-radius:6px}}
.nota-f{{left:400px;right:110px;font-family:'Caveat';font-weight:600;color:{rgba(P, .72)};font-size:66px;line-height:.98;transform:rotate(-5deg)}}
.nota{{font-family:'Caveat';font-weight:500;color:{rgba(P, .56)};font-size:64px;line-height:.95;transform:rotate(-9deg)}}
/* busca */
.busca{{left:50%;top:84px;transform:translateX(-50%);width:640px;height:68px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);display:flex;align-items:center;padding:0 30px 0 44px;font:400 23px 'Nunito';color:rgba(255,255,255,.72)}}
.busca .ic{{margin-left:auto;display:flex;gap:20px;align-items:center;color:rgba(255,255,255,.65)}} .busca svg{{width:22px;height:22px}}
.indice{{left:66px;top:400px;font:400 14px/1.9 'Nunito';color:rgba(255,255,255,.2)}} .indice b{{color:rgba(255,255,255,.32)}}
.col{{color:{B}}}
.col p{{margin-bottom:34px}}
.p1{{font-size:38px;line-height:1.15}} .p2{{font-size:27px;line-height:1.28;font-weight:400}}
.balao{{display:inline-block;position:relative;padding:28px 54px;font-family:'Caveat';font-weight:500;font-size:38px;line-height:1.05;text-align:center;color:{B}}}
.balao svg{{position:absolute;inset:-6px -10px;width:calc(100% + 20px);height:calc(100% + 12px);overflow:visible}}
.fecho{{font-size:56px;line-height:1.08}}
/* lateral / texto */
.rod{{left:200px;right:210px;top:940px;text-align:center;font-size:35px;line-height:1.22;font-weight:400}}
.liga{{position:absolute;z-index:9;overflow:visible;color:rgba(255,255,255,.75)}} body.claro .liga{{color:{rgba(P, .55)}}} body.claro .rod{{color:{rgba(P, .8)}}}
body.claro .col{{color:{rgba(P, .82)}}} body.claro .colchete{{border-color:{rgba(P, .7)}}}
.colchete{{border-left:2px solid rgba(255,255,255,.85);border-bottom:2px solid rgba(255,255,255,.85);width:48px;height:150px;flex:none;margin-top:-30px}}
.brilho{{position:absolute;inset:0;pointer-events:none}}
.brilho i{{position:absolute;border-radius:50%;background:{K['clara']};box-shadow:0 0 8px 2px {rgba(K['clara'], .8)};z-index:4}}
/* vidro */
.vid{{left:50%;transform:translateX(-50%);text-align:center;border-radius:36px;padding:40px 52px;background:{rgba(P, .34)};border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(16px) saturate(1.1);
font-size:40px;line-height:1.16;color:{B};box-shadow:0 20px 60px rgba(0,0,0,.35)}}
.vid .brl{{position:absolute;left:50%;top:-6px;width:150px;height:12px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse,rgba(255,255,255,.95),rgba(255,255,255,0) 70%)}}
.vid small{{display:block;margin-top:26px;font-size:30px;line-height:1.2}}
body.claro .vid{{background:{rgba(B, .62)};border-color:{rgba(P, .1)};color:{rgba(P, .85)};box-shadow:0 20px 60px rgba(0,0,0,.12)}}
/* janela */
.jan{{left:50%;transform:translateX(-50%);width:640px;border-radius:30px;background:linear-gradient(180deg,{mix(P, B, .1)},{mix(P, B, .045)});box-shadow:0 30px 70px rgba(0,0,0,.35);color:{B};overflow:hidden}}
.jan .barra{{height:62px;display:flex;align-items:center;padding:0 26px;font:400 23px 'Nunito';color:rgba(255,255,255,.8)}}
.jan .barra i{{width:16px;height:16px;border-radius:50%;margin-right:10px;display:inline-block}}
.jan .barra span{{position:absolute;left:0;right:0;text-align:center}} .jan .barra em{{margin-left:auto;font-style:normal;font-size:30px;color:rgba(255,255,255,.7)}}
.jan .corpo{{padding:38px 46px 52px;text-align:center;font-size:44px;line-height:1.14}}
.abaixo{{left:170px;right:170px;text-align:center;font-size:38px;line-height:1.18;font-weight:400}}
/* pergunta */
.sel{{left:50%;transform:translateX(-50%);width:690px;border:2px dashed {rgba(P, .68)};padding:52px 46px;text-align:center;font-size:52px;line-height:1.16;font-weight:400}}
.sel b{{font-weight:800}}
body.escuro .sel{{border-color:{rgba(B, .55)}}} body.escuro .sel i.h{{border-color:{rgba(B, .7)};background:{P}}}
.sel i.h{{position:absolute;width:20px;height:20px;border:2px solid {rgba(P, .68)};background:{B}}}
"""


def nuvens(seed=7):
    r = random.Random(seed)
    bolhas = []
    for faixa in (-60, 1260):
        for _ in range(9):
            tam = r.randint(260, 520)
            bolhas.append(f"<i style='left:{r.randint(-200, 1000)}px;top:{faixa + r.randint(-140, 140) - tam // 2}px;width:{tam}px;height:{tam}px'></i>")
    return "<div class='nuvens' data-el='Nuvens (fundo)'>" + "".join(bolhas) + "</div>"


def brilho(seed=3):
    r = random.Random(seed)
    pts = []
    for _ in range(26):
        t = r.choice([2, 3, 3, 4, 5])
        pts.append(f"<i style='left:{r.randint(40, 1040)}px;top:{r.randint(80, 1280)}px;width:{t}px;height:{t}px;opacity:{r.uniform(.35, .9):.2f}'></i>")
    return "<div class='brilho' data-el='Brilhos (partículas)'>" + "".join(pts) + "</div>"


def balao_svg():
    return ("<svg data-el='Contorno do balão' viewBox='0 0 100 50' preserveAspectRatio='none' fill='none' stroke='currentColor' stroke-width='0.9' stroke-linecap='round'>"
            "<path vector-effect='non-scaling-stroke' style='stroke-width:2.2px' d='M8 30 C2 14,28 3,52 3 C80 3,99 12,97 26 C95 41,70 48,47 47 C30 46,16 43,11 37 L2 47 L13 36 C9 34,8 32,8 30 Z'/></svg>")


def cena_inteira(s, base, chave="imagem", estilo=""):
    """Foto inteira de fundo (sem recorte): <div class='bg'> cobrindo o slide."""
    arq = caminho(s.get(chave), base)
    if not arq:
        return ""
    cls = "bg" + (f" arte {s['mistura']}" if s.get("mistura") in ("clarear", "multiplicar") else "")
    g = f"transform:rotate({s['girar']}deg);" if s.get("girar") else ""
    return (f"<div class='{cls}' data-el='Foto de fundo (cena cheia)' data-original='{url(arq)}' "
            f"style=\"background-image:url('{url(arq)}');background-position:{s.get('imagem_pos') or 'center'};{g}{estilo}\"></div>")


def arte(s, base, chave, area, ancora, rotulo, modo="auto", encaixe="", folga=0, sob=False):
    """Arte do slide como elemento próprio. Padrão: recorte real (fundo liso → PNG transparente, apara, encaixa na área sem distorcer,
    âncora). "mistura": cena / clarear / multiplicar = sem recorte (flag explícita). sob=True: o texto passa sobre esta arte
    de propósito (cartões de vidro, balão), então a verificação 'texto sobre a arte recortada' não se aplica."""
    arq = caminho(s.get(chave), base)
    if not arq:
        return ""
    suf = "2" if chave == "imagem2" else ""
    mist = s.get("mistura") or "recorte"
    area = s.get(chave + "_area") or area
    anc = s.get("ancora" + suf) or ancora
    modo = s.get("modo_recorte" + suf) or s.get("modo_recorte") or modo
    extra = f"transform:rotate({s['girar']}deg);" if s.get("girar") else ""
    classe, recorte = "arte", True
    if mist in ("cena", "clarear", "multiplicar"):
        classe, recorte = f"arte {mist}", False
    out = arte_posicionada(arq, area, anc, modo, recorte=recorte, rotulo=rotulo, classe=classe, encaixe=encaixe, folga=folga, extra=extra,
                           buracos=bool(s.get("recorte_buracos")))
    return out.replace("data-arte='1'", "data-arte-sob='1'", 1) if sob else out


# Ponte do slide de busca para o seguinte: caixa de 600x540 centrada na divisa dos dois slides (x = 1080). O mesmo recorte, no
# mesmo tamanho, entra no slide seguinte deslocado 1080 px para a esquerda: na troca de slide a emenda some.
PONTE_AREA = (740, 680, 560)  # x, largura, altura (o topo vem do slide: "ponte_topo", padrão 320)


def ponte_html(arq, topo, modo="auto", desloc=0, buracos=False):
    out = arte_posicionada(arq, [PONTE_AREA[0], topo, PONTE_AREA[1], PONTE_AREA[2]], "meio-centro", modo, recorte=True, buracos=buracos,
                           rotulo="Arte · ponte (continua no " + ("slide anterior)" if desloc else "próximo slide)"), classe="arte")
    if desloc:
        out = re.sub(r"left:(-?\d+)px", lambda m: f"left:{int(m.group(1)) - desloc}px", out, count=1)
    return out


def slide(s, M, base, C):
    tipo = s["tipo"]
    img = url(caminho(s.get("imagem"), base))
    ipos = s.get("imagem_pos")
    tema = s.get("tema", "escuro")
    cena = s.get("mistura") in ("cena", "clarear", "multiplicar")
    corpo = ""
    K = paleta(M)
    if tipo == "capa":
        tema = "escuro capa"
        cont = f"<div class='z cont' data-el='Contador'>{html.escape(s['contador'])}</div>" if s.get("contador") else ""
        scr_l = " longa" if len(s.get("script", "")) > 12 else ""
        caixa_l = " longa" if len(s.get("caixa", "")) > 40 else ""
        scr = f"<span class='scr{scr_l}' data-el='Palavra cursiva'>{html.escape(s['script'])}</span>" if s.get("script") else ""
        caixa = f"<div class='z caixa-x{caixa_l}' data-el='Caixa tracejada'>{XIS}<span>{fmt(s['caixa'])}</span>{XIS}</div>" if s.get("caixa") else ""
        nome = html.escape(M.get("nome", "")); assin = html.escape(s.get("assinatura", M.get("profissional", "Jorge Souto")))
        corpo = f"""<div class='bg cartao' data-el='Foto de fundo (cartão)' data-original='{img}' style="background-image:url('{img}');background-position:{ipos or 'center'}"></div><div class='vinheta' data-el='Vinheta (escurecimento)'></div>{cont}
<div class='z tit' data-el='Título' style='top:{s.get('topo', 200)}px'><div class='l1' data-el='Título · linha 1' data-max='900'>{fmt(s.get('linha1',''))}</div><br><div class='l2' data-el='Título · linha 2' data-max='900'>{fmt(s.get('linha2',''))}</div>{scr}</div>
{caixa}<div class='z assin' data-el='Assinatura'>{nome}<em data-el='Divisor da assinatura'></em><b>{assin}</b></div>"""
    elif tipo == "capa2" and s.get("estilo") == "foto":
        # capa B · variante "foto" (2026-10-21): título em 2 linhas só na Anton (2ª linha em degradê),
        # subtítulo logo abaixo, foto inteira num cartão arredondado (sem recorte), etiqueta do cursor no canto do
        # cartão e nota à mão embaixo com a seta. Título: "LINHA 1<br>==LINHA 2==".
        tema = "escuro"
        fy, fh = s.get("foto_topo", 560), s.get("foto_altura", 640)
        cursor = (f"<div class='z cursor-f' data-el='Cursor' style='top:{fy + 18}px'><svg data-el='Seta do cursor' viewBox='0 0 46 52'><defs><linearGradient id='gc' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{K['clara']}'/><stop offset='1' stop-color='{K['media']}'/></linearGradient></defs>"
                  f"<path d='M4 4 L42 22 L24 27 L16 46 Z' fill='url(#gc)'/></svg><span data-el='Nome do cursor'>{html.escape(s['cursor'])}</span></div>") if s.get("cursor") else ""
        nota = ""
        if s.get("nota"):
            nota = ("<svg class='z' data-el='Seta desenhada' style='left:150px;top:" + str(fy + fh - 40) + "px;width:240px;height:150px' viewBox='0 0 240 150' fill='none' stroke='" + K['rgba'](K['preto'], .55) + "' stroke-width='3.2' stroke-linecap='round'>"
                    "<path d='M30 6 C8 60,40 118,120 124 C160 127,190 122,222 112'/><path d='M200 98 L224 111 L203 127'/></svg>"
                    f"<div class='z nota-f' data-el='Nota à mão' style='top:{fy + fh + 30}px'>{fmt(s['nota']).replace(chr(10), '<br>')}</div>")
        corpo = f"""<div class='janela-b' data-el='Janela clara'></div><div class='z ctrl' data-el='Botão minimizar' style='left:84px'>&ndash;</div><div class='z ctrl' data-el='Botão fechar' style='right:84px'>&times;</div>
<div class='z tbf' data-el='Título' style='top:{s.get('topo', 120)}px'><div class='t' data-el='Título · texto' data-max='900'>{fmt(s.get('titulo',''))}</div><div class='sbf' data-el='Subtítulo'>{fmt(s.get('sub',''))}</div></div>
<div class='bg foto-f' data-el='Foto (cartão)' data-original='{img}' style="top:{fy}px;height:{fh}px;background-image:url('{img}');background-position:{ipos or 'center 30%'}"></div>{cursor}{nota}"""
    elif tipo == "capa2":
        tema = "escuro"
        nota = ""
        if s.get("nota"):
            nota = ("<svg class='z' data-el='Seta desenhada' style='left:250px;top:1035px;width:300px;height:230px' viewBox='0 0 300 230' fill='none' stroke='" + K['rgba'](K['preto'], .5) + "' stroke-width='3' stroke-linecap='round'>"
                    "<path d='M70 8 C10 60,20 170,120 195 C170 207,215 205,268 196'/><path d='M244 180 L270 196 L246 212'/></svg>"
                    f"<div class='z nota' data-el='Nota à mão' style='left:560px;top:1110px'>{fmt(s['nota']).replace(chr(10), '<br>')}</div>")
        cursor = ""
        if s.get("cursor"):
            cursor = (f"<div class='z cursor' data-el='Cursor'><svg data-el='Seta do cursor' viewBox='0 0 46 52'><defs><linearGradient id='gc' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='{K['clara']}'/><stop offset='1' stop-color='{K['media']}'/></linearGradient></defs>"
                      f"<path d='M4 4 L42 22 L24 27 L16 46 Z' fill='url(#gc)'/></svg><br><span data-el='Nome do cursor'>{html.escape(s['cursor'])}</span></div>")
        papel = arte(s, base, "imagem", [140, 460, 800, 460], "meio-centro", "Arte · recorte (centro)", modo="borda")
        corpo = f"""<div class='janela-b' data-el='Janela clara'></div><div class='z ctrl' data-el='Botão minimizar' style='left:84px'>&ndash;</div><div class='z ctrl' data-el='Botão fechar' style='right:84px'>&times;</div>
<div class='z tb' data-el='Título'><div class='t' data-el='Título · texto' data-max='900'>{fmt(s.get('titulo',''))}</div></div><div class='z sb' data-el='Subtítulo'>{fmt(s.get('sub',''))}</div>{cursor}
{papel}{nota}"""
    elif tipo == "busca":
        icones = ("<span class='ic' data-el='Ícones da busca'>" + XIS + "<em style='width:1px;height:28px;background:rgba(255,255,255,.3)'></em>"
                  "<svg data-el='Ícone teclado' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><rect x='3' y='6' width='18' height='12' rx='2'/><path d='M7 10h1M11 10h1M15 10h1M8 14h8'/></svg>"
                  "<svg data-el='Ícone microfone' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><rect x='9' y='3' width='6' height='11' rx='3'/><path d='M5 11a7 7 0 0 0 14 0M12 18v3'/></svg>"
                  "<svg data-el='Ícone câmera' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8'><circle cx='12' cy='12' r='4'/><path d='M3 8V5a2 2 0 0 1 2-2h3M16 3h3a2 2 0 0 1 2 2v3M21 16v3a2 2 0 0 1-2 2h-3M8 21H5a2 2 0 0 1-2-2v-3'/></svg>"
                  "<svg data-el='Ícone lupa' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><circle cx='10.5' cy='10.5' r='6.5'/><path d='M20 20l-4.8-4.8'/></svg></span>")
        indice = ""
        if s.get("indice"):
            indice = "<div class='z indice' data-el='Índice (lateral)'>" + "<br>".join((f"<b>{html.escape(x)}</b>" if k == 0 else html.escape(x)) for k, x in enumerate(s["indice"])) + "</div>"
        paras = "".join(f"<p class='{'p1' if k == 0 else 'p2'}' data-el='Parágrafo {k + 1}'>{fmt(p)}</p>" for k, p in enumerate(s.get("texto", [])))
        balao = f"<div class='balao' data-el='Balão de fala' style='margin:6px 0 40px 40px'>{balao_svg()}{fmt(s['balao']).replace(chr(10), '<br>')}</div>" if s.get("balao") else ""
        # figura sangrando embaixo-esquerda (abaixo dos parágrafos; o balão sai da cabeça, por isso "sob") + objeto/quadro sangrando à direita
        figura = arte(s, base, "imagem", [-20, 690, 540, 680], "base-esq", "Arte · figura (recorte)", encaixe=".paras", sob=True)
        # objeto à direita = PONTE: centrado na divisa (x = 1080), metade aqui e metade no slide seguinte
        arq2 = caminho(s.get("imagem2"), base)
        quadro = (ponte_html(arq2, s.get("ponte_topo", 320), s.get("modo_recorte2") or s.get("modo_recorte") or "auto",
                             buracos=bool(s.get("recorte_buracos"))) if arq2 else "")
        corpo = f"""<div class='z busca' data-el='Barra de busca'><span data-el='Texto da busca'>{html.escape(s.get('busca',''))}</span>{icones}</div>{indice}
{figura}{quadro}
<div class='z col' data-el='Bloco de texto' style='left:{s.get('esquerda', 290)}px;right:{360 if s.get('imagem2') else 120}px;top:{s.get('topo', 400)}px'><div class='paras' data-el='Parágrafos'>{paras}</div>{balao}</div>
<div class='z col fecho' data-el='Texto de fecho' style='left:{s.get('fecho_x', 520)}px;right:70px;top:{s.get('fecho_topo', 880)}px'>{fmt(s.get('fecho',''))}</div>"""
    elif tipo in ("lateral", "quadro"):
        paras = "".join(f"<p data-el='Parágrafo {k + 1}' style='font-size:42px;line-height:1.14;margin-bottom:46px'>{fmt(p)}</p>" for k, p in enumerate(s.get("texto", [])))
        # se o slide anterior é a busca com objeto, a arte da esquerda é a outra metade dele (a ponte); senão, a arte do slide
        quadro = (ponte_html(s["_ponte"]["arq"], s["_ponte"]["topo"], s["_ponte"]["modo"], desloc=W, buracos=s["_ponte"]["buracos"]) if s.get("_ponte") else
                  arte(s, base, "imagem", [-70, s.get("imagem_topo", 375), 650, 640], "meio-dir", "Arte · quadro (recorte)"))
        corpo = f"""{quadro}
<div class='z col' data-el='Bloco de texto' style='left:{420 if s.get('_ponte') else 610}px;right:70px;top:{s.get('topo', 470)}px'>{paras}</div>
<svg class='liga' data-el='Colchete de ligação' style='left:830px;top:840px;width:200px;height:290px' viewBox='0 0 200 290' fill='none' stroke='currentColor' stroke-width='2'><path d='M10 7 L158 196 L56 274'/></svg>
<div class='z rod' data-el='Rodapé' style='top:{s.get('rodape_topo', 1030)}px'>{fmt(s.get('rodape',''))}</div>"""
    elif tipo == "vidro":
        topos = s.get("topos", [290, 960])  # cartões em cima e embaixo, a arte entre eles
        larg = s.get("larguras", [540, 720])
        cards = "".join(f"<div class='z vid' data-el='Cartão de vidro {k + 1}' style='top:{topos[k] if k < len(topos) else 355 + 520 * k}px;width:{larg[k] if k < len(larg) else 720}px'><i class='brl' data-el='Brilho do cartão {k + 1}'></i>{fmt(c)}</div>"
                        for k, c in enumerate(s.get("cartoes", [])))
        if cena:
            fundo = cena_inteira(s, base, estilo="filter:brightness(.85)")
        else:
            # mãos/objeto recortado (~900x360) sob os cartões de vidro (o texto passa sobre ela de propósito → "sob")
            fundo = arte(s, base, "imagem", [40, 470, 1000, 520], "meio-centro", "Arte · mãos (recorte)", modo="borda", sob=True)
        corpo = f"{fundo}{cards}"
    elif tipo == "texto":
        nota = ""
        if s.get("nota"):
            nota = (f"<div data-el='Nota' style='display:flex;gap:30px;margin:46px 0 0 120px'><div class='colchete' data-el='Colchete'></div>"
                    f"<div data-el='Texto da nota' style='font-size:29px;line-height:1.26;font-weight:400;max-width:420px'>{fmt(s['nota'])}</div></div>")
        if cena:  # foto inteira escurecida: o texto branco lê em qualquer foto (a nota caía no rosto da pessoa)
            artes = cena_inteira(s, base, estilo=f"filter:brightness({s.get('brilho', .5)})")
        else:
            # dois recortes sangrando: canto superior esquerdo (imagem) e base (imagem2, opcional)
            artes = (arte(s, base, "imagem", [-40, -30, 700, 410], "topo-esq", "Arte · canto superior (recorte)")
                     + arte(s, base, "imagem2", [175, 1110, 840, 290], "base-dir", "Arte · base (recorte)"))
        corpo = f"""{artes}{brilho()}
<div class='z col' data-el='Bloco de texto' style='left:{s.get('esquerda', 210)}px;right:200px;top:{s.get('topo', 440 if s.get('imagem2') or cena else 520)}px'><div data-el='Texto principal' style='font-size:42px;line-height:1.2;max-width:500px'>{fmt(s.get('texto',''))}</div>{nota}</div>"""
    elif tipo == "janela":
        cor_txt = K["rgba"](K["preto"], .55) if tema == "claro" else K["rgba"](K["branco"], .8)
        corpo = f"""{nuvens() if tema == 'claro' else ''}<div class='z jan' data-el='Janela' style='top:{s.get('topo', 450)}px'>
<div class='barra' data-el='Barra da janela'><i data-el='Botão 1' style='background:{K['clara']}'></i><i data-el='Botão 2' style='background:{K['principal']}'></i><i data-el='Botão 3' style='background:{K['profunda']}'></i><span data-el='Título da janela'>{html.escape(s.get('barra',''))}</span><em data-el='Ícone »'>&raquo;</em></div>
<div class='corpo' data-el='Texto da janela'>{fmt(s.get('janela',''))}</div></div>
<div class='z abaixo' data-el='Texto abaixo da janela' style='top:{s.get('texto_topo', 900)}px;color:{cor_txt}'>{fmt(s.get('texto',''))}</div>"""
        if tema == "claro":
            corpo = corpo.replace("<b>", f"<b style='color:{K['rgba'](K['preto'], .75)}'>")
    elif tipo == "pergunta":
        alcas = "".join(f"<i class='h' data-el='Alça de seleção' style='{p}'></i>" for p in ("left:-11px;top:-11px", "right:-11px;top:-11px", "left:-11px;bottom:-11px", "right:-11px;bottom:-11px"))
        cor = K["rgba"](K["preto"], .62) if tema == "claro" else K["branco"]
        corpo = f"""{nuvens(11) if tema == 'claro' else ''}<div class='z sel' data-el='Caixa de seleção' style='top:{s.get('topo', 520)}px;color:{cor}'>{alcas}<div data-el='Texto da pergunta'>{fmt(s.get('texto',''))}</div></div>"""
        if tema == "claro":
            corpo = corpo.replace("<b>", f"<b style='color:{K['rgba'](K['preto'], .78)}'>")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css(K)}</style></head>"
            f"<body class='{tema}'>{corpo}{GRAO_EL}{AJUSTE_JS}{ENCAIXE_JS}</body></html>")
