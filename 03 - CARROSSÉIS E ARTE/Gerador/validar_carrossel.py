"""Valida o texto de um carrossel (carrossel.json) contra a Ficha de conteúdo e as regras editoriais do método
BrandsDecoded, antes de gerar artes e renderizar. Só biblioteca padrão. Não mexe na diagramação: só lê o JSON.

Uso:
  python validar_carrossel.py "<pasta>/carrossel.json"                   ERROS/AVISOS; código 1 se houver erro
  python validar_carrossel.py "<pasta>/carrossel.json" --montar-fontes   valida e, se passar, escreve "## Fontes" e
                                                                         "## Nível de certeza" no carrossel.md da pasta

Campos extras no JSON (os geradores ignoram o que não usam):
  no topo   "ficha": "<Tema> - Ficha"   (o nome antigo "Ficha - <tema>" também vale)
            "tipo_carrossel": "tendencia|tese|tese-mito|case|previsao" · "eixo" · "funil": "topo|meio|fundo" ·
            "headline": "<headline completa>" · "cta": {"tipo": "consultoria|ebook", "beneficio"} (consultoria = treino
            individualizado com o Jorge; ebook só se ele tiver um material próprio)
            (no M5 o "cta" pode ficar dentro do slide de CTA). Ausentes = AVISO: carrossel antigo continua válido.
  por slide "funcao": "capa|hook|mecanismo|prova|expansao|aplicacao|direcao|cta" (papel na anatomia BD; usado na voz
            mista: a 2ª pessoa só pode no slide de aplicação e no CTA). Ausente = AVISO.
            "afirmacoes": [6, 7, "N1"] em cada slide com afirmação científica ou número (nº da tabela "Afirmações prontas";
            N1… = "Números de impacto"; M1… = "Mitos"; H1… = "Histórias reais").
O texto do slide NÃO leva [#n] (apareceria na arte): a referência fica só em "afirmacoes".

Confere, slide a slide, em todos os campos de texto (os de sempre + os do M5: headline, tag, titulo, ponte, setas,
componente.*, cta.*; lista CAMPOS_TEXTO do editorial.py):
  · limites de caracteres do modelo: LIMITES/limites() do render_carrossel.py, os mesmos do render (no M5: por bloco,
    célula e item, máx. 2 blocos, imagem_fundo só no dark)
  · evidência (02 - ROTEIROS/_SISTEMA/validar_roteiro.py, módulo compartilhado): ids existem na ficha · verbo calibrado
    pela certeza · números só da(s) linha(s) citada(s) · palavras proibidas. A "tag" (rótulo de seção, "COMO FUNCIONA")
    só entra no verbo × certeza e nos números se tiver algarismo; nas palavras proibidas entra sempre.
  · regras editoriais BD (editorial.py): estruturas binárias, cacoetes de IA, "de forma X", dados vagos, anglicismo
    numérico, aberturas/fechos proibidos, CTA cordial, headline proibida = ERRO; 2ª pessoa fora da aplicação/CTA,
    jargão, tom de coach, slide sem "funcao", campos de topo ausentes, CTA × funil e as regras do M5 (palavras por
    fundo, 3 fundos iguais seguidos, tabela < 3 linhas, CTA sem ponte) = AVISO. Lista completa no topo do editorial.py.
Sem "ficha" no topo: ERRO, e a evidência não é conferida (limites e regras editoriais rodam assim mesmo).
A ética (CONFEF, nutrição fora da competência, remédio/hormônio) e as palavras proibidas valem em todos os campos.

Dependência: o módulo de evidência é compartilhado com a frente de roteiros (../../02 - ROTEIROS/_SISTEMA/validar_roteiro.py,
caminho relativo a este arquivo). As Fichas ficam em ../../01 - BASE CIENTÍFICA/**/<Tema> - Ficha.md.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # sem __pycache__ no Gerador (regra de zero lixo)
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from render_carrossel import LIMITES, limites  # noqa: E402
import editorial as ED  # noqa: E402

_VR_CAM = AQUI.parents[1] / "02 - ROTEIROS" / "_SISTEMA" / "validar_roteiro.py"
if not _VR_CAM.is_file():
    sys.exit(f"validar_carrossel: falta o módulo de evidência {_VR_CAM} (frente 02 - ROTEIROS). Baixe o repositório inteiro: "
             "o validador do carrossel usa o mesmo conferidor de Ficha dos roteiros.")
_spec = importlib.util.spec_from_file_location("validar_roteiro", _VR_CAM)
VR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VR)

# Campos de texto que aparecem na arte (posições, imagens e números de layout ficam de fora). Lista única no editorial.py.
TEXTO = ED.CAMPOS_TEXTO
# Rótulo de seção ("COMO FUNCIONA", "O QUE MUDA"): não é afirmação, então só entra na conferência de verbo/número se
# tiver algarismo. Palavras proibidas valem sempre.
ROTULOS = ED.ROTULOS


def textos(s):
    """Todos os textos do slide (desce em componente.*, cta.*, setas…)."""
    return [v for _, v in ED.campos_de_texto(s)]


def textos_de_evidencia(s, modelo=None):
    """Os textos que passam pela conferência com a ficha (verbo × certeza, números): tudo, menos rótulo sem número."""
    out = []
    for c, v in ED.campos_de_texto(s):
        if re.match(r"[a-z_]+", c).group(0) in ROTULOS and not re.search(r"\d", v):
            continue
        out.append(v)
    return out


# As mensagens de evidência vêm do validar_roteiro (onde o [#n] vai no texto). No carrossel o id vai em "afirmacoes".
_TRADUCAO = [
    ("(ponha o [#n] logo depois)", '(liste o id da linha em "afirmacoes"; nunca [#n] no texto do slide)'),
    ("se for afirmação, marque", 'se for afirmação, liste o id em "afirmacoes"'),
    ("cite a linha da ficha", 'liste o id da linha da ficha em "afirmacoes"'),
    (" sem [#n]", ' sem id em "afirmacoes"'),
]


def _traduzir(msg):
    for a, b in _TRADUCAO:
        msg = msg.replace(a, b)
    return msg


def _ordem(msg):
    """Mensagens do carrossel inteiro primeiro; depois por slide, na ordem em que foram achadas."""
    m = re.match(r"slide-(\d+)", msg)
    return (1, int(m.group(1))) if m else (0, 0)


def validar(caminho):
    E, A = [], []
    try:
        C = json.loads(Path(caminho).read_text(encoding="utf-8-sig"))
    except Exception as e:
        return [f"JSON inválido: {e}"], [], {}
    if not isinstance(C, dict):
        return ["JSON inválido: o topo tem de ser um objeto { … }"], [], {}
    modelo = C.get("modelo", "manga-dark")
    if modelo not in LIMITES:
        E.append(f"modelo '{modelo}' desconhecido (válidos: {', '.join(LIMITES)})")
    cam_ficha, msg = VR.achar_ficha(C.get("ficha"))
    ficha = VR.carregar_ficha(cam_ficha) if cam_ficha else None
    if not ficha:
        E.append((msg if str(C.get("ficha") or "").strip() else 'falta "ficha" no topo do JSON')
                 + ' — no topo do JSON: "ficha": "<Tema> - Ficha" (sem ela, a evidência não foi conferida)')
    usados = []
    slides = [s for s in (C.get("slides") or []) if isinstance(s, dict)]
    for n, s in enumerate(slides, 1):
        p = ED.prefixo(n, s)
        campos = textos(s)
        if any("[#" in t for t in campos):
            E.append(f'{p}: [#n] no texto apareceria na arte — tire do texto e liste em "afirmacoes"')
        texto = re.sub(r"\[#[^\]]*\]", "", ". ".join(ED.limpar(t) for t in textos_de_evidencia(s, modelo)))
        todo = re.sub(r"\[#[^\]]*\]", "", ". ".join(ED.limpar(t) for t in campos))
        E += [f"{p}: {x}" for x in limites(modelo, s)]
        bruto = s.get("afirmacoes") or []
        ids = [str(x).strip().lstrip("#").upper() for x in (bruto if isinstance(bruto, list) else [bruto])]
        for i in [i for i in ids if not re.fullmatch(r"\d+|[NMH]\d+", i)]:
            E.append(f'{p}: referência inválida "{i}" em "afirmacoes" (use 6, "N1", "M2" ou "H1" = história real)')
        ids = [i for i in ids if re.fullmatch(r"\d+|[NMH]\d+", i)]
        if ficha:
            e, a = VR.checar_trecho(texto, ids, ficha) if ids else VR.checar_sem_referencia(texto)
            E += [f"{p}: {_traduzir(x)}" for x in e]
            A += [f"{p}: {_traduzir(x)}" for x in a]
            usados += [i for i in ids if i in ficha["itens"] and i not in usados]
        e2, a2 = VR.checar_proibidas(todo)
        E += [f"{p}: {x}" for x in e2]
        A += [f"{p}: {x}" for x in a2]
    if not slides:
        E.append('JSON sem "slides"')
    elif ficha and not usados:
        A.append('nenhum slide com "afirmacoes": o carrossel não cita a ficha')
    e, a = ED.validar(C)
    E = sorted(E + e, key=_ordem)
    A = sorted(A + a, key=_ordem)
    return E, A, {"ficha": ficha, "usados": usados, "slides": len(slides)}


def relatorio(nome, E, A, info):
    linhas = [f"validar_carrossel · {nome}" + (f" · {info['ficha']['nome']}" if info.get("ficha") else "")]
    linhas += [f"ERRO  {x}" for x in E] + [f"AVISO {x}" for x in A]
    resumo = f"{len(E)} erro(s), {len(A)} aviso(s)"
    if info.get("slides"):
        resumo += f" · {info['slides']} slides · refs: {', '.join('#' + i for i in info['usados']) or '—'}"
    return "\n".join(linhas + [resumo])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    caminho = Path(args[0])
    E, A, info = validar(caminho)
    print(relatorio(caminho.parent.name + "/" + caminho.name, E, A, info))
    if "--montar-fontes" in sys.argv:
        if E:
            print("\nFontes NÃO montadas: corrija os erros primeiro.")
        else:
            md_cam = caminho.parent / "carrossel.md"
            md = md_cam.read_text(encoding="utf-8-sig") if md_cam.exists() else f"# Carrossel · {caminho.parent.name}\n"
            bloco, notas, av = VR.montar_secoes(info["ficha"], info["usados"])
            md_cam.write_text(VR.atualizar_fontes_fm(VR.substituir_secoes(md, bloco), notas), encoding="utf-8")
            for x in av:
                print(f"AVISO {x}")
            print(f"\nFontes e Nível de certeza escritos em {md_cam.name} ({len(notas)} nota(s)-base).")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
