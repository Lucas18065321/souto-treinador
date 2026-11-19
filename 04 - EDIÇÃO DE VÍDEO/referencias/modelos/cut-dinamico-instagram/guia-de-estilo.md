# Guia de estilo: INSTAGRAM - EDIÇÃO CUT DINÂMICO (rascunho)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Status: **v1 (05/10/2026)**, consolidada de 5 análises paralelas (ritmo, tipografia, motion, cor/marca, refs de apoio) e de uma crítica adversarial que conferiu as afirmações no vídeo a 30 fps (`analises/analise_*.md`, `analises/critica.md`). **A seção "Ajustes para nutrição e bruto 1080" prevalece sobre o resto do guia.** Referências em `videos/`:
- **ref496** (`ref496_principal-integral.mp4`, 33 s): é a **referência principal**. O conteúdo vai de 0 a 24,0 s. De 24,0 a 33,1 s é a vinheta da marca, que fica fora das métricas.
- **ref644**: a mesma edição dentro de uma vitrine de antes/depois. Ela é útil porque mostra o bruto: um único plano aberto e fixo. Todos os "ângulos" da edição são recortes digitais desse plano, com zoom de 1,3× a 3×.
- **ref274**: tela do Premiere filmada pelo celular. Serve de apoio para palavra gigante atrás da pessoa, 3D extrudado, tela tipográfica e cartão 3D.

Convenções:
- **q = quadro a 24 fps** (segundos × 24).
- Os tempos das refs estão em segundos da própria ref. A fonte é de 30 fps, então há erro de ±1 q.
- Os tempos do `edicao.json` são da SAÍDA, ou seja, depois da `montagem`.

Princípio:
- O dinamismo vem de **um elemento novo a cada ~4 q (mediana)** e da **câmera que nunca para**, não de B-roll. A pessoa fica em tela cheia ~70% do tempo.
- Para nutrição, a edição é dinâmica mas **clean** e legível, porque o público de saúde é mais velho. Não usar texto de cabeça para baixo, rabisco agressivo, tremida nem documento falso.

## Ajustes para nutrição e bruto 1080 (prevalecem sobre o resto)
Vindos da crítica adversarial e das preferências do usuário (dinâmico mas clean; autoridade de saúde precisa passar confiança).

**Quantidade**
- Momentos-assinatura: **6–8 por vídeo de ~110 s** (não 12–16). No gancho, 2–3 até 7 s; depois, 1 a cada 10–15 s.
- Depois dos 30 s: mediana de 8–12 q entre eventos (o gancho segue a ref: ≤ 5 q).
- Saídas especiais (chicote, estilhaço, voo): no máximo 2–3 por vídeo.
- Padrões de empilhamento: só 4 (`pilha`, `mae`, `etiqueta`, `larga`). Inclinação de 0–4° nas explicações; −6° a −12° só no gancho.

**Cortado ou limitado**
- Flash vermelho de tela cheia no meio do vídeo: **não usar** (agressivo e arriscado para fotossensíveis). A silhueta fica só na abertura, 1×.
- Mosaico de olhos e boca: **não usar** (estranho para autoridade de saúde e inviável em 1080).
- Rabisco "fervendo" e ornamento prata: **não usar**.
- Cena de IA fotorrealista: padrão 0. Se houver, ilustração gráfica, nunca foto falsa.
- P&B com pretos esmagados: no máximo 1×.
- Impacto (`palavra-impacto`, estilhaço) em termo médico soa sensacionalista: reservar para **números verificáveis**, com a peça `fonte` (rodapé "Fonte: revista, ano") quando for dado de estudo.
- Câmera: sem pan de 25% em 3–4 q, sem giro de 15°; punch-out de no máximo 12% em 5 q.

**Bruto 1080×1920 (o piloto SONO X IMUNIDADE é 1080)**
- Escala máxima 1,25. Variação de zoom por plano: 6–12%. Toda junção muda o zoom em pelo menos 8% **ou** entra `lente`.
- Close de 1,8–2× só com bruto 4K vertical (pedir exportação em 2160×3840 quando houver punch-in forte planejado).
- Com zoom 1,0 o `foco` não desloca nada: alternar o enquadramento só com zoom ≥ 1,08.

**Correções de medida**
- Silhueta de abertura: #9D0A00 (não o acento profundo). A do meio (#F7171F) não é usada.
- Marca: ícone completo em ~0,4 s (quadrado 0,13 s, lente 0,27 s, ponto 0,33 s); @ entra de 0,85 a 1,0 s. Card final: virada creme → gradiente em 6–12 q.
- Cartão (card dentro de card): sai com **chicote** (blur horizontal de ~2 q, sem mudar de escala), não com voo.
- Dolly da cena de IA da ref: ~2,5× no total.
- Impacto definido pela **largura** (70–85% do quadro), em 2 linhas ou com falsa condensada (`scaleX` 0,6–0,7): Inter Tight 900 não é condensada, e "IMUNIDADE" a 85% da largura só dá ~120–130 px de altura de maiúscula.
- Cor: 10º percentil de luma 25–50 nas falas (não 20–35); saturação 11–17 é do quadro inteiro, não da pele.
- Acento da ref medido: azul elétrico #1F33A3–#2E49CE. O tomate #D7311E é escolha nova, mais alaranjada (decisão do usuário).

**Exceções e peças que faltavam**
- Número traduzido ao lado da fala é permitido ("sete a oito horas" na voz + "7–8 h" gigante), exceção à regra "a mesma fala nunca aparece duas vezes".
- Peças novas: `fonte` (rodapé de fonte do dado), `contador` (número contando, para dado), `texto-curvo` (texto em curva parada acompanhando a cabeça, diferente do anel giratório), `objeto-3d` (adesivo com texto próprio, ex.: "MITO", "pH 7,4", nunca marca real).
- Orçamento de recorte (até 6 s), em ordem de prioridade: 1ª palavra atrás da cabeça no gancho → palavra gigante atrás no conceito central → neon atrás no fim.

**Adendos do Jorge (2026-10-22, obrigatórios em todo vídeo; prevalecem):**
- **Enquadramento:** rosto centralizado, cabeça inteira, pouca mesa. Equipamento de estúdio no topo pode aparecer. Plano base com o menor zoom que centraliza o rosto (estúdio de gravação original: ≈ 1,15) e closes a partir dele, até 2,0 com 4K.
- **1ª palavra do gancho SEMPRE atrás da cabeça**, centralizada no quadro (`x: 0.5`, regra fixa desde 2026-10-28). Meça a cabeça no quadro da própria cena (já com zoom e foco) e escolha só o `y` da `palavra-impacto` `plano: "atras"`: ela cruza o topo da cabeça e a cabeça cobre 10–30%. Mudou o enquadramento? Reajuste o `y`.
- **Centralização e texto inteiro (calibração original, 2026-10-28, regra fixa; o motor força e o validador dá ERRO):**
  - Toda palavra atrás da pessoa (`palavra-impacto` e `texto-3d` com `plano: "atras"`) fica no centro do quadro (`x: 0.5`). Símbolo solto de canto, como o "@" do vídeo do sal, fica fora da regra.
  - Todo `card-vidro` fica no centro do quadro. Sem lista, o texto é centralizado; com lista, o bloco fica no meio do card e os marcadores seguem alinhados.
  - **Ícone e título do card na mesma linha** (observação do Jorge no "mais um deles" do lipedema, onde o título caiu embaixo do bloco do ícone). O motor faz isso sozinho no CUT quando o card tem `icone` e `titulo` sem `rotulo`.
  - Nenhum texto sai da tela: palavra com no máximo 96% da largura e a ≥ 2% das bordas, card com ≤ 972 px. A legenda cinética encolhe a linha contando o recuo da `pilha` (a linha mais larga em 84% da largura, como sempre, e nenhuma linha, com o recuo, passa de 94%).
  - Origem: no vídeo do lipedema, o "NÃO EXISTE" foi para x 0,434, o texto do card ficou à esquerda e o "adipocitocinas" da 3ª linha da `pilha` saiu da tela.
- **Recortes de objetos como elemento gráfico** (`imagem` PNG sem fundo, do Flow com fundo azul ou de banco, com pop, órbita ou voo, perto do corpo): no mínimo **max(3, duração ÷ 20 s)** por vídeo (2 min → 6), complementando a fala nos planos de `fala`. Não substituem o B-roll, somam a ele. Nunca sobre o rosto nem sobre a legenda.
- **Rodízio de peças de informação (preferência, sem trava):** quando houver ensejo, alterne no mesmo vídeo `ficha-papel` (papel), `card-vidro` e `escala-ph` (liquid glass; a régua do SONO X IMUNIDADE pode virar régua ou índice de outros dados), `contador`, `grafico-barras`/`grafico-linha` e B-roll com objeto recortado animado. Não repita o mesmo tipo de card em seguida. O gosto fica com o editor: entra quando a fala pede.
- **Trava (`validar-edicao.mjs`, AVISO):** `abertura-atras` se nenhuma camada `plano: "atras"` começar nos primeiros 3 s; `recortes-objeto` se houver menos `imagem`/`orbita` que o mínimo acima. A altura da palavra em relação à cabeça não é medida pelo script: confira no `quadros.mjs`. **ERRO** (2026-10-28): `centro` (palavra atrás ou card fora de x 0.5) e `texto-cortado` (largura acima do limite).

## Formato
- Vertical 9:16, **1080×1920, 24 fps**. É a regra do Instagram, gravada em `modelos.json`; não subir.
- Composição `CutDinamico` (`MotorCamadas`), com `"modelo": "cut-dinamico-instagram"`. O render usa `--gl=angle`, que já está no `modelos.json`.
- Duração típica: 60–120 s. A ref tem 24 s, então as métricas abaixo valem por trecho.
- Marca depois da última fala: **no máximo 2,5 s**. A ref usa 9 s (27% do vídeo); não copiar.
- Áreas seguras do Reels:
  - texto entre y 10% e 75% (o impacto pode descer até 80%);
  - nada nos 18% de baixo;
  - nada na coluna de botões (x > 86%, y 55–90%).
- Bruto:
  - o ideal é câmera 4K vertical (2160×3840 depois do `preparar.mjs`), que permite closes de até 2×;
  - com bruto 1080×1920 (celular), a escala máxima é 1,25.

## Ritmo (regras mensuráveis)
Medido na ref496: 13 planos e 12 trocas em 24 s, e 100 eventos (palavra, objeto, efeito, corte ou movimento de câmera) em 24 s.

| Medida | ref496 | Alvo CUT |
|---|---|---|
| Duração do plano | 20–73 q; média 44 q (1,82 s); mediana 41 q | igual |
| Plano no gancho (0–7 s) | média 33 q (1,39 s); máx. 38 q | ≤ 38 q |
| Plano depois do gancho | 40–73 q (média 2,2 s) | 40–73 q. Em vídeo > 60 s, depois dos 30 s, até 84 q, só com câmera em movimento e bloco novo (adaptação, a validar no piloto) |
| Teto sem troca de plano | 73 q | 75 q (84 q na adaptação acima) |
| Intervalo entre eventos | mediana 4 q; p75 8 q; p90 14 q; máx. 27 q | mediana ≤ 5 q; p90 ≤ 15 q; lacuna máx. de 27 q, só com câmera em movimento |
| Densidade | 5,3/s (0–6 s), caindo para 3,5/s (18–24 s) | 5/s no gancho; 3,5–4/s até 30 s; 2,5–3,5/s depois |
| Momento-assinatura | a cada 2–4 s | a cada 2–4 s até ~15 s; depois, a cada 6–10 s |

- **Contas para um vídeo de ~110 s:** ~45–55 cenas, 12–16 momentos-assinatura, 6–10 palavras de impacto e 2–3 textos atrás da pessoa.
- **Arco de densidade:** o gancho concentra ~30% dos eventos, com planos curtos. Depois os planos alongam e o dinamismo passa para a câmera (zoom contínuo, degraus, dolly) e para animações longas (anel girando).
- **Todo corte zera o texto.** Nenhum bloco atravessa uma troca de cena. O bloco novo entra 0–4 q depois do corte (padrão: 2 q).
- **Toda junção da `montagem`** (corte de silêncio ou de tomada) **é troca de cena**: muda o enquadramento (zoom ou `foco` pelo menos 15% diferente) ou entra uma transição. Nunca jump cut no mesmo enquadramento.
- Corte de cena sempre em fim de palavra (`palavras.json`), alinhado ao grid de quadros.

## Layouts e camadas
| Layout (`cenas[].layout`) | Uso | % do tempo |
|---|---|---|
| `fala`: pessoa em tela cheia, em 3 tamanhos (aberto 1,0×; médio ~1,3×; close 1,8–2× com bruto 4K) | Padrão: gancho, frases de impacto, explicação | 65–75% |
| `fala` com `cartao` (card dentro de card; peça nova) | Frase de confiança ou autoridade | 1× por vídeo, ~40 q |
| `broll`: tela cheia com Ken Burns | Quando a fala cita algo mostrável; o bloco de texto continua por cima | 15–20%, planos de 36–72 q |
| `tela` com fundo `acentoProfundo` (papel rasgado, tela tipográfica) ou `escuro` (card final) | Número revelado, virada de bloco, encerramento | 5–10% (1–2 telas + card final) |

- **Por plano:** 1 bloco de texto + no máximo 1 objeto ou efeito (sem @ fixo: decisão de 2026-10-08).
- Até 3 camadas ao mesmo tempo só nos momentos-assinatura (vídeo + texto + objeto/efeito).
- No máximo 6 palavras na tela; 9 só no mosaico.
- Escolha o momento-assinatura pela função da frase (catálogo em "Motion e efeitos"). Cada tipo aparece 1× por vídeo; silhueta e P&B, até 2×; impacto e primeiro plano repetem conforme a tabela.

## Tipografia
Papéis fixos, todos com a fonte A (sem fonte nova):

| Papel | Fonte (`kit/fontes.ts`) | Cor | Tamanho em 1080×1920 | Uso |
|---|---|---|---|---|
| Voz | Inter Tight 500–600 (`base`) | creme #F2F4F8 | x-height 60–75 px (corpo ≈ 110–135 px; na Inter Tight, corpo ≈ 1,83 × x-height) | Toda palavra sem papel especial |
| Destaque | Inter Tight **900** (carregar; hoje o kit vai até 800) | acento | 1,2–1,6× a voz: x-height 75–90 px (corpo ≈ 135–165 px) | 1 por bloco (máx. 2), da lista `destaques` |
| Conector | Instrument Serif itálica (`serifa`) | creme a 90% ou cinza quente #BDB7AE | 0,6–0,8× a voz; altura de maiúscula 45–60 px | Artigo, preposição, pronome, verbo de ligação. 1 por bloco, encaixado no vão entre duas linhas |
| Impacto | Inter Tight 900 em caixa-alta, tracking −0,04em, altura de linha 0,85; `skewX` de −8° a −12° opcional | face no acento, extrusão creme para baixo e para a direita (3–6% da altura da letra), sombra escura | altura de maiúscula 200–460 px (3–6× a voz; corpo ≈ 275–630 px) | Número ou conceito central (peça `palavra-impacto`) |
| Ornamento | Instrument Serif itálica com gradiente #9A9A9A→#FFFFFF | prata | grande, atravessando 2 linhas | 1 por vídeo (ref "actually" 8,0–9,5) |
| Marca | Inter Tight 600 | creme a 92% | 40 px | @ só no card final (sem @ fixo desde 2026-10-08) |

- **"a" de um andar:** testar `fontFeatureSettings: '"cv11" 1'` na Inter Tight num quadro renderizado. Se a versão do Google não tiver o cv11, fica o "a" normal; não trocar de fonte por isso.
- **Sem Anton, Bebas, cursiva de pincel ou grunge.** A condensada de impacto da ref vira Inter Tight 900 em caixa-alta apertada, mantendo a identidade A já decidida.

### Empilhamento (padrões; parâmetro `padrao` da `legenda-cinetica`)
| Padrão | Como | Ref (s) |
|---|---|---|
| `pilha` | 3 linhas: voz 500 / conector encaixado / destaque 900 maior. Entrelinha de 0,72–0,85 (20–30% de sobreposição), inclinação de −6° a −12°, alinhada à esquerda com recuos de 4–10% da largura | "about/your/logo" 2,25; "that/you're/real" 11,6–12,4; "and/shown/consistently" 19,53 |
| `crescente` | Cresce para cima: 1ª palavra grande na base, as seguintes acima e menores | "They care about" 3,3–3,7 |
| `mae` | Apoio pequeno (voz + conector) sobre uma palavra de impacto | "They need PROOF" 17,07–17,5; "on a REBRAND" 6,5 |
| `larga` | Palavra de voz + destaque em caixa-alta larga, inclinada −8° | "Most BRANDS" 15,0–15,2 |
| `escada` | Linhas descendo em diagonal, cada uma 6–10% mais à direita. **Sem** virar espiral nem inverter | "gonna/hold/your" 0,23–0,5 |
| `etiqueta` | Palavra no acento dentro de uma barra creme, no meio da linha | "and [people] can" 13,6–14,85 |
| `arco` | Ver `texto-arco` | 0,2–1,83; 20,65–23,15 |

- Nunca repetir o mesmo padrão em blocos seguidos.
- `pilha` em até 40% dos blocos. `arco` e `etiqueta` contam como momentos-assinatura.
- Palavra na vertical: no máximo 1 por vídeo (a ref usa "this" em 1,17 e "spend" em 5,0) e nunca de cabeça para baixo.
- Posição do texto: perto do rosto e do tronco, sem cobrir o rosto.
  - Close: y 40–72%.
  - Médio: tronco, y 35–70%.
  - Aberto: arco acima da cabeça, y 10–18%.

### Animações (em q a 24 fps)
**Entradas:**
- **Palavra inteira (padrão):** fade de 2 q a partir de um "fantasma" (60% de opacidade, blur de 4 px).
- **Digitação:** 1 letra por quadro, cada letra com fade de 2 q. Em palavras de 6+ letras, em 1 de cada 2–3 blocos (ref "Nobody" 1,9–2,17; "clients" 9,87–10,13).
- **Slide com motion blur:** 3–4 q, vindo da esquerda (ref "ten" 5,70–5,83; "and" 19,53).
- **Conector:** revelação da esquerda para a direita em 3–4 q, com `clipPath: inset()` (ref "that" 13,4–13,57).
- **Destaque:** blur para nítido em 2–3 q.
  - Virada de creme para acento com clarão em 1–2 q, só 1–2× por vídeo (ref "logo" 2,5; "TRUST" 14,4).
- **Impacto:** letra a letra, a cada 1,5 q. Cada letra surge creme a 50% e vira acento em 2 q; a palavra fica completa em 6–9 q (ref "PROOF" 17,10–17,50).
- **Brilho de entrada** (glow creme de 8–15 px): só nas palavras principais, decaindo em 6–8 q.
- **Teto:** nunca fade acima de 4 q. O `titulo` atual leva ~8 q, com blur de 12 e cascata de 3 q a 30 fps: lento para o CUT.

**Saídas:**
- Padrão: o bloco morre no corte.
- Especiais, no máximo 1 a cada ~5 s:
  - chicote para a direita com motion blur, 8 q (ref 15,93–16,27);
  - estilhaço, 9–10 q (ref 16,23–16,6);
  - voo para a frente com escala 2× e blur, 7 q (ref 16,8–17,1);
  - desfoque junto com a câmera (ref 2,57–3,2);
  - empurrado para a borda pelo pan (ref 12,5–13,1).

**Acabamento:**
- Sombra em todo texto: `0 4px 10px rgba(0,0,0,.45)`.
- Extrusão só no papel de impacto.

## Legenda
- **No CUT, a legenda é a própria tipografia cinética.** Não há faixa no rodapé.
  - A peça `legenda-cinetica` gera os blocos a partir do `palavras.json` (já no tempo da saída), aplica os papéis e padrões acima e zera em cada troca de cena.
- **100% das palavras faladas aparecem** (a ref mostra ~85–99%). Ficam de fora só as muletas ("né", "tipo", "ah", "tá") e as repetições cortadas.
- **Blocos:**
  - 2–6 palavras (a ref vai de 2 a 9, média 4,4);
  - 24–60 q no ar (1,0–2,5 s);
  - 1 por plano; até 3 em plano longo, trocando com saída de 4–8 q.
- **Sincronismo:** cada palavra entra de 0 a +2 q do início falado (tolerância de −2 a +5 q).
  - Adiantar ou atrasar até 22 q só para fechar a frase antes do corte ou para cair num evento de câmera (ref 7,7–8,4 e 19,53).
- **Corrigir a transcrição antes da prévia é obrigatório** (`corrigir-palavras.mjs`), porque 100% da fala vira texto.
  - No piloto SONO X IMUNIDADE, o Whisper errou "chotezinho", "curco", "boi gene", "circarianos", "acidosia", "alcalóis" e "cascada".
- **Papéis automáticos:**
  - `destaques` define a palavra no acento de cada bloco (1 por bloco).
  - Os conectores saem de uma lista fixa: o/a/os/as, de/da/do, em/no/na, pra/para, com, que, e, um/uma, se, seu/sua, teu/tua.
- **A mesma fala nunca aparece duas vezes na tela.** Quando um `titulo` ou `palavra-impacto` repete a fala, o bloco cinético daquele trecho omite essas palavras.
- **Até a peça existir:** `legenda: true` (legenda padrão do motor, em y 0,74, blocos de 3 palavras) + `titulo` nos momentos-chave, com `semLegenda: true` nas cenas que eles cobrem.

## Texto atrás da pessoa e recortes
- **O recorte é a etapa mais cara.**
  - Custo: ~1,3 s por quadro em 1080×1920 (≈ 31 s de CPU por segundo de recorte); 2–7 s por quadro em 4K.
  - Orçamento: **até 6 s de recorte por vídeo** (≈ 144 q ≈ 3 min de CPU em 1080).
  - Nunca rodar em paralelo com render ou conversão.

| Uso | Duração | Vezes por vídeo | Ref (s) |
|---|---|---|---|
| 1ª palavra do gancho atrás da cabeça (acento, 900) | ~34 q | 1 | "I'm" 0,2–1,6 |
| Palavra gigante atrás (`palavra-impacto` com `plano: "atras"`, x 0.5, 80–85% da largura, y 12–38%) no conceito central do vídeo | 36–48 q | 1–2 | ref274 "MIDDLE" 10,5–12,0; "SO STOP POSTING" 22,0–22,5 |
| Silhueta (alfa do plano que entra) | 6–12 q | 2 | 0,000–0,200; 4,467–4,567 |
| Neon atrás da pessoa na última frase | ~20 q | 1 | 23,2–23,9 |

- **Fluxo:** `node scripts/recortar.mjs <proj> <brutoIni> <brutoFim> [nome]` e copiar a linha impressa para `recortes`. A camada `atras` precisa ficar dentro do intervalo do recorte.
- A cabeça cobre no máximo ~30% da palavra, numa letra que não muda a leitura (como o "m" de "I'm").
- Objeto na mão some no recorte, porque não é "humano". Escolha trechos sem objeto (por exemplo, sem a xícara de chá do gancho do piloto).
- Mosaico, P&B, cartão e anel de texto **não** precisam de recorte.

## Motion e efeitos (catálogo: quando usar)
| Efeito (peça) | Quando usar | Duração | Máx. por vídeo | Ref (s) |
|---|---|---|---|---|
| Flash de silhueta (`silhueta`) | Abertura e 1 virada forte do roteiro | 5 q (abertura: 2 no acento profundo + 3 brancos) ou 3 q (meio: 2 + 1) | 2 | 0,000–0,200; 4,467–4,567 |
| P&B seletivo com retícula (cena `pb`) | Frase de confronto (ex.: "tu tá perdendo teu tempo"). O texto no acento continua colorido | 14–20 q | 2 | 1,000–1,833; ref274 12,5–13,5 e 36,0–37,0 |
| Texto em arco ou anel (`texto-arco`) | Frase curta do gancho em volta do corpo; frase da solução ou CTA em anel 3D no fecho | 26–60 q, girando 20–40°/s | 2 | 0,2–1,83; 4,567–5,633; 20,65–23,15 |
| Palavra de impacto (`palavra-impacto`) | Número ou conceito central ("7 A 8 HORAS", "pH 7,4", "IMUNIDADE") | 15–36 q | 1 a cada 4–6 s no gancho; depois, 1 a cada 10–15 s | "PROOF" 17,10–17,95; "EVIDENCE" 10,03–11,45; "REBRAND" 6,53–7,15; ref274 "NEED" 5,0–5,5 |
| Caixa de seleção (`selecao`) | A palavra do mito que o público acha que importa ("detox", "alcalinizar") | 30–34 q | 2 | 1,83–3,2 |
| Etiqueta (`etiqueta`) | Palavra de confiança no meio da frase | ~30 q | 2 | 13,63–14,85 |
| Mosaico de recortes do rosto (`mosaico`) | Frase de ênfase longa, com o rosto expressivo em close | 48–55 q | 1 | 7,267–9,567 |
| Papel rasgado (`papel-rasgado`, em `tela`) | Número ou dado revelado | 32–37 q | 1 | 5,633–7,167 |
| Card dentro de card (cena `cartao`) | Frase de autoridade; sai com `voo` | 36–42 q | 1 | 13,200–14,933 |
| Letterbox com light leak (`letterbox`) | Entrada de uma inserção ou de um B-roll | ~15 q | 1 | 3,567–4,40 |
| Primeiro plano desfocado (`primeiro-plano`) | Moldura de profundidade em `tela` e `broll`; variante wipe esconde um corte | 30–40 q | 3–5 | 5,633–7,167; 10,40–11,50 |
| Cena surreal de IA (`broll` + `amplitude` + `rack`) | Metáfora claramente fictícia; nunca para ilustrar um dado | 60–72 q | 0–1 | 14,933–17,967 |
| Tela tipográfica (`tela-tipografica`) | Divisor de bloco ("VAMOS VIRAR A PÁGINA") | 24–48 q | 1 | ref274 6,0–6,5; 23,0–23,5 |
| Cartão 3D (`cartao-3d`) | Definição de termo técnico ("ritmo circadiano", "acidose") | 36–60 q | 2 | ref274 20,0–21,5 |
| Estilhaço de saída (`particulas`) | Palavra negada ("não precisa de mais SHOTS") | 9–10 q | 1 | 16,23–16,6 |
| Neon atrás da pessoa (`neon-atras`) | Última frase | ~16 q | 1 | 23,200–23,900 |
| Rabiscos à mão (`rabisco`) | Opcional, só no gancho | até 44 q | 1 | 0,0–1,83 |
| Motion blur direcional | Palavras deslizando, voos, giros. Usar filtro SVG direcional (barato); `CameraMotionBlur` só em trechos ≤ 24 q | junto com o movimento | — | "this" 1,17–1,30; "ten" 5,70–5,87 |
| Tremida de câmera | **Não usar** (não aparece na ref) | — | 0 | — |

## Transições (campo `transicao`: como a cena ENTRA)
| Nome | Duração | Quando | % das trocas | Som automático | Status |
|---|---|---|---|---|---|
| `lente` | 2 q de desfoque no plano que sai, corte seco, 3 q de foco no que entra (pico de 24–30 px; escala 1,03→1). Sem crossfade | Padrão do formato | ~55% | `whooshes/whooshes_14_simple-whoosh`, vol 0,2, em 1 de cada 3 | a construir (até lá, `corte`) |
| `corte` | 0 | Com a câmera já em movimento ou escondido por `primeiro-plano` (wipe) | ~10% | — | existe |
| `zoom` | hoje 6 q (escala 1,22→1 + blur de 16 px); encurtar para 2–3 q no CUT | Corte disfarçado de ângulo (aberto ↔ close ou contra-plongée) | ~10% | `whooshes/whooshes_20_epic-fast-whoosh-345469`, vol 0,45 | existe (duração por estilo a fazer) |
| `silhueta` | 5 q (abertura) ou 3 q (meio) | Abertura + 1 virada | 2 por vídeo | `camera-shutters/camera-shutters_02_little-bit-hard-cammera-shutter`, vol 0,5 (+ `impact_sub` na abertura) | a construir |
| `voo` | 3 q (o card voa para a câmera: escala 1→1,6 + blur horizontal de 40 px) | Saída do `cartao` | 1 | `whooshes/whooshes_10_high-and-fast-whoosh`, vol 0,4 | a construir |
| `giro` | 6 q (rotação 0→15°, escala 1→1,25, zoom-blur crescente, ease-in) | Saída do P&B do gancho | 1 | `whooshes/whooshes_02_cinematic-fast-normal-whoosh`, vol 0,35 | a construir |
| `flash` | 6 q (branco que decai) | Só como substituto da `silhueta` quando não houver recorte | ≤ 2 | `camera-shutters/camera-shutters_03_smooth-cammera-shutter`, vol 0,45 | existe |
| `blur` | 7 q, crossfade | **Não usar no CUT** (a ref não tem crossfade; fica para o MIX) | 0 | `whooshes/whooshes_16_smooth-and-fast-whoosh` | existe |

- A proporção fica em ~2/3 de cortes (`lente` + `corte`) e ~1/3 de cortes disfarçados (`zoom`, `silhueta`, `voo`, `giro`, wipe por objeto).
- A transição cai sempre em fim de palavra, e o texto zera no mesmo quadro.

## Movimento contínuo (zoom e câmera)
- **Todo plano `fala` tem `zoom` contínuo**, com variação de 12–35% ao longo do plano (a ref vai de ×0,63 a ×1,4; o mínimo é 5–10% no B-roll).
  - O sentido alterna entre planos vizinhos.
  - Zoom-out é o mais comum (5 dos 8 planos de fala da ref). Exemplos: `[1.3, 1.0]`, `[1.0, 1.18]`, `[1.25, 1.0]`.
  - O padrão atual do estilo, `[1, 1.06]`, é fraco: deve alternar in/out sozinho quando a cena não traz `zoom`.
- **Limite de escala:** 1,25 com bruto 1080; 2,0 com bruto 4K vertical. Conferir a nitidez num quadro renderizado com `--trecho`.
- **`curva`:**
  - `suave` é o padrão;
  - `entrada` (expo-out) para push-in rápido de 8–9 q (ref P3: ×1,17 em 0,37 s);
  - `linear` em dolly longo.
- **`foco`:** medir no rosto num quadro em resolução cheia. Com câmera fixa, alternar o x entre 0,42 e 0,58 em cenas vizinhas para variar o enquadramento.
- **No máximo 1 aceleração por plano** (campo `chaves`, peça nova):
  - punch-out de ~20% em 5 q (ref 19,40–19,60);
  - ou pan de 25% da largura em 3–4 q (ref 12,40–12,53);
  - ou rampa de dolly ×2 no último segundo (ref 16,7–17,0).
- **Plano parado:** só até 26 q, e com outro elemento girando (anel de texto; ref 4,567–5,633).
- **Texto preso ao cenário** (`camera: true` na camada): o bloco acompanha o zoom e o pan da cena.
  - Em movimentos fortes, paralaxe de 1,2–1,5× (o texto anda mais que o fundo).
  - A marca fica fora da câmera.
- **B-roll:**
  - vídeo com push-in de 5–10% (hoje o motor faz 4%);
  - foto com 10–15% (hoje 10%);
  - cena de IA com dolly de 1,0 a 1,6 e rack focus de 40 a 0 px em ~45 q.

## Cor e acabamento
- **Valores do `estilos.ts` (CUT):**
  - `acento: '#D7311E'` (a confirmar);
  - novo campo `acentoProfundo: '#141A3D'`;
  - `cor: {contraste: 1.08, saturacao: 0.9, calor: 0.02}`;
  - `vinheta: 0.3`;
  - `grao: 0.03` (a ref não mostra grão);
  - `fundoTela: 'escuro'`.
- **Paleta fechada**, com uma cor de destaque só:

  | Uso | Cor |
  |---|---|
  | Texto (creme) | #F2F4F8 |
  | Acento | #D7311E |
  | Painéis (acento profundo) | #141A3D, escurecendo até #2A0603 |
  | Brilho | #FF5A3C a 40% |
  | Preto | #0B0B0C |
  | Card | gradiente do acento até #1E1D1C |

- **Pele natural:** rosa quente, nunca laranja. A saturação da pele fica contida (na ref, 11–17, contra 36–43 nos painéis): o "punch" de cor vem dos grafismos.
- **Low-key sem esmagar os pretos:** luma média de 66–120 (de 255) nas falas; 10º percentil de 20–35. A exceção é o P&B do gancho, com pretos esmagados.
- **Divisão de tons** (sombras azul-petróleo #192129/#25353B, realces quentes): não cabe nos campos do motor. Testar no `preparar.mjs --comparar` (opção `cinema`, ainda não verificada).
- **Retícula (halftone):** só no P&B e no `cartao`, com pontos de passo 9–10 px a 45°.
- **Vinheta:** mais por desfoque de borda que por escurecimento (opcional: `radial-progressive-blur` nos closes). Escurecimento de 15–25% só no `cartao` e no `letterbox`.

## Marca (@soutotreinador)
- **Sem @ fixo durante o vídeo** (decisão do usuário em 2026-10-08: "isso não precisa ficar"). A peça `marca-arroba` (ícone do Instagram + @ no canto) **não entra mais** em nenhum vídeo. O @ só aparece no card final (`encerramento-insta`).
- **Gradiente do Instagram** (#FEDA75→#D62976→#962FBF→#4F5BD5) por 48 q: só no card final.
- **Não copiar:** monograma BS, nome BARSOL MEDIA, glitch com orbe, e-mail e site, azul elétrico #8C000B.

## Abertura e fechamento
**Abertura (0–2 s, quatro estados visuais):**
1. **q 0–1:** silhueta do 1º plano no acento profundo, com "???" creme brilhando no rosto ou um símbolo do tema (ex.: "Zzz" em SONO X IMUNIDADE).
2. **q 2–4:** silhueta branca com bloom quente (#fff6c8/#ffe9a0) sobre o plano estourado (brightness 1,6, blur de 6 px), com SFX de impacto.
3. **q 5:** corte seco para `fala`, já com o primeiro bloco no 1º quadro útil. A 1ª palavra pode ficar atrás da cabeça (recorte de ~34 q).
4. **P&B seletivo de 14–20 q** na frase de confronto, saindo com `giro`.
5. **Close colorido** com `selecao` ou `palavra-impacto`.

Regras do gancho:
- Até 7 s: planos ≤ 38 q, 5 eventos/s, 2–3 momentos-assinatura.
- Escolher uma tomada inicial com gesto para a câmera.

**Fechamento (no máximo 2,5 s de marca depois da última palavra):**
1. **Última frase (CTA):** `texto-arco` em anel 3D ou bloco normal, + `neon-atras` (monograma "LM" ou "@" em contorno creme) por ~16 q.
2. **`fade-tinta`** para preto em 5–6 q.
3. **Card final:**
   - `{pausa: 2}` na `montagem` + cena `tela` com fundo `escuro` (#0B0B0C) + `encerramento-insta`;
   - ícone de 150 px no centro (y 47%), creme virando gradiente em 24 q;
   - @ em Inter Tight 600, 40 px;
   - linha opcional em Instrument Serif itálica.
4. **Trilha** com `fim` na última nota do card e `fade` de 0,25 s.

## B-roll
- **Sem repetição visual** (regra comum). Termos recorrentes ("imunidade", "inflamação", "pH", "sono") ganham 3–5 variações. Listar os `broll` repetidos antes da prévia.
- **Uso:**
  - 15–20% do tempo, em planos de 36–72 q;
  - entra com `lente` ou `letterbox`;
  - sempre com bloco de texto novo e push-in.
- **Ordem de busca:**
  1. biblioteca (`biblioteca.mjs buscar`);
  2. `04_broll/meus`;
  3. banco (`stock.mjs`);
  4. internet, só com direito de uso;
  5. Flow (imagem custa 0 créditos; vídeo só com aprovação).
- **As telas gráficas (`tela`) contam como B-roll:** número em `papel-rasgado`, divisor em `tela-tipografica`.
- **Cena de IA:** no máximo 1, e só como metáfora claramente fictícia (ex.: o "shot milagroso" exagerado). Nunca para ilustrar um dado ou uma afirmação científica.
- **Proibido:** documento, estudo, laudo, manchete ou logo inventado (o adesivo "PROOF" da ref usa marca real). Estudo ou manchete real só como print intacto, com o veículo visível.
- **Objetos para `imagem` e `primeiro-plano`:** gerar no Flow com fundo azul #0000FF e recortar com chromakey.

## Áudio
### Música
- Pixabay Music, sempre 2–3 opções com link. Sem vocal, com pulso marcado (95–125 BPM).
  - Isso é sugestão minha: a trilha da ref não foi medida.
- Não repetir suspense investigativo (vídeo 1) nem quarteto de cordas (vídeo 2).
- **`musica`:**
  - `vol` 0,10 com fala e `volSemFala` 0,28;
  - `quedas` com vol 0,4 nos 0,5 s antes da virada;
  - `fim` na última nota do card final, com `fade` de 0,25.
- **`{pausa}`** na montagem só no card final: o CUT não respira com tela vazia.

### Efeitos (Motionix, em `sfx/biblioteca/motionix/`, sem `.wav`)
| Evento | Som | Vol |
|---|---|---|
| Transições `zoom`, `flash`, `silhueta`, `voo`, `giro`, `lente` | Automáticos, ver tabela de transições | — |
| `palavra-impacto` | `whooshes/whooshes_02_cinematic-fast-normal-whoosh` + `clicks/clicks_01_cinematic-click` na última letra | 0,3 / 0,35 |
| Digitação de uma palavra | `ui-sound-effects/ui-sound-effects_21_v4-type-delete-2` (1 por palavra, não por letra) | 0,15 |
| `selecao` | `ui-sound-effects/ui-sound-effects_07_ui-click-digital-04` | 0,3 |
| `etiqueta` | `ui-sound-effects/ui-sound-effects_18_ui-stretch` | 0,3 |
| `mosaico` | `pop/pop_05_smooth-pop`, 3× escalonado junto com as janelas | 0,25 |
| `imagem` (automático) | `pop/pop_05_smooth-pop` | 0,35 |
| Dinheiro ou preço (painel com R$) | `money/money_02_cinematic-money-2` | 0,35 |
| Número ou percentual contando | `data-collect/data-collect_04_data-collect` | 0,3 |
| Anel girando (`texto-arco`) | `gear/gear_04_soft-gear-1` | 0,2 |
| Antes da virada (o riser termina no corte) | `risers/risers_05_smooth-riser` | 0,35 |
| Gradiente do @ | `pop/pop_06_sweet-ui-open` | 0,3 |
| `encerramento-insta` | `ui-sound-effects/ui-sound-effects_03_ui-premium-open` | 0,35 |
| Papel rasgando | Não há na biblioteca: `swish_air` (sintetizado) + `clicks/clicks_01_cinematic-click` até achar um grátis | 0,35 |

- No máximo 1 som por evento visual, e em média 1 som a cada 24–48 q. Não sonorizar cada palavra.
- `impact_sub`: no máximo 2–3 por vídeo. Risers: no máximo 2.
- Os SFX da ref não foram medidos: os pares acima são proposta, a validar ouvindo a prévia.
- **Voz:** perguntar no fim, como sempre (regra comum).

## A confirmar com o usuário (perguntas abertas em 05/10/2026)
1. **Cor de destaque:** vermelho-tomate #D7311E (fundo #141A3D) ou laranja-cenoura #E0601A (fundo #4A1A06). Hoje o motor usa #ff2e2e, que é neon demais perto da ref.
2. ~~**@ fixo** na tela durante o vídeo inteiro, trocando de canto.~~ Decidido em 2026-10-08: **sem @ fixo**.
3. **Neon final** com monograma "LM" ou com o "@".
4. **Densidade de texto:** 100% da fala como texto cinético (como na ref) ou legenda limpa + 1 destaque por frase (sugestão da análise de apoio para nutrição). Este rascunho adota 100%, com hierarquia limpa.
5. **Dica de gravação para os próximos:**
   - 4K vertical;
   - roupa neutra + 1 objeto de cena na cor do acento;
   - mãos livres nos trechos que vão para recorte;
   - abrir com um gesto para a câmera.

## Peças do kit a construir

### Já existe no motor
| Peça | Onde | O que faz | Ajuste para o CUT |
|---|---|---|---|
| `titulo` | camada | Palavras em cascata, `*destaque*`, fontes pesada/base/leve/serifa, saída com blur | Entra em ~8 q: precisa de um modo rápido (2 q) ou cede lugar à `legenda-cinetica` |
| `imagem` | camada | PNG com pop de mola e flutuação | Usar para objetos recortados |
| `zoom` / `curva` / `foco` | cena `fala` | Zoom contínuo `[ini, fim]` com easing e ponto fixo | Padrão `[1, 1.06]` fraco: alternar in/out de 12–35% |
| `desfoque` / `escurecer` | cena | Blur e escurecimento fixos na cena | São estáticos; para animar, usar `chaves` |
| `flash`, `blur`, `zoom` | transição | 6 / 7 / 6 q, com SFX Motionix | `blur` fica fora do CUT; `zoom` encurta para 2–3 q |
| `recortes` + `plano: "atras"` | edição + camada | Pessoa sem fundo por cima das camadas de trás | Orçamento de até 6 s por vídeo |
| `montagem` | edição | Trechos do bruto + `{pausa}` | Toda junção vira troca de cena |
| `legenda` | edição | Palavra a palavra, y 0,74, blocos de 3 palavras | Provisória até a `legenda-cinetica` |
| `tela` (`fundo` CSS), `musica.fim`/`quedas`, `sfxAuto` | cena / edição | Fundo próprio, fim da trilha, SFX automáticos | `tela` com fundo `acentoProfundo` |

### A construir (em ordem de prioridade)
Depois de cada peça: prévia curta na vitrine e `node scripts/regressao.mjs` (precisa sair IDÊNTICO).

| Prior. | Peça | Onde | O que faz | Como implementar no Remotion | Esf. | Refs (s) |
|---|---|---|---|---|---|---|
| 1 | `estilo-cut` | `estilos.ts` + `kit/fontes.ts` | Paleta, zoom, cor, vinheta e grão do formato; Inter Tight 900; duração das transições por estilo | Campos `acento`, `acentoProfundo`, `creme` e `trans` (zoom 3 q, lente 2+3 q) no `Estilo`. Adicionar o peso `'900'` no `loadInterTight`. O MIX mantém os valores atuais | P | — |
| 1 | `legenda-cinetica` | `legenda: "cinetica"` (padrão do CUT) | Tipografia cinética = legenda: blocos por cena, papéis voz/destaque/conector, 7 padrões em rodízio, entrada sincronizada, zerada no corte | Componente no lugar do `LegendaCamadas`:<br>• agrupa `palavras` da saída e quebra em `cena.ini`, pontuação, pausa ≥ 0,35 s ou 6 palavras;<br>• destaque vem de `destaques`; conector, de uma lista fixa;<br>• `measureText` (@remotion/layout-utils) para encaixar;<br>• rotação de −6° a −12°, entrelinha 0,78;<br>• posição fora da região do `foco` (±12% da altura);<br>• override opcional `blocos: [{ini, padrao, x, y, saida}]` | G | ref496 0,2–23,15 inteiro; ref274 1,0–40,5 |
| 1 | `lente` | `transicao` | Desfoque de saída de 2 q, corte seco, foco de entrada em 3 q (24–30 px, escala 1,03→1), sem crossfade | No `Entrada`: blur sem opacidade. Na cena que sai, usar a `cauda` já existente para aplicar o blur nos últimos 2 q | P | 3,167/3,267; 7,167; 13,133; 17,967; 20,567; 23,067/23,167 |
| 1 | `camera` | parâmetro de camada (`camera: true`, `paralaxe`) | Texto preso ao cenário: acompanha o zoom e o pan da cena | Envolver a peça no `enquadrar(...).quadro` da cena ativa (a mesma conta que Pessoa e Recortado usam), com translate × `paralaxe` (1–1,5) | P | 18,27–20,5; 12,40–12,53 |
| 1 | `zoom-chaves` | cena (`chaves: [{t, zoom, foco?, curva?}]`) | Degrau de zoom, punch-out de 20% em 5 q, pan de 25% em 3–4 q, rampa de dolly | Interpolar segmento a segmento com `CURVAS`, dentro do `enquadrar()`, para pessoa e recorte continuarem alinhados | P | 19,40–19,60; 12,40–12,53; 16,7–17,0; 3,267–3,63 |
| 1 | `palavra-impacto` | camada (frente ou atrás) | Caixa-alta 900 com falsa extrusão creme, letra a letra (1,5 q) de creme 50% para acento; opções de virada, eco e inclinação | 8–12 cópias deslocadas 1–1,5 px para baixo e para a direita + sombra. `virar`: `rotateY(90°→0)` por letra com `spring({damping: 14})`, trocando a cor na metade. `eco`: cópia abaixo a 40%. Parâmetros: `texto`, `x`, `y`, `altura`, `rot`, `skew` | M | "PROOF" 17,10–17,95; "EVIDENCE" 10,03–11,45; "REBRAND" 6,53–7,15; "10,000" 5,93–7,15; ref274 "NEED" 5,0–5,5, "MIDDLE" atrás 10,5–12,0 |
| 1 | `silhueta` | `transicao` (usa recorte de 6–12 q) | Silhueta no acento profundo com "???" ou símbolo (2 q), depois branca com bloom (3 q); versão do meio com 2 + 1 q | `<OffthreadVideo transparent>` do recorte. Cor chapada: filtro SVG `feFlood` + `feComposite operator="in"`. Branca: `brightness(0) invert(1) drop-shadow(0 0 40px #fff6c8) drop-shadow(0 0 90px #ffe9a0)`. Fundo com `brightness(1.6) blur(6px)`. Troca seca, sem interpolação | M | 0,000–0,200; 4,467–4,567 |
| 1 | `pb-seletivo` | cena (`pb: true`, `reticula`) | P&B com retícula; o texto acima continua colorido | `grayscale(1) contrast(1.1) brightness(.85)` no `filtro` da cena, entrando em 2–3 q. Retícula em CSS (`radial-gradient` com passo de 9–10 px a 45°, `mix-blend-mode: multiply` a 35%), mais barata que o `halftone` WebGL | P | 1,000–1,833; ref274 12,5–13,5, 36,0–37,0 |
| 1 | `marca-arroba` | camada automática do estilo | Ícone do Instagram em linha + @; montagem por partes, troca de canto em 6 q, brilho em gradiente | SVG com `strokeDashoffset` por parte, posições A e B do guia. Parâmetros: `trocas: [{t, pos}]`, `brilho: [t]` (gradiente por 48 q via `linearGradient` com stops animados) | P | ref496 0,1–24,3 (trocas 9,5 e 17,0; gradiente 2,25–4,25); ref644; ref274 |
| 1 | `encerramento-insta` | camada sobre `tela` escura + `{pausa: 2}` | Card final de até 2,5 s: ícone de 150 px creme → gradiente → creme, @ de 40 px | Ícone com `simple-icons` (`siInstagram`) ou o mesmo SVG da `marca-arroba`. Gradiente em 24 q; @ em fade de 6 q a partir de +6 q | M | ref496 29,0–33,1; ref644 24,0–27,9; ref274 41,0–45,3 |
| 2 | `texto-arco` | camada | Palavras num trilho elíptico em volta da cabeça ou do corpo, girando 20–40°/s. `perspectiva: true` vira anel 3D (a palavra mais próxima cresce 2–3×) | SVG `<textPath>` numa elipse (raio de 0,35–0,50 da largura), animando `startOffset` e a rotação do grupo; palavras entram no tempo da fala. Anel 3D: CSS 3D por letra (`rotateY(θ) translateZ(R)`), contêiner com `rotateX(-15°)`, `perspective: 1200px`, blur proporcional ao z (6–10 px na frente). O lado invertido fica sempre desfocado | M | 0,2–1,83; 4,567–5,633; 20,65–23,15; ref274 1,5–2,5 |
| 2 | `selecao` | camada | Caixa de seleção estilo Figma: ponto no acento → 4 alças → contorno tracejado em volta da palavra, + 3 faíscas | Pop do ponto em 2–3 q; alças de 16–20 px se afastando em 3 q; `strokeDasharray="8 6"`; faíscas 6 q depois. Parâmetros: caixa-alvo `x`, `y`, `w`, `h` | P | 1,83–3,2 |
| 2 | `etiqueta` | camada (ou padrão da legenda) | Barra creme com glow que nasce como linha; palavra 900 no acento dentro | `scaleY` 0→1 em 3 q (expo-out); palavra em fade de 2 q aos +4 q | P | 13,63–14,85 |
| 2 | `cartao` | cena (`cartao: {escala, raio, fundo}`) + `transicao` `voo` | O plano encolhe para um card arredondado sobre gradiente, com a palavra da marca desfocada atrás; sai voando para a câmera | Div com `borderRadius` (4% da largura) e `overflow: hidden`, escala 1→0,73 em 5 q (`Easing.out(Easing.exp)`), borda de 1 px, retícula fina. Fundo do acento até #1E1D1C. `voo`: escala 1→1,6 + `feGaussianBlur stdDeviation="40 0"` em 3 q | M | 13,200–14,933 |
| 2 | `mosaico` | camada | 3–5 janelas sem moldura com o rosto ampliado 2–2,5× (olhos, boca), em cascata, sincronizadas com o vídeo | Cada janela é uma div `overflow: hidden` com o mesmo `<Video>` e o mesmo trim. Entrada de escala 0,3→1 em 2–3 q (`spring({damping: 20, stiffness: 220})`), uma janela a cada 1–2 q; deriva com `noise2D` de ±6 px. Medir olhos e boca num quadro cheio. Cada janela decodifica o vídeo de novo (ou pré-recortar com ffmpeg) | M | 7,267–9,567 |
| 2 | `papel-rasgado` | camada sobre `tela` | Fenda serrilhada que abre em degraus e revela uma imagem; o número sai da fenda | `tear({progress})` num `<Img>` do papel: `progress` 0→0,06 em 4 q, salta para 0,5 em 1 q, chega a 0,7 em 6 q. Alternativa: 2 PNGs de papel do Flow (chromakey) se afastando com `spring`. Retícula na borda. Exige `--gl=angle` | M | 5,633–7,167 (fenda 5,933; aberturas 6,133 e 6,367) |
| 2 | `primeiro-plano` | camada | Objeto PNG muito desfocado na frente, com paralaxe; variante `wipe` cobre mais de 90% da tela no pico do corte | `blur` de 25–40 px, escala 1,5–2×, deslocamento 1,5–2× o da cena; entra e sai por uma borda | P | 5,633–7,167; 10,40–11,50 |
| 2 | `neon-atras` | camada `atras` + recorte de ~20 q | Monograma ou @ em contorno creme de 25–30 px desenhado por segmentos atrás da cabeça, com luz de recorte no cabelo | `evolvePath` (@remotion/paths) em 6 q; glow crescendo em 12 q; `radial-gradient` #FFB070 em `screen` a 20–30% | M | 23,200–23,900 |
| 2 | `letterbox` | camada | A tela cheia vira uma faixa de 33–38% da altura, inclinada 1–2°, com light leak dourado nos cantos | `clipPath: inset()` animado em expo-out (~9 q) + `@remotion/light-leaks` (#C8A050) | M | 3,567–4,40 |
| 2 | `giro` | `transicao` | Rotação de 0→15° com escala 1→1,25 e zoom-blur crescente, depois corte seco | `rotate` + `scale` em ease-in por 6 q + `zoom-blur({amount})` (WebGL) ou blur radial em SVG | M | 1,600–1,833 |
| 2 | `fade-tinta` | camada | Escurece por manchas orgânicas, a partir da esquerda e da base | `feTurbulence` + `feColorMatrix` com limiar animado em 6 q, usado como máscara preta | M | 23,867–24,100 |
| 2 | `cena-ia` | cena `broll` (`amplitude`, `rack: [px0, px1, dur]`) | Ken Burns forte (1,0→1,6) com rack focus de 40→0 px; paralaxe opcional em 2 camadas | Parametrizar `amp` no `Broll` (hoje fixo em 0,04/0,1) e interpolar o blur; camadas de fundo e frente vindas de imagens do Flow | P | 14,933–17,967 |
| 3 | `cartao-3d` | camada | Card no gradiente do acento (75% da largura, contorno creme de 2 px) que gira em 3D e para de frente, com brilho cruzando; define um termo | CSS 3D `rotateX/rotateY` com `spring` (~24 q), faixa de brilho em `linear-gradient` animado | M | ref274 20,0–21,5 |
| 3 | `tela-tipografica` | camada sobre `tela` | Fundo no acento com listras curvas (cilindro) ou cortina; palavra de impacto passando em pan com motion blur | Listras em SVG com `path` curvo; `palavra-impacto` grande com `translateX` e blur direcional | M | ref274 6,0–6,5; 23,0–23,5 |
| 3 | `particulas` | camada (saída especial) | 20–40 cacos triangulares no acento caindo e girando a partir da palavra | Trajetória com `noise2D` + `rotate3d`, em 9–10 q, com seed fixa | M | 16,0–16,8 |
| 3 | `rabisco` | camada | "!!!" desenhado à mão em creme, "fervendo" (jitter a cada 2–3 q), preso ao plano | SVG `path` com variação por `random(seed + Math.floor(frame/3))` + `camera: true` | P | 0,0–1,83 |