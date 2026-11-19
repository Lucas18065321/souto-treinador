"""Hook PostToolUse (Write|Edit): valida a peça assim que ela é salva e devolve os erros ao modelo.

  02 - ROTEIROS/Roteiros/*.md                          → 02 - ROTEIROS/_SISTEMA/validar_roteiro.py
  02 - ROTEIROS/_SISTEMA/teste/Roteiro*.md             → o mesmo validador (teste do motor, com Ficha fictícia)
  03 - CARROSSÉIS E ARTE/Carrosséis/**/carrossel.json  → 03 - CARROSSÉIS E ARTE/Gerador/validar_carrossel.py
  <projeto de vídeo>/03_roteiro/edicao.json            → node "04 - EDIÇÃO DE VÍDEO/motor/scripts/validar-edicao.mjs" --hook
                                                         (os projetos de vídeo podem morar fora do repositório; só roda
                                                         se o script existir e o Node estiver instalado)

Qualquer outro arquivo: sai calado. Frente ausente (pasta, validador ou Node que não existe): sai calado, nunca quebra.
Com ERRO → {"decision": "block", "reason": relatório} (o modelo, inclusive um subagente, recebe e corrige).
Só AVISO → vai como contexto adicional. Os validadores Python precisam expor validar(caminho) → (E, A, info) e
relatorio(nome, E, A, info) → str.

Caminhos relativos a este arquivo (a raiz do repositório é a pasta acima de .claude): funciona em qualquer computador.
Registro no .claude/settings.json da raiz (ver docs/guias/02-roteiros.md, seção "Hook").
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
VALIDAR_EDICAO = RAIZ / "04 - EDIÇÃO DE VÍDEO" / "motor" / "scripts" / "validar-edicao.mjs"


def _n(t):
    return unicodedata.normalize("NFC", t).lower()


# (trecho do caminho em minúsculas, como o resto do caminho começa (ou ""), final do caminho, validador Python)
ALVOS = [
    ("/02 - roteiros/roteiros/", "", ".md", RAIZ / "02 - ROTEIROS" / "_SISTEMA" / "validar_roteiro.py"),
    ("/02 - roteiros/_sistema/teste/", "roteiro", ".md", RAIZ / "02 - ROTEIROS" / "_SISTEMA" / "validar_roteiro.py"),
    ("/03 - carrosséis e arte/carrosséis/", "", "/carrossel.json",
     RAIZ / "03 - CARROSSÉIS E ARTE" / "Gerador" / "validar_carrossel.py"),
]


def saida(obj):
    print(json.dumps(obj, ensure_ascii=True))


def alvo_de(caminho):
    """Validador Python do arquivo salvo, ou None (arquivo de fora, pasta _arquivo, frente ausente)."""
    p = "/" + _n(caminho.replace("\\", "/")).lstrip("/")  # caminho relativo também vale
    if "/_arquivo/" in p:
        return None
    for trecho, comeco, final, script in ALVOS:
        t = _n(trecho)
        i = p.find(t)
        if i < 0 or not p.endswith(final):
            continue
        resto = p[i + len(t):]
        if comeco and not resto.startswith(comeco):
            continue
        if final == ".md" and "/" in resto:  # Roteiros/*.md: só o nível de cima
            continue
        return script if script.is_file() else None
    return None


def validar_edicao(bruto):
    """Repassa o JSON do hook ao validador de vídeo (Node), que já fala o protocolo do hook. Calado se faltar algo."""
    node = shutil.which("node")
    if not node or not VALIDAR_EDICAO.is_file():
        return
    try:
        r = subprocess.run([node, str(VALIDAR_EDICAO), "--hook"], input=bruto, capture_output=True, timeout=110,
                           cwd=str(VALIDAR_EDICAO.parents[1]))
    except (OSError, subprocess.TimeoutExpired) as e:
        saida({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                      "additionalContext": f"validar-edicao.mjs não rodou ({type(e).__name__}); rode-o à mão."}})
        return
    out = r.stdout.decode("utf-8", "replace").strip()
    if out:
        print(out)


def main():
    bruto = sys.stdin.buffer.read()
    try:
        texto = bruto.decode("utf-8-sig")
    except UnicodeDecodeError:  # teste à mão no PowerShell 5.1 sem $OutputEncoding UTF-8 manda cp1252
        texto = bruto.decode("cp1252", "replace")
        bruto = texto.encode("utf-8")
    try:
        dados = json.loads(texto or "{}")
    except ValueError:
        return
    cam = (dados.get("tool_input") or {}).get("file_path") or (dados.get("tool_response") or {}).get("filePath") or ""
    if not cam:
        return
    if _n(cam.replace("\\", "/")).endswith("/03_roteiro/edicao.json"):
        validar_edicao(bruto)
        return
    script = alvo_de(cam)
    if script is None:
        return
    try:
        spec = importlib.util.spec_from_file_location(script.stem, script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        E, A, info = mod.validar(cam)
        rel = mod.relatorio(Path(cam).name, E, A, info)
    except Exception as e:  # validador quebrado não pode travar o trabalho
        saida({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                      "additionalContext": f"{script.name} falhou ({type(e).__name__}: {e}); rode-o à mão."}})
        return
    if E:
        saida({"decision": "block",
               "reason": rel + "\nCorrija TODOS os ERROS e salve o arquivo de novo (o validador roda sozinho a cada gravação)."})
    else:  # sem erro: avisos completos, ou só a linha de resumo (para o modelo saber que passou)
        saida({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                      "additionalContext": rel if A else f"{script.stem}: " + rel.splitlines()[-1]}})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
