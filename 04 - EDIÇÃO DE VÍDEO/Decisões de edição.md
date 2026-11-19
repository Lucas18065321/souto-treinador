---
tipo: preferencias
atualizada: 2026-10-20
---

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).

# Decisões de edição (padrões herdados; o Jorge pode mudar qualquer um)

Cada decisão nova do Jorge entra aqui com a data. Enquanto ele não disser o contrário, valem as de baixo.

Trazido das memórias do projeto Edições Dinâmicas (05 e 06/10/2026, piloto SONO X EMAGRECIMENTO). Complementa o manual do motor (`04 - EDIÇÃO DE VÍDEO/CLAUDE.md`), que tem as preferências gerais.

## Identidade (YOUTUBE - MIX EDIT, vale também para o CUT DINÂMICO)
- Acento **azul elétrico #2E49CE** nos dois canais, não o laranja da referência.
- Card de apresentação: nome, "educador físico", **CREF 000000-G/UF**, ícones Instagram + YouTube, @soutotreinador. Entra por volta de 0:36, depois do gancho.
- **Text Match Cut:** manchetes reais de veículos sérios e artigos científicos recentes de alto fator de impacto e metodologia sólida. Cada item é conferido e aprovado antes de entrar.

## Ritmo (MIX; considerar também no CUT)
- **Sem respiração entre frases:** "aperto" automático corta pausa < −36 dB com ≥ 0,14 s, deixando 0,06 s depois da palavra e 0,05 s antes da próxima (`02_analise/pausas_aperto.json` + `apertar` no `montar_edicao.mjs`).
- **Zoom a cada corte** em rodízio A → C → B2 → A → C → B1, com plano mínimo de **1 s** em troca de enquadramento.
- **Análise de coerência:** entre tomadas parecidas ou explicações repetidas, fica só a melhor; cortar metacomentário e transição sem conteúdo.
- **Intro:** colagem em papel (palavra/número grande em vermelho, caneta circulando, foto recortada P&B; peça `colagem-papel`) e título em colagem stop-motion (`colagem-titulo`), no estilo da intro de referência que ele mandou.
- **Música:** só na intro, tensão investigativa crescendo até **parada brusca** no título; corpo do vídeo sem música. Não pedir para ele escolher ou baixar trilhas.

## Marca na tela (todos os formatos)
- **(2026-10-08) Sem @ fixo no canto.** O ícone do Instagram + "@soutotreinador" que ficava o vídeo inteiro no canto (`marca-arroba`) sai de todos os próximos vídeos. O @ só aparece no card final.

## Pergunta de entrada (formatos com vídeo)
- **(2026-10-11) Ao receber o bruto, perguntar: "É para decupar, corrigir cor e ajustar o áudio?"** (junto com a pergunta do formato). Fazer só o que ele marcar; sem nada marcado, ir direto para a edição. As ferramentas de bruto cru (transcrição grande, decupagem inteligente, estúdio de áudio) são demoradas: só entram quando ele pedir. Ele passa a mandar os brutos em 1080 (o 4K deixou o arquivo pesado).
- **(2026-10-20) INSTAGRAM - PAPER VOX ANIMATION (só áudio):** a mesma regra, adaptada ao formato: junto com a pergunta do formato, só "Ajustar o áudio?" (Sim / Não, já vem tratado). Sem cor e sem decupar: as pausas são o lugar das montagens.

## Cor (todos os formatos)
- **(2026-10-09) Não mexer na cor.** Os brutos dele chegam com a cor já ajustada: sem preset do `preparar.mjs` e sem o filtro padrão do Tela Dividida. Use `"cor": {"contraste": 1, "saturacao": 1, "calor": 0}`. No "criativo 1" o preset "cinema" (escolhido por mim, sem resposta dele) + o filtro do formato deixaram o vídeo "parecendo uma caverna".

## Música (todos os formatos)
- **(2026-10-08) Volume: no máximo 1/4 da voz (−12 dB).** A música é de fundo e suave; nunca fica alta nem cobre a voz, nem sem fala. Conta: medir com `ebur128` a voz (LUFS integrado do bruto) e o pico curto (janela de 3 s) do trecho usado da trilha; `vol` = 10^((LUFS_voz − 13 − pico_curto_trilha)/20) (1 dB de folga) e `volSemFala` no máximo 10^((LUFS_voz − 12 − pico_curto_trilha)/20). Prevalece sobre os volumes escritos nos guias.
- **(2026-10-08) Gosto no CUT:** recusou hip hop "dramedy", techno minimal, house e chillwave/synthwave; escolheu ouvindo um **lofi** ("Lofi", Sub_Clair, Pixabay) e pediu para começar no segundo 24. Quando ele não gostar de 2 rodadas de opções, peça a referência ou o link em vez de seguir chutando.

## TELA DIVIDIDA: mudanças pedidas em 2026-10-27 (depois do vídeo da dieta restritiva)
- **Emenda esfumaçada fixa no `split`:** "uma transição suave entre as linhas que dividem os b-rolls e eu… um esfumaçado entre as divisórias. Fica estiloso." Versão final: fusão cruzada longa (o rosto sobe por baixo, o B-roll some em curva suave), sem faixa de desfoque. Ele recusou a 1ª ("o blur ficou muito duro") e pediu "o mais suave e sem bordas de saída do efeito". Código no `Edicao.tsx`; regressão regravada depois do aprovado.
- **Legenda acompanha o corte:** quando sai o B-roll e corta só para ele, a legenda desce no mesmo quadro. Antes, "viraram" (22 s) ficava no meio do rosto; acontecia várias vezes.

## B-roll gerado no Flow em todo vídeo (2026-10-27)
- "Gere vídeos (geração única, apenas uma versão) com animações que exemplifiquem ou ilustrem bem o que tô falando em mais momentos, só fotos tá ficando meio batido." → vídeos do Flow x1 nos momentos de impacto (~1 a cada 20–25 s) e mais imagens do Nano Banana com apelo de gancho visual.
- Tudo o que for gerado (vídeos e imagens) vai para a biblioteca etiquetado, como o material de banco, para reaproveitar. Nunca repetir nada dentro do mesmo vídeo.

## Efeitos sonoros (INSTAGRAM - TELA DIVIDIDA)
- **(2026-10-19) SFX variado e mais baixo, aprovado de ouvido no comparativo do criativo 1.** Ele reclamou de efeitos "altos e repetitivos": o mesmo whoosh em toda transição e um pop em toda palavra destacada.
  - Agora o `sfx-variado.mjs` (etapa 5b do `/editar`) sorteia o som por tipo, sem repetir em seguida.
  - Volume: transição ~12 dB e pop ~17 dB abaixo da voz (antes: 8 e 14 dB).
  - Pop só na 1ª vez de cada palavra destacada.
  - No criativo 1: de 40 sons e 6 diferentes para 22 sons e 21 diferentes.

## PAPER VOX ANIMATION (INSTAGRAM - PAPER VOX ANIMATION, `paper-vox-instagram`)
- **(2026-10-20) Consolidado como formato fixo:** "O estilo de edição ficou simplesmente perfeito! … Consolidado. Só a partir de um áudio." e "Pode renderizar". Fixo como o CUT e o MIX, não congelado: formato, estilo e guia só mudam a pedido dele. No lab era o "formato 4"; ele o chamou de 5º. Nos documentos, sempre pelo nome e pelo id. Piloto: "sociedade que adoece" (`%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece`).
- **(2026-10-19) Estilo por código, 0 crédito:** sem Seedance; quadro contínuo 100% por código + imagens do Nano Banana (grátis); montagens na opção A (stills do Flow). Proposta de cenas com alto impacto visual, dinamismo, fluidez, referência visual e magnetismo.
- **(2026-10-19) Montagem de ~0,2 s nos silêncios** (ideia dele).
- **(2026-10-19) Dúvidas da transcrição:** ele responde por texto; a palavra em dúvida fica fora da tela até lá.
- **(2026-10-19) Shot list, prompts e 47 imagens aprovados.**
- **(2026-10-20) Prévia 1:** "a estrutura ficou simplesmente sensacional", com 4 críticas:
  1. SFX altos e extremamente repetitivos em cada imagem, card e elemento → 26 SFX (eram 106), 12–17 dB abaixo da voz, ≥ 1,15 s entre eles, nunca a mesma categoria em seguida; entrada de imagem, papel, fita e plano de montagem sem som.
  2. Textos da cor do fundo → palavra-chave no degradê da marca (branco só sobre a marca azul elétrico).
  3. Recortes (cadeira, estátua, a mão aos 49 s) apareciam junto com o painel → vêm de fora com curva smooth "extremamente dinâmica" (entrada `voa`: 1.400 px, em arco, giro de 24°, blur 18 → 0, 0,36–0,42 s, só depois que a câmera assenta) e ficam "boiando" (±7 px, ±1,1°); aparições ainda mais rápidas e nunca estáticas.
  4. Trilha: "encontrar a trilha sonora perfeita, corte a música e deixe só a voz quando for momentos mais tensos, ou que minha voz precisa ser enfatizada" → 7 cortes só voz; trilha ≤ 1/4 da voz.
- **(2026-10-20) Prévia 2:**
  - Trilha: "gostei de ambas"; escolheu a A, suspense de investigação ("vou ficar com a 1ª opção"). Padrão do formato (padrão do fluxo, não pedido dele): 2 opções da biblioteca mixadas para comparar.
  - Degradês variados: "variar os degradês, e não só uma ou outra cor" → os 3 em rodízio, dois seguidos nunca iguais (hex em `marca/marca-souto.json`, lidos por `motor/src/marca.ts`).
  - Texto nunca por baixo de imagem ou linha: "corrija para os próximos" (a correção já entrou no motor e também saiu no final do piloto, avisado).
  - SFX com timing milimétrico ("faz a diferença"; "nesse 88% ficou perfeito"): etapa de refino só para os próximos ("n precisa fazer nesse só para os próximos").

## CUT DINÂMICO: obrigatórios em todo vídeo (2026-10-22, depois do vídeo do sal)
- **Enquadramento:** rosto centralizado, cabeça nunca cortada, pouca mesa. No estúdio de gravação original (20 vídeos gravados assim), a softbox pode aparecer no topo ("é um charme"). Plano base com zoom ≈ 1,15 e closes a partir dele (fórmula no `motor de vídeo/CLAUDE.md`).
- **Texto do início ATRÁS da cabeça, sempre**, em qualquer vídeo e qualquer posição da cabeça. A palavra é posicionada pela cabeça daquela cena, medida no quadro e não por número fixo: ela cruza o topo da cabeça e a cabeça cobre 10–30%, numa letra que não muda a leitura. No vídeo do sal, a v1 cobria 35%; ao refazer o enquadramento, a palavra ficou acima da cabeça porque as camadas foram mantidas (pedido de não mexer no resto).
- **Recortes como elemento gráfico dinâmico:** objetos sem fundo (Flow com fundo azul #0000FF + `recorte-chroma.mjs`, ou PNG de banco) entrando com pop, órbita ou voo perto do corpo, complementando a fala. Nunca sobre o rosto nem sobre a legenda. No vídeo do sal só entrou 1 (a colher do card), contra 3–4 nos anteriores: foi escolha minha de plano, que preferiu B-roll de tela cheia, e não falta de ferramenta. Não repetir.
- Os dois entram no plano (etapa 3) e nos prompts do Flow (recortes = imagens de 0 crédito). Mínimo de recortes de objeto: max(3, duração ÷ 20 s), ou seja, 6 num vídeo de 2 min.
- **Variedade de peças de informação, em rodízio no mesmo vídeo (2026-10-22, "precisamos de dinamismo"):** ele gostou das escolhas do vídeo do sal, como a colher como B-roll com motion e o card dos 5 g. Pediu para usar **também**, quando houver ensejo:
  - **liquid glass:** a régua `escala-ph` do SONO X IMUNIDADE ("foi bizarro em liquid glass") e o `card-vidro`, alternando com a `ficha-papel` em vez de só papel;
  - **o índice da régua adaptado a outros dados:** gráficos, faixas e escalas diferentes no mesmo visual de vidro (`contador`, `grafico-barras`, `grafico-linha`, `escala-ph` reaproveitada como régua genérica);
  - **B-roll com motion:** objeto recortado entrando ou animando sobre a cena.
  
  Liberdade total de escolha: "confio no seu gosto; você quem sabe a hora e se vai precisar". É preferência, não trava. No plano, alterne os formatos (papel, vidro, contador, gráfico, objeto) e evite repetir o mesmo tipo de card seguido.
- **Trava no validador (pedido dele, 2026-10-22):** `validar-edicao.mjs` dá AVISO (`abertura-atras`, `recortes-objeto`) quando faltar algum dos dois. Nos CUTs anteriores, todos tinham a abertura atrás; os recortes ficaram abaixo do mínimo em todos (sal 1/6, antioxidante 3/4, fitoterápico 4/5, sono 4/6, vitaminas 0/3).

## CUT DINÂMICO: centralização fixa e texto inteiro (2026-10-28, depois do vídeo do lipedema)
- Ele apontou no final: o "NÃO EXISTE" atrás da cabeça fora do centro (x 0,434), o texto do card de vidro alinhado à esquerda num card centralizado e o "adipocitocinas" cortado na borda da tela. Pediu: "deixe essa regra da centralização fixa para esse estilo, nessas partes específicas. E para não cortar texto. Como um reforço no motor e no script. […] Que não se repita."
- **Regra fixa:**
  - Palavra atrás da pessoa e `card-vidro` sempre no centro do quadro.
  - Card sem lista com o texto centralizado; com lista, o bloco fica no meio do card.
  - Nenhum texto sai da tela.
- **Ícone e título do card na mesma linha** (observação dele no "mais um deles": o símbolo vermelho ficou em cima e o título embaixo). Pediu como observação para os próximos, sem precisar corrigir neste. O motor passou a montar assim no CUT (card com ícone e título, sem rótulo), e por isso o re-render deste vídeo já saiu com a correção.
- O motor força (`estilos.ts`, `centrarTexto`) e o `validar-edicao.mjs` dá ERRO (`centro`, `texto-cortado`). Detalhes no guia do CUT.
- Antes disso, 6 dos 7 CUTs já tinham a palavra em x 0,5 ("nunca tinha acontecido"); a exceção foi o das vitaminas, com x 0,46, já publicado.
- No mesmo vídeo ele pegou 2 repetições curtas que a decupagem deixou passar ("Não acredite em…" e "E para você?"), escondidas porque o Whisper juntou cada repetição com a frase certa. Ele disse que foi erro dele não ter visto antes. Foram cortadas e o vídeo foi renderizado de novo. De resto: "ficou perfeito!". Ele aceitou reforçar o decupador ("Sim, reforçar"). A decupagem passou a procurar a repetição escondida (👂, `decupar-inteligente.mjs` + `lib/repeticoes.mjs`) retranscrevendo em trecho curto cada pausa no meio de frase. No teste, ela achou as 2 do lipedema e não deu falso alarme no sal.

## VOX - B-ROLLs (INSTAGRAM - VOX - B-ROLLs, `vox-broll-instagram`; nasceu no LAB em 2026-10-28, fixo desde 2026-10-30)
Guia oficial: `04 - EDIÇÃO DE VÍDEO\referencias/modelos\vox-broll-instagram\guia-de-estilo.md` (o rascunho do lab, `05_LAB\formatos\5-paper-vox-broll\`, fica como histórico).
- **(2026-10-28) Motor:** continua 100% Remotion ("n mexemos em time que se ganha"). O HyperFrames fica só no recorte da pessoa.
- **(2026-10-28) Estrutura:**
  - nos 2 primeiros segundos, o rosto dele com texto grande e dinâmico acompanhando a fala;
  - a tela é inundada por colagens que exemplificam a fala, com texto cinético;
  - tela dividida com uma animação que exemplifica a fala por analogia;
  - só ele;
  - nova invasão de colagens: a câmera segue sem corte até outra cena de colagem e dá zoom numa parte, deixando um resquício da anterior no canto;
  - tela dividida com uma animação na proporção de B-roll;
  - só ele no encerramento.
  - Entra também a faixa em que ele fica "meio cortado no cenário", com a animação rolando atrás (ref-08).
- **(2026-10-28) Ritmo:** "frenético e visualmente forte", com entrada e saída rápidas e efeito cinético nos objetos. Na tela dividida, a fluidez das 3 telas de animação da ref-08.
- **(2026-10-28) Legenda:** fora da área morta do Reels (botão de seguir, curtidas, repost etc.).
- **(2026-10-29) O foco são as animações no estilo Vox, não artigos:** "o foco desse novo modelo n é artigos, apesar que eventualmente vá ter por conta das temáticas que eu abordo. Mas o foco é as animações no estilo vox."
  - Print de artigo (circulado) só entra quando a fala cita um estudo, como apoio rápido, nunca como a peça principal da cena.
  - No teste da creatina, onde a fala cita o estudo, ficam 1 ou 2 prints, e o card "Obs." da idade média entra depois da frase.
- **(2026-10-29) Tela dividida:** uma animação por vez na metade de cima, trocando a cada 2 s ou menos (pergunta 1 = A); as 2 faixas empilhadas ficam fora.
- **(2026-10-29) Abertura:** texto digitado fora do rosto + cartão azul elétrico, como a ref-09 (pergunta 2 = B), sem recorte da pessoa; a palavra atrás da cabeça segue obrigatória só no CUT.
- **(2026-10-29) 2ª invasão (mural):** a cena nova nasce dentro de uma parte da anterior e a câmera mergulha nela, com o resquício da anterior no canto (pergunta 3 = A).
- **(2026-10-29) Moldura de baixo:** depois do mural, antes da 2ª tela dividida (pergunta 4 = A), "podendo aparecer cards e informações sobrepostas e cards com informações complementando o contexto".
- **(2026-10-29) Imagens do Flow:** sem teto fixo por vídeo (nenhuma das 3 opções): "1 cenário e até quantos recortes forem necessários, lembre que precisamos de vários elementos para compor uma cena às vezes complexa mas bonita".
- **(2026-10-29) Legenda:** pequena e discreta em tudo, como a ref-09 (pergunta 6 = B): 1 a 3 palavras, branca, caixa cinza só sobre fundo claro, sempre dentro da área segura do Reels; a palavra grande fica no texto da cena.
- **(2026-10-30) 1º vídeo do formato (creatina, 112 s): aprovado** ("Aprovado").
  - Foi feito direto, sem as paradas, a pedido dele: "deixo todas permissões ok. Quero ver a versão final". A liberação valeu para esse vídeo.
  - Acima de 75 s, a espinha ficou em 2 atos: o 1º é a espinha inteira; o 2º alterna "só ele" com tela dividida, com a 2ª moldura (card "Obs.") e um 2º mural.
  - Ele perguntou se todo vídeo nesse modelo demoraria 1–2 dias. A estimativa para os próximos é de ~2–3 h de máquina.
- **(2026-10-30) Promovido a 5º modelo fixo do `/editar`** ("Pode promover", na pergunta da promoção, depois de ele perguntar se o modelo já estava entre os oferecidos). Nome: INSTAGRAM - VOX - B-ROLLs.
  - Com 5 modelos, o `/editar` pergunta antes a plataforma (Instagram ou YouTube) e depois o formato. O VOX tem fluxo próprio (V0–V11) e o agente `diretor-vox`.
  - Ficam os padrões do vídeo aprovado: render com concurrency 1 e sem angle, câmera a 24 fps, emenda esfumada; 2 atos acima de 75 s. As 4 comparações não medidas (aceleração gráfica, concurrency 2, câmera 12 × 24 fps, emenda reta × esfumada) seguem pendentes.
  - O vídeo da creatina virou o piloto do formato: a pasta foi para `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino` (o vídeo não mudou) e 3 trechos do final aprovado são a referência da regressão do VOX.

## Defeitos que ele percebe (não repetir)
- Piscada de 1 quadro no zoom dentro de bloco desfocado: **bloco desfocado = uma cena só**, desfoque só nas pontas.
- Rodapé de fonte grande engolindo o gráfico: **rodapé a 26 px, numa linha**, discreto.
- Rodar `checar-mix.mjs` (também com `--video` no final) antes de entregar.
- (PAPER VOX, 2026-10-20) Texto coberto por imagem ou linha ("polêmica" ficou atrás da estátua, "caminho" atrás da linha): **texto sempre por cima** de papel, foto, recorte e objeto dentro de cada plano; só o traço à mão e o flash passam por cima dele. As lascas do plano da frente ficam nos cantos, fora da zona de texto.
- (PAPER VOX, 2026-10-20) SFX fora do tempo: o som cai no instante visual que marca, pelo ponto MEDIDO no arquivo (ataque ou pico), não suposto. Antes do final, a etapa de refino milimétrico (`refinar-sfx.mjs` + carretel de audição, ⏸ Jorge). No piloto, o riser "terminando no mergulho" soou 2,3 s antes, porque bate no começo.
