# Guia de estilo: INSTAGRAM - TELA DIVIDIDA (`tela-dividida-2-instagram`)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Nasceu no laboratório em 2026-10-27, a calibração original ("vamos melhorar esse modelo e deixá-lo mais viral"). Foi aprovado no mesmo dia no piloto de 24/10 ("excelente") e **substitui o Tela Dividida clássico no `/editar`**. O clássico (`tela-dividida-instagram`, composição `Edicao`) fica arquivado só para re-render de vídeos antigos e para a regressão.

- Composição: `TelaDividida2` (`motor/src/modelos/tela-dividida-2/`).
- Props: `03_roteiro/edicao.json` no tipo **`EdicaoTD2`** (`src/tipos.ts`).
- Render: `render.mjs` de sempre, **sem `--gl=angle`** (o `modelos.json` já diz `gl: null`).
- Piloto: `%SOUTO_VIDEO_PROJETOS%/2026-10-24_lv0-0929/03_roteiro/edicao_td2.json`, gerado por `05_LAB/td2/montar_td2.mjs`. Final em `07_final/2026-10-24_lv0-0929_final_td2.mp4`.

## Formato
- Vertical 9:16, 1080×1920, 24 fps. Tempos em segundos do bruto, que chega já decupado (saída = bruto, sem `montagem`).
- Cor do bruto intocável: o motor não aplica filtro de cor.

## Layouts (`layout` da cena)
| Layout | O que é | Quando |
|---|---|---|
| `split` | B-roll em cima + rosto embaixo, **emenda esfumaçada** (fusão longa e sem bordas; o rosto sobe 230 px por baixo e o B-roll desce 190 px) | A maior parte do vídeo (~55%) |
| `split` **composto** (`recortes`) | Fundo do Flow (vídeo ou imagem) + objetos recortados que **voam de fora em arco na palavra** e ficam **boiando**; o fundo ganha profundidade de campo quando o 1º pousa | Toda fala que cita um objeto concreto. É a assinatura do formato |
| `split` com `sequencia` | Stop-motion de imagens | Ganchos de "transformação" |
| `fala` | Rosto em tela cheia, `punch` 1 ou 1,15 alternando | Frases de impacto, perguntas, viradas |
| `vidro` | A tela inteira desfoca e escurece 30%, o Jorge segue falando ao fundo, e sobe um card **liquid glass** com o gráfico | Números de estudo (2–3 por vídeo: o desfoque pesa no render) |
| `tela` | B-roll em tela cheia (quebra de padrão); `giro` vira a imagem 180° na fala | Metáforas visuais ("de cabeça para baixo"), cenas fortes |
| `texto` | Card escuro com a frase-chave na fonte B | Conceito central, virada, CTA |

**Ritmo:** troca a cada 2–5 s. **Quebra de padrão** (`tela`, `texto` ou `vidro`) a cada 8–20 s; o validador avisa trecho com mais de 20 s sem nenhuma.

## Legenda (fonte B, aprovada em 2026-10-27)
- Apoio: Inter Tight 700, caixa alta, 48 px, creme.
- Palavra-chave: **Anton** caixa alta, 167 px (a do teste menos 15%, calibração original), nos **3 degradês da marca** em rodízio (névoa→azul elétrico, claro→aço, royal→azul claro), entrando com mola e leve giro.
  - Acentos das maiúsculas (Ã, Â, Á): até 2026-10-27 sumiam ("DESNUTRIÇAO" no piloto), porque o degradê só pintava dentro da caixa de 0,95 da letra. Corrigido no `LegendaB` (`VidroTD2.tsx`) com folga em cima e margem negativa: a palavra não mudou de lugar. O card de texto não tinha o problema.
- Posição: na emenda no `split`; y 1330 na `fala` e na `tela`; abaixo do card (y 1640) no `vidro`; nenhuma no `texto`. **Acompanha o layout do quadro**: quando o B-roll sai e corta para a fala, a legenda desce no mesmo quadro.
- `destaques`: palavra solta (o motor não destaca expressão). A palavra destaca em todas as ocorrências.

## Trocas (`transicao`: como a cena ENTRA)
| Troca | Dentro do split (só a metade de cima troca) | Troca de layout (o quadro inteiro) |
|---|---|---|
| `mascara` | cortina diagonal com fio de luz, 0,4 s | zoom + desfoque |
| `zoom` | a velha atravessa a câmera e a nova chega de longe, 0,36 s | zoom + desfoque |
| `chicote` | pan rápido com rastro, 0,3 s | deslocamento + desfoque |
| `blur` | desfoque cruzado, 0,32 s | desfoque + leve zoom |
| `flash` | clarão branco (viradas fortes, 1–2 por vídeo) | clarão branco |
| `corte` | seco | seco |
- **Nunca do preto:** a troca de layout entra só com desfoque e zoom, sem opacidade. A v1 do piloto nascia do preto em 22 trocas (o Jorge viu aos 0:22, 1:03 e 1:20).
- Rodízio sugerido entre splits: cortina, corte, zoom, chicote, corte.

## Flashes P&B (`flashes` no split)
- 1 a 3 imagens P&B de 0,15 s no começo da cena, com som de obturador. Ficam nos respiros e nas viradas ("Sendo que quando os cientistas…").
- São imagens do vídeo e entram na regra de não repetir.

## B-roll: gerado no Flow em todo vídeo (2026-10-27)
- **Vídeos do Flow** que ilustram a fala nos momentos de mais impacto: ~1 a cada 20–25 s, **x1, uma versão só** (Omni 1.1 Flash = 12 créditos). O total vai no ⏸ do plano.
- **Imagens do Nano Banana** (0 crédito) com gancho visual forte, no lugar de foto genérica de banco.
- **Recortes** (0 crédito): Flow com fundo azul `#0000FF` (1:1, "Studio product photo of …, isolated on a solid flat pure blue background (#0000FF), no shadow, no text") + `recorte-chroma.mjs --aparar`. Objeto branco sai levemente roxo: tire o tom com `hue=s=0.12` + `colorbalance`. Mínimo de recortes por vídeo: max(3, duração/20 s).
- **Recorte (`recortes[]`):**
  - `t` = início da palavra no `palavras.json` (o objeto voa ~0,15 s antes e pousa nela);
  - `x`, `y`: centro, com `y` medido na metade de cima, ≤ 0,72;
  - `tamanho`: 270–600 px;
  - `de`: esq, dir, baixo ou cima;
  - `rot`: inclinação final, ±4–12°.
- Tudo o que for gerado (vídeo, imagem, recorte) vai para a biblioteca, etiquetado. **Nada se repete dentro do mesmo vídeo.**

## Vidro (`grafico`)
- `titulo`: caixa alta.
- `subtitulo` (opcional).
- `barras`: rótulos com `\n`.
- Números em Anton contando **com decimais** (`casas`, padrão 1). O clássico arredondava 46,5 para 47.
- `destaqueEm`: segundos desde o início da cena; na palavra que compara, desenha o colchete e põe o selo "≈".
- `fonte`: rodapé de 26 px, obrigatório. Só números da Ficha; nenhum número novo.

## Áudio
- **Voz:** `voz` (tratada), ou o áudio do bruto. A pergunta do áudio continua no fim.
- **Trilha:**
  - `vol` com fala e `volSemFala` sem fala, com ducking;
  - regra de no máximo 1/4 da voz (Decisões de edição);
  - trilha mais curta que o vídeo: estenda com emenda no compasso.
- **SFX automáticos em rodízio** (nunca o mesmo seguido):
  - whoosh por tipo de troca;
  - pop variado no pouso de cada recorte;
  - obturador nos flashes.
  - `sfxAuto: false` desliga, e a lista `sfx` soma sons manuais. **Não rode o `sfx-variado.mjs`**: ele é do clássico.

## Conferência antes de mostrar ao Jorge
- `validar-edicao.mjs` em 0 ERRO (estrutura `EdicaoTD2` e as regras do formato).
- Depois do render: brilho médio quadro a quadro (`signalstats` YAVG); nenhum quadro com Y < 10 fora de um card escuro de propósito.

## Correções para os próximos vídeos (revisão do piloto, 2026-10-27)
Revisão do final de 24/10 pelo `revisor-de-video`. O Jorge pediu para valer nos próximos, sem re-renderizar o piloto ("só registre as correções para os próximos").
- **Acentos da palavra-chave** ("DESNUTRIÇAO", "MEDITERRANEO"): **corrigido no motor** (ver Legenda).
- **Pontuação no card de texto:** fica dentro dos asteriscos ("Quanto mais restrito, *melhor?*"). Fora deles ("*melhor*?"), o "?" cai sozinho numa 3ª linha. O validador avisa.
- **Palavra-chave do card com até 10 letras:** em Anton 200 px cada letra tem ~92 px. "COMPARTILHA" (11) ficou a 25 px da borda, junto dos botões do Reels; com até 10 letras sobra ≥ 60 px. O validador avisa.
  - Na frase comum, destaque uma palavra mais curta.
  - No CTA ("Segue @soutotreinador e *compartilha*"), não troque o texto. Na próxima edição, faça o motor encolher a palavra-chave do card até caber com 60 px de margem e **mostre na prévia ao Jorge** antes de fixar.
- **Legenda sobre `tela` clara:** a legenda creme some sobre fundo claro (0:25 do piloto, "GASTROINTESTINAIS"). Para `tela`, escolha imagem com a faixa da legenda (y ≈ 1200–1460) escura, ou ponha a frase em outra cena. Confira no quadro antes do render.
- **Legenda na boca/queixo nas falas com zoom 1,15** (0:06, 1:50, 2:18 do piloto):
  - A legenda fica em y 1330 nos dois zooms, mas no 1,15 o rosto cresce (origem 50% 30%) e o queixo desce ~110 px.
  - **Pendente no motor:** na próxima edição, proponha a posição nova (ex.: acompanhar o zoom, y ≈ 576 + 754 × zoom = 1443 no 1,15) e **mostre na prévia ao Jorge** antes de fixar. É decisão visual dele.
  - Depois de aprovada, regrave a referência da regressão `--td2` com o ok dele.
