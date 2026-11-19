"""Folha rápida dos recortes, ANTES do render (2026-10-21: acelerar o carrossel).

Uso: python conferir_recortes.py <carrossel.json>
Recorta cada arte que o layout usa como recorte, com os mesmos parâmetros do render (modo pelo fundo ou "modo_recorte",
"recorte_buracos"), e monta <pasta>/recortes.jpg: cada recorte sobre fundo escuro (M1, M4) e sobre xadrez (mostra o que
ficou transparente). Leva segundos. Confira ali halo, borda comida, fundo preso em vão, parte transparente que sumiu
(tubo, gota, jato) e buraco no sujeito; corrija a arte ou o JSON e só então rode o render_carrossel.py.
Fotos inteiras (capa A do M4, "mistura": "cena", "tratamento": "cena", fotos do M3, M5) ficam de fora: não são recortadas.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comum  # noqa: E402

CENA = ("cena", "clarear", "multiplicar")


def recortes_do_slide(modelo, s):
    """Lista (campo, sufixo do modo) das artes do slide que viram recorte no layout."""
    if s.get("mistura") in CENA or s.get("tratamento") == "cena" or modelo == "brandsdecoded":
        return []
    tipo = s.get("tipo")
    if modelo == "cinema" and tipo == "capa":
        return []
    if modelo == "dossie" and (tipo in ("manchete", "foto", "cta") or (tipo == "capa" and s.get("fundo") == "foto")):
        return []
    return [(c, "2" if c == "imagem2" else "") for c in ("imagem", "imagem2") if s.get(c)]


def main():
    from PIL import Image, ImageDraw
    cam = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cam)
    C = json.load(open(cam, encoding="utf-8"))
    modelo = C.get("modelo", "manga-dark")
    tiles, LADO = [], 420
    for i, s in enumerate(C["slides"], 1):
        for campo, suf in recortes_do_slide(modelo, s):
            arq = comum.caminho(s[campo], base)
            if not arq or not os.path.exists(arq):
                print(f"   FALTA slide-{i:02d} {campo}: {s[campo]}")
                continue
            modo = s.get("modo_recorte" + suf) or s.get("modo_recorte") or s.get("recorte_modo") or "auto"
            if modo == "auto":
                modo = comum.modo_pelo_fundo(arq)
            rec = Image.open(comum.aparar(comum.recortar(arq, modo=modo, buracos=bool(s.get("recorte_buracos"))))).convert("RGBA")
            rec.thumbnail((LADO - 20, LADO - 50))
            par = Image.new("RGB", (LADO * 2, LADO), (20, 20, 20))
            xadrez = Image.new("RGB", (LADO, LADO), (255, 255, 255))
            d = ImageDraw.Draw(xadrez)
            for yy in range(0, LADO, 20):
                for xx in range(0, LADO, 20):
                    if (xx + yy) // 20 % 2:
                        d.rectangle([xx, yy, xx + 19, yy + 19], fill=(205, 205, 205))
            par.paste(xadrez, (LADO, 0))
            for ox in (0, LADO):
                par.paste(rec, (ox + (LADO - rec.width) // 2, 40 + (LADO - 50 - rec.height) // 2), rec)
            ImageDraw.Draw(par).text((10, 10), f"slide {i:02d} · {campo} · {modo}" + (" · buracos" if s.get("recorte_buracos") else ""),
                                     fill=(255, 170, 120))
            tiles.append(par)
            print(f"   ok slide-{i:02d} {campo} ({modo})")
    if not tiles:
        print("Nenhuma arte de recorte neste carrossel.")
        return
    col = 2
    lin = (len(tiles) + col - 1) // col
    folha = Image.new("RGB", (LADO * 2 * col, LADO * lin), (40, 40, 40))
    for k, t in enumerate(tiles):
        folha.paste(t, ((k % col) * LADO * 2, (k // col) * LADO))
    saida = os.path.join(base, "recortes.jpg")
    folha.save(saida, quality=88)
    print(f"Folha dos recortes: {saida}")


if __name__ == "__main__":
    main()
