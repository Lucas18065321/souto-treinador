"""Anexos de evolução em cards, a partir do bloco `evolucao` do JSON (SVG por script, sem internet, sem biblioteca).

  números   evolucao.peso, adesao, constancia → números grandes (peso, check-ins, dias no plano, treinos)
  peso      evolucao.peso + peso_inicial_kg  → área do peso de tendência em % do início + régua neutra de 5% e 10% (se houve déficit)
  adesão    evolucao.adesao                  → grade de 7 quadrados por semana (dias no plano) + anel com a % de dias
  treino    evolucao.treino.series           → um card por exercício-chave (só com documento.tem_treino)
  intestino evolucao.sintomas.series         → um card por sintoma, de 0 a 10 (só na linha gastro)

Modelo A (claro): números em fileira, peso, grade com anel, cards de treino e intestino.
Modelo B (escuro): painel "bento" (anel grande dos dias no plano + números grandes ao lado), peso, grade, cards sem eixo.
Cada troca de plano (evolucao.planos) vira linha tracejada + etiqueta v1, v2…; na tela, cada ponto tem a dica com data,
valor e plano (calorias e macros só com os números ligados). Cores só por classe CSS (g-…). Uma série por gráfico, no
escala de azuis da marca: sem verde × vermelho. Seção sem dado some.
"""
import datetime as dt
import html
import itertools
import math

_ids = itertools.count(1)
CFG = {"numeros": True}   # todos() ajusta: com os números desligados, a dica não mostra calorias nem gramas
# escala de azuis da marca Souto Treinador em 7 degraus sólidos (de baixo para cima): leve para qualquer leitor de PDF
DEGRADE_7 = ["#1F33A3", "#293EB0", "#334ABC", "#3E56C8", "#4861D5", "#526CE2", "#5C78EE"]


# ---------- utilitários ----------
def _d(iso):
    return dt.date.fromisoformat(str(iso)[:10])


def _br(data, ano=True):
    return data.strftime("%d/%m/%Y" if ano else "%d/%m")


def _num(v, casas=0):
    s = f"{float(v):,.{casas}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".").replace("-", "−")


def _q(v):
    v = float(v)
    return _num(v, 0 if v.is_integer() else 1)


def _esc(s):
    return html.escape(str(s), quote=True)


def _plano_em(planos, data):
    for p in planos:
        if _d(p["inicio"]) <= data and (not p.get("fim") or data <= _d(p["fim"])):
            return p
    return None


def _dica(titulo, valor, planos, data):
    p = _plano_em(planos, data)
    txt = f"<b>{titulo}</b><br>{valor}"
    if p:
        txt += f"<div class='dica-plano'>Plano v{p['versao']}"
        if CFG["numeros"]:
            macros = " · ".join(f"{n} {_q(p[k])}\u00a0g" for n, k in (("proteína", "proteina_g"), ("carboidrato", "carboidrato_g"),
                                                                ("gordura", "gordura_g")) if p.get(k) is not None)
            txt += (f" · {_num(p['kcal_dia'])} calorias" if p.get("kcal_dia") else "") + (f"<br>{macros}" if macros else "")
        txt += "</div>"
    return _esc(txt)


def _passo_redondo(faixa, alvo=4):
    """Passo de 1, 2, 2,5 ou 5 × 10^n que dá cerca de `alvo` marcas no eixo."""
    bruto = max(faixa, 1e-9) / alvo
    base = 10 ** math.floor(math.log10(bruto))
    return next(m * base for m in (1, 2, 2.5, 5, 10) if m * base >= bruto)


class Eixo:
    def __init__(self, x0, x1, y0, y1, w, h, ml, mr, mt, mb):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.w, self.h, self.ml, self.mr, self.mt, self.mb = w, h, ml, mr, mt, mb
        self.dias = max((x1 - x0).days, 1)

    def x(self, data):
        return self.ml + (data - self.x0).days / self.dias * (self.w - self.ml - self.mr)

    def y(self, v):
        return self.mt + (self.y1 - v) / ((self.y1 - self.y0) or 1) * (self.h - self.mt - self.mb)

    @property
    def base(self):
        return self.h - self.mb


def _svg(uid, e, corpo, rotulo):
    defs = (f"<defs><linearGradient id='{uid}l' gradientUnits='userSpaceOnUse' x1='{e.ml}' y1='0' x2='{e.w - e.mr}' y2='0'>"
            f"<stop class='g-c1' offset='0'/><stop class='g-c2' offset='.48'/><stop class='g-c3' offset='1'/></linearGradient></defs>")
    return (f"<svg viewBox='0 0 {e.w:.0f} {e.h:.0f}' role='img' aria-label='{_esc(rotulo)}' xmlns='http://www.w3.org/2000/svg'>"
            f"{defs}{corpo}</svg>")


def _pilula_v(x_centro, topo, versao, w_max):
    larg = 22 if versao < 10 else 28
    px = min(max(x_centro - larg / 2, 1), w_max - larg - 1)
    return (f"<rect class='g-pilula' x='{px:.1f}' y='{topo - 21:.1f}' width='{larg}' height='15' rx='7.5'/>"
            f"<text class='g-pilula-tx' x='{px + larg / 2:.1f}' y='{topo - 10.4:.1f}' text-anchor='middle'>v{versao}</text>")


def _marcas_plano(e, planos, ult=None):
    """Faixa por plano (alternada), linha tracejada e etiqueta vN no começo de cada plano.
    ult: data do último registro; um plano que começa depois dele tem a linha afastada do último ponto."""
    faixas, marcas = [], []
    for i, p in enumerate(sorted(planos, key=lambda p: p["inicio"])):
        ini, fim = _d(p["inicio"]), (_d(p["fim"]) if p.get("fim") else e.x1)
        a, b = max(ini, e.x0), min(fim, e.x1)
        if a > e.x1 or b < e.x0:
            continue
        xa, xb = e.x(a), e.x(b)
        if ult and ini > ult:
            xa = min(max(xa, e.x(ult) + 10), e.w - e.mr)
        if i % 2 == 0 and xb > xa:
            faixas.append(f"<rect class='g-faixa' x='{xa:.1f}' y='{e.mt:.1f}' width='{xb - xa:.1f}' height='{e.base - e.mt:.1f}'/>")
        if e.x0 <= ini <= e.x1:
            marcas.append(f"<line class='g-marca' x1='{xa:.1f}' x2='{xa:.1f}' y1='{e.mt - 2:.1f}' y2='{e.base:.1f}'/>")
            marcas.append(_pilula_v(xa, e.mt, p["versao"], e.w))
    return "".join(faixas), "".join(marcas)


def _grade_y(e, ticks, fmt, rotulos=True):
    out = ""
    for t in ticks:
        out += f"<line class='g-grade' x1='{e.ml}' x2='{e.w - e.mr}' y1='{e.y(t):.1f}' y2='{e.y(t):.1f}'/>"
        if rotulos:
            ymin = " y-min" if t == min(ticks) else ""
            out += f"<text class='g-tx{ymin}' x='{e.ml - 7}' y='{e.y(t) + 4:.1f}' text-anchor='end'>{fmt(t)}</text>"
    return out


def _semanas_x(e, inicio, fim, max_rot=9, so_pontas=False):
    """Datas do eixo em semanas regulares (semana sem registro não abre buraco na régua).
    Rótulos alternados levam a classe x-alt, que some na tela estreita do celular."""
    semanas, d = [], inicio
    while d <= fim:
        semanas.append(d)
        d += dt.timedelta(days=7)
    y = e.base + 20
    if so_pontas and len(semanas) > 1:
        sel = [(semanas[0], "start", ""), (semanas[-1], "end", "")]
    else:
        passo = max(1, -(-len(semanas) // max_rot))
        sel = [(s, "middle", " x-alt" if (k // passo) % 2 else "") for k, s in enumerate(semanas) if k % passo == 0]
    return "".join(f"<text class='g-tx{c}' x='{e.x(s):.1f}' y='{y:.1f}' text-anchor='{a}'>{_br(s, False)}</text>" for s, a, c in sel)


def _linha_area(uid, e, pts, raio=3.6):
    caminho = " ".join(f"{'M' if k == 0 else 'L'}{e.x(d):.1f},{e.y(v):.1f}" for k, (d, v) in enumerate(pts))
    area = f"{caminho} L{e.x(pts[-1][0]):.1f},{e.base:.1f} L{e.x(pts[0][0]):.1f},{e.base:.1f} Z"
    pontos = "".join(f"<circle class='g-pt' cx='{e.x(d):.1f}' cy='{e.y(v):.1f}' r='{raio}'/>" for d, v in pts)
    return (f"<path class='g-area' d='{area}'/><path d='{caminho}' fill='none' stroke='url(#{uid}l)' stroke-width='2.6' "
            f"stroke-linejoin='round' stroke-linecap='round'/>{pontos}")


def _alvos(e, pts, dica_de, r=14):
    return "".join(f"<circle class='alvo' cx='{e.x(d):.1f}' cy='{e.y(v):.1f}' r='{r}' fill='transparent' data-dica='{dica_de(d, v)}'/>"
                   for d, v in pts)


def _dominio_x(datas, planos, folga=4):
    x0, x1 = min(datas), max(datas)
    for p in planos:
        ini = _d(p["inicio"])
        if x1 < ini <= x1 + dt.timedelta(days=10):   # plano que começa logo depois do último registro entra na régua
            x1 = ini
    return x0, x1 + dt.timedelta(days=folga)          # folga separa o último ponto da linha do plano novo


def _card(corpo, classe=""):
    return f"<div class='card{(' ' + classe) if classe else ''}'>{corpo}</div>"


def _topo(titulo, pilula=""):
    p = f"<span class='pilula'>{pilula}</span>" if pilula else ""
    return f"<div class='card-topo'><h3>{titulo}</h3>{p}</div>"


def _anel(frac, classe="anel"):
    r, esp = 46, 11
    circ = 2 * math.pi * r
    uid = f"g{next(_ids)}"
    return (f"<svg viewBox='0 0 120 120' class='{classe}' role='img' aria-label='{round(frac * 100)}% dos dias no plano'>"
            f"<defs><linearGradient id='{uid}' x1='0' y1='0' x2='1' y2='1'><stop class='g-c1' offset='0'/>"
            f"<stop class='g-c3' offset='1'/></linearGradient></defs>"
            f"<circle class='g-trilho' cx='60' cy='60' r='{r}' stroke-width='{esp}' fill='none'/>"
            f"<circle cx='60' cy='60' r='{r}' stroke='url(#{uid})' stroke-width='{esp}' fill='none' stroke-linecap='round' "
            f"stroke-dasharray='{circ * frac:.1f} {circ:.1f}' transform='rotate(-90 60 60)'/></svg>")


# ---------- dados derivados ----------
def _resumo(E, D):
    """Os números grandes: (rótulo, valor HTML, legenda, fração da barra ou None)."""
    out = []
    pts = sorted((_d(p["data"]), p["kg"]) for p in E.get("peso") or [])
    ini = E.get("peso_inicial_kg")
    if len(pts) >= 2 and ini:
        pct = (pts[-1][1] - ini) / ini * 100
        out.append(("Peso", f"{_num(pct, 1)}<small>%</small>", f"{_num(ini, 1)} → {_num(pts[-1][1], 1)} kg", None))
    c = E.get("constancia") or {}
    if (c.get("checkins") or {}).get("esperados"):
        f, t = c["checkins"]["feitos"], c["checkins"]["esperados"]
        out.append(("Check-ins", f"{f}<small> de {t}</small>", "enviados", f / t))
    sem = E.get("adesao") or []
    if sem:
        media = sum(s["dias_no_plano"] for s in sem) / len(sem)
        out.append(("Dias no plano", f"{_num(media, 1)}<small> de 7</small>", "média por semana", media / 7))
    if D.get("tem_treino") and (c.get("treinos") or {}).get("planejados"):
        f, t = c["treinos"]["feitos"], c["treinos"]["planejados"]
        out.append(("Treinos", f"{f}<small> de {t}</small>", "feitos", f / t))
    return out


def _num_card(rot, val, sub, frac, classe="num-card"):
    barra = f"<div class='num-barra'><span style='width:{min(frac, 1) * 100:.0f}%'></span></div>" if frac is not None else ""
    return (f"<div class='{classe}'><span class='rot'>{_esc(rot)}</span><b class='num-grande'>{val}</b>"
            f"<span class='num-sub'>{_esc(sub)}</span>{barra}</div>")


# ---------- modelo A: números em fileira ----------
def numeros(E, D):
    tiles = _resumo(E, D)
    if len(tiles) < 2:
        return ""
    cards = "".join(_num_card(*t) for t in tiles[:4])
    return f"<div class='numeros-evol' style='--n:{min(len(tiles), 4)}'>{cards}</div>"


# ---------- modelo B: painel bento (anel grande + números ao lado) ----------
def bento(E, D):
    sem = E.get("adesao") or []
    tiles = [t for t in _resumo(E, D) if t[0] != "Dias no plano"]
    if not sem or not tiles:
        return numeros(E, D)
    feitos, total = sum(int(s["dias_no_plano"]) for s in sem), 7 * len(sem)
    frac = feitos / total
    anel = (f"<div class='card bento-anel'><span class='rot'>Dias no plano</span><div class='anel-caixa grande'>{_anel(frac)}"
            f"<div class='anel-centro'><b>{round(frac * 100)}%</b><span>dos dias</span></div></div>"
            f"<p class='anel-leg'>{feitos} de {total} dias no plano, em {len(sem)} semanas · média de "
            f"{_num(feitos / len(sem), 1)} de 7 por semana</p></div>")
    lado = "".join(_num_card(*t, classe="card bento-num") for t in tiles[:3])
    return f"<div class='bento'>{anel}<div class='bento-lado'>{lado}</div></div>"


# ---------- peso ----------
def peso(E):
    pts = sorted((_d(p["data"]), p["kg"]) for p in E.get("peso") or [])
    ini = E.get("peso_inicial_kg")
    if len(pts) < 2 or not ini:
        return ""
    planos = E.get("planos") or []
    serie = [(d, (kg - ini) / ini * 100) for d, kg in pts]
    kg = dict(pts)
    vals = [v for _, v in serie]
    lo, hi = min(vals) - .5, max(vals) + .4
    passo = _passo_redondo(hi - lo, 4)
    lo = math.floor(lo / passo) * passo
    hi = 0 if max(vals) <= 0 else math.ceil(hi / passo) * passo   # o início (0%) fica no topo quando só caiu
    x0, x1 = _dominio_x([d for d, _ in serie], planos)
    e = Eixo(x0, x1, lo, hi, 680, 194, 44, 16, 34, 30)
    uid = f"g{next(_ids)}"
    ticks = [lo + k * passo for k in range(int(round((hi - lo) / passo)) + 1)]
    faixas, marcas = _marcas_plano(e, planos, serie[-1][0])
    corpo = faixas + _grade_y(e, ticks, lambda t: f"{_num(t, 0 if float(t).is_integer() else 1)}%")
    corpo += _semanas_x(e, x0, max(d for d, _ in serie)) + _linha_area(uid, e, serie) + marcas
    d_ult, v_ult = serie[-1]
    xp, yp = e.x(d_ult), e.y(v_ult)
    ex = xp - 64 if xp - 64 > e.ml + 4 else xp + 10          # à esquerda do ponto (longe da linha do plano novo)
    y_ant = e.y(serie[-2][1])
    ey = min(yp, y_ant) - 34                                  # e acima da linha, sem cobrir o trecho final
    corpo += (f"<circle class='g-pt-forte' cx='{xp:.1f}' cy='{yp:.1f}' r='5.5'/>"
              f"<rect class='g-etiqueta' x='{ex:.1f}' y='{ey:.1f}' width='60' height='19' rx='9.5'/>"
              f"<text class='g-etiqueta-tx' x='{ex + 30:.1f}' y='{ey + 13.4:.1f}' text-anchor='middle'>{_num(kg[d_ult], 1)} kg</text>")

    def dica_peso(d, v):
        if abs(v) < 0.05:
            return _dica(_br(d), f"{_num(kg[d], 1)} kg · peso do início", planos, d)
        return _dica(_br(d), f"{_num(kg[d], 1)} kg · {_num(abs(v), 1)}% {'abaixo' if v < 0 else 'acima'} do peso do início", planos, d)

    xs = [e.x(d) for d, _ in serie]
    for k, (d, v) in enumerate(serie):
        a = (xs[k - 1] + xs[k]) / 2 if k else e.ml
        b = (xs[k] + xs[k + 1]) / 2 if k < len(xs) - 1 else e.w - e.mr
        corpo += (f"<rect class='alvo' x='{a:.1f}' y='{e.mt:.1f}' width='{b - a:.1f}' height='{e.base - e.mt:.1f}' fill='transparent' "
                  f"data-dica='{dica_peso(d, v)}'/>")
    svg = _svg(uid, e, corpo, "Peso de tendência em % do peso do início")

    regua = ""
    if any(p.get("fase") == "deficit" for p in planos):
        perda = max(0.0, -v_ult)
        topo = max(11.0, perda + 1)
        pos = perda / topo * 100
        marcas_r = "".join(f"<span class='regua-marca' style='left:{r / topo * 100:.2f}%'><i></i>{r}%</span>" for r in (5, 10))
        dif_kg = kg[d_ult] - ini
        if v_ult < 0:
            frase = f"Você está <b>{_num(perda, 1)}% abaixo do peso do início</b> ({_num(dif_kg, 1)} kg)."
        else:
            frase = f"Você está <b>{_num(v_ult, 1)}% acima do peso do início</b> (+{_num(dif_kg, 1)} kg)."
        regua = (f"<div class='regua'><div class='regua-trilho'><span class='regua-ponto' style='left:{pos:.2f}%'></span>"
                 f"<span class='regua-marca zero' style='left:0'><i></i>0</span>{marcas_r}</div>"
                 f"<p class='regua-leg'>{frase} As marcas de 5% e 10% são referências do acompanhamento, não meta nem previsão.</p></div>")
    guia = (f"Em % do peso do início ({_num(ini, 1)} kg). O peso de tendência é como a média da semana: tira o sobe e desce "
            "de água, sal e intestino.")
    pil = f"{_num(kg[d_ult] - ini, 1)} kg desde {_br(serie[0][0], False)}"
    return _card(_topo("Peso de tendência", pil) + f"<p class='guia'>{_esc(guia)}</p>{svg}{regua}")


# ---------- adesão ----------
def adesao(E, com_anel=True):
    sem = sorted(E.get("adesao") or [], key=lambda s: s["semana"])
    if len(sem) < 2:
        return ""
    planos = E.get("planos") or []
    n = len(sem)
    lado, vao, ml, mt = (22, 5, 30, 40) if com_anel else (18, 4, 30, 40)   # sem o anel (modelo B), a grade fica mais baixa
    col = max(lado + 14, min(58, (560 - ml) / n)) if com_anel else max(lado + 18, min(76, (660 - ml) / n))
    w = ml + col * n + 8
    base = mt + 7 * (lado + vao) - vao
    h = base + 28
    uid = f"g{next(_ids)}"
    datas = [_d(s["semana"]) for s in sem]
    e = Eixo(datas[0], datas[-1] + dt.timedelta(days=7), 0, 7, w, h, ml, 8, mt, 28)

    def cx(i):
        return ml + col * i + col / 2

    corpo = ""
    for i, (s, d) in enumerate(zip(sem, datas)):
        v = int(s["dias_no_plano"])
        x = cx(i) - lado / 2
        for j in range(7):
            y = base - (j + 1) * lado - j * vao
            corpo += (f"<rect x='{x:.1f}' y='{y:.1f}' width='{lado}' height='{lado}' rx='5' fill='{DEGRADE_7[j]}'/>" if j < v else
                      f"<rect class='g-off' x='{x:.1f}' y='{y:.1f}' width='{lado}' height='{lado}' rx='5'/>")
        alt = " x-alt" if i % 2 else ""
        corpo += (f"<text class='g-tx-forte' x='{cx(i):.1f}' y='{mt - 8:.1f}' text-anchor='middle'>{v}</text>"
                  f"<text class='g-tx{alt}' x='{cx(i):.1f}' y='{base + 19:.1f}' text-anchor='middle'>{_br(d, False)}</text>")
        semana = f"Semana de {_br(d, False)} a {_br(d + dt.timedelta(days=6), False)}"
        corpo += (f"<rect class='alvo' x='{cx(i) - col / 2:.1f}' y='{mt - 22}' width='{col:.1f}' height='{base - mt + 44:.1f}' "
                  f"fill='transparent' data-dica='{_dica(semana, f'{v} de 7 dias no plano', planos, d)}'/>")
    marcas = ""
    for p in sorted(planos, key=lambda p: p["inicio"]):
        ini = _d(p["inicio"])
        if not (datas[0] <= ini <= datas[-1] + dt.timedelta(days=7)):
            continue
        xa = ml + col * (ini - datas[0]).days / 7
        if ini > datas[0]:
            marcas += f"<line class='g-marca' x1='{xa:.1f}' x2='{xa:.1f}' y1='{mt - 30}' y2='{base:.1f}'/>"
            marcas += _pilula_v(xa, mt - 13, p["versao"], w)
        else:
            marcas += _pilula_v(cx(0), mt - 13, p["versao"], w)   # plano que começa na 1ª semana: etiqueta sobre a 1ª coluna
    corpo += (f"<text class='g-tx' x='{ml - 8}' y='{base - lado / 2 + 4:.1f}' text-anchor='end'>1</text>"
              f"<text class='g-tx' x='{ml - 8}' y='{base - 7 * (lado + vao) + vao + lado / 2 + 4:.1f}' text-anchor='end'>7</text>")
    svg = _svg(uid, e, corpo + marcas, "Dias no plano por semana")
    feitos, total = sum(int(s["dias_no_plano"]) for s in sem), 7 * n
    guia = "Cada coluna é uma semana; cada quadrado aceso é um dia que seguiu o plano, contado pelo seu check-in."
    topo = _topo("Dias no plano por semana", f"média de {_num(feitos / n, 1)} de 7")
    if not com_anel:
        return _card(topo + f"<p class='guia'>{guia}</p><div class='adesao-grade'>{svg}</div>")
    frac = feitos / total
    bloco_anel = (f"<div class='anel-bloco'><div class='anel-caixa'>{_anel(frac)}<div class='anel-centro'><b>{round(frac * 100)}%</b>"
                  f"<span>dos dias</span></div></div><p class='anel-leg'>{feitos} de {total} dias no plano, em {n} semanas</p></div>")
    return _card(topo + f"<p class='guia'>{guia}</p><div class='adesao-corpo'><div class='adesao-grade'>{svg}</div>{bloco_anel}</div>")


# ---------- treino e intestino: um card por série ----------
def _mini(serie, planos, unidade, lo=None, hi=None, sufixo="", eixo_y=True):
    pts = sorted((_d(p["data"]), p["valor"]) for p in serie.get("pontos", []))
    if len(pts) < 2:
        return ""
    vals = [v for _, v in pts]
    if lo is None:
        folga = max((max(vals) - min(vals)) * .25, 1)
        passo = _passo_redondo(max(vals) - min(vals) + 2 * folga, 3)
        lo = max(0, math.floor((min(vals) - folga) / passo) * passo)
        hi = math.ceil((max(vals) + folga) / passo) * passo
    else:
        passo = _passo_redondo(hi - lo, 2)
    x0, x1 = _dominio_x([d for d, _ in pts], planos)
    e = Eixo(x0, x1, lo, hi, 320, 104, 30 if eixo_y else 12, 12, 26, 24)
    uid = f"g{next(_ids)}"
    ticks = [lo + k * passo for k in range(int(round((hi - lo) / passo)) + 1)]
    faixas, marcas = _marcas_plano(e, planos, pts[-1][0])
    corpo = faixas + _grade_y(e, ticks if eixo_y else [lo], _q, eixo_y) + _semanas_x(e, x0, max(d for d, _ in pts), so_pontas=True)
    corpo += _linha_area(uid, e, pts, raio=3.2) + marcas
    un = f" {unidade}" if unidade else ""
    if not eixo_y:   # sem eixo: o valor do começo e o de hoje escritos junto dos pontos
        (da, va), (db, vb) = pts[0], pts[-1]
        corpo += (f"<text class='g-tx-forte' x='{e.x(da) + 2:.1f}' y='{e.y(va) - 9:.1f}' text-anchor='start'>{_q(va)}</text>"
                  f"<text class='g-tx-forte' x='{e.x(db) - 2:.1f}' y='{e.y(vb) - 9:.1f}' text-anchor='end'>{_q(vb)}</text>")
    corpo += _alvos(e, pts, lambda d, v: _dica(_br(d), f"{serie['nome']}: {_q(v)}{un}{sufixo}", planos, d), r=11)
    svg = _svg(uid, e, corpo, f"{serie['nome']} ao longo das semanas")
    d0, v0 = pts[0]
    v1 = pts[-1][1]
    dif = v1 - v0
    pil = "igual ao início" if dif == 0 else f"{'+' if dif > 0 else '−'}{_q(abs(dif))}{un} desde {_br(d0, False)}"
    return _card(f"<div class='card-topo'><span class='rot'>{_esc(serie['nome'])}</span><span class='pilula'>{pil}</span></div>"
                 f"<b class='num-grande'>{_q(v1)}<small>{un}{sufixo}</small></b>"
                 f"<span class='num-sub'>era {_q(v0)}{un}{sufixo} em {_br(d0, False)}</span>{svg}", "mini")


def treino(E, eixo_y=True):
    b = E.get("treino") or {}
    cards = [c for c in (_mini(s, E.get("planos") or [], b.get("unidade", "kg"), eixo_y=eixo_y) for s in (b.get("series") or [])[:4]) if c]
    if not cards:
        return ""
    return (f"<div class='bloco-evol'><h3>Carga nos exercícios principais</h3>"
            f"<p class='guia'>Peso usado em cada exercício, semana a semana.</p><div class='minis'>{''.join(cards)}</div></div>")


def intestino(E, eixo_y=True):
    b = E.get("sintomas") or {}
    cards = [c for c in (_mini(s, E.get("planos") or [], "", 0, 10, " de 10", eixo_y) for s in (b.get("series") or [])[:4]) if c]
    if not cards:
        return ""
    escala = f" ({_esc(b['escala'])})" if b.get("escala") else ""
    return (f"<div class='bloco-evol'><h3>Seu intestino</h3><p class='guia'>Média da semana, pelo seu check-in{escala}.</p>"
            f"<div class='minis'>{''.join(cards)}</div></div>")


def todos(E, D, P, modelo="a", mostrar=True):
    CFG["numeros"] = bool(mostrar)
    b = modelo == "b"
    blocos = [bento(E, D) if b else numeros(E, D), peso(E), adesao(E, com_anel=not b)]
    if D.get("tem_treino"):
        blocos.append(treino(E, eixo_y=not b))
    if D.get("linha") == "gastro":
        blocos.append(intestino(E, eixo_y=not b))
    return "".join(x for x in blocos if x)
