"""Monta a ficha de treino do aluno (HTML + PDF A4) na identidade azul do SOUTO TREINADOR.

Só biblioteca padrão. O PDF sai pelo Chrome sem janela (variável CHROME ou detecção automática; Edge serve).

    python "05 - TREINO/montar_ficha.py" --plano <mesociclo.json> [--semana 1]
           [--registro <registro.json|csv>] [--checkin <checkin.json>] [--decisao-semana 3]
           [--saida <pasta>] [--previa <pasta para PNGs>] [--sem-pdf]

Páginas: 1 capa · 2 plano da semana · 3 mesociclo, regras de progressão e como registrar as cargas · 4 painel de volume
(séries por grupo e volume load dos exercícios principais, com as decisões do motor quando há registro).
Saída padrão: %USERPROFILE%\\SoutoTreinador\\Alunos\\<nome>\\Treinos\\ (nunca no repositório).
Cores sólidas no painel (leitor de PDF falha com degradê transparente); sem laranja.
"""
import argparse
import base64
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import calcular_treino as ct  # noqa: E402

# ------------------------------------------------------------------------------------------------ marca
def _ler(p, padrao):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return padrao


MARCA = _ler(os.path.join(RAIZ, "marca", "marca-souto.json"), {})
COR = {"eletrico": "#2E49CE", "royal": "#1F33A3", "aco": "#445DB4", "noite": "#141A3D", "grafite": "#1C1B24",
       "preto": "#0B0B0E", "nevoa": "#DCE1ED", "papel": "#F2F4F8", "branco": "#FFFFFF"}
for k, v in (MARCA.get("cores") or {}).items():
    COR[k.replace("azul_", "")] = v
# escala sequencial azul (semana 1 → última): um só matiz, do claro ao escuro
SEQ = ["#A9B6E6", "#6E84D9", "#2E49CE", "#1F33A3", "#141A3D"]

_cfg = _ler(os.path.join(RAIZ, "06 - GESTÃO DA CONSULTORIA", "config-st.json"), {})
PROF = {"marca": "Souto Treinador", "nome": "Jorge Souto", "registro": "CREF 000000-G/UF", "arroba": "@soutotreinador"}
PROF.update({k: v for k, v in (_cfg.get("profissional") or {}).items() if k in ("nome", "registro", "arroba") and v})
RODAPE = " · ".join(x for x in (PROF["marca"], PROF["nome"], PROF["registro"], PROF["arroba"]) if x)


def logo_data(tipo="branco"):
    p = os.path.join(RAIZ, "marca", "logo", f"souto-logo-{tipo}.png")
    if not os.path.isfile(p):
        return ""
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def chrome():
    cands = [os.environ.get("CHROME", "")]
    for var, partes in (("PROGRAMFILES", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("PROGRAMFILES(X86)", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("LOCALAPPDATA", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("PROGRAMFILES(X86)", ("Microsoft", "Edge", "Application", "msedge.exe")),
                        ("PROGRAMFILES", ("Microsoft", "Edge", "Application", "msedge.exe"))):
        if os.environ.get(var):
            cands.append(os.path.join(os.environ[var], *partes))
    cands += [shutil.which(n) or "" for n in ("chrome", "google-chrome", "chromium", "msedge")]
    return next((c for c in cands if c and os.path.isfile(c)), None)


def rodar_chrome(args, timeout=120):
    exe = chrome()
    if not exe:
        sys.exit("Chrome não encontrado. Instale o Google Chrome ou defina a variável CHROME com o caminho do chrome.exe.")
    perfil = tempfile.mkdtemp(prefix="st-chrome-")
    try:
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                        "--disable-extensions", f"--user-data-dir={perfil}", "--run-all-compositor-stages-before-draw",
                        "--virtual-time-budget=6000"] + args,
                       check=True, timeout=timeout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        shutil.rmtree(perfil, ignore_errors=True)


# ------------------------------------------------------------------------------------------------ helpers
E = lambda x: html.escape("" if x is None else str(x))


def fmt_kg(x):
    if x is None:
        return "—"
    return f"{x:g}".replace(".", ",")


def fmt_desc(s):
    s = int(s or 0)
    if s >= 60:
        m, r = divmod(s, 60)
        return f"{m} min" + (f" {r} s" if r else "")
    return f"{s} s"


def data_br(iso):
    try:
        return datetime.date.fromisoformat(iso).strftime("%d/%m/%Y")
    except Exception:
        return iso or ""


NOMES_GRUPO = {"quadriceps": "Quadríceps", "posteriores": "Posteriores de coxa", "gluteos": "Glúteos", "panturrilha": "Panturrilha",
               "peitoral": "Peitoral", "costas": "Costas", "ombros": "Ombros", "biceps": "Bíceps", "triceps": "Tríceps", "outros": "Outros"}
NOME_MODELO = {"linear": "Linear", "ondulatoria": "Ondulatória", "blocos": "Em blocos"}
NOME_OBJ = {"hipertrofia": "Hipertrofia", "forca": "Força", "força": "Força"}

# ------------------------------------------------------------------------------------------------ CSS
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
@page { size: A4; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #FFFFFF; }
body { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; color: %(preto)s; font-size: 9.6pt; line-height: 1.38; }
.pagina { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; background: #FFFFFF; }
.pagina:last-child { page-break-after: auto; break-after: auto; }
h1, h2, h3, .cond { font-family: 'Saira Condensed', 'Arial Narrow', Arial, sans-serif; letter-spacing: .3px; }
/* capa */
.capa { background: %(royal)s; background-image: linear-gradient(160deg, %(noite)s 0%%, %(royal)s 45%%, %(eletrico)s 100%%); color: #FFFFFF; }
.capa .logo { position: absolute; top: 34mm; left: 0; right: 0; text-align: center; }
.capa .logo img { width: 112mm; }
.capa .titulo { position: absolute; top: 118mm; left: 22mm; right: 22mm; }
.capa .kicker { font-family: 'Saira Condensed', Arial, sans-serif; font-weight: 700; font-size: 15pt; letter-spacing: 4px; color: %(nevoa)s; text-transform: uppercase; }
.capa h1 { font-size: 50pt; line-height: .95; margin: 3mm 0 6mm; font-weight: 800; text-transform: uppercase; color: #FFFFFF; }
.capa .barra { width: 34mm; height: 2.2mm; background: #FFFFFF; margin-bottom: 8mm; }
.capa .aluno { font-size: 22pt; font-weight: 700; color: #FFFFFF; }
.capa .meta { margin-top: 5mm; display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm 8mm; max-width: 150mm; }
.capa .meta div { border-left: 1.2mm solid %(nevoa)s; padding: 1mm 0 1mm 3.5mm; }
.capa .meta b { display: block; font-size: 8pt; letter-spacing: 1.5px; text-transform: uppercase; color: %(nevoa)s; font-weight: 600; }
.capa .meta span { font-size: 13pt; font-weight: 600; color: #FFFFFF; }
.capa .rodape-capa { position: absolute; bottom: 14mm; left: 22mm; right: 22mm; border-top: .3mm solid %(nevoa)s; padding-top: 4mm;
  font-size: 9.5pt; color: #FFFFFF; display: flex; justify-content: space-between; }
/* páginas internas */
.topo { height: 20mm; background: %(royal)s; color: #FFFFFF; display: flex; align-items: center; justify-content: space-between; padding: 0 14mm; }
.topo img { height: 11mm; }
.topo .t { text-align: right; }
.topo .t b { display: block; font-family: 'Saira Condensed', Arial, sans-serif; font-size: 17pt; letter-spacing: 1px; text-transform: uppercase; line-height: 1; }
.topo .t span { font-size: 8.5pt; color: %(nevoa)s; }
.miolo { padding: 7mm 14mm 0; }
.rodape { position: absolute; bottom: 0; left: 0; right: 0; height: 10mm; background: %(noite)s; color: #FFFFFF; font-size: 8pt;
  display: flex; align-items: center; justify-content: space-between; padding: 0 14mm; }
h2 { font-size: 17pt; margin: 0 0 2.5mm; color: %(royal)s; text-transform: uppercase; font-weight: 800; }
h3 { font-size: 12.5pt; margin: 4.5mm 0 1.8mm; color: %(noite)s; text-transform: uppercase; font-weight: 700; }
.sub { color: #3B3F55; font-size: 9pt; margin: -1mm 0 3mm; }
table { width: 100%%; border-collapse: collapse; }
.dia { margin-bottom: 3.6mm; break-inside: avoid; }
.dia-cab { background: %(eletrico)s; color: #FFFFFF; padding: 1.4mm 3mm; font-family: 'Saira Condensed', Arial, sans-serif; font-size: 12pt; font-weight: 700;
  text-transform: uppercase; letter-spacing: .6px; display: flex; justify-content: space-between; }
.dia-cab span { font-family: 'Inter', Arial, sans-serif; font-size: 8pt; font-weight: 500; text-transform: none; letter-spacing: 0; color: %(nevoa)s; padding-top: 1mm; }
.plano th { background: %(nevoa)s; color: %(noite)s; font-size: 7.4pt; text-transform: uppercase; letter-spacing: .4px; text-align: left; padding: 1.2mm 1.6mm; font-weight: 700; }
.plano td { padding: 1.3mm 1.6mm; border-bottom: .25mm solid %(nevoa)s; vertical-align: top; font-size: 8.8pt; }
.plano td.n { text-align: center; white-space: nowrap; font-weight: 600; }
.plano td.ex { font-weight: 600; width: 30%%; }
.plano td.obs { color: #3B3F55; font-size: 7.8pt; width: 27%%; }
.plano tr:nth-child(even) td { background: %(papel)s; }
.caixa { background: %(papel)s; border-left: 1.4mm solid %(eletrico)s; padding: 2.6mm 3.5mm; margin: 2.5mm 0; font-size: 9pt; }
.caixa b { color: %(royal)s; }
.lista { margin: 0; padding-left: 4.5mm; }
.lista li { margin: .9mm 0; }
.duas { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.meso th { background: %(royal)s; color: #FFFFFF; font-size: 7.6pt; text-transform: uppercase; padding: 1.4mm 2mm; text-align: left; }
.meso td { padding: 1.3mm 2mm; border-bottom: .25mm solid %(nevoa)s; font-size: 8.8pt; }
.meso tr.deload td { background: %(nevoa)s; font-weight: 600; }
.qr { width: 32mm; height: 32mm; border: .6mm dashed %(aco)s; display: flex; align-items: center; justify-content: center; text-align: center;
  font-size: 7.5pt; color: %(aco)s; background: #FFFFFF; flex: none; }
.registro { display: flex; gap: 5mm; align-items: center; }
.link { font-family: 'Consolas', monospace; font-size: 8.5pt; color: %(royal)s; word-break: break-all; }
.selo { display: inline-block; padding: .5mm 2mm; border-radius: 1mm; font-size: 7.4pt; font-weight: 700; letter-spacing: .3px; white-space: nowrap; }
.s-PROGREDIR { background: %(eletrico)s; color: #FFFFFF; }
.s-MANTER { background: %(nevoa)s; color: %(noite)s; }
.s-REDUZIR { background: %(aco)s; color: #FFFFFF; }
.s-DELOAD { background: %(noite)s; color: #FFFFFF; }
.dec td { padding: 1.1mm 1.6mm; border-bottom: .25mm solid %(nevoa)s; font-size: 7.9pt; vertical-align: top; }
.dec th { background: %(nevoa)s; color: %(noite)s; font-size: 7.2pt; text-transform: uppercase; text-align: left; padding: 1.1mm 1.6mm; }
.nota { font-size: 7.4pt; color: #3B3F55; margin-top: 1.5mm; }
.legenda { display: flex; gap: 4mm; font-size: 8pt; margin: 1mm 0 1.5mm; align-items: center; flex-wrap: wrap; }
.legenda i { display: inline-block; width: 3.4mm; height: 3.4mm; border-radius: .6mm; margin-right: 1.2mm; vertical-align: -0.6mm; }
.alerta { background: %(noite)s; color: #FFFFFF; padding: 2mm 3mm; font-size: 8.6pt; margin: 2mm 0; border-radius: 1mm; }
svg text { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; }
"""


def css():
    return CSS % COR


def topo(titulo, sub):
    return (f'<div class="topo"><img src="{logo_data("branco")}" alt="Souto Treinador">'
            f'<div class="t"><b>{E(titulo)}</b><span>{E(sub)}</span></div></div>')


def rodape(n, total):
    return f'<div class="rodape"><span>{E(RODAPE)}</span><span>{n}/{total}</span></div>'

# ------------------------------------------------------------------------------------------------ páginas


def pag_capa(p, semana):
    A = p["aluno"]
    s = p["semanas"][semana - 1]
    ultima = p["semanas"][-1]
    fim = (datetime.date.fromisoformat(ultima["inicio"]) + datetime.timedelta(days=6)).isoformat()
    fase = "Semana leve (deload)" if s["tipo"] == "deload" else f"Semana {semana} de {len(p['semanas'])} · {s['fase']}"
    return f"""<section class="pagina capa">
<div class="logo"><img src="{logo_data('branco')}" alt="Souto Treinador"></div>
<div class="titulo">
 <div class="kicker">Ficha de treino</div>
 <h1>Mesociclo<br>{E(NOME_MODELO.get(p['modelo'], p['modelo']))}</h1>
 <div class="barra"></div>
 <div class="aluno">{E(A.get('nome'))}</div>
 <div class="meta">
  <div><b>Objetivo</b><span>{E(NOME_OBJ.get(p['objetivo'], p['objetivo']).capitalize())}</span></div>
  <div><b>Fase / bloco</b><span>{E(fase)}</span></div>
  <div><b>Período</b><span>{data_br(p['semanas'][0]['inicio'])} a {data_br(fim)}</span></div>
  <div><b>Frequência</b><span>{len(p['divisao'])} treinos por semana</span></div>
 </div>
</div>
<div class="rodape-capa"><span>{E(RODAPE)}</span><span>Gerada em {data_br(p.get('gerado_em', ''))}</span></div>
</section>"""


def pag_plano(p, semana, n, total):
    s = p["semanas"][semana - 1]
    nomes = p.get("nomes_dias", {})
    blocos = []
    for d, linhas in s["sessoes"].items():
        rows = []
        for l in linhas:
            if l.get("carga_kg") is not None:
                carga = f"{fmt_kg(l['carga_kg'])} kg"
                pct = f"{l['pct_1rm']:g}%".replace(".", ",")
            else:
                carga = "pelo RIR"
                pct = f"~{l['pct_1rm']:.0f}%" if l.get("pct_1rm") else "—"
            rows.append(f"<tr><td class='ex'>{E(l['exercicio'])}</td><td class='n'>{l['series']}</td><td class='n'>{E(l['reps'])}</td>"
                        f"<td class='n'>{carga}</td><td class='n'>{pct}</td><td class='n'>{l['rir']:g}</td><td class='n'>{fmt_desc(l['descanso_s'])}</td>"
                        f"<td class='obs'>{E(l.get('obs'))}</td></tr>")
        blocos.append(f"""<div class="dia"><div class="dia-cab">Treino {E(d)}{(' · ' + E(nomes[d])) if nomes.get(d) else ''}<span>{len(linhas)} exercícios</span></div>
<table class="plano"><tr><th>Exercício</th><th>Séries</th><th>Reps</th><th>Carga</th><th>% máx.</th><th>RIR alvo</th><th>Descanso</th><th>Observação / técnica</th></tr>
{''.join(rows)}</table></div>""")
    tit = "Semana leve (deload)" if s["tipo"] == "deload" else f"Semana {semana}: {s['fase']}"
    return f"""<section class="pagina">{topo('Plano da semana', f"{p['aluno'].get('nome')} · início {data_br(s['inicio'])}")}
<div class="miolo"><h2>{E(tit)}</h2>
<p class="sub"><b>Carga</b> = ponto de partida estimado; ajuste para bater o <b>RIR alvo</b> (quantas repetições ainda sobrariam ao terminar a série). <b>% máx.</b> = porcentagem da sua carga máxima estimada.</p>
{''.join(blocos)}</div>{rodape(n, total)}</section>"""


def pag_meso(p, n, total):
    grupos = sorted({g for s in p["semanas"] for g in s["series_por_grupo"]})
    rows = []
    for s in p["semanas"]:
        reps = sorted({l["reps"] for d in s["sessoes"].values() for l in d}, key=lambda r: int(str(r).split()[0]))
        rirs = sorted({l["rir"] for d in s["sessoes"].values() for l in d})
        vol = [s["series_por_grupo"][g] for g in grupos]
        rows.append(f"<tr class='{'deload' if s['tipo'] == 'deload' else ''}'><td>{s['semana']}</td><td>{data_br(s['inicio'])}</td>"
                    f"<td>{E('deload (semana leve)' if s['tipo'] == 'deload' else s['fase'])}</td><td>{E(' / '.join(map(str, reps)))}</td>"
                    f"<td>{E(' / '.join(f'{r:g}' for r in rirs))}</td><td>{min(vol)} a {max(vol)}</td></tr>")
    url = p.get("check_in_cargas_url") or "https://tally.so/r/TROCAR"
    return f"""<section class="pagina">{topo('Mesociclo e progressão', p['aluno'].get('nome', ''))}
<div class="miolo"><h2>Como vai ser o seu ciclo</h2>
<table class="meso"><tr><th>Sem.</th><th>Início</th><th>Fase</th><th>Repetições</th><th>RIR alvo</th><th>Séries/grupo na semana</th></tr>{''.join(rows)}</table>
<p class="nota">O volume sobe aos poucos e a última semana é mais leve, para recuperar e começar o próximo ciclo mais descansado.</p>
<div class="duas"><div>
<h3>Como progredir</h3>
<ul class="lista">
<li><b>Fez todas as repetições e sobrou mais do que o RIR alvo?</b> Na próxima semana, faça 1 repetição a mais com o mesmo peso.</li>
<li><b>Chegou no topo da faixa de repetições?</b> Aumente o peso (o Jorge passa o número) e volte para o começo da faixa.</li>
<li><b>Não completou as repetições ou ficou mais pesado do que o alvo?</b> Mantenha o peso e avise no check-in.</li>
<li><b>Semana muito cansativa, dormindo mal, com dor muscular forte?</b> Conte no check-in: pode ser hora de uma semana leve.</li>
<li><b>Sentiu dor diferente, em articulação, ou que piora a cada treino?</b> Pare o exercício e fale com o Jorge antes do próximo treino.</li>
</ul></div><div>
<h3>O que é RIR (repetições na reserva)</h3>
<div class="caixa">Ao terminar a série, pergunte: <b>"quantas repetições boas eu ainda faria?"</b> Essa é a sua reserva. RIR 2 = pararia com 2 sobrando. Não precisa ir até não aguentar mais: perto do limite, com técnica boa, já dá o estímulo.</div>
<h3>Descanso e técnica</h3>
<ul class="lista"><li>Respeite o descanso indicado: descanso curto demais derruba as repetições das séries seguintes.</li>
<li>Amplitude completa e controle na descida valem mais do que carga a mais.</li></ul>
</div></div>
<h3>Como registrar suas cargas</h3>
<div class="registro"><div class="qr">QR do check-in<br>de cargas<br>(TROCAR)</div>
<div><p style="margin:0 0 1.5mm">Depois de cada semana, preencha o <b>check-in de cargas</b> (Tally): peso usado e repetições de cada exercício, o RIR da última série, como dormiu, cansaço, dor muscular e se teve alguma dor diferente.</p>
<div class="link">{E(url)}</div>
<p class="nota">Com isso o sistema calcula o seu volume da semana e o Jorge decide: progredir, manter, reduzir o volume ou fazer uma semana leve.</p></div></div>
<div class="caixa"><b>Alimentação:</b> dúvidas sobre dieta, suplementos ou peso são com o nutricionista responsável técnico da consultoria. Esta ficha é só de treino.</div>
</div>{rodape(n, total)}</section>"""

# ------------------------------------------------------------------------------------------------ gráficos (SVG sólido)


def svg_barras(res, grupos, faixa):
    """Barras horizontais agrupadas: séries de trabalho por grupo, uma barra por semana (azul do claro ao escuro)."""
    semanas = list(res)
    n_s = len(semanas)
    idx = [round(i * (len(SEQ) - 1) / max(1, n_s - 1)) for i in range(n_s)] if n_s > 1 else [2]
    cores = [SEQ[min(k, len(SEQ) - 1)] for k in idx]  # do claro (semana mais antiga) ao escuro (mais recente)
    W, esq, dir_ = 680, 132, 30
    bh, gap_b, gap_g = 7, 2, 9
    alt_g = len(semanas) * (bh + gap_b) - gap_b
    H = 26 + len(grupos) * (alt_g + gap_g) + 22
    vmax = max([faixa[1] + 2] + [res[w]["grupos"].get(g, 0) for w in semanas for g in grupos])
    x = lambda v: esq + (W - esq - dir_) * v / vmax
    o = [f'<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Séries por grupo muscular por semana">']
    # faixa-alvo (sólida, clara)
    o.append(f'<rect x="{x(faixa[0]):.1f}" y="18" width="{x(faixa[1]) - x(faixa[0]):.1f}" height="{H - 40}" fill="{COR["papel"]}"/>')
    o.append(f'<text x="{(x(faixa[0]) + x(faixa[1])) / 2:.1f}" y="13" font-size="10" fill="#3B3F55" text-anchor="middle">faixa-alvo {faixa[0]}–{faixa[1]} séries (Protocolo [V2])</text>')
    for t in range(0, int(vmax) + 1, 5):
        o.append(f'<line x1="{x(t):.1f}" y1="18" x2="{x(t):.1f}" y2="{H - 22}" stroke="{COR["nevoa"]}" stroke-width="1"/>')
        o.append(f'<text x="{x(t):.1f}" y="{H - 8}" font-size="10" fill="#3B3F55" text-anchor="middle">{t}</text>')
    y = 24
    for g in grupos:
        o.append(f'<text x="{esq - 8}" y="{y + alt_g / 2 + 4:.1f}" font-size="11" fill="{COR["preto"]}" text-anchor="end" font-weight="600">{E(NOMES_GRUPO.get(g, g))}</text>')
        for i, w in enumerate(semanas):
            v = res[w]["grupos"].get(g, 0)
            yy = y + i * (bh + gap_b)
            if v > 0:
                o.append(f'<rect x="{esq}" y="{yy}" width="{max(1.0, x(v) - esq):.1f}" height="{bh}" rx="2" fill="{cores[i]}"/>')
            if i == len(semanas) - 1:
                rot = f"{v:g}".replace(".", ",")
                o.append(f'<text x="{x(v) + 4:.1f}" y="{yy + bh - 0.5}" font-size="9.5" fill="{COR["preto"]}" font-weight="600">{rot}</text>')
        y += alt_g + gap_g
    o.append(f'<line x1="{esq}" y1="18" x2="{esq}" y2="{H - 22}" stroke="#3B3F55" stroke-width="1"/>')
    o.append("</svg>")
    leg = "".join(f'<span><i style="background:{cores[i]}"></i>Semana {w}</span>' for i, w in enumerate(semanas))
    return "".join(o), leg


def svg_linha(valores, titulo):
    """Mini gráfico de linha (uma série) do volume load semanal de um exercício."""
    W, H, e, d, t, b = 210, 112, 38, 10, 22, 22
    ws = list(valores)
    vs = [valores[w] for w in ws]
    lo, hi = 0, max(vs) * 1.15 if vs and max(vs) > 0 else 1
    X = lambda i: e + (W - e - d) * (i / max(1, len(ws) - 1)) if len(ws) > 1 else (e + W - d) / 2
    Y = lambda v: t + (H - t - b) * (1 - (v - lo) / (hi - lo))
    o = [f'<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{E(titulo)}">',
         f'<text x="2" y="12" font-size="10.5" font-weight="700" fill="{COR["noite"]}">{E(titulo)}</text>']
    for frac in (0, .5, 1):
        v = lo + (hi - lo) * frac
        o.append(f'<line x1="{e}" y1="{Y(v):.1f}" x2="{W - d}" y2="{Y(v):.1f}" stroke="{COR["nevoa"]}" stroke-width="1"/>')
        rot = f"{v / 1000:.1f} t".replace(".", ",")
        o.append(f'<text x="{e - 4}" y="{Y(v) + 3:.1f}" font-size="8" fill="#3B3F55" text-anchor="end">{rot}</text>')
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vs))
    if len(vs) > 1:
        o.append(f'<polyline points="{pts}" fill="none" stroke="{COR["eletrico"]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (w, v) in enumerate(zip(ws, vs)):
        o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{COR["eletrico"]}" stroke="#FFFFFF" stroke-width="2"/>')
        o.append(f'<text x="{X(i):.1f}" y="{H - 6}" font-size="8.5" fill="#3B3F55" text-anchor="middle">S{w}</text>')
    if vs:
        rot = f"{vs[-1]:,.0f} kg".replace(",", ".")
        o.append(f'<text x="{X(len(vs) - 1) - 2:.1f}" y="{Y(vs[-1]) - 8:.1f}" font-size="9" font-weight="700" fill="{COR["preto"]}" text-anchor="end">{rot}</text>')
    o.append("</svg>")
    return "".join(o)


def pag_painel(p, res, dec, n, total):
    nivel = p.get("nivel", "intermediario")
    faixa = (ct.REGRAS["inicio_series"].get(nivel, 10), ct.REGRAS["teto_series"].get(nivel, 20))
    if res:
        grupos = sorted({g for W in res.values() for g in W["grupos"]}, key=lambda g: list(NOMES_GRUPO).index(g) if g in NOMES_GRUPO else 99)
        barras, leg = svg_barras(res, grupos, faixa)
        exmap = ct.mapa_exercicios(p)
        principais = [e["nome"] for e in p["exercicios"] if e.get("principal")][:6]
        minis = []
        for nome in principais:
            vals = {w: W["exercicios"][nome]["vl"] for w, W in res.items() if nome in W["exercicios"]}
            if vals:
                minis.append(f"<div>{svg_linha(vals, nome)}</div>")
        linhas = "<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:2mm 5mm'>" + "".join(minis) + "</div>"
        fonte = "do registro de cargas (séries com RIR até 4; exercício que trabalha o grupo de forma secundária conta meia série)"
    else:
        res_plan = {s["semana"]: {"grupos": s["series_por_grupo"]} for s in p["semanas"]}
        grupos = sorted({g for s in p["semanas"] for g in s["series_por_grupo"]})
        barras, leg = svg_barras(dict(list(res_plan.items())[:5]), grupos, faixa)
        linhas = "<p class='nota'>Ainda sem registro de cargas: o gráfico mostra o volume planejado. O volume levantado aparece aqui depois dos primeiros check-ins.</p>"
        fonte = "do plano (séries diretas por grupo)"
    return f"""<section class="pagina">{topo('Painel de volume', p['aluno'].get('nome', ''))}
<div class="miolo"><h2>Volume × desempenho</h2>
<h3 style="margin-top:0">Séries por grupo muscular na semana</h3>
<div class="legenda">{leg}<span><i style="background:{COR['papel']};border:.2mm solid {COR['nevoa']}"></i>faixa-alvo</span></div>
{barras}
<p class="nota">Fonte: {fonte}.</p>
<h3>Volume levantado nos exercícios principais (séries × repetições × kg)</h3>
{linhas}
</div>{rodape(n, total)}</section>"""


def pag_decisao(p, dec, n, total):
    al = "".join(f"<div class='alerta'>{E(a.split(' [E1]')[0])}</div>" for a in dec.get("alertas", []))
    rows = []
    for d in dec["exercicios"]:
        cls = d["decisao"].split()[0]
        rows.append(f"<tr><td><b>{E(d['exercicio'])}</b></td><td><span class='selo s-{cls}'>{E(d['decisao'])}</span></td>"
                    f"<td>{E(d['sugestao'] or '—')}</td><td>{E(d['regra'])}</td></tr>")
    grows = []
    for g in dec.get("grupos", []):
        cls = g["decisao"].split()[0]
        grows.append(f"<tr><td><b>{E(NOMES_GRUPO.get(g['grupo'], g['grupo']))}</b></td><td><span class='selo s-{cls}'>{E(g['decisao'])}</span></td>"
                     f"<td>{E(g['motivo'].split(' [')[0])}</td></tr>")
    return f"""<section class="pagina">{topo('Decisão da semana', p['aluno'].get('nome', ''))}
<div class="miolo"><h2>Semana {dec['semana']}: o que muda</h2>
<p class="sub">Proposta do motor a partir das suas cargas e do check-in, revisada e aprovada pelo Jorge. Prontidão da semana (sono, cansaço, dor muscular e estresse, de 0 a 10): <b>{E(dec.get('prontidao'))}</b>.</p>
{al}
<table class="dec"><tr><th>Exercício</th><th>Decisão</th><th>O que muda</th><th>Regra</th></tr>{''.join(rows)}</table>
<h3>Volume por grupo muscular</h3>
<table class="dec"><tr><th>Grupo</th><th>Decisão</th><th>Séries na semana</th></tr>{''.join(grows)}</table>
<div class="legenda" style="margin-top:3mm"><span class='selo s-PROGREDIR'>PROGREDIR</span> mais carga, repetição ou série
<span class='selo s-MANTER'>MANTER</span> repetir a prescrição <span class='selo s-REDUZIR'>REDUZIR VOLUME</span> menos séries, mesma carga
<span class='selo s-DELOAD'>DELOAD</span> semana leve</div>
<p class="nota">Regras: Protocolo "Hipertrofia e força" (base científica do Souto Treinador), linhas [P1] a [P5], [D1], [D2] e [E1]. Cargas máximas são estimativas de grupo; cada pessoa varia.</p>
</div>{rodape(n, total)}</section>"""


def documento(paginas, titulo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(titulo)}</title>
<style>{css()}</style></head><body>{''.join(paginas)}</body></html>"""

# ------------------------------------------------------------------------------------------------ principal


def main():
    ap = argparse.ArgumentParser(description="Ficha de treino (HTML + PDF A4) do SOUTO TREINADOR.")
    ap.add_argument("--plano", required=True, help="mesociclo gerado por calcular_treino.py mesociclo")
    ap.add_argument("--semana", type=int, default=1, help="semana mostrada no plano (padrão 1)")
    ap.add_argument("--registro", help="registro de cargas (.json/.csv) para o painel")
    ap.add_argument("--checkin", help="check-in semanal (.json) para a decisão")
    ap.add_argument("--decisao-semana", type=int, help="semana da decisão mostrada no painel (padrão: última do registro)")
    ap.add_argument("--saida", help="pasta de saída (padrão: %%USERPROFILE%%/SoutoTreinador/Alunos/<nome>/Treinos)")
    ap.add_argument("--previa", help="pasta para PNGs de prévia (capa, plano, painel)")
    ap.add_argument("--sem-pdf", action="store_true")
    a = ap.parse_args()

    p = ct.ler_json(a.plano)
    nome = p["aluno"].get("nome", "aluno")
    res, dec = None, None
    if a.registro:
        res = ct.resumo_semanal(ct.ler_registro(a.registro), ct.mapa_exercicios(p))
        dec = ct.decidir(p, ct.ler_registro(a.registro), ct.ler_checkin(a.checkin), a.decisao_semana)
    total = 5 if dec else 4
    paginas = {
        "capa": pag_capa(p, a.semana),
        "plano": pag_plano(p, a.semana, 2, total),
        "mesociclo": pag_meso(p, 3, total),
        "painel": pag_painel(p, res, dec, 4, total),
    }
    if dec:
        paginas["decisao"] = pag_decisao(p, dec, 5, total)
    saida = os.path.abspath(a.saida) if a.saida else ct.pasta_treinos(nome)
    os.makedirs(saida, exist_ok=True)
    import unicodedata
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()).strip("-")
    base = f"ficha-treino-{slug}-sem{a.semana}"
    arq_html = os.path.join(saida, base + ".html")
    with open(arq_html, "w", encoding="utf-8") as f:
        f.write(documento(paginas.values(), f"Ficha de treino · {nome}"))
    print("HTML:", arq_html)
    if not a.sem_pdf:
        arq_pdf = os.path.join(saida, base + ".pdf")
        rodar_chrome(["--no-pdf-header-footer", "--print-to-pdf-no-header", f"--print-to-pdf={arq_pdf}", "file:///" + arq_html.replace("\\", "/")])
        print("PDF: ", arq_pdf if os.path.isfile(arq_pdf) else "(falhou)")
    if a.previa:
        a.previa = os.path.abspath(a.previa)
        os.makedirs(a.previa, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="st-previa-")
        try:
            for i, (k, pg) in enumerate(paginas.items(), 1):
                h = os.path.join(tmp, f"{k}.html")
                with open(h, "w", encoding="utf-8") as f:
                    f.write(documento([pg], k).replace("<style>", "<style>body{width:210mm}"))
                png = os.path.join(a.previa, f"treino-0{i}-{k}.png")
                # um Chrome por vez (pouca RAM)
                rodar_chrome(["--hide-scrollbars", "--force-device-scale-factor=1.5", "--window-size=794,1123",
                              f"--screenshot={png}", "file:///" + h.replace("\\", "/")])
                print("PNG: ", png)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
