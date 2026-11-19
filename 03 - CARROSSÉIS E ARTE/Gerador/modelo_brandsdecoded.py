"""Modelo 5 — BrandsDecoded (estilo Moderno: alternado claro/escuro, headline condensada em caixa-alta, corpo em sans
moderna, conteúdo alinhado pela base). Importado por render_carrossel.py quando "modelo": "brandsdecoded".
Especificação visual: inspirada no estilo "Moderno" do método BrandsDecoded (design system do curso:
e brandsdecoded-principios-design.md, material do curso, fora do repositório), com as cores do Souto Treinador (marca.json).

Fontes: Barlow Condensed 900 (headline, títulos, número grande, palavra do CTA) e Plus Jakarta Sans 400–800 (corpo),
pelo Google Fonts. Cores: degradê da marca (marca.json "gradiente"), fundo escuro #0B0B0E, fundo claro #F2F4F8.
A palavra-chave em destaque é SEMPRE em degradê (background-clip:text), nunca azul chapado. No slide grad (fundo já em
degradê) o destaque do TÍTULO vira um degradê quase preto (contraste de texto grande); nas setas e no corpo do grad o destaque
sai em branco forte, como o strong da BD (o validador avisa: no grad, destaque só no título).

JSON (campos extras como "funcao", "afirmacoes", "tipo_carrossel", "funil", "headline" do topo são do validador; aqui
são ignorados):
{
 "modelo": "brandsdecoded", "ficha": "Hipertrofia - Ficha", "tipo_carrossel": "tese", "funil": "topo",
 "headline": "...", "saida": ".",
 "slides": [
  {"tipo": "capa", "imagem": "artes/slide-01.png", "posicao_imagem": "center top",
   "headline": "O FIM DO *TREINO ATÉ A EXAUSTÃO*: O QUE A CIÊNCIA DIZ SOBRE VOLUME"},
  {"tipo": "dark", "tag": "O PROBLEMA", "titulo": "opcional, curto", "texto": ["bloco 1 com **negrito** e *destaque*", "bloco 2"]},
  {"tipo": "light", "tag": "...", "texto": ["..."], "componente": {"tipo": "card", "texto": "..."}},
  {"tipo": "light", "tag": "OS NÚMEROS", "texto": ["..."],
   "componente": {"tipo": "tabela", "cabecalho": ["Indicador", "Número"], "linhas": [["...", "..."], ["...", "..."], ["...", "..."]],
                  "fonte": "fonte simples"}},
  {"tipo": "dark", "tag": "...", "componente": {"tipo": "stat", "valor": "4 → 10", "legenda": "..."}, "texto": ["..."]},
  {"tipo": "dark", "imagem_fundo": "artes/slide-06.png", "texto": ["..."]},
  {"tipo": "light", "imagem": "artes/slide-07.png", "texto": ["..."]},
  {"tipo": "grad", "tag": "A REGRA FINAL", "titulo": "frase de impacto 2–4 palavras", "setas": ["...", "...", "..."]},
  {"tipo": "cta", "ponte": "frase-ponte com **negrito**", "titulo": "QUER AJUDA COM O SEU CASO?",
   "cta": {"tipo": "consultoria", "beneficio": "treino montado para a sua rotina e o seu momento"}}
 ]
}
Tipos de slide: capa · dark · light · grad · cta. Sequência padrão de 9: capa, dark, light, dark, light, dark, light, grad, cta
(nunca 3 seguidos do mesmo fundo; o CTA tem fundo claro).

Componentes ("componente": {...} em dark/light/grad; um por slide):
  card     {"tipo": "card", "texto": "..."}                       destaque/citação num cartão com filete em degradê à esquerda
  tabela   {"tipo": "tabela", "cabecalho": [...], "linhas": [[...], ...], "fonte": "..."}   3+ linhas; 2–3 colunas;
           cabeçalho em faixa de degradê; a última coluna sai em negrito; "fonte" = fonte simples, por extenso
  stat     {"tipo": "stat", "valor": "4 → 10", "legenda": "..."}  número protagonista (200 px, encolhe se passar da largura)
  setas    {"tipo": "setas", "itens": ["...", "..."]}             2–4 pontos em sequência (também aceito como "setas" no slide)
  cards    {"tipo": "cards", "itens": [{"titulo": "...", "texto": "..."}, ...]}   2–3 cartões numerados (01, 02, 03)
Imagens nos slides internos (opcionais):
  "imagem"       = caixa de imagem (img-box) no topo do conteúdo: 100% da largura x 360 px, cantos de 20 px, cover.
                   Só quando o slide tem espaço sobrando (texto ocupa < 60% da área). Ajuste: "posicao_imagem" (object-position).
  "imagem_fundo" = SÓ em dark: foto de fundo inteira com véu escuro de 70–92% (texto sempre legível). Ajuste: "posicao_fundo".
Ordem dentro do conteúdo: caixa de imagem → tag → título → número grande (stat) → texto → componente → setas.
Hierarquia de 3 níveis: título (ou o 1º bloco, quando não há título) = âncora; corpo = contexto; tag/brand bar/progresso = metadata.
Sem título e com 2 blocos, o 1º bloco sai maior e mais forte (abre o slide) e o 2º no corpo normal.

CTA ("cta.tipo") pelo conteúdo:
  consultoria  (padrão) caixa "Consultoria individualizada" + "LINK NA BIO" + "beneficio" (opcional); rodapé
               "<profissional> · <profissao> · <registro>" do marca.json (ex.: "Jorge Souto · treinador · CREF ...")
  ebook        (material gratuito/pago do Jorge, se existir) caixa "E-book" + "LINK NA BIO" + "beneficio" (opcional); rodapé = o @
  palavra / salvar  saíram em 2026-10-15 (o gerador ainda desenha, só para peças antigas; o validador avisa)
  A frase-ponte ("ponte") é obrigatória no BD: liga o último insight ao CTA. Layout à esquerda, sem seta de arraste.
  Título do CTA a 72 px e chamada da caixa a 80 px (a caixa é a âncora). A chamada da caixa já sai em degradê e conta nas
  3 palavras de destaque do slide: em consultoria e ebook ("LINK NA BIO") o título fica sem *destaque*.
  O "cta" deste slide é o que vai para a arte e tem de ser igual ao "cta" do topo do JSON (o validador confere).

Marcação: **negrito** (strong) · *destaque* (palavra-chave em degradê; no máximo 3 palavras por slide) · <br> (ou \\n).
Títulos e headline vão em caixa-alta (o CSS força).

Elementos fixos em todos os slides: barra de destaque no topo (7 px, degradê; no grad, branco translúcido), barra da marca
(assinatura | @ | registro do marca.json, 14 px: JORGE SOUTO · TREINADOR | @... | CREF ...), barra de progresso no rodapé (trilho de 3 px,
preenchimento proporcional ao slide e contador N/total) e número decorativo grande no fundo dos slides dark e grad.
O índice do slide vem do render (s["_n"], s["_total"]); sem eles, é procurado em C["slides"].

Capa: foto cheia (cover) + degradê preto forte na base; selo do @ (bolinha em degradê com o logo da marca + o @) acima
da headline; headline Barlow Condensed 900 caixa-alta a 108 px (entrelinha 0,98, para o acento não encostar na linha de cima;
quebra equilibrada, text-wrap: balance), encolhe de 2 em 2 até 88 px para ficar em até 4 linhas (no mínimo de 88 px aceita 5). Se não couber em 5 linhas a 88 px, a verificação acusa "texto não coube … headline longa:
use a versão curta mantendo o padrão". Bloco ancorado a 120 px da base. Sem badge de tipo nem data.
Slides internos: conteúdo ancorado pela base (120 px da borda = 80 de margem + 40 de respiro, nunca encosta na progress
bar), margens laterais de 56 px, texto à esquerda. Se o conteúdo passar da área (de 110 px do topo até a base), a caixa
de imagem encolhe até 260 px e depois o corpo até 32 px (card, setas, legenda do número, cartões e tabela encolhem junto:
o tamanho deles é amarrado ao do corpo, --fc); se nem assim couber, a verificação acusa "texto não coube". Nos slides dark e
light, o ajuste grava em data-preench quanto da área o conteúdo ocupa: abaixo de 50%, sem imagem, o render dá um AVISO (não
bloqueia) sugerindo caixa de imagem ou card.

O QUE PEDIR AO GOOGLE FLOW (foto realista/ultrarrealista, estética Tumblr, conceitual, sóbria e clean, sem texto na imagem,
sem anime/3D):
  capa          foto realista conceitual 4:5 (1080x1350 ou 2K), cena cheia, sujeito/rosto no TERÇO SUPERIOR, metade de baixo
                mais simples e escura (a headline entra sobre o degradê preto). Gancho visual forte do tema. Pessoas e rostos
                funcionam bem. Sem recorte.
  imagem        (img-box) foto 16:9 ou 3:2, sujeito no centro e com folga em cima e embaixo (a caixa corta para ~2,7:1).
  imagem_fundo  foto 4:5 escura (low-key), pouca informação no terço inferior; vai sob véu escuro de 70–92%.

Todo elemento visível tem data-el="Nome em português" (o editor visual lista e edita cada um). A barra da marca (.cab), o
número decorativo (.num) e a barra de progresso (data-livre) ficam fora da checagem de fonte pequena/sobreposição: são
moldura fixa, com tamanho do design system.
"""
import html
import os
import re

from comum import caminho, url

W, H = 1080, 1350
AQUI = os.path.dirname(os.path.abspath(__file__))
REGISTRO = "CREF 000000-G/UF"  # só se o marca.json não tiver "registro" (o valor certo fica lá)
NB = chr(0xA0)  # espaço inquebrável
TOPO_CONTEUDO, BASE_CONTEUDO = 110, 120  # área útil do conteúdo: de 110 px do topo até 120 px da base
CAPA_LH, CAPA_MAX, CAPA_MIN = 0.98, 108, 88
FONTES = ("@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900"
          "&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap');")


# ───────────────────────── texto ─────────────────────────

def sem_orfas(t):
    """Espaço inquebrável onde a quebra fica feia: número + palavra curta ("1 em 263"), palavra curta + número, palavra
    de 1 letra + a seguinte ("o exame") e a última palavra de cada linha (evita uma palavra sozinha na última linha)."""
    t = re.sub(r"(?<=\d) (?=\w{1,3}\b)", NB, t)
    t = re.sub(r"(?<!\w)(\w{1,2}) (?=\d)", r"\1" + NB, t)
    t = re.sub(r"(?<![\w&;])(\w) (?=\S)", r"\1" + NB, t)  # a, o, e, é não ficam sozinhos no fim da linha
    t = re.sub(r" (?=\(\w{1,3}\))", NB, t)  # parêntese curto ("(a)", "(HF)") não começa linha sozinho
    return "&lt;br&gt;".join(re.sub(r" (?=\S+\s*$)", NB, parte) for parte in t.split("&lt;br&gt;"))


def fmt(t):
    """**negrito** → <strong> · *destaque* → palavra-chave em degradê · <br> ou \\n → quebra."""
    t = html.escape(str(t or "")).replace("\n", "&lt;br&gt;")
    t = re.sub(r"&lt;br\s*/?&gt;", "&lt;br&gt;", t)
    t = sem_orfas(t).replace("&lt;br&gt;", "<br>")
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(?!\s)(.+?)(?<!\s)\*", r"<em class='dest'>\1</em>", t)
    return t


def esc(t):
    return html.escape(str(t or ""), quote=True)


def blocos(v):
    if not v:
        return []
    return [x for x in (v if isinstance(v, list) else [v]) if str(x).strip()]


# ───────────────────────── estilo ─────────────────────────

def _rgba(hexa, al):
    hexa = hexa.lstrip("#")
    return "rgba(%d,%d,%d,%s)" % (int(hexa[0:2], 16), int(hexa[2:4], 16), int(hexa[4:6], 16), al)


def _escurecer(hexa, k):
    hexa = hexa.lstrip("#")
    r, g, b = (int(hexa[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02X%02X%02X" % (round(r * (1 - k)), round(g * (1 - k)), round(b * (1 - k)))


def cores(M):
    pal = M.get("paleta", {})
    P = M.get("cor_destaque", "#2E49CE")
    PL = pal.get("clara", "#445DB4")
    PM = pal.get("media", "#1F33A3")
    PD = pal.get("profunda", "#141A3D")
    LB, DB = M.get("fundo_claro", "#F2F4F8"), M.get("fundo_escuro", "#0B0B0E")
    return {
        "P": P, "PL": PL, "PM": PM, "PD": PD, "LB": LB, "DB": DB, "LR": _escurecer(LB, 0.06),
        "G": M.get("gradiente", f"linear-gradient(100deg, {PL} 0%, {P} 48%, {PM} 100%)"),
        # texto em degradê sobre fundo escuro (capa, dark): a versão clara do azul (o tom escuro some no preto)
        "GD": M.get("gradiente_escuro") or M.get("gradiente", f"linear-gradient(100deg, {PL} 0%, {P} 48%, {PM} 100%)"),
        # slide grad: claro no alto, escuro embaixo (o texto fica sobre a parte mais escura = mais contraste)
        "GS": f"linear-gradient(165deg, {PL} 0%, {P} 36%, {PM} 70%, {PD} 100%)",
        "GV": f"linear-gradient(180deg, {PL} 0%, {P} 50%, {PD} 100%)",  # filete vertical dos cards
        "GT": f"linear-gradient(100deg, {P} 0%, {PM} 60%, {PD} 100%)",  # faixa do cabeçalho da tabela (branco legível)
        "GE": f"linear-gradient(100deg, {DB} 0%, {PD} 100%)",  # destaque do título no slide grad (escuro sobre o azul)
    }


def css(K):
    return f"""{FONTES}
:root{{--GD:{K['GD']};--P:{K['P']};--PL:{K['PL']};--PD:{K['PD']};--LB:{K['LB']};--LR:{K['LR']};--DB:{K['DB']};--G:{K['G']};--GS:{K['GS']};
--FH:'Barlow Condensed',sans-serif;--FB:'Plus Jakarta Sans',sans-serif}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{position:relative;font-family:var(--FB);-webkit-font-smoothing:antialiased;--fc:38px}}
body.capa{{background:#000}} body.dark{{background:var(--DB)}} body.light,body.cta{{background:var(--LB)}} body.grad{{background:var(--GS)}}
strong{{font-weight:700}}
em.dest{{font-style:normal;font-weight:800;background:var(--G);-webkit-background-clip:text;background-clip:text;color:transparent;
-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.dark em.dest,.capa em.dest{{background:var(--GD);-webkit-background-clip:text;background-clip:text}}
.grad em.dest{{background:none;color:#fff;font-weight:800}}
.grad .tit em.dest{{background:{K['GE']};-webkit-background-clip:text;background-clip:text;color:transparent}}
.gt{{background:var(--G);-webkit-background-clip:text;background-clip:text;color:transparent}}
/* elementos fixos */
.accent{{position:absolute;top:0;left:0;right:0;height:7px;z-index:30;background:var(--G)}}
.grad .accent{{background:rgba(255,255,255,.18)}}
.cab{{position:absolute;top:7px;left:0;right:0;padding:32px 56px 0;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;z-index:20;
font:700 14px/1 var(--FB);letter-spacing:1.5px;text-transform:uppercase}}
.cab span:first-child{{justify-self:start}} .cab .arroba{{justify-self:center}} .cab span:last-child{{justify-self:end}}
.cab .arroba{{text-transform:none;letter-spacing:.8px}}
.light .cab,.cta .cab{{color:rgba(15,13,12,.45)}} .dark .cab{{color:rgba(255,255,255,.45)}} .grad .cab{{color:rgba(255,255,255,.62)}}
.capa .cab{{color:rgba(255,255,255,.78);text-shadow:0 1px 8px rgba(0,0,0,.35)}}
.prog{{position:absolute;bottom:0;left:0;right:0;padding:0 56px 30px;z-index:20;display:flex;align-items:center;gap:16px}}
.prog .trilho{{flex:1;height:3px;border-radius:2px;overflow:hidden}}
.prog .cheio{{height:100%;border-radius:2px}}
.prog .cont{{font:600 15px/1 var(--FB);letter-spacing:.5px}}
.light .trilho,.cta .trilho{{background:rgba(0,0,0,.08)}} .light .cheio,.cta .cheio{{background:var(--G)}} .light .cont,.cta .cont{{color:rgba(0,0,0,.32)}}
.dark .trilho,.capa .trilho{{background:rgba(255,255,255,.12)}} .dark .cheio,.capa .cheio{{background:#fff}} .dark .cont,.capa .cont{{color:rgba(255,255,255,.34)}}
.grad .trilho{{background:rgba(255,255,255,.18)}} .grad .cheio{{background:rgba(255,255,255,.7)}} .grad .cont{{color:rgba(255,255,255,.5)}}
.num{{position:absolute;right:-10px;bottom:50px;z-index:1;font:900 380px/1 var(--FH);letter-spacing:-14px;color:rgba(255,255,255,.04);pointer-events:none;white-space:nowrap}}
.grad .num{{right:-15px;bottom:40px;font-size:420px;letter-spacing:-16px;color:rgba(255,255,255,.05)}}
/* fotos */
.capa-bg,.bgimg{{position:absolute;inset:0;background-size:cover;background-position:center;background-repeat:no-repeat;z-index:0}}
.capa-sem{{background:radial-gradient(ellipse 80% 60% at 50% 30%,#262a33,#0b0b0e)}}
.capa-grad{{position:absolute;inset:0;z-index:1;background:linear-gradient(to bottom,rgba(0,0,0,.35) 0%,rgba(0,0,0,.08) 25%,rgba(0,0,0,.15) 40%,
rgba(0,0,0,.65) 55%,rgba(0,0,0,.92) 75%,rgba(0,0,0,.99) 100%)}}
.veu{{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(11,11,12,.80) 0%,rgba(11,11,12,.70) 30%,rgba(11,11,12,.76) 60%,rgba(11,11,12,.92) 100%)}}
/* capa */
.capa-area{{position:absolute;left:56px;right:56px;bottom:{BASE_CONTEUDO}px;z-index:10}}
.selo{{display:flex;align-items:center;gap:14px;width:fit-content;margin-bottom:32px;padding:12px 26px 12px 14px;border-radius:60px;
background:rgba(0,0,0,.38);border:1.5px solid rgba(255,255,255,.12);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}}
.dot{{width:40px;height:40px;border-radius:50%;background:var(--G);display:flex;align-items:center;justify-content:center;overflow:hidden;flex:none}}
.dot img{{width:30px;height:30px;object-fit:contain;display:block}}
.dot b{{font:800 15px/1 var(--FB);color:#fff}}
.selo-arroba{{font:700 22px/1 var(--FB);color:#fff;letter-spacing:.3px}}
.hl{{font:900 {CAPA_MAX}px/{CAPA_LH} var(--FH);letter-spacing:-.028em;text-transform:uppercase;color:#fff;text-wrap:balance}}
.hl em.dest,.tit em.dest,.cta-tit em.dest{{font-weight:inherit}}
/* conteúdo dos slides internos */
.conteudo{{position:absolute;left:56px;right:56px;bottom:{BASE_CONTEUDO}px;z-index:10}}
.tag{{width:fit-content;font:700 18px/1.25 var(--FB);letter-spacing:3px;text-transform:uppercase;margin-bottom:24px}}
.dark .tag{{background:var(--GD);-webkit-background-clip:text;background-clip:text;color:transparent}}
.light .tag,.cta .tag{{background:linear-gradient(100deg,var(--P),var(--PD));-webkit-background-clip:text;background-clip:text;color:transparent}}
.grad .tag{{color:rgba(255,255,255,.85)}}
.tit{{font:900 80px/1 var(--FH);letter-spacing:-.025em;text-transform:uppercase;margin-bottom:36px;text-wrap:balance}}
.dark .tit{{color:#fff}} .grad .tit{{color:#fff;margin-bottom:40px}}
.light .tit{{font-size:72px;line-height:1;letter-spacing:-.021em;color:var(--DB);margin-bottom:32px}}
.corpo{{font-size:var(--fc);font-weight:400;line-height:1.5;letter-spacing:-.2px}}
.corpo+.corpo{{margin-top:30px}}
.dark .corpo{{color:rgba(255,255,255,.58)}} .dark .corpo strong{{color:#fff;font-weight:700}}
.light .corpo{{line-height:1.55;color:rgba(15,13,12,.62)}} .light .corpo strong{{color:var(--DB);font-weight:800}}
.grad .corpo{{line-height:1.55;color:rgba(255,255,255,.84)}} .grad .corpo strong{{color:#fff;font-weight:800}}
.corpo.lead{{font-size:calc(var(--fc) + 6px);font-weight:500;line-height:1.36;letter-spacing:-.4px}}
.dark .corpo.lead{{color:rgba(255,255,255,.88)}} .light .corpo.lead{{color:rgba(15,13,12,.86)}} .grad .corpo.lead{{color:#fff}}
.comp{{margin-top:40px}} .comp:first-child{{margin-top:0}}
.tag+.comp,.tit+.comp{{margin-top:0}}
/* caixa de imagem */
.img-box{{width:100%;height:360px;border-radius:20px;overflow:hidden;margin-bottom:40px}}
.img-box img{{width:100%;height:100%;object-fit:cover;display:block}}
.dark .img-box{{border:1.5px solid rgba(255,255,255,.08)}} .light .img-box{{box-shadow:0 4px 24px rgba(0,0,0,.06)}}
/* número grande */
.stat{{width:fit-content;white-space:nowrap;font:900 200px/1 var(--FH);letter-spacing:-.012em;padding:.12em .04em 0 0;margin:-.12em 0 -4px;
background:var(--G);-webkit-background-clip:text;background-clip:text;color:transparent}}
.stat-leg{{font:600 32px/1.3 var(--FB);font-size:calc(var(--fc) - 6px);letter-spacing:-.2px;margin-bottom:44px}} .stat-leg:last-child{{margin-bottom:0}}
.dark .stat-leg{{color:rgba(255,255,255,.72)}} .light .stat-leg{{color:rgba(15,13,12,.72)}} .grad .stat-leg{{color:rgba(255,255,255,.9)}}
.grad .stat{{background:none;color:#fff}}
.dark .stat,.dark .pc-n{{background:var(--GD);-webkit-background-clip:text;background-clip:text}}
/* card */
.card{{border-radius:16px;padding:44px 48px 44px 54px;background:{K['GV']} left top/6px 100% no-repeat,rgba(255,255,255,.05)}}
.light .card{{border-radius:18px;padding:52px 56px 52px 63px;background:{K['GV']} left top/7px 100% no-repeat,#fff;box-shadow:0 4px 24px rgba(0,0,0,.05)}}
.grad .card{{background:linear-gradient(#fff,#fff) left top/6px 100% no-repeat,rgba(255,255,255,.12)}}
.card-t{{font:600 36px/1.45 var(--FB);font-size:var(--fc);letter-spacing:-.3px}}
.dark .card-t{{color:rgba(255,255,255,.88)}} .dark .card-t strong{{color:#fff;font-weight:800}}
.light .card-t{{color:rgba(15,13,12,.82)}} .light .card-t strong{{color:var(--DB);font-weight:800}}
.grad .card-t{{color:#fff}}
/* tabela */
.tabela{{border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 4px 24px rgba(0,0,0,.05)}}
.tab-cab{{display:flex;background:{K['GT']};color:#fff}}
.tab-cab>div{{padding:20px 28px;font:700 18px/1.25 var(--FB);letter-spacing:2px;text-transform:uppercase}}
.tab-lin{{display:flex;border-top:1px solid var(--LR)}} .tab-cab+.tab-lin{{border-top:none}}
.tab-lin>div{{padding:22px 28px;font:500 28px/1.35 var(--FB);font-size:calc(var(--fc) - 10px);color:rgba(15,13,12,.7)}}
.tab-lin>div:last-child{{font-weight:800;color:var(--DB)}}
.tabela .c1{{flex:1.3 1 0}} .tabela .cn{{flex:1 1 0}}
.dark .tabela{{background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.08);box-shadow:none}}
.dark .tab-lin{{border-top-color:rgba(255,255,255,.08)}} .dark .tab-lin>div{{color:rgba(255,255,255,.66)}} .dark .tab-lin>div:last-child{{color:#fff}}
.fonte{{margin-top:16px;font:italic 500 18px/1.4 var(--FB);color:rgba(15,13,12,.5)}}
.dark .fonte,.grad .fonte{{color:rgba(255,255,255,.5)}}
/* setas */
.seta{{display:flex;align-items:flex-start;gap:22px;margin-bottom:30px}} .seta:last-child{{margin-bottom:0}}
.seta svg{{flex:none;width:36px;height:36px;margin-top:6px}}
.seta .st{{font:500 34px/1.42 var(--FB);font-size:calc(var(--fc) - 4px);letter-spacing:-.2px}}
.dark .st{{color:rgba(255,255,255,.74)}} .dark .st strong{{color:#fff;font-weight:800}}
.light .st{{color:rgba(15,13,12,.7)}} .light .st strong{{color:var(--DB);font-weight:800}}
.grad .st{{font-size:calc(var(--fc) - 6px);line-height:1.45;color:rgba(255,255,255,.88)}} .grad .st strong{{color:#fff;font-weight:800}}
/* cartões numerados */
.pc{{border-radius:18px;padding:34px 44px;margin-bottom:20px}} .pc:last-child{{margin-bottom:0}}
.light .pc{{background:#fff;border:1.5px solid var(--LR)}} .dark .pc{{background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.09)}}
.grad .pc{{background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.2)}}
.pc-n{{width:fit-content;font:800 18px/1 var(--FB);letter-spacing:3px;margin-bottom:14px;background:var(--G);-webkit-background-clip:text;background-clip:text;color:transparent}}
.grad .pc-n{{background:none;color:rgba(255,255,255,.75)}}
.pc-t{{font:800 32px/1.2 var(--FB);font-size:calc(var(--fc) - 6px);letter-spacing:-.3px;margin-bottom:10px}}
.pc-x{{font:400 26px/1.45 var(--FB);font-size:calc(var(--fc) - 12px)}}
.light .pc-t{{color:var(--DB)}} .light .pc-x{{color:rgba(15,13,12,.62)}} .light .pc-x strong{{color:var(--DB);font-weight:800}}
.dark .pc-t,.grad .pc-t{{color:#fff}} .dark .pc-x{{color:rgba(255,255,255,.62)}} .grad .pc-x{{color:rgba(255,255,255,.85)}}
.dark .pc-x strong,.grad .pc-x strong{{color:#fff}}
/* CTA */
.ponte{{font:500 var(--fc)/1.5 var(--FB);letter-spacing:-.2px;color:rgba(15,13,12,.58);margin-bottom:44px}}
.ponte strong{{color:var(--DB);font-weight:800}}
.cta-tit{{font:900 72px/1 var(--FH);letter-spacing:-.025em;text-transform:uppercase;color:var(--DB);margin-bottom:40px;text-wrap:balance}}
.kbox{{background:#fff;border:3px solid {_rgba(K['P'], .18)};border-radius:20px;padding:40px 48px;margin-bottom:34px}}
.k-ic{{display:flex;gap:18px;margin-bottom:18px}} .k-ic svg{{width:52px;height:52px}}
.k-instr{{font:500 20px/1.3 var(--FB);color:rgba(15,13,12,.56);margin-bottom:12px}}
.k-pal{{width:fit-content;white-space:nowrap;font:900 80px/1 var(--FH);letter-spacing:-.025em;padding:.12em .03em 0 0;margin:-.12em 0 14px;text-transform:uppercase;
background:var(--G);-webkit-background-clip:text;background-clip:text;color:transparent}}
.k-ben{{font:500 22px/1.5 var(--FB);color:rgba(15,13,12,.58)}}
.k-ben strong{{color:var(--DB);font-weight:800}}
.cta-rod{{display:flex;align-items:center;gap:16px}}
.cta-rod span{{font:500 18px/1.3 var(--FB);color:rgba(15,13,12,.5)}}
"""


# Encaixe automático (roda antes da verificação do render): headline da capa, número grande/palavra do CTA e altura do conteúdo.
# O editor visual tira o data-fith quando o tamanho da fonte é mudado à mão; daí em diante o ajuste respeita a escolha.
AJUSTE_M5_JS = f"""<script>
(document.fonts ? document.fonts.ready : Promise.resolve()).then(function(){{
  document.querySelectorAll('.hl[data-fith]').forEach(function(el){{
    var s = {CAPA_MAX}, lh = {CAPA_LH};
    function linhas(){{ return Math.round(el.getBoundingClientRect().height / (s * lh)); }}
    el.style.fontSize = s + 'px';
    while (s > {CAPA_MIN} && (linhas() > 4 || el.scrollWidth > el.clientWidth + 1)) {{ s -= 2; el.style.fontSize = s + 'px'; }}
  }});
  document.querySelectorAll('[data-maxw]').forEach(function(el){{
    var max = el.parentElement.clientWidth, s = parseFloat(getComputedStyle(el).fontSize), min = +el.dataset.maxw;
    while (el.getBoundingClientRect().width > max && s > min) {{ s -= 4; el.style.fontSize = s + 'px'; }}
  }});
  document.querySelectorAll('.conteudo[data-fith]').forEach(function(el){{
    var max = +el.dataset.fith, box = el.querySelector('.img-box'), fc = 38, k = 0;
    while (el.scrollHeight > max && k++ < 80) {{
      if (box && box.offsetHeight > 260) {{ box.style.height = (box.offsetHeight - 10) + 'px'; continue; }}
      if (fc > 32) {{ fc -= 1; el.style.setProperty('--fc', fc + 'px'); continue; }}
      break;
    }}
    // quanto da área útil o conteúdo ocupa (só dark/light): o render avisa abaixo de 50% (BD: sugerir imagem ou card)
    if (document.body.classList.contains('dark') || document.body.classList.contains('light'))
      el.dataset.preench = Math.round(100 * el.scrollHeight / max);
  }});
  document.body.classList.add('pronto');
}});
</script>"""


# ───────────────────────── peças ─────────────────────────

def _defs(K):
    """Degradê da marca para os ícones em SVG (setas, ícones do CTA)."""
    return (f"<svg data-el='Degradê dos ícones (definição)' width='0' height='0' style='position:absolute'><defs>"
            f"<linearGradient id='gm' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='{K['PL']}'/>"
            f"<stop offset='.5' stop-color='{K['P']}'/><stop offset='1' stop-color='{K['PD']}'/></linearGradient></defs></svg>")


def _logo(M):
    lg = M.get("logo")
    if lg:
        p = lg if os.path.isabs(lg) else os.path.join(AQUI, lg)
        if os.path.exists(p):
            return f"<img data-el='Logo' src='{url(p)}' alt=''>"
    return f"<b data-el='Logo (texto)'>{esc((M.get('profissional') or 'S')[:1])}</b>"


def _fixos(M, tipo, n, total):
    nome = esc(M.get("assinatura", "JORGE SOUTO · TREINADOR"))
    arroba = esc(M.get("nome", ""))
    reg = esc(M.get("registro", REGISTRO))
    pct = max(0, min(100, round(100 * n / max(1, total), 2)))
    out = ("<div class='accent' data-el='Barra de destaque (topo)'></div>"
           f"<div class='cab' data-el='Barra da marca'><span data-el='Barra da marca · nome'>{nome}</span>"
           f"<span class='arroba' data-el='Barra da marca · @'>{arroba}</span><span data-el='Barra da marca · registro'>{reg}</span></div>"
           f"<div class='prog' data-livre='1' data-el='Barra de progresso'><div class='trilho' data-el='Progresso · trilho'>"
           f"<div class='cheio' data-el='Progresso · preenchimento' style='width:{pct}%'></div></div>"
           f"<span class='cont' data-el='Progresso · contador'>{n}/{total}</span></div>")
    if tipo in ("dark", "grad"):
        out += f"<div class='num' data-el='Número decorativo'>{n:02d}</div>"
    return out


def _seta_svg(k, grad):
    cor = "rgba(255,255,255,.6)" if grad else "url(#gm)"
    return (f"<svg data-el='Seta {k} · ícone' viewBox='0 0 36 36' fill='none' stroke='{cor}' stroke-width='3.2' stroke-linecap='round' "
            f"stroke-linejoin='round'><path d='M5 18h24M20 9l9 9-9 9'/></svg>")


def _setas(itens, grad, rotulo="Setas"):
    linhas = "".join(f"<div class='seta' data-el='Seta {k}'>{_seta_svg(k, grad)}<div class='st' data-el='Seta {k} · texto'>{fmt(x)}</div></div>"
                     for k, x in enumerate(blocos(itens), 1))
    return f"<div class='comp setas' data-el='{rotulo}'>{linhas}</div>" if linhas else ""


def _tabela(c):
    cab = c.get("cabecalho") or []
    linhas = [l if isinstance(l, list) else [l] for l in (c.get("linhas") or [])]
    ncol = max([len(cab)] + [len(l) for l in linhas] + [1])

    def cel(v, j, rot):
        return f"<div class='{'c1' if j == 0 else 'cn'}' data-el='{rot} · coluna {j + 1}'>{fmt(v)}</div>"
    out = ""
    if cab:
        out += "<div class='tab-cab' data-el='Tabela · cabeçalho'>" + "".join(cel(cab[j] if j < len(cab) else "", j, "Tabela · cabeçalho") for j in range(ncol)) + "</div>"
    for i, l in enumerate(linhas, 1):
        out += f"<div class='tab-lin' data-el='Tabela · linha {i}'>" + "".join(cel(l[j] if j < len(l) else "", j, f"Tabela · linha {i}") for j in range(ncol)) + "</div>"
    fonte = f"<div class='fonte' data-el='Tabela · fonte'>Fonte: {fmt(c['fonte'])}</div>" if c.get("fonte") else ""
    return f"<div class='comp' data-el='Tabela (bloco)'><div class='tabela' data-el='Tabela'>{out}</div>{fonte}</div>"


def _cards(itens):
    out = ""
    for k, it in enumerate(itens or [], 1):
        if isinstance(it, str):
            it = {"texto": it}
        tit = f"<div class='pc-t' data-el='Cartão {k} · título'>{fmt(it.get('titulo'))}</div>" if it.get("titulo") else ""
        tx = f"<div class='pc-x' data-el='Cartão {k} · texto'>{fmt(it.get('texto'))}</div>" if it.get("texto") else ""
        out += f"<div class='pc' data-el='Cartão {k}'><div class='pc-n' data-el='Cartão {k} · número'>{k:02d}</div>{tit}{tx}</div>"
    return f"<div class='comp pcards' data-el='Cartões numerados'>{out}</div>" if out else ""


def _componente(c, tipo_slide):
    if not isinstance(c, dict):
        return ""
    t = c.get("tipo")
    if t == "card":
        return f"<div class='comp card' data-el='Card'><div class='card-t' data-el='Card · texto'>{fmt(c.get('texto'))}</div></div>"
    if t == "tabela":
        return _tabela(c)
    if t == "setas":
        return _setas(c.get("itens"), tipo_slide == "grad")
    if t == "cards":
        return _cards(c.get("itens"))
    return ""  # stat é montado à parte (vem antes do texto)


def _indice(s, C):
    n, total = s.get("_n"), s.get("_total")
    slides = (C or {}).get("slides") or []
    if not n:
        limpo = {k: v for k, v in s.items() if not k.startswith("_")}
        n = next((k for k, x in enumerate(slides, 1) if x is s or x == limpo), 1)
    return n, total or max(len(slides), n)


# ───────────────────────── slides ─────────────────────────

def _capa(s, M, base):
    arq = caminho(s.get("imagem"), base)
    if arq:
        fundo = (f"<div class='capa-bg' data-el='Foto de fundo (capa)' data-original='{url(arq)}' "
                 f"style=\"background-image:url('{url(arq)}');background-position:{esc(s.get('posicao_imagem') or 'center')}\"></div>")
    else:
        fundo = "<div class='capa-bg capa-sem' data-el='Fundo da capa (sem foto)'></div>"
    # 5 linhas a 88 px + a sobra da última linha (o glifo da Barlow passa um pouco da caixa da linha e entra no scrollHeight)
    fith = int(5 * CAPA_MIN * CAPA_LH + 0.14 * CAPA_MIN) + 2
    return (f"{fundo}<div class='capa-grad' data-el='Degradê da capa'></div>"
            f"<div class='capa-area' data-el='Bloco da capa'>"
            f"<div class='selo' data-el='Selo do @'><div class='dot' data-el='Selo · bolinha'>{_logo(M)}</div>"
            f"<span class='selo-arroba' data-el='Selo · @'>{esc(M.get('nome', ''))}</span></div>"
            f"<div class='hl' data-el='Headline' data-fith='{fith}' data-dica='headline longa: use a versão curta mantendo o padrão'>"
            f"{fmt(s.get('headline') or s.get('titulo'))}</div></div>")


def _interno(s, base, tipo):
    partes = []
    img = caminho(s.get("imagem"), base)
    if img:
        partes.append(f"<div class='img-box' data-el='Caixa de imagem'><img data-el='Imagem' data-original='{url(img)}' src='{url(img)}' "
                      f"style='object-position:{esc(s.get('posicao_imagem') or 'center')}' alt=''></div>")
    if s.get("tag"):
        partes.append(f"<div class='tag' data-el='Tag'>{fmt(s['tag'])}</div>")
    if s.get("titulo"):
        partes.append(f"<div class='tit' data-el='Título'>{fmt(s['titulo'])}</div>")
    comp = s.get("componente") if isinstance(s.get("componente"), dict) else {}
    stat = comp.get("tipo") == "stat"
    if stat:
        partes.append(f"<div class='stat' data-el='Número grande' data-maxw='96'>{fmt(comp.get('valor'))}</div>")
        if comp.get("legenda"):
            partes.append(f"<div class='stat-leg' data-el='Legenda do número'>{fmt(comp['legenda'])}</div>")
    txt = blocos(s.get("texto"))
    lead = not s.get("titulo") and not stat and len(txt) >= 2
    for k, b in enumerate(txt, 1):
        partes.append(f"<p class='corpo{' lead' if lead and k == 1 else ''}' data-el='Texto · bloco {k}'>{fmt(b)}</p>")
    if not stat:
        partes.append(_componente(comp, tipo))
    if s.get("setas"):
        partes.append(_setas(s["setas"], tipo == "grad"))
    fundo = ""
    if tipo == "dark" and s.get("imagem_fundo"):
        arq = caminho(s["imagem_fundo"], base)
        fundo = (f"<div class='bgimg' data-el='Foto de fundo' data-original='{url(arq)}' style=\"background-image:url('{url(arq)}');"
                 f"background-position:{esc(s.get('posicao_fundo') or 'center')}\"></div><div class='veu' data-el='Véu escuro (sobre a foto)'></div>")
    alt = H - TOPO_CONTEUDO - BASE_CONTEUDO
    return fundo, (f"<div class='conteudo' data-el='Conteúdo' data-fith='{alt}' data-dica='corte o texto, tire a imagem ou troque o componente'>"
                   + "".join(p for p in partes if p) + "</div>")


def _cta(s, M):
    c = s.get("cta") if isinstance(s.get("cta"), dict) else {}
    tipo = c.get("tipo") or "consultoria"  # CTA pelo conteúdo: consultoria (padrão) ou ebook (material do Jorge)
    partes = []
    if s.get("tag"):
        partes.append(f"<div class='tag' data-el='Tag'>{fmt(s['tag'])}</div>")
    if s.get("ponte"):
        partes.append(f"<div class='ponte' data-el='Frase-ponte'>{fmt(s['ponte'])}</div>")
    if s.get("titulo"):
        partes.append(f"<div class='cta-tit' data-el='Título do CTA'>{fmt(s['titulo'])}</div>")
    caixa, rodape = "", ""
    arroba = esc(M.get("nome", ""))
    if tipo == "ebook":
        instr = c.get("instrucao") or "E-book"
        caixa = (f"<div class='k-instr' data-el='CTA · instrução'>{fmt(instr)}</div>"
                 f"<div class='k-pal' data-el='CTA · chamada' data-maxw='48'>{fmt(c.get('palavra') or 'LINK NA BIO')}</div>")
        rodape = arroba
    elif tipo == "consultoria":
        instr = c.get("instrucao") or "Consultoria individualizada"
        caixa = (f"<div class='k-instr' data-el='CTA · instrução'>{fmt(instr)}</div>"
                 f"<div class='k-pal' data-el='CTA · chamada' data-maxw='48'>{fmt(c.get('palavra') or 'LINK NA BIO')}</div>")
        rodape = " · ".join(esc(x) for x in (M.get("profissional", "Jorge Souto"), M.get("profissao", "treinador"),
                                             M.get("registro", REGISTRO)) if x)
    elif tipo == "salvar":
        ic = ("<div class='k-ic' data-el='CTA · ícones'>"
              "<svg data-el='Ícone salvar' viewBox='0 0 46 46' fill='none' stroke='url(#gm)' stroke-width='3.4' stroke-linejoin='round'><path d='M12 5h22v36L23 32 12 41z'/></svg>"
              "<svg data-el='Ícone enviar' viewBox='0 0 46 46' fill='none' stroke='url(#gm)' stroke-width='3.4' stroke-linejoin='round'><path d='M41 5L5 20l14 6 6 14z'/><path d='M41 5L19 26'/></svg></div>")
        instr = f"<div class='k-instr' data-el='CTA · instrução'>{fmt(c['instrucao'])}</div>" if c.get("instrucao") else ""
        caixa = f"{ic}{instr}<div class='k-pal' data-el='CTA · chamada' data-maxw='48'>{fmt(c.get('palavra') or 'SALVA ESTE POST')}</div>"
        c = dict(c, beneficio=c.get("beneficio") or "e manda para quem precisa")
        rodape = arroba
    else:
        caixa = (f"<div class='k-instr' data-el='CTA · instrução'>{fmt(c.get('instrucao') or 'Comenta a palavra abaixo:')}</div>"
                 f"<div class='k-pal' data-el='CTA · palavra' data-maxw='48'>{fmt(c.get('palavra'))}</div>")
        rodape = f"{arroba} · envio automático na DM"
    if c.get("beneficio"):
        caixa += f"<div class='k-ben' data-el='CTA · benefício'>{fmt(c['beneficio'])}</div>"
    partes.append(f"<div class='kbox' data-el='Caixa do CTA'>{caixa}</div>")
    partes.append(f"<div class='cta-rod' data-el='Rodapé do CTA'><div class='dot' data-el='Rodapé · bolinha'>{_logo(M)}</div>"
                  f"<span data-el='Rodapé · texto'>{rodape}</span></div>")
    alt = H - TOPO_CONTEUDO - BASE_CONTEUDO
    return (f"<div class='conteudo' data-el='Conteúdo' data-fith='{alt}' data-dica='encurte a frase-ponte ou o título'>"
            + "".join(partes) + "</div>")


def slide(s, M, base, C):
    """HTML de UM slide 1080x1350 do Modelo 5."""
    tipo = s.get("tipo", "dark")
    if tipo not in ("capa", "dark", "light", "grad", "cta"):
        tipo = "dark"
    K = cores(M)
    n, total = _indice(s, C)
    fundo = ""
    if tipo == "capa":
        corpo = _capa(s, M, base)
    elif tipo == "cta":
        corpo = _cta(s, M)
    else:
        fundo, corpo = _interno(s, base, tipo)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css(K)}</style></head>"
            f"<body class='{tipo}'>{_defs(K)}{fundo}{_fixos(M, tipo, n, total)}{corpo}{AJUSTE_M5_JS}</body></html>")
