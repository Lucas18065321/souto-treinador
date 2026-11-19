"""Primeira carga da base: coloca a coleção de treino de força na fila e baixa o texto completo de acesso aberto.

Uso (da raiz do repositório):
    python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/baixar_colecao.py"            # mostra o plano (não baixa nada)
    python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/baixar_colecao.py" --baixar   # baixa e cataloga (~15 min)

- `colecao-treino.jsonl` (nesta pasta) tem os metadados dos artigos: curadoria de volume, carga, RIR, periodização,
  autorregulação, deload e monitoramento + os artigos de treino de força de Schoenfeld, Jonato Prestes, Belmiro F. de Salles,
  Thiago B. Trindade e Santiago T. Paes (levantados no Europe PMC em 2026-11-19).
- Só o texto de ACESSO ABERTO é baixado (PMC). Os pagos vão para `_MÁQUINA/para-baixar.md`: baixe pelo seu acesso
  (CAPES, universidade) e solte o PDF em `ENTRADA/`; o `catalogar` reconhece pelo DOI.
- Pode rodar de novo quando quiser: o que já foi baixado é pulado.
"""
import json
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
AQUI = Path(__file__).resolve().parent
MAQ = AQUI.parent
sys.path.insert(0, str(AQUI))
from texto_aberto import baixar, jats_para_texto, pmc_html_para_texto  # noqa: E402

COLECAO = AQUI / "colecao-treino.jsonl"
FILA = MAQ / "fila.jsonl"
FF = MAQ / "fontes_fila"
PARA_BAIXAR = MAQ / "para-baixar.md"


def ler_jsonl(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main():
    baixa = "--baixar" in sys.argv
    colecao = ler_jsonl(COLECAO)
    fila = ler_jsonl(FILA)
    na_fila = {(x.get("doi") or x.get("titulo")).lower() for x in fila}
    novos = [x for x in colecao if (x.get("doi") or x.get("titulo")).lower() not in na_fila]
    abertos = [x for x in colecao if x.get("pmcid")]
    pagos = [x for x in colecao if not x.get("pmcid")]
    print(f"Coleção: {len(colecao)} artigos · {len(abertos)} de acesso aberto · {len(pagos)} pagos")
    print(f"Entram na fila agora: {len(novos)}")
    if not baixa:
        print("\nNada foi baixado. Para baixar o texto aberto e catalogar, rode de novo com --baixar")
        return
    MAQ.mkdir(parents=True, exist_ok=True)
    with open(FILA, "a", encoding="utf-8") as f:
        for x in novos:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    FF.mkdir(exist_ok=True)
    ok, sem = 0, []
    for k, it in enumerate(abertos, 1):
        nome = unicodedata.normalize("NFC", it["titulo"])
        dest = FF / f"{nome}.txt"
        if dest.exists():
            ok += 1
            continue
        bruto = ""
        try:
            bruto = pmc_html_para_texto(baixar(f"https://pmc.ncbi.nlm.nih.gov/articles/{it['pmcid']}/", tentativas=2))
        except Exception:  # noqa: BLE001
            pass
        if len(bruto.split()) < 800:
            try:
                bruto = jats_para_texto(baixar(
                    f"https://www.ebi.ac.uk/europepmc/webservices/rest/{it['pmcid']}/fullTextXML", tentativas=1))
            except Exception:  # noqa: BLE001
                bruto = ""
        if len(bruto.split()) >= 800:
            dest.write_text(f"# {nome}\n# origem: {it['pmcid']}\n" + bruto, encoding="utf-8")
            ok += 1
        else:
            sem.append(it)
        if k % 10 == 0:
            print(f"  {k}/{len(abertos)} baixados={ok}", flush=True)
        time.sleep(0.6)
    print(f"\nTexto aberto: {ok} de {len(abertos)} · sem texto aberto: {len(sem)}")
    with open(PARA_BAIXAR, "a", encoding="utf-8") as fh:
        fh.write("\n## treino-forca (coleção inicial)\n")
        for it in pagos + sem:
            fh.write(f"- [ ] **{it['titulo']}**" + (f" · DOI {it['doi']}" if it.get("doi") else "") + "\n"
                     + "".join(f"  - {l}\n" for l in it.get("links", [])))
    print(f"Lista dos que precisam do seu acesso: {PARA_BAIXAR}")
    print("\nCatalogando (pode levar alguns minutos)...", flush=True)
    subprocess.run([sys.executable, str(AQUI / "biblioteca.py"), "catalogar"], check=False)


if __name__ == "__main__":
    main()
