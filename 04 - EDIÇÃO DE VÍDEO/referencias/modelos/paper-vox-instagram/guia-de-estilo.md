# Guia de estilo: INSTAGRAM - PAPER VOX ANIMATION (v1)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Status: **v1 (2026-10-20), ✅ fixo** (como o CUT e o MIX; **não** congelado). Id `paper-vox-instagram`, composição `PaperVox`. No lab ele era o "formato 4", e o Jorge o chamou de 5º; aqui é sempre pelo nome e pelo id.
- Consolidado pelo Jorge em 2026-10-20, depois da prévia 2 do piloto "sociedade que adoece": "O estilo de edição ficou simplesmente perfeito! … Consolidado. Só a partir de um áudio." e "Pode renderizar".
- Formato, estilo e guia só mudam a calibração original. Mudança no motor passa nas 4 regressões: `regressao-paper-vox.mjs`, `regressao.mjs` (TELA DIVIDIDA), `regressao.mjs --cut` e, para o MIX, `node scripts/vez.mjs node scripts/regressao.mjs --mix`. Ver "Checagens".
- **Ordem de precedência:** "Decisões de edição" prevalece sobre tudo; depois "Correções do Jorge no piloto"; depois o resto do guia.
- **O código é a fonte de verdade do comportamento:** `motor/src/modelos/paper-vox/*.ts*` e `motor/scripts/lib/mural.mjs`. Os números deste guia foram lidos de lá; se divergirem, vale o código e o guia se corrige.
- Apoio nesta pasta: `prompts-flow.md` (blocos de prompt e operação do Flow) e `shotlist-esquema.md` (esquema real da `shotlist.json`).
- Substitui o rascunho do lab (`05_LAB/formatos/4-paper-vox-animation/guia-de-estilo.md`, anterior ao mural contínuo), que fica só como histórico.

Referências:
- **Principal: o piloto** `%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece` (aprovado em 2026-10-20).
  - Final: `07_final/2026-10-19_sociedade-que-adoece_final.mp4` (1080×1920, 24 fps, 144,3 s, −14,3 LUFS, pico −0,9 dB, 388 MB).
  - Prévia aprovada: `06_previas/previa-2_formato4_2026-10-20_trilha-A.mp4`.
  - Geradores (o molde de todo vídeo novo): `03_roteiro/montar_shotlist.mjs` e `03_roteiro/montar_quadro.mjs`; saídas `shotlist.json`/`.md` e `quadro.json`.
  - Áudio original: `%USERPROFILE%\Videos\1019(1)\1019(1).MP3` (142 s, já tratado).
  - É a referência da regressão (`%SOUTO_VIDEO_PROJETOS%/_sistema/regressao/paper-vox_base*.mp4`): o `quadro.json` dele só muda com calibração original.
- **Refs do lab** (`05_LAB/referencias/videos/ref-01…08`, análises em `05_LAB/referencias/analises/ref-NN/analise.md`; compartilhadas com o PAPER VOX B-ROLL, em teste no lab). Valem pela linguagem; nenhuma é 100% dark e nenhuma tem mural contínuo entre cenas nem montagem ≤ 0,3 s por plano (medido em `02_analise/refs-quadro-continuo.md` do piloto). Essas duas coisas são peças novas, e a montagem de ~0,2 s é ideia do Jorge.

  | Ref | O que é | Vale | Não vale |
  |---|---|---|---|
  | ref-01 | "Vox article effect" (After Effects), 32,9 s, 23,976 fps | Página que nunca para (zoom, snap), textura de papel real, marca-texto que se desenha, papel a 12 fps com câmera a 24. O trecho 18,44–24,52 s é o mais perto do mural (uma página gigante como canvas) | Papel claro (aqui o jornal é escuro), NYT/Vox na tela, legenda queimada, o criador na câmera (24,5–29 s) e a tela do TikTok |
  | ref-02 | Colagem de papel em stop-motion (o tutorial do Seedance), 24 s, 30 fps | Peças que entram da borda, giram, desaceleram e travam; papelão; colagem | Seedance (calibração original), membros articulados, os dois cartões empilhados, papel milimetrado claro |
  | ref-03 | "CC Page Turn + Posterize 8 fps", 47,3 s | Traço que treme a 8 fps, mesa vista de cima, persiana, virada de página | Tela do After Effects, legenda queimada, pessoa |
  | ref-04 | Dioramas de papel (vídeo gerado), 25,4 s, 30 fps | Cena que se monta camada a camada (elemento novo a cada 0,3–0,6 s) | Vídeo gerado (Omni custa crédito: só exceção com ⏸), os dois cartões |
  | ref-05 | "Perfeccionismo" (PT-BR), 39,2 s, 30 fps | Estátuas + tipografia em duas escalas, palavra entrando de borrada para nítida, 1 acento, ~2,4 palavras/s | Paleta clara (só 16–19,3 s e 35–39 s são escuros); **palavra atrás da estátua** (reprovada: o texto nunca fica coberto); a montagem final de clipes de cinema |
  | ref-06 | "Going through a change?" (EN), 20,4 s, 24 fps, 4:3 | Tipografia + ícones, flash vermelho de abertura, spotlight, escala extrema, a única rajada de planos curtos (0,25–0,42 s, L·O·V·E) | O 4:3, pixel-art (aqui só recorte realista), inversão para fundo claro |
  | ref-07 | "Harvard predicted this" (EN), 37 s, 30 fps | Interface como palco, zoom-through, recursão (a foto vira anexo), mesa que gira | É propaganda de template (CTA "Comment 'Link'"), sala 3D, barras pretas |
  | ref-08 | Tutorial "Claude skill + Seedance", 50,1 s, 30 fps | O esqueleto da shot list (estilo / texto de tela / planos com duração), colagem halftone | A pessoa na tela (é o layout do PAPER VOX B-ROLL), Seedance, multidão e tentáculo |

Convenções:
- **q = quadro a 24 fps** (1 q = 41,7 ms; 2 q = 83 ms). 24 fps está fixo no código (`calcularPaperVox` usa × 24).
- **Tempos em segundos da saída**, que são os segundos do áudio da voz a partir de `vozIni` (0 no vídeo inteiro). O card soma ~3,2 s no fim.
- **px do mundo × px da tela:** tamanhos e posições do `quadro.json` são px do mundo. Com a câmera em zoom 1, 1 px do mundo = 1 px da tela 1080×1920.
  - Estação em escala `k` (uma estação-filha dentro de outra, ex. a E12 dentro da tela do celular com k 0,42): as peças saem × k e a câmera chega com zoom 1/k. Na tela, tudo fica do mesmo tamanho.
  - Planos de parallax: o plano anda × 0,55 (`fundo`), × 1 (`meio`) ou × 1,35 (`frente`) a câmera. A coordenada de uma peça no plano é a do meio × esse fator.
  - Em px de tela: `viva` (deriva da câmera, 5 px), o limiar e o espaço do motion blur.

Princípio:
- **Só a voz do Jorge. Ele não aparece.** O vídeo nasce de um áudio. É 100% dark.
- **Um mural só.** Todas as cenas moram num mundo grande de papel escuro, e a câmera desliza de estação em estação sem corte, com parallax em 3 planos e motion blur nos chicotes. A cena anterior fica no mural. No fim, a câmera recua e mostra o mural inteiro ligado pelo traço do "caminho", e mergulha no card da marca.
- **O dinamismo vem da câmera e das peças, não de cortes:** um evento a cada ~0,43 s no piloto. O único "corte" é a montagem, escondida num mergulho da câmera.
- **Feito à mão:** papel e objetos de papel a 12 fps, traço que treme a 8 fps, câmera e blur nos 24 fps cheios (ref-01, ref-03).
- **Chega rápido, assenta macio:** expo-out e `assento`, blur só no pico de velocidade, nada fica estático (tudo "boia").
- **A palavra-chave é o cursor do olho:** gigante, em degradê da marca, com punch-in da câmera.
- **Som econômico:** a voz manda; SFX só nos acentos que contam a história; trilha a 1/4 da voz, que para seco nos momentos tensos.

## Decisões de edição (datadas, prevalecem sobre tudo)
- **2026-10-19 · Sem Seedance.** Estilo por código + stills do Nano Banana grátis; vídeo gerado (Omni/Veo) só como exceção, com ⏸ e custo.
- **2026-10-19 · "Quadro contínuo 100% por código, 0 crédito, montagens na opção A (stills do Flow)".**
- **2026-10-19 · Proposta de cenas** com alto impacto visual, dinamismo, fluidez, referência visual e magnetismo.
- **2026-10-19 · Montagem de ~0,2 s nos silêncios** (ideia dele; não está nas refs).
- **2026-10-19 · Dúvidas da transcrição:** ele responde por texto; até lá, a palavra em dúvida fica FORA da tela.
- **2026-10-19 · "Pestana" = virar página de papel:** a categoria de SFX `papel`.
- **2026-10-19 · Shot list, prompts e 47 imagens aprovados** no piloto.
- **2026-10-20 · Prévia 1:** "a estrutura ficou simplesmente sensacional", com 4 críticas (ver "Correções do Jorge no piloto"). Viraram regra:
  - SFX ~1 a cada 5 s, 12–17 dB abaixo da voz, ≥ 1,15 s entre eles, nunca a mesma categoria em seguida; entrada de imagem, papel, fita e plano de montagem **sem som**;
  - palavra-chave no degradê da marca; branco só sobre a marca azul elétrico;
  - recortes, fotos e objetos vêm de fora com curva smooth "extremamente dinâmica" e ficam "boiando"; aparições mais rápidas e nunca estáticas;
  - trilha: "encontrar a trilha sonora perfeita, corte a música e deixe só a voz quando for momentos mais tensos, ou que minha voz precisa ser enfatizada".
- **2026-10-20 · Prévia 2:**
  - trilha A, suspense de investigação ("vou ficar com a 1ª opção"; "gostei de ambas");
  - SFX com timing milimétrico ("faz a diferença; nesse 88% ficou perfeito"): etapa de refino (P7) **só para os próximos** ("n precisa fazer nesse só para os próximos");
  - degradês variados: "salmão-vermelho, salmão-laranja, eletrico-aco, e não só uma ou outra cor";
  - texto nunca por baixo de imagem ou linha ("polêmica" ficou atrás da estátua, "caminho" atrás da linha): "corrija para os próximos";
  - "O estilo de edição ficou simplesmente perfeito! … Consolidado. Só a partir de um áudio." → consolidado; "Pode renderizar".

## Correções do Jorge no piloto (prevalecem sobre o resto)
**Prévia 1 → prévia 2 (2026-10-20)**
1. **"SFX altos e extremamente repetitivos" em cada imagem, card e elemento.**
   - Causa: 106 SFX (0,7 por segundo), um por entrada de peça, com alvos de volume 5–11 dB mais altos.
   - Mudou: alvos de loudness por categoria em `lib/mural.mjs` (`ALVO_M`, `ALVO_PICO`; transição ~12 dB e pop ~17 dB abaixo da voz) e plano curado no gerador (26 SFX). O `M.sfx` **para com erro** se dois SFX ficarem a < 1,15 s ou se a mesma categoria vier em seguida. Entrada de imagem, papel, fita e plano de montagem ficaram sem som.
2. **Textos da cor do fundo.**
   - Causa: a cor da palavra-chave se confundia com o papel escuro.
   - Mudou: toda palavra-chave com `cor: 'marca'` (degradê aplicado com `background-clip: text` no próprio nó, sombra por `drop-shadow`). Branco `#F2F4F8` só sobre a marca azul elétrico ("vergonha").
3. **Recortes (cadeira, estátua, a mão aos 49 s) apareciam junto com o painel.**
   - Causa: a peça nascia no mesmo instante da estação e ficava parada.
   - Mudou: entrada `voa` em `elementos.tsx` (de fora da tela, em arco, giro, blur) e `M.voaBoia()` no mural (a peça só sai 0,05 s depois que a câmera assenta, vinda do lado em que mora). Depois, `boiar`. Peças presas não boiam (`boia: 0`); o traço sobre uma peça boia junto (`boiaId`). Entradas mais rápidas no geral (`pousa` 0,4 s, `sobe` 0,24 s, `desliza` 0,3 s).
4. **Trilha sem respiro nos momentos tensos.**
   - Mudou: a composição não toca mais a trilha. O `mixar-audio.mjs` (nasceu no lab como `mixar-trilha.mjs`) mistura depois do render: ≤ 1/4 da voz, **para seco** em 12 ms nos 7 cortes só voz e volta em 0,12 s com a frase seguinte. Comparar trilhas leva segundos, sem re-render.

**Prévia 2 → final (2026-10-20)**
1. **Trilha:** a A (`escolhida: 'A'` no gerador).
2. **Degradês variados.**
   - Causa: um degradê só em todas as palavras-chave (`#8C9BE4 → #2E49CE → #B74F2A`).
   - Mudou: os 3 degradês em `elementos.tsx` (`DEGRADES`) e o rodízio `M.degrades()` por ordem de entrada (dois seguidos nunca iguais).
3. **Texto por baixo de imagem ou linha.**
   - Causa: a ordem de desenho era a do array (o recorte da E14 vinha depois do texto; o caminho entra depois da E34).
   - Mudou: `camada()` em `PaperVox.tsx`. Dentro de cada plano, o texto fica sempre por cima de papel, foto, recorte e objeto; traço à mão e flash ficam por cima do texto. A correção já entrou no motor e também saiu no final do piloto (o Jorge foi avisado).
4. **Timing milimétrico dos SFX:** etapa P7 nova (`refinar-sfx.mjs`, `M.ev.*`, `sfxNaMixagem`, ponto do som medido). O piloto **não** passou por ela.

## Formato
- **Quadro:** vertical 9:16, **1080×1920, 24 fps**, `gl: angle` (linha `paper-vox-instagram` no `src/modelos.json`; composição registrada no `src/Root.tsx`).
- **Composição:** `PaperVox` (`src/modelos/paper-vox/PaperVox.tsx`). Props = `03_roteiro/quadro.json`, com **`"modelo": "paper-vox-instagram"`**, gravado pelo `M.gravar()` e conferido pelo `render-paper-vox.mjs`.
  - O arquivo se chama `quadro.json`, nunca `edicao.json`: o hook valida todo `edicao.json` contra a estrutura do motor de camadas e daria ERRO.
  - Os tipos (`QuadroProps`, `Elemento`, `ChaveCamera`…) moram em `src/modelos/paper-vox/tipos.ts`, nunca no `src/tipos.ts`.
- **Render:** `scripts/render-paper-vox.mjs`, sempre pela fila (`vez.mjs`). Não usa o `render.mjs` (os 3 outros modelos ficam sem nenhuma mudança).
- **Entrada:** só um áudio (`01_bruto/bruto.mp3`, `.wav` ou `.m4a`; o `.oga` do WhatsApp se converte antes). Não há bruto de vídeo, cor nem decupagem: as pausas são o lugar das montagens.
- **Duração:** a do áudio + 3,2 s de card (fim da última fala + 0,1 s + 3,1 s). Piloto: 142 s de áudio → 144,29 s. Duração típica: a confirmar com o Jorge.
- **Áreas seguras do Reels** (proposta do rascunho do lab; o piloto não foi medido contra ela, conferir na folha de quadros):
  - texto fora de ~250 px embaixo, ~180 px em cima e ~70 px nas laterais;
  - nada na coluna de botões (x > 86%, y 55–90%).
- **Marca:** sem @ fixo. O @ só aparece no card final.

## Estrutura do vídeo
| Parte | O que se vê | Regra |
|---|---|---|
| Gancho (0–3 s) | A 1ª estação já com a imagem mais forte e a 1ª frase; a câmera abre (`abre`, zoom 0,98 do alvo) e a foto voa a 0,05 s | **≥ 4 eventos nos 3 primeiros s** (ERRO no `validar-shotlist.mjs`); nada de preto vazio |
| Blocos | Uma coluna do mural por bloco do texto (piloto: 7 blocos de 2 a 7 estações) | 1 look por bloco, alternando: `editorial` (jornal escuro), `colagem` (mesa de papelão), `marmore` (estátuas). Nunca 3 receitas iguais seguidas (ERRO) |
| Estações | Uma frase ou meia frase por estação: base de papel + apoio + palavra-chave + 1 foto, recorte ou objeto + alvo de câmera | Piloto: 36 estações de 1,14–7,23 s (mediana 3,43 s). Estação < 1 s = AVISO |
| Montagens | Nos silêncios longos, a câmera mergulha numa peça, passam 4–10 planos de ~0,2 s em tela cheia e a câmera emerge na estação seguinte | Ver "Montagens" |
| Recuo final | Nas últimas frases (piloto: de "Como esse caminho é feito" a "o resultado"), a câmera acompanha o traço do caminho e recua até o **mural inteiro** (zoom 0,098 no piloto), com o texto gigante por cima | `M.caminho()` + estação do mural inteiro |
| Card | A câmera mergulha num papel em branco do mural: "Jorge Souto" no degradê, "educador físico", CREF 000000-G/UF, ícones do Instagram e do YouTube, @soutotreinador | o vídeo fecha 3,2 s depois do fim da última fala; fixo (`M.card()`); fade da trilha de 2,5 s |

- **Receitas usadas no piloto** (campo `receita` da shot list): `tipo-escala` 7, `objeto-papel` 9, `jornal-vivo` 3, `mesa-escura` 3, `interface-palco` 3, `estatua-sanduiche` 3, `colagem-vox` 2, `cena-em-camadas` 2, `capitulo-vox` 1, `silhueta-gradiente` 1, `colagem-monta` 1, `icone-orbital` 1. A `estatua-sanduiche` agora é só estátua + palavra **por cima** (nunca atrás).
- **Respiro** (`respiro: true` na shot list): frase delicada, câmera quase parada, sem ruído visual (piloto: E05, E19, E21). Não conta no aviso de buraco sem evento.

## Ritmo (números do piloto)
| Medida | Piloto | Regra |
|---|---|---|
| Fala | 142 s, 311 palavras (2,2 por s) | — |
| Eventos (chegada, cada palavra de texto de tela, evento, plano de montagem) | 328, 1 a cada 0,43 s | ≥ 4 nos 3 primeiros s (ERRO); buraco > 1,5 s sem evento fora de respiro = AVISO |
| Estações | 36 em 7 blocos; mediana 3,43 s | < 1 s = AVISO (exceto `rajada`) |
| Chaves de câmera | 167 (22 em `snap`: punch-ins e chegadas snap) | câmera nunca parada (deriva + câmera viva) |
| Palavras-chave em degradê | 34 (≈ 1 por estação) | rodízio dos 3 degradês |
| Peças que voam | 26 | todo recorte, foto e objeto físico (os objetos de efeito, como silhuetas, spot e engrenagens, entram pelos próprios `ev`) |
| Montagens | 5, com 37 planos, nas pausas de 1,08 · 1,48 · 1,98 · 3,04 · 2,6 s | plano 0,12–0,4 s; cabe na pausa |
| SFX | 26, 1 a cada 5,5 s; mínimo de 1,2 s entre dois | ~1 a cada 5 s; ≥ 1,15 s |
| Cortes só voz da trilha | 7 (20,4 s no total) | nos momentos tensos ou de ênfase |
| Elementos | 268: papel 97, texto 87, luz 31, objeto 27 (24 tipos), recorte 8, foto 7, fita 5, traço 5, marca 1 | — |

## Mural e câmera
**Layout em serpentina** (`criarMural` em `lib/mural.mjs`)
- `celulas: {1: [ids…], 2: […]}`: uma coluna por bloco; a última termina em `CARD`.
- Coluna de 1.500 px (`COLW`) e linha de 1.900 px (`ROWH`). Bloco ímpar desce, bloco par sobe.
- Desvio sorteado com semente fixa (1234567): ±160 px em x, ±120 px em y, ±2,5°.
- Estação-filha (sem célula própria) reaproveita a de outra, com outro alvo de câmera ou outra escala: E06 na E05; E12 dentro do celular da E11 (k 0,42); E16 e E17 na E15.
- **A ordem das chamadas no gerador importa** (ids, sementes e sorteio dependem dela): estações (`ctx`/`base`/`alvo`/`extraCam`) → `caminho()` → estação do mural inteiro → `card()` → `decoracao()` → `camera()` → `voaBoia()` → `degrades()` → `sfx(plano)` → `trilha()` → `gravar()`.

**Chave de câmera:** `{t, x, y, zoom, rot, curva, arco}`. O zoom é interpolado em escala log; a `curva` vale para o trecho que chega na chave; `arco` = recuo de zoom no meio do trecho (0,22 = 22%), que transforma o chicote num arco suave.

**Curvas** (`CURVAS_LAB` em `camera.ts`): `suave`, `entrada` (expo-out), `saida`, `linear`, `expo`, `assento` (do kit) + `snap` (bezier 0,3/1,45/0,45/1, overshoot curto) e `chicote` (0,9/0/0,1/1). `snap` e `chicote` só existem no `camera.ts`.

**Chegada por tipo** (`CHEGADA` em `lib/mural.mjs`)

| Chegada | dur (s) | Curva | Arco | Extra | Uso no piloto |
|---|---|---|---|---|---|
| `abre` | 0 | — | — | zoom 0,98 do alvo | 1ª estação |
| `chicote` | 0,55 | `suave` | 0,22 | — | troca de bloco, pausa curta (E02, E08, E11, E14, E23, E27) |
| `deslize` | 0,8 | `suave` | 0,06 | **padrão** (texto sem nome conhecido) | a maioria |
| `snap` / `snap-zoom` | 0,32 | `snap` | 0 | — | entrar num detalhe (E04, E06, E16, E21, E32) |
| `giro` | 0,6 | `suave` | 0,1 | rot ±8°, alternando por estação | E18, E33 |
| `queda` | 0,45 | `assento` | 0,04 | — | E09 |
| `recuo` | 0,7 | `suave` | 0,35 | — | sair de um detalhe (E17, E20, E30) |
| `recursao` | 0,6 | `expo` | 0 | — | a estação mora dentro de uma peça (E12 no celular) |
| `emerge` | 0,45 | `assento` | — | feita pela montagem | estação depois de cada montagem |

- **Início da chegada:** `ts = max(fim da fala anterior − 0,05; 1ª palavra − 0,8 × dur; última chave + 0,05)`; `te = ts + dur` = o instante em que a câmera "chegou".
- **Punch-in na palavra-chave:** de `tc − 0,02` a `tc + 0,16` s, zoom × 1,055 e 8 px para cima, curva `snap`. Pulado se cair a < 0,12 s da última chave, a < 0,35 s da próxima estação ou a < 0,8 s de uma chave própria da estação.
- **Deriva:** zoom × 1,03 (`suave`) até o fim da estação (0,6 s antes da 1ª palavra da seguinte, ou 0,03 s antes da montagem).
- **Chaves próprias** (`extraCam[id] = [{t, dx, dy, zoom, rot, curva}]`): viagem dentro da estação (ex.: E29 desce a lista longa; E30 recua para mostrar as engrenagens; E33 gira com a espiral).
- **Câmera viva** (`viva` 5): ruído de ±5 px na tela, zoom ±0,6%, rotação ±0,25°, também com a câmera parada.
- **Montagem (mergulho, teleporte, emergência):** segura no início da pausa → mergulha na peça (`mergulho: {Mn: [estação, dx, dy]}`) com zoom (1/k) × 3,4 em `saida`, no tempo da entrada → 0,03 s depois salta escondida (`linear`) para a estação seguinte, já com zoom × 3,4 → segura até o fim dos planos → emerge com `assento` em max(0,45 s; saída + 0,2 s). Falta o mergulho de uma montagem? O gerador para com erro.
- **Recuo final** (`final: {de, recuo, card, tRecuo, tMural, tSegura, tSai, tCard}`): as chaves depois de `tRecuo` saem; a câmera vai a meio caminho entre a última estação e o centro do mural, com zoom 0,32, em `tMural`; chega ao mural inteiro 1,6 s depois, cresce × 1,02 e × 1,03, sobe para o card com zoom 0,35 em `tCard − 0,1`, assenta no zoom 1 em `tCard + 0,7` (`assento`) e termina em 1,04.
- **Zoom do mural inteiro:** `min(1080/largura, 1920/altura) × 0,96` do retângulo das células com folga de 700 px nas laterais e 1.100 px em cima e embaixo.
- **Motion blur de câmera:** liga quando a velocidade na tela passa de 18 px por quadro (`limiar`). Rastro = velocidade × obturador 0,5; de 3 a 8 cópias sub-quadro (`maxAmostras`), uma a cada 14 px (`espaco`), somadas em `plus-lighter`. Com cópias a mais de 5 px, um blur leve de meio espaçamento no conjunto. Desligado enquanto a montagem cobre a tela.
- **Fundo infinito:** ladrilho preto-fosco de 512 px que anda a 0,4 da câmera (mais longe que o plano de fundo).

## Elementos e entradas
**Tipos de elemento** (`tipos.ts`; desenho em `elementos.tsx`; atalho no `ctx` do mural)

| Tipo | Campos próprios | Atalho e padrões do mural |
|---|---|---|
| `papel` | `cor`, `semente`, `vincos`, `colunas` (texto fantasma em barras), `rasgado` | `c.papel(dx, dy, w, h, o)`; `base(c, look)` = papel 1040×1640 do look + luz. Sombra de contato, filete de luz na borda de cima, borda rasgada |
| `foto` | `src`, `borda` (14), `halftone`, `zoomInterno` | `c.foto(src, dx, dy, w, h, o)`: `voa` 0,36 s, rot ±2°, zoom interno 1 → 1,07. Borda creme `#E4DED2` rasgada; halftone de 6 px (desligar com `halftone: false` nas fotos que já vêm halftone) |
| `recorte` | `src` (PNG com alfa) | `c.rec(src, dx, dy, w, h, o)`: `voa` 0,42 s, boia 1 |
| `texto` | `palavras [{t, w}]`, `escala` (`apoio`, `chave`, `capitulo`), `tamanho`, `cor`, `alinhar`, `recua`, `torto`, `degrade` | `c.tx(frase, escala, dx, dy, o)`: as palavras saem do áudio (cada uma entra 0,03 s antes da fala dela); largura 940; chave com `cor: 'marca'` e `tamChave` |
| `objeto` | `nome`, `ev {}`, `p {}` | `c.obj(nome, dx, dy, w, h, ev, p, o)`; `o.voa: true` = `voa` 0,36 s |
| `marca` | `cor`, `dur` | `c.marca(dx, dy, w, h, ini)`: marca-texto azul elétrico que se desenha em 0,26 s, borda rasgada, −1,5° |
| `fita` | `semente` | `c.fita(dx, dy, ini, rot)`: 230×56, −30°, `pousa`, passo 2; não boia (segura a peça) |
| `traco` | `d`, `vb`, `cor`, `espessura`, `dur` | `c.traco(d, vb, dx, dy, w, ini, o)`: desenho em 0,4 s (curva `risco`), passo 3, treme ±1,5 px, espessura 6, tinta clara (azul elétrico nos destaques) |
| `luz` | `cor`, `forca` | `c.luz(forca)`: poço radial em `screen`, 1.500 px, 0,07 (0,1 no mármore) |

- **Campos de base:** `id`, `x`, `y` (centro, no mundo), `w`, `h`, `rot`, `plano`, `ini`, `fim` (sem `fim`, a peça fica até o fim do vídeo, o que permite o mural inteiro), `entra`, `passo`, `boia`, `boiaId`.
- **Saída** (quando há `fim`): blur 8 + fade em 0,13 s.

**Entradas** (`entra: {tipo, dur, de, dist}`; duração padrão em `DUR_PADRAO`)

| Entrada | dur (s) | Como |
|---|---|---|
| `surge` | 0,25 | fade (padrão sem `entra`) |
| `pousa` | 0,4 | mola `snappy`: escala 1,18 → 1, giro 7° → 0, cai de −50 px; opacidade em 0,08 s |
| `sobe` | 0,24 | sobe 70 px, blur 10 → 0 (expo-out) |
| `escala` | 0,15 | 0,9 → 1, blur 8 → 0 |
| `slam` | 0,16 | 1,55 → 1, blur 6 → 0; no texto, cada palavra 1,45 → 1 com opacidade em 0,05 s |
| `desliza` | 0,3 | atravessa 900 px da direita, blur 12 → 0, giro 4° → 0 |
| `voa` | 0,42 (padrão; o mural usa 0,36 em foto e objeto) | ver abaixo |
| `nenhuma` | 0 | — |

**`voa`, todos os parâmetros** (`elementos.tsx` + `M.voaBoia()`)
- Vem de fora: `dist` 1.400 px do mundo, do lado `de` (`esq`, `dir`, `baixo`, `cima`, `ne`, `no`, `se`, `so`).
- O mural escolhe o lado pelo setor de 45° em que a peça mora em relação ao alvo da câmera. Peça a < 160 px do centro alterna baixo → esq → cima → dir.
- Curva `entrada` (expo-out): quase todo o caminho nos primeiros ~0,12 s, assenta macio.
- Trajetória em arco: desvio lateral de sen(π·(1−p)) × dist × 0,24.
- Giro de ±24° → 0; escala 1,12 → 1; blur 18 × (1−p)^1,5 → 0; opacidade em 0,04 s.
- **Só começa 0,05 s depois que a câmera chega na estação** (`ini = max(ini, chegou + 0,05)`). O `voaBoia` tira o `passo` da peça que voa.

**Boiar** (deriva orgânica depois que a peça entra; rampa de 0,5 s)
- ±7 px em x, ±9 px em y, ±1,1°, ±1% de escala, × a intensidade `boia`.
- Padrão: recorte 1, foto 0,7, objeto 0,8, texto 0,3 (o texto usa metade), traço 0. Papel, fita, marca e luz não boiam.
- Estação em escala k: o mural multiplica a intensidade por k (o mesmo "boiando" na tela).
- **Não boia** (`boia: 0`): peça presa com fita, peça que contém outra estação (o celular da E11), foto com persiana por cima, o coração preso pela fita.
- `boiaId`: boia junto com outra peça, sem rampa (a rachadura sobre a mão da E18).

**Passos (feito à mão):** `passo` 1 = 24 fps; **2 = 12 fps** (fita, papel que pousa, papéis do card); **3 = 8 fps** (traço que treme). A câmera e o blur seguem em 24 fps. Dentro dos objetos: `riscos` em passo 3; `bateria`, `calendario`, `lista`, `folhas`, `agenda` e `caminho` em passo 2.

**Planos de parallax** (`PARALLAX`): `fundo` 0,55 · `meio` 1 · `frente` 1,35.
- Decoração automática (`M.decoracao()`), por célula: uma folha grande `#141215` de 1.300×1.000 no fundo e uma lasca `#26221F` de 140–210 × 180–250 px na frente, no canto (± 640 px em x, ± 980 px em y), fora da zona de texto.

**Camadas dentro de cada plano** (`camada()` em `PaperVox.tsx`)

| Camada | O que fica nela |
|---|---|
| 0 | papel, foto, recorte, objeto, marca, fita, luz |
| 1 | **texto** (sempre por cima das peças) |
| 2 | traço à mão e o objeto `flash` (o risco que corta a palavra continua cortando) |

- A ordem do `quadro.json` vale dentro de cada camada.
- **Entre planos, a frente fica por cima do meio:** as lascas da frente podem passar por cima do texto do meio. Por isso ficam nos cantos, fora da zona de texto.

## Objetos de papel (catálogo)
Desenhados em código em `objetos.tsx` (SVG e CSS, nada é imagem gerada), cada um numa caixa w×h do mundo. `ev` = instantes (s) ancorados nas palavras pelo gerador; `p` = parâmetros. Texto dentro de objeto sempre em HTML.

| Objeto | `ev` | `p` | Uso no piloto |
|---|---|---|---|
| `silhuetas` | `entra` (uma cabeça a cada 2 q), `tinta` | `n` (7) | E03 "uma sociedade que adoece": cabeças iguais, sem rosto, tinta azul elétrico em "adoece" |
| `aspas` | `entra` (mola `snappy`) | — | E04 "chama isso de liberdade" |
| `carimbo` | `bate` (escala 1,8 → 1 em 0,12 s, tremor de 3 q) | `texto`, `tamanho` (150) | E06 "culpa" (rot −9°) |
| `riscos` | `desenha` (passo 3, 0,05 s entre riscos) | `n` (4) | E08 "correndo" |
| `persiana` | `passa` (1,4 s) | — | E09, sobre a foto (que não boia) |
| `bateria` | `esvazia` (1 s, passo 2), `pisca` (0,75 s) | — | E10 "sem energia" |
| `celular` | `rola` (620 px/s) | — | E11 "tela de celular"; contém a E12 (não boia) |
| `relogio` | `gira` | — | E11 "horas" |
| `calendario` | `monta`, `marca`, `repete` (passo 2) | — | E12 "sedentarismo … rotineiro" |
| `lista` | `checks`, `cresce`, `marca` (passo 2) | `n` (8), `altura` (84), `rotulo`, `idx` (5) | E13 "autocuidado"; E29 lista de 40 linhas com "o próprio corpo" no último lugar |
| `manometro` | — | `niveis [[t, valor 0–1]]` (o último ≥ 0,99 em `snap`; treme acima de 0,9; faixa azul elétrico de 0,8 a 1) | E15 "pressão social" |
| `spot` | `acende`, `apaga` (0,3 s) | — | E16 "Exatamente"; E27 "exausto" |
| `espelho` | `foco` (blur 12 → 0 em 0,4 s) | `src` (o recorte, espelhado) | E19 "si mesma" |
| `coracao` | `rasga` (0,3 s), `cai` (0,8 s) | — | E22 "romantizar o adoecimento" (preso com fita) |
| `folhas` | `vira` (passo 2, 3 q entre folhas) | — | E23 "deixo para depois" |
| `perfis` | `surge`, `fio`, `vibra`, `pulso` | — | E24 "a saúde do outro importa" |
| `balanca` | `desce`, `oscila`, `afunda`, `volta` | — | E26 "não quer abrir mão de nada" (pratos vazios, sem ponteiro e sem número) |
| `agenda` | `cai`, `tenta`, `empurra` (passo 2) | `rotulo` | E28 "saúde … prioridades" |
| `engrenagens` | — | `gears [{x, y, r, n, dir, ini, para}]` | E30 "produtividade de máquina", E31; todas param no "Mas" da E32 |
| `espiral` | `desenha`, `fecha`, `acelera` | `voltas` (4,5) | E33 "obsessão" |
| `caminho` | `desenha`, `fim`, `acende` (passo 2) | `d`, `espessura` (14; o mural usa 30) | o traço que liga o mural (`M.caminho()`) |
| `fichas` | `separa` (0,45 s) | — | E20 "confunda as coisas" |
| `icones` | `entra` (0,12 s entre eles) | — | Instagram e YouTube, só no card |
| `flash` | `em` (azul elétrico em `screen`: 2 q a 0,8 + 1 q a 0,35) | — | E17 "Pressão". **No máximo 2 por vídeo**; fica na camada de cima |

- **Objeto novo é peça nova num modelo fixo:** só entra com ⏸ do Jorge. Proponha na shot list (camada marcada "objeto novo") e peça o ok dele. Quem implementa é a conversa principal (o `diretor-paper-vox` não mexe em `src/`): componente + linha no `MAPA` do `objetos.tsx`, conferência com `quadros.mjs` e depois a regressão (ver "Checagens", item 11), antes do P5.
- Nome fora do `MAPA`: o gerador do mural **para com erro** no `M.gravar()` (antes, o render não acusava e a peça sumia).
- Cabeça é sempre a forma simples sem rosto (`CABECA` no `objetos.tsx`).

## Montagens
- **Onde:** só nos silêncios da fala (pausas longas). Piloto: 5 montagens em pausas de 1,08 a 3,04 s.
- **Validador (ERRO):** plano fora de 0,12–0,4 s; planos + entrada + saída maior que a pausa + 0,3 s; palavra da fala dentro da montagem.
- **Medidas do piloto:** entrada de 0,25–0,4 s; saída de 0,1–0,3 s; 4–10 planos de 0,2 s. Na maior pausa (3,04 s), rampa que acelera: 0,3 → 0,15 s, com o último plano segurando 0,2 s.
- **Como aparece** (`Montagem` em `PaperVox.tsx`):
  - entrada: a tela do 1º plano cresce de 2,2 → 1 de dentro do mergulho, com blur 14 → 0;
  - planos em tela cheia, em P&B (contraste 1,08), com movimento em rodízio `push` → `pan-e` → `pull` → `pan-d` → `tilt`;
  - cada troca: 2 q de blur 9 + clarão de 35%;
  - saída: encolhe 1 → 0,45 com blur 12 e some enquanto a câmera emerge.
- **Planos:** stills 9:16 do Flow (bloco MONT), em `04_broll/ia_flow/Mnn.jpg`. Só mãos, objetos e gente de costas; telas e papéis ilegíveis.
- **Sem repetição visual.** Confira na `shotlist.json` que nenhuma `fonte` (`flow:Fnn`, `flow:Mnn`, `biblioteca:<arquivo>`) aparece em duas estações ou planos de montagem: o `validar-shotlist.mjs` só conta o teto. Repetições entre montagens viram rima de propósito (no piloto, a M4 "escolhas" rima com a M3 "deixar para depois": tênis na caixa → amarrando o cadarço).
- **Plano claro demais** (área clara > 15%): `escurecer` no gerador (piloto: M27 0,68; M25 0,85).
- **Som:** o plano de montagem não tem SFX. Antes dela entra um whoosh (início da montagem − 0,05 s) ou um swell/riser com o pico no mergulho; a trilha sobe um pouco na pausa (`volSemFala`). Uma montagem pode entrar sem SFX quando a trilha volta (M1 do piloto).
- **Gerador:** `mergulho: {M1: ['E06', 40, 170], …}` = estação e deslocamento da peça onde a câmera some. A montagem casa com as estações pelos tempos (fim da estação de antes = início da pausa; início da seguinte = fim da pausa, ±0,02 s).

## Tipografia
Fonte A, sem fonte nova: Inter Tight + Instrument Serif itálica (`src/kit/fontes.ts`).

| Papel | Fonte | Tamanho (px do mundo) | Entrada | Cor | Uso |
|---|---|---|---|---|---|
| Apoio | Inter Tight 600, −0,01em, linha 1,1 | 64 (padrão); 44–60 no card; 46 nos rótulos de ícone | palavra a palavra: blur 8 → 0 e 0,9 → 1 em 0,15 s | `#F2F4F8` com sombra `0 4px 24px rgba(0,0,0,.65)` | o resto da frase, em geral acima da chave |
| Chave | Instrument Serif itálica, −0,02em, linha 0,95 | `tamChave(frase, 920)`, até 210; explícito de 120 a 250; escala extrema até 520 ("não") | igual, em 0,2 s; ou `slam` | `cor: 'marca'` = um dos 3 degradês | 1 palavra-chave por estação; punch-in da câmera |
| Capítulo | Instrument Serif itálica | 560 | — | — | existe no código; não foi usado no piloto |
| Carimbo | Inter Tight 900, caixa-alta, +0,1em | 150 (140 no piloto) | `bate` | azul elétrico | objeto `carimbo` |
| Card | chave e apoio | "Jorge Souto" 170 · profissão 56 · CREF 44 · @ 60 | em cascata (0,3 → 1,3 s) | nome no degradê; o resto `#F2F4F8` | fixo |
| Mural inteiro | chave e apoio | tamanho × 1/zoom do mural (≈ × 10: 70 → 717; 200 → 2.049) | — | **até o apoio no degradê** (o branco some sobre as fotos) | estação do recuo final |

- **`tamChave(t, larg, max)`** = `round(min(max, larg ÷ (letras da maior palavra × 0,47)))`, com `larg` 920 e `max` 210 no `ctx`.
- **Truques de texto:** `recua` (a palavra gigante encolhe até virar legenda, curva `expo`, 0,6 s; E04, E21); `torto` (letras caem uma a uma e tremem a 8 fps; E32); `rot` inclinado (E08); branco sobre a marca azul elétrico (E02).
- **Sem legenda separada:** na tela entram só os trechos da fala escolhidos na shot list (apoio + chave). Todo texto de tela vem da fala da estação (ERRO no validador).
- **Texto sempre em HTML**, nunca `<text>` dentro de SVG.

**Degradês da marca** (`DEGRADES` em `elementos.tsx`; `linear-gradient(100deg, …)`)

| Nome | Cores (paradas) |
|---|---|
| `nevoa-eletrico` | `#C0C8F0` 0% → `#8C9BE4` 52% → `#2E49CE` 100% |
| `claro-aco` | `#DCE1ED` 0% → `#C0C8F0` 45% → `#8C9BE4` 100% |
| `eletrico-aco` | `#1F33A3` 0% → `#2E49CE` 55% → `#8C9BE4` 100% |

- **Rodízio** (`M.degrades()`): por ordem de entrada, salmão-vermelho → eletrico-aco → salmão-laranja → …; dois seguidos nunca iguais. Piloto: 12, 11 e 11.
- Aplicado com `background-clip: text` no próprio nó de cada palavra, cor transparente, `paddingRight: 0.06em` (a itálica não corta) e sombra por `drop-shadow(0 6px 18px rgba(0,0,0,.7))`.

## Cor e acabamento
| Papel | Hex | Uso |
|---|---|---|
| Preto-fosco (fundo) | `#0E0C10` | fundo infinito, montagem |
| Carvão | `#1C1A18` | papel do look `editorial` (com colunas de texto fantasma e vincos) |
| Papelão | `#2E2620` | papel do look `colagem` (o `#4A3A2A` existe no `COR`) |
| Mármore | `#141316` | papel do look `marmore` |
| Folha de fundo / tela | `#141215` | decoração do plano de fundo; tela da E12 |
| Lasca da frente | `#26221F` | decoração do plano da frente |
| Papéis do card | `#2B2522`; papel em branco `#1E1B19` | card |
| Tinta clara (texto) | `#F2F4F8` | apoio, traço, objetos |
| Azul elétrico (marca) | `#2E49CE` | marca-texto, carimbo, flash, acentos dos objetos. **Nunca como cor de texto sobre o escuro** |
| Borda da foto | `#E4DED2` | moldura rasgada |
| Sombra dos objetos | `#2A2624` | engrenagens e afins |

- **100% dark:** área clara ≤ 15% do quadro (conta fundo, papel e superfície; texto e traço não contam). Não há script que meça: conferência visual na folha de contato e na folha de quadros. O plano claro de montagem é escurecido no código (`escurecer`).
- **Acabamento** (`Acabamento` em `PaperVox.tsx`, por cima de tudo):
  - poço de luz radial (70% × 55%, centro em y 45%) a 6% de `#F2F4F8` em `screen`;
  - vinheta radial (85% × 75%) até 62% de preto;
  - grão `grao` 0,09 (`Grao` do kit).
- **Papel:** sombra de contato `0 28px 60px rgba(0,0,0,.75)`, filete `inset 0 2px 0 rgba(242,239,234,.16)`, borda rasgada, textura com manchas, grão, fibras, colunas de texto fantasma (só barras, nunca letra) e vincos (`texturas.ts`). A textura segura o quadro até decodificar (`delayRender`): sem isso, um quadro podia sair sem grão nem fibras e dois renders do mesmo código diferiam mais (PSNR mín. 41 dB; agora ≥ 42–44 dB).
- **Foto:** P&B, sombra `0 30px 70px rgba(0,0,0,.8)`, halftone de 6 px em `multiply` a 55%.
- **Flash:** só azul elétrico, 2 q, no máximo 2 por vídeo. Nunca branco.

## Imagens
- **Origem:** stills do Google Flow com **Nano Banana 2.1 = 0 crédito** (conferir a linha "A geração vai usar 0 créditos"). Sem vídeo gerado. Fotos da biblioteca (`%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel`) viram P&B no gerador (`pb()`: 1.200 px, contraste 1,22, brilho −0,05, cópia em `04_broll/meus/*_pb.jpg`).
- **Três blocos de prompt** (texto exato em `prompts-flow.md`):
  - **FOTO** (foto do jornal ou da estação, halftone P&B, 3:4 ou 4:3);
  - **RECORTE** (objeto ou estátua em fundo azul `#0000FF`, 1:1);
  - **MONT** (plano de montagem, 9:16, P&B cinematográfico de pouca luz).
- **Ids:** `Fnn` nas estações (fotos e recortes), `Mnn` nas montagens. Variações: x2 (x4 nas de destaque).
- **P&B sempre:** as fotos já vêm halftone; os recortes passam por `--pb`; os planos de montagem são P&B no código.
- **Recorte:** `node scripts/recorte-chroma.mjs <proj>/04_broll/ia_flow/<id>.jpg <proj>/04_broll/ia_flow/recortes/<id>.png --pb --aparar [--choke 1|2]` (de dentro do motor, com os caminhos completos: o script não recebe `<proj>`; comando inteiro em `prompts-flow.md`). A cor-chave é medida nos 4 cantos; halo > 3% (> 6% com `--pb`) = refazer. Objeto fino (tubo, fio) pede `--choke`.
- **Resolução:** o "Baixar lote" entrega 1K, que serve só para escolher. **A escolhida se baixa em 2K.** Os planos de montagem são ampliados 1,6–1,8× no final.
- **Escolha:** agente `diretor-de-arte` (da frente de carrosséis) dá a nota de cada variação em `04_broll/ia_flow/escolhas.json` (`{id: {v, nota}}`) → folha de contato `06_previas/imagens-escolhidas_<n>.jpg` → ⏸ Jorge.
- **Pastas:** escolhidas em `04_broll/ia_flow/<id>.jpg`; recortes em `04_broll/ia_flow/recortes/Fnn.png`; variações em `04_broll/ia_flow/_brutos/<id>/` até a prévia ser aprovada (guarde a variante escolhida antes de apagar, para poder recortar de novo).
- **Orçamento:** teto de 25 imagens por minuto (ERRO); ≥ 35% das estações sem imagem (AVISO). Piloto: 47 do Flow + 5 da biblioteca.
- Texto nunca dentro da imagem.

## Áudio
### Voz
- A voz do Jorge é a base: a composição toca `01_bruto/bruto.mp3` (ou `.wav`/`.m4a`) desde `vozIni`.
- Na etapa 0, perguntar "Ajustar o áudio?" (`tratar-voz.mjs`/`estudio-audio.mjs` só se ele marcar). O piloto já veio tratado (voz a −19,8 LUFS).
- Se ele marcar e escolher uma versão, ela entra no gerador do mural: `criarMural(PROJ, {celulas, voz: '05_audio/<arquivo>.wav'})`. Sem `voz`, o mural volta sozinho para o `01_bruto/bruto.*`, e o volume da trilha e dos SFX é medido sobre a voz que entrar.

### SFX
**Banco por categoria** (`BANCO` em `lib/mural.mjs`; a biblioteca `sfx/lab/` já é de produção, não mover). Alvos para voz a −19,8 LUFS; com outra gravação, andam junto com a voz (`vozI`).

| Categoria | Fonte | Alvo M máx. | Alvo de pico | Uso (piloto) |
|---|---|---|---|---|
| `whoosh` | Motionix `whooshes` (fast, simple, short, mediam, smooth-and-fast) | −32 | −17 | mergulhos e viagens grandes (6) |
| `impacto` | `sfx/lab/impacto` + `impact_sub` | −31 | −13 | onde a trilha corta (5) |
| `papel` (pestana) | `05_audio/sfx/lab/papel/` do projeto, se houver; senão `sfx/lab/papel/` (6 sintetizados, até o Mixkit chegar) | −35 | −24 | carimbo, card (2) |
| `gear` | Motionix `gear` | −34 | −22 | manômetro, engrenagens (2) |
| `riser` | Motionix `risers` | −33 | −19 | viradas (2) |
| `swell` | `reverse_swell`, `shimmer` (`sfx/biblioteca`) | −33 | −19 | viradas, mural inteiro (2) |
| `scroll-ui` | `sfx/lab/scroll-ui` | −36 | −26 | celular, lista longa (2) |
| `ui` | Motionix `ui-sound-effects` (click, button, enter, open, select) | −36 | −25 | bateria (1) |
| `glitch` | `sfx/lab/glitch` (8 primeiros) | −35 | −25 | "polêmica" (1) |
| `clique` | `sfx/lab/clique` | −27 (padrão) | −25 | spot que acende (1) |
| `ding` | `sfx/lab/ding` | −35 | −24 | perfis ligados (1) |
| `pop` | Motionix `pop` | −36 | −24 | ícones (1) |

- Som curto (< 0,4 s) se mede pelo pico; o longo, pelo menor entre o M máx. e o pico. `vol` = 10^(dB/20), teto 1, × o multiplicador da linha do plano.
- **Regras** (travas do Jorge, o gerador para com erro):
  - ~1 SFX a cada 5 s, 12–17 dB abaixo da voz;
  - **≥ 1,15 s entre dois SFX**;
  - **nunca a mesma categoria em seguida** (e nunca o mesmo arquivo: o banco gira).
- **Só nos acentos:** impacto onde a trilha corta, whoosh nos mergulhos e viagens grandes, swell/riser nas viradas, um som próprio por objeto.
- **Sem som:** entrada de imagem, papel, fita e plano de montagem.
- O plano do gerador é a lista curada; os `sfx` da shot list são só candidatos.

### Refino milimétrico (P7, para todo vídeo novo)
- **Por quê:** a composição só acerta a grade de 1/24 s (41,7 ms) e o ponto que "bate" em cada som é diferente. O riser premium da Motionix bate no começo e decai (pico em 0,05 s): no piloto, posto para "terminar no mergulho", soou 2,3 s antes. O reverse swell tem o pico a 0,89 s de 1,21 s, não no fim. **Medir, não supor.**
- **Cada SFX declara o instante visual** (use depois de `M.camera()` e `M.voaBoia()`):

  | `M.ev.*` | Instante |
  |---|---|
  | `palavra(id, frase, n)` | início da palavra |
  | `slam(textoEl)` | a palavra bate (90% da escala) |
  | `pouso(el)` | a peça que voa assenta (92% do caminho) |
  | `viagem(id)` | meio da viagem da câmera até a estação (velocidade máxima) |
  | `chegada(id)` | a câmera chega |
  | `mergulho(j)` | a câmera some na peça da montagem j |
  | `objeto(el, chave, atraso)` | evento interno de um objeto (ex.: `'bate'` do carimbo) |
  | `em(tipo, t)` | instante livre |

- **Ponto do som** que cai no evento: `ataque` (o transiente: impacto, papel, clique, pop, ding, glitch, ui, gear) ou `pico` (whoosh, riser, swell; `ALVO_PADRAO`). Medido no arquivo (`pontosDoSom`: envelope de 5 ms; ataque refinado na amostra). O `alvo` só aceita `'ataque'` ou `'pico'` (`SfxLab` em `tipos.ts`).
- **Cache das medidas:** `05_audio/sfx/lab/medidas.json` do projeto. Os instantes ficam em `t_ataque`/`t_pico` (s no arquivo), separados do `pico` (nível em dB) da medida de volume.
- **Linha do plano:** `[null, 'whoosh', 0.8, M.ev.viagem('E05'), {ajuste: 0}]` (opcional `alvo: 'ataque' | 'pico'`) e `M.sfx(plano, {naMixagem: true})`. Com `sfxNaMixagem`, a composição não toca os SFX e o `mixar-audio.mjs` põe cada um na amostra exata.
- **Ciclo:** `refinar-sfx.mjs <proj> --video <prévia com trilha>` → `03_roteiro/sfx_refino.md` (cada SFX: evento, ponto do som, desvio em ms, quadro) + carretel `06_previas/sfx-refino_<data>.mp4` (1 clipe de 1,5 s por SFX, número e evento escritos, barra azul elétrico no quadro exato) → o Jorge ouve e pede "o 7 entra 2 quadros antes" → `{ajuste: -83}` (ms; negativo = antes) no plano → gerador → `node scripts/mixar-audio.mjs <proj> --video 06_previas/previa_<AAAAMMDDHHMM>_paper.base.mp4 --props 03_roteiro/quadro.json --trilha <X> [--saida …]` (segundos; sem `--saida`, sai `…_paper.base_trilha-<X>.mp4`, o `--video` do `refinar-sfx.mjs` seguinte) → carretel novo → ⏸.

### Trilha
- **Da biblioteca** (`%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/`; o gerador para se o arquivo não estiver lá). **2 opções** mixadas para comparar (A e B) em toda prévia (regra do fluxo).
- **Trilha nova:** sem 2 opções adequadas no `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/catalogo.md` (evite as do vídeo anterior)? Busque no Pixabay Music conforme o arco, ⏸ apresente 2–3 com link, duração e Content ID e baixe só as aprovadas **direto em `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/`** (o `lib/mural.mjs` recusa trilha fora de lá; não use `05_audio/musica`). Depois, acrescente a linha no `catalogo.md`.
- **≤ 1/4 da voz** (`volTrilha`): com fala, o pico curto da trilha (S máx.) fica 13 dB abaixo da voz; sem fala (pausas ≥ 0,5 s e montagens), 12 dB.
- **Cortes só voz** nos momentos tensos ou de ênfase: a trilha para seco em 12 ms e volta em 0,12 s com a frase seguinte. No gerador: `fimFala(id)` = fim da fala + 0,06 s; `ateProxima(id)` = o silêncio segura até 0,08 s antes da frase seguinte.
- **Fade de 2,5 s** no card. Loudness final −14 LUFS / −1 dBTP em 2 passadas lineares (`mixar-audio.mjs`).
- **Piloto:** A = `suspense_mystery-detective-investigation_ViacheslavStarostin_pixabay.mp3` desde 0,7 s (vol 0,0624 com fala, 0,07 sem; S máx. −8,7), a escolhida; B = `documentary_string-quartet_The-Mountain_pixabay.mp3` desde 0 (0,055 / 0,0617; S máx. −7,6). 7 cortes, 24 pausas. **As duas têm Content ID no YouTube.**

## Ética (CFN e regras visuais do formato)
- **CFN:** sem promessa de resultado, sem antes/depois, sem depoimento, sem prescrição individual, sem preço. Card com nome + CREF 000000-G/UF.
- **Texto de tela:** só da fala da estação (ERRO); palavra em dúvida fora da tela até o Jorge responder (ERRO); palavras vetadas: promessa, cura, curar, garantia, garantido(a), 100%, milagre, definitivo(a) (ERRO). O `checador-de-afirmacoes` roda sobre o texto de tela antes das imagens, recebendo a fala de cada estação e o aviso: a fala está gravada, então correção só com palavras da própria fala (ou no visual). Grava em `03_roteiro/checagem-texto-tela.md` (modelo: o do piloto).
- **Nenhum corpo no tema emagrecimento:** cabeças iguais e sem rosto; estátua só com cabeça e ombros; balança sem ponteiro e sem número.
- **Montagens** só com mãos, objetos e gente de costas. Telas, jornais e papéis ilegíveis; sem veículo nem marca real.
- **Imagens:** sem rosto reconhecível, sem marca ou logo, sem "no estilo de", texto nunca dentro da imagem.
- Ponto de opinião vira opinião na tela (no piloto: "uma opinião polêmica"), com ressalva e fecho.

## Passo a passo (P0–P9)
Scripts de dentro do motor (`motor`); geradores de dentro do projeto. Render, alinhamento e regressão sempre pela fila (`node scripts/vez.mjs node scripts/…`). Do áudio à prévia 2 do piloto: ~5 h, com as esperas do Jorge.

| Etapa | O que fazer | Script / agente | ⏸ | Tempo (piloto) |
|---|---|---|---|---|
| P0 Entrada | Chega um ÁUDIO. `.oga` do WhatsApp → mp3 (`ffmpeg -i "<áudio>.oga" "<áudio>.mp3"`); mp3/wav/m4a direto. Projeto: `novo-projeto.mjs "<nome>" "<áudio>"` (aspas: o nome do WhatsApp costuma ter parênteses e espaços) → `01_bruto/bruto.mp3`. Pergunta da etapa 0: o formato (com áudio, este é o óbvio, mas pergunte junto) + "Ajustar o áudio?". Sem "corrigir cor" nem decupagem | `novo-projeto.mjs` | ⏸ etapa 0 | — |
| P1 Transcrição | **Nesta ordem:** `transcrever.mjs <proj>/01_bruto/bruto.mp3 <proj>/02_analise --principal` → `02_analise/correcoes.json` (à mão) → `corrigir-palavras.mjs <proj> <proj>/02_analise/correcoes.json` → `alinhar-palavras.mjs <proj>` → `02_analise/transcricao_corrigida.md` (à mão) com as dúvidas ⚠ (ver "P1 em detalhe") | `transcrever`, `corrigir-palavras`, `alinhar-palavras`; conversa principal | ⏸ dúvidas | transcrição ~1 min; alinhamento ~2 min para 142 s (placa de vídeo, desde 2026-10-27) |
| P2 Proposta de cenas | Copiar o `montar_shotlist.mjs` do piloto para `03_roteiro/` e reescrever o criativo (ver `shotlist-esquema.md`) → `node 03_roteiro/montar_shotlist.mjs` → `shotlist.json`/`.md` → `validar-shotlist.mjs <proj>` 0 ERRO → repetição visual conferida → `checador-de-afirmacoes` com o texto de tela e a fala de cada estação → `03_roteiro/checagem-texto-tela.md` (ver "P2 em detalhe") | agente `diretor-paper-vox` (modo "cenas"); `checador-de-afirmacoes` | ⏸ shot list (+ objeto novo, se houver) | — |
| P3 Prompts do Flow | `03_roteiro/prompts_flow.md` e `.json` (blocos FOTO, RECORTE, MONT) | `diretor-paper-vox` (modo "prompts"); `prompts-flow.md` | ⏸ prompts | — |
| P4 Imagens | Geração no Flow pelo Chrome do Jorge (0 crédito) → escolha → 2K da escolhida → `recorte-chroma.mjs <proj>/04_broll/ia_flow/<id>.jpg <proj>/04_broll/ia_flow/recortes/<id>.png --pb --aparar [--choke 1-2]` → folha de contato | Claude in Chrome; `diretor-de-arte` | ⏸ imagens | operação estimada em 45–60 min |
| P5 Mural | Copiar o `montar_quadro.mjs` do piloto e reescrever só o criativo: células, peças de cada estação, `mergulho`, `escurecer`, `final`, plano de SFX com `M.ev.*` e `naMixagem: true`, cortes da trilha e 2 opções (trilha nova: ver Áudio › Trilha), voz tratada se houver (`criarMural(PROJ, {celulas, voz: '05_audio/<arquivo>.wav'})`) → `node 03_roteiro/montar_quadro.mjs` → `quadro.json` | `diretor-paper-vox` (modo "mural") | ⏸ trilha nova, se baixar | — |
| P6 Prévia | `render-paper-vox.mjs <proj> --previa --manter-base` → 2 versões (trilha A e B) em `06_previas/previa_<AAAAMMDDHHMM>_paper_trilha-<X>.mp4` + a base sem trilha `06_previas/previa_<AAAAMMDDHHMM>_paper.base.mp4` + folha de quadros + revisão | `render-paper-vox`; `revisor-de-video` | ⏸ prévia | ~10 min para 144 s (4,2 s/s) |
| P7 Refino dos SFX | `refinar-sfx.mjs <proj> --video <prévia com trilha>` → `sfx_refino.md` + carretel → ajustes → gerador → `mixar-audio.mjs <proj> --video 06_previas/previa_<AAAAMMDDHHMM>_paper.base.mp4 --props 03_roteiro/quadro.json --trilha <X> [--saida …]` → carretel novo | `refinar-sfx`, `mixar-audio` | ⏸ refino | mixagem em segundos |
| P8 Final | Render longo: `render-paper-vox.mjs <proj>` → `07_final/<proj>_final.mp4` com a trilha escolhida (`musica`) → folha de quadros + loudness | `render-paper-vox` | ⏸ render longo | ~30 min para 144 s (12,4 s/s) |
| P9 Fechamento | `legendista` (fonte: `02_analise/transcricao_corrigida.md` + `03_roteiro/shotlist.md`) → registro em `Publicados.md` ("Reels · PAPER VOX ANIMATION") | `legendista` | ⏸ publicar | — |

- **P1 em detalhe:** nenhum script gera o `correcoes.json` nem a `transcricao_corrigida.md`. Quem escreve os dois é a conversa principal, no molde dos do piloto (`%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece/02_analise/`).
  - `correcoes.json`: lido da `transcricao_turbo.md` + `suspeitos_turbo.json`; lista de trocas `{t, de, para}` e inserções `{t, inserir, ini, fim}` (formato no cabeçalho do `corrigir-palavras.mjs`).
  - `transcricao_corrigida.md`: escrita depois do alinhamento, a partir do `palavras.json` alinhado. Cabeçalho (áudio, passadas, nº de correções, se veio ou não de roteiro) e uma linha `- [m:ss.d] frase` por frase; embaixo de cada dúvida, `⚠ "o que se ouviu"; "alternativa"?`. O `diretor-paper-vox` (modo cenas) para sem ela.
  - Cada dúvida também entra em `duvidas` na shot list, e a palavra fica FORA da tela até o Jorge responder (por texto). Rodou o `corrigir-palavras` de novo? Rode o alinhamento depois.
- **P2 em detalhe:**
  - **Sem repetição visual:** nenhuma `fonte` (`flow:Fnn`, `flow:Mnn`, `biblioteca:<arquivo>`) em duas estações ou planos de montagem da `shotlist.json` (o `validar-shotlist.mjs` só conta o teto). Rima entre montagens só de propósito.
  - **Checador:** chame o `checador-de-afirmacoes` com o texto de tela e a fala de cada estação, avisando que a fala está gravada: correção só com palavras da própria fala (ou no visual). Resultado em `03_roteiro/checagem-texto-tela.md` (modelo: o do piloto).
  - **Objeto fora do catálogo:** vai junto com a shot list, marcado "objeto novo" (⏸ Jorge), e é implementado antes do P5 (ver "Objetos de papel").
- Mudou a trilha escolhida depois do render? `mixar-audio.mjs` na base guardada (`--manter-base`), sem renderizar de novo.
- Prévia de um trecho: `--trecho a b` (a trilha entra alinhada com `--desde`).

## Custo de render (medido no piloto)
| Item | Custo | Base |
|---|---|---|
| Prévia (meia resolução, CRF 26) | **601 s para 144 s = 4,2 s/s**; ~15,7 MB | prévia 2 |
| Final (1080×1920, CRF 17, AAC 320k) | **1.786 s para 144 s = 12,4 s/s** (~30 min); 388 MB | final do piloto |
| Quadro parado | 0,3–0,5 s por quadro | protótipo |
| Quadro de chicote com motion blur | 1,2–1,45 s por quadro (era 3,9 com um blur por cópia) | protótipo |
| Mixagem e troca de trilha | segundos (sem re-render) | `mixar-audio.mjs` |
| Alinhamento das palavras | ~2 min para 142 s na placa de vídeo (2026-10-27; era ~12 min na CPU, com a máquina carregada) | `alinhar-palavras.mjs` |

- Um render por vez (máquina de 7,7 GB de RAM, sem GPU). Avise o Jorge do tempo antes de rodar.
- Não operar o Flow com um render rodando: falta RAM e o Chrome para de responder (ver "Armadilhas").

## Checagens antes da prévia e do final
**Antes da prévia**
1. `node scripts/validar-shotlist.mjs <proj>` com **0 ERRO** (ler os avisos: buraco sem evento, estação < 1 s, chegada ou categoria 3× seguidas).
2. `checador-de-afirmacoes` aplicado ao texto de tela, com a fala de cada estação (`03_roteiro/checagem-texto-tela.md`); nenhuma palavra em dúvida na tela.
3. **Sem repetição visual:** nenhuma `fonte` repetida em duas estações ou planos de montagem da `shotlist.json` (o validador não confere).
4. O gerador do mural roda sem erro (travas de SFX, mergulho de toda montagem, alvo de câmera de toda estação, todo objeto existe no `MAPA`).
5. **Área clara ≤ 15%** em cada quadro: conferir os planos de montagem e as fotos claras na folha de contato; acima disso, `escurecer`. (Não há script para isso: conferência visual.)
6. **Folha de quadros** dos pontos novos (`node scripts/quadros.mjs <proj> <t1> <t2> … --edicao 03_roteiro/quadro.json`; a conferir na 1ª vez, porque no piloto a conferência foi na prévia).
7. **Texto coberto:** nenhum texto por baixo de foto, recorte, objeto ou linha; lascas da frente nos cantos, longe do texto.

**Antes do final**
8. `refinar-sfx.mjs` **sem avisos** (nenhum SFX sem evento, fora do quadro, colado ou com categoria repetida) e o carretel aprovado pelo Jorge.
9. Folha de quadros da prévia aprovada (`revisor-de-video`): texto coberto, área clara, peça que surge sem voar.
10. **Loudness** do final: −14 LUFS integrado, pico ≤ −1 dBTP (`ffmpeg -af ebur128=peak=true`).
11. Mexeu no motor (`src/modelos/paper-vox/`, `src/kit/`, `Root.tsx`, `render-paper-vox.mjs`, `lib/mural.mjs` ou pacotes)?
    - `node scripts/vez.mjs node scripts/regressao-paper-vox.mjs`: IDÊNTICO ou EQUIVALENTE ≥ 40 dB (limiar calibrado em `regressao-paper-vox.mjs`: o ruído entre dois renders fica ≥ 42 dB; uma palavra de 30×15 px trocada de cor dá 38,6 dB).
    - `regressao.mjs` (TELA DIVIDIDA, IDÊNTICO), `regressao.mjs --cut` (EQUIVALENTE ≥ 42 dB) e, para o MIX, `node scripts/vez.mjs node scripts/regressao.mjs --mix` (EQUIVALENTE ≥ 42 dB).
    - O gerador do piloto tem de gerar o mesmo `quadro.json`, sem sobrescrever o dele: `node <piloto>/03_roteiro/montar_quadro.mjs --saida <scratchpad>/quadro.json` e compare por md5 com o `03_roteiro/quadro.json` do piloto. Diferente = mudança do modelo (⏸ Jorge).

## Armadilhas aprendidas
1. **`<text>` dentro de SVG** saiu 2,4× maior no render longo (quadro isolado e trecho curto saíam certos). Texto sempre em HTML (o rótulo da `lista` é HTML por isso).
2. **`CURVAS.snap` não existe no kit:** `snap` e `chicote` só moram no `CURVAS_LAB` do `camera.ts`. Não pôr no kit: mudaria o CUT e o MIX.
3. **Plano da frente × 1,35 e fundo × 0,55:** a coordenada de mundo de uma peça nesses planos é a da estação × o fator; senão a peça aparece longe.
4. **Comentário `//` no meio de uma linha de estação:** as estações do gerador ficam numa linha só, e um `//` no meio apaga o resto (o `alvo()`): o gerador para com "sem alvo de câmera". No meio, use `/* */`; `//` só no fim da linha.
5. **`background-clip: text` só funciona no nó do texto** (não pega filho com transform). Sombra por `drop-shadow` (o `text-shadow` vazaria pelo texto transparente); itálica com `paddingRight: 0.06em`.
6. **Whisper em pedaços longos deriva:** "A gente quer emagrecer" saiu 2,7 s cedo, com um "Obrigado" alucinado no silêncio. O `alinhar-palavras.mjs` retranscreve em trechos ≤ 8 s; rodou o `corrigir-palavras.mjs` de novo? Rode o alinhamento depois.
7. **A cor do chroma tem de ser medida:** o fundo veio ~`#0035FF`, não `#0000FF`. O `recorte-chroma.mjs` mede nos cantos; objeto fino pede `--choke`.
8. **Flow com a máquina sem RAM:** evento de mouse dá timeout e o texto colado por JS não chega ao editor. Espere o render de outra sessão terminar; não clique "às cegas" (saíram 7 lotes repetidos).
9. **Stills em 1K:** o "Baixar lote" entregou F01 896×1200 e M01 768×1376; o recorte bruto 1024×1024 virou F04 com 458×914. Baixe a escolhida em 2K.
10. **Chegada em texto livre:** o `tipoChegada` procura os nomes na ordem chicote, deslize, snap-zoom, snap, giro, queda, recuo, recursão, emerge, abre. "giro 8° + deslize ←" vira `deslize`. Use o nome de código exato.
11. **`pushK` descarta em silêncio** a chave a ≤ 5 ms da anterior. O recuo final apaga as chaves depois de `tRecuo`.
12. **O validador é mais fraco que o gerador:** categoria de SFX 3× seguidas é só AVISO na shot list, mas 2× seguidas faz o gerador parar. A trava que vale é a do `M.sfx`.
13. **Montagem casa com a estação pelos tempos** (±0,02 s): mexeu no `ini`/`fim` de uma estação à mão? Gere a shot list de novo.
14. **Palavra com pontuação na âncora:** a âncora da shot list leva a palavra como está no `palavras.json` (ex. `exercitar.@22.45`); o validador ignora a pontuação.

## A confirmar com o Jorge
1. ~~As 3 dúvidas da transcrição do piloto~~ **resolvido em 2026-10-20** (Jorge: "não esquenta, tá ok"): ficam como estão, fora da tela, e o final do piloto vale assim. Regra que segue: palavra em dúvida nunca vai para a tela.
2. ~~CTA de consultoria no card?~~ **resolvido em 2026-10-20** (mesma resposta): o card fica como está, sem CTA (nome, profissão, CREF, ícones e @).
3. **Entrada:** sempre de um roteiro do `/roteiro` ou qualquer áudio? O piloto não veio de `02 - ROTEIROS`.
4. **Duração típica** do formato (o piloto tem 144 s).
5. ~~Regressão `--mix` quebrada~~ **resolvido em 2026-10-20** (ok do Jorge): o `regressao.mjs` acha o piloto também nas subpastas de canal (`%SOUTO_VIDEO_PROJETOS%/`); `--mix` EQUIVALENTE de novo.
6. **Licença da Motionix (SOUTO TREINADOR):** o pacote original não pode ser redistribuído e NÃO vem no repositório. A pasta `sfx/biblioteca/motionix/` é gerada pelo instalador com sons livres (CC0 + sintetizados) de mesmo nome (`node scripts/sfx/sfx-substitutos.mjs`); ver `docs/guias/04-video.md`, seção SFX.

## Peças
### Já existe no código
| Peça | Onde | O que faz |
|---|---|---|
| `PaperVox` + `calcularPaperVox` | `src/modelos/paper-vox/PaperVox.tsx` | Mundo em 3 planos + fundo infinito, motion blur de câmera, montagens, acabamento, voz e SFX |
| Câmera | `camera.ts` | `cameraEm` (chaves, zoom log, `arco`), `cameraViva`, `velocidadeTela`, `transformPlano`, `PARALLAX`, `CURVAS_LAB` |
| Elementos | `elementos.tsx` | 9 tipos, 8 entradas, `boiar`, `tempoPasso`, `DEGRADES`, `COR` |
| Objetos de papel | `objetos.tsx` | os 24 objetos do catálogo (`MAPA`) |
| Texturas | `texturas.ts` | papel, borda rasgada, ladrilho do fundo, prng; segura o quadro até a textura decodificar |
| Tipos | `tipos.ts` | `QuadroProps`, `Elemento`, `ChaveCamera`, `SfxLab`, `Musica`, `MontagemLab` |
| Biblioteca do gerador | `scripts/lib/mural.mjs` | âncoras, serpentina, `ctx` e atalhos, looks, caminho, card, decoração, câmera, `voaBoia`, degradês, SFX com travas e `M.ev.*`, trilha, `gravar` (confere os objetos contra o `MAPA`; `--saida <arquivo>` grava fora do `03_roteiro/quadro.json`), `acharRaiz` |
| Scripts | `scripts/` | `render-paper-vox`, `mixar-audio`, `refinar-sfx`, `validar-shotlist`, `alinhar-palavras`, `recorte-chroma`, `regressao-paper-vox` |
| Geradores por vídeo | `03_roteiro/` do piloto | `montar_shotlist.mjs` e `montar_quadro.mjs` (o molde) |

### O que pode crescer
- **Objetos novos** no `objetos.tsx` (um componente + uma linha no `MAPA`), só com ⏸ do Jorge (regra dos fixos: peça nova só a pedido dele), implementados pela conversa principal. Depois, a regressão (os objetos antigos não podem mudar).
- **Pestana real:** a categoria `papel` troca os 6 sintetizados pelos do Mixkit quando o Jorge baixar (licença registrada no lab).
- Existem no código e não foram usados no piloto: escala `capitulo`, entrada `desliza`.
- **Proposta (não feita):** receitas como funções na biblioteca (`jornalVivo`, `estatuaSanduiche`…) e peças declaradas na `shotlist.json` (célula, peças, câmera, corte de trilha), para o gerador por vídeo encolher.
