---
name: carrossel
description: Cria carrosséis prontos para o Instagram do Jorge Souto (SOUTO TREINADOR, educador físico; 1080x1350, exportados em 2160x2700) pelo método de texto nativo de carrossel (inspirado na BrandsDecoded), em 5 formatos visuais (M1 Mangá Dark, M2 Editorial Clean, M3 Dossiê, M4 Cinema, M5 BrandsDecoded), na identidade azul da marca. Pipeline com aprovações do Jorge — entrada (conteúdo existente ou tema da base) e Ficha do tema → triagem recomenda o TIPO (Tendência, Tese / Mito × evidência, Case, Previsão) → FORMATO → 10 headlines → texto por slide validado por script (evidência, ética do CONFEF, nutrição fora da competência) e por revisão editorial → aprovação → artes em foto realista (Gemini/Google Flow no navegador ou Higgsfield pelo MCP) → render local com 0 ALERTA → legenda. Use quando o usuário digitar /carrossel ou pedir um carrossel/post em slides.
---

# /carrossel: frente 03 - CARROSSÉIS E ARTE

`RAIZ` = a raiz do repositório `souto-treinador` (a pasta em que o Claude Code foi aberto). Todos os caminhos abaixo são relativos a ela; os scripts acham as próprias pastas sozinhos.
- Manual da frente: `RAIZ/03 - CARROSSÉIS E ARTE/CLAUDE.md`. Guia para humanos: `RAIZ/docs/guias/03-carrossel.md`.
- **Método de texto:** `RAIZ/03 - CARROSSÉIS E ARTE/Referências/Método BrandsDecoded/Método de texto - carrossel.md` (resumo próprio; o curso original não está no repositório).
- Gerador: `RAIZ/03 - CARROSSÉIS E ARTE/Gerador/` (abaixo, `GER`). Marca: `GER/marca.json` — logo branca transparente, paleta azul (aço `#445DB4` → elétrico `#2E49CE` → royal `#1F33A3` → noite `#141A3D`), fundos `#0B0B0E` e `#F2F4F8`, **sempre em degradê**, assinatura "JORGE SOUTO · TREINADOR", o @ (`nome`) e o CREF (`registro`). **O @ e o CREF estão provisórios (TROCAR)**: o render imprime um LEMBRETE enquanto não forem trocados; antes da primeira publicação, peça ao Jorge os valores certos e edite só o `marca.json`.
- Formato do JSON de cada modelo: docstring no topo de `render_carrossel.py` (M1), `modelo_editorial.py` (M2), `modelo_dossie.py` (M3), `modelo_cinema.py` (M4), `modelo_brandsdecoded.py` (M5).
- Testes de referência (texto fictício, marcadores cinza): `RAIZ/03 - CARROSSÉIS E ARTE/Carrosséis/_testes/` (`_teste-modelo1.json` a `_teste-modelo5.json`).

## Como conduzir
- **Sequência fixa, sem pular etapa.** Cada ⏸ espera a resposta do Jorge. Pular só com pedido explícito dele ("pula a espinha"); registre no `carrossel.md`. **A aprovação do texto antes da arte nunca é pulada.**
- **Paradas fundidas (para não demorar):**
  1. **Formato já dito na entrada** (ex.: "M5"): uma chamada ao `chefe-de-pauta` em modo "triagem + headlines"; mostre triagem, 10 headlines e capas numa mensagem só. Sem formato na entrada, pergunte o formato na mesma mensagem da triagem.
  2. **Espinha pulada por padrão:** o `redator-de-carrossel` monta a espinha por dentro e grava o texto direto; a espinha aparece no topo do TEXTO FINAL. Mostrar antes só se o Jorge pedir.
- **Tipo antes do formato:** a triagem recomenda o TIPO (1 dos 4) e o Jorge confirma; depois ele escolhe o FORMATO.
- Ler a base, escrever e revisar fica com os agentes (seção 11). Se um agente não aparecer na lista da sessão, leia `RAIZ/.claude/agents/03-carrosseis/<nome>.md` e rode um agente general-purpose com aquelas instruções.
- Respostas curtas, no formato da etapa, sem narrar bastidor.
- Pasta da peça: `RAIZ/03 - CARROSSÉIS E ARTE/Carrosséis/<AAAA-MM-DD - tema curto>/` com `carrossel.json` (`"saida": "."`), `artes/`, `html/`, PNGs, `folha.jpg`, `prompts_arte.md` e `carrossel.md`.

| Etapa | Quem faz | Aprovação | Sai |
|---|---|---|---|
| 0 Entrada e Ficha | conversa principal | — | insumo + caminho da Ficha |
| 1 Triagem e tipo | `chefe-de-pauta` | ⏸ tipo | tipo, eixo, funil, CTA |
| 2 Formato e slides | Jorge | ⏸ formato (no M1, ⏸ estilo de capa) | modelo, capa, nº de slides |
| 3 Headlines | `chefe-de-pauta` | ⏸ headline (+ versão de capa) | headline + capa |
| 4 Espinha dorsal | `redator-de-carrossel` | ⏸ só se o Jorge pedir | estrutura |
| 5 Texto e validação | `redator-de-carrossel` → `editor-de-texto` → validador | — | `carrossel.json` com 0 ERRO |
| 6 Aprovação do texto | conversa principal | ⏸ "aprovado" | texto travado |
| 7 Artes | `diretor-de-arte` + Gemini/Flow ou Higgsfield | ⏸ créditos | `artes/` |
| 8 Render e revisão | conversa principal (`revisor-de-diagramacao` se houver dúvida) | — | PNGs com 0 ALERTA |
| 9 Editor visual | Jorge (opcional) | — | ajustes finos |
| 10 Fechamento | scripts + `legendista` | — | `carrossel.md`, fontes, legenda |

## 0. Entrada e Ficha
1. Se o Jorge já deu o tema (ex.: `/carrossel volume de treino`), vá direto à Ficha. Senão, pergunte: **A. transformar um conteúdo existente** (link, texto, roteiro de `RAIZ/02 - ROTEIROS/Roteiros/`, transcrição) ou **B. criar a partir de um tema da base**. Conteúdo de terceiros é só matéria-prima: nada é copiado, e todo fato científico precisa estar na Ficha.
2. **Ficha do tema:** `RAIZ/01 - BASE CIENTÍFICA/00 - ÍNDICE.md` → `RAIZ/01 - BASE CIENTÍFICA/<Área>/<Tema> - Ficha.md`. Nunca varrer a base. **Sem Ficha:** diga "não temos isso processado" e ofereça `/montar-condicao <tema>`. Pare aqui.
3. **Fato não científico** (case, tendência, notícia): só com fonte verificável (link que abre); com o ok do Jorge, grave na Ficha como H (`## Histórias reais (verificáveis)`) **antes de usar**. Nunca inventar número, estudo, pessoa, caso ou citação.

## 1. Triagem e TIPO (⏸ o Jorge confirma o tipo)
Chame o `chefe-de-pauta` (modo triagem) com o insumo e o caminho da Ficha. **Mostre o bloco como veio, sem reescrever** (formato no agente). Fecho do bloco: "Confirma o tipo? (ok, ou 1 Tendência · 2 Tese [2b Mito × evidência] · 3 Case · 4 Previsão). Depois vem o formato: M1 Mangá Dark · M2 Editorial Clean · M3 Dossiê · M4 Cinema · M5 BrandsDecoded."

### Os 4 tipos
| Tipo | Quando | Arco |
|---|---|---|
| Tendência (`tendencia`) | algo mudando agora, com data | Hook → Contexto → Mudança → Impacto → Ação → CTA |
| Tese (`tese`) | crença comum que a evidência contradiz | Crença → Dados que desafiam → Verdade → Novo modelo → Aplicação → CTA |
| ↳ Mito × evidência (`tese-mito`) | alguém vende a crença (suplemento, método milagroso, guru) | Crença → Quem vende → O que a evidência diz → Por que engana → O que fazer → CTA |
| Case (`case`) | história real verificável (ids H obrigatórios) | Resultado → Quem fez → Como → Princípio → O que levar → CTA |
| Previsão (`previsao`) | só sinais apontando uma direção | Sinais → Padrão → Direção → Quem se adianta → Ações → CTA |

### CTA pelo conteúdo (um só, diretivo, sem agradecimento)
| Conteúdo | `cta.tipo` |
|---|---|
| Qualquer tema (padrão) | `consultoria`: treino/consultoria individualizada com **Jorge Souto, treinador, CREF (do `marca.json`)**, link na bio. Sem preço. Ex.: "Quer um treino para a sua rotina? Treino individualizado com Jorge Souto · CREF … · link na bio" |
| Material próprio do Jorge (só se existir) | `ebook`: "<material> · link na bio" |
"Salvar" e "Comenta PALAVRA" não são o padrão (o validador avisa).

## 2. FORMATO e nº de slides (⏸ o Jorge escolhe)
Pergunte em texto: o formato, a capa (quando houver) e o nº de slides (**padrão 9**; 5, 7 ou 12 também valem).
- **M1 — Mangá Dark** (`"manga-dark"`): slides escuros/claros, recortes, destaques em degradê azul, CTA dividido com a foto do tema desfocada (`imagem_blend`, obrigatória) e assinatura com o CREF. Internos em diagonal (texto em cima de um lado, foto embaixo do outro, alternando sozinho). ⏸ **estilo de capa:** 1 fundo preto · 2 fundo branco · 3 quadriculado · 4 fundo desfocado (pede `imagem_blend`). Exemplos: os slides 1 de `Carrosséis/_testes/_teste-modelo1/`.
- **M2 — Editorial Clean** (`"editorial"`): fundo claro quadriculado, título serifado em degradê azul, #01/#02 esbatidos, recorte invadindo o slide, CTA com caixa tracejada e logo. Capa só `capa2`. Tópicos alternam sozinhos (ímpares: foto no canto de baixo à direita; pares: foto embaixo no centro).
- **M3 — Dossiê** (`"dossie"`): manchetes condensadas, fotos emolduradas, texto sobre foto. Capa A (`capa`, `"fundo"`: `cor`/`azul` (o degradê azul da marca, padrão), `preto`, `branco`, `#RRGGBB` ou `foto`; leitura e degradê preto automáticos) ou capa B (`capa2`). Manchetes revezam a cor sozinhas (azul → noite → branco). CTA com foto **sem pessoa** (para ninguém achar que é o Jorge, a não ser que seja uma foto real dele).
- **M4 — Cinema** (`"cinema"`): storytelling cinematográfico; fundo escuro texturizado, barra de busca, janela, vidro fosco; capa A (foto + título + cursiva + caixa) ou capa B (`capa2`, janela clara; variante `"estilo": "foto"`). O objeto da busca é ponte para o slide seguinte.
- **M5 — BrandsDecoded** (`"brandsdecoded"`): alternado claro/escuro (`#0B0B0E` / `#F2F4F8`, slide `grad` no degradê azul); headline Barlow Condensed caixa-alta; barra de destaque, barra da marca (JORGE SOUTO · TREINADOR | @ | CREF), barra de progresso; componentes card, tabela, stat, setas, cards; CTA com caixa "LINK NA BIO" e frase-ponte.

### Anatomia (9 slides; `funcao` de cada slide)
| Função | M5 | M1 | M2 | M3 | M4 |
|---|---|---|---|---|---|
| 1 capa | capa | capa | capa2 | capa (ou capa2) | capa (ou capa2) |
| 2 hook | dark | texto | topico #01 | manchete | busca |
| 3 mecanismo | light | texto | topico #02 | foto | lateral |
| 4 mecanismo | dark | texto | topico #03 | manchete | texto |
| 5 prova | light (tabela/stat) | texto | topico #04 | foto | vidro |
| 6 expansão | dark | texto | topico #05 | manchete | lateral |
| 7 aplicação | light | texto | topico #06 | manchete | texto |
| 8 direção | grad | texto | resumo | foto | janela |
| 9 cta | cta | cta | cta | cta | pergunta |
Outros tamanhos: Método 4.5.

## 3. Headlines (⏸ o Jorge escolhe)
`chefe-de-pauta` (modo headlines) com triagem, tipo, formato e Ficha → 10 headlines (1–5 Investigação com dois-pontos; 6–10 Narrativa em 3 frases) + versão de capa das 3 melhores. Mostre como veio. Fecho: "Escolhe 1–10, pede 'refazer headlines' ou ajusta uma." Se o Jorge escolher uma fora das 3, chame de novo em modo **capa**.
**Tom:** provocativo, com cara de manchete, apontando o dedo para a desinformação fitness (mitos de academia, promessas de suplemento, "treino milagroso"), sem atacar pessoa. O carrossel entrega o que a capa promete; nada inventado.

## 4. Espinha dorsal (só se o Jorge pedir)
`redator-de-carrossel` (modo espinha). Fecho: "Estrutura aprovada? Se sim, escrevo o texto de cada slide."

## 5. Texto por slide e validação (até 0 ERRO)
1. **`redator-de-carrossel` (modo texto)** grava `carrossel.json` na pasta da peça (topo: `modelo`, `ficha`, `tipo_carrossel`, `eixo`, `funil`, `headline`, `cta`, `saida`; por slide: `funcao` e `afirmacoes`). O texto nunca leva `[#n]`. Arte obrigatória: `"imagem": "artes/slide-NN.png"` (marcador cinza + ALERTA até a arte existir).
2. **`editor-de-texto`**: 7 parâmetros ≥ 8 por slide, 5 testes; reescreve no JSON os blocos reprovados. Se voltar "pendente", mostre só os slides reprovados e pergunte ao Jorge: reescrever ou aceitar com ressalva.
3. **Validador:** `python "RAIZ/03 - CARROSSÉIS E ARTE/Gerador/validar_carrossel.py" "<pasta>/carrossel.json"` → **0 ERRO**. AVISOs conferidos um a um. (Se o hook estiver registrado, ele roda sozinho a cada gravação: guia, seção "Hook".)

**O que o validador cobra** (detalhe no topo de `GER/editorial.py`):
- ERRO: limites de caracteres; id inexistente na Ficha; verbo mais forte que a certeza; número fora da linha citada; palavras proibidas (cura, milagre, garantido, segredo, nunca mais, 100%, sem esforço); estruturas binárias; cacoetes de IA; dados vagos; anglicismo numérico; aberturas/fechos proibidos; CTA cordial; headline proibida; **ética** (antes/depois, depoimento/resultado de aluno, preço/promoção, promessa de quilos/centímetros com prazo ou garantia); **nutrição fora da competência** (dieta, cardápio, calorias ou suplemento com dose para o leitor = atividade do nutricionista); ordem sobre remédio ou hormônio.
- AVISO: ordem de comida/suplemento sem dose; **slide que fala de dieta, proteína, caloria ou suplemento sem id da Ficha** (nutrição só como educação geral, com fonte); "exercício que seca a barriga"; ordem de treino com número para o leitor; 2ª pessoa fora de aplicação/CTA; jargão; tom de coach; sigla/termo técnico (RM, RIR, RPE, VO2, HIIT, %, síntese proteica…); consultoria sem CREF no CTA (M1–M4); forma do M5.

## 6. Aprovação do texto (⏸ "aprovado")
Mostre o TEXTO FINAL (formato no `redator-de-carrossel`). Fecho: "Revisa o texto de cada slide. Pode pedir ajuste em qualquer um. Quando estiver tudo ok, digita 'aprovado' e eu parto para as artes." Nada de arte antes do "aprovado".

## 7. Artes (foto realista conceitual) — duas rotas
**Estilo:** foto realista/ultrarrealista, estética de revista independente, conceitual, sóbria e clean; um ponto focal; nada de anime, 3D ou ilustração; sem texto, logo, marca, celebridade ou pessoa real reconhecível; nada de corpo de "antes/depois" nem físico extremo para chocar. Treino real e plausível (técnica correta, carga coerente, ambiente de academia ou rua). Acentos azuis são bem-vindos, mas a foto pode ter outras cores; a paleta da marca é obrigatória só nos elementos gráficos (isso é do gerador).
1. ⏸ **Tratamento da foto, slide a slide** (M1; no M3 só o fundo da capa A): foto inteira (`"tratamento": "cena"`) ou recorte (`"tratamento": "recorte"`) sobre `"fundo"` `branco` · `preto` · `quadriculado` · `blend` (2ª arte `imagem_blend`, desfocada) · `liso`. Mostre a sua recomendação; sem resposta, pergunte de novo. `python "GER/render_carrossel.py" <json> --guias` mostra a zona do sujeito.
2. **Prompts:** `diretor-de-arte` (modo prompts) grava `<pasta>/prompts_arte.md` com a tabela (inclui a coluna **"Rota"**: banco, Gemini/Flow ou Higgsfield, e a coluna **"No JSON"**).
3. ⏸ **Créditos:** mostre quantas artes e variações vão ser geradas e **em qual rota**; espere o ok antes de gastar créditos.
4. **Gerar** pela rota escolhida pelo Jorge:
   - **Rota A — Gemini / Google Flow no navegador** (ferramentas `mcp__claude-in-chrome__*`, no Chrome do Jorge, janela visível): `https://flow.google.com` (Flow; se o endereço mudar, procure "Google Flow") ou `https://gemini.google.com` (Gemini, modelo de imagem "Nano Banana"). No Flow: Novo projeto → modelo de imagem → proporção → 1 a 4 variações → prompt → gerar; confira o custo antes de enviar. **No máximo 1 ou 2 gerações por disparo, com pausa** (disparo em sequência pode bloquear por "atividade incomum"). Nunca contornar verificação/CAPTCHA: se aparecer, pare e avise o Jorge. Baixe na maior resolução (2K quando houver); o lado menor precisa de ≥ 1080 px na área usada.
   - **Rota B — Higgsfield pelo MCP** (conector `Higgsfield`, quando estiver conectado; instalação no guia, seção "Higgsfield"): use a ferramenta de geração de imagem do conector com o prompt do `diretor-de-arte`, a proporção da tabela e 1 a 4 variações; confira o saldo de créditos antes (toda geração pelo MCP gasta créditos, mesmo em plano "ilimitado" no site). Baixe o resultado (URL ou Assets do Higgsfield) para `artes/`. Personagem recorrente: o recurso de personagem (Soul) do Higgsfield mantém o mesmo rosto entre slides; só com pessoa fictícia ou com fotos do próprio Jorge, com o ok dele.
   - **Banco de imagens (cena, fundo, textura):** `node "RAIZ/04 - EDIÇÃO DE VÍDEO/motor/scripts/stock.mjs" <pasta-rascunho> <id> "<busca em inglês>" --image --n 4 [--horizontal]` (Pixabay e Pexels com as chaves `PIXABAY_API_KEY` e `PEXELS_API_KEY` do `.env` da raiz; Openverse/Wikimedia sem chave; ver guia). Use a própria pasta da peça como `<pasta-rascunho>`: as fotos saem em `<pasta>/04_broll/fotos/` e o crédito em `<pasta>/04_broll/creditos.json`; copie a escolhida para `artes/slide-NN.png` e leve o crédito para o `carrossel.md`. O motor de vídeo precisa estar instalado (`npm install` em `RAIZ/04 - EDIÇÃO DE VÍDEO/motor/`; guia da frente 04).
   - Se nada funcionar: entregue o `prompts_arte.md` para o Jorge gerar e soltar na pasta `artes/` com os nomes do passo 5.
5. Salve em `<pasta>/artes/slide-NN.png` (2ª arte do slide: `slide-NN-2.png`; blend: `slide-NN-fundo.png`). Opcional: uma cópia em `RAIZ/03 - CARROSSÉIS E ARTE/Banco de artes/` com a linha no `ÍNDICE.md` (crie a pasta se não existir).
6. **Grave no `carrossel.json` os campos da coluna "No JSON"** (a conversa principal grava; o validador roda): `imagem`, `imagem2`, `imagem_fundo`, `imagem_blend`, tratamento, `fundo`, `zona`, `enquadramento`, `posicao_imagem`, `modo_recorte` (`recorte_modo` no M3).
7. **Controle de qualidade:** `diretor-de-arte` (modo qualidade) e `python "GER/conferir_recortes.py" "<pasta>/carrossel.json"` → `recortes.jpg`. Refaça o que for reprovado.
- **Recortes:** gerados em FUNDO BRANCO puro, sem degradê, vinheta, sombra ou reflexo; sujeito opaco e de tom médio/escuro (roupa branca, garrafa transparente e água somem no recorte). Fundo preto puro só para objeto luminoso (modo "tinta").
- **Nenhuma foto se repete no mesmo carrossel** (o render dá ALERTA).

## 8. Render e revisão (0 ALERTA)
0. Recortes antes: `python "GER/conferir_recortes.py" "<pasta>/carrossel.json"` → `recortes.jpg`.
1. `python "GER/render_carrossel.py" "<pasta>/carrossel.json"` → PNGs 2160x2700 + ALERTAS/AVISOS (precisa do Google Chrome instalado; ~10 s por slide). Rode em segundo plano.
2. `python "GER/folha.py" "<pasta>"` → abra a `folha.jpg` na conversa principal. O `revisor-de-diagramacao` só entra se a folha deixar dúvida.
3. Corrija e renderize só os slides alterados: `--slides=4,6`. Repita até **0 ALERTA** com a folha inteira conferida. Texto mudado volta ao validador.
4. Antes das artes, o único ALERTA aceito é "arquivo da arte não encontrado". AVISO "conteúdo < 50% da área" (M5) = candidato a caixa de imagem.

### Limites de caracteres (tabela `LIMITES` do `render_carrossel.py`)
- **M1**: capa linha1 24 · linha2 18 · sub 60 | texto 300 | cta antes 40 · palavra 14 · depois 80 · chamada 90
- **M2**: capa2 título 50 · sub 60 | tópico título 40 · texto 260 · fecho 80 | resumo título 60 · item 40 · fecho 80 | cta título 45 · sub 70 · caixa 90
- **M3**: capa topo 16 · base 13 · sub 80 · tag 28 | capa2 pre 30 · título_topo 28 · título 70 · tag 34 | manchete título 130 · texto 200 | foto texto 330 | cta tag 34 · título 110 · caixa 70
- **M4**: capa linha1 14 · linha2 14 · script 45 · caixa 110 | capa2 título 30 · sub 40 · nota 40 | busca texto 230 · balão 45 · fecho 55 | lateral/quadro texto 150 · rodapé 160 | vidro cartão 140 | texto 130 · nota 130 | janela 110 · texto 130 | pergunta 90
- **M5**: capa headline 120 | tag 32 · título 70 | texto 2 blocos de 230 | card 200 · tabela célula 40, fonte 80 · stat valor 12 / legenda 90 · setas item 110 · cards título 40 / texto 140 | cta tag 32 · ponte 200 · título 60 · instrução 50 · palavra 16 · benefício 90
Passou do limite → sintetize; nunca diminua a fonte.

### Regras de diagramação (inegociáveis)
1. Fonte nunca distorcida. 2. Prumo e esquadro. 3. Texto nunca sobre texto, rosto ou ponto focal. 4. Nenhum texto a menos de 14 px da borda; acentos inteiros. 5. Fonte mínima de 18 px (exceto o cabeçalho decorativo e a barra da marca do M5, 14 px). 6. Foto nunca esticada. 7. 1 headline e 1–2 destaques por slide. 8. M5: conteúdo pela base, margem de 56 px, nada encostando na barra de progresso, destaque em até 3 palavras. 9. Só entregar com 0 ALERTA e depois de olhar a folha inteira.

## 9. Editor visual
Dois cliques em `RAIZ/03 - CARROSSÉIS E ARTE/Abrir editor de carrossel.bat` (ou `python "GER/editor.py" --abrir`) → http://localhost:8765/editor. Tudo é editável (texto, posição, tamanho, fonte, cor, camadas, foto, recorte); "Gerar PNG" usa o mesmo Chrome do render. Slide salvo no editor não é sobrescrito pelo render (só com `--refazer`). Mudança de conteúdo vai no JSON (para passar pelo validador).

## 10. Fechamento
1. **`carrossel.md`** na pasta: tipo, eixo, formato, funil, CTA, triagem, headline, espinha, texto por slide, QA, prompts das artes (com a rota usada), etapas puladas e ressalvas.
2. **Fontes por script** (nunca à mão): `python "GER/validar_carrossel.py" "<pasta>/carrossel.json" --montar-fontes`.
3. **Legenda:** agente `legendista` (grava `## Legenda` no `carrossel.md`).
4. **Entrega:** os PNGs, a legenda pronta para copiar e as fontes. O Jorge publica.

## 11. Mapa de agentes e scripts
| Agente / script | Onde | Faz |
|---|---|---|
| `chefe-de-pauta` | `RAIZ/.claude/agents/03-carrosseis/` | triagem, tipo, eixo, funil, CTA; 10 headlines + versão de capa |
| `redator-de-carrossel` | idem | espinha; texto no `carrossel.json` até 0 ERRO |
| `editor-de-texto` | idem | 7 parâmetros ≥ 8, 5 testes, tabela QA |
| `diretor-de-arte` | idem | prompts por espaço de arte (rotas Gemini/Flow, Higgsfield, banco) e controle de qualidade |
| `revisor-de-diagramacao` | idem | diagnóstico de render e folha quando houver dúvida |
| `legendista` | `RAIZ/.claude/agents/05-publicacao/` | legenda |
| `pesquisador-de-evidencia` · `checador-de-afirmacoes` | outras frentes (se existirem) | evidência que falta · AVISO de calibração |
| `validar_carrossel.py` (+ `editorial.py`) | `GER/` | limites, ids, verbo × certeza, números, ética, regras editoriais; `--montar-fontes` |
| `render_carrossel.py` · `modelo_*.py` | `GER/` | HTML editável + PNG + ALERTAS (M1 no próprio render; M2–M5 nos módulos) |
| `folha.py` · `conferir_recortes.py` · `editor.py` | `GER/` | folha de contato · prévia dos recortes · editor visual |

**Comandos do Jorge no meio do fluxo:** "refazer headlines" · "ajusta a N" · "mistura a N com a M" · "aprovado" · "trocar slide N" · "trocar imagem da capa" · "usar Higgsfield" / "usar Gemini" · "reiniciar".
