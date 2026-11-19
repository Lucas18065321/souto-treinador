# Teste do motor de roteiros (FICTÍCIO)

Arquivos para conferir se o motor funciona num computador novo, **sem depender da base científica ter Fichas**:

| Arquivo | O que é |
|---|---|
| `TESTE Volume de treino - Ficha.md` | Ficha **fictícia** (toda linha marcada `[FICTÍCIO]`). Não é evidência. |
| `TESTE-Ficticio 2099 - volume semanal.md` | Nota-base **fictícia** (o artigo não existe), para o `--montar-fontes` ter de onde tirar a referência. |
| `Roteiro teste - mais séries mais músculo.md` | Roteiro de teste que cita a Ficha fictícia. Deve dar **0 erro**. |

O validador só enxerga Fichas desta pasta se o nome começar por `TESTE`. O hook (`.claude/hooks/validar_peca.py`) também valida arquivos daqui que começam por `Roteiro`.

## Rodar o teste (PowerShell, na raiz do repositório)
```powershell
python "02 - ROTEIROS\_SISTEMA\validar_roteiro.py" "02 - ROTEIROS\_SISTEMA\teste\Roteiro teste - mais séries mais músculo.md" --montar-fontes
```
Esperado: `0 erro(s), 0 aviso(s) · 6 partes · 132 palavras ≈ 53 s · refs: #1, #2` e a mensagem de que o Texto para gravar, as Fontes e o Nível de certeza foram montados.

**Nunca publique nada daqui.** Quando a base tiver uma Ficha real de treino, teste com ela.
