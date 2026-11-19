# Guia de estilo: YOUTUBE - MIX EDIT (v1)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Status: **v1 (05/10/2026)**. Consolida 5 análises paralelas:
- ritmo e curvas da ref384, medidos quadro a quadro;
- composição, tipografia e cor da ref384, reprojetada para 1920×1080;
- pesquisa "Apple style" + "3D flash edit";
- gancho + Text Match Cut;
- retenção no corpo de vídeo longo.

Passou por crítica adversarial (`analises/critica.md`), ainda não por piloto; o que está "(a validar)" depende da prévia do piloto SONO X EMAGRECIMENTO. **"Correções da crítica" prevalece sobre todo o resto, inclusive sobre "Ajustes para o piloto e o cenário".**

Referências:
- **ref384** (`videos/ref384_fluidez-curvas-composicao.mp4`, 102 s, 30 fps).
  - É um celular filmando um notebook que mostra uma peça 16:9.
  - Vale pelo **fluxo, curvas, ritmo e composição**. Não vale pelo formato.
  - Cor e blur têm erro: a câmera estoura o laranja, levanta os pretos e soma o rastro de uma tela de 60 Hz.
  - A embalagem do repost não conta: título fixo "CLAUDE JUST KILLED IT", ícones Ae/Claude e @ trocando de canto.
- **Briefing do usuário** da intro (vídeo do açúcar), em `analises/analise.md`. Define a ordem dos beats da intro.
- **Refs do CUT** (ref496, ref274): texto atrás da pessoa, palavras 3D, flash.
- **Pesquisa externa:** Apple HIG (motion, materiais), WWDC23 (molas), Ajuda do YouTube (capítulos, métrica "Intro"), WCAG 2.3.1, Mayer (redundância), Lang 2000 (edits), Guo 2014 (rosto). Números de blogs valem só como ordem de grandeza.

Convenções:
- **q = quadro a 30 fps** (segundos × 30). É o fps do formato e da ref384, então os quadros medidos na ref valem direto.
- Os tempos do `edicao.json` são da SAÍDA (depois da `montagem`).
- Tamanhos em px de 1920×1080. "Maiúscula" = altura de maiúscula. Corpo (font-size) ≈ maiúscula ÷ 0,727 na Inter Tight (a conferir num quadro renderizado).
- **Níveis de evento:**
  - **micro:** reenquadramento, palavra-chave, número, rodapé de fonte;
  - **beat:** B-roll, card, tela gráfica, gráfico, card de capítulo, quebra de modo;
  - **pico:** 3D flash, texto atrás da pessoa, Text Match Cut, papel rasgado.

Princípio:
- **Três linguagens, uma identidade.**
  - A intro é cinematográfica e densa como a ref384 (de 0 a ~50 s).
  - O corpo é **Apple premium**: calmo, 1 ideia por tela, e o movimento vem de dentro do plano, não do corte.
  - O **3D flash** é só tempero nos picos, com ≤ 20 q por golpe.
  - As três usam a mesma fonte, a mesma paleta e as mesmas curvas. Só mudam amplitude e velocidade.
- **O rosto é a âncora:** 65–75% do corpo. Ele sustenta a autoridade de saúde, e o rosto intercalado com slides engaja mais que só slides (Guo 2014).
- **Fluidez da ref384:**
  - chega rápido e pousa devagar (sai em 2–4 q, assenta em 10–16 q);
  - o que sai vira o que entra;
  - blur só no pico de velocidade;
  - nada fica parado;
  - um acento único funciona como cursor de atenção ("o que está ativo agora");
  - sem quique.
- **Dinâmico mas clean** (preferência do usuário): sem tremida, sem RGB split contínuo, sem neon, sem vários acentos.

## Decisões do usuário (05/10/2026, prevalecem sobre tudo, inclusive as correções abaixo)
- **Acento: azul elétrico #2E49CE** (o mesmo do CUT DINÂMICO), não o laranja #ff6a1a. Onde o guia diz "acento" ou #ff6a1a, leia #2E49CE. O azul elétrico também perde contraste na parede laranja: texto direto na parede continua em preto quente #0B0B0E; o azul elétrico entra em cards escuros, telas e destaques.
- **Apresentação:** "Jorge Souto", "educador físico", **CREF 000000-G/UF**, ícones Instagram + YouTube, @soutotreinador.
- **Text Match Cut:** manchetes reais de veículos sérios **e** artigos científicos recentes de alto fator de impacto com metodologia sólida, cada um conferido e aprovado antes de entrar.
- **Intro reordenada** (gancho primeiro, apresentação ~0:36) aprovada no piloto. Legenda: só CC.
- **Ritmo sem respiração (05/10, ~21h; substitui o "Respiro" de "Ritmo"):** acabou a frase, emenda na outra; cortar as pausas de pensar e os alongamentos ("sonoooo").
  - Aperto automático: corta pausa/respiração < −36 dB com ≥ 0,14 s, deixando 0,06 s depois da palavra e 0,05 s antes da próxima (`02_analise/pausas_aperto.json` + `apertar` no gerador). No piloto tirou ~95 s de 19 min.
- **Zoom in/out a cada corte:** rodízio A → C → B2 → A → C → B1 nas junções (close C ≤ 4 s), com plano mínimo de 1 s e sem corte no rosto desfocado (correções de 06/10, abaixo).
- **Análise de coerência antes de montar:** comparar tomadas parecidas e explicações repetidas em pontos diferentes do vídeo e deixar só a melhor; cortar metacomentário e trechos irrelevantes. No gerador do piloto: a lista `REMOVER`.
- **Intro no estilo da referência dele** (`videos/ref_intro-colagem-papel.mp4`). Substitui os beats 3 e 4 da tabela da intro; `flash-foto`, `ponto-luz` e `titulo-quente` ficam no kit como opção.
  - **Colagem em papel** (`colagem-papel`): palavra/número grande no acento, caneta circulando, foto P&B rasgada. Entra no lugar das fotos-flash.
  - **Título em colagem stop-motion** (`colagem-titulo`) com fotos do Flow. Entra no lugar da tela escura com ponto de luz.
  - O Text Match Cut com artigos e manchetes continua (ele gostou).
- **Música (05/10, ~21h20; substitui "Pelo menos duas trilhas" em "Áudio > Música"):** só na intro, tensão investigativa crescendo até uma **parada brusca quando o título aparece**; **corpo sem música** (mais sério; ele põe trilha depois se quiser).
  - Não oferecer várias trilhas para ele escolher.
  - A do piloto foi feita por código e não tem Content ID: `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/tensao-investigativa_parada-brusca_sintetizada.wav`.
- **Como montar:** o `edicao.json` do piloto sai de um gerador (`%SOUTO_VIDEO_PROJETOS%/2026-10-05_sono-x-emagrecimento/03_roteiro/montar_edicao.mjs`). Ele faz:
  - âncoras em tempo do bruto → saída;
  - aperto, remoções e rodízio com plano mínimo;
  - blocos desfocados, capítulos e rodapés de fonte.

  Para um vídeo novo: copiar e trocar só os eventos (falas, peças, B-roll).

## Correções do usuário no piloto (06/10/2026, prevalecem sobre tudo)
Erro apontado no vídeo entregue: "a cada vez que ele dá o zoom a imagem pisca" e "a fonte da informação ficou grande, engolindo o gráfico".
1. **Rosto desfocado é um bloco só.** Nada de corte nem troca de enquadramento dentro dele. O desfoque entra (0,3 s, `entrada`) e sai (0,3 s, `saida`) só nas pontas do bloco. Blocos a menos de 1 s um do outro viram um. O trecho que continua o bloco depois de um B-roll já começa desfocado.
   - Causa: cada pedaço de cena refazia o desfoque (24 → 0 → 24). O corte mostrava 1 quadro nítido e +14 a +24 de brilho, e no piloto foram 14 piscadas.
2. **Plano mínimo de 30 q (1 s)** em toda troca de enquadramento.
   - A junção mais perto que isso fica como jump cut no mesmo enquadramento.
   - Rosto de menos de 0,6 s entre dois eventos (B-roll, tela) não aparece: o evento anterior vai até o seguinte.
   - Causa: planos de 2 a 12 q com outro zoom (sobras do aperto das pausas + rodízio) "gaguejavam".
3. **Rodapé de fonte com 26 px** (peça `fonte` e o `Rodape` de gráfico, contador e painel), numa linha só, abaixo do gráfico.
   - Linha longa encolhe até 20 px; nunca passa de 2 linhas.
   - Causa: a 40 px a citação quebrava em 3 linhas e subia por cima dos rótulos das barras.
4. **Conferência obrigatória.**
   - `checar-mix.mjs` dá ERRO nos itens 1 e 2.
   - Com `--video <mp4>`, mede as piscadas de 1–2 quadros (≥ 6 de YAVG; o detector de flash, ≥ 26, não pegava).
   - Antes do render final, `node scripts/quadros.mjs <proj> <t1> <t2> …` tira stills dos pontos novos (≈ 20 s + 17 s por quadro).

## Correções da crítica (prevalecem sobre todo o resto)
1. **Junções em px da saída, não em fração de foco.** O `foco` é o ponto fixo do zoom: Δfoco 0,08 a 1,10 move só ~15 px. Conta como troca de enquadramento: rosto deslocado ≥ 5% W **ou** escala ≥ 10% diferente; troca lateral só B1 ↔ B2 (~99 px a 1,12). Reenquadrar só saltos visíveis, com ≥ 3 s entre reenquadramentos; o resto com dissolve de 2–4 q ou cobertura (B-roll, card, tela). Detector de junções **só por imagem** (o Whisper do FFmpeg dá tempos de palavra colados: 3674 de 3750 lacunas valem 0).
2. **Proteger os tempos.** Congelar a `montagem` antes de posicionar cenas e camadas (qualquer ajuste nela desloca tudo depois). **`render-partes` é prioridade 1**: final por capítulo + junção sem recompressão; áudio mixado inteiro e normalizado uma vez só no master (2 passadas lineares, `--loudnorm-linear`).
3. **Áudio e SFX.** Piso de vol 0,55 para SFX durante a fala; palavra-chave sem som obrigatório; `volSemFala` não sobe nos cards (os tempos de palavra são colados): para a trilha subir num card, usar `quedas` com vol > 1 ou trilha própria. Medir SFX numa trilha só de efeitos, não na mixagem.
4. **Intro enxuta como padrão.** Gancho reordenado pela `montagem` (cortando a conversa e o "fala, galera" do começo do bruto); nome + CREF num rodapé discreto até ~15 s; capítulo 1 até ~0:40. Re-gancho só com material que já existe no bruto (reordenação, texto ou teaser visual). A intro longa de 7 beats (~50 s) fica como opção do usuário.
5. **Área livre depende de zoom e foco.** Medir a área livre de cada enquadramento (A, B1, B2, C) antes de posicionar: cards ≤ 520 px de largura (ou usar B2, que abre a parede direita); título atrás da cabeça ≤ 64% W, dentro de x 0,30–0,94, para não passar na frente do abajur.
6. **Legibilidade de quem dá confiança.** Rodapé `fonte` ≥ 3 s no ar, com corpo de **26 px** numa linha só (a crítica pedia 40–44 px; o usuário corrigiu em 06/10/2026: grande demais, engolia o gráfico); números de painel com maiúscula ≥ 44 px. `manchete-falada` só em telas de mecanismo; no resto, palavras-chave (resolve a contradição com a redundância de Mayer).
7. **Evidência e ética.** `03_roteiro/fontes.json` por afirmação (tempo, frase, fonte primária com DOI/PMID, desenho do estudo, n, população, efeito); o usuário revisa as afirmações da fala antes dos grafismos; rótulo "esquemático" em toda curva sem dado; nunca vender sono como substituto de déficit calórico; CFN (Res. 599/2018): identificação com CREF, sem sensacionalismo nem promessa de resultado, sem número de pacientes/seguidores como autopromoção; imagens de corpo não estigmatizantes (sem corpo sem cabeça, sem fita apertando barriga); marcar "conteúdo alterado ou sintético" no YouTube Studio quando houver imagem de IA realista. **Text Match Cut só com cada manchete conferida** (diz o que a fala diz, veículo sério, data visível no hold); se não, `match-cut-tipo`. Captura pelo caminho B (headless), com recusa de cookies.
8. **Correções sobre a ref384.** Título da tela escura é leve (Inter Tight 300, caixa baixa, sublinhado), não 900 caixa-alta; `texto-3d` vem das refs do CUT, não da ref384; gráfico de curva desenhando em ~14,7–17,0 s e arco com cabeça de brilho em ~88,3–92,7 s; a tela final de 97,7 s é embalagem do repost (a peça termina no ponto, 94–97,7 s); há ≥ 7 trocas de mundo (algumas com estouro branco); medidas em px e quadros são ordem de grandeza (celular filmando tela de 60 Hz). Pico barato que faltava: **câmera 3D inclinada em CSS** (`perspective` + `rotateX` sobre piso de grade, ref 21–31 s). Quebras de modo: 5–7 por vídeo de 20–25 min.
9. **Motor.** `grao` é global (não por cena); padrões do estilo MIX passam a `cor {1,1,0}` e `vinheta` 0,25; `seguro` das peças com padrão por modelo (false no MIX); bruto com GOP ≈ 5 s: se o render medido vier lento, reencodar uma vez com `-g 30`.

## Ajustes para o piloto e o cenário (prevalecem sobre o resto)

**Bruto do piloto:** `%SOUTO_VIDEO_PROJETOS%/2026-10-05_sono-x-emagrecimento/01_bruto/bruto.mp4`.
- Medido com ffprobe: 1920×1080, 30 fps, 24:53 (1493 s).
- O usuário já tirou os silêncios e corrigiu cor e áudio. Ficaram erros e frases repetidas.
- Duração estimada depois da decupagem: 20–24 min (a medir).

Regras que valem para este bruto:
- **Escala máxima de 1,20 no corpo.** 1,25 só em golpe de ≤ 1 s, conferindo a nitidez com `--trecho`. Push-in de 1,5–2× só com bruto 4K.
- **Com zoom 1,0 o `foco` não desloca nada:** o bruto tem o mesmo aspecto do quadro. A 1,12, o deslocamento lateral possível é de ~±115 px.
- **Cor:** usar `cor: {contraste: 1, saturacao: 1, calor: 0}`, porque a cor já veio corrigida e não se empilha correção. `vinheta` 0,25; `grao` 0,03.
- **Junções internas** (silêncios já tirados) não aparecem na `montagem`, mas também precisam de reenquadramento (ver "Ritmo").

**Cenário medido** em 4 quadros (0:30, 6:40, 15:00 e 21:40), câmera fixa:

| Elemento | Posição (fração do quadro) | Cor medida |
|---|---|---|
| Parede | fundo inteiro, em degradê | #E26E3C perto do abajur → #DF7D4F (x 0,3) → #D5986D à direita |
| Rosto | centro em x ≈ 0,47; olhos em y ≈ 0,27–0,29; cabeça de y 0,12 a 0,42 | — |
| Ombros e mãos | x 0,29–0,67; as mãos gesticulam até x ~0,62 | camisa branca |
| Abajur aceso | x 0,05–0,26, y 0,05–0,88; lâmpada em ~(0,20; 0,21) | — |
| Tablet de costas | x 0,64–0,92, y 0,62–0,88 | preto |
| Mesa | y > 0,88 | preta |

- **`foco` inicial: [0.47, 0.28].** Confirmar num quadro em resolução cheia antes da prévia.
- **Área livre padrão:** parede à direita, x 0,66–0,95 e y 0,06–0,58, acima do tablet. É ali que entram card, painel e título lateral. A esquerda é do abajur.
- **Contraste sobre a parede (crítico):**

  | Texto | Contraste com a parede |
  |---|---|
  | Acento #ff6a1a | ≈ 1,1:1 (some) |
  | Creme #F2F4F8 | 2,2–2,6:1 (fraco) |
  | Preto quente #0B0B0E | 6–7,8:1 (bom) |

  - **Com o rosto nítido, o texto direto na parede sai só em preto quente.** É o "preto sobre laranja" da ref (31–33 s), que o cenário já dá de graça.
  - Creme e acento só entram sobre superfície escura: card de vidro escuro, rosto desfocado com `escurecer` ≥ 0,4 ou tela grade.
- **Texto atrás da pessoa:** só na parede lisa acima e ao lado da cabeça (y < 0,55, x 0,28–0,95). Abajur e tablet não entram no recorte, que só pega o "humano". Um texto atrás passaria na frente deles.
- **Ideia a aprovar:** a lâmpada do abajur como o "ponto de luz" da ref. Mergulho na lâmpada (zoom até 1,25 + estouro de brilho) → tela escura com o ponto no mesmo lugar (continuidade de objeto).

## Formato
- **Quadro:** horizontal 16:9, **1920×1080, 30 fps** (`modelos.json`). A regra do Instagram (24 fps) não vale aqui.
- **Composição:** `MixEdit` (`MotorCamadas`), com `"modelo": "mix-edit-youtube"`. Render com `--gl=angle`, que já está no `modelos.json`.
- **Duração típica:** 10–25 min.
- **Áreas seguras:**
  - margem de 5% para tudo (96 px nas laterais, 54 px em cima e embaixo);
  - títulos a partir de 7,5% (144 px);
  - nada essencial abaixo de y 88% (barra do player e legenda CC);
  - canto inferior direito livre (x > 85%, y > 80%), para a marca d'água do canal;
  - nos últimos 5–20 s, a metade direita fica livre para os elementos da tela final do YouTube.
- **Legibilidade no celular em pé:** o 16:9 fica com ~390 pt de largura (escala ≈ 0,2).
  - Todo texto que precisa ser lido tem **maiúscula ≥ 44 px** (corpo ≥ 60 px).
  - Micro-rótulo abaixo disso é só textura.
- **Capítulos do YouTube:** 0:00 obrigatório, no mínimo 3, cada um com ≥ 10 s.

## Estrutura do vídeo
### Intro (0 a ~50 s), beat a beat
- **O quadro 0 já é o rosto falando a promessa do título.** A métrica "Intro" do YouTube Studio mede a % do público que passa dos 30 s.
- **Nada antes da fala:** sem ponto de luz, logo ou "fala, pessoal" no começo. A apresentação vem depois da pergunta e do título.
- **Tempos:** são alvos; o corte final segue a fala.

| # | Saída (s) | Duração | O que se vê | Peças | Som |
|---|---|---|---|---|---|
| 1 | 0,0–5,0 | 120–150 q | **Gancho falado.** Rosto com `zoom` `[1.00, 1.20]` `linear`. A 1ª palavra em ≤ 6 q e a palavra-chave do título nos 3 primeiros segundos. 1 `titulo` com 2–4 palavras-chave (para o autoplay mudo), em preto quente na parede, x 0,66–0,94, y 0,15–0,45 | `fala` + `titulo` | `risers/risers_03_riser-2` (6 s), vol 0,25, terminando no 1º cartão do beat 2 |
| 2 | 5,0–7,6 | 78 q | **Text Match Cut** (seção própria) | `tela` + `match-cut` (sobre `{pausa: 2.6}` ou sobre a fala) | ver a seção |
| 3 | 7,6–15,0 | 150–270 q | **Volta ao rosto** (a pergunta) com zoom no sentido oposto (`[1.18, 1.05]`, `suave`) + 3–5 **flashes de fotos** nos substantivos | `fala` + `flash-foto` | `camera-shutters/camera-shutters_02_little-bit-hard-cammera-shutter`, vol 0,45 por foto |
| 4 | 15,0–20,0 | 90–180 q (manda a música) | **Tela escura com trilha crescente**: ponto de luz, título do vídeo quente→frio, corte na última nota | `{pausa}` + `tela` `escuro` + `ponto-luz` + `titulo-quente` | trilha sozinha; nenhum SFX na nota |
| 5 | 20,0–24,5 | 120–150 q | **Apresentação "Apple"** (≤ 5 s): cards de vidro com nome, credencial, ícones das redes e @. Mostra credencial, não "me segue" | `fala` + `apresentacao-redes` | `ui-sound-effects/ui-sound-effects_03_ui-premium-open` 0,55; `pop/pop_06_sweet-ui-open` 0,45 nos ícones |
| 6 | 24,5–34,0 | 150–300 q | **Rosto desfocado com infos técnicas** = prévia do vídeo ("NESTE VÍDEO" + 01/02/03), com termo técnico em card de dicionário | `fala` (`chaves` de desfoque) + `painel-tecnico` (+ `dicionario`) | `data-collect/data-collect_04_data-collect` 0,6 nos números; `ui-sound-effects/ui-sound-effects_21_v4-type-delete-2` 0,35 por linha |
| 7 | 34–50 | 2–3 golpes de 12–24 q | **3D flash** na frente e atrás da pessoa; entra o capítulo 1 | `golpe` / `texto-3d` / `objeto-3d` + `recortes` + `card-capitulo` | `whooshes/whooshes_20_epic-fast-whoosh-345469` 0,6 + `impact_sub` 0,5 |

**O capítulo 1 começa até 0:45–1:00.**

**Beat 3: flashes de fotos**
- **Fotos:** 6–10 q cada, em tela cheia.
- **Flash:** branco de 2 q a 60–80% (nunca 100%).
- **Efeitos:** aberração cromática de 10–14 px → 0 em 4 q; Ken Burns 1,00→1,05.
- **Rosto entre fotos:** ≥ 12 q.
- **Limite:** **≤ 3 flashes por segundo** (WCAG 2.3.1; o público de saúde é mais velho).
- **Fonte:** afirmação da pergunta só com fonte conferida.

**Beat 4: tela escura**
- **Fundo:** #0D0E13 sem grade, como a abertura da ref.
- **Ponto de luz** (q 0–8):
  - acende no centro, em y 47%;
  - núcleo creme de 6–8 px + halo no acento de 60–120 px;
  - pulsa de 0,9 a 1,1 em 30 q;
  - cantoneiras "L" de visor a 3% das bordas (opcional).
- **Título** (2–4 palavras), nasce do ponto:
  - Inter Tight 900, caixa-alta, maiúscula 130–150 px, 1–1,5 q por letra;
  - cada letra chega no acento com glow e esfria para creme em 6–12 q, em onda da esquerda para a direita;
  - sublinhado de 2 px desenhando em 12 q (`entrada`);
  - subtítulo opcional em Instrument Serif itálica, 44–56 px, creme a 70%.
- **Câmera:** push de 1,00 a 1,04, `linear`.
- **Na última nota (±1 q):**
  1. estouro de brilho de 3 q (brightness 1→1,8);
  2. colapso para um ponto em 6–8 q (escala Y 1→0,02, X 1→0, `saida`);
  3. preto por 3–6 q;
  4. beat 5.

**Beat 5: apresentação**
- **Cards:** à direita, em x 0,58–0,94 e y 0,24–0,76.
- **Enquadramento:** `zoom` 1,12 com `foco` [0.9, 0.28]. Isso leva o rosto de x 0,47 para ~0,42 (≈ 100 px) e abre a parede direita.
- **Material:** card de **vidro escuro**, porque a parede é clara.
- **Entrada:** subida de 24 px + blur 12→0 + fade em 10–12 q (`entrada`), com cascata de 4 q entre cards.
- **Ícones:** mola `snappy`, 3 q entre eles.
- **Detalhes:** reflexo diagonal atravessando 1× em 18 q; gradiente do Instagram 1× no ícone.
- **Saída:** blur 0→12 + escala 0,96 em 8 q.

**Beat 6: rosto desfocado**
- **Rosto:** `desfoque` 20–24 px (≈ 1% W) + `escurecer` 0,4, entrando em 8–10 q.
- **Composição:** igual à da tela grade:
  - frase de apoio em cima (linha de base em y 21–27%);
  - objeto visual em y 55–60%;
  - grade opcional a 50%.
- **Linhas:** digitadas a ~2 q por letra, no tempo da fala.
- **Conectores:** desenhados por `evolvePath` em 10–14 q.
- **Dado de estudo:** sempre com `fonte`.

**Beat 7: 3D flash**
- **Golpe:** até 3 ingredientes:
  - flash de 2 q a 70%;
  - punch 1,0→1,10 em 4 q;
  - texto 3D, zoom-blur de 40–80 px→0 em 5–6 q, ou aberração de 10–14 px→0 em 3–4 q.
- **Motion blur:** `CameraMotionBlur` (6–8 amostras) só em trechos de até 24 q.
- **Orçamento de recorte na intro:** ≤ 6 s.

**Versão enxuta (~25 s)**, para temas sem manchetes reais ou com gancho curto:
- Ordem: 1 (0–4 s) → 3 (4–9) → `match-cut-tipo` (9–11) → 4 (11–15) → 6 com o roteiro (15–25) → capítulo 1.
- A apresentação passa para ~1:30 (4 s, card de vidro lateral) ou só para a tela final.

### Corpo
| Elemento | Regra |
|---|---|
| Capítulo | A cada 2,5–4 min (5–8 num vídeo de 20–25 min), nos cortes do roteiro. Os mesmos títulos vão para a descrição |
| Card de capítulo | 60–90 q, sobre rosto desfocado (24 px, `escurecer` 0,45) ou tela grade. `{pausa: 0.8–1.5}` opcional, com a trilha subindo |
| Re-gancho | No início de cada capítulo e em 40–50% do vídeo: uma frase sobre "o que vem" + teaser visual de 2–4 s. Reengajamentos fortes em ~3:00 e ~6:00 |
| Pico | 4–6 por vídeo, 1 por capítulo, ≥ 90 s entre picos, 60–120 q cada. Lugares: o número central, a virada mito × verdade, o mecanismo principal e a conclusão |
| Quebra de modo (troca de paleta: tela de acento, ficha de papel, papel rasgado) | 1 a cada 2–3 min, durando 2–6 s. Nunca o mesmo tipo duas vezes seguidas; cada tipo no máximo 3× |
| Gráfico | 1 por número verificável, no máximo 1 por minuto (6–12 por vídeo) |

### Fechamento e CTA
1. **Último capítulo:** ~4 s entre eventos. A conclusão é o último pico. O resumo entra num `checklist` de vidro à direita (3–5 itens, no tempo da fala).
2. **CTA falado** ("se inscreve", "me segue"): **só aqui**, mais 1 menção curta opcional em 40–50%. Card de vidro com ícone e @ por 3–4 s.
3. **Tela final (10–20 s):** `tela` grade, ou rosto desfocado com `escurecer` 0,45, + `encerramento-youtube`.
   - O ponto de luz fecha o vídeo como abriu a tela escura.
   - @ e ícones ficam à esquerda (x 0,08–0,45).
   - **A metade direita fica livre** para o vídeo sugerido e o botão de inscrever, que o usuário posiciona no YouTube Studio. A peça desenha molduras-guia só na prévia.
   - Trilha do corpo com `fim` na última nota e `fade` 0,25.
4. **Pós-render:** os capítulos (com 0:00) vão para a descrição e o `.srt` vai como legenda (ver "Legenda").

## Ritmo (regras mensuráveis)
**O que a ref384 mede (30 fps):**
- 24 trocas de painel em ~96 s.
- Intervalo médio entre trocas: 2,3 s (0–17 s) → 4 s (17–53 s) → 5,9 s (53–94 s).
- ~6,4 eventos/s no gancho e ~2,3/s no miolo.
- No máximo ~15 q sem elemento novo, sempre com algo ambiente vivo.
- Só 4 cortes secos, todos em troca de mundo.

| Medida | ref384 | Intro (0–50 s) | Corpo |
|---|---|---|---|
| Troca de ideia visual | mediana 100 q (3,3 s); 70 q em 0–17 s | 45–90 q | micro: mediana 120–180 q (4–6 s). Beat: a cada 600–1200 q (20–40 s), nunca > 1800 q (60 s) |
| Eventos | 6,4/s no gancho; 2,3/s no miolo | 4–6/s nos beats 2–3; 1–2/s nos outros | 10–15 por minuto (micro + beat) |
| Lacuna máxima sem evento | ~15 q | 45 q | 300 q (10 s) no rosto. Exceção: frase emocional até 450 q, com push-in contínuo ≥ 4% |
| Dentro de tela gráfica (painel, gráfico, grade) | algo novo a cada 10–45 q | igual | igual; nunca > 60 q sem elemento novo e sempre com algo ambiente vivo (deriva, glow, cursor) |
| Plano de fala sem troca | — | ≤ 150 q | 90–360 q (3–12 s); teto de 450 q (15 s) |
| Corte seco | só na troca de mundo | idem | idem + junções da fala (com reenquadramento) |

**Arco do corpo**
- Do 1º ao 3º minuto depois do gancho: mediana de 3–4 s entre eventos. É onde a queda de público é mais íngreme.
- Meio do vídeo: 5–6 s.
- Rampa de 2–3 s nos 10–15 s antes de cada pico.
- Último capítulo: ~4 s.

**Junções da fala** (as da `montagem` e as que já vêm dentro do bruto)
- **Toda junção muda o enquadramento**, com uma de três saídas:
  - escala ≥ 8% diferente;
  - `foco` x ≥ 0,08 diferente (só funciona com zoom ≥ 1,08);
  - cobrir a junção com B-roll, card ou tela.
  - Base: mais trocas de câmera dentro da mesma cena aumentam atenção e memória sem custo cognitivo (Lang 2000).
- Nunca dois planos seguidos no mesmo enquadramento.
- Junções a menos de 45 q uma da outra: de preferência não reenquadrar duas vezes (cobrir o trecho). **Nunca um plano com menos de 30 q trocando o enquadramento** (pisca o zoom; correção do usuário de 06/10/2026).
- Dentro do rosto desfocado não há corte (ver "Correções do usuário no piloto").
- **Corte:** sempre em fim de palavra (`palavras.json`), no grid de quadros.
- **Respiro:** ~~4–8 q entre frases e 12–20 q na troca de assunto~~. **Decisão do usuário (05/10):** sem respiro entre frases (aperto automático, ver "Decisões do usuário"); pausa só onde a edição pede (título, capítulo).
- **Microfade:** 1–2 q na voz em cada junção. O motor ainda não faz (peça `microfade`).

**Junções internas do bruto**
- **Como achar:** pela fala, onde há intervalo < 0,05 s entre frases no `palavras.json`, cruzada com a diferença de quadro (`tblend`). O detector `juncoes.mjs` ainda está a calibrar.
- **Medição de 05/10:**
  - a varredura `scene > 0,04` do bruto levou 8,5 min e achou só 78 eventos, no nível do ruído;
  - o limiar do `assistir.mjs` (0,3) não pega jump cut no mesmo enquadramento.
- Até o detector existir, conferir nas folhas de quadros.

**Decupagem**
- Rodar `decupar.mjs` (fica a última tomada) e revisar `decupagem.md` lendo o texto.
- Erro que não se repete sai com `--tirar N`.

## Layouts e camadas
| Layout | Uso | % do corpo |
|---|---|---|
| `fala` A/B/C em tela cheia (ver "Movimento contínuo") | Padrão | 65–75% |
| `fala` + card ou painel na área livre à direita | Lista curta, número, definição rápida, com a pessoa nítida | dentro dos 65–75% |
| `fala` desfocada + infos (`desfoque` 20–28 px, `escurecer` 0,35–0,45; o bloco inteiro numa cena só) | Definição, mecanismo, lista, roteiro. É o "beat" mais barato | 8–12% |
| `fala` + título atrás (recorte) | Conceito central | picos (≤ 4 usos, ≤ 10 s) |
| `tela` grade (mundo técnico) | Título-impacto, diagrama, gráfico, painel, manchete falada | 8–12% |
| `tela` acento, papel ou escura | Quebra de modo, beat 4 e tela final | 2–4% |
| `broll` com Ken Burns | Substantivo concreto, número, print de estudo | 8–12% |

**Cobertura total** (B-roll + telas + rosto desfocado): 25–35% do corpo, com teto de 40% num capítulo muito visual.

**Composição das telas gráficas** (vale também sobre o rosto desfocado):
- **Grade de layout:** 20 colunas de 96 px.
  - Margem mínima de 1,5 coluna (144 px).
  - Títulos nas colunas 2–3 (x 192–288).
- **Divisão vertical:**
  - frase falada no terço de cima, com linha de base em y 21–27%;
  - objeto visual com centro em y 55–60%;
  - rodapé (12–15% de baixo) vazio ou só com micro.
- **Respiro:** ≥ 60% do quadro é só fundo; no máximo 12 palavras legíveis por tela.
- **Alinhamento:** à esquerda, com frase e objeto na mesma borda esquerda. Só o título-impacto é centrado.
- **Duas colunas:** objeto com 44% W à esquerda, vão de ~58 px, lista com 48% W à direita.

**Hierarquia por tela**
- 1 destaque (título-impacto **ou** objeto) + 1 frase de apoio + 0–n micro-rótulos decorativos.
- Escala: título ≈ 4,2× a frase; frase ≈ 3,5× o micro.

**Sobre o rosto nítido**
- Fora dos picos, no máximo 1 peça por vez (+ rodapé de fonte).
- Nada na faixa de ±12% da altura em volta do rosto.
- Card nunca cobre o rosto. Grade nunca sobre o rosto nítido.

**Nos picos:** até 4 camadas ao mesmo tempo (vídeo + 3D + texto + efeito).

## Tipografia
- **Fonte:** A (Inter Tight + Instrument Serif); nada de fonte nova.
- **Pesos carregados hoje:** Inter Tight 300/500/600/800/900; Instrument Serif só em itálico.

| Papel | Fonte | Maiúscula (corpo) | Tracking e linha | Cor | Uso |
|---|---|---|---|---|---|
| Título-impacto | Inter Tight 900, caixa-alta | 200–250 px (275–345 px); 60–76% W; até 2 linhas, a 2ª com 80–100% da 1ª | −0,02em (mais aberto que o CUT); linha 0,9 | creme, com gradiente horizontal até gelo #AFC8DA na última sílaba; palavra-chave no acento | Tela grade: número ou conceito central |
| Palavra na tela de acento | Inter Tight 900, caixa-alta | 330–360 px (455–495 px); 60–76% W; 1 palavra | −0,02em | #0B0B0E | Quebra de modo, `match-cut-tipo` |
| Título com a pessoa | Inter Tight 900 | lateral: 110–150 px (150–205 px). Atrás da cabeça: 260–340 px, 70–80% W, y 12–45% | −0,02em | na parede, #0B0B0E; no escuro, creme ou acento | Conceito central com a pessoa em cena |
| Título da tela escura | Inter Tight 900, caixa-alta | 130–150 px (180–205 px) | −0,02em | acento → creme | Beat 4 |
| Palavra-chave (sinalização) | Inter Tight 800–900 | 70–115 px (96–160 px) | −0,02em | na parede, #0B0B0E; no escuro, creme ou acento | 1–4 palavras sobre o rosto |
| Número | Inter Tight 900, `tabular-nums` | 100–130 px (140–180 px); em painel, 35–52 px (48–72 px) | −0,02em | creme, com o valor-chave no acento | Contador, gráfico, painel |
| Frase falada (apoio, manchete falada) | Inter Tight 600, sentence case | 44–56 px (60–77 px); 1 linha ≤ 66% W; 2ª linha a 1,63× a maiúscula (base a base) | −0,02em | creme a 85%; palavra ativa no acento | Telas gráficas e rosto desfocado |
| Abertura leve | Inter Tight 300 | 90–100 px (~130 px), ~70% W, sublinhado de 2–3 px no acento | +0,01em | creme | 1ª frase de uma tela escura |
| Serifa | Instrument Serif itálica | corpo de 72–96 px no título de capítulo; 44–56 px no subtítulo; 40 px na credencial | −0,01em | creme (70–100%) | Elegância, contraste com a grotesca |
| Dicionário | Instrument Serif **normal** (carregar) + itálica | entrada com corpo de 110–130 px; definições em itálica de 30–36 px, entrelinha 1,6 | — | creme; as sílabas viram acento da esquerda para a direita | Termo técnico ("gre·li·na") |
| Rótulo de painel | Inter Tight 500–600, caixa-alta | corpo de 20–24 px | +0,08 a +0,16em, `tnum` | creme a 60% / #8A8F9C | Apoio. Nada essencial fica só no rótulo |
| Micro (meta, "Fig. 1 —") | Inter Tight 600 caixa-alta, 16–22 px; "Fig." em Instrument Serif itálica, 24–28 px | — | +0,16em | #9C9CA8 | Textura (ilegível no celular) |
| Fonte do dado | Inter Tight 500 | corpo de 26–30 px | — | creme a 70% | Peça `fonte` |
| Marca | Inter Tight 600 | @ com corpo de 36–40 px | — | creme | Apresentação e tela final |

- **Mono para código ou prompt:** **não**, por padrão (a fonte está decidida). O painel usa Inter Tight 500 com `tnum`.
- **Gelo:** nunca em palavra solta.

### Animações de texto (q a 30 fps)
**Entradas**

| Nome | Como | Uso | Ref |
|---|---|---|---|
| Cascata Apple (`titulo`, já existe) | Palavra por palavra: blur 12→0, subida de 0,35em, escala 0,92→1, em 11 q (`entrada`), cascata de 2–3 q | Padrão do corpo | pesquisa Apple |
| Digitação quente | 1–1,5 q por letra em título (2 q quando acompanha a fala). A letra nasce no acento com glow e 1 q de blur, sem interpolar posição, e esfria para creme 6–12 q depois, em onda (atraso de 1–1,5 q por letra) | Títulos de tela escura e grade | ref 1,77–3,3; 4,0–5,0 |
| Fantasma | A linha aparece antes só em contorno (1,5 px, #9AA0B0 a 40%); depois o preenchimento varre da esquerda para a direita | Variante da digitação | ref q194–204 |
| Slam (palavra batendo) | Escala 1,10–1,15→1 e blur 10→0 px em 2–3 q (expo-out), sem overshoot. O glow decai em 8–12 q | Título-impacto, palavra de pico | ref q371, q382, q2790 |
| Karaokê | A palavra surge em cinza fantasma (35%) quando a fala dela começa, enche no acento letra a letra junto com a fala e vira creme quando a próxima começa. A próxima não aparece antes da hora | Manchete falada | ref 3,3–8,0 |
| Máscara de linha | Cada linha sobe de translateY 100% para 0 dentro de `overflow: hidden`, em 14–18 q, com defasagem de 4 q | Listas e frases longas em card | pesquisa Apple |
| Texto vira cabeçalho | A frase sobe e encolhe para ~70% em 4 q (expo-out) e passa a ser o título da tela seguinte | Continuidade entre telas | ref 3,30 |
| Contador | Conta em 30–45 q (expo-out, `Intl.NumberFormat('pt-BR')`) e assenta com escala 1,04→1 em 6 q. Variante caça-níquel: 6–8 q por dígito, em sequência; sublinhado desenhado em 8 q | Números | ref q395–420 |
| Palavra por batida | 1 palavra por tela, trocando no ritmo da fala (2–13 q por palavra; a última segura 15 q), com 1 q de fantasma sobreposto na troca | Tela de acento | ref 31,3–33,3 |

**Saídas**
- **Apple (padrão):** 9–12 q, ease-in, blur 0→10 px, subida de −20 px. O `titulo` já sai assim: 9 q, blur 14.
- **Chicote:** 3 q em expo-in + blur direcional crescente até 20–40 px, sem fade. Usar na troca entre telas.
- **Outras:** o texto vira cabeçalho (continuidade) ou morre no corte da cena.
- **Sobreposição mínima entre saída e entrada:** 1 q.

**Brilho e sombra**
- Texto no acento: `0 0 18px rgba(255,106,26,.55), 0 0 48px rgba(255,106,26,.25)`, para maiúscula de ~150 px; escalar na proporção.
- Título creme: `0 0 30px rgba(245,241,234,.18)`.
- Creme sobre o rosto escurecido: `0 4px 14px rgba(0,0,0,.35)`.
- Preto quente sobre a parede: sem sombra.

## Legenda
- **Padrão do MIX: sem legenda queimada** (`legenda: false` no estilo). Motivos:
  - texto que repete a narração piora a aprendizagem (Mayer, redundância);
  - a dublagem automática do YouTube (com português) e a TV mostrariam o texto queimado;
  - a legenda CC atende acessibilidade e busca.
- **Legenda CC:**
  - gerar um `.srt` PT-BR a partir do `palavras.json` **corrigido** (`corrigir-palavras.mjs`) e **no tempo da saída**, porque o `palavras.srt` do `assistir.mjs` está no tempo do bruto;
  - script novo: `srt-saida.mjs`;
  - o arquivo sobe no YouTube como legenda.
- **Texto queimado é sinalização** (palavra-chave junto do gráfico ajuda, pelo próprio Mayer):
  - 1–4 palavras: palavra-chave, número, termo ou nome de estudo;
  - frequência: 1 a cada 10–20 s (≈ 1 em cada 3–4 frases);
  - no ar: 0,5 s + 0,33 s por palavra, com mínimo de 45 q e padrão de 60–90 q;
  - entrada: blur 8→0 + subida de 2% da altura em 6–10 q; saída em 6–9 q;
  - **primeiros 5 s: palavras-chave na tela**, por causa do autoplay mudo no feed (a confirmar).
- **Manchete falada:** só em telas gráficas e no rosto desfocado. É a frase dita em 1 linha no topo à esquerda (x 7,5–10%, linha de base em y 21–27%), com karaokê no acento.
- **Se o usuário pedir legenda queimada:** `legenda: true` (legenda padrão do motor, palavra a palavra) com `legendaY` 0,82, para não passar de y 88%.
- **Transcrição:** corrigir antes da prévia continua obrigatório, porque os textos queimados e o SRT saem dela.

## Text Match Cut
**Definição:** a mesma palavra fica travada no mesmo ponto da tela enquanto o layout em volta troca muito rápido. São 8–12 trocas por segundo, 1 palavra focal e um som percussivo curto.

| Parâmetro | Valor |
|---|---|
| Palavra focal | 1 (ex.: "sono", "açúcar") |
| Âncora | Centro da caixa da palavra em (960, 500) px = (0,5; 0,463) |
| Altura da caixa da palavra | 120 px (11% H), igual em todos os cartões rápidos. A largura segue a fonte do veículo |
| Prints | 15 reais. Mínimo 8; com menos, alongar os cartões para 4–6 q e nunca repetir print |
| Rampa (q) | 8, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2 = 48 q (mediana de 3 q ≈ 10 trocas/s). Mínimo de 2 q: 1 q vira tremida |
| Último cartão (hold) | 30 q no print mais forte. q 0–4 parado; q 4–18, recuo ancorado até a manchete inteira **e o veículo** caberem em 1728×880 px (`entrada`); a partir do q 10, rodapé `fonte` ("Veículo, dd/mm/aaaa") |
| Push | Escala global de 1,00 a 1,06 (`linear`) nos cartões rápidos, ancorada na palavra |
| Destaque | Caixa #ff6a1a em `multiply` a 85%; padding de 0,15×h na horizontal e 0,08×h na vertical; raio de 6 px. Nasce no 1º cartão (`scaleX` 0→1 em 4 q, da esquerda) e fica; a largura acompanha cada palavra |
| Fora do print | #0D0E13 + o próprio print desfocado em 40 px a 30%; vinheta 0,35; grão 0,04 |
| Luminância | Só prints claros (sem modo escuro alternando). No máximo 3 inversões por segundo de ≥ 10% de luminância em > 25% da tela |
| Deriva | ≤ 2 px, conferida com `debug` numa folha recortada em volta da âncora |
| Som | `camera-shutters/camera-shutters_01_camera-shutter` 0,4 só nos cartões de ≥ 4 q. 1 `risers/risers_02_rjd-riser` (1,0 s) terminando no hold. `clicks/clicks_01_cinematic-click` 0,6 no 1º q do hold |

**Ética (regra do projeto)**
- **Só print real, intacto e com o veículo visível.**
  - Sem IA: nem gerar, nem "melhorar".
  - Sem templates que imitam veículos (matchcut.news, workflows que geram manchete por IA).
  - Sem montar manchete com fonte de jornal.
- **O destaque é anotação nossa por cima** (`multiply`, letras intactas). O hold mostra a manchete inteira, para o recorte não mudar o sentido. Exemplo do risco: travar "açúcar" em "açúcar não mata".
- **A manchete diz o que a fala diz.** Nada de manchete de outro contexto usada como "prova".
- **Registro** em `04_broll/internet/manchetes/manchetes.json`, com: arquivo, caixa da palavra, caixa da manchete, veículo, URL, data da matéria e data de acesso.
- **Alternativa sem manchetes: `match-cut-tipo`.** Usa as fontes do kit e nunca simula jornal. Dois modos:
  - **palavra por tela:** #0B0B0E sobre o acento, Inter Tight 900, 60–74% W, 10–20 q por palavra, no ritmo da fala;
  - **frases-tema:** a palavra travada no centro e o resto mudando ("SONO ENGORDA?", "SONO EMAGRECE?"), em 8–12 tratamentos (Inter Tight 300/500/800/900, Instrument Serif itálica; creme, acento ou preto sobre acento).
- **Opção de autoridade:** títulos reais de estudos no PubMed (layout idêntico, revista visível). A palavra fica em inglês, então é decisão do usuário.

**Captura dos prints**
- **Fontes, em ordem:** Google Notícias (o card já junta veículo e manchete) → página da matéria.
  - Recusar cookies não essenciais.
  - **Não contornar paywall nem CAPTCHA:** se o site bloquear, pular.
- **Caminho A (padrão): Claude in Chrome.**
  1. Zoom do navegador em 175–200%.
  2. Rodar a função abaixo no `javascript_tool`. Ela devolve a caixa em px do print; no Chrome, o `devicePixelRatio` já inclui o zoom.
  3. Capturar e salvar em `04_broll/internet/manchetes/mNN.png`.
  - **A resolução da captura não foi verificada.** Se vier reduzida, multiplicar a caixa por `larguraPNG / (innerWidth × dpr)`.
- **Caminho B (a construir): `capturar-manchete.mjs`.**
  - Chrome headless via CDP (WebSocket nativo do Node 24).
  - `Emulation.setDeviceMetricsOverride {1920, 1080, deviceScaleFactor: 2}` → a mesma função → `Page.captureScreenshot` (3840×2160).
  - Só funciona em páginas abertas.
- **Caminho C:** caixa digitada à mão e conferida com `debug`.
- **Qualidade:** a palavra precisa ter ≥ 100 px de altura de caixa no PNG (escala ≤ 1,2; nunca ampliar mais de 1,3×).

```js
async (palavra) => {
  await document.fonts.ready;
  const re = new RegExp(`(?<![\\p{L}\\p{N}])${palavra}(?![\\p{L}\\p{N}])`, 'iu');
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode()); ) {
    const m = re.exec(n.data); const h = n.parentElement?.closest('h1,h2,h3,[role=heading]');
    if (!m || !h) continue;
    h.scrollIntoView({block: 'center', behavior: 'instant'});
    const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
    const b = r.getBoundingClientRect(), d = devicePixelRatio;
    return {caixa: [b.x * d, b.y * d, b.width * d, b.height * d], largura: innerWidth * d, altura: innerHeight * d,
      manchete: h.innerText, veiculo: document.querySelector('meta[property="og:site_name"]')?.content,
      data: document.querySelector('meta[property="article:published_time"]')?.content, url: location.href};
  }
}
```

## Motion e efeitos (catálogo: quando usar)
| Efeito (peça) | Linguagem | Quando usar | Duração | Máx. por vídeo | Ref |
|---|---|---|---|---|---|
| Card de vidro (`card-vidro`) | Apple | Lista curta, número, credencial, definição ao lado do rosto | 90–240 q (entrada em 15–18 q) | livre (é o beat padrão) | ref 43,0–44,0 (reflexo) |
| Checklist de vidro (`checklist`) | Apple | Solução ou resumo em itens | 4–10 s | 2 | CUT |
| Painel técnico (`painel-tecnico`) | ref | Mecanismo; roteiro "NESTE VÍDEO", sobre rosto desfocado ou grade | 150–300 q | 1 por capítulo | ref 19,6; 30,5; 47,6 |
| Manchete falada (`manchete-falada`) | ref | Junto com toda tela gráfica | a da tela | — | ref 3,3–8,0 |
| Título-impacto com slam (`palavra-impacto` com `entrada: 'pop'`) | ref | Número ou conceito central na tela grade | 45–90 q | 1 por capítulo | ref 5,0; 13,6; 93,7 |
| Título quente→frio (`titulo-quente`) | ref | Tela escura (beat 4), abertura de capítulo forte | 60–150 q | 2–3 | ref 1,77–3,3; 12,3–13,6 |
| Dicionário (`dicionario`) | ref | Termo técnico (grelina, leptina, cortisol) | 90–150 q | 2–3 | ref 64–67 |
| Diff mito/verdade (`diff`) | ref | "− dormir 5 h / + dormir 7–8 h" (nunca sono no lugar do déficit) | 60–120 q | 2 | ref 75 |
| Ficha de papel (`ficha-papel`) | ref | Quebra de modo: mitos riscados à caneta (8 q, curva `risco`), carimbo "MITO" girado −5°, ☒ e ✓. Claramente gráfica: sem timbre, CREF ou cara de laudo | 120–300 q | 2 | ref 53,7–64; 82–88 |
| Tela de acento (`match-cut-tipo`, modo palavra) | ref | Quebra de modo: frase de virada em 3–6 palavras | 45–75 q | 1–2 | ref 31,3–33,3 |
| Gráfico de barras (`grafico-barras`) | Apple + ref | Comparação de 2–4 valores. Monta em 45–75 q, segura ≥ 60 q, sai em 10–12 q | 150–270 q | ≤ 1/min | Tela Dividida |
| Gráfico de linha (`grafico-linha`) | ref | Curva no tempo (cortisol no dia, fome × horas de sono). A linha desenha em 16 q por segmento (`desenho`), com cabeça de glow e anéis no ponto final | 150–270 q | ≤ 1/min | ref 66,6–78,5 |
| Contador (`contador`) | Apple | Número isolado | 60–120 q | — | ref 13,6 |
| Escala (`escala`, a partir da `escala-ph`) | Apple | Valor numa faixa (horas de sono de 4 a 10 h, faixa ideal de 7 a 9 h) | 4–10 s | 1–2 | CUT |
| Traços e conectores | ref | Ligar rótulo a objeto, sublinhar, X de negação. Ponta no acento esfriando para creme | 3–14 q por traço | — | ref q111–359 |
| Faísca ou cometa | ref | Ponta de linha chegando. Impacto: anéis em 5–6 q + partículas por 8–10 q | 6–10 q | — | ref 11,33 |
| Ponto de luz (`ponto-luz`) | ref | Abre a tela escura e fecha o vídeo; é o fio condutor | — | 2–3 | ref 0–1,75; 94–98 |
| Flash de fotos (`flash-foto`) | 3D flash | Beat 3 da intro; re-gancho com 2–3 fotos | 6–10 q por foto | intro + 1–2 | briefing |
| Texto 3D extrudado (`texto-3d`) | 3D flash | Palavra de pico. Entra em rotateY 70°→−5°→0° e z de −800 a 0 em 8–12 q (mola com bounce 0,15); segura 15–30 q com deriva de 4°/s; sai voando para a câmera (escala 1→2,5 + blur de 40 px) em 4–6 q | 30–48 q | 1 por pico | ref 5,33 |
| Objeto 3D (`objeto-3d`) | 3D flash | Objeto do tema (lua, relógio, prato) passando rente à câmera como wipe, ou orbitando atrás da cabeça | 12–48 q | 2–3 | TesteKit |
| Golpe (`golpe`) | 3D flash | Picos e beat 7. Até 3 ingredientes: flash de 2 q a 70%; punch 1,0→1,10 em 4 q ou recuo 1,12→1,0 em 8 q; zoom-blur de 40–80 px→0 em 5–6 q ou aberração de 10–14 px→0 em 3–4 q | ≤ 20 q | 1–2 por pico | pesquisa 3D flash |
| Texto atrás da pessoa (`recortes` + `plano: "atras"`) | 3D flash | Conceito central; 1ª palavra de um capítulo forte | 36–90 q | ≤ 4 usos, ≤ 10 s | CUT |
| Caixa de seleção (`selecao`) | CUT | A palavra do mito que o público acha que importa | 30–45 q | 2 | CUT |
| Papel rasgado (`papel-rasgado`) | CUT | Número revelado; quebra de modo | 32–45 q | 1 | CUT |
| Light leak (`lightLeak()`) | Apple | Só na entrada do card de capítulo | 12–20 q | 1 por capítulo | — |

**Motion blur**
- Filtro SVG direcional (barato) em chicotes e voos.
- `CameraMotionBlur` (6–8 amostras) só em trechos de ≤ 12–24 q.
- `Trail` (4–6 camadas, atraso de 0,5–1) para o eco de saída.

**Não usar:**
- tremida de câmera, RGB split contínuo, glitch, posterize ou "look de filme retrô", neon, mais de um acento;
- flash branco fora dos picos;
- vidro sobre fundo liso: vira "plástico sujo"; usar card sólido #141416;
- o tema da ref (editor de curvas, código, wireframes de software).

## Transições (campo `transicao`: como a cena ENTRA)
Lógica da ref384: **dentro do mesmo mundo, a troca é por movimento**. Corte seco só na troca de mundo (rosto quente ↔ grade técnica ↔ papel ↔ tela de acento) e nas junções da fala, com reenquadramento.

| Nome | Duração | Quando | % das trocas | Som automático | Status |
|---|---|---|---|---|---|
| `corte` (com reenquadramento) | 0 | Junções da fala; troca de mundo | ~70% | — | existe |
| `lente` | 2 q de desfoque na saída + corte seco + 4 q de foco (26 px, escala 1,03→1) | Troca de ideia no rosto | ~15% | `whooshes/whooshes_14_simple-whoosh` em 1 de cada 3. Hoje 0,2: subir para 0,35 no MIX | existe (`trans.lente` [2, 4]) |
| `chicote` | Saída em 3 q (expo-in, blur direcional até 30–40 px, deslocamento de 30–60% W) + entrada em 3–5 q já em movimento no mesmo sentido, com o blur caindo. Variante de relayout: 10–12 q em `expo` | Entre telas gráficas e gráficos; rosto ↔ tela no mesmo assunto | ~10% | `whooshes/whooshes_16_smooth-and-fast-whoosh` 0,5 (`whooshes/whooshes_10_high-and-fast-whoosh` na variante rápida) | a construir |
| `mergulho` | 10–12 q em ease-in (0.55, 0, 1, 0.45) num elemento-alvo, terminando no escuro com o ponto | Entrar num detalhe; tela → beat 4; lâmpada → ponto de luz | ≤ 1 por capítulo | `whooshes/whooshes_03_cinematic-fast-whoosh` 0,5 | a construir |
| `zoom` | 7 q (escala 1,22→1 + blur de 16 px) | Corte disfarçado de ângulo | ≤ 1 por capítulo | `whooshes/whooshes_20_epic-fast-whoosh-345469` 0,45 | existe |
| `blur` | 9 q, crossfade | Só na entrada e saída do card de capítulo e da tela final | ≤ 2 por capítulo | `whooshes/whooshes_16_smooth-and-fast-whoosh` 0,35 | existe |
| `flash` | Pico de 2 q a 60–80% + decaimento de 6–10 q. Hoje: 8 q a 100% | Só nos picos | ≤ 2 por pico | `camera-shutters/camera-shutters_03_smooth-cammera-shutter` 0,45 | existe (duração e opacidade por estilo a fazer) |
| `esticao` | 3 q de esticão vertical de pixels (scaleY 1→3 + blur vertical) | Troca de tela no mesmo mundo; variação do chicote | ≤ 3 por vídeo | `whooshes/whooshes_08_fast-whoosh` 0,4 | a construir (baixa prioridade) |
| `silhueta` | — | **Não usar no MIX** (é assinatura do CUT) | 0 | — | existe |

- **Estouro + colapso para um ponto:** saída especial da tela escura e do fim do vídeo. Faz parte do `titulo-quente` e do `ponto-luz`.
- **Continuidade de objeto** vale mais que qualquer transição: frase → cabeçalho, ponto → linha → moldura, card → tela. Use sempre que a peça permitir.
- **Momento do corte:** a transição cai sempre em fim de palavra.

## Movimento contínuo (zoom, câmera e tokens de curva)
### Tokens de movimento (30 fps)
| Token | q (s) | Curva (cubic-bezier) | Uso | No motor hoje (`kit/tempo.ts`) |
|---|---|---|---|---|
| `micro` | 2 (0,067) | expo-out (0.16, 1, 0.3, 1) | Dissolve, esticão, blur→nítido do slam, troca de cor | `DUR.micro` 0,1 (3 q): ok |
| `rapido` | 4 (0,133) | expo-out | Entrada de palavra, texto virando cabeçalho, achatamento | `DUR.rapido` 0,15: ok |
| `base` | 8 (0,267) | expo-out; pan em `suave` (0.65, 0, 0.35, 1) | Linha curta, conector, pan curto, contorno | `DUR.base` 0,25: ok |
| `lento` | 12 (0,4) | push: expo-out. Mergulho: (0.55, 0, 1, 0.45). Relayout: `expo` (0.87, 0, 0.13, 1) | Push-in, mergulho, card | `DUR.lento` 0,35. O `titulo` do CUT aprovado usa esse valor: **não mudar o global**, criar token do estilo |
| `desenho` | 16 (0,533) | (0.25, 0.15, 0.5, 1) | Arco, moldura dobrando a esquina, gráfico desenhando | novo |
| `risco` | 8 (0,267) | (0.37, 0, 0.63, 1) | Tachado, X, caneta | novo |
| `assento` | 14 (0,467) | quint-out (0.22, 1, 0.36, 1) | Câmera assentando depois de movimento grande | novo |
| `saida` (Apple) | 9–12 (0,3–0,4) | expo-in (0.7, 0, 0.84, 0) | Saída de card e título, com blur 0→10 | `DUR.saida` 0,3: ok |
| `chicote` | 3 (0,1) | expo-in + blur direcional de 20–40 px | Saída por chicote, sem fade | novo |
| `ambiente` | ≥ 90 (3 s) | linear ou seno | Deriva, órbita, glow pulsando | novo |

**Molas**
- A mola padrão do Remotion (stiffness 100, damping 10, fator 0,5) está **proibida**.
- Predefinições da Apple (mass 1):

  | Mola | Stiffness | Damping | Uso |
  |---|---|---|---|
  | `smooth` (0,5 s) | 158 | 25 | padrão |
  | `snappy` | 158 | 21 | pop de ícone |
  | `bouncy` | 158 | 18 | só 3D |
  | elementos pequenos (0,35 s) | 322 | 36 | — |

- Confira com `measureSpring()` quantos quadros cada mola leva para assentar.
- Fora de ícone e 3D: **nenhum overshoot visível**. A `imagem` do kit usa damping 12 e passa do ponto, então precisa do parâmetro `mola`.

**Regras de timing**
- **Cascata:** letras a cada 1–1,5 q (2 q com a fala); palavras a cada 2–3 q; filhos de card a cada 3–5 q.
- **Sobreposição mínima entre saída e entrada:** 1 q.
- **Esfriamento de cor:** 6–12 q por letra, em onda. A cor continua animando depois que a posição parou, e o olho ainda vê movimento.
- **Blur só no pico de velocidade (2–4 q).** O assentamento é sempre nítido.

### Zoom na pessoa (bruto 1080)
| Enquadramento | Escala | `foco` | Parcela do corpo |
|---|---|---|---|
| A, aberto | 1,00–1,03 | não desloca | 45–55% |
| B1, médio centrado | 1,10–1,12 | [0.47, 0.28] | 30–40% (B1 + B2) |
| B2, médio com a parede livre | 1,10–1,12 | [0.9, 0.28]: rosto em x ≈ 0,42 | (junto com B1) |
| C, close | 1,18–1,20 | [0.47, 0.28] | ≤ 15%, no máximo 3 s seguidos |

- **Zoom contínuo em todo plano:** 2–4%, alternando o sentido, com `curva` `suave`. Exemplos: A `[1.00, 1.03]`, B `[1.12, 1.09]`, C `[1.18, 1.20]`.
  - O padrão do estilo (`[1, 1.03]`, alternando sozinho) cobre o A, mas não a regra das junções.
  - Declarar `zoom` em toda cena `fala`, ou usar a peça `enquadramento-auto`.
- **Frase-chave:** push-in de 6–8% em 60–90 q, com `entrada`.
- **Gancho:** `[1.00, 1.20]` `linear` em ~5 s. Beat 3: `[1.18, 1.05]` `suave`.
- **Rosto desfocado:** o motor amplia o vídeo em 1 + 2,5 × desfoque / 1080 para esconder a borda (≈ 1,05 a 24 px). Isso conta como escala.
- **`chaves`:** zoom, desfoque e escurecer animados. O rosto desfoca em 9 q (`entrada`) e volta em 9 q (`saida`), só nas pontas do bloco desfocado (cena que continua um bloco começa com a chave `{t: 0, desfoque: 24, escurecer: 0.45}`, sem rampa).

### Câmera virtual nas telas gráficas
- **Nunca parada:** deriva de 1,00 para 1,03–1,08 em ≥ 90 q (`linear`), ou órbita leve de 1–2°.
- **Push-in:** 1,0→1,2 em 12 q (expo-out), com blur só nos 4–5 q iniciais.
- **Pan para revelar o próximo painel:** 10–15% W em 12–18 q, `suave`; às vezes em 2 tempos (6 + 5 q).
- **Assentamento** depois de movimento grande: 12–14 q (`assento`).
- **No motor:** hoje a `tela` não se move. A peça `camera-tela` resolve isso, com `camera: true` nas camadas presas.

## Cor e acabamento
Proporção 60/30/10: 60% escuro (ou a parede), 30% creme, 10% acento.

| Papel | Hex | Uso e contraste |
|---|---|---|
| Fundo técnico | **#0D0E13** (hoje #0B0B0C) | Tela grade e escura; levemente azulado, como a ref |
| Linha da grade | **#222634** (≈ rgba(150,165,210,.12)), 1,5 px, passo de **96 px** (hoje 80 px, #ffffff17) | `backgroundPosition: 0px 60px`, para as linhas passarem pelo centro (960, 540). Só em tela grade e sobre rosto desfocado (a 50%). Testar 1,5–2 px a 8–10% contra a compressão do YouTube |
| Luz de topo (opcional) | elipse de 60% W × 50% H, centro em y −10%, branco a 4–6% | Tela grade |
| Texto | creme **#F2F4F8** | Identidade |
| Acento | **#ff6a1a** (manter) | 1 conceito por tela, < 5% da área. 6,7:1 sobre #0D0E13. **Nunca direto sobre a parede do cenário** |
| Texto sobre o acento e sobre a parede | **#0B0B0E** | 6,7:1 sobre o acento; 6–7,8:1 sobre a parede |
| Gelo (2ª cor) | **#AFC8DA** | Só no fim do gradiente dos títulos e em objetos de "estado novo" |
| Cinza de apoio | #9C9CA8 (rótulos em #8A8F9C) | — |
| Contorno fantasma | #9AA0B0 a 40% | — |
| Painel | preenchimento #0A0B0F a 92% (esconde a grade); traço de 1,5–2 px #C9CFDA a 75% | Cantoneiras "+" ou "L" de 12–16 px. Borda tracejada 8/6 = "não existe" |
| Card sólido | #141416 | Sobre fundo liso |
| Papel | **#F2F4F8**, tinta **#C2381A** | A tinta dá 4,5:1 no papel; o acento daria só 2,6:1 |
| Acento profundo | #4A1A06 | Extrusão 3D, gradiente de card |

**Vidro (`card-vidro`)**
- **Sobre imagem rica** (rosto desfocado, B-roll):

  | Propriedade | Valor |
  |---|---|
  | Fundo | rgba(255,255,255,.08–.12) |
  | Filtro | `backdrop-filter: blur(20–28px) saturate(140–180%)` |
  | Borda | 1 px rgba(255,255,255,.18) |
  | Sombra | `0 20px 60px rgba(0,0,0,.35)` |
  | Brilho de borda | `inset 0 1px 0 rgba(255,255,255,.3)` |
  | Medidas | raio de 28–36 px, padding de 40–48 px, largura de 560–720 px |

- **Sobre a parede clara (rosto nítido): vidro escuro**, rgba(13,14,19,.55–.70) + blur de 24 px, para o creme ler. O `checklist` já faz assim (`vidro` 0,55).
- **Sobre a grade lisa:** card sólido #141416 ou painel. O vidro sobre fundo liso some.
- **Custo:** animar só a opacidade e chegar ao blur final em ≤ 15 q. Blur de backdrop animado é caro.

**Pessoa**
- Cor neutra no piloto, porque o bruto já veio corrigido. Pele natural: o "punch" de cor vem dos grafismos.
- `vinheta` 0,25: com a parede clara, mais que isso suja os cantos.
- `grao` 0,03 na pessoa e 0,04 nas telas gráficas.

**Flashes (WCAG 2.3.1)**
- No máximo 3 por segundo.
- Flash a 60–80%, nunca 100%.
- Sem flash vermelho saturado em tela cheia.
- A tela de acento cheia entra e sai com corte seco (1 inversão por troca).

## Marca (@soutotreinador)
- **Sem @ fixo durante o vídeo.** O @ trocando de canto na ref é embalagem do repost, e no YouTube o nome do canal já aparece.
  - A marca d'água do canal é ativada pelo próprio usuário no YouTube Studio (canto inferior direito, que fica livre).
- **Apresentação** (beat 5, ≤ 5 s): mostra credencial, não "me segue". Faltam em `kit/marca/marca.json`:
  - nome de exibição;
  - outras redes e o @ de cada uma;
  - credenciais (CREF, especializações);
  - números (só os que o usuário fornecer).
- **Ícones das redes:** `simple-icons` (Instagram, YouTube, TikTok…), em creme monocromático, 44 px.
  - Gradiente do Instagram (#FEDA75→#D62976→#962FBF→#4F5BD5) 1× na apresentação e 1× na tela final, por 48 q.
- **Ícones de informação:** `lucide-react`, traço 1,5 no viewBox de 24, 64–88 px, desenhados por `evolvePath` em 15–20 q.
- **CTA** ("se inscreve", "me segue"): só no fechamento, mais 1 menção opcional em 40–50%.
- **Assinatura da tela final:** ícone do Instagram em creme → gradiente → creme, com o @ embaixo (ref 97,7–101,7).
- **Não copiar da ref:** título fixo "CLAUDE JUST KILLED IT", ícones Ae/Claude, @ do criador.

## B-roll
- **Sem repetição visual** (regra comum). Termos recorrentes ("sono", "fome", "peso", "cortisol") ganham 3–5 variações. Listar os `broll` repetidos antes da prévia.
- **Cobertura:**
  - 25–35% do corpo, somando as telas e o rosto desfocado;
  - plano de B-roll de 3–6 s (90–180 q);
  - no máximo 3 planos seguidos (12 s); voltar ao rosto em ≤ 15 s.
- **Literal, nunca decorativo.** Entra 0–6 q antes do substantivo concreto ou do número. Imagem decorativa atrapalha ("detalhes sedutores": g = −0,33, pior com imagem estática).
- **Ken Burns:** vídeo com 4–8% (o motor usa 6%); foto com 8–12% (o motor usa 12%).
- **Ordem por custo:**
  1. rosto desfocado + card de vidro;
  2. tela grade com diagrama e manchete falada;
  3. biblioteca (`biblioteca.mjs buscar`), depois `04_broll/meus`;
  4. banco gratuito (`stock.mjs`), sempre revisado numa folha de miniaturas;
  5. imagem do Flow (0 créditos) com Ken Burns;
  6. vídeo do Flow, só com aprovação de créditos.
- **Conta para 20 min:** 5–7 min de cobertura ≈ 70–90 inserções sem repetir. Metade sai em telas por código (sem custo de busca) e metade em B-roll.
- **Print de estudo ou manchete:**
  - intacto, com o veículo ou a revista visível;
  - 3–5 s, push-in de 5%;
  - marca-texto #ff6a1a a 35% (`multiply`) no trecho citado;
  - acompanhado da peça `fonte`.
- **Fotos do flash (beat 3):** banco, Flow ou domínio público. Nunca "melhorar" foto do Google.
- **IA:** imagem do Flow só como metáfora claramente fictícia ou ilustração genérica. Nunca para ilustrar um dado, e sem pessoas reais identificáveis.
- **Objetos para 3D e overlays:** gerar no Flow com fundo azul #0000FF e recortar com chromakey (`CLAUDE.md`).

## Áudio
### Música
**Padrão do usuário (05/10/2026):** trilha só na intro, com parada brusca no título, e corpo sem música (ver "Decisões do usuário"). O resto desta seção só vale se ele pedir trilha no corpo.
- **Pelo menos duas trilhas:**
  - **intro:** investigativa e crescente, com batida final clara, que **some na última nota** (beat 4);
  - **corpo:** outra trilha, documental calma ou ambient com pulso, 80–110 BPM, sem vocal.
  - Trocar de trilha ou de seção a cada 1–2 capítulos (5–8 min).
  - Pedir 2–3 opções com link por bloco (intro, corpo A, corpo B).
  - Não repetir a trilha do vídeo anterior (o suspense investigativo do vídeo 1 fica de fora).
  - **O motor hoje aceita 1 trilha só:** `musica` em lista é pré-requisito.
- **Alinhamento da intro pelo fim:**
  - `musica.ini = t_ultimaNota_na_trilha − t_corte_do_beat4_na_saida`;
  - achar o ataque da nota pelo RMS do ffmpeg em janelas de 50 ms (salto de ≥ 10 dB depois do trecho baixo) e **validar ouvindo**;
  - `fim` = fim natural da nota (≤ 1,5 s depois do ataque); `fade` 0,25.
- **Níveis:**

  | Trecho | `vol` (com fala) | `volSemFala` | Nota |
  |---|---|---|---|
  | Intro | 0,10 | 0,55–0,7 nos beats 2 e 4 | a trilha é protagonista |
  | Corpo | 0,06–0,09 | 0,2–0,28 nas pausas e nos cards | trilha 18–25 dB abaixo da voz (a medir) |

  - Trilha presente em 70–85% do corpo. Tirar (fade de 12–18 q) em 1–2 momentos sérios, deixando 5–15 s de voz seca.
  - `quedas` com vol 0,7 (−3 dB) por 0,3 s junto de cada SFX de pico.
- **Master:**
  - −14 LUFS integrado, pico real ≤ −1 dBTP (`ffmpeg -af ebur128=peak=true`);
  - se estiver fora, perguntar junto com a pergunta do áudio. Nada de tratamento por padrão.
- **Content ID:**
  - faixas do Pixabay podem estar registradas (a funk groove do catálogo está);
  - preferir faixas sem esse aviso;
  - guardar o certificado de licença para contestar.

### Efeitos (Motionix, em `sfx/biblioteca/motionix/`, sem `.wav`)
**Resposta ao piloto do CUT** ("os efeitos sonoros para os gráficos, para alguns textos, eu não escutei"):
- Lá, os sons de gráfico e texto ficaram em 0,3–0,45.
- Os cliques de 0,09–0,14 s (`clicks/clicks_01_cinematic-click`, `clicks/clicks_05_high-click`) somem por baixo da voz.

Regras no MIX:
- **Todo gráfico, card, rodapé de fonte, card de capítulo e palavra-chave entra com som.** Evento de nível beat ou pico sem som conta como erro na checagem.
- **Volume final de 0,55–0,8.** O motor hoje multiplica o som de entrada das peças por 1,5 e corta em 0,7; o estilo MIX ganha um ganho próprio com teto de 1,0.
- **Durante a fala, preferir sons com corpo (≥ 0,3 s):** `pop/pop_05_smooth-pop`, `ui-sound-effects/ui-sound-effects_03_ui-premium-open`, `data-collect/data-collect_04_data-collect`. Clique curto só em silêncio, ou com vol ≥ 0,6.
- **Conferir na prévia com `astats`:** o pico do SFX fica no máximo ~6 dB abaixo do pico da voz no mesmo trecho. **Validar ouvindo** (eu não ouço áudio).

| Evento | Som | Vol final |
|---|---|---|
| `titulo` e palavra-chave | `whooshes/whooshes_02_cinematic-fast-normal-whoosh` (automático) + `pop/pop_05_smooth-pop` no pouso | 0,45 / 0,55 |
| Slam (título-impacto) | `whooshes/whooshes_03_cinematic-fast-whoosh` + `clicks/clicks_01_cinematic-click` no assento | 0,5 / 0,65 |
| Digitação de título ou de linha de painel | `ui-sound-effects/ui-sound-effects_21_v4-type-delete-2`, 1 por palavra ou linha (não por letra) | 0,35 |
| Card de vidro, checklist, apresentação | `ui-sound-effects/ui-sound-effects_03_ui-premium-open` | 0,55 |
| Item de lista (✓) | `ui-sound-effects/ui-sound-effects_13_ui-granular-button-select-9` | 0,55 |
| Ícone das redes, brilho do Instagram | `pop/pop_06_sweet-ui-open` | 0,45 |
| Barras do gráfico | `pop/pop_05_smooth-pop` por barra (≥ 8 q de distância) + `data-collect/data-collect_04_data-collect` na contagem | 0,55 / 0,6 |
| Linha do gráfico desenhando | `whooshes/whooshes_07_data-whoosh` | 0,5 |
| Selo ou destaque do gráfico | `clicks/clicks_01_cinematic-click` | 0,65 |
| Contador | `data-collect/data-collect_04_data-collect` | 0,6 |
| Conector desenhando | `ui-sound-effects/ui-sound-effects_18_ui-stretch` | 0,4 |
| Rodapé `fonte` (hoje sem som) | `clicks/clicks_05_high-click` | 0,5 |
| Card de capítulo | `ui-sound-effects/ui-sound-effects_03_ui-premium-open` + `whooshes/whooshes_15_slow-and-smooth-whoosh` | 0,55 / 0,35 |
| Dicionário | `ui-sound-effects/ui-sound-effects_10_ui-enter` | 0,5 |
| Caneta riscando (ficha) | `swish_air` (sintetizado) | 0,45 |
| Carimbo | `impact_sub` + `clicks/clicks_01_cinematic-click` | 0,4 / 0,6 |
| Dinheiro ou preço | `money/money_02_cinematic-money-2` | 0,45 |
| Golpe 3D | `whooshes/whooshes_20_epic-fast-whoosh-345469` + `impact_sub` | 0,6 / 0,5 |
| Antes de um pico | `risers/risers_05_smooth-riser` (2,5 s) ou `risers/risers_02_rjd-riser` (1 s), terminando no golpe | 0,35 |
| Flash de foto | `camera-shutters/camera-shutters_02_little-bit-hard-cammera-shutter` | 0,45 |
| Ponto de luz acendendo | `shimmer` (sintetizado) | 0,3 |
| Transições | automáticas (tabela de transições) | — |

- **Densidade:**
  - no corpo, 1 som a cada 5–10 s em média;
  - nunca 2 sons a menos de 8 q um do outro (exceto os pares da mesma peça);
  - na tela de acento, a fala marca o ritmo: sem som por palavra.
- **`impact_sub`:** no máximo 2 na intro e 1 por pico (≤ 6 no vídeo). **Risers:** no máximo 2 na intro e 1 por pico.
- **Voz:** perguntar no fim, como sempre. O bruto já veio tratado pelo usuário, então o comparativo inclui o original sem tratamento.

## Custo de render
| Item | Custo | Base |
|---|---|---|
| Base (rosto + camadas DOM) | Final: **6–9 s de render por segundo de vídeo**, ou seja, ≈ 2,2–3,3 h para 22 min. Prévia em meia resolução: ≈ 3–4 s/s (≈ 1–1,5 h) | Estimativa: o 9:16 a 24 fps mede 7,1 s/s no final, e o MIX tem 25% mais quadros. **Medir no piloto** com `--trecho 0 60` |
| 3D (`ThreeCanvas`) e efeitos WebGL em resolução cheia | ≈ 0,8–1,2 s por quadro (24–36 s/s) | 0,4 s/q medido no TesteKit a meia resolução, × 2–3 |
| `CameraMotionBlur` | Multiplica o custo da cena pelo número de amostras (6–8×) | — |
| Recorte da pessoa | 1,3 s de CPU por quadro do bruto 1080 (39 s por segundo de recorte). Etapa separada, nunca junto com render | `CLAUDE.md` |
| `backdrop-filter` animado | Caro: chegar ao blur final em ≤ 15 q e mantê-lo fixo | — |
| Arquivo final | ~10–11 Mbit/s (CRF 17, taxa do piloto CUT) → ~1,5–1,8 GB para 22 min | piloto CUT |

**Orçamento por vídeo de 20 min**

| Peça | Limite | Custo extra |
|---|---|---|
| 3D | ≤ 15 s no total (4–6 picos de 2–3 s) | ≈ +6–9 min |
| Recorte | ≤ 10 s, em até 4 usos (≤ 6 s na intro) | ≈ 6,5 min de CPU |
| WebGL leve (glow, light leak, aberração em foto) | ≤ 30 s | — |
| `CameraMotionBlur` | só em chicotes e golpes de ≤ 12–24 q | — |

- **Meta:** peças pesadas em ≤ 2% do corpo; o final em ≤ 1,15× o custo base.
- **Prévia:** por capítulo (`--trecho`), com aprovação por partes.
- **Final:** em segundo plano, avisando o usuário para não fechar a sessão. Render por partes + junção (`render-partes`), para uma falha não custar 3 h.
- **Sempre** `--gl=angle --concurrency=2`. Nunca rodar render e recorte ao mesmo tempo.

## Checagens antes da prévia (`checar-mix.mjs`)
1. Nenhuma lacuna > 300 q sem evento no rosto; nenhuma > 60 q dentro de tela gráfica.
2. Nenhuma junção sem mudança de enquadramento (escala ≥ 8% ou `foco` x ≥ 0,08) ou sem cobertura; **nenhum plano de fala < 30 q trocando o enquadramento; nenhum corte dentro do rosto desfocado** (ERRO no checador).
3. Nenhum `broll` repetido.
4. Todo número com `fonte`.
5. Todo evento de nível beat ou pico com som; nenhum par de sons a < 8 q.
6. Cobertura de 25–35% em cada capítulo.
7. Picos a ≥ 90 s um do outro; 3D e recorte dentro do orçamento.
8. No máximo 3 flashes por segundo. Medição aproximada: `signalstats` por quadro, contando inversões de YAVG ≥ 26 com o lado escuro < 204. **Nenhuma piscada de 1–2 quadros** (≥ 6 de YAVG fugindo dos vizinhos), fora transição flash e golpe: `checar-mix.mjs <proj> --video <prévia ou final>`. Rodar também no final, antes de entregar.
9. Nenhum texto creme ou no acento direto sobre a parede (cena `fala` sem desfoque, sem escurecer e sem card por baixo).
10. Nada essencial abaixo de y 0,88; tela final com a metade direita livre.

## A confirmar com o usuário
1. **Acento:** laranja #ff6a1a, que combina com a parede do cenário. Com ele, texto direto na parede sai em preto quente.
2. **Dados da apresentação:** nome de exibição, outras redes e @, credencial (CREF, especializações) e números.
3. **Posição da apresentação:** em ~20 s (versão completa, como no briefing) ou em ~1:30 / só na tela final (versão enxuta, recomendada pela pesquisa de retenção).
4. **Text Match Cut:** prints reais de manchetes sobre sono e emagrecimento ou `match-cut-tipo`? Títulos do PubMed em inglês?
5. **Legenda:** só CC, sem legenda queimada?
6. **Trilhas:** intro + 1 ou 2 no corpo? Pausa de respiro nos capítulos?
7. **Ponto de luz:** usar a lâmpada do abajur?
8. **Dica de gravação para os próximos:**
   - 4K para closes de 1,5–2×;
   - mãos livres e parede lisa atrás da cabeça nos trechos de texto atrás.

## Peças do kit a construir

### Já existe no motor (reaproveitar do CUT em 16:9)
- As peças medem em `min(W, H)/1080`. No 16:9 essa escala é 1, então os px de 1080 valem direto.
- As larguras em fração do quadro precisam ser recalibradas para 1920 px.
- `seguro` (zonas do Reels) fica `false` no MIX.

| Peça | Onde | O que faz | Ajuste para o MIX |
|---|---|---|---|
| `titulo` | camada | Cascata Apple, `*destaque*`, 4 fontes, saída com blur | Já é a entrada Apple (11 q, cascata de 3 q). Hoje encaixa em 88% W: precisa de `largura` (fração) e `sombra`. Na parede, `cor` #0B0B0E |
| `imagem` | camada | PNG com pop de mola e flutuação | A mola passa do ponto (damping 12): criar o parâmetro `mola: 'suave'` |
| `palavra-impacto` | camada (frente ou atrás) | Caixa-alta 900 pela largura, extrusão, entradas letras/pop/virar | Título-impacto e texto atrás: `largura` 0,6–0,76, `alturaMax` 250 (360 na tela de acento), `extrusao: false` no Apple, `seguro: false` |
| `selecao` | camada | Caixa de seleção estilo Figma | `seguro: false`; acento do estilo |
| `checklist` | camada | Checklist de vidro escuro, com ✓ no tempo da fala | `x` 0,76, `largura` 0,34–0,38, `y` 0,4; som do ✓ subir para 0,55 |
| `escala-ph` | camada | Régua com faixa normal, agulha e número contando | Generalizar em `escala` (mínimo, máximo, faixa e rótulos livres) |
| `fonte` | camada | Rodapé de fonte do dado | `x` 0,075, `y` 0,84, `tamanho` 28; ganhar som |
| `papel-rasgado` | camada sobre `tela` | Papel no acento profundo que rasga | 1× como quebra de modo |
| `marca-arroba`, `encerramento-insta` | camada | Ícone do Instagram + @; card final do Instagram | Reaproveitar o `IconeInstagram` na apresentação e na tela final. Não usar o @ fixo |
| Cena `fala` (`zoom`, `curva`, `foco`, `desfoque`, `escurecer`) | cena | Zoom contínuo, rosto desfocado | São estáticos: animar com `chaves` |
| Cena `tela` (`grade`, `escuro`, CSS) e `broll` | cena | Fundos e Ken Burns | Grade nova: 96 px, #222634, linhas pelo centro |
| `corte`, `flash`, `blur`, `zoom`, `lente` | transição | Com SFX automático | `flash` curto por estilo; `lente` com som a 0,35 |
| `recortes` + `plano: "atras"` + `recortar.mjs` | edição + camada | Texto atrás da pessoa | Orçamento de ≤ 10 s |
| `montagem` + `{pausa}`, `musica.fim`/`fade`/`quedas`, `sfxAuto` | edição | Trechos, pausas, trilha, SFX | `musica` em lista |
| `GraficoBarras` (Tela Dividida) | `Edicao.tsx` (congelado) | Barras com mola, contagem e selo | **Copiar** para `kit/pecas/`; não importar nem mexer no `Edicao.tsx` |
| `TesteKit` | `src/testes/TesteKit.tsx` | 3D, motion blur, ícones, curva, papel rasgado, texto atrás | Base de `texto-3d`, `objeto-3d` e `golpe` |

### A construir (em ordem de prioridade)
Depois de cada peça:
- prévia curta na vitrine (`src/testes/entrada-<peça>.tsx`, em 16:9);
- `node scripts/regressao.mjs` (precisa sair IDÊNTICO).

Mudanças em `tempo.ts` e `fontes.ts` não podem alterar o CUT aprovado: os tokens novos entram ao lado dos atuais.

| Prior. | Peça | Onde | O que faz | Como implementar no Remotion | Esf. |
|---|---|---|---|---|---|
| 1 | `estilo-mix` | `estilos.ts`, `kit/tempo.ts`, `kit/fontes.ts`, `MotorCamadas` | Paleta nova, grade, tokens, flash curto, ganho de SFX, serifa normal | No `Estilo`: campos `fundo`, `grade` {passo 96, cor, offset}, `gelo`, `cinza`, `papel`, `tinta`, `sobreAcento`, `trans.flash` [2, 8] e `ganhoSfx` (teto 1,0). `TOKENS` novos (desenho, risco, assento, chicote, ambiente) e `MOLAS` (smooth, snappy, bouncy), sem mexer em `DUR`. `loadInstrumentSerif('normal')`. Cor neutra no piloto | P |
| 1 | `chaves` | cena (`chaves: [{t, zoom?, foco?, desfoque?, escurecer?, curva?}]`) | Zoom, foco, desfoque e escurecer animados | Interpolar segmento a segmento com `CURVAS` dentro do `enquadrar()`, para pessoa e recorte continuarem alinhados, e no `escurecer`. Serve também ao CUT (`zoom-chaves`) | P |
| 1 | `musica` em lista | `tipos.ts` + `MotorCamadas` | Intro, corpo A e corpo B, cada um com `ini`, `fim`, `fade` e `vol` próprios | `musica: Musica \| Musica[]`; um `<Audio>` por trilha, com `from` na saída e a mesma envoltória de ducking | M |
| 1 | `microfade` | `MotorCamadas` (voz) | Fade de 1–2 q em cada junção da voz | `volume` por quadro no `<Audio>` de cada trecho | P |
| 1 | `enquadramento-auto` + `juncoes.mjs` | `resolverCenas` + script | Rodízio A/B1/B2/C nas junções; lista das junções internas do bruto | Regra entre vizinhas: Δescala ≥ 8% ou Δfoco x ≥ 0,08. Script: intervalos < 0,05 s no `palavras.json` × pico de diferença de quadro (`tblend=all_mode=difference` + `signalstats`), só em volta dos candidatos | M |
| 1 | `srt-saida.mjs` | script | SRT PT-BR no tempo da saída | Reaproveita `montarSegs` e `paraSaida`. Blocos de até 2 linhas × 42 caracteres, 1–6 s cada | P |
| 1 | `card-vidro` | camada | Card Apple em vidro claro (sobre imagem), escuro (sobre a parede) ou sólido: título, texto, ícone Lucide, número; reflexo diagonal | Entrada em 15–18 q (y +40→0, escala 0,96→1, blur 12→0, opacidade); filhos em cascata de 3–5 q; `backdropFilter` fixo; reflexo = `linear-gradient` de 135° animado em 18 q. Aproveita o card do `checklist` | M |
| 1 | `manchete-falada` | camada | Frase dita no topo à esquerda, com karaokê no acento | Palavras no tempo da saída (como a legenda): fantasma a 35% → acento letra a letra → creme quando a próxima começa | P |
| 1 | `titulo-quente` | camada | Digitação quente→frio, contorno fantasma, sublinhado, estouro e colapso para um ponto | Um span por letra. Cor com `interpolateColors` (acento → creme) e atraso por letra; `text-shadow` do glow decaindo; sublinhado em `scaleX` com `desenho`; colapso com `scaleY` 1→0,02 + `scaleX` 1→0 em 6–8 q (`saida`) | M |
| 1 | `ponto-luz` | camada | Ponto laranja com halo pulsando; cantoneiras de visor | Div de 6–8 px + `radial-gradient` de 60–120 px, `scale` em seno de 0,9 a 1,1 em 30 q. Opcional: sai como cometa (`desenho`) | P |
| 1 | `card-capitulo` | camada | "02" + título serifado; `{pausa}` opcional | `titulo` com 2 fontes + linha em `desenho`; entrada expo-out em 12 q, saída com blur em 7–9 q | P |
| 2 | `apresentacao-redes` | camada | Nome, credencial, ícones das redes, @ e contador opcional | 2–3 `card-vidro` empilhados à direita, cascata de 4 q. `simple-icons` com mola `snappy` (3 q entre ícones). Gradiente do IG com o `IconeInstagram` | M |
| 2 | `painel-tecnico` | camada | Painel com traço, cantoneiras, micro-rótulos, linhas digitadas no tempo da fala, conectores e valores tabulares; modo "NESTE VÍDEO 01/02/03" | DOM + SVG; `evolvePath` (@remotion/paths) nos conectores (10–14 q); linhas com `t` relativo à camada | M |
| 2 | `grafico-barras` | camada | Barras com mola sem overshoot, contagem, selo e som por barra | Copiar o `GraficoBarras` do Tela Dividida para `kit/pecas/`, adaptar para 16:9 e molas Apple, `sons` no registro | M |
| 2 | `grafico-linha` | camada | Linha desenhando com cabeça de glow e anéis no ponto final; eixo com rótulos | `@remotion/paths` (`evolvePath`, `getPointAtLength`) com `desenho` (16 q por segmento); anéis em 5–6 q | M |
| 2 | `contador` | camada | Número contando com `tabular-nums` e assento 1,04→1 | `interpolate` + `Intl.NumberFormat('pt-BR')`; modo caça-níquel por dígito | P |
| 2 | `chicote` | `transicao` | Saída em 3 q + entrada em 3–5 q, com blur direcional | `translateX` + filtro SVG `feGaussianBlur stdDeviation="N 0"` na cauda da cena anterior e na entrada, como a `lente` | M |
| 2 | `flash-foto` | camada | Fotos de 6–10 q com flash de 2 q, aberração em 4 q e Ken Burns; ≥ 12 q de rosto entre fotos | `<Img effects={[chromaticAberration({amount})]}>` (`--gl=angle`); flash = div branca a 60–80%; `fotos: [{t, arquivo}]` | M |
| 2 | `match-cut` | camada sobre `tela` | Text Match Cut de manchetes reais | Conta por quadro: escala `s = (altura·H/1080) / bh · Z(t)`; posição `left = ancoraX·W − (bx + bw/2)·s` e `top = ancoraY·H − (by + bh/2)·s`; hold com recuo até `caixaManchete`; `debug`; `sons` nos cartões de ≥ 4 q | M |
| 2 | `match-cut-tipo` | camada | Palavra por tela no acento, ou frases-tema com a palavra travada | 3 spans (`antes`, `palavra`, `depois`) + `measureText` (@remotion/layout-utils) para manter a palavra na âncora; `fontSize = maiúscula / 0,727` | M |
| 2 | `camera-tela` | cena `tela` (`zoom`, `pan`, `deriva`) + `camera: true` nas camadas | Câmera virtual nas telas gráficas | A mesma conta do `enquadrar()` aplicada ao contêiner da tela e das camadas presas | P |
| 2 | `dicionario` | camada | Palavra-entrada com sílabas que acendem, classe gramatical e definições numeradas | Instrument Serif normal + itálica; cor das sílabas por tempo | P |
| 2 | `checar-mix.mjs` | script | Checagens antes da prévia | Lê `edicao.json`, `palavras.json` e o `signalstats` da prévia | M |
| 2 | `render-partes` | `render.mjs` | Final por capítulo + junção sem recompressão | `--trecho` por capítulo; `ffmpeg -f concat -c copy` no vídeo; áudio renderizado inteiro à parte e mapeado com `-map`, para não estalar nas emendas | M |
| 3 | `golpe` | efeito sobre a cena | Preset de 3D flash (flash + punch + zoom-blur ou aberração), ≤ 20 q | `zoomBlur` / `chromaticAberration` no `<Video>` da pessoa via prop `efeitos` na cena; punch com `chaves` | M |
| 3 | `texto-3d` | camada (frente ou atrás) | Texto extrudado com rotação e voo | CSS 3D: 16–24 cópias com `translateZ(-i·k px)`, `preserve-3d`, `perspective: 1400px`, laterais em gradiente até #4A1A06; mola `snappy` | M |
| 3 | `objeto-3d` | camada | Objeto 3D passando rente à câmera ou orbitando atrás da cabeça | `ThreeCanvas` (@remotion/three), a partir do TesteKit, com `MeshPhysicalMaterial`; `CameraMotionBlur` só em ≤ 24 q | G |
| 3 | `diff` | camada | Linha "−" em cinza riscada sobre linha "+" no acento | DOM + risco com a curva `risco` (8 q) | P |
| 3 | `ficha-papel` | camada sobre `tela` | Papel creme com caneta vermelha tremida, carimbo, ☒ e ✓ | SVG com `noise2D` no traço; carimbo com escala 1,3→1 em 3 q e rotação de −5° | M |
| 3 | `mergulho` | `transicao` | Mergulho em ease-in num ponto-alvo, terminando no escuro | `scale` 1→6 com origem no alvo (`alvo: [x, y]`) em 10–12 q + escurecer | P |
| 3 | `encerramento-youtube` | camada sobre `tela` | Tela final: ponto de luz, @ e ícones à esquerda, metade direita livre, molduras-guia só na prévia | Reaproveita `IconeInstagram` e `ponto-luz`; parâmetro `guias: true` | P |
| 3 | `capturar-manchete.mjs` | script | Captura de manchete em Chrome headless (CDP) | WebSocket nativo do Node 24, `deviceScaleFactor: 2`, mesma função de caixa do caminho A | M |
| 3 | `esticao` | `transicao` | Esticão vertical de pixels em 3 q | `scaleY` 1→3 + blur vertical | P |