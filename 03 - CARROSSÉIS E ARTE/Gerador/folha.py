"""Folha de contato de um carrossel renderizado (para a conferência visual de TODOS os slides de uma vez).

Uso: python folha.py "caminho/da/pasta/do/carrossel"   → gera folha.jpg na mesma pasta
     python folha.py "pastaA" "pastaB" --saida "x.jpg"  → uma folha só com as pastas em sequência (cada pasta começa numa
                                                          linha nova, com o nome dela em cima); serve para juntar os
                                                          testes de vários modelos numa folha só
O número de cada slide fica numa faixa ACIMA da miniatura, para não cobrir nada do slide (barra da marca, cantos, texto).
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

args = [a for a in sys.argv[1:] if not a.startswith("--saida")]
saida_arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--saida=")), None)
if "--saida" in sys.argv[1:]:
    k = sys.argv.index("--saida")
    saida_arg = sys.argv[k + 1]
    args = [a for a in args if a != saida_arg]
pastas = [os.path.abspath(p) for p in args]
cols, w, h, gap, faixa = 3, 480, 600, 12, 26
titulo = 44 if len(pastas) > 1 else 0  # nome da pasta em cima de cada bloco, só na folha de várias pastas
blocos = [(p, sorted(glob.glob(os.path.join(p, "slide-*.png")))) for p in pastas]
altura = sum(titulo + ((len(s) + cols - 1) // cols) * (faixa + h + gap) for _, s in blocos) - gap
F = Image.new("RGB", (cols * (w + gap) - gap, max(altura, 10)), "white")
D = ImageDraw.Draw(F)
try:
    fonte = ImageFont.truetype(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "arialbd.ttf"), 24)
except OSError:
    fonte = None
y0 = 0
for pasta, slides in blocos:
    if titulo:
        D.text((4, y0 + 10), os.path.basename(pasta), fill="black", font=fonte)
        y0 += titulo
    for k, p in enumerate(slides):
        x, y = (k % cols) * (w + gap), y0 + (k // cols) * (faixa + h + gap)
        D.rectangle([x, y + 3, x + 34, y + faixa - 3], fill="magenta")
        D.text((x + 8, y + 7), str(k + 1), fill="white")
        F.paste(Image.open(p).convert("RGB").resize((w, h)), (x, y + faixa))
    y0 += ((len(slides) + cols - 1) // cols) * (faixa + h + gap)
saida = os.path.abspath(saida_arg) if saida_arg else os.path.join(pastas[0], "folha.jpg")
F.save(saida, quality=88)
print(saida)
