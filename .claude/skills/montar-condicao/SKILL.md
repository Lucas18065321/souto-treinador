---
name: "montar-condicao"
description: "Monta (ou atualiza) na base científica do Jorge Souto (SOUTO TREINADOR) a Ficha de um tema de treino e saúde (hipertrofia, volume de treino, força em idosos, emagrecimento com treino, mitos de academia…), com Protocolo quando o tema pede conduta técnica. A Edison Scientific e scripts acham e catalogam as fontes sem gastar token; o Jorge aprova de 3 a 10 fontes; o agente fichador (Sonnet) escreve; scripts conferem e geram o índice. Use quando o Jorge pedir para montar, processar ou atualizar um tema, ou quando um roteiro precisar de uma Ficha que não existe."
argument-hint: "<tema>"
---

# /montar-condicao

> Caminhos relativos à **raiz do repositório** (o diretório de trabalho da sessão, onde está `.claude/`). Base: `01 - BASE CIENTÍFICA` (`B`). Máquina: `B/_MÁQUINA` (`M`). Manual: `B/CLAUDE.md`. Guia para humanos: `docs/guias/01-base-cientifica.md`.
> Scripts (sempre a partir da raiz):
> - `python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/biblioteca.py" <comando>` (`catalogar`, `buscar`, `ver`, `trecho`, `conferir-ficha`, `importar-fila`, `panorama`)
> - `python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/edison.py" <comando>` (`chave`, `creditos`, `plano`, `perguntar`, `coletar`, `candidatos`): **1º passo da busca** (descoberta)
> - `python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/gerar_indice.py"`
> - `python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/atualizar_pautas.py"` (só se existir no repositório)
>
> **Princípio:** script faz o mecânico (0 token); só o agente `fichador` (Sonnet) escreve. Nunca leia PDF, JSON de artigo, Ficha ou Protocolo inteiros na conversa principal. Um tema por vez. Sem fonte aprovada, nada é afirmado.

## 0. Tipo, área e nome
- **Tema com conduta técnica** (ex.: hipertrofia, treino para idosos, emagrecimento com treino): `<Tema> - Protocolo.md` + `<Tema> - Ficha.md` em `B/<Área>/`.
- **Tema transversal** (ex.: mitos de academia, como ler um estudo, sono e recuperação): só `<Tema> - Ficha.md`, em `B/Transversais/`.
- **Área:** use uma da lista `AREAS` de `M/scripts/gerar_indice.py` (o índice só mostra essas). Área ambígua ou faltando na lista: pergunte ao Jorge.
- Já existe? Grep do nome em `B/00 - ÍNDICE.md`. Se existir, é **atualização**: busque só fontes novas e diga o que já está lá.

## 1. Buscar as fontes (script, 0 token)
### 1.0 Edison primeiro (descoberta, só para tema novo ou lacuna)
A **Edison Scientific** (antiga FutureHouse) lê a literatura e cita artigos: **Literature** responde perguntas com referências; **Precedent** responde "alguém já testou X em humanos?". Ela só **acha candidatos**. **A resposta do agente nunca é evidência e nunca entra na Ficha.**
1. `edison.py creditos`: vê o plano e o gasto do mês. **Passar do plano só com ⏸ do Jorge** (o script recusa sem `--autorizado`). Sem chave: `edison.py chave --abrir` abre o Bloco de Notas para o Jorge colar a chave (ela fica em `%USERPROFILE%\.edison-key`; **nunca** aceite chave colada no chat).
2. Uma pergunta ao Literature por tema, com termos técnicos em inglês: `edison.py perguntar "<tema>" "<pergunta>"` (ex.: `"resistance training volume hypertrophy dose-response in adults"`). Literature High só se o tema for confuso e o Jorge topar (custa mais). "Já testaram em humanos?": `--agente precedent`. Pode passar de 2 min: rode em segundo plano.
3. `edison.py candidatos "<tema>"`: tira os DOIs/PMIDs citados e confere cada um no Europe PMC. **Artigo marcado com ⚠ pode ter sido inventado pela IA: nunca aprove sem o conferido.** Resultado em `M/edison/<tema>/candidatos.md`.
4. Edison sem chave, sem créditos ou fora do ar: siga o resto e avise o Jorge em uma linha.

### 1.1 Catálogo, fila e sinônimos (complemento)
1. Sinônimos em português e inglês. Ex.: hipertrofia → `hypertrophy`, `muscle mass`, `lean mass`; volume → `training volume`, `weekly sets`; idosos → `older adults`, `sarcopenia`, `falls`; emagrecimento → `fat loss`, `weight loss`, `body composition`; falha → `proximity to failure`, `repetitions in reserve`.
2. No catálogo: `biblioteca.py buscar "<termo>"` por sinônimo principal, repetindo com `--tipo diretriz`, `--tipo meta-analise`, `--tipo revisao-sistematica` (e `--desde 2020`). Anote id, tipo, ano, teto de certeza.
3. Na fila (fontes curadas ainda não catalogadas): Grep sem diferenciar maiúsculas dos sinônimos em `M/fila.jsonl`. `biblioteca.py importar-fila` (sem `--baixar`) mostra o plano. Também vale olhar `B/Curadoria inicial - treino de força.md` (se existir).
4. **Mostre ao Jorge**, em até 20 linhas (marque o que veio da Edison):
   - **Encontradas**, nesta ordem: posicionamento/diretriz vigente → consenso → meta-análise → revisão sistemática → ensaio. Cada uma: id, tipo, ano, teto de certeza.
   - **Faltando:** (a) *acesso aberto*: `biblioteca.py importar-fila --baixar` (⏸; baixa todas as abertas da fila, diga o total); (b) *pagas*: lista com link (Grep em `M/para-baixar.md`) para o Jorge baixar **pelo acesso dele (CAPES, universidade, biblioteca)** e soltar em `B/ENTRADA/`. Nunca use site pirata.
   - Sem diretriz/posicionamento vigente: avise que as lacunas serão grandes.

## 2. ⏸ O Jorge aprova de 3 a 10 fontes
Pergunte quais entram, com sugestão: pelo menos 1 posicionamento/diretriz vigente quando existir, a meta-análise ou revisão sistemática mais recente por desfecho principal, e 1 ou 2 ensaios relevantes. Mais de 10 candidatos: ranqueie e proponha as 10 melhores. Ele também decide sobre o `--baixar` e sobre os PDFs em `B/ENTRADA/`. Sem fontes aprovadas, **pare**.

## 3. Catalogar (script, 0 token)
Depois do download ou dos PDFs em `ENTRADA/`: `biblioteca.py catalogar`. Confira que cada id aprovado existe (`biblioteca.py buscar "<trecho do título>"` ou `ver "<id>"`). Id ausente: volte ao Jorge.

## 4. Escrever: agente `fichador` (Sonnet)
Prompt: `Tema: <nome>. Tipo: com Protocolo | transversal. Área: <área>. Modo: criar | atualizar. Ids aprovados: <lista, um por linha>.` Nada mais: as regras estão no agente. Se ele não aparecer na sessão, leia `.claude/agents/01-base/fichador.md` e rode um general-purpose com `model: sonnet` e essas instruções. Um tema por vez; nunca dois fichadores em paralelo.

## 5. Conferir (script, 0 token)
`biblioteca.py conferir-ficha "01 - BASE CIENTÍFICA/<Área>/<Tema> - Ficha.md"`. Deve sair com 0 erro. Sobrou erro: devolva ao `fichador` com a lista (no máximo 2 voltas); depois mostre ao Jorge.

## 6. Atualizar o que os outros leem (script, 0 token)
`gerar_indice.py` (`B/00 - ÍNDICE.md`) e, se existir, `atualizar_pautas.py` (Banco de pautas).

## 7. Mostrar ao Jorge
- Links para os arquivos (`[[<Tema> - Ficha]]`, `[[<Tema> - Protocolo]]`).
- Nº de afirmações e de fontes.
- As **3 melhores pautas** (Grep em `## Ângulos` da Ficha, `-A 14`), preferindo as de certeza alta ou moderada com gancho forte.
- Lacunas principais e fontes pagas pendentes.
- Uma linha no fim de `M/registro.md` (crie com cabeçalho se não existir): `| AAAA-MM-DD | <tema> | fontes: N | afirmações: N | fichador: ~N tokens | erros finais: 0 |`.

## Regras
- Edison: resposta de agente = pista, não fonte. Só entra na Ficha o artigo baixado, catalogado e aprovado. Créditos: `creditos` antes de perguntar; nunca passar do plano sem ⏸.
- ⏸ antes de baixar qualquer arquivo. Fonte paga fica na lista para o Jorge (acesso institucional dele), nunca "de memória".
- Linguagem leiga em tudo que pode virar texto publicado; o rigor fica na Ficha e no Protocolo.
- Nutrição aparece na Ficha como informação dos estudos, nunca como prescrição (Lei 8.234/1991).
- Não apague nada. Só scripts escrevem dentro de `_MÁQUINA/` (exceções à mão: `modelos/` e `registro.md`). Sem arquivo residual.
- Repositório público: PDFs e textos de artigo pagos **não** devem ir para o GitHub (confira o `.gitignore` da raiz).
