---
tipo: template
atualizada: 2026-11-19
status: modelos A (claro) e B (escuro) portados e rebatizados para a marca Souto Treinador; a escolha é por aluno
---
# Template do plano alimentar

O PDF que o aluno recebe: abertura do novo plano + plano alimentar, num arquivo só, **na marca Souto Treinador** (capa no degradê azul com o logo branco) e **com o bloco do Responsável Técnico** no fim: "Prescrição dietética: Lucas Melo · Nutricionista · CRN6 - 50479-P" + a imagem da assinatura dele. Sai de **um JSON**, por script, no Chrome do PC, **sem token e sem internet**. Quem preenche o JSON é o `/montar-dieta` (ver `../README.md`).

## Como gerar
```
python montar_plano.py exemplo-ficticio.json --saida "%TEMP%\plano-teste"
python montar_plano.py exemplo-ficticio.json --saida "%TEMP%\plano-teste\modelo-b" --modelo b
```
- Sai `Plano alimentar v{n} - {primeiro nome} - AAAA-MM-DD` em **.pdf** (estático) e **.html** (passar o mouse ou o dedo num ponto do gráfico mostra a data, o valor e o plano daquela data).
- O PDF sai em duas passadas: a 1ª conta as páginas, a 2ª escreve "página 1 de N" no rodapé da capa.
- **Modelo:** vem de `documento.modelo` no JSON (`a` claro, padrão · `b` escuro); `--modelo` passa por cima. O B é para ler no celular; para imprimir, o A gasta menos tinta. `--png`: prévia de cada página em `png/` (descartável). `--so-html`: não gera o PDF. `--mostrar-numeros`: liga "Como montei seu plano".
- Precisa do Chrome (achado sozinho; ou defina a variável `CHROME` com o caminho do chrome.exe) e do Python 3. O Chrome roda com um perfil temporário, sem mexer no seu.
- **Nunca gere o PDF de um aluno dentro do repositório:** use a pasta do aluno, `%USERPROFILE%\SoutoTreinador\Alunos\<nome>`.

## Marca, CREF e o bloco do RT
- Tudo vem de `../../config-st.json` (um arquivo só): nome da marca, Jorge Souto, profissão, **CREF** e **@** (os dois com TROCAR), e o bloco do RT.
- **Rodapé de toda página (2 linhas):** "Souto Treinador · Jorge Souto · CREF … · @…" e "Prescrição dietética: Lucas Melo · Nutricionista · CRN6 - 50479-P"; à direita, "Documento individual de {nome} · página X de Y".
- **Última página:** dois blocos de assinatura: "Acompanhamento e treino" (Jorge) e "Prescrição dietética · Responsável Técnico" (Lucas Melo, com a imagem da assinatura), mais a nota legal (a dieta é ato privativo do nutricionista).
- **Assinatura do RT = imagem fora do repositório:** `%USERPROFILE%\SoutoTreinador\privado\assinatura-rt.png` (PNG com fundo transparente, ~600×180 px). Outro caminho: variável `ST_ASSINATURA_RT`. **Se a imagem não existir,** o PDF sai com a linha "assinatura do nutricionista RT" e o script imprime um AVISO; o `dieta_supabase.py salvar` se recusa a salvar um PDF assim (a não ser com `--sem-assinatura`, só para teste).

## Arquivos
| Arquivo | O que é |
|---|---|
| `montar_plano.py` | monta o HTML de cada seção e imprime o PDF A4 |
| `graficos.py` | a evolução em cards (peso, dias no plano, treino), na escala de azuis da marca |
| `plano.css` | modelo A (claro): papel branco, névoa `#DCE1ED`, títulos em azul royal `#1F33A3`, degradê `#2E49CE → #1F33A3` |
| `plano-b.css` | modelo B (escuro): preto `#0B0B0E` com a luz azul (degradê "noite") e cards em azul-grafite |
| `interacao.js` | a dica ao passar o mouse nos gráficos (só no HTML) |
| `textos-padrao.json` | textos fixos, iguais para todos: fases, metas, como usar, cocção, marmitas, alarmes, check-in e as fontes das notas de rodapé. O que está em `_conferir` ainda não foi aprovado pelo RT |
| `fontes/` | Bricolage Grotesque (capa, títulos e números) e Inter Tight (texto), com a licença `OFL.txt`; vão embutidas no HTML e no PDF. Quando a fonte oficial do logo (Saira Condensed, a confirmar) chegar, ponha o .woff2 aqui e troque `--serifa` e `--fonte-capa` no `plano.css` |
| `pdf_para_png.ps1` | prévia das páginas pela API de PDF do próprio Windows (o `--png` já chama) |
| `exemplo-ficticio.json` | aluna inventada ("Ana Exemplo", plano v2, 8 semanas do v1 nos gráficos) para testar o template |

Logo: `../../../marca/logo/souto-logo-branco.png` (ou um `logo.png` nesta pasta, que tem prioridade).

## Regras que o template já cumpre
- A4 em pé, corpo de 11 pt, rodapé de 2 linhas em toda página (marca + RT).
- Degradê da marca só em faixa e destaque. Gráficos com uma série cada, em azul, sem verde × vermelho.
- **Seção sem dado some**, nunca gráfico vazio.
- Quantidades em gramas do alimento **pronto para consumo**.
- Sem projeção de peso, sem preço, sem antes e depois.
- A régua de 5% e 10% é neutra e diz "referências do acompanhamento, não meta nem previsão".
- **Leitores de PDF:** nada de texto em degradê com a fonte da capa, nem degradê radial ou transparente na capa. Os quadradinhos usam cores sólidas, o que deixa o PDF leve.

## De onde sai cada seção (ordem do documento)
| # | Seção | Campos do JSON | Some quando |
|---|---|---|---|
| 1 | Capa | `documento.aluno_nome`, `primeiro_nome`, `inicio`, `validade`, `ficticio` · `plano.versao`, `fase` | nunca |
| 2 | Anexos de evolução | `evolucao.peso`, `peso_inicial_kg`, `constancia`, `adesao`, `treino` (com `documento.tem_treino`), `sintomas` (linha gastro), `planos` | cada bloco com menos de 2 pontos |
| 3 | Recapitulação | `relatorio.recapitulacao` | primeiro plano, ou sem dado |
| 4 | Último mês | `relatorio.acertos`, `atencao`, `melhorar` (repetição: `por_que_manter`) | primeiro plano |
| 3-4 no 1º plano | Como usar o seu plano | `textos-padrao.como_usar` | a partir da v2 |
| 5 | Metas + o que muda | `relatorio.metas[]` + `plano.o_que_muda` | sem metas e sem mudança |
| 6 | Como montei seu plano | `plano.get_metodo`, `tmb_kcal`, `fator_atividade`, `get_kcal`, `kcal_dia`, macros, água | `documento.mostrar_numeros` = false |
| 7 | Plano alimentar | `plano.refeicoes[]`, `plano.substituicoes[]`, `documento.treino` | nunca |
| 8 | Refeição livre · água · suplementação | `plano.livre_*`, `meta_agua_l`, `suplementacao[]` | cada bloco sem dado |
| 9 | Preparo e marmitas | `textos-padrao.coccao`, `conservacao` | nunca |
| 10 | Sinais de alerta · check-in · assinaturas (Jorge + RT) | `textos-padrao.alarme`, `checkin` + `documento.dia_checkin`, `documento.data_assinatura` | nunca |

## Contrato do JSON (resumo)
- **`documento`:** `aluno_nome`, `primeiro_nome`, `sexo`, `linha`, `tem_treino`, `treino` {`dias`, `horario`}, `inicio`, `validade`, `dia_checkin`, `mostrar_numeros`, `modelo` (`a` ou `b`), `data_assinatura`, `ficticio`.
- **`plano`:** `aluno_id` (código AL-n), `versao`, `tipo_versao`, `plano_anterior_id`, `fase` (`deficit`, `manutencao`, `pausa`, `superavit`), `dias_validade`, `get_kcal`, `tmb_kcal`, `get_metodo`, `fator_atividade`, `fator_atividade_texto`, `peso_usado_kg`, `data_peso`, `kcal_dia`, macros, `fibra_g`, refeição livre (`livre_*`), água (`agua_ml_por_kg`, `meta_agua_l`), `refeicoes[]`, `substituicoes[]`, `suplementacao[]`, `avisos[]`, `justificativa_rt` (só na trava de < 800 kcal) e `conferencia` (escrita pelo `calcular_plano.py`).
- **`relatorio`** e **`evolucao`:** como na tabela acima (o `dieta_supabase.py pacote` já entrega `documento` e `evolucao` prontos).
