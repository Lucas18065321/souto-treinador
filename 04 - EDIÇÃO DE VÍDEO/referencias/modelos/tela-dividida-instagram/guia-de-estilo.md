# Guia de estilo: tela dividida dinâmica e clean

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Mistura de duas referências (vídeos em `referencias/videos/`):
- **ref1 (tela dividida)**: Tommy Hilfiger, 90 s. Base da estrutura.
- **ref2 e ref3 (só o lado "DEPOIS/EDITADO")**: base da tipografia, das transições e do acabamento. Os lados "ANTES/BRUTO" são ignorados.

## Formato
- Vertical 9:16, 1080×1920, 30 fps.

## Layouts (nome no `edicao.json` → uso → % do tempo)
| Layout | Uso | % |
|---|---|---|
| `split`: B-roll em cima (50%), você embaixo (50%) | Sempre que a fala cita algo mostrável (pessoa, lugar, objeto, número) | ~55% |
| `card`: B-roll em tela cheia num card arredondado sobre fundo preto | História/ilustração, sem rosto | ~15% |
| `fala`: você em tela cheia, com punch-in alternando 100% e 112% | Frases de impacto, perguntas, viradas | ~25% |
| `texto`: card limpo, escuro ou claro, com a frase-chave (`*destaque*`) | Abertura de bloco, conceito central, CTA final | ~5% |

| `grafico`: barras animadas com contagem (dados de estudos, comparações) | Sempre que a fala citar números/percentuais | pontual |
| stop-motion (`sequencia` de imagens em split/card) | Ganchos visuais de "transformação" (ex.: mesa perdendo alimentos) | pontual |

- No `split` não há linha divisória: a **emenda é esfumaçada** (desde 2026-10-27, calibração original: "fica estiloso"). Fusão cruzada longa e sem bordas (3ª versão, depois de "o blur ficou muito duro" e "o mais suave e sem bordas de saída do efeito"): o rosto sobe 230 px por baixo da emenda (`ESFUMA_CIMA`, mesmo enquadramento) e o B-roll desce 190 px (`ESFUMA`) e some sobre ele em curva smootherstep. Sem faixa de desfoque (as bordas dela apareciam). Fixo do formato: não precisa de campo no `edicao.json`.
- A legenda fica exatamente na emenda enquanto a cena é `split`. **Quando o B-roll sai e corta para `fala`/`card`, a legenda desce junto no mesmo quadro** (2026-10-27: antes o bloco que começava no split ficava na emenda, no meio do rosto, como o "viraram" aos 22 s do vídeo de 24/10).
- Troca de layout a cada **2–5 s**; troca de B-roll dentro do `split` a cada **1,5–3 s**.

## Legenda
- Posição: na emenda do `split`; no terço inferior em `fala` e `card`; nenhuma no `texto`.
- Blocos de até 3 palavras / 18 caracteres, sincronizados palavra a palavra.
- Base: sans fina. **Palavra-chave**: fonte de destaque grande, ~1 a cada 1–2 frases (lista `destaques`).
- Entrada palavra a palavra: blur 8→0 px + subida de 10 px em ~200 ms. Saída: fade de ~130 ms.

## Fontes (decidido: campo `fonte` = `"A"` em todos os vídeos)
- **Destaque: Instrument Serif itálica.** Serifa editorial fina, a "assinatura" dos editores premium de Reels em 2025–26 e a mesma linha visual das referências.
- **Base: Inter Tight.** Sans neutra, compacta, ótima leitura no celular.
- Por que não as fontes "virais" (Montserrat Bold, Anton, Bebas): são o padrão do caption estilo Hormozi, chamativo e saturado. O nosso formato é dinâmico mas **clean**; o contraste vem da serifa itálica grande contra a sans pequena, não de caixa-alta pesada.
- As alternativas B/C/D continuam no motor (`src/fonts.ts`) só para testes pontuais.

## Transições (campo `transicao`: como a cena ENTRA)
| Nome | Duração | Quando | Som automático |
|---|---|---|---|
| `corte` | 0 | Padrão dentro do mesmo layout (~60%) | — |
| `blur` | 330 ms | Mudança de layout | `whoosh_soft` |
| `whip` | 230 ms | Mudança de assunto | `whoosh_fast` |
| `flash` | 300 ms | Viradas fortes (máx. 1–2 por vídeo) | `shimmer` |
| `glitch` | 200 ms | No máximo 1 vez por vídeo | `glitch` |
- Easing ease-in-out; transição sempre num respiro da fala, nunca no meio de uma palavra.

## Movimento contínuo
- Foto: Ken Burns de 10% (`movimento`: `in`, `out`, `esq`, `dir`). Vídeo de B-roll: 4%. Rosto: zoom leve contínuo.

## Cor e acabamento
- Contraste +8%, saturação −5%, leve calor (campo `cor`). Vinheta sutil e grão fino (`grao`, padrão 0.07).

## Abertura e fechamento
- Abertura (0–3 s): `split` com o B-roll mais forte + palavra-chave grande.
- Fechamento: `fala` → card `texto` com CTA.

## B-roll: sem repetição visual (diretriz do usuário)
- **Nunca repita o mesmo arquivo (nem variações quase idênticas) dentro de um vídeo.** Termos que voltam na fala ("doenças inflamatórias intestinais", "sintomas", "dieta"…) recebem **3 a 5 variações visuais diferentes** (ângulo, tipo de mídia — foto, vídeo, ilustração, 3D, gráfico — e composição).
- No plano, liste os termos recorrentes e quantas aparições cada um tem; prepare uma variação por aparição.
- Na biblioteca, catalogue as variações com as mesmas tags do termo, para que a próxima busca já traga várias opções.

## B-roll: ordem de preferência
1. **Seus arquivos** (`04_broll/meus`): sempre primeiro.
2. **Banco gratuito** (`04_broll/banco` e `fotos`): Pexels/Pixabay (vídeo), Openverse/Wikimedia (fotos). Créditos registrados em `04_broll/creditos.json`.
3. **Internet** (`04_broll/internet`): só material que você tem direito de usar (seu, licenciado, domínio público).
4. **IA no Google Flow** (`04_broll/ia_flow`): **desde 2026-10-27 é parte fixa de todo vídeo, não só exceção** (calibração original: "só fotos tá ficando meio batido"). Ver "B-roll gerado (Flow)" abaixo. Prompts em `03_roteiro/prompts_flow.md`.

## B-roll gerado (Flow): vídeos + imagens em todo vídeo (2026-10-27)
- **Vídeos animados** que exemplificam ou ilustram a fala, nos momentos de mais impacto (gancho, virada, mecanismo, analogia): ~1 a cada 20–25 s de vídeo (6–8 num vídeo de 2:45). **Geração única: x1, uma versão só** (Omni 1.1 Flash 720p 8 s = 12 créditos cada). O total de créditos continua indo no ⏸ do plano.
- **Mais imagens do Nano Banana** (0 crédito): autênticas, com apelo de gancho visual forte, no lugar das fotos de banco genéricas. Banco só quando servir de verdade.
- Prompts com gancho visual: ação, contraste, metáfora concreta, movimento de câmera; nada de foto parada "de banco".
- **Tudo o que for gerado (vídeo e imagem) entra na biblioteca** no fechamento, etiquetado (tema, tags, descrição, origem `flow`), como o material de banco, para reaproveitar em outros vídeos. **Nunca repetir nada dentro do mesmo vídeo.**

## Áudio
### Música
- Pixabay Music, escolhida por vídeo conforme o arco: tensão → construção → queda antes da virada → resolução.
- Ducking automático: `vol` com fala (padrão 0.10) e `volSemFala` (padrão 0.28); fade de entrada e de saída.

### Efeitos (pacote próprio em `sfx/biblioteca`)
| Efeito | Onde entra |
|---|---|
| `whoosh_soft`, `whoosh_fast`, `shimmer`, `glitch` | Automáticos nas transições |
| `pop_soft` | Automático em cada palavra-chave |
| `swish_air`, `click_soft`, `tick_micro`, `riser_short`, `impact_sub`, `reverse_swell` | Manuais (lista `sfx`), em momentos de storytelling |
- Regra: no máximo 1 efeito por evento visual; `impact_sub` no máximo 2–3 vezes por vídeo.
- **Desde 2026-10-19 (calibração original: "efeitos altos e repetitivos"):**
  - Os automáticos acima não tocam mais. O `scripts/sfx/sfx-variado.mjs` (etapa 5b do `/editar`) grava `"sfxAuto": false` e uma lista `sfx` com som sorteado por tipo de transição, sem repetição seguida.
  - Volume: ~12 dB abaixo da voz, com o pico no corte.
  - Clique variado só na 1ª vez de cada palavra-chave, com ≥ 5 s entre eles.
  - Os manuais da tabela continuam valendo e são renivelados (~11 dB abaixo da voz).
  - A composição `Edicao` não mudou.
