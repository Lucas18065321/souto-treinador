"""Editor visual dos carrosséis (os 4 modelos). Abre cada slide HTML no navegador e deixa mexer em TODOS os elementos:
texto (direto no slide, com negrito/itálico/destaque), posição, tamanho, fonte, cor, alinhamento, camadas, opacidade,
imagem (trocar, enquadrar, zoom, recortar o fundo) e fundo do slide. Exporta o PNG 2160x2700 pelo mesmo Chrome do
gerador (mesma fonte, mesmo grão, mesmo degradê) e roda a verificação de diagramação (ALERTAS).

Uso:  python editor.py [--porta 8765] [--abrir]      →  http://localhost:8765/editor
Só escuta em 127.0.0.1 (nada sai da máquina). "Salvar" grava por cima de html/slide-NN.html com a marca data-editado:
daí em diante o render_carrossel.py não sobrescreve esse slide (só com --refazer).
"""
import base64
import glob
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import webbrowser
import zipfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)  # 03 - CARROSSÉIS E ARTE
CARROSSEIS = os.path.join(RAIZ, "Carrosséis")
sys.path.insert(0, AQUI)
sys.dont_write_bytecode = True  # sem __pycache__ no Gerador (regra de zero lixo)
import render_carrossel as R  # noqa: E402
from comum import aparar, recortar  # noqa: E402

TIPOS_IMG = {".png", ".jpg", ".jpeg", ".webp"}


def dentro(u):
    """Endereço do site (/Carrosséis/...) → caminho absoluto, sempre dentro de 03 - CARROSSÉIS E ARTE."""
    u = urllib.parse.urlsplit(u).path
    p = os.path.normpath(os.path.join(RAIZ, urllib.parse.unquote(u).lstrip("/\\")))
    if os.path.commonpath([p, RAIZ]) != RAIZ:
        raise ValueError("caminho fora da pasta do editor")
    return p


def site(p):
    return "/" + urllib.parse.quote(os.path.relpath(p, RAIZ).replace("\\", "/"))


def relativo(p, slide):
    """Caminho de um arquivo relativo à pasta html/ do slide (funciona no Chrome local e no editor)."""
    return urllib.parse.quote(os.path.relpath(p, os.path.dirname(slide)).replace("\\", "/"), safe="/._-~")


def slide_html(arquivo):
    p = dentro(arquivo)
    if not re.fullmatch(r"slide-\d+\.html", os.path.basename(p)) or os.path.basename(os.path.dirname(p)) != "html":
        raise ValueError("arquivo de slide inválido")
    return p


def png_do(h):
    return os.path.join(os.path.dirname(os.path.dirname(h)), os.path.basename(h).replace(".html", ".png"))


def carrosseis():
    grupos = {}
    for h in glob.glob(os.path.join(CARROSSEIS, "**", "html", "slide-*.html"), recursive=True):
        grupos.setdefault(os.path.dirname(os.path.dirname(h)), []).append(h)
    out = []
    for pasta, hs in grupos.items():
        hs.sort()
        nome = os.path.relpath(pasta, CARROSSEIS).replace("\\", "/")
        out.append({"nome": nome, "pasta": site(pasta), "slides": [site(h) for h in hs],
                    "pngs": [site(png_do(h)) if os.path.exists(png_do(h)) else "" for h in hs],
                    "editados": [R.editado(h) for h in hs], "_t": max(os.path.getmtime(h) for h in hs), "_teste": nome.startswith("_")})
    out.sort(key=lambda c: (c["_teste"], -c["_t"]))
    return out


def exportar(h):
    png = png_do(h)
    ok = R.fotografar(h, png)
    al = R.verificar(h)
    return {"png": site(png) + f"?v={int(time.time())}" if ok else "", "ok": ok,
            "alertas": al if al is not None else ["verificação visual não rodou (confira o slide a olho)"]}


def pasta_artes(h):
    saida = os.path.dirname(os.path.dirname(h))
    for p in (os.path.join(saida, "artes"), os.path.join(os.path.dirname(saida), "artes")):
        if os.path.isdir(p):
            return p
    p = os.path.join(saida, "artes")
    os.makedirs(p, exist_ok=True)
    return p


class Editor(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, dados, cod=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(cod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        try:
            if u.path in ("/", "/editor"):
                with open(os.path.join(AQUI, "editor.html"), "rb") as fh:
                    corpo = fh.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
            elif u.path == "/api/carrosseis":
                self._json({"carrosseis": carrosseis()})
            elif u.path == "/api/zip":
                pasta = dentro(urllib.parse.parse_qs(u.query)["pasta"][0])
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as z:
                    for p in sorted(glob.glob(os.path.join(pasta, "slide-*.png"))):
                        z.write(p, os.path.basename(p))
                corpo = buf.getvalue()
                nome = urllib.parse.quote(os.path.basename(pasta) + ".zip")
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{nome}")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
            elif re.search(r"/html/slide-\d+\.html$", u.path):
                # slide antigo com endereços file:/// → relativos (abre igual no editor e no Chrome local)
                h = slide_html(u.path)
                with open(h, encoding="utf-8") as fh:
                    doc = fh.read()
                corpo = R.relativizar(doc, os.path.dirname(h)).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
            else:
                super().do_GET()
        except Exception as e:  # noqa: BLE001
            self._json({"erro": str(e)}, 400)

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            d = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            rota = urllib.parse.urlsplit(self.path).path
            if rota == "/api/salvar":
                h = slide_html(d["arquivo"])
                with open(h, "w", encoding="utf-8") as fh:
                    fh.write(d["html"])
                self._json({"ok": True})
            elif rota == "/api/exportar":
                self._json(exportar(slide_html(d["arquivo"])))
            elif rota == "/api/exportar-todos":
                pasta = dentro(d["pasta"])
                res = [dict(exportar(h), n=k) for k, h in enumerate(sorted(glob.glob(os.path.join(pasta, "html", "slide-*.html"))), 1)]
                subprocess.run([sys.executable, os.path.join(AQUI, "folha.py"), pasta], capture_output=True, timeout=120)
                self._json({"slides": res, "folha": site(os.path.join(pasta, "folha.jpg")) + f"?v={int(time.time())}"})
            elif rota == "/api/enviar":
                h = slide_html(d["arquivo"])
                ext = os.path.splitext(d["nome"])[1].lower()
                if ext not in TIPOS_IMG:
                    raise ValueError("use PNG, JPG ou WEBP")
                base = re.sub(r"[^\w.-]+", "-", os.path.splitext(os.path.basename(d["nome"]))[0]).strip("-") or "arte"
                destino, k = os.path.join(pasta_artes(h), base + ext), 2
                while os.path.exists(destino):
                    destino, k = os.path.join(pasta_artes(h), f"{base}-{k}{ext}"), k + 1
                with open(destino, "wb") as fh:
                    fh.write(base64.b64decode(d["dados"].split(",", 1)[-1]))
                self._json({"src": relativo(destino, h)})
            elif rota == "/api/recortar":
                h = slide_html(d["arquivo"])
                origem = dentro(d["imagem"])
                if os.path.splitext(origem)[1].lower() not in TIPOS_IMG or not os.path.exists(origem):
                    raise ValueError("imagem não encontrada")
                saida = aparar(recortar(origem, modo=d.get("modo", "tinta")))
                self._json({"src": relativo(saida, h), "original": relativo(origem, h)})
            else:
                self._json({"erro": "rota desconhecida"}, 404)
        except Exception as e:  # noqa: BLE001
            self._json({"erro": str(e)}, 400)


def main():
    porta = int(sys.argv[sys.argv.index("--porta") + 1]) if "--porta" in sys.argv else 8765
    srv = ThreadingHTTPServer(("127.0.0.1", porta), partial(Editor, directory=RAIZ))
    url = f"http://localhost:{porta}/editor"
    print(f"Editor de carrossel: {url}   (Ctrl+C para fechar)", flush=True)
    if "--abrir" in sys.argv:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
