"""Gera o guia completo em PDF (docs/Guia Souto Treinador.pdf) a partir dos guias em Markdown e dos prints.

Uso (da raiz do repositório):
    pip install markdown==3.7 pillow
    python docs/gerar_guia_pdf.py

Precisa do Google Chrome (ou da variável CHROME apontando para ele).
"""
import base64
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DOCS = Path(__file__).resolve().parent
RAIZ = DOCS.parent
GUIAS = DOCS / "guias"
PRINTS = DOCS / "prints"
SAIDA = DOCS / "Guia Souto Treinador.pdf"
MARCA = json.loads((RAIZ / "marca" / "marca-souto.json").read_text(encoding="utf-8"))
C = MARCA["cores"]
REPO = "https://github.com/Lucas18065321/souto-treinador"

CAPITULOS = [
    ("00-instalacao-geral.md", "Instalação geral", []),
    ("01-base-cientifica.md", "Cérebro científico", []),
    ("06-treino.md", "Prescrição de treino e controle de volume", [
        ("treino", "Ficha de treino e painel de volume (exemplo fictício)")]),
    ("02-roteiros.md", "Motor de roteiros", []),
    ("03-carrossel.md", "Motor de carrossel", [
        ("carrossel", "Carrosséis de teste nos 5 formatos (artes em cinza = espaço da foto)")]),
    ("04-video.md", "Motor de edição de vídeo", [
        ("video", "Quadros do render de teste na identidade azul")]),
    ("05-dieta-e-painel-st.md", "Dieta e Painel ST", [
        ("painel", "Painel ST (modo demonstração, dados fictícios)"),
        ("dieta", "Documento do plano alimentar, modelos A e B (exemplo fictício)")]),
]
EXTRA_PRINTS = {
    "carrossel": [
        RAIZ / "03 - CARROSSÉIS E ARTE/Carrosséis/_testes/_teste-modelo5/folha.jpg",
        RAIZ / "03 - CARROSSÉIS E ARTE/Carrosséis/_testes/_teste-modelo2/folha.jpg",
        RAIZ / "03 - CARROSSÉIS E ARTE/Carrosséis/_testes/_folha-modelos-1-3-4.jpg",
    ],
}


def achar_chrome():
    for c in [os.environ.get("CHROME"),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              shutil.which("chrome"), shutil.which("google-chrome")]:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome não encontrado. Instale o Google Chrome ou defina a variável CHROME.")


def img64(p):
    p = Path(p)
    tipo = "jpeg" if p.suffix.lower() in (".jpg", ".jpeg") else "png"
    return f"data:image/{tipo};base64," + base64.b64encode(p.read_bytes()).decode()


def img_leve(p, largura=1300):
    """Print reduzido em JPEG (o PDF fica leve)."""
    import io
    from PIL import Image
    im = Image.open(p).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def galeria(chave, titulo):
    arqs = sorted((PRINTS / chave).glob("*.png")) + sorted((PRINTS / chave).glob("*.jpg")) if (PRINTS / chave).exists() else []
    arqs = [a for a in EXTRA_PRINTS.get(chave, []) if Path(a).exists()] + arqs
    if not arqs:
        return ""
    figs = "".join(f'<figure><img src="{img_leve(a)}"><figcaption>{Path(a).stem.replace("-", " ").replace("_", " ")}</figcaption></figure>'
                   for a in arqs)
    return f'<section class="galeria"><h2>Como fica</h2><p class="leg">{titulo}</p><div class="grade">{figs}</div></section>'


def md_para_html(texto, n):
    texto = re.sub(r"^---\n.*?\n---\n", "", texto, flags=re.S)
    html = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    html = re.sub(r"<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S)  # o capítulo já tem título
    return html


def main():
    chrome = achar_chrome()
    logo_b = img64(RAIZ / "marca/logo/souto-logo-branco.png")
    logo_a = img64(RAIZ / "marca/logo/souto-logo-azul.png")
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    caps, sumario = [], []
    n = 0
    for arq, titulo, gals in CAPITULOS:
        p = GUIAS / arq
        if not p.exists():
            print(f"AVISO: falta {arq}, capítulo pulado")
            continue
        n += 1
        corpo = md_para_html(p.read_text(encoding="utf-8"), n)
        for chave, leg in gals:
            corpo += galeria(chave, leg)
        sumario.append(f'<li><span class="num">{n:02d}</span>{titulo}<span class="arq">docs/guias/{arq}</span></li>')
        caps.append(f'<section class="cap"><div class="abre"><span class="num">{n:02d}</span><h1>{titulo}</h1></div>{corpo}</section>')

    css = f"""
    @page {{ size: A4; margin: 18mm 16mm 20mm 16mm; }}
    @page :first {{ margin: 0; }}
    * {{ box-sizing: border-box; }} html, body {{ width: 100%; max-width: 100%; }} img {{ max-width: 100%; }}
    body {{ font-family: 'Inter', 'Segoe UI', Arial, sans-serif; color: {C['grafite']}; font-size: 10.5pt; line-height: 1.55; margin: 0; }}
    .capa {{ height: 296mm; width: 100%; padding: 26mm 22mm; overflow: hidden; color: #fff; page-break-after: always;
             background: linear-gradient(160deg, {C['preto']} 0%, {C['azul_noite']} 45%, {C['azul_royal']} 75%, {C['azul_eletrico']} 100%);
             display: flex; flex-direction: column; justify-content: space-between; }}
    .capa img {{ width: 70mm; }}
    .capa h1 {{ font-size: 34pt; line-height: 1.05; margin: 0 0 6mm; font-weight: 800; letter-spacing: -0.5px; }}
    .capa p {{ color: {C['nevoa']}; font-size: 12pt; margin: 0; }}
    .capa .rod {{ font-size: 9pt; color: {C['nevoa']}; border-top: 1px solid rgba(255,255,255,.35); padding-top: 4mm; }}
    .sumario {{ page-break-after: always; }}
    .sumario h1 {{ color: {C['azul_royal']}; font-size: 22pt; }}
    .sumario ol {{ list-style: none; padding: 0; }}
    .sumario li {{ display: flex; align-items: baseline; gap: 4mm; padding: 3.2mm 0; border-bottom: 1px solid {C['nevoa']}; font-size: 12.5pt; font-weight: 600; }}
    .sumario .num, .abre .num {{ color: {C['azul_eletrico']}; font-weight: 800; }}
    .sumario .arq {{ margin-left: auto; font-size: 8.5pt; color: #6b7184; font-weight: 400; font-family: Consolas, monospace; }}
    .cap {{ page-break-before: always; }}
    .abre {{ background: {C['azul_noite']}; color: #fff; padding: 9mm 8mm; border-radius: 3mm; margin-bottom: 7mm;
             border-left: 3mm solid {C['azul_eletrico']}; }}
    .abre .num {{ font-size: 13pt; display: block; color: {C['nevoa']}; }}
    .abre h1 {{ margin: 1mm 0 0; font-size: 22pt; }}
    h2 {{ color: {C['azul_royal']}; font-size: 14.5pt; margin: 8mm 0 2mm; padding-bottom: 1.5mm; border-bottom: 2px solid {C['nevoa']}; page-break-after: avoid; }}
    h3 {{ color: {C['azul_noite']}; font-size: 12pt; margin: 5mm 0 1.5mm; page-break-after: avoid; }}
    h4 {{ color: {C['azul_aco']}; margin: 4mm 0 1mm; }}
    a {{ color: {C['azul_eletrico']}; text-decoration: none; }}
    code {{ overflow-wrap: anywhere; font-family: Consolas, 'Cascadia Mono', monospace; font-size: 9pt; background: {C['papel']}; padding: .3mm 1.2mm; border-radius: 1mm; color: {C['azul_noite']}; }}
    pre {{ background: {C['azul_noite']}; color: #fff; padding: 3.5mm 4mm; border-radius: 2mm; white-space: pre-wrap; word-break: break-word; page-break-inside: avoid; }}
    pre code {{ background: none; color: #fff; padding: 0; }}
    table {{ border-collapse: collapse; width: 100%; table-layout: fixed; overflow-wrap: anywhere; margin: 3mm 0; font-size: 9pt; page-break-inside: auto; }}
    th {{ background: {C['azul_royal']}; color: #fff; text-align: left; padding: 2mm; }}
    td {{ padding: 1.8mm 2mm; border-bottom: 1px solid {C['nevoa']}; vertical-align: top; }}
    tr {{ page-break-inside: avoid; }}
    tr:nth-child(even) td {{ background: {C['papel']}; }}
    blockquote {{ margin: 3mm 0; padding: 2.5mm 4mm; background: {C['papel']}; border-left: 1.2mm solid {C['azul_eletrico']}; color: {C['azul_noite']}; }}
    .galeria {{ page-break-before: always; }}
    .galeria .leg {{ color: #6b7184; }}
    .grade {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }}
    figure {{ margin: 0; page-break-inside: avoid; }}
    figure img {{ width: 100%; border: 1px solid {C['nevoa']}; border-radius: 2mm; }}
    figcaption {{ font-size: 8pt; color: #6b7184; text-align: center; margin-top: 1mm; }}
    """
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Guia Souto Treinador</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>{css}</style></head><body>
    <section class="capa"><img src="{logo_b}">
      <div><p>SISTEMA SOUTO TREINADOR</p><h1>Guia de instalação,<br>uso, ferramentas<br>e boas práticas</h1>
      <p>Cérebro científico · Prescrição de treino · Roteiros · Carrosséis · Vídeo · Dieta e Painel ST</p></div>
      <div class="rod">Repositório: {REPO}<br>Versão de {hoje} · Jorge Souto, educador físico · Prescrição dietética: Lucas Melo, nutricionista RT</div>
    </section>
    <section class="sumario"><img src="{logo_a}" style="width:38mm"><h1>Sumário</h1><ol>{''.join(sumario)}</ol>
      <p>Cada capítulo é também um arquivo no repositório (coluna da direita): o Claude Code lê esses arquivos para responder às suas dúvidas.</p></section>
    {''.join(caps)}
    </body></html>"""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "guia.html").write_text(html, encoding="utf-8")
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
           f"--print-to-pdf={SAIDA}", (tmp / "guia.html").as_uri()]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    shutil.copy2(tmp / "guia.html", DOCS / "guia.html") if "--html" in sys.argv else None
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"PDF gerado: {SAIDA} ({SAIDA.stat().st_size / 1e6:.1f} MB) · {n} capítulos")


if __name__ == "__main__":
    main()
