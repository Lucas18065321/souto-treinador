"""Configuração comum da gestão Souto Treinador: lê config-st.json, resolve as pastas fora do repositório
(privado e alunos), o Chrome, a assinatura do RT e as chaves do Supabase (de supabase.env, na pasta privada).

Nada aqui grava arquivo. As chaves nunca são impressas.
"""
import json
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True
COMUM = os.path.dirname(os.path.abspath(__file__))
GESTAO = os.path.dirname(COMUM)                      # .../06 - GESTÃO DA CONSULTORIA
REPO = os.path.dirname(GESTAO)                        # raiz do repositório
ARQ_CONFIG = os.path.join(GESTAO, "config-st.json")


def _expandir(caminho):
    """%USERPROFILE% e ~ viram a pasta do usuário; barras viram as do sistema."""
    c = os.path.expandvars(os.path.expanduser(caminho or ""))
    if "%USERPROFILE%" in c:  # fora do Windows a variável pode não existir
        c = c.replace("%USERPROFILE%", os.path.expanduser("~"))
    return os.path.normpath(c.replace("\\", os.sep).replace("/", os.sep))


def carregar():
    with open(ARQ_CONFIG, encoding="utf-8") as f:
        return json.load(f)


CFG = carregar()
MARCA, PROF, RT = CFG["marca"], CFG["profissional"], CFG["rt"]


def caminho_repo(rel):
    """Caminho relativo a esta pasta (06 - GESTÃO DA CONSULTORIA) → absoluto."""
    return os.path.normpath(os.path.join(GESTAO, rel))


def pasta_privada():
    return _expandir(os.environ.get("ST_PRIVADO") or CFG["pastas"]["privado"])


def pasta_alunos():
    return _expandir(os.environ.get("ST_ALUNOS") or CFG["pastas"]["alunos"])


def assinatura_rt():
    """Caminho da imagem da assinatura do RT (fica FORA do repositório). None se não existir."""
    c = _expandir(os.environ.get("ST_ASSINATURA_RT") or CFG["pastas"]["assinatura_rt"])
    return c if os.path.isfile(c) else None


def logo(tipo="branco"):
    c = caminho_repo(MARCA.get(f"logo_{tipo}") or MARCA["logo_branco"])
    return c if os.path.isfile(c) else None


def nome_de_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*]', "", str(nome)).strip(" .")


def pasta_do_aluno(nome, sub=None, criar=True):
    """%USERPROFILE%\\SoutoTreinador\\Alunos\\<nome do aluno>[\\sub]. Dado de aluno fica só aqui (fora do repositório e do OneDrive)."""
    p = os.path.join(pasta_alunos(), nome_de_arquivo(nome), *( [sub] if sub else []))
    if criar:
        os.makedirs(p, exist_ok=True)
    return p


def chrome():
    """Chrome (ou Edge) para gerar PDF e abrir o painel: variável CHROME, caminhos de sempre ou o PATH."""
    candidatos = [os.environ.get("CHROME", "")]
    for var, partes in (("PROGRAMFILES", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("PROGRAMFILES(X86)", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("LOCALAPPDATA", ("Google", "Chrome", "Application", "chrome.exe")),
                        ("PROGRAMFILES(X86)", ("Microsoft", "Edge", "Application", "msedge.exe")),
                        ("PROGRAMFILES", ("Microsoft", "Edge", "Application", "msedge.exe"))):
        if os.environ.get(var):
            candidatos.append(os.path.join(os.environ[var], *partes))
    candidatos += [shutil.which(n) or "" for n in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge")]
    candidatos += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in candidatos:
        if c and os.path.isfile(c):
            return c
    return None


def ler_env(caminho=None):
    """Lê o supabase.env (CHAVE=valor por linha). Variáveis de ambiente com o mesmo nome passam por cima."""
    caminho = caminho or _expandir(os.environ.get("ST_SUPABASE_ENV") or CFG["pastas"]["supabase_env"])
    vals = {}
    if os.path.isfile(caminho):
        with open(caminho, encoding="utf-8-sig") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                k, v = linha.split("=", 1)
                vals[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_BUCKET", "RT_PIN_HASH"):
        if os.environ.get(k):
            vals[k] = os.environ[k]
    vals["_arquivo"] = caminho
    return vals


def rodape_profissional():
    """'Souto Treinador · Jorge Souto · CREF … · @…' (o que estiver vazio não sai)."""
    partes = [MARCA["nome"], PROF["nome"], PROF.get("registro"), PROF.get("arroba")]
    return " · ".join(p for p in partes if p)
