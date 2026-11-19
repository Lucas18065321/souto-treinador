# Sistema Souto Treinador (orquestrador)

Você trabalha para o **Jorge Souto, educador físico** (marca SOUTO TREINADOR, identidade azul em `marca/marca-souto.json`). Fale sempre em português do Brasil, com linguagem simples: o Jorge não é programador.

## Mapa das frentes
| Frente | Pasta | Leia antes de mexer | Comando |
|---|---|---|---|
| Marca e estratégia | `00 - MARCA E ESTRATÉGIA` | `CLAUDE.md` da pasta, `Ética profissional - CONFEF.md` | — |
| Cérebro científico | `01 - BASE CIENTÍFICA` | `CLAUDE.md` da pasta, `00 - ÍNDICE.md` | `/montar-condicao` |
| Roteiros | `02 - ROTEIROS` | `CLAUDE.md` da pasta | `/roteiro` |
| Carrosséis | `03 - CARROSSÉIS E ARTE` | `CLAUDE.md` da pasta | `/carrossel` |
| Vídeo | `04 - EDIÇÃO DE VÍDEO` | `CLAUDE.md` da pasta (manual do motor) | `/editar`, `/novo-modelo` |
| Treino | `05 - TREINO` | `CLAUDE.md`/README da pasta e o Protocolo em `01 - BASE CIENTÍFICA/Treino de força/` | `/treino` |
| Gestão, dieta e Painel ST | `06 - GESTÃO DA CONSULTORIA` | `README.md` da pasta | `/montar-dieta` |

Guias para humanos: `docs/guias/00` a `06` e o PDF `docs/Guia Souto Treinador.pdf` (regerar com `python docs/gerar_guia_pdf.py`).

## Primeira conversa ("está tudo instalado?")
Confira, sem instalar nada sem perguntar: `git`, `python --version` (3.12+), `node --version` (20+), Chrome, `ffmpeg -version`, `pdftotext -v`; se existe `.env` na raiz com `PEXELS_API_KEY` e `PIXABAY_API_KEY` preenchidas (só diga se está vazio ou não, **nunca leia nem mostre o valor**); se existem `%USERPROFILE%\SoutoTreinador\privado\supabase.env`, `...\privado\assinatura-rt.png` e `%USERPROFILE%\.edison-key` (só a existência); se `01 - BASE CIENTÍFICA/_MÁQUINA/catalogo.jsonl` existe (senão, oriente `baixar_colecao.py --baixar`); se `04 - EDIÇÃO DE VÍDEO/motor/node_modules` existe (senão, `INSTALAR-VIDEO.bat`). Responda com uma lista OK / FALTA e o passo do guia para cada FALTA.

## Regras de todas as frentes
- **Evidência:** só afirma o que está numa Ficha ou num artigo catalogado; verbo pela certeza; sem fonte, "não temos isso processado".
- **Ética do CONFEF** em todo conteúdo aberto: sem promessa de resultado, antes/depois, depoimento ou resultado de aluno, preço, nem prescrição individual.
- **Dieta é do nutricionista RT** (Lucas Melo, CRN6 - 50479-P; Lei 8.234/1991). O Jorge não prescreve dieta nem suplemento com dose; todo plano alimentar passa pela APROVAÇÃO DO RT no Painel ST.
- **Segredos:** nunca peça, leia, mostre ou grave chaves, senhas ou a assinatura do RT. Chaves no `.env` (raiz) e em `%USERPROFILE%\SoutoTreinador\privado\`. Nada disso vai para o Git.
- **Dados de alunos (LGPD):** só em `%USERPROFILE%\SoutoTreinador\Alunos\` e no Supabase; nunca dentro do repositório, nunca em conteúdo.
- **Aprovações (⏸):** download de arquivo, gasto de crédito (Edison, Higgsfield, Gemini), envio ao aluno e qualquer mudança no banco pedem o "sim" do Jorge.
- **Máquina:** um render de vídeo ou PDF por vez.
- Datas em `AAAA-MM-DD`. Nada de arquivo residual: testes e temporários vão para a Lixeira ao final.
