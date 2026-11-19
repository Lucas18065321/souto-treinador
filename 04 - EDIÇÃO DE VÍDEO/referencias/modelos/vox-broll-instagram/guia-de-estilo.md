# Guia de estilo: INSTAGRAM - VOX - B-ROLLs (`vox-broll-instagram`)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Status: **✅ fixo desde 2026-10-30** (como o CUT, o MIX e o PAPER VOX; **não** congelado). Id `vox-broll-instagram`, composição `VoxBroll`. No lab ele era o "formato 5" (antes "PAPER VOX B-ROLL").
- **Promovido a calibração original em 2026-10-30**, depois do 1º vídeo inteiro aprovado (creatina, 112 s: "Aprovado"), no mesmo molde do PAPER VOX (regra 1 do `05_LAB/CLAUDE.md`, exceção 3). A vitrine de 20 s foi aprovada em 2026-10-29.
- Formato, estilo e guia só mudam a calibração original. Mudança no motor passa nas 6 regressões (ver "Checagens antes da prévia e do final").
- **Ordem de precedência:** "Decisões de edição" prevalece sobre tudo; depois as "Escolhas do Jorge" e o que o piloto firmou; depois o resto do guia.
- **O código é a fonte de verdade do comportamento:** `motor/src/modelos/vox/*.ts*` (composição), `scripts/lib/vox.mjs` e `scripts/lib/vox-mural.mjs` (geradores), `scripts/validar-vox.mjs` (trava) e `scripts/render-vox.mjs` (render). Se o guia divergir, vale o código e o guia se corrige.
- **Piloto e molde do gerador:** `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino` (gerador `03_roteiro/montar_creatina.mjs` → `vox.json` + `plano-de-batidas.md`; final em `07_final/`). É também a base da regressão (`regressao-vox.mjs`).
- Nasceu como o guia v2 do lab (2026-10-28, revisado em 2026-10-29 por 3 críticas: fidelidade, viabilidade, regras), que substituiu a v1 (2026-10-19, guardada no GitHub privado). O material de apoio continua na pasta do lab, `05_LAB/formatos/5-paper-vox-broll/`: as 7 perguntas, com a escolha dele no campo `decisao`, em `perguntas.json` (folhas em `perguntas/q1…q7`); sugestão de montagem em `sugestao-montagem.jpg` (1 quadro de referência por bloco, com o tempo do vídeo de 60 s; anterior às escolhas, ver "Estrutura"); storyboard do mural (mergulho) em `storyboard-mural.jpg`; a vitrine e a referência da legenda com a interface do Reels em `previas/`. As análises das refs ficam em `05_LAB/referencias/`.
- Onde este texto diz "(proposta)", a regra não veio de referência nem de pedido dele: vale como padrão até ele pedir outra coisa. Onde diz "vitrine" ou "1º teste", é o que se mediu no lab (vitrine de 2026-10-29; creatina, o piloto, em 2026-10-30).

**De onde vem cada regra** (entre parênteses):
- `ref-NN`: `05_LAB/referencias/analises/ref-NN/analise.md`; `ref-08 mov` = `ref-08/analise-movimento-2026-10-28.md`. A **ref-09 é a referência principal**; a ref-08 é o modelo de movimento; ref-01…07 ficam nas receitas.
- `TD2`: INSTAGRAM - TELA DIVIDIDA (`referencias/modelos/tela-dividida-2-instagram/guia-de-estilo.md` e `motor/src/modelos/tela-dividida-2/`).
- `PAPER VOX`: INSTAGRAM - PAPER VOX ANIMATION (guia oficial e `src/modelos/paper-vox/`).
- `CUT`: guia do CUT DINÂMICO (só a palavra atrás da cabeça e os recortes de objeto).
- `Decisões AAAA-MM-DD`: `04 - EDIÇÃO DE VÍDEO/Decisões de edição.md`. **Valem acima deste guia.**
- `Jorge, 2026-10-29`: as respostas dele às folhas `perguntas/q1…q6` (ver "Escolhas do Jorge"). Também estão nas Decisões.
- `área segura`: medição da interface do Reels conferida em 2026-10-29 (2 imagens oficiais medidas pixel a pixel + guia de anúncios da Meta). Para Reels orgânico não existe número oficial.
- `gbro`, `lemo`: repositórios lidos em 2026-10-28 pelo `gh api`, sem clonar nem instalar (ver "Kit › gbro e lemo").
- `v1`: regra da v1 que continua valendo.
- **proposta**: não está em nenhuma fonte. Tempo e custo medidos: "Kit de peças".

## O que mudou da v1
| v1 (2026-10-19) | v2 (2026-10-28) |
|---|---|
| Nome PAPER VOX B-ROLL | **VOX - B-ROLLs** (Decisões 2026-10-28) |
| ref-01…08 com o mesmo peso | **ref-09 principal**; ref-08 para o movimento (medido em 2026-10-28) |
| Molde: TELA DIVIDIDA clássico (`Edicao.tsx`, congelado) | Molde: **TD2** (split, trocas, rosto) + **PAPER VOX** (palco, câmera, peças, mergulho), copiados para `src/modelos/vox/`; legenda pequena da ref-09 (calibração original, 2026-10-29) |
| Layouts por % (split 60, fala 25, card 10, texto 5) | **Espinha fixa do Jorge** (8 blocos), com linha do tempo para 45, 60 e 75 s |
| "100% dark" como regra | **Look C, foto-colagem com luz real** (decidido: Jorge 2026-10-28, ref-09) |
| 1 evento a cada 0,5–1,5 s | **Piso medido**: rajada de ≥ 7 peças no 1º segundo em tela cheia (≥ 5 no painel do split), entrada mediana ≤ 0,30 s, sem overshoot, ≥ 0,54 troca por segundo |
| Texto fora de "x > 86%, y 55–90%" e dos 10% do topo | **Faixa segura medida**: y 240–1500; x 90–850 (ou 90–990 acima de y 1000) |
| Layouts `texto` e `grafico` | Saem como layout: o número vira peça da animação (R8, R14) |
| Variante P2 (faixa) e P2a | Vira o layout `moldura`, com a geometria medida na ref-08 e a cabeça vazando (decidida pelo print dele); entra entre o mural e o split 2, com cards de contexto que se sobrepõem (calibração original, 2026-10-29) |
| 8 perguntas (Seedance, acento amarelo, emenda, P2b, quadriculado, card, densidade, bordô) | Seedance decidido; acento = azul elétrico (marca); look, cabeça vazando e emenda esfumada decididos (2026-10-29); as 7 que ficaram (split, abertura, mural, lugar da moldura, stills, legenda e bruto do teste) foram respondidas em 2026-10-29 (ver "Escolhas do Jorge") |

**Fica da v1:** composição própria (nasceu em `src/lab`; desde 2026-10-30 em `src/modelos/vox/`), sem tocar no TD2 nem no PAPER VOX; carry com trava; sincronia de 0–2 q antes da palavra medida; 1 acento azul elétrico com a regra de contraste; texto nunca dentro da imagem; ordem de origem das imagens; ética do CFN; receitas R1–R8 (adaptadas); SFX "pestana"; regras de música.

## Formato
- 1080×1920, 24 fps (TD2, PAPER VOX). Tempos em segundos do bruto já decupado: saída = bruto (TD2).
- Entrada: bruto de vídeo do Jorge falando. Pergunta da etapa 0: "É para decupar, corrigir cor e ajustar o áudio?" (Decisões 2026-10-11).
- Cor do bruto intocável: `"cor": {"contraste": 1, "saturacao": 1, "calor": 0}` (Decisões 2026-10-09). Sem grão e sem vinheta sobre o rosto (v1).
- Motor 100% Remotion. HyperFrames só no recorte da pessoa, pelo `scripts/recortar.mjs` (Decisões 2026-10-28).
- Composição `VoxBroll` em `motor/src/modelos/vox/` (os tipos ficam no módulo, `tipos.ts`), registrada no `src/Root.tsx` com a linha `vox-broll-instagram` do `src/modelos.json` (`gl: null`); props em `03_roteiro/vox.json`, nunca `edicao.json` (o hook validaria contra outro motor; PAPER VOX). O gerador grava `"modelo": "vox-broll-instagram"` (`gravar` do `lib/vox.mjs`) e o `render-vox.mjs` recusa outro. Projeto em `%SOUTO_VIDEO_PROJETOS%/<AAAA-MM-DD>_<slug>/` (`novo-projeto.mjs`). Bruto que não vier em 1080×1920 a 24 fps ganha o **bruto de trabalho em 1080×1920, H.264, quadro-chave a cada 1 s** (TD2; ver Pipeline, etapa 0) (proposta). O do piloto (creatina corrigida) já veio no formato de saída: ver "Bruto do 1º teste", no Pipeline.
- Render **sem `--gl=angle` e com `--concurrency 1`**, os padrões do vídeo aprovado (`render-vox.mjs`; 5,6 s/s no piloto): no TD2, com o angle, os `<Video>` de B-roll do `@remotion/media` dentro de `Sequence` estouram o tempo (o rosto é um `<Video>` só, fora de `Sequence`; `TelaDividida2.tsx` l. 12 e 327). As comparações com `--gl angle` e com `--concurrency 2` não foram medidas (pendentes; até lá, vale o padrão). Efeito WebGL (zoom-blur, aberração, glow) fica fora ou vira clipe pré-renderizado (proposta).
- **Memória** (7,7 GB; em 2026-10-29 havia 0,6 GB livres): antes de Flow, recorte ou render, ≥ 2 GB livres (`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory`), CapCut e o Chrome do Flow fechados quando não estiverem em uso e nenhuma outra sessão rodando Whisper. O final do piloto rodou com ~1,3 GB livres, com concurrency 1, depois de o Jorge liberar o fechamento de OneDrive, WhatsApp, Vincular ao Celular e Widgets (reabertos no fim). Cada still no tamanho em que aparece (2K só onde o zoom passa de 1,5×) (proposta).
- Cadência: peças de colagem a 12 fps (passo 2), traço à mão a 8 fps (passo 3), rosto, legenda e pós a 24 fps; sem tremor de posição, o "stop-motion" é o passo (ref-09 §10, ref-08 mov §5, PAPER VOX). Câmera da animação: **24 fps com motion blur** (PAPER VOX), a do vídeo aprovado; a comparação com 12 fps (as refs) não foi medida e segue pendente.

## Estrutura do vídeo (calibração original, 2026-10-28)
### A espinha (ordem fixa)
| # | Bloco | Layout | O que se vê |
|---|---|---|---|
| 1 | Abertura | `abertura` | Rosto dele com texto grande e dinâmico acompanhando a fala (~2 s): texto digitado fora do rosto + cartão azul elétrico (calibração original, 2026-10-29) |
| 2 | Invasão | `invasao` | Colagens inundam a tela e ele sai; exemplificam a fala, com texto cinético |
| 3 | Split 1 | `split` | Animação que exemplifica a fala por analogia, em cima, uma por vez (calibração original, 2026-10-29); ele embaixo |
| 4 | Só ele | `ele` | Ele em tela cheia |
| 5 | Mural | `mural` | Nova invasão que vira câmera contínua: segue sem corte até outra cena, que nasce dentro de uma parte da anterior, e mergulha nela (calibração original, 2026-10-29), com um resquício da anterior no canto |
| 6 | Moldura | `moldura` | Ele "meio cortado no cenário", embaixo, com a animação rolando atrás e cards de contexto que podem se sobrepor (calibração original, 2026-10-29) |
| 7 | Split 2 | `split` | Animação na proporção certa de B-roll, uma por vez |
| 8 | Fecho | `ele` | Só ele até o fim |

- Blocos 1–5, 7 e 8 e a moldura: Decisões 2026-10-28. **Lugar da moldura: entre o mural e o split 2** (calibração original, 2026-10-29; ele a tinha pedido "além da tela dividida", sem posição): a cena do mural segue atrás dele, como o Capitólio atrás do cartão na ref-08, 36,5 s.
- Sugestão de montagem em quadros: `sugestao-montagem.jpg` (1 quadro de referência por bloco). É anterior às escolhas de 2026-10-29: a palavra atrás da cabeça do quadro 1 e a legenda grande do TD2 nos quadros 4, 7 e 8 não valem mais (abertura e legenda: ver "Escolhas do Jorge").

### Linha do tempo (proposta)
| Bloco | 45 s | 60 s | 75 s |
|---|---|---|---|
| Abertura | 0–2,0 | 0–2,5 | 0–2,5 |
| Invasão | 2,0–8,0 | 2,5–10,5 | 2,5–11,5 |
| Split 1 | 8,0–15,0 | 10,5–21,5 | 11,5–23,5 |
| Só ele | 15,0–19,0 | 21,5–26,5 | 23,5–28,5 |
| Mural | 19,0–28,0 | 26,5–38,5 | 28,5–42,5 |
| Moldura | 28,0–32,0 | 38,5–44,5 | 42,5–49,5 |
| Split 2 | 32,0–39,5 | 44,5–54,0 | 49,5–59,5 |
| Só ele (virada) | — | — | 59,5–63,5 |
| Split 3 (curto) | — | — | 63,5–69,5 |
| Fecho | 39,5–45,0 | 54,0–60,0 | 69,5–75,0 |
| **% por layout** | ele 25,6 · tela cheia 33,3 · split 32,2 · moldura 8,9 | ele 22,5 · tela cheia 33,3 · split 34,2 · moldura 10,0 | ele 22,7 · tela cheia 30,7 · split 37,3 · moldura 9,3 |

- Na ref-09: 38% de animação em tela cheia, 35% de split, 27% só a pessoa (ref-09 §1). Aqui a animação fica na tela 74–78% do tempo (tela cheia + split + moldura); na ref-09, 73%.
- Acima de 60 s, o par `ele → split` extra antes do fecho (o "só ele (virada)" e o "split 3" da coluna de 75 s) é **opção marcada no plano de batidas** (⏸), não regra: não está na visão dele. Abaixo de 45 s, a moldura encolhe para 3–4 s; tirar só com ok dele (proposta).
- **Acima de 75 s: 2 atos** (padrão desde o piloto, aprovado pelo Jorge em 2026-10-30; vale até ele pedir outro desenho). A espinha soma no máximo ~90 s, contando o par extra e uma 2ª moldura:
  - **ato 1** = a espinha inteira, até o 2º split;
  - **ato 2** = pares `ele → split`, com a 2ª moldura (no máximo 2 molduras e 10 s no total) e um 2º mural quando a fala pedir (uma história que se desdobra), até o fecho. Na creatina (112,3 s): ato 1 até 44,8 s; ato 2 = `ele → split → moldura ("Obs.") → mural → split → ele → split → ele → split → fecho`, 17 blocos no total, 2 um pouco fora da faixa (um `ele` de 6,4 s e um split de 6,3 s). Registro: `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/03_roteiro/plano-de-batidas.md`;
  - o `validar-vox.mjs` aceita o ato 2 acima de 75 s (e só o par extra `ele → split` entre 60 e 75 s); outro desenho (só pares, blocos mais longos) é pergunta para ele no plano de batidas.
- A espinha troca de layout a cada 5,6–7,5 s; a ref-09, a cada 4,2 s. O que falta vem das trocas internas, com mínimo por bloco: invasão com ≥ 3 planos ou chegadas de câmera; split com troca a cada ≤ 2 s; mural com ≥ 4 estações; `ele` e `fecho` com punch por corte seco a cada ≤ 2,5 s. Meta: **≥ 0,54 troca por segundo** no vídeo, na régua do §7 da ref-09 (ver "Especificação de movimento").

### Como a fala vira batidas
1. **Frases:** `palavras.json` alinhado + pontuação do roteiro. Cada frase ganha uma função (proposta):

   | Função da frase | Bloco que ela puxa |
   |---|---|
   | gancho (1ª frase) | `abertura` |
   | 1º exemplo concreto, imagem forte | `invasao` |
   | mecanismo, analogia do roteiro | `split` |
   | virada, pergunta, opinião, frase curta e seca | `ele` |
   | ideia que se desdobra em 2–4 detalhes | `mural` (1 detalhe = 1 estação) |
   | dado, número, estudo | `moldura` (cartão que cai + cards de contexto) ou peça dentro do `split` |
   | CTA, encerramento | `fecho` |

2. **Blocos:** a ordem é a da espinha. A fala decide onde cada bloco começa: no fim de frase mais perto do tempo-alvo (± 30% da duração do bloco), preferindo a frase cuja função casa com o bloco (proposta).
3. **Gatilhos:**

   | Troca | Quando | Fonte |
   |---|---|---|
   | Layout | no fim de frase (pausa ≥ 0,12 s ou pontuação), nunca no meio de palavra; a cena nova já tem imagem 0,1–0,15 s antes do corte, nada nasce do preto | TD2; lemo |
   | Animação nova no bloco | a cada ideia nova (sujeito novo), na 1ª palavra-chave dela | v1 (ref-05, ref-07) |
   | Peça nova na animação | em cada palavra-chave (substantivo concreto, verbo de ação, número), na ordem de montagem | v1 (ref-04); gbro |
   | Foco no mural | na palavra que nomeia o detalhe novo | proposta |
   | Corte para `ele` | na frase de virada; a legenda muda de lugar no mesmo quadro | Decisões 2026-10-27 |
   | SFX | no instante visual, pelo ponto medido do som | Decisões 2026-10-20 |

4. **Sincronia:** toda entrada cai de 0 a 2 q ANTES do início medido da palavra; o início real se mede por energia do áudio na janela da palavra (v1; ref-05).
5. **Carry com trava** (v1, 2026-10-19): a mesma animação dura 2–3 frases só dentro da mesma ideia e só se evoluir na tela (peça nova, câmera num detalhe, recorte novo). Ideia nova = animação nova.

## Layouts
Medidas em px de 1080×1920. "q" = quadro a 24 fps (41,7 ms), salvo indicação.

### `abertura` · rosto + texto digitado + cartão (calibração original, 2026-10-29)
- **Escolha:** texto digitado fora do rosto + cartão azul elétrico, como o "LOOK AT THIS" + "Vox" da ref-09 (pergunta 2 = B). **Sem recorte da pessoa e sem palavra atrás da cabeça** (essa segue obrigatória só no CUT).
- **Geometria:** rosto em tela cheia, no enquadramento do `ele` (abaixo): centralizado, cabeça inteira (Decisões 2026-10-22). Texto e cartão **nunca sobre o rosto**, na faixa do texto grande (área segura): y 240–1000 em x 90–990, ou até y 1500 em x 90–850. Na ref-09 o texto fica em x 16–60%, y 43–53%, mas sobre a animação: com o rosto dele no centro, essa posição cairia na boca e no queixo. Aqui, texto acima da cabeça e cartão no peito (ou o contrário, se a frase pedir), medidos pela cabeça do quadro; no bruto da creatina corrigido, o topo da cabeça fica perto de y 600 e o queixo perto de 950 no quadro inteiro (estimado pela folha de quadros; medir) (proposta).
  - **texto:** Instrument Serif em caixa alta, creme #F2F4F8, 1–2 linhas, maiúscula de ~86 px (4,5% da altura; ref-09 §5.1);
  - **cartão:** azul elétrico #2E49CE (o acento da cena), com a palavra-chave do gancho em branco (Decisões 2026-10-20: branco só sobre o azul elétrico); nunca o @ nem logo (o @ só no card final; Decisões 2026-10-08). Na ref-09: 57% × 18% da tela (616 × 346 px), inclinado ≈ −3°, com risco de brilho no canto e a borda direita em x 93%. Aqui: x 90–850 quando passa de y 1000 (até 760 px de largura), e encolhe até caber entre o queixo e y 1500 (área segura).
- **Entra:** o 1º quadro já tem o rosto; o 1º texto aparece até 0,15 s (lemo; ref-09: texto em 0,10 s). Digitação de 2–3 letras por passo (10 letras em 0,23 s; ref-09 §5.1), terminando 0,1 s antes de a palavra acabar de ser dita. Cartão que abre como aba em 0,17 s, girando na própria borda, e a palavra que acende em 0,20 s **na** palavra falada (ref-09 §5.1: texto 0,10 → cartão 0,33 → logo 0,57 s). As palavras seguintes vêm em pedaços de 2–3: **cada pedaço entra 0–2 q antes da 1ª palavra dele**; os 0,12 s são a cascata entre as palavras dentro do pedaço (lemo). O texto acompanha a fala, nunca corre na frente. Deriva até a saída: o texto cresce ~10% e o cartão ~2% (ref-09).
- **Rosto:** push contínuo de +6–8% em 2 s (expo-out, cabeça sempre inteira) ou punch de 1,0 para 1,15 por corte seco na 2ª frase (ref-09: push contínuo de ~2,7× na abertura, com 2ª arrancada em 1,8 s) (proposta).
- **Sem legenda** enquanto o texto e o cartão dizem as mesmas palavras (ref-09 §5.1: ela volta em 1,9 s).
- **Sai:** a invasão come a tela por cima dele (`invasao`), mas texto e cartão saem juntos antes (dissolve + desfoque de 0,20 s; ref-09 1,80–2,00 s) de a 1ª peça chegar neles: imagem nunca passa por cima de texto (Decisões 2026-10-20).
- **Duração:** 1,5–2,5 s (Decisões 2026-10-28). **Piso:** ≥ 3 eventos de texto ou cartão no 1º 1,0 s (o 1º até 0,15 s) e ≥ 7 eventos nos 3 primeiros segundos, contando a invasão (ref-09: ~7 em 2 s: texto 0,10, cartão 0,33, luminária 0,40, logo 0,57, 2º push e dissolve 1,8, legenda 1,9; ref-08: mais de 9 em 3 s).
- **Código:** rosto e punch do `TelaDividida2.tsx` (copiar). Texto digitado e cartão: peças novas, `TextoDigitado` (a digitação do `TextoNaCena`, fora do palco) e `CartaoAba` (ver "Kit"). Nada do `recortar.mjs` nesta cena: o leitor da sequência WebP fica na `moldura`.

### `invasao` · colagem toma a tela (ele sai)
- **Geometria:** palco de tela cheia. Sujeito em y 240–1040 quando a legenda está embaixo (1150–1420); até y 1500 (x 90–850) só com a legenda em 960 e a faixa 920–1000 livre. Faixa da legenda livre (ver "Legenda").
- **Entra** (uma por vez; nunca a mesma em duas invasões seguidas; proposta):
  1. **papel invade:** manchas de papel amassado nascem nas bordas e comem a tela em 0,10 s (25% → 70% → 100%) e estouram para o claro em mais 0,10 s; da pessoa à cena montada, ~1,2 s (ref-08 mov §1.1);
  2. **monta do vazio:** corte seco para o cenário vazio, ~0,1 s parado, e as peças voam das bordas e travam: S curto, 50% em ~0,2 s, 90% em ~0,4 s, assenta em ~0,5 s (ref-08 mov §4, Pisa);
  3. **cenário pronto:** corte seco para o cenário já com etiqueta e fita; as peças entram por cima (ref-09 15,18 s, garagem);
  4. **peças cobrem:** 6–10 recortes voam das bordas por cima dele, em cascata de 0,05–0,1 s, cobrem a tela em ~0,4 s e o último vira o fundo da cena (proposta);
  5. **faixas** (abaixo).
- **Monta:** rajada de **≥ 7 peças novas no 1º 1,0 s** (ref-09: de 5 peças em 0,7 s a 12 em 1,6 s, ~7/s; Pisa 16/s por 0,5 s), na ordem base → sujeito ou cartões → conectores (seta, fita, fio) → ação → resultado, cada passo numa palavra-chave (gbro). Quadro composto com ≥ 10 elementos (ver "Ficha da animação"). Texto do tema digitado dentro da cena (ref-09).
- **Depois:** câmera sempre andando (push de 1,3–2,7× em 2–3 s, mergulho de ~0,7 s, recuo ×0,3 em ~1,4 s ou travelling com o 1º plano cruzando; ref-09 §10; ref-08 mov §2) **e** 1 peça nova ou ação de objeto a cada 0,15–0,7 s até a saída (Capitólio ~2,8/s; Pisa, a cada 4–20 q depois da montagem), com 1 movimento em laço sempre ligado: pêndulo, onda, gesto (ref-08 mov §1.3). A ref-09 deixa só a câmera trabalhar; o Capitólio, que o Jorge apontou como a tela cheia, não: vale o mais rápido.
  - 1 vez por bloco de tela cheia: **peça gigante invade pelo 1º plano** e cobre ~70% em 0,17 s, e **o fundo escurece −50% em 0,4 s** para o número ou rótulo entrar (pombo + contador do Capitólio; ref-08 mov §2). O 1º plano que cruza passa por baixo do texto da cena e da legenda, ou só cruza com a tela sem texto (Decisões 2026-10-20).
  - ≥ 1 texto cinético por plano, preso ao mundo, na palavra-chave falada.
- **Sai:** corte seco (ref-09); empurra ×1,8 acelerando em 0,4 s + estouro claro em 0,2 s (ref-08 mov §2); desmonta pelo mesmo caminho em ease-in, 2× mais rápido (ref-08 mov §4); encolhe num ícone em 0,33 s (ref-08 mov §1.4); ou o split sobe (`split`).
- **Duração:** 6–9 s, com ≥ 3 planos ou chegadas de câmera: planos de 1,5–3 s, ou 1 plano contínuo de até 4,5 s com a câmera sempre andando e ≥ 2,8 peças novas/s (Capitólio: 4,33 s; ref-09: plano médio de 2,4 s).
- **A sequência que o Jorge apontou na ref-08:** 3 faixas (0,8–5,1 s) → encolhem num ícone → cena em tela cheia com a câmera sempre andando (Capitólio, 5,1–9,4 s).
- **Variante `faixas`** (ref-08 mov §1.2–1.4):
  - 3 faixas na largura toda, emendas retas em y 624 e 1254 (alturas 624, 630 e 666), sem borda, vão nem sombra; still 16:9 ampliado 3–10%, laterais cortadas;
  - entram do claro em cascata, de cima para baixo, com 0,13–0,17 s entre elas; cada uma em ~0,6 s, subindo 50 px (2,6%) em easeOutQuad, sem overshoot;
  - cada faixa é um clipe com relógio próprio (na ref: 12, ~24 e ~30 fps; aqui, num vídeo de 24 fps: 8, 12 e 24 fps = passo 3, 2 e 1 do `tempoPasso`), câmera travada ou 1 pan de ~0,5 s; ~4,5 entradas/s somadas; 3–6 coisas se mexendo;
  - saem juntas encolhendo num ícone em 0,33 s (expo-out, 50% em 2 q a 30 fps), com âncora no ícone;
  - nada importante em y < 240 (faixa 1) nem em y > 1500 (faixa 3): o sujeito da faixa 3 fica na metade de cima dela (still 16:9 composto com o sujeito no alto); legenda centrada na emenda 2/3 (y 1254, até 620 px); texto da faixa 3 só em y 1290–1500 (área segura);
  - só em tela cheia: no split, uma animação por vez (calibração original, 2026-10-29);
  - emendas mantidas nas da ref-08 (624 e 1254): em 660 e 1080, as faixas teriam 660, 420 e 840 px, e o still 16:9 (607 px de altura) precisaria de ~38% de zoom na faixa 3;
  - uso: lista de 3, "3 exemplos" (proposta).
- **Código:** palco do PAPER VOX (copiar `Mundo` e `BlurMovimento` de `PaperVox.tsx`, `camera.ts` sem o `snap`, `elementos.tsx`, `texturas.ts`), `voa` + `boiar` (copiar). Novas: `PapelInvade`, `MontaDesmonta`, `FaixasEmpilhadas`, `EncolheEmIcone`, `EmpurraEstoura`.

### `split` · tela dividida com animação
- **Geometria:** animação em cima, 1080×960 (9:8, a proporção da ref-09: 720×640); ele embaixo, 1080×960 (TD2). Emenda em y 960: **esfumada, a do TD2** (decidida: Decisões 2026-10-27, "fica estiloso"; o rosto sobe 230 px e o B-roll desce 190 px), a do vídeo aprovado. A reta da ref-09 não foi comparada lado a lado (pendente).
- **A animação é feita para o painel**, não uma tela cheia espremida (Jorge: "com as proporções certas para caber como B-roll"): palco de 1080×960, still 1:1, sujeito em x 162–918 e y 240–900 do painel (o topo 0–240 fica sob as abas "Reels | Amigos"; imagem sem texto pode subir até 144) e a faixa y 920–960 do painel livre para a legenda pequena, que fica na emenda (área segura; proposta).
- **Rosto embaixo:** no split do TD2, o rosto fica sob a faixa de baixo do Reels (final do TD2, 20,0 e 96,6 s: olhos em ~1460–1490, boca em ~1650–1680, queixo em ~1750; a linha social, 1531–1676, cobre nariz e boca, e o @/Seguir cobre o queixo). É imagem, não texto, mas o split ocupa ~1/3 do vídeo: medir o queixo e mostrar na vitrine 1 quadro com a interface do Reels por cima; o Jorge decide se o rosto sobe, sem cortar a cabeça (área segura).
- **Entra:** vindo da invasão, o painel dele **sobe de baixo** (30% do curso em 0,1 s, 56% em 0,2, 86% em 0,4, 96% em 0,6, assenta em 0,8 s; ease-out sem quique) enquanto a cena de cima encolhe ~20% e é recortada em 9:8 (ref-09 8,00 s). A cena herdada fica **≤ 1,0 s** no painel: a 1ª animação própria do split (still 1:1) entra por chicote ou troca de camada na 1ª palavra-chave da 1ª frase do split (ele pediu "a próxima animação"). Vindo de `ele`: corte seco (ref-09) ou a entrada de layout do TD2 (desfoque + zoom, nunca opacidade).
- **Uma animação por vez** (calibração original, 2026-10-29; pergunta 1 = A), trocando a cada ≤ 2 s por chicote ou troca de camada, no ritmo das 3 telas da ref-08 somadas (abaixo).
- **Trocas dentro do painel** (só a metade de cima troca, o rosto segue; TD2):
  - chicote horizontal de 0,30–0,33 s, com 2–3 q da cena velha sobrando na borda (ref-09 10,73 s);
  - troca de camada: o sujeito fica e o fundo troca (cortina de 0,4 s), ou o fundo fica e o sujeito troca (sai em 0,2 s, entra em 0,3 s) (ref-09 4,2 e 6,6 s);
  - painéis de papel que se abrem em 0,4 s, com o sujeito parado (ref-09 22,4 s);
  - cortina diagonal 0,4 s, zoom 0,36 s, blur 0,32 s (TD2);
  - nunca a mesma troca em seguida (TD2).
- **Ritmo do painel** (= as 3 faixas da ref-08 **somadas**, que o Jorge apontou como a fluidez da tela dividida: Decisões 2026-10-28; ref-08 mov §1.3): ≥ 4,5 entradas/s nos 2 primeiros segundos de cada animação e ≥ 3/s de média; ≥ 2 relógios no painel (colagem a 12 fps + laço ou peça a 24); 3–6 coisas mexendo; corte interno ou troca a cada ≤ 2 s (ref-09: 1,1–2,7 s); 1 movimento em laço sempre ligado; câmera travada com 1 pan curto, ou push lento; ≥ 7 elementos no quadro composto do painel. **Trava:** ERRO abaixo de 3 entradas/s de média ou de 5 no 1º segundo de cada animação.
- **Variante 60/40** (ref-09 41,34 s): animação de y 0 a 1160, ele de 1160 a 1920, quando a animação pede altura. Legenda na emenda (centro ~1160), até 620 px. Só se o queixo ficar ≤ 1500 sem cortar a cabeça; senão, não usar (proposta).
- **Sem faixas no painel** (calibração original, 2026-10-29): as 2 faixas de 1080×480 empilhadas ficaram de fora. Lista ou comparação no split se faz por trocas seguidas (chicote, R10); as 3 faixas seguem só em tela cheia (variante `faixas` da `invasao`).
- **Sai:** corte seco para `ele` (ref-09); o painel dele desce e a câmera abre a mesma cena em tela cheia, sem corte (v1; exige still 9:16); ou a célula vira tela cheia em 0,42 s com flash quente (lemo).
- **Duração:** 7–12 s, com 3–5 animações e troca a cada ≤ 2 s. O corte rápido para `ele` (1,3–2 s) dentro de split > 8 s é **opção marcada no plano de batidas** (⏸), não regra (ref-09: trechos só da pessoa a partir de 1,3 s).
- **Código:** `TelaDividida2.tsx` (copiar: o `<Video>` único do rosto com enquadramento por layout, `entra`/`sai`, `entraQuadro`, `mascaraEmenda`, o arredondamento `q()` das cenas); `SplitCompostoTD2.tsx` (copiar o `Recorte` que voa e boia); palco do PAPER VOX num retângulo de 1080×960. Nova: `SplitSobe`.

### `ele` · só ele
- **Geometria:** rosto em tela cheia, centralizado, cabeça inteira (Decisões 2026-10-22), **queixo em y ≤ 1410 no enquadramento base** (a legenda pequena fica em queixo + 50 px, com teto 1460; com a LegendaB, o limite era 1208). Punch 1,0 ↔ 1,15 por corte seco, com origem na altura do queixo, para o queixo não descer no punch (TD2; ref-09: punch-out de 1,15 para 1,0 em 20,85 s). No piloto do TD2 (gravado em casa), o queixo fica em ~1250 com 1,0 e em ~1400 com 1,15 (117,6 e 137,0 s): cabe sem subir, e o punch com origem no queixo o segura em ~1250. No estúdio de gravação original (bruto da creatina corrigido), o queixo fica perto de y 950 no quadro inteiro (estimado pela folha de quadros; medir na vitrine, com 1 quadro e a legenda por cima) (área segura; proposta).
- **Entra e sai:** corte seco (ref-09) ou as trocas de layout do TD2, sem opacidade.
- **Duração:** 1,3–6 s (ref-09: 1,3–3,6 s), com punch por corte seco a cada ≤ 2,5 s (proposta, para fechar as trocas por segundo).
- **Densidade:** até 1 ícone no peito por bloco, entrando e saindo em 4–5 q com varredura, 0,6 s no total, na palavra que o nomeia (ref-09 §5.4), sempre fora do bloco da legenda (centro ± 60 px; Decisões 2026-10-22: recorte nunca sobre a legenda).
- **Legenda:** a pequena, abaixo do queixo: centro = queixo medido + 50 px, teto y 1460 (ver "Legenda").
- **Código:** layout `fala` do `TelaDividida2.tsx` (copiar).

### `mural` · invasão + câmera contínua + mergulho com resquício
- **O que é:** nova invasão (entradas do `invasao`); a cena A se monta; a câmera viaja sem corte pelo mesmo mundo e dá zoom na parte de A onde a cena B se compõe; um pedaço de A fica no canto: "a câmera apenas mudou de foco" (Decisões 2026-10-28). **A cena B nasce dentro de uma parte de A, e a câmera mergulha nela** (calibração original, 2026-10-29; pergunta 3 = A). Storyboard: `storyboard-mural.jpg`; na folha `perguntas/q3_mural.jpg`, a câmera entrando no celular do PAPER VOX (28,6 s).
- **Como** (nenhuma ref mostra a cena B se compondo com A no canto: é peça nova):
  - B mora numa parte de A (janela, tela, quadro na parede, porta) em escala k = 0,35–0,5, como a estação-filha do PAPER VOX (E12 dentro do celular da E11, k 0,42: as peças saem × k e a câmera chega com zoom de até 1/k; guia do PAPER VOX). Cada estação nova mora dentro de uma parte da anterior.
  - O hospedeiro de B (a parte de A onde B mora: janela, tela, porta) fica **ao lado** do objeto-chave de A, dentro de A, nunca nele. A câmera para em **0,8–0,9/k, não 1/k**: com o zoom cheio, o hospedeiro enche o quadro e A some (PAPER VOX 29,6 s, quadro 3 do storyboard). Ela fica deslocada para o objeto-chave de A ocupar 10–25% do quadro num **canto de cima**, com 15–40% dele fora da borda (o canto de baixo fica sob a legenda e os botões), e B se compõe centrado no resto. Os laços de A seguem rodando enquanto B se monta.
  - **Resquício = só imagem, sem texto.** O texto de A sai (dissolve + desfoque de 0,20 s) antes de A virar resquício: imagem pode ficar cortada na borda, texto nunca (Decisões 2026-10-28: nenhum texto sai da tela; os cantos são área morta). Escurece 20–30% enquanto B está em foco (rack focus); o desfoque de 8–12 px vem da cópia pré-desfocada do still (ver "Kit", plano B) ou por quadro, se a vitrine aguentar. Nunca cobre a legenda nem o sujeito de B. ERRO no `validar-vox` para texto dentro do resquício. No print da escolha (PAPER VOX 28,6 s), o "horas" fica desfocado e cortado no canto: aqui, não.
  - Na ref: o mergulho da garagem deixa a etiqueta e a mão cortadas na borda por ~0,3 s (ref-09 16,6–17,3 s); o 1º plano que cruza dá a profundidade (ref-08 mov §2).
  - O desfoque esconde a perda de resolução de A ampliada. Sem desfoque, still ampliado até 1,25–1,5× (v1; lemo). Mergulho mais fundo numa foto: o nível fino sai da MESMA imagem (ampliação ou geração no Flow com ela de referência, que pede o upload por interceptação do input), alinhado ao grosso; still novo da mesma região não casa (lemo). O nível fino é still a mais: entra na conta de stills do plano (sem teto; Jorge, 2026-10-29).
- **Câmera** (cópia do `camera.ts` do PAPER VOX em `src/modelos/vox/camera.ts`): chaves `{t, x, y, zoom, rot, curva, arco}`, zoom em escala log; motion blur por amostras acima de 18 px/q. Durações de chegada do `CHEGADA` de `scripts/lib/mural.mjs` (l. 145–156): `snap-zoom` 0,32 s, `chicote` 0,55 s (arco 0,22), `recursao` 0,6 s, `recuo` 0,7 s. **Sem o `snap` do PAPER VOX:** `Easing.bezier(0.3, 1.45, 0.45, 1)` (`camera.ts` l. 14) passa ~6,6% do alvo em x, y e zoom, contra o "overshoot 0". Na cópia, trocar pelo `CURVAS.entrada` (`bezier(0.16, 1, 0.3, 1)`, sem overshoot e com 90% do curso no 1º terço) ou usar `assento`; o PAPER VOX de produção não muda. Para o frenético: chegadas curtas (`snap-zoom` sem overshoot, `chicote`, `recursao`) (proposta). Recuo de ×0,30 em ~1,4 s com o 1º plano cruzando (ref-08 mov §2). Nunca parada mais de 1 s: deriva de 2–5% (lemo) e câmera viva de 5 px (PAPER VOX). **Mergulho entre estações:** a chegada `recursao` (0,6 s, expo, arco 0) ou o mergulho de ~0,7 s da ref-09, sempre sem overshoot, parando em 0,8–0,9/k. O zoom se acumula a cada mergulho (× 1/k; com k 0,42, a 4ª estação fica a ~13× da 1ª): a câmera trabalha em escala log; conferir a nitidez na vitrine.
- **Estações:** ≥ 4 por bloco (até 5), de 2–3,5 s, cada uma dentro de uma parte da anterior (proposta; o Capitólio da ref-08 tem 3 movimentos em 4,33 s).
- **Duração:** 9–14 s.
- **Código:** `PaperVox.tsx` (`Mundo`, `BlurMovimento`; copiar), `camera.ts` (copiar, sem o `snap`) e um `scripts/lib/vox-mural.mjs` novo: cópia das âncoras (`T`, `PAL`, `primeira`, `ultimaFim`), da câmera, do `ctx(id, base, k)` (`mural.mjs` l. 229: a estação em escala k, base do mergulho; fica dentro do `criarMural`, não é exportado) e do `voaBoia` **sem** o `delete el.passo` (l. 414, que devolve a colagem a 24 fps), aceitando vários palcos e gravando `03_roteiro/vox.json`. Do `mural.mjs`, importar só os exports puros: `CHEGADA`, `CURVA`, `quando`, `tipoChegada`, `tamChave`, `criarSfx`, `BANCO`, `ALVO_PADRAO`, `pontosDoSom`, `medirTrilha`, `volTrilha`, `acharRaiz`. O `criarMural` não serve: exige `03_roteiro/shotlist.json` com `estacoes` e mural em serpentina com recuo final e card, e grava `quadro.json` com `modelo: 'paper-vox-instagram'`. Novas: `Resquicio` (foco por grupo de peças, P0) e `Mergulho` (estação dentro da anterior, P0; ver "Kit").

### `moldura` · ele meio cortado, animação atrás, cards de contexto
- **Lugar:** entre o mural e o split 2 (calibração original, 2026-10-29; pergunta 4 = A): a última estação do mural segue atrás dele.
- **Geometria** (ref-08 mov §3.1): moldura em x 58–1021, y 1354–1920; raio de 102 px nos cantos de cima, cantos de baixo fora do quadro, sem borda e sem sombra. Dentro, o bruto dele. A cabeça vaza por cima da animação a partir da linha dos olhos (topo da cabeça em ~y 1095).
- **Cabeça vazando: decidida** (o print que ele mandou é a cabeça vazando: "eu tô meio cortado no cenário"; Jorge 2026-10-28). Custo: recorte da cabeça em 1080×1920 (o tamanho da creatina corrigida e do bruto de trabalho) ≈ 1,3 s por quadro (~31 s de máquina por segundo; 10 s ≈ 5 min, pela fila). É o único recorte da pessoa no vídeo (a abertura não tem). Plano B, se o recorte falhar (pacote ou modelo fora do cache): moldura mais alta, cabeça inteira dentro, sem recorte.
- **Atrás:** animação em tela cheia, sempre em movimento: a cena anterior ampliada ~1,4×, com desfoque moderado, a 12 fps (ref-08 mov §3.3). O texto da cena anterior sai antes do zoom de 1,4× ou some no desfoque; texto legível no fundo só inteiro em y 240–900 e x 90–850 depois do zoom, e sem card por cima dele (Decisões 2026-10-20: texto nunca por baixo de imagem; 2026-10-28: nenhum texto sai da tela). Na ref, o "FAKE" aparece cortado atrás da pessoa: o look vale, o texto não.
- **Cards** (calibração original, 2026-10-29: "podendo aparecer cards e informações sobrepostas e cards com informações complementando o contexto"):
  - **o 1º cai e assenta:** 655 px em 1,63 s, easeOutCubic, rotação −6° → 0° (ref-08 mov §3.3), com o dado da Ficha (R14). Na ref, depois disso ele fica parado ao pixel por 2,5 s (~0,5 peça nova/s, a cena mais calma da ref-08), abaixo do piso deste guia. Aqui, depois que assenta, ele **boia** (±7 px, ±1,1°; Decisões 2026-10-20: recortes "nunca estáticos"), e a cena ganha 1 evento a cada ≤ 0,7 s: card novo (cai, voa ou sobe da borda), número contando, sublinhado, carimbo, ícone. Alternativa: a moldura é o respiro do vídeo, com no máximo 3 s sem evento (marcado no plano);
  - **o que dizem:** informação que completa o contexto da fala (o dado, de onde ele vem, uma comparação simples, o que uma palavra quer dizer), só da Ficha do tema ou do kit de fontes (`02 - ROTEIROS/Referências/Fontes por tema/`), em linguagem leiga, sem sigla e com o absoluto ao lado de todo relativo. É texto fora da fala, como o card "Obs." (Decisões 2026-10-29): entra no plano de batidas com a fonte (⏸) e passa pelo `checador-de-afirmacoes`;
  - **sobreposição:** os cards se sobrepõem entre si e à cena. O novo cobre só papel, foto ou borda do anterior, nunca o texto dele: o texto de baixo fica inteiro e legível, ou sai antes (dissolve + desfoque de 0,20 s) (Decisões 2026-10-20: texto nunca por baixo de imagem). Nunca sobre o rosto nem sobre a legenda. ERRO no `validar-vox`;
  - **leitura:** cada card fica inteiro e sem mudar por ≥ (letras ÷ 15) + 1,5 s (ver "Texto cinético"): quantos cabem no trecho sai dessa conta.
- **Faixas:** o 1º card desce até y ~1150, **atrás da cabeça**: o matte cobre a base dele, como no print do Jorge (ref-08: cartão em y 150–1133). Papel e foto dos cards podem descer atrás da cabeça; o texto, não: texto dos cards só em y 240–900 e x 90–850. A faixa 920–1000 fica sem texto de card, para a legenda (centro 960): o papel do 1º card, que desce atrás da cabeça, passa por baixo dela, e a legenda leva a caixa cinza sobre o papel claro (legenda sempre por cima); cabeça a partir de ~1095 (área segura; proposta).
- **Entra e sai:** corte seco: a moldura nasce no lugar e a pessoa não se move, só trocam fundo e objeto (ref-08 mov §3.2: a pessoa sempre entra e sai por corte). Saída para o split 2 também por corte seco. A moldura que sobe e vira o painel do split só entra depois de aprovada num teste à parte, com a geometria escrita (raio 102 → 0, largura 963 → 1080, a cabeça que vaza voltando para dentro, reenquadramento do rosto).
- **Área morta:** o corpo dele fica sob o @/Seguir, a linha social e parte da coluna de botões: só imagem, nunca texto. O queixo (~y 1517) fica acima da linha social (1531) (área segura).
- **Duração:** 4–7 s por trecho; no máximo 2 trechos e 10 s no total por vídeo (custo do recorte). O da espinha fica entre o mural e o split 2 (calibração original, 2026-10-29); um 2º, só como opção marcada no plano (⏸). Abaixo de 45 s, encolhe para 3–4 s; tirar só com ok dele.
- **Código:** novas `MolduraPessoa`, `CartaoQueCai` e `CardsContexto`. Matte da cabeça = sequência WebP do `recortar.mjs` (rodar, não editar; pela fila e só com o cache, ver Pipeline, etapa 7): `04_broll/recortes/<nome>/q0001.webp…` (pasta terminada em `/`; o `_alfa.webm` é apagado, l. 41–47), lida com `<Img>` quadro a quadro como o `Recortado` de `src/modelos/MotorCamadas.tsx` (l. 578–599): `staticFile(arquivo + 'q' + String(n).padStart(4, '0') + '.webp')`, com n = floor((desde + frame/fps) × fpsSeq) + 1, e o mesmo transform do `<Video>` do rosto. Copiar esse leitor para `src/modelos/vox/`; **nunca `OffthreadVideo`** (falha com "No frame found at position"). O manual do motor (l. 156 e 179) ainda fala em `.webm`: corrigir lá é calibração original.

### `fecho` · só ele no encerramento
- Igual ao `ele` (punch a cada ≤ 2,5 s), com a última frase legendada.
- **Padrão: card final** com nome + @ (no máximo 2,5 s depois da última fala; `CardTexto` do TD2, copiar) e, depois dele, o corte para preto em ~0,2 s (ref-09 54,95 s, que não tem card). O @ só aparece no card final (Decisões 2026-10-08, todos os formatos). Tirar o card só se ele pedir. Nome + CREF 000000-G/UF quando ele se apresenta.
- CTA no meio do vídeo só na fala e na legenda, sem @ na tela (ref-09: CTA aos 37,7 s).

### Costura entre blocos (proposta)
| De → para | Como | Ref |
|---|---|---|
| abertura → invasão | papel invade ou peças cobrem, por cima dele; texto e cartão saem antes de a 1ª peça chegar neles | ref-08 0,77 s; ref-09 1,80 s |
| invasão → split | o painel dele sobe e a cena encolhe para o painel; ela fica ≤ 1,0 s, e a 1ª animação própria do split entra por chicote ou troca de camada na 1ª palavra-chave | ref-09 8,0 s |
| split → ele | corte seco; a legenda muda de lugar no mesmo quadro | ref-09; Decisões 2026-10-27 |
| ele → mural | corte seco + montagem do vazio, ou "peças cobrem" / "papel invade" por cima dele (a que não entrou no bloco 2: ele pediu "entra invasão de colagens novamente") | ref-08 32,67 s; Jorge 2026-10-28 |
| mural → moldura | a última estação segue atrás, ampliada e desfocada, sem o texto; ele entra na moldura por corte (calibração original, 2026-10-29) | ref-08 36,5 s |
| moldura → split 2 | corte seco (a moldura que sobe só depois de um teste aprovado) | ref-08 mov §3.2 |
| split 2 → fecho | corte seco | ref-09 |
| fecho → fim | card final + corte para preto | Decisões 2026-10-08; ref-09 54,95 s |
- Troca de layout com efeito: só desfoque e zoom, nunca opacidade (o quadro nasceria do preto; TD2).

## A animação de exemplificação
### Unidade
- **1 ideia ou analogia da fala = 1 animação** (ref-05; ref-07; Decisões 2026-10-28). A animação mostra a analogia ou a imagem mental do roteiro (v1; explicação sempre por analogia, regra da raiz).
- As animações do vídeo contam uma história: problema → mecanismo → consequência → saída, na ordem da espinha (gbro). No mural, o resquício é o objeto-chave da animação anterior.
- **O foco são as animações, não artigos:** print de estudo (circulado) só quando a fala cita o estudo, como apoio rápido, nunca a peça principal; a observação (ex.: card "Obs.") entra depois da frase (Decisões 2026-10-29).

### Ficha da animação (texto, 1ª aprovação; gbro + v1)
Uma linha por animação no plano de batidas:
- `id`, `bloco`, `layout` (invasão, split, mural, moldura, faixa), `palavra de entrada` (âncora no `palavras.json`);
- `analogia do roteiro`, `metáfora em 1 frase`, `sentido` (o que a pessoa entende);
- `objetos-chave` (3–6), cada um com papel: sujeito, conector, ação ou resultado, + `peças de apoio` até **≥ 10 elementos no quadro composto de tela cheia e ≥ 7 no painel do split** (cofre do print do Jorge na ref-08: ~12, com cofre, multidão, papéis nas mãos, gaveta, cartão, ACCOUNT CLOSED, PANIC, OCTOBER 1907, caderneta, jornal, alfinete e fita; garagem da ref-09: 12 peças em 1,6 s). Peças de código contam: etiqueta, carimbo, fita, alfinete, papel, traço, número. AVISO no `validar-vox` abaixo disso;
- `ordem de montagem` ligada às palavras-chave;
- `texto da cena` (1–3 palavras da fala; número só da Ficha);
- `câmera` e `transição` de saída;
- `fica para a próxima` (resquício, sujeito que continua, ícone);
- `stills` (1 cenário + quantos recortes a cena pedir, sem teto; Jorge, 2026-10-29) e a proporção, `receita`, `SFX`.

Depois da aprovação, o **esquema por elemento** (gbro): `elementos[]` com o que é, papel, entrada, saída e posição em px do palco; `espaço livre` (a faixa da legenda e do texto, fora da área morta); `quadro final` (o still composto aprovado). O Jorge aprova por número: só o aprovado avança (gbro).

### Receitas
Assinatura comum: recorte com borda de papel de ~7 px por fora da máscara, que ainda esconde o erro do chroma (lemo; ref-02, ref-08); 1 acento por cena (ref-05, ref-09); texto sempre por cima das peças (Decisões 2026-10-20); peças a 12 fps; sem overshoot.

| Receita | Ref | Quando | Como (tela cheia) | No split | Stills (ponto de partida; sem teto) |
|---|---|---|---|---|---|
| R1 Estudo em 1 s | ref-01 | Só quando a fala cita estudo (Decisões 2026-10-29) | Só print real conferido (`capturar-manchete.mjs`), aprovado no plano; sem print, R8 com o número da Ficha (página genérica com frase marcada vira estudo com texto inventado). Zoom rápido até a frase + marca-texto azul elétrico ou círculo à caneta; ≤ 1,5 s | igual | 0–1 |
| R2 Cena em camadas | ref-04 | Mecanismo (intestino, inflamação, digestão) | 3–5 camadas, uma por palavra-chave, sobem e travam | 3 camadas | 3–5 |
| R3 Colagem que se monta | ref-02; ref-08 (Pisa) | Virada, "o corpo reage", ação | 6–8 peças voam das bordas e montam em ~0,5 s; depois 1 por vez a cada 0,15–0,7 s; desmonta 2× mais rápido | 5–6 peças | 3–4 |
| R4 Mesa de arquivo | ref-03 | Contexto, história | 2–3 objetos pousam; seta e rabisco à mão; virada de página para "mito → verdade" | igual | 2–3 |
| R5 Recorte + palavra | ref-05 | Frase de impacto, conceito | 1 recorte P&B + 1 palavra gigante POR CIMA (nunca atrás; Decisões 2026-10-20); mancha ou linha azul elétrico | igual | 1–2 |
| R6 Objeto isolado | ref-06 | Palavra-chave isolada, lista | 1 objeto, spot, estrela azul elétrico; anel orbital para lista | igual | 0–1 |
| R7 Interface como palco | ref-07 | "Pesquisou no Google", mensagem | UI genérica em código, sem marca real | igual | 0 |
| R8 Colagem halftone | ref-08 | Número, notícia, comparação | Duotone + retícula (passo 20–26 px; abaixo de 14 px vira moiré; lemo); círculo atrás do sujeito, fita, clipe; contador "X em cada 10" | igual | 1–2 |
| R9 Cenário que se monta (nova) | ref-09 (garagem) | Cena principal da invasão e do mural | Cenário já no corte + etiqueta de papel rasgado com fita + texto do tema digitado + mão que entra pela borda em 0,1 s com objeto em pêndulo + "porta" que abre em 0,1 s revelando o sujeito + seta e brilhos ✦ + push 1,8× e mergulho | sem mergulho; push ≤ 1,3× | 1 cenário + 3–5 recortes |
| R10 Troca de camada (nova) | ref-09 (4,2 · 6,6 · 22,4 s) | "Em vez de", mito × verdade, comparação de conceito (nunca de corpo) | Fica o sujeito e troca o mundo (cortina 0,4 s), fica o mundo e troca o sujeito (0,2 + 0,3 s) ou painéis de papel abrem (0,4 s) | igual | 2–3 |
| R11 Faixas (nova) | ref-08 (0,8–5,1 s) | 3 exemplos, lista de 3 | Variante `faixas` | — (uma animação por vez: a lista vira trocas seguidas; Jorge, 2026-10-29) | 3–6 |
| R12 Viagem com parallax (nova) | ref-09 (fábrica); ref-08 (Capitólio) | Contexto amplo ("na rotina", "no mundo") | Travelling lateral ou recuo ×0,3, com o 1º plano cruzando a 4–6% da largura por quadro, por baixo do texto (ou sem texto na tela); fundo e meio andam quase juntos; peça nova a cada 0,15–0,7 s; 1 vez por bloco de tela cheia, peça gigante pelo 1º plano (~70% em 0,17 s) + fundo −50% em 0,4 s + contador linear | travelling ≤ 30% da largura | 3–4 |
| R13 Anotação sobre a cena (nova) | ref-09 (noite) | Apresentar personagem, órgão, alimento | Cena parada + nome à mão em itálico serifado (~17 letras/s) + sublinhado 0,27 s + coroa ou círculo 0,13 s, com 70–130 ms entre eles | igual | 1 |
| R14 Cartão que cai (nova) | ref-08 (36,5 s) | Dado da Ficha, na `moldura` | Cartão preso por 2 prendedores cai 655 px em 1,6 s, −6° → 0°, assenta e boia; depois, 1 evento a cada ≤ 0,7 s | — | 0–1 |
| R15 Congela e marca (nova) | lemo (telestrator, visual-investigation) | Explicar um detalhe da animação | Flash de 0,1 s a 0,55, punch 1,035 → 1,0 em 0,35 s; fora do foco, escurece a 0,42; anel → área → rótulo com 0,3–0,6 s entre eles; incerteza em tracejado e "≈" | igual | 0 |

- A coluna "Stills" é ponto de partida, não teto (calibração original, 2026-10-29): cada cena leva 1 cenário e quantos recortes precisar para ficar densa e bonita. O código fica com o que já é código (traço, texto, número, etiqueta, fita, carimbo, interface) e não entra no lugar de um recorte de foto só para poupar Flow.
- A mesma receita nunca em duas animações seguidas e no máximo 3 vezes por minuto (v1).
- Termo que volta na fala muda de sujeito visual dentro da família: corte anatômico, escala (célula, órgão, corpo), objeto-analogia do roteiro, recorte clássico (v1).
- R1, R7 e R8 só quando a fala cita fonte, busca ou número (v1).
- Ficam fora até um teste à parte, aprovado pelo Jorge: multidão que cresce, tentáculo, torre em espiral com mola (risco alto; v1, ref-08).

### Tela cheia × meia tela
| Destino | Palco | Still | Sujeito | Livre para texto |
|---|---|---|---|---|
| Tela cheia (`invasao`, `mural`) | 1080×1920 | 9:16 | y 240–1040 com a legenda embaixo; até 1500 (x 90–850) só com a legenda em 960 | faixa da legenda (ver "Legenda") |
| Meia tela (`split`) | 1080×960 | 1:1 | x 162–918, y 240–900 do painel (imagem sem texto até 144) | y 920–960 do painel (legenda na emenda) |
| Faixa (só tela cheia) | 1080×624–666 | 16:9, ampliado 3–10% | centro da faixa; na faixa 3, metade de cima | emenda 2/3 (y 1254) para a legenda |
| Fundo da `moldura` | 1080×1920 | 9:16 | texto dos cards em y 240–900, x 90–850 (papel e foto podem descer atrás da cabeça) | y 920–1000 (legenda por cima; sem texto de card, o papel pode passar por baixo) |
- Cheia → meia: `SplitSobe` (a cena encolhe ~20% e recorta 9:8) e fica ≤ 1,0 s no painel. O sujeito do still 9:16 precisa estar nos 50% do meio da altura (área segura).
- Meia → cheia: a câmera sai do painel e abre a mesma cena (v1; exige still 9:16).

### De onde vem cada peça (nesta ordem; v1)
1. **Código:** forma, traço, texto, contador, interface, ícones (`lucide-react`), objetos de papel do PAPER VOX. Zero imagem.
2. **Biblioteca** (`%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel`, etiquetada): só peças neutras (textura, papel, objeto solto). A cena-chave de cada ideia é sempre gerada para a frase (v1).
3. **Nano Banana no Flow** (0 crédito em 1K, Chrome do Jorge): bloco FOTO, RECORTE ou MONT do `prompts-flow.md` do PAPER VOX + o bloco do look C (foto-colagem com luz real) + o assunto. **Por cena: 1 cenário e quantos recortes ela pedir** (calibração original, 2026-10-29). Ritmo (anti-robô, aprendido em 2026-10-21; memória "flow-limites": o bloqueio veio depois de ~12 gerações seguidas): no máximo 1 ou 2 gerações por disparo, com pausa entre elas, nunca uma atrás da outra (calibração original, 2026-10-21; `03 - CARROSSÉIS E ARTE/CLAUDE.md`); ~1,5–2 min por still (estimativa, medir na 1ª sessão: 30 stills ≈ 45–60 min); acima de 20 stills, 2 ou mais sessões de Flow, em dias diferentes se o anti-robô aparecer; sempre 0 crédito. Para virar camadas: 3–6 grupos grandes e separáveis, campo livre para o texto, sujeito no meio; sem número, logo, marca-d'água, interface, legenda nem 3D brilhante (gbro). Recorte sobre azul #0000FF + `recorte-chroma.mjs`; 2–3 poses do mesmo personagem (v1, ref-02). Grupo do still aprovado que precisa mexer sozinho é gerado de novo sobre o azul e recortado (gbro).
4. **Vídeo gerado** (Omni/Veo): só como exceção, com ⏸ e custo (regra 5 do lab).
- As stills ficam em `<proj>/04_broll/ia_flow/` e só vão para a `%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel`, etiquetadas (Decisões 2026-10-27), no fechamento, com ok do Jorge, ou com a exceção escrita no `05_LAB/CLAUDE.md` (regra 1 do lab: só se escreve no lab; o TD2 já pôs 7 recortes na biblioteca). Nada se repete no mesmo vídeo (Decisões 2026-10-27).
- **Sem teto de stills por vídeo** (calibração original, 2026-10-29: "1 cenário e até quantos recortes forem necessários, lembre que precisamos de vários elementos para compor uma cena às vezes complexa mas bonita"). Mandam a densidade mínima (≥ 10 elementos no quadro de tela cheia, ≥ 7 no painel) e a beleza do quadro. O nº de stills (contando as refeitas sobre o azul, as 2–3 poses e o nível fino) e o tempo de Flow entram no ⏸ do plano de batidas (Pipeline, etapa 3).

### Ética (CFN e evidência)
- Sem antes/depois de corpo, promessa, depoimento de paciente nem preço (CLAUDE.md da raiz; v1). Nenhum corpo no tema emagrecimento: cabeças sem rosto, estátua só com cabeça e ombros, balança sem número (PAPER VOX).
- Números só da Ficha (nos cards de contexto da `moldura` e no card "Obs.", também do kit de fontes; ver abaixo), simples e comparativos ("8 em cada 10"); sem views nem likes (v1). Palavra nunca mais forte que a fonte; incerteza desenhada com "≈" e tracejado (lemo; regra da base).
- Sem pessoa real reconhecível, marca real, nem página que imite jornal ou estudo real com texto inventado (v1).
- Efeito relativo só com o absoluto na mesma tela (ex.: "de 2 para 3 em cada 100"; nunca só "50% a mais" ou "2 vezes mais"). Rótulo e número sem sigla nem termo técnico. Sem prescrição individual (dose ou porção para quem assiste) (CLAUDE.md da raiz). ERRO no `validar-vox` para "%" ou "vezes" sem o absoluto ao lado.
- Essas regras valem para o que a edição põe na tela. A fala dele não se corta nem vira proposta de regravação: o que a fonte não sustenta vira um card "Obs." depois da frase (Decisões 2026-10-29; teste da creatina, `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/03_roteiro/checagem-texto-tela.md`).
- Texto que não está na fala (os cards de contexto da `moldura`, Jorge 2026-10-29, e o card "Obs."): só da Ficha do tema ou do kit de fontes (`02 - ROTEIROS/Referências/Fontes por tema/`), com a fonte no plano de batidas (⏸) e o `checador-de-afirmacoes`.

## Especificação de movimento
**Frenético = piso, não teto.** O ritmo não pode ficar abaixo do medido nas refs. **Onde ref-08 e ref-09 divergem em ritmo, vale o número mais rápido.**

| Medida | Regra (faixa permitida) | Medido | Fonte |
|---|---|---|---|
| Entrada de peça (posição) | 0,08–0,60 s; **mediana da cena ≤ 0,30 s** | ref-09: mediana 0,28 s (0,10–0,60); ref-08: 0,27 s | ref-09 §10; ref-08 mov §5 |
| Snap de objeto (mão, porta) | 0,08–0,17 s | 3–5 q a 30 fps | ref-09 |
| Carimbo, pop | 1 passo a 2,2× e depois 1×, só em peça ou palavra de até ~400 px de tinta (2,2 × 400 ≈ 900: nada sai da tela) | "?" a 2,2× por 2 q | ref-08; Decisões 2026-10-28 |
| Peça que sobe da borda | 0,23–0,33 s | 7–10 q a 30 fps | ref-08 |
| Peça que voa e monta | ~0,5 s em S (50% em ~0,2 s, 90% em ~0,4 s) | Pisa | ref-08 |
| Recorte que voa (`voa`) | 0,30 s (0,24–0,42), em arco, giro 24° → 0°, blur 18 → 0 | 0,36–0,42 s | PAPER VOX; Decisões 2026-10-20 (0,30 s é proposta) |
| Digitação | 15–43 letras/s, 2–3 letras por passo | 0,23–0,53 s por palavra | ref-09 |
| Abertura (1º 1,0 s) | ≥ 3 eventos de texto ou cartão, o 1º até 0,15 s; ≥ 7 eventos nos 3 primeiros segundos, contando a invasão; texto e cartão saem juntos em 0,20 s | texto 0,10 → cartão 0,33 → logo 0,57; ~7 em 2 s | ref-09 §5.1; Jorge 2026-10-29 |
| Cartão da abertura (aba) | abre em 0,17 s, girando na própria borda; a palavra acende em 0,20 s, na palavra falada | 5 q + 6 q a 30 fps | ref-09 §5.1 |
| Traço à mão | 0,13–0,47 s; ponta da seta nos últimos 10% | seta 0,33; sublinhado 0,27; coroa 0,13 | ref-09; lemo |
| Troca de camada | 0,30–0,40 s | 0,4 s; 0,2 + 0,3 s | ref-09 |
| Troca de layout | corte seco ou ≤ 0,60 s | split que sobe: 0,6 s até 96% | ref-09 |
| Saída | corte seco; 0,13–0,20 s (dissolve + desfoque, chicote); peças voltam pela borda em ease-in, 2× mais rápido; encolhe em ícone 0,33 s | 4–6 q; 8 q; 10 q a 30 fps | ref-09; ref-08 |
| **Overshoot de posição** | **0**. Impacto = entrar grande (2,2× → 1×) ou passar para menos (72% → 100% em ~0,23 s) | 0% em todas | ref-09; ref-08 |
| Curva | expo-out: ≥ 50% do curso no 1º terço do tempo | 56% em 1/3 | ref-09 |
| Escalonamento entre peças | 0,07–0,40 s; mediana ≤ 0,15 s | mediana 0,15 s | ref-09 |
| Mexendo juntas | 3–6, fora a câmera | 3–6 | ref-09; ref-08 |
| **Rajada de cada animação** | **≥ 7 peças novas no 1º 1,0 s em tela cheia** (invasão, cada estação do mural, faixas); **≥ 5 no painel do split** | ref-09: 5 em 0,7 s a 12 em 1,6 s (~7/s); Pisa 16/s por 0,5 s | ref-09 §3, §5.3; ref-08 |
| Peças novas por segundo (média da animação) | tela cheia ≥ 2,8; painel do split ≥ 3, e ≥ 4,5 nos 2 primeiros segundos de cada animação | ref-09 2,5; Capitólio 2,8; faixas somadas 4,5 | ref-09; ref-08 mov §1.3, §2 |
| Densidade do quadro composto | ≥ 10 elementos em tela cheia; ≥ 7 no painel (peças de código contam) | cofre ~12; garagem 12 | ref-08 (print do Jorge); ref-09 |
| Peça gigante pelo 1º plano | 1 por bloco de tela cheia: cobre ~70% em 0,17 s, por baixo do texto | pombo: 5 q a 30 fps | ref-08 mov §2 |
| Escurece para o número | −50% em 0,4 s | 12 q a 30 fps | ref-08 mov §2 |
| Buraco sem evento | ≤ 1,0 s na animação; 1 respiro de até 3 s por vídeo, marcado no plano | — | lemo; v1 |
| Plano | 0,7–4,5 s; **média ≤ 2,4 s** | média 2,4 s (2,1 com os cortes internos; 0,70–4,4) | ref-09 §3 |
| Trocas no vídeo (layout, corte interno, punch por corte, troca de camada, chicote, mergulho ou puxada, chegada de câmera) | **≥ 0,54 por s** | ~30 eventos dessa lista em 55 s (§7: 26 trocas de plano + 6 passagens dentro do plano); só os cortes dão 0,40 | ref-09 §3, §7 |
| Câmera na animação | sempre andando: push total de 1,3–2,7× ou travelling ≥ 10% da largura; nunca parada > 1 s (deriva 2–5%) | push 1,8–2,7×; maior contínuo 4,1 s | ref-09; lemo |
| Puxada seca | 2× → 1× em 0,17 s, expo-out | 5 q a 30 fps | ref-09 |
| Mergulho (entre as estações do mural; Jorge, 2026-10-29) | ~0,7 s, pico de velocidade no meio, ou `recursao` 0,6 s (expo); para em 0,8–0,9/k; peças saem pela borda e ficam ~0,3 s cortadas | garagem; E12 no celular (k 0,42) | ref-09; PAPER VOX |
| Recuo | ×0,30 em ~1,4 s (acelera 1,1 s, freia 0,3 s) | Capitólio | ref-08 |
| Empurra + estouro | ×1,8 em 0,4 s (ease-in) + estouro claro em 0,2 s | Capitólio | ref-08 |
| Física | pêndulo de 22°, período 2,0 s, amortecimento 0,25: ângulo = 22·sen(πt)·e^(−0,25t); peça que se solta e voa em 0,4 s | luminária, chave, roda | ref-09 |
| Cadência | colagem 12 fps; traço 8 fps; rosto, legenda e pós 24 fps; sem tremor de posição. Relógios possíveis num vídeo de 24 fps: 8, 12 e 24 fps (passo 3, 2 e 1) | 12–15 fps; pessoa a 29,97 | ref-09; ref-08; PAPER VOX |

- **Trava** (`scripts/validar-vox.mjs`; a lista exata fica no cabeçalho do script; ver "Checagens", no Pipeline):
  - ERRO: mediana de entrada > 0,30 s; rajada < 7 no 1º segundo em tela cheia ou < 5 no painel (fora do respiro); painel do split abaixo de 3 entradas/s de média; buraco > 1,0 s; overshoot de posição, inclusive chave de câmera com curva que passa de 1; trocas < 0,54/s; plano médio > 2,8 s; texto dentro do resquício; "%" ou "vezes" sem o absoluto ao lado; card da moldura sobre o texto de outro card, sobre a legenda ou sobre o rosto; texto ou cartão da abertura sobre o rosto (caixa do rosto medida na vitrine).
  - AVISO: plano médio > 2,4 s; tela cheia abaixo de 2,8 peças novas/s; menos de 10 elementos no quadro de tela cheia ou de 7 no painel; mais de 6 peças se mexendo juntas (poluição; gbro: "no clutter").
- **Prova fixa depois do render:** o `validar-vox`, o brilho médio (YAVG) e o loudness (ver "Pipeline").
- **Opcional, com ⏸ antes de portar (tarefa grande):** relatório de ritmo (lemo `rhythm_report`, a portar para Node + ffmpeg): energia de movimento por quadro, médias por 0,5 e 1 s, janelas chapadas, cortes e distância de cada evento ao onset de áudio mais próximo (meta ≤ 40 ms). Medir a ref-09 com o mesmo script antes, para comparar na mesma régua (na ref-09 §3: pessoa 3,4–3,8; animação 4,2–7,6; montagens 20–30).

## Texto cinético e legenda
### Área morta do Reels (medida; área segura)
- **Topo:** status e abas "Reels | Amigos" até y ~200. Com folga: nada em y < 240.
- **Coluna de botões:** x 913–994, y 1042–1880 (coração, comentar, repostar, compartilhar, mais, capa do áudio, com as contagens). Com folga: nada em x > 850 a partir de y 1000 (pt-BR "12,3 mil" e Android começam em ~890–903).
- **Faixa de baixo:** linha social 1531–1676, avatar/@/Seguir/áudio 1715–1799, legenda do post 1834–1878. Com folga: nada abaixo de y 1500.
- **Laterais:** o vídeo ampliado perde 46 px (iPhone) a ~70 px (Android) de cada lado. Com folga: 90 px.
- A barra de navegação fica fora do quadro.
- Reels impulsionado: topo 269, base 1248, laterais 65 (Meta).
- A regra antiga do kit ("x > 86%, y 55–90%") fica curta: perde 16–40 px na coluna, não pega a faixa de baixo e para 6–8 px dentro do ícone de cima. Neste formato vale a régua acima.

**Faixa segura da legenda:** a tinta inteira e a caixa (acento, cedilha e o pico da entrada, se houver) em y 240–1500; x 90–850 quando alguma parte fica em y ≥ 1000; x 90–990 quando o bloco todo fica acima de y 1000.
**Faixa segura do texto grande:** y 240–1000 em x 90–990; até y 1500 só em x 90–850; nada abaixo de 1500. Vale para o texto da cena, o texto e o cartão da abertura e os cards da moldura.

### Texto cinético (dentro da cena)
- **A palavra grande fica aqui, não na legenda** (calibração original, 2026-10-29: legenda pequena em tudo): no texto da cena, no cartão da abertura e nos cards da moldura.
- Preso ao mundo: anda e cresce com a câmera; a legenda é fixa (ref-09 §5.3). A caixa inteira fica na faixa segura enquanto é lida; só sai pela borda ao sair de cena (proposta).
- Fonte do tema (ref-09: serifa de alto contraste, itálico serifado, estêncil), sem fonte nova:

  | Papel | Fonte | Tamanho | Entrada | Fonte da regra |
  |---|---|---|---|---|
  | Palavra gigante (impacto, R5; fora da abertura) | Anton ou Inter Tight 900 condensada | 80–83% da largura (até 900 px de tinta, x 90–990), inteira acima de y 1000; ≥ 15% da altura | letra a letra, como no CUT; carimbo (2,2× → 1×) só em palavra de até ~400 px de tinta | CUT; v1; Decisões 2026-10-28 |
  | Texto digitado da abertura | Instrument Serif em caixa alta, creme, 1–2 linhas | maiúscula ~86 px | digitação 2–3 letras por passo (~43 letras/s), termina 0,1 s antes de a palavra acabar | ref-09 §5.1; Jorge 2026-10-29 |
  | Palavra do cartão da abertura | Anton ou Instrument Serif, branca sobre o azul elétrico | cabe no cartão (até 760 px de largura) | acende em 0,20 s na palavra falada | ref-09 §5.1; Decisões 2026-10-20 |
  | Texto do tema (etiqueta, nome do objeto) | Inter Tight 900 ou Anton | maiúscula ~48 px, cresce com a câmera | digitação | ref-09 |
  | Anotação à mão | Instrument Serif itálica | maiúscula ~60 px | letra a letra, ~17 letras/s | ref-09 |
  | Número | Anton, dígitos de largura fixa | conforme a cena | conta até o valor em 0,45–0,9 s | lemo; TD2 |

  Estêncil e geométrica do tema pedem fonte nova: só com ok do Jorge (proposta).
- Pedaços de 2–3 palavras: cada pedaço entra 0–2 q antes da 1ª palavra dele, com 0,12 s de cascata entre as palavras dentro do pedaço; escala 1,3 → 1 em 0,13 s, sem passar de 1, opacidade cheia em 0,04 s (lemo, adaptado às refs: sem quique). Saída em dissolve + desfoque de 0,20 s (ref-09) ou corte.
- **Imagem nunca por cima de texto:** o 1º plano que cruza passa por baixo do texto da cena e da legenda, ou só cruza sem texto na tela; recorte nunca sobre a legenda; as lascas do plano da frente ficam nos cantos, fora da zona de texto (Decisões 2026-10-20 e 2026-10-22).
- Cor: palavra-chave nos 3 degradês da marca em rodízio, dois seguidos nunca iguais; apoio em creme #F2F4F8; branco só sobre o azul elétrico (Decisões 2026-10-20). Azul elétrico nunca em texto ou traço fino sobre o escuro (contraste de 2,5–2,9:1; creme sobre azul elétrico dá 5,6:1; v1). A legenda é a exceção: branca, como a ref-09 (calibração original, 2026-10-29, legenda B), com caixa cinza sobre fundo claro.
- Leitura (lemo `readcheck`; calibrar em PT-BR): texto que não é falado (rótulo, número, card de contexto da moldura) fica inteiro e sem mudar por ≥ (letras ÷ 15) + 1,5 s; comparação, ≥ 2,5 s. Texto falado fica inteiro até a palavra terminar + 0,3 s (proposta).
- Nunca texto dentro da imagem gerada: todo texto vai em código (v1; ref-08; gbro).
- Texto sempre em HTML, nunca `<text>` em SVG (PAPER VOX).

### Legenda (calibração original, 2026-10-29: pequena e discreta em tudo)
Escolha B da pergunta 6, como a ref-09 (§12): grotesca bold em caixa alta, branca, ~45 px (maiúscula ~33 px), 1–3 palavras, sombra suave; caixa cinza #81817A arredondada só quando o fundo atrás é claro. Aqui, Inter Tight 700 (já no kit, sem fonte nova) (proposta). O bloco tem ~59 px de altura. **A palavra grande não vai na legenda:** fica no texto cinético da cena (acima). A LegendaB do TD2 (apoio + chave Anton de 167 px) não entra no VOX.

| Layout | Centro (y) | Largura máxima da tinta | Observação |
|---|---|---|---|
| `split`, `moldura` | **960** (na emenda; na moldura, acima da cabeça) | 620 px | ref-09: 50%, parada sobre a emenda. Tinta em ~930–990. Na moldura, a cabeça começa em ~1095 e nenhum texto de card entra na faixa 920–1000 (o papel do 1º card passa por baixo da legenda, que leva a caixa cinza) |
| `ele`, `fecho` | **queixo medido + 50 px, teto 1460** | 620 px | Na ref-09 fica a 50%, no peito; no Jorge, 50% cairia no queixo (~950 no estúdio de gravação original). O bloco começa ~20 px abaixo do queixo, nunca no rosto. Medir o queixo no bruto corrigido |
| `invasao`, `mural` | **1150–1420** (abaixo do sujeito) | 620 px | ref-09: 64,5–73,9%. Ou centro 960, se a cena deixar livre a faixa 920–1000 |
| `faixas` | 1254 (na emenda 2/3) | 620 px | Texto da faixa 3 só em y 1290–1500 |
| `split` 60/40 | ~1160 (na emenda) | 620 px | Só com o queixo ≤ 1500 |
| `abertura` | nenhuma enquanto o texto digitado e o cartão dizem as palavras | — | ref-09: ela volta em 1,9 s |
- Largura: até 620 px, centrada em x 540 (x 230–850), em todos os layouts: cabe na régua de y ≥ 1000 e sobra (na ref-09, a legenda não passa de 34% da largura, ~370 px). O `montarBlocos` deixa uma palavra sozinha passar de 18 caracteres: bloco maior que o limite encolhe a fonte até caber, nunca vaza da tela (proposta; CUT: nenhum texto sai da tela). O encaixe se faz na composição, com `fitText`/`measureText` do `@remotion/layout-utils` (já usados no `palavra-impacto.tsx`). O `validar-vox` roda em Node, sem métrica de fonte (opentype e fontkit pedem instalação, com ⏸): faz só uma estimativa conservadora pela largura média por letra da legenda (~45 px) e das fontes do texto cinético, medida 1 vez numa still.
- Reels impulsionado: centro ≤ 1215 (tinta até 1248) (área segura).
- A legenda muda de lugar no mesmo quadro da troca de layout (Decisões 2026-10-27).
- Caixa cinza só quando o fundo atrás da legenda é claro (ref-09; no TD2, a legenda creme sumiu sobre uma tela clara).
- Blocos de até 3 palavras / 18 caracteres (`montarBlocos`); ~1,6 troca/s na ref-09.

## Visual
**Look: C · foto-colagem com luz real (decidido em 2026-10-29).** Fonte: o Jorge chamou a ref-09 de "principal vídeo reference" e disse que ela é "o exemplo do tipo de colagem e dinamismo entre as peças que eu quero que componham a cena e sua complexidade" (2026-10-28). A e B ficam na tabela só como registro; trocar de look depois é trocar o bloco de estilo do prompt, sem mudar código. O look continua o C: as escolhas de 2026-10-29 (abertura B e legenda B) vêm da mesma referência (calibração original, 2026-10-29).

| | A · Escuro de papel | B · Claro e colorido | **C · Foto-colagem com luz real (escolhido)** |
|---|---|---|---|
| Ref | PAPER VOX; v1 | ref-08 (faixas, Pisa) | ref-09 |
| Fundo | carvão #1C1A18 com vincos e grão; vinheta até #0B0B0C (fundo alternativo bordô #3E1D24, ref-03, não decidido) | papel creme #EDE3C8, branco #FBFBFB, quadriculado claro #D9D9DC | cenário fotográfico P&B ou dessaturado, médio-escuro (garagem #3E3D40), vinheta |
| Objetos | recorte P&B, papel #E9E9E6, jornal #D8D5CE, tinta #151515, papelão #4A3A2A | recortes P&B ou duotone (azul #3B4FA8 + creme), papel amassado, fita, clipe; campo #1FA67A → #0B4F5C | recortes P&B com luz de cena; papel #D6D1CA–#E7E8DA, tinta #1C1A19, texto #EFECE2 |
| Luz | spot ou gobo; borda de luz no recorte (no escuro a sombra some) | chapada; só vinheta e halftone | luz real (cone de luminária, luz vazando), rack focus, 1º plano desfocado |
| Acento | azul elétrico #2E49CE | azul elétrico no lugar do vermelho #D12B2B | azul elétrico no lugar do amarelo #F9CF19 |
| Atenção | parecido com o PAPER VOX | a legenda branca some no claro: caixa cinza obrigatória | prompt de luz mais preciso no Flow |

**Em qualquer look:**
- Acento: azul elétrico #2E49CE, a marca (Decisões; Identidade da marca), 1 por cena (ref-05, ref-09). Sobre o escuro, só em forma grande ou preenchida (barra, mancha, círculo, estrela) ou com glow (v1).
- Recortes P&B ou dessaturados, com borda de papel (lemo; ref-02, ref-08); luz da cena em vez de sombra no escuro (v1; ref-09 §6).
- Papel em pontos certos: etiqueta rasgada com fita cinza, folha com a borda visível, faixa de papel (ref-09); vincos e grão das `texturas.ts` (PAPER VOX).
- Traços à mão: seta, sublinhado, coroa, riscos, brilho ✦ (ref-09).
- Profundidade por luz e desfoque, não por sombra projetada (ref-09 §6).
- Halftone e duotone no PNG, uma vez por still (v1). Retícula gráfica com passo ≥ 14 px (lemo).
- Nunca preto liso em área grande (Preferências 2026-10-14, citadas na v1).
- Grão só no `Palco`, por quadro (o `Grao` do kit dentro do retângulo do palco); nunca no encode final, que pegaria o rosto (v1; Decisões 2026-10-09: cor do bruto intocável). A vitrine mede só o custo do grão por quadro no palco.
- Quadriculado escuro fica de fora: foi reprovado no carrossel (Preferências 2026-10-14, citadas na v1). O claro só no look B (ref-08).

## Áudio e SFX
- **Voz:** o bruto, ou a voz tratada se ele marcar na etapa 0 (TD2).
- **Música:** no máximo 1/4 da voz, pela conta do `ebur128` (Decisões 2026-10-08). Mixada depois do render, com cortes só voz nos momentos tensos (Decisões 2026-10-20) e 2 opções da biblioteca para comparar (padrão do fluxo do PAPER VOX, não pedido dele; Decisões 2026-10-20).
- **A `VoxBroll` não toca música:** não copiar o ducking nem o `sfxAuto` do TD2 (a trilha sairia dobrada). O `sfx` fica no formato `SfxLab` do PAPER VOX (via `criarSfx`, com `evento`/`alvo` e `sfxNaMixagem: true`); o render sai com `--sem-loudnorm`, e trilha, SFX e loudness entram no `mixar-audio.mjs <proj> --video <mp4> --props 03_roteiro/vox.json`. O `sfx` do TD2 (`som: 'motionix/…'` sem `.wav`) não é lido pelo `refinar-sfx.mjs`. No gancho, se a trilha tiver pulso claro, as trocas dos primeiros 15 s caem nele quando houver fim de frase a ±0,15 s (ref-09 §8: boom a cada 2,4 s) (proposta). Fora do gancho, a imagem segue a fala, não a batida (v1).
- **SFX:**
  - ~1 a cada 4–5 s, ≥ 1,15 s entre dois, nunca a mesma categoria em seguida, 12–17 dB abaixo da voz (Decisões 2026-10-20; ref-09: ~12 SFX em 55 s).
  - Só nos acentos: invasão = papel amassando (ref-08 0,8 s); chicote, split que sobe e mergulho = whoosh (ref-09 6,74 · 8,08 · 10,78 · 16,92 s); corte para a cena = impacto (15,24 s); porta = metal (15,76 s); painéis = papel (22,46 s); carimbo = thump + clack (lemo); marca-texto = risco de marcador e digitação = ticks (v1).
  - Sem hit em todo corte: a pessoa entra sem som (ref-09). Entrada de imagem, papel e fita sem som (Decisões 2026-10-20).
  - "Pestana" = virar página de papel: categoria `papel` (Decisões 2026-10-19, via v1).
  - Timing milimétrico: cada SFX no instante visual pelo ponto medido do som (ataque ou pico), com carretel de audição antes do final (Decisões 2026-10-20; PAPER VOX P7).
  - Fade de 25 ms no começo do áudio: o gancho abre com impacto (lemo).
  - Banco: `sfx/lab/`, Motionix e `sfx/biblioteca` (PAPER VOX). Download novo só com ⏸ (fonte, arquivos, tamanho; licença CC0 ou royalty-free comercial) (v1).
- **Final:** −14 LUFS, pico ≤ −1 dBTP (PAPER VOX; TD2).

## Pipeline do vídeo
O `/editar` segue estas etapas (V0–V11 em "Por formato"); o piloto mostra cada uma na prática.

| Etapa | O que sai | Como | ⏸ |
|---|---|---|---|
| 0 Bruto | `%SOUTO_VIDEO_PROJETOS%/<AAAA-MM-DD>_<slug>/01_bruto/` (`novo-projeto.mjs`) + bruto de trabalho (só se o bruto não vier em 1080×1920 a 24 fps; o do piloto já veio, ver abaixo) | Etapa 0 do `/editar` (decupar, cor, áudio) e "direto ou com as paradas", com a estimativa. Bruto de câmera: antes, `preparar.mjs <proj> --modelo vox-broll-instagram --cor <escolhida>` (sem `edicao.json`, ele pede `--modelo`). Depois, pela fila, o **bruto de trabalho em 1080×1920**: `ffmpeg -i <origem> -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 16 -pix_fmt yuv420p -g 24 -c:a copy 01_bruto/bruto_1080.mp4` (+ `-r 24` se a origem não for 24 fps), e o `02_analise/meta.json` regravado para ele antes do `recortar.mjs` (o `transcrever.mjs` não sobrescreve meta existente). Sem isso, o recorte roda na resolução nativa (`preparar.mjs` mantém 4K) | ⏸ etapa 0 (Decisões 2026-10-11) |
| 1 Decupagem | bruto decupado (só se ele marcar) | `decupar-inteligente.mjs` + agente `decupador` (repetição escondida: `lib/repeticoes.mjs`). Com decupagem, o `--render` gera `01_bruto/bruto_decupado.mp4`, mas três coisas seguem lendo o original: rodar `alinhar-palavras.mjs <proj> --audio 01_bruto/bruto_decupado.mp4` (o regex dele pega o `bruto.mp4`), gerar o bruto de trabalho a partir do decupado e apontar para ele o `meta.json` e a prop `bruto` | — |
| 2 Palavras | `02_analise/palavras.json` com tempos finos + `transcricao_corrigida.md` | `transcrever.mjs --principal` → `correcoes.json` (à mão) → `corrigir-palavras.mjs` → `alinhar-palavras.mjs`, pela fila (PAPER VOX; a sincronia de 0–2 q pede o alinhamento; o TD2 usa o `assistir.mjs`). **Bruto sem pausa** (o Jorge já aperta os cortes): no padrão (−35 dB, 0,35 s) sobram poucos silêncios e saem trechos longos demais (89 s no piloto); rode com `--limiar -30 --min 0.15`. Esse limiar marca fala baixa como silêncio e empurra palavras para fora dela: confira o `alinhamento.md` e conserte a corrida com erro ≥ 0,45 s ou espremida, voltando para a média do turbo longo com o small quando os dois concordam (no piloto, 37 palavras em 8 corridas; molde: `02_analise/transcricao_corrigida.md` do piloto, "Tempo das palavras"; o `palavras_alinhadas.json` guarda a saída do alinhar) | palavra em dúvida fora da tela até ele responder (PAPER VOX) |
| 3 Plano de batidas | `03_roteiro/plano-de-batidas.md`: blocos nos fins de frase (2 atos acima de 75 s), ficha de cada animação, imagens por origem e nº de stills do Flow (sem teto; Jorge, 2026-10-29), recorte da cabeça (só a moldura), texto dos cards de contexto com a fonte, opções marcadas (par extra `ele → split`, corte para `ele` dentro do split), plano de SFX, trilha e render estimado | agente `diretor-vox`, modo plano, com as âncoras do `lib/vox.mjs` (nunca segundos digitados); `checador-de-afirmacoes` no texto de tela e nos cards (`03_roteiro/checagem-texto-tela.md`) | **⏸** (por número; gbro) |
| 4 Prompts do Flow | `prompts_flow.md`/`.json` | modo prompts: blocos FOTO e RECORTE (azul #0000FF) do `prompts-flow.md` do PAPER VOX + o look C; "3–6 grupos grandes e separáveis", campo livre para o texto, sujeito no meio (gbro). Por cena, 1 cenário + os recortes que ela pedir, sem teto (calibração original, 2026-10-29), já divididos em sessões (1 ou 2 gerações por disparo, com pausa; Jorge, 2026-10-21). Sempre 0 crédito: se o 2K "aprimorado" debitar (etapa 5), o custo × nº de stills entra neste ⏸ antes de qualquer 2K | **⏸** |
| 5 Stills e recortes | escolhidas + folha numerada; PNG com alfa | Flow no Chrome do Jorge, Nano Banana 2.1, 1 ou 2 gerações por disparo, com pausa entre elas (anti-robô; Jorge, 2026-10-21), em quantas sessões o plano pedir, com ≥ 2 GB livres e nada renderizando; 1K "tamanho original" é 0 crédito. O 2K "aprimorado" pode custar (manual do motor l. 198): no 1º download em 2K, conferir o saldo antes e depois e registrar aqui ("0 crédito, conferido em AAAA-MM-DD" ou o custo); 2K só onde o zoom passa de 1,5×. `diretor-de-arte` escolhe (`04_broll/ia_flow/escolhas.json`); `recorte-chroma.mjs --pb --aparar [--choke]`, só nas stills aprovadas. Piloto: 7 recortes novos, 0 crédito | **⏸** folha numerada; aprovação por número antes da montagem (gbro; PAPER VOX) |
| 6 Recorte da cabeça | sequência WebP da pessoa (`04_broll/recortes/<nome>/q0001.webp…`) + `04_broll/recortes/<nome>.json` | `recortar.mjs` (só a moldura: a abertura não tem recorte), pela fila e **só com o cache**: PowerShell `$env:npm_config_offline='true'; node scripts/vez.mjs node scripts/recortar.mjs <proj> <ini> <fim> <nome>`; bash `npm_config_offline=true node scripts/vez.mjs node scripts/recortar.mjs …`. O script chama `npx -y hyperframes` sem versão (l. 38): online, o npx baixaria sozinho uma versão nova (download sem ⏸, e a CLI ou o modelo podem mudar o recorte). Se falhar por falta de pacote ou modelo: ⏸ com fonte e tamanho antes de liberar a rede (plano B: moldura sem recorte). Ele imprime o JSON do recorte (`arquivo`, `brutoIni`, `brutoFim`, `fps`) mas não grava: grave à mão em `04_broll/recortes/<nome>.json`, que o gerador lê (piloto: `cabeca1.json` e `cabeca2.json`, 115 + 137 quadros em 183 + 200 s) | — |
| 7 Montagem | `03_roteiro/vox.json` + `plano-de-batidas.md` regravado (o registro do que se montou) | modo gerador: `03_roteiro/montar_<slug>.mjs`, cópia adaptada do `montar_creatina.mjs` do piloto (78 KB para 112 s), sobre `scripts/lib/vox.mjs` + `scripts/lib/vox-mural.mjs`; composição `VoxBroll`. `validar-vox.mjs` até 0 ERRO; `refinar-sfx.mjs <proj> --props 03_roteiro/vox.json` (só a tabela) até "Avisos: nenhum" | — |
| 8 Prévia | meia resolução, uma por trilha, + a base sem trilha | `node scripts/vez.mjs node scripts/render-vox.mjs <proj> --previa --manter-base` (não medida; o final do piloto levou 5,6 s/s). Folha da prévia pelo ffmpeg no MP4 (`-ss <t> -i previa.mp4 -frames:v 1` por instante + `xstack`) e brilho quadro a quadro (YAVG); `revisor-de-video`. Ajuste pontual: gerador → `--trecho a b`. Área segura num instante sem render: `scripts/lab/quadros-lab.mjs <proj> --props 03_roteiro/vox.json --comp ConferenciaReels <t>` (a VoxBroll com a interface do Reels por cima; ferramenta do lab, pela fila) | **⏸** |
| 9 Refino dos SFX | `sfx_refino.md` + carretel de audição | `refinar-sfx.mjs <proj> --props 03_roteiro/vox.json --video <prévia com trilha>` (lê o `vox.json`: 28 SFX e 0 aviso no piloto). O Jorge pede por número ("o 7 entra 2 quadros antes") → `{ajuste: -83}` como 5º item da linha do `PLANO_SFX` (o `planejarSfx` aplica) → gerador → `mixar-audio.mjs <proj> --video <base> --props 03_roteiro/vox.json --trilha <X> --saida <caminho absoluto>` (segundos, sem render) → carretel novo | **⏸** (Decisões 2026-10-20) |
| 10 Final | `07_final/<proj>_final.mp4` | `node scripts/vez.mjs node scripts/render-vox.mjs <proj>`, com o tempo estimado antes: resolução cheia, concurrency 1, sem angle, ~5,6 s/s + ~75 s de mixagem (piloto: 626 s para 112,3 s). Depois: folha de quadros, YAVG (Y < 10 só no preto final) e loudness (−14 LUFS, pico ≤ −1 dB) | **⏸** render longo |
| 11 Fechamento | legenda do post e registro | `legendista`; `Publicados.md`; as stills do Flow para a `%SOUTO_VIDEO_PROJETOS%/_biblioteca` (etapa 8 do `/editar`) | ⏸ publicar |

**Bruto do piloto** (pergunta 7, resolvida): a creatina, na versão corrigida pelo Jorge em 2026-10-29: `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/01_bruto/bruto.mp4` (112,3 s, 1080×1920, 24 fps, H.264; `02_analise/meta.json` já aponta para ele), já transcrito em `02_analise/`, com as decisões de texto em `03_roteiro/checagem-texto-tela.md` (as correções de transcrição listadas lá entram na etapa 2). Já está no formato de saída: pula o `preparar.mjs` e o bruto de trabalho, e o recorte da moldura roda direto nele. Só o quadro-chave fica a cada 6,25 s (18 no vídeo; o `preparar.mjs` põe a cada ~1 s, e o `normalizar-broll.mjs` existe porque arquivo com poucos quadros-chave estoura o render com "Timeout while extracting frame"): na vitrine e no piloto, nem busca lenta nem esse erro. Se um bruto novo der um dos dois, regravar só o GOP, pela fila, sem mudar tamanho, fps nem cor (`ffmpeg -i bruto.mp4 -c:v libx264 -crf 16 -pix_fmt yuv420p -g 24 -c:a copy bruto_g24.mp4`) (proposta).

**Checagens antes da prévia e do final**
- `validar-vox.mjs` (ERRO trava; AVISO vai para o relatório; a lista exata fica no cabeçalho do script): espinha (com o par extra acima de 60 s e o ato 2 acima de 75 s); piso do movimento (rajada, densidade mínima, trocas/s, plano médio, overshoot inclusive nas chaves de câmera); travas de SFX; "%" e "vezes" sem o absoluto; texto no resquício; card da moldura sobre o texto de outro card ou fora da faixa dele; texto ou cartão da abertura sobre o rosto; **toda legenda e todo texto na faixa segura, com a largura da tinta e o pico da entrada (carimbo, escala)** (porte da ideia do `camcheck` do lemo, MIT; estimativa por letra, ver "Legenda"); tempo de leitura dos cards; imagem repetida; arquivo que não existe. Sem teto de stills (calibração original, 2026-10-29). Piloto: 0 ERRO e 6 AVISO (troca dentro da frase, um `ele` de 6,4 s, um split de 6,3 s, leitura de 3 cards um pouco curta).
- Ficam com o agente e o `checador-de-afirmacoes`, não com o script: sincronia de 0–2 q; receita repetida em seguida; texto de tela só da fala, fora os cards de contexto da moldura e o card "Obs." (esses levam no plano a fonte da Ficha ou do kit de fontes); palavras vetadas (PAPER VOX).
- Depois do render: brilho médio quadro a quadro (`signalstats` YAVG), nenhum quadro com Y < 10 fora de escuro de propósito (TD2; no piloto, só os 2 quadros do preto final); 1º e último quadro de cada animação ao lado do still aprovado, numa folha do ffmpeg (gbro); loudness; relatório de ritmo só se for portado (opcional).
- **Mexeu no motor?** As 6 regressões, de dentro de `motor`, uma por vez: `regressao.mjs` (TELA DIVIDIDA clássico, IDÊNTICO), `regressao.mjs --cut` e, pela fila, `regressao.mjs --mix`, `regressao.mjs --td2`, `regressao-paper-vox.mjs` e `regressao-vox.mjs` (EQUIVALENTE com PSNR ≥ 45 dB a 135×240, contra 3 trechos do final aprovado do piloto). A do VOX é obrigatória depois de qualquer mudança em `src/modelos/vox/`, `src/kit/`, `src/legendas.ts`, `Root.tsx`, `scripts/render-vox.mjs` ou pacotes (só o vídeo se compara). Mudou `scripts/lib/vox.mjs` ou `vox-mural.mjs`? Confira também que o gerador do piloto grava o mesmo `vox.json`: `node %SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/03_roteiro/montar_creatina.mjs --saida <arquivo no scratchpad>` e compare o md5 com o `03_roteiro/vox.json` (nunca sem `--saida`: grava em cima do piloto).

## Kit de peças
Custo de render (estimativa do rascunho; os números medidos vêm logo abaixo): **baixo** = transformações CSS; **médio** = máscara, traço SVG, vários palcos; **alto** = desfoque de camada grande ou motion blur. Base medida:
- PAPER VOX: 0,3–0,5 s/quadro parado e 1,2–1,45 s/quadro com motion blur; prévia 3,2–4,2 s/s, final 12,4 s/s. **Medidos com `--gl=angle`**, e a VOX renderiza sem ele.
- TD2: prévia de meia resolução 4,4–6,0 s/s; o desfoque do vidro levou a 8,8 s/s e o B-roll composto (de onde sai o `Recorte` copiado) a 9,5 s/s, as duas em meia resolução; **final 16,0 s/s** (2639 s para 164,7 s; `05_LAB/td2/previas/render_final.log`). Razão final/prévia medida: 3,0 (PAPER VOX) a 3,6 (TD2).
- Recorte da pessoa: **1,3 s/quadro só em 1080×1920** (~31 s por segundo); 4K, 4,4–5,4 s/quadro (manual do motor l. 156, 300 e 312); 1440×2560 (a 1ª versão da creatina), ≈ 2 s/quadro pela área (estimativa). Por isso o bruto de trabalho em 1080×1920 (Pipeline, etapa 0); a creatina corrigida já vem nesse tamanho. Só a moldura usa recorte (calibração original, 2026-10-29: abertura sem recorte).
- **Medido no piloto** (creatina, 112,3 s, aprovado em 2026-10-30; resolução cheia, `--concurrency 1`, sem angle, ~1,3 GB livres; o `render-vox.mjs` é o mesmo render): **626 s = 5,6 s/s**, + ~75 s do `mixar-audio --final`. Vale no lugar das estimativas deste guia e da vitrine.
  - Por bloco: **moldura 1, 14,2 s/s** (o pior caso: cabeça recortada + fundo desfocado + cards); mural 6,7–7,1; invasão 4,9; split 2,7–3,1; ele e fecho ~2.
  - Recorte da cabeça: 115 + 137 quadros em 183 + 200 s (~1,5 s/quadro, só do cache).
  - Para os próximos, a estimativa de ponta a ponta é de ~2–3 h de máquina (Decisões 2026-10-30).
- **Medido na vitrine** (2026-10-29, aprovada pelo Jorge; `05_LAB/formatos/5-paper-vox-broll/previas/vitrine_v1_2026-10-29.mp4` e `.tempos.json`).
  - **Final** (resolução cheia, `--concurrency 1`, sem angle, `scripts/lab/render-medido.mjs`, de onde nasceu o `render-vox.mjs`): **6,1–7,1 s/s**. Por bloco:
    - moldura 8,7 s/s, o **pior caso**;
    - mural 5,9 (quadros do mergulho com blur até 1,5 s);
    - invasão 5,0; split 3,4; ele e fecho ~2;
    - abertura 7,7: só o 1º quadro, que abre o navegador, leva 9,5 s.
  - Projeção para a creatina (112 s): 12–16 min de final (deu 10,4 min de render).
  - **Recorte da cabeça** em 1080×1920: 0,8 s/quadro (76 q em 147 s, só do cache).
  - O `<Video>` com quadro-chave a cada 6,25 s não deu Timeout e bate quadro a quadro com o bruto.
  - Leitor da sequência WebP: quadro mais próximo (`round`), não `floor`: o `brutoIni` impresso vem arredondado, e o `floor` deixava a cabeça 1 quadro atrás do rosto nas emendas do bruto.

| Prio | Peça | O que faz | Ref | Origem | Custo |
|---|---|---|---|---|---|
| P0 | `VoxBroll` | Composição: blocos, um `<Video>` do rosto, trocas de layout sem opacidade, legenda, áudio | ref-09; TD2 | copiar `TelaDividida2.tsx` e adaptar | base do TD2 |
| P0 | `Palco` | Mundo da animação com câmera, 3 planos e motion blur, num retângulo (tela cheia, painel 1080×960, fundo da moldura). Recebe `W` e `H` por prop e os repassa a `transformPlano`, `visivel` e `velocidadeTela` (no PAPER VOX vêm do `useVideoConfig()`, 1080×1920: no painel, a câmera centraria em y 960, a borda de baixo). `Acabamento` (vinheta, poço de luz, grão) só dentro do retângulo do palco; rosto e recorte da pessoa sempre fora do `BlurMovimento` (seriam decodificados uma vez por amostra, até 8) | ref-09; ref-08 | copiar `PaperVox.tsx` (`Mundo`, `BlurMovimento`), `camera.ts` (sem o `snap`), `elementos.tsx`, `texturas.ts`, `tipos.ts` | médio–alto |
| P0 | `LegendaVox` | legenda pequena (calibração original, 2026-10-29): 1–3 palavras, branca, posição por layout, encolhe até caber; caixa cinza #81817A só sobre fundo claro | ref-09 §12; área segura | nova, com os blocos do `montarBlocos` (`src/legendas.ts`, importar); a `LegendaB` do TD2 não entra | baixo |
| P0 | `TextoDigitado` + `CartaoAba` | abertura: texto serifado digitado 2–3 letras por passo, fora do rosto; cartão azul elétrico que abre como aba em 0,17 s e acende na palavra; os dois saem juntos em dissolve + desfoque de 0,20 s | ref-09 §5.1; Jorge 2026-10-29 | nova (a digitação do `TextoNaCena`, fora do palco) | baixo |
| P0 | Entradas VOX | `voa` 0,30 s, carimbo, sobe da borda, monta/desmonta, sem overshoot | ref-08; ref-09 | estender a cópia do `elementos.tsx` | baixo |
| P0 | `SplitSobe` + trocas do painel | painel que sobe; chicote com sobra na borda | ref-09; TD2 | `entra`/`sai` do TD2 (copiar) + nova | baixo |
| P0 | `PapelInvade` | papel amassado come a tela e estoura | ref-08 | nova (máscara orgânica; textura procedural ou still do Flow) | médio |
| P0 | `TextoNaCena` | texto preso ao mundo, digitado em passos, em pedaços | ref-09 | nova (texto HTML no `Palco`) | baixo |
| P0 | `Anotacao` | seta, sublinhado, coroa, riscos, brilho ✦ | ref-09 | copiar `traco` (PAPER VOX) + formas novas | baixo |
| P0 | `validar-vox.mjs` | piso do movimento e área segura, lendo as props | ref-09; área segura; lemo | nasceu em `scripts/lab/`; hoje `scripts/validar-vox.mjs` | 0 |
| P0 | `Resquicio` (versão barata) | foco por grupo: a cena A escurece 20–30% e troca, por opacidade, para a cópia pré-desfocada de cada still (ffmpeg 1 vez: `gblur=sigma=5,colorchannelmixer=rr=0.75:gg=0.75:bb=0.75`); desfoque por quadro só se a vitrine aguentar. Sem ele, a 1ª vitrine sai sem a marca do mural | ref-09; Jorge | nova, sobre a câmera do PAPER VOX | baixo (por quadro: alto, medir) |
| P0 | `Mergulho` | estação nova dentro de uma parte da anterior (k 0,35–0,5); a câmera entra por `recursao` sem overshoot e para em 0,8–0,9/k, com o resquício no canto | Jorge 2026-10-29; PAPER VOX (E12 no celular, k 0,42); ref-09 (garagem) | chaves do `camera.ts` copiado + `ctx(id, base, k)` do `criarMural` (`scripts/lib/mural.mjs` l. 229, copiar) | médio |
| P0 | `lib/vox.mjs` + `lib/vox-mural.mjs` (no lab, `vox-lib.mjs` e `vox-mural.mjs`) | lógica comum dos geradores; âncoras, câmera sem overshoot, estação em escala k (mergulho) e `voaBoia` sem `delete el.passo`, com vários palcos; desde 2026-10-30, também a largura da etiqueta (`larguraEtiqueta`), o plano de SFX com a escolha reaproveitada (`planejarSfx`) e o `--saida` do `gravar` | PAPER VOX | copiar de `scripts/lib/mural.mjs` + importar os exports puros | 0 |
| P1 | `MolduraPessoa` (+ cabeça vazando, decidida) | moldura de baixo + matte da cabeça (o único recorte da pessoa no vídeo) | ref-08 | nova + sequência WebP do `recortar.mjs` (leitor do `Recortado`) | recorte em 1080×1920: 10 s ≈ 5 min |
| P1 | `FaixasEmpilhadas` + `EncolheEmIcone` | 3 faixas com relógio próprio, só em tela cheia; saída num ícone em 0,33 s | ref-08 | nova | médio (3 palcos) |
| P1 | `CartaoQueCai` + `CardsContexto` | prendedores + queda de 1,6 s, −6° → 0°; cards de contexto que se sobrepõem entre si e à cena, com informação da Ficha ou do kit de fontes, sem cobrir o texto de outro card, o rosto nem a legenda | ref-08; Jorge 2026-10-29 | nova | baixo |
| P1 | `TrocaCamada` | troca de fundo, de sujeito, painéis de papel, porta | ref-09 | nova | baixo |
| P1 | `MaoQueEntra` + `Pendulo` | mão pela borda em 0,1 s; pêndulo amortecido | ref-09 | nova | baixo |
| P1 | `EmpurraEstoura` + puxada seca | empurra ×1,8 + estouro; 2× → 1× em 0,17 s | ref-08; ref-09 | nova (chaves de câmera) | médio |
| P1 | `readcheck` + `ritmo` (opcional) | tempo de leitura; energia e cortes do vídeo | lemo | portar a lógica para `scripts/lab/`, com aviso MIT; ⏸ antes (tarefa grande, não pedida) | 0 / 1 leitura |
| P2 | `IconeHolograma` | ícone no peito com varredura, 0,6 s | ref-09 | nova | baixo |
| P2 | `Travelling` + `PecaQueSolta` | 1º plano desfocado cruzando; roda que salta e voa | ref-09 | nova | médio |
| P2 | `Reticula` + wipe de pontos | passo 20–26 px, 2–3 camadas; wipe em 0,44 s | lemo; ref-08 | nova | médio |
| P2 | `FaixaCarmim` | faixa de ~260 px a 72° varrendo em 0,25 s | lemo | nova | baixo |
| P2 | `rescheck` | px da fonte por px da tela no zoom (≤ 1,5×) | lemo | portar, com aviso MIT | 0 |
| P2 | `Split6040`, `Contador` "X em cada 10" | variantes | ref-09; v1 | `contador` do kit (adaptar) | baixo |
| P2 | `InterfacePalco`, `AnelOrbital`, `TintaMascara`, `PageTurn` | receitas R4–R7 | v1 | objetos do PAPER VOX (`celular`, `lista`, `folhas`, `spot`; copiar) ou nova | baixo–médio |

- **O que se copiou de cada lugar** (registro de como o kit nasceu no lab, 2026-10-29; só leitura nos originais, a cópia está em `src/modelos/vox/`):
  - TD2: `TelaDividida2.tsx` (`calcularTD2`, rosto por layout, `entra`/`sai`/`entraQuadro`, `FioMascara`, `mascaraEmenda`, `CardTexto`, arredondamento `q()`; **sem** o ducking da trilha e sem o `sfxAuto`, porque a VOX não toca música); `SplitCompostoTD2.tsx` (`Recorte`, foco do fundo no 1º pouso). A `LegendaB` do `VidroTD2.tsx` não entra (a legenda é a pequena; Jorge, 2026-10-29). Leitor da pessoa recortada (moldura): o `Recortado` de `src/modelos/MotorCamadas.tsx` (só a parte do `<Img>` da sequência WebP).
  - PAPER VOX: `camera.ts` (sem o `snap`, que tem overshoot); `PaperVox.tsx` (`Mundo` com `camada()`, texto sempre por cima; `BlurMovimento`; `Acabamento`; `visivel`); `elementos.tsx` (`ElementoView`, entradas, `boiar`, `tempoPasso`, `COR`, `DEGRADES`); `texturas.ts`; só os objetos usados de `objetos.tsx` (componente + linha do `MAPA`); `tipos.ts` como base.
  - Kit e motor (importar): `kit/tempo.ts`, `kit/Grao.tsx`, `kit/fontes.ts`, `legendas.ts`. Copiar e adaptar: `kit/pecas/palavra-impacto.tsx` (só a palavra gigante por cima, da R5; sem recorte), `contador.tsx`.
  - Scripts (rodar, não editar): `recortar.mjs`, `recorte-chroma.mjs`, `alinhar-palavras.mjs`, `mixar-audio.mjs`, `refinar-sfx.mjs`, `vez.mjs`; do lab: `render-lab.mjs`, `stills-lab.mjs`.
- **Total medido** (substitui a estimativa do rascunho, que previa final de 20–35 s/s): final 5,6 s/s no piloto (acima); recorte da pessoa só na moldura (a abertura não tem; Jorge, 2026-10-29), ~1,5 s/quadro em 1080×1920; num bruto 4K sem bruto de trabalho, 3–4× mais. Tudo pela fila, um por vez.
- **Plano B do desfoque** (aciona se um render passar de 12 s/s fora da moldura; a moldura 1 do piloto deu 14,2 s/s e ficou assim): (a) resquício pela cópia pré-desfocada do still (acima), sem blur por quadro; (b) fundo da moldura = clipe curto pré-renderizado da última estação (`render-lab --trecho`, 12 fps), desfocado no ffmpeg e lido como `<Video>`, como os B-rolls do TD2; (c) na prévia, `blur: {ativo: true, maxAmostras: 4, limiar: 30}` (props do `PaperVox.tsx`), ou câmera a 12 fps sem motion blur. Para comparar: só o desfoque de fundo do vidro levou o TD2 a 8,8 s/s em meia resolução.

### gbro e lemo
| Repositório | O que entrou | Como | Licença |
|---|---|---|---|
| `pyang5166/gbro-collage-broll` (a1a4ee2) | Ficha de metáfora; aprovação por número (lá são 2 aprovações; a 3ª, da prévia, é nossa); esquema por elemento; ordem de montagem; "monta do vazio e trava, sem fade"; still em 3–6 grupos separáveis + lista de proibições do prompt; metáforas em sequência; conferência do 1º e do último quadro | **Só ideia** (método reescrito). Nenhum código: exige Python, Codex e chave paga, o modelo padrão foi desligado em 2026-10-22 e entrega MP4 chapado, sem camadas e com câmera travada | MIT © 2026 狗哥笔记. Frase copiada do template de prompt ou do esquema JSON = aviso no `05_LAB/LICENCAS.md` (ainda não está lá) |
| `lemomo-ai/lemo-opuscar` | Números de texto cinético, carimbo, troca de layout, câmera log, níveis de zoom, B-roll explicativo, linguagem da certeza, transições de colagem, "0,1–0,15 s antes do corte", checklist de direção, som por ação (o grão no encode ficou de fora: pegaria o rosto) | **Só ideia** (números parafraseados). Não instalar: motor próprio, áudio em Python, Windows só por WSL | MIT © 2026 LemoLab (código e docs); demos em CC BY 4.0, não usados |
| `lemomo-ai/lemo-opuscar` | `readcheck`, `camcheck`, `rescheck`, `rhythm_report` | **Receita a portar** para Node em `scripts/lab/` (ainda não feito): a ideia do `camcheck` entra no `validar-vox`; as outras 3 são opcionais, com ⏸ antes | MIT: aviso no arquivo portado e no `LICENCAS.md` |
- Nada foi clonado, instalado ou baixado.

## Armadilhas (aprendidas nos outros formatos, na vitrine e no piloto)
1. `--gl=angle` + `<Video>` dentro de `Sequence` = "Timeout while extracting frame" (TD2). Render sem angle.
2. Troca de layout por opacidade faz o quadro nascer do preto (TD2 v1: 22 trocas). Só desfoque e zoom.
3. A cena do quadro usa o mesmo arredondamento das `Sequence`; por tempo, a fronteira escapa 1 quadro e sai metade preta (TD2).
4. Degradê da palavra-chave (texto da cena) com `background-clip: text` só no nó do texto, com folga em cima para o acento (TD2: "DESNUTRIÇAO").
5. Objeto na mão some no recorte da pessoa (CUT): moldura sem objeto na mão (a abertura não tem recorte).
6. Cor do chroma medida nos cantos (vem ~#0035FF); objeto fino pede `--choke` (PAPER VOX).
7. "Baixar lote" do Flow entrega 1K: a escolhida se baixa em 2K "aprimorada" (PAPER VOX), que pode custar crédito (manual do motor l. 198): conferir o saldo antes e depois no 1º download; 1K onde não há zoom.
8. Não operar o Flow com render rodando nem com menos de 2 GB livres: o Chrome trava (PAPER VOX; memória "flow-limites").
9. O `recortar.mjs` entrega sequência WebP, não `.webm`: `OffthreadVideo` falha com "No frame found at position" (o manual do motor, l. 156 e 179, ainda fala em `.webm`).
10. `npx -y hyperframes` sem versão (no `recortar.mjs`) baixa sozinho quando há versão nova: rodar com `npm_config_offline=true`.
11. O `snap` do `camera.ts` do PAPER VOX passa ~6,6% do alvo: na cópia da VOX, trocar a curva.
12. Recorte na resolução nativa: em 4K custa 3–4× mais que em 1080×1920; gerar o bruto de trabalho antes.
13. O leitor da sequência WebP da moldura usa o quadro mais próximo (`round`), não `floor`: o `brutoIni` impresso pelo `recortar.mjs` vem arredondado, e o `floor` deixava a cabeça 1 quadro atrás do rosto nas emendas do bruto (o Jorge pegou na vitrine, 15,6 s). O `Recortado` do CUT (`MotorCamadas.tsx`) usa a mesma conta com `floor`: risco anotado, não mexido.
14. O `criarSfx` (`lib/mural.mjs`) lista e mede o banco inteiro a cada escolha: no piloto, a 1ª rodada do gerador passou de 1 h com pouca RAM. Use o `planejarSfx` do `lib/vox.mjs`, que reaproveita a escolha do `vox.json` anterior quando o evento é o mesmo (a rodada caiu para ~3 min).
15. Fim padrão das peças no validador: `?? Infinity`, não `?? 99` (com 99, em vídeo acima de 99 s, todo painel contava 0 elemento).
16. A folga da etiqueta é 1,4 × a letra (`larguraEtiqueta`), não um número fixo de px de mundo: 70 px viravam 800 px de tela no mural, com o zoom de 11× da 4ª estação.
17. O `recortar.mjs` imprime o JSON do recorte, mas não grava: grave à mão em `04_broll/recortes/<nome>.json`.
18. O `mixar-audio.mjs` resolve `--saida` a partir da pasta do projeto: passe o caminho absoluto (o `render-vox.mjs` já passa).
19. Bruto sem pausa: o `alinhar-palavras.mjs` no padrão corta trechos longos demais; com `--limiar -30 --min 0.15`, confira e conserte as palavras espremidas (Pipeline, etapa 2).

## Escolhas do Jorge (2026-10-29)
Respostas dele pelas folhas numeradas de `05_LAB/formatos/5-paper-vox-broll/perguntas/` (q1…q6; as opções são as de `perguntas.json`, que guarda cada escolha no campo `decisao`). Prints conferidos com ffprobe em 2026-10-29 (arquivo existe e o tempo cabe na duração do vídeo). Arquivos: refs em `05_LAB/referencias/videos/` (ref-08 50,1 s; ref-09 55,1 s); PAPER VOX = `%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece/07_final/2026-10-19_sociedade-que-adoece_final.mp4` (144,3 s); TD2 = `%SOUTO_VIDEO_PROJETOS%/2026-10-24_lv0-0929/07_final/2026-10-24_lv0-0929_final_td2.mp4` (164,7 s); CUT = `%SOUTO_VIDEO_PROJETOS%/2026-10-27_ecoar5377/07_final/2026-10-27_ecoar5377_final.mp4` (127,0 s); creatina = `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/01_bruto/bruto.mp4` (112,3 s, a versão corrigida; a 1ª tinha 118,9 s).

**Decididos sem pergunta (2026-10-29, com a fonte):**
- Look: C, foto-colagem com luz real (calibração original, 2026-10-28: a ref-09 é "o exemplo do tipo de colagem… que eu quero").
- Cabeça vazando na moldura: sim (o print dele é a cabeça vazando: "eu tô meio cortado no cenário"). Custo ≈ 5 min de recorte para 10 s, pela fila; plano B sem recorte.
- Emenda do split: esfumada, a do TD2 (Decisões 2026-10-27: "fica estiloso"), a do vídeo aprovado; a reta ficou sem comparar (pendente).

| # | Pergunta | Escolha (calibração original, 2026-10-29) | Onde entrou |
|---|---|---|---|
| 1 | Split: quantas animações em cima | **A** · uma por vez em 1080×960, trocando a cada ≤ 2 s por chicote ou troca de camada, no ritmo das 3 telas da ref-08 somadas; as 2 faixas empilhadas ficam fora (a sugestão "A com 1 trecho B" não entra) | `split`; R11; kit |
| 2 | Texto grande dos 2 primeiros segundos | **B** · texto serifado digitado fora do rosto + cartão azul elétrico que abre na palavra-chave, como o "LOOK AT THIS" + "Vox" da ref-09; sem recorte e sem palavra atrás da cabeça | `abertura`; texto cinético; movimento; Pipeline (etapa 7); kit; estimativas |
| 3 | 2ª invasão: onde a cena nova nasce | **A** · dentro de uma parte da anterior: a câmera mergulha nela, para antes de ela encher a tela e deixa o resquício (sem texto) no canto de cima | `mural`; movimento; kit |
| 4 | Onde entra a moldura de baixo | **A** · depois do mural, antes do 2º split, com a última cena do mural atrás dele: "podendo aparecer cards e informações sobrepostas e cards com informações complementando o contexto" | espinha; `moldura`; ética; validador; kit |
| 5 | Imagens do Flow por vídeo | **Nenhuma das 3, sem teto fixo:** "1 cenário e até quantos recortes forem necessários, lembre que precisamos de vários elementos para compor uma cena às vezes complexa mas bonita". Mandam a densidade mínima e a beleza; Flow devagar (1 ou 2 gerações por disparo, com pausa; Jorge, 2026-10-21), em quantas sessões precisar, sempre 0 crédito; o nº entra no ⏸ do plano | Ficha da animação; receitas; "De onde vem cada peça"; Pipeline (etapas 3, 5 e 6); validador |
| 6 | Legenda | **B** · pequena e discreta em tudo, como a ref-09: 1–3 palavras, branca, caixa cinza só sobre fundo claro, sempre na área segura; a palavra grande fica no texto da cena | "Legenda"; layouts; texto cinético; kit |
| 7 | Bruto do 1º teste | **A** · a creatina, na versão corrigida por ele em 2026-10-29 (112,3 s, 1080×1920, 24 fps, já transcrita; decisões de texto em `03_roteiro/checagem-texto-tela.md`) | Formato; Pipeline ("Bruto do 1º teste"); estimativas |

**Regras que continuam valendo, e como cada escolha encaixa nelas:**
- **Texto sempre por cima de imagem:** o card novo da moldura cobre só papel, foto ou borda do anterior, nunca o texto dele (ou o texto de baixo sai antes); texto e cartão da abertura saem antes de a invasão chegar neles.
- **Nada cobre o rosto:** texto e cartão da abertura ficam acima da cabeça e no peito (a posição do texto na ref-09 cairia na boca); cards da moldura nunca no rosto; no `ele`, a legenda fica abaixo do queixo (os 50% da ref-09 cairiam no queixo).
- **Nenhum texto na área morta nem cortado na borda:** no print da escolha 3 (PAPER VOX 28,6 s), o "horas" fica cortado no canto; aqui, o texto da cena anterior sai antes do mergulho. Na ref-09, o cartão vai a x 93%; aqui, x ≤ 850 quando passa de y 1000. Texto dos cards só em y 240–900.
- **Números e informação só da Ficha ou do kit de fontes:** os cards de contexto são texto fora da fala, como o card "Obs.": entram no plano com a fonte (⏸) e passam pelo `checador-de-afirmacoes`; a exceção à regra "texto de tela só da fala" do `validar-vox` vale só para eles e para o "Obs.".
- **O @ só no card final** (Decisões 2026-10-08): o cartão da abertura leva a palavra-chave do gancho, nunca um logo, como o "Vox" da ref-09.
- **Branco só sobre o azul elétrico** (PAPER VOX, Decisões 2026-10-20): segue no texto cinético; a legenda branca é a escolha explícita dele (B).
- **Sem teto × tempo de Flow e limite de uso:** o nº de stills e o tempo de Flow vão para o ⏸ do plano de batidas; a densidade mínima (≥ 10 elementos em tela cheia, ≥ 7 no painel) segue como AVISO no `validar-vox`.

**Item visual sem resposta não vira padrão:** o que se comparar lado a lado, ele escolhe (memória "cor do bruto intocável").

**Conferido na vitrine e no piloto:** queixo medido no bruto corrigido, com a legenda do `ele` por cima (x ≈ 553, topo ≈ 627, olhos ≈ 840, queixo ≈ 1008; ele anda ±25 px: o gerador guarda o rosto de cada trecho); texto e cartão da abertura em volta da cabeça; nitidez dos mergulhos seguidos do mural; busca do `<Video>` com o quadro-chave a cada 6,25 s; rosto do split com a interface do Reels por cima (`05_LAB/formatos/5-paper-vox-broll/previas/referencia-legenda-reels_2026-10-29.jpg`; no split, o queixo fica em 1470, acima da linha social).

**Pendentes (não medidos; o padrão é o do vídeo aprovado):** câmera da animação a 24 fps (padrão) × 12 fps (refs); emenda esfumada (padrão) × reta lado a lado; `--gl nenhum` (padrão) × `--gl angle`; `--concurrency 1` (padrão) × 2; moldura que sobe para virar o split (só se aprovada).
