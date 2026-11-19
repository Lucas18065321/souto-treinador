#!/usr/bin/env python3
"""Gera o ícone do Painel ST: o monograma "ST" branco num quadrado arredondado com o degradê azul da marca
(#2E49CE → #1F33A3 → #141A3D). Saída: icone.ico (atalho da área de trabalho) e web/icone.png (janela e barra de tarefas).

Só precisa rodar de novo se quiser mudar o ícone. Precisa do Pillow (pip install pillow), que só é usado aqui.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
LADO = 1024
CORES = [(0x2E, 0x49, 0xCE), (0x1F, 0x33, 0xA3), (0x14, 0x1A, 0x3D)]


def fonte(tam):
    """Fonte grossa e condensada (lembra o logo). Tenta a Bahnschrift do Windows; senão, Segoe UI Black/Bold; senão, a padrão."""
    pasta = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    try:
        f = ImageFont.truetype(os.path.join(pasta, "bahnschrift.ttf"), tam)
        try:
            f.set_variation_by_name("Bold Condensed")
        except Exception:
            f.set_variation_by_axes([700, 75])
        return f
    except Exception:
        pass
    for nome in ("seguibl.ttf", "segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(os.path.join(pasta, nome) if os.path.isdir(pasta) else nome, tam)
        except Exception:
            continue
    return ImageFont.load_default()


def degrade(lado):
    """Degradê diagonal (canto de cima à esquerda → canto de baixo à direita) em 3 paradas."""
    g = Image.new("RGB", (lado, lado))
    px = g.load()
    for y in range(lado):
        for x in range(lado):
            t = (x + y) / (2 * (lado - 1))
            a, b, u = (CORES[0], CORES[1], t / 0.55) if t < 0.55 else (CORES[1], CORES[2], (t - 0.55) / 0.45)
            px[x, y] = tuple(round(a[i] + (b[i] - a[i]) * u) for i in range(3))
    return g


def main():
    base = degrade(256).resize((LADO, LADO), Image.BICUBIC).convert("RGBA")
    mascara = Image.new("L", (LADO, LADO), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, LADO - 1, LADO - 1], radius=int(LADO * 0.23), fill=255)
    icone = Image.new("RGBA", (LADO, LADO), (0, 0, 0, 0))
    icone.paste(base, (0, 0), mascara)
    # brilho suave no topo (vidro)
    brilho = Image.new("L", (LADO, LADO), 0)
    ImageDraw.Draw(brilho).ellipse([-LADO * 0.3, -LADO * 0.75, LADO * 1.1, LADO * 0.42], fill=16)
    branco = Image.new("RGBA", (LADO, LADO), (255, 255, 255, 255))
    icone.paste(branco, (0, 0), Image.composite(brilho, Image.new("L", (LADO, LADO), 0), mascara))
    d = ImageDraw.Draw(icone)
    f = fonte(int(LADO * 0.56))
    texto = "ST"
    caixa = d.textbbox((0, 0), texto, font=f)
    w, h = caixa[2] - caixa[0], caixa[3] - caixa[1]
    d.text(((LADO - w) / 2 - caixa[0], (LADO - h) / 2 - caixa[1] + LADO * 0.01), texto, font=f, fill=(255, 255, 255, 255))
    os.makedirs(os.path.join(AQUI, "web"), exist_ok=True)
    icone.resize((512, 512), Image.LANCZOS).save(os.path.join(AQUI, "web", "icone.png"), optimize=True)
    tamanhos = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    try:  # BMP nos tamanhos pequenos: o Explorer do Windows nem sempre mostra ícone só em PNG
        icone.save(os.path.join(AQUI, "icone.ico"), sizes=tamanhos, bitmap_format="bmp")
    except TypeError:
        icone.save(os.path.join(AQUI, "icone.ico"), sizes=tamanhos)
    print("ícone gerado: icone.ico e web/icone.png")


if __name__ == "__main__":
    sys.exit(main())
