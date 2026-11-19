---
name: editar
description: "Edita um vídeo bruto (de celular ou de câmera, decupado ou não) ou um áudio narrado do início ao fim num dos modelos de edição treinados (INSTAGRAM - TELA DIVIDIDA, INSTAGRAM - EDIÇÃO CUT DINÂMICO, YOUTUBE - MIX EDIT, INSTAGRAM - PAPER VOX ANIMATION, INSTAGRAM - VOX - B-ROLLs), perguntando primeiro a plataforma e o formato, com pontos de aprovação do usuário. Um áudio do Jorge narrando (sem vídeo, como o .oga do WhatsApp ou um mp3) vai para o INSTAGRAM - PAPER VOX ANIMATION (o .oga de pedido falado não é bruto; transcreva e execute). Use quando o usuário enviar/arrastar um vídeo bruto ou um áudio narrado, disser 'edita esse vídeo', 'novo vídeo', 'começa a edição' ou chamar /editar."
argument-hint: "<caminho do vídeo bruto ou áudio> [nome do vídeo]"
---

# /editar

> **Onde fica o motor:** `04 - EDIÇÃO DE VÍDEO/motor` (dentro do repositório souto-treinador). **`CLAUDE.md` = manual do motor** (`04 - EDIÇÃO DE VÍDEO/CLAUDE.md`): leia antes de começar (não é carregado sozinho quando a sessão está na raiz do repositório). Histórico completo de calibração: `04 - EDIÇÃO DE VÍDEO/referencias/MANUAL-COMPLETO-DO-MOTOR.md`. Decisões de estilo: `04 - EDIÇÃO DE VÍDEO/Decisões de edição.md`. Scripts: `cd "04 - EDIÇÃO DE VÍDEO/motor"` antes de `node scripts/...`.
> **Projetos, brutos, renders, B-roll e músicas ficam FORA do repositório**, na pasta da variável `SOUTO_VIDEO_PROJETOS` (padrão `%USERPROFILE%\Videos\Souto-Projetos`; definida no `.env` da raiz). `<proj>` = `%SOUTO_VIDEO_PROJETOS%/<AAAA-MM-DD>_<nome>`. O mapa de pastas está em `motor/scripts/lib/caminhos.mjs`.
> **Adaptação para o Jorge Souto (SOUTO TREINADOR):** este fluxo foi calibrado em outro canal. Onde o texto cita um **piloto** por nome (ex.: `2026-10-05_sono-x-imunidade`, `2026-10-19_sociedade-que-adoece`, `2026-10-28_creatina-sem-treino`, `2026-10-24_lv0-0929`), entenda: **o 1º vídeo do Jorge aprovado naquele formato**. Esses projetos NÃO vêm no repositório. Enquanto o Jorge não tiver piloto num formato: (a) no MIX, PAPER VOX e VOX escreva o gerador do vídeo do zero a partir de `scripts/lib/mural.mjs` / `scripts/lib/vox.mjs` / tipos em `src/tipos.ts` e do guia do formato (avise que o 1º vídeo leva mais tempo); (b) pule as comparações "gerador do piloto gera o mesmo json"; (c) as regressões avisam "piloto não configurado" até ele aprovar um vídeo e configurar `pilotos.json` (guia `docs/guias/04-video.md`, seção Regressão). Identidade: azul (`marca/marca-souto.json`) e `04 - EDIÇÃO DE VÍDEO/marca-video.json` (nome, @ e CREF; campos TROCAR). Agentes de outras frentes citados aqui (`legendista`, `checador-de-afirmacoes`, `diretor-de-arte`, `fichador`) só se existirem em `.claude/agents/`; se não, faça você mesmo a tarefa e avise. Publicados: `05 - PUBLICAÇÃO E CRESCIMENTO/Publicados.md`, se existir.

Você é o editor. As regras comuns estão em `CLAUDE.md` (fluxo, restrições, preferências do usuário). Fale com o usuário em português, de forma curta.

> **Bruto 100% cru (sem decupar, sem tratar áudio e cor), desde 11/10/2026.** As etapas abaixo continuam iguais. **Só faça o que o Jorge marcar na pergunta da Etapa 0**; o que ele não marcar, pule:
> - **Corrigir cor** → 1b: comparativo e escolha dele (só faz sentido em bruto log/RAW).
> - **Decupar** →
>   - 2: `transcrever.mjs` (modelo grande) no lugar da transcrição do `assistir.mjs`;
>   - 2b: `decupar-inteligente.mjs` (desde 2026-10-28, procura também a 👂 repetição escondida, que o Whisper junta numa frase só: +2–4 min na placa de vídeo) → agente `decupador` → `--aplicar`. Use `palavras_montagem.json` como `palavras.json` e `montagem.json` como `montagem`. No Tela Dividida, que não tem `montagem`, use `--render`, que gera o `bruto_decupado.mp4`.
> - **Ajustar o áudio** → 7b: `estudio-audio.mjs` (3 intensidades + comparativo) além do `tratar-voz.mjs`.
> - **Áudio narrado (INSTAGRAM - PAPER VOX ANIMATION):** só existe a pergunta "Ajustar o áudio?"; sem cor e sem decupar. Fluxo próprio (P0–P9) em "Por formato".
>
> Sem nada marcado: vá direto para a edição no estilo de sempre, com o `assistir.mjs` normal. Ele vai mandar em 1080 (o 4K deixou o arquivo pesado). Detalhes no `CLAUDE.md`, seção "Bruto 100% cru". Em trabalho longo, peça para manter o computador acordado.

**Etapa 0 — Plataforma e formato (SEMPRE as primeiras perguntas, logo que o bruto ou o áudio chegar):** leia `referencias/modelos/MODELOS.md`. São 5 modelos desde 2026-10-30: passou de 4, então a plataforma vem antes (ferramenta de perguntas, se disponível):
   1. **"Qual plataforma?"**: **Instagram** (vertical 9:16: TELA DIVIDIDA, CUT DINÂMICO, PAPER VOX ANIMATION e VOX - B-ROLLs) ou **YouTube** (horizontal 16:9: MIX EDIT). Na mesma chamada, a pergunta do bruto (abaixo).
   2. **"Qual formato?"**, só no Instagram, com uma opção por modelo, cada uma com o formato e o resumo curto na descrição. No YouTube, o MIX EDIT é o único: siga sem esta pergunta.
   - **INSTAGRAM - TELA DIVIDIDA**: vertical 9:16; B-roll em cima + rosto embaixo, objetos voando na fala, gráficos em vidro, quebras de padrão (id interno `tela-dividida-2-instagram`, desde 2026-10-27; substituiu o clássico, que foi arquivado).
   - **INSTAGRAM - EDIÇÃO CUT DINÂMICO**: vertical 9:16; ritmo alto, camadas de motion, texto atrás da pessoa, 3D.
   - **INSTAGRAM - PAPER VOX ANIMATION**: vertical 9:16; só a partir de um áudio, 100% dark, mural de papel animado por código, o Jorge não aparece.
   - **INSTAGRAM - VOX - B-ROLLs**: vertical 9:16; colagens animadas no estilo Vox sobre o vídeo dele: colagens invadem a tela, tela dividida, mural com mergulho, moldura com a cabeça vazando e legenda pequena (id interno `vox-broll-instagram`, desde 2026-10-30).
   - (YouTube, fora da pergunta) **YOUTUBE - MIX EDIT**: horizontal 16:9; Apple edit + 3D flash edit, intro cinematográfica com manchetes em Text Match Cut.
   **Chegou um áudio (sem vídeo)?** O PAPER VOX é o óbvio (os outros 4 precisam do rosto), mas pergunte a plataforma e o formato do mesmo jeito e, na chamada da plataforma, só **"Ajustar o áudio?"** (opções **Sim** e **Não, já vem tratado**). Corrigir cor e decupar não entram: não há imagem, e as pausas são o lugar das montagens. Siga "Por formato" → INSTAGRAM - PAPER VOX ANIMATION.
   **Chegou um vídeo? Na chamada da plataforma** (calibração original, 11/10/2026: as perguntas do início saem juntas), faça a pergunta do bruto: **"É para decupar, corrigir cor e ajustar o áudio?"**, com `multiSelect` e as opções:
   - **Decupar**;
   - **Corrigir cor**;
   - **Ajustar o áudio**;
   - **Nenhum: já vem tratado**.
   Faça só o que ele marcar (ver o quadro "Bruto 100% cru" acima). "Nenhum" = pular direto para a edição. Nunca faça um desses três por conta própria.
   (O Instagram tem 4 modelos e ainda cabe numa pergunta só. Se passar de 4, divida também a pergunta do formato.) Se o escolhido estiver 🚧 (em construção), avise e ofereça terminar o modelo com `/novo-modelo` usando este vídeo como piloto. Depois leia o `guia-de-estilo.md` do modelo e siga-o em todas as etapas; registre `"modelo": "<id>"` no `edicao.json` (o render escolhe tamanho e composição por esse id). No PAPER VOX e no VOX - B-ROLLs não há `edicao.json`: o gerador grava `"modelo": "paper-vox-instagram"` no `03_roteiro/quadro.json` e `"modelo": "vox-broll-instagram"` no `03_roteiro/vox.json`.

**Motor principal = o nosso Remotion (`04 - EDIÇÃO DE VÍDEO/motor`).** Skills HyperFrames/video-use/embedded-captions não substituem este fluxo; use-as só para uma peça isolada (ex.: um motion graphic) que vira um clipe em `04_broll/` e entra no `edicao.json` como B-roll. Para qualquer transcrição, use `assistir.mjs` (que também gera `transcript.json` no formato HyperFrames) — nunca instale WhisperX, faster-whisper, torch ou similares. **Exceção: INSTAGRAM - PAPER VOX ANIMATION e INSTAGRAM - VOX - B-ROLLs.** Lá a ilustração entra na palavra, então a transcrição é `transcrever.mjs` → `corrigir-palavras.mjs` → `alinhar-palavras.mjs`, nesta ordem (P1 e V2 em "Por formato").

Rode os scripts de dentro de `04 - EDIÇÃO DE VÍDEO/motor`. `<proj>` = pasta do projeto em `%SOUTO_VIDEO_PROJETOS%`.

## Etapas (pare nos ⏸ e espere o usuário)

1. **Projeto**: se `$ARGUMENTS` traz um caminho, `node scripts/novo-projeto.mjs "<nome>" "<caminho>"` (sem nome, pergunte um curto). Se o vídeo já está num projeto, use-o.
1b. **Bruto de câmera** (4K, 10 bits, 4:2:2, perfil log/lavado ou com rotação; confira com `ffprobe`): o Chrome do Remotion não lê esse vídeo. Rode `node scripts/preparar.mjs <proj> --modelo <id> --foco x,y --comparar` → mostre `06_previas/comparativo_cor.jpg` e ⏸ pergunte a cor (nenhuma, neutra, viva, cinema), como no áudio: cada gravação é diferente. Depois `node scripts/preparar.mjs <proj> --modelo <id> --foco x,y --cor <escolhida>` (original fica em `01_bruto/original.*`; trabalho em `bruto.mp4`, já recortado no formato e a 24 fps nos formatos do Instagram).
2. **Assistir**: `node scripts/assistir.mjs <proj>/01_bruto/bruto.<ext> <proj>/02_analise`. Leia `transcricao.md`, `segundo_a_segundo.md` e TODAS as `folha_*.jpg`. Descubra: assunto, arco da história, momentos fortes, onde está o rosto (`rostoY`), problemas técnicos (som, luz, enquadramento).
   Anote também (sem agir ainda) o diagnóstico da voz para a etapa 7: pico − RMS (< ~14 dB = muito comprimida), sibilância, aspereza 2,5–4 kHz, embolado ~300 Hz, ruído nas pausas.
2b. **Decupagem** (formatos do motor de camadas; o Tela Dividida recebe bruto já decupado): `node scripts/decupar.mjs <proj>` → leia `03_roteiro/decupagem.md` inteiro e confira cada fala: tomadas repetidas já saem marcadas (fica a última); frases erradas que não se repetem → `--tirar N`; falsos positivos → `--manter N`. A `montagem.json` vira o campo `montagem` do `edicao.json` (cenas e camadas passam a usar o tempo da saída). Se cortou mais de ~10% ou alguma frase inteira, mostre o resumo no plano.
3. **Plano** → escreva `<proj>/03_roteiro/plano.md`: tabela cena a cena (tempo, fala, layout, B-roll pretendido + fonte: meus/banco/internet/Flow, transição, destaques), lista de destaques, mood da música e estimativa de créditos do Flow. Proporções e ritmo do guia do modelo escolhido (ex.: Tela Dividida ≈55% split e troca a cada 2–5 s; MIX sem respiro entre frases, zoom a cada corte e capítulos).
   ⏸ Mostre um resumo do plano e peça aprovação/ajustes.
4. **Material**:
   - **primeiro a biblioteca**: `node scripts/biblioteca.mjs buscar <termos>` para cada cena; o que servir, copie para `04_broll/meus/` e marque no plano como "biblioteca". Peças fixas (intro, apresentação com @, encerramento, ícones, motions prontos) vêm do kit: `kit/KIT.md`.
   - banco: `node scripts/stock.mjs <proj> <id> "<query em inglês>" [--image] [--n 3]` → veja as opções (folha de quadros/imagem) e escolha a melhor.
   - **Flow em todo vídeo (desde 2026-10-27, calibração original):**
     - vídeos animados que ilustram a fala nos momentos de mais impacto, ~1 a cada 20–25 s (x1, uma versão só; Omni 1.1 Flash = 12 créditos);
     - mais imagens do Nano Banana (0 crédito) com gancho visual forte, no lugar de foto genérica de banco.
     O plano (etapa 3) já marca quais cenas são vídeo do Flow e soma os créditos.
   - Flow: escreva `<proj>/03_roteiro/prompts_flow.md`. ⏸ Peça aprovação da lista e dos créditos. Gere pelo Claude in Chrome seguindo as regras do `CLAUDE.md`; ⏸ confirme a lista de downloads; mova para `04_broll/ia_flow/<id>.<ext>`.
   - música: busque no Pixabay Music conforme o arco. ⏸ Apresente 2–3 opções (nome, link, duração, por que combina). Baixe só a aprovada → `05_audio/musica`. **No MIX o padrão do usuário é outro:** trilha só na intro, com parada brusca no título, e corpo sem música; não ofereça várias trilhas (a da biblioteca, feita por código, serve).
5. **Montagem (agente `montador` + validador)**: a IA escreve o `edicao.json`, o script confere as regras e o hook roda o script sozinho.
   - Antes, corrija erros de transcrição em `02_analise/palavras.json` (nomes próprios, termos técnicos) com `corrigir-palavras.mjs`.
   - Chame o agente `montador` (`.claude/agents/04-video/montador.md`). Se ele não estiver na lista, rode um general-purpose com as instruções desse arquivo. Passe o projeto, o `modelo` e o `plano.md` aprovado.
   - Ele escreve `<proj>/03_roteiro/edicao.json` (no MIX, adaptando o gerador do piloto) e roda `node scripts/validar-edicao.mjs <proj>` até dar `0 ERRO`.
   - **O que o validador confere (regras duras do formato):**
     - estrutura do `tipos.ts`;
     - corte da montagem fora de palavra: só em fronteira de palavra, pausa medida ou ponto da decupagem;
     - plano mínimo;
     - rodízio de zoom e música só na intro (MIX);
     - rodapé de fonte a 26 px;
     - B-roll sem repetir e arquivos que existem;
     - Instagram em 1080×1920 a 24 fps.
     No MIX ele também roda o `checar-mix.mjs`. ERRO trava; AVISO vai para o relatório.
   - **Hook:** com o hook configurado no `.claude/settings.json` da raiz (ver `docs/guias/04-video.md`), todo Write/Edit em `03_roteiro/edicao.json` roda o validador e devolve os ERROS ao modelo. Vale também para os ajustes da etapa 7.
   - Nunca edite o validador, os guias ou o `tipos.ts` para "passar". Regra nova de formato só entra a calibração original, no guia e no validador juntos.
   - Leia o relatório do montador (avisos e decisões pendentes) antes de abrir a ilha.
5b. **SFX variado (só no TELA DIVIDIDA clássico, arquivado; o atual tem SFX automáticos em rodízio no motor e NÃO usa este script):** com o `edicao.json` em 0 ERRO e antes de abrir a ilha, rode `node scripts/sfx/sfx-variado.mjs <proj>`.
   - **O que ele faz:** troca o SFX automático do `Edicao.tsx` (o mesmo whoosh em toda transição e um pop em toda palavra destacada) por:
     - sons sorteados por tipo de transição, sem repetir em seguida;
     - volume medido, ~12 dB abaixo da voz (pop ~17 dB), com o pico no ponto do corte;
     - pop só na 1ª vez de cada palavra destacada, com ≥ 5 s entre eles.
   - **O que ele grava:** `"sfxAuto": false` + a lista `sfx`; o backup `03_roteiro/edicao.antes-sfx.json`; os manuais e os gerados em `03_roteiro/sfx-variado.edicao.json`.
   - **Depois:** leia o relatório (antes × depois) e confira com `validar-edicao.mjs`.
   - **Som manual** (riser, impacto) continua indo na lista `sfx` do json; na rodada seguinte ele vira manual sozinho.
   - **Mexeu em cenas, transições ou destaques na ilha?** Rode de novo. Antes do final, `--conferir` dá código 2 se estiver desatualizado.
   - **Volume:** se o Jorge pedir os efeitos mais altos ou mais baixos, use `--trans <dB>` / `--pop <dB>` (padrão −12 / −17).
   - **Sons:** Motionix, os sintetizados e a biblioteca do lab (`sfx/lab`: Glitch Noises, e o Mixkit quando importado). Regras e testes: `sfx/lab/README.md`.
6. **Prévia na ILHA (sem render)**: nos formatos novos, rode antes `node scripts/normalizar-broll.mjs <proj>` (e no MIX, `checar-mix.mjs`). Grave o nome da pasta do projeto em `%SOUTO_VIDEO_PROJETOS%/.projeto-ativo` e abra a ilha: `preview_start` com o nome `ilha` (configurado em `.claude/launch.json` da raiz do repositório); se não houver essa configuração, `node scripts/ilha.mjs <proj>` em segundo plano. Navegue para `http://127.0.0.1:3123/<composição do modelo>`. Confira você mesmo 3–5 pontos (início, cards, gráficos, fim) com print do navegador antes de chamar o Jorge.
   ⏸ Diga ao Jorge que a ilha está aberta (painel do navegador) e peça que ele assista e aponte ajustes **com o tempo** ("1:23 tira o zoom", "0:45 troca o B-roll").
7. **Ajustes na ilha** até o "aprovado": edite o `edicao.json` → a ilha se atualiza sozinha em segundos (o `ilha.mjs` refaz as props a cada mudança). Confira o ponto alterado com print. **Não renderize prévia a cada ajuste.** Prévia em arquivo (`render.mjs --previa`) só se o Jorge pedir para ver no celular. Na ilha, trechos pesados (3D, recortes) podem engasgar ao tocar: o render final é a versão fiel. Ao aprovar, encerre a ilha (`preview_stop`) para liberar memória antes do render.
7b. **Tratamento de voz — SEMPRE PERGUNTAR, nesta etapa, antes do render final** (nunca aplicar por padrão; nunca reaproveitar automaticamente o tratamento de outro vídeo: cada gravação tem ambiente e microfone diferentes).
   ⏸ Pergunte: "Quer que eu trate o áudio da voz antes do render final?" e resuma em 1 linha o diagnóstico da etapa 2.
   - Se **não**: siga sem o campo `voz`.
   - Se **sim**: os presets de `scripts/tratar-voz.mjs` são só **ponto de partida** — ajuste a cadeia ao diagnóstico deste bruto (frequências e ganhos), gere 2–3 variações com `--comparar <a>,<b>,<c>` (incluindo `original` se ajudar) e envie o comparativo para o usuário escolher de ouvido (eu não ouço áudio). Itere a partir do que ele descrever ("abafado" → faltou presença/ar; "estourado/áspero" → 2,5–4 kHz e sibilância; "lata" → redução de ruído demais). Confirme cada mudança com medição por faixas a volume igual. Use a escolhida com `"voz": "05_audio/voz_<nome>.wav"` no `edicao.json`.
   - Regras: nunca o filtro `deesser` (abafa); de-esser = `adynamicequalizer` calibrado; sem redução de ruído agressiva. Se for distorção grave demais para EQ, ofereça o **Adobe Podcast Enhance Speech v2** (30–50%) — nuvem: só com permissão explícita para enviar o áudio.
7c. **Final**: no TELA DIVIDIDA clássico (só re-render de vídeo antigo), antes rode `node scripts/sfx/sfx-variado.mjs <proj> --conferir` (código 2 → rode de novo sem `--conferir`). Depois `node scripts/render.mjs <proj>` → `07_final/` (vídeo longo do MIX: por partes, ver "Por formato"). Informe o caminho, a duração e os créditos de terceiros (`04_broll/creditos.json`) que precisam aparecer na legenda do post, se houver.
8. **Biblioteca**: importe o material usado (sempre **todos os vídeos e imagens gerados no Flow**, etiquetados como o material de banco) + bons candidatos que sobraram (`lote_biblioteca.json` → `biblioteca.mjs importar`), copie a trilha para `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/` e atualize `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/catalogo.md`. Todo motion novo que puder voltar em outro vídeo vira peça do kit (componente em `motor/src/kit/` ou clipe em `kit/clipes/`) com uma linha no `KIT.md`. Anote no `CLAUDE.md` qualquer aprendizado novo (custos, problemas, tempos de render).

## Por formato (o guia do modelo manda; aqui só o que muda nos comandos)
- **INSTAGRAM - TELA DIVIDIDA** (id interno `tela-dividida-2-instagram`, composição `TelaDividida2`; fixo desde 2026-10-27, substitui o clássico). Guia: `referencias/modelos/tela-dividida-2-instagram/guia-de-estilo.md`. Piloto: `%SOUTO_VIDEO_PROJETOS%/2026-10-24_lv0-0929/03_roteiro/edicao_td2.json`.
  - **Plano (etapa 3):** layouts `split` (simples, stop-motion ou **composto** com `recortes`), `fala`, `vidro` (números de estudo, 2–3 por vídeo), `tela` (quebra de padrão; `giro` 180° em metáfora) e `texto` (fonte B). Quebra de padrão a cada 8–20 s. Trocas `mascara`/`zoom`/`chicote`/`blur`/`flash`/`corte`; flashes P&B nos respiros.
  - **Material (etapa 4):** vídeos do Flow x1 nos momentos de impacto (~1 a cada 20–25 s, 12 créditos cada, ⏸), imagens do Nano Banana com gancho visual e **recortes** (fundo azul + `recorte-chroma.mjs --aparar`; mínimo max(3, duração/20 s)), todos 0 crédito menos os vídeos.
  - **Montagem (etapa 5):** `edicao.json` no tipo `EdicaoTD2` (`src/tipos.ts`), escrito pelo `montador`; `validar-edicao.mjs` até 0 ERRO (o hook roda sozinho).
  - **Sem etapa 5b:** os SFX vêm do motor (rodízio por troca, pop no pouso de cada recorte, obturador nos flashes). Não rode `sfx-variado.mjs`.
  - **Ilha e render:** os de sempre (`render.mjs`; o `modelos.json` já tira o `--gl=angle`, que trava os vídeos deste formato). Antes de mostrar o final: brilho quadro a quadro (`signalstats` YAVG), sem quadro preto nas trocas.
  - **Correções da revisão do piloto (2026-10-27), para os próximos:** pontuação e tamanho da palavra-chave do card e legenda sobre `tela` clara já entram na montagem (o validador avisa). Dois ajustes de motor ficam para a próxima edição, propostos e mostrados na prévia ao Jorge antes de fixar: a legenda no zoom 1,15 (cai na boca/queixo) e o encolhimento da palavra-chave longa do card (o "COMPARTILHA" do CTA). Detalhes no fim do guia.
  - **O clássico** (`tela-dividida-instagram`, composição `Edicao`, congelado e arquivado) só para re-render de vídeo antigo; o `/editar` não o oferece.
- **INSTAGRAM - EDIÇÃO CUT DINÂMICO** (motor de camadas, 9:16 a 24 fps):
  - decupagem (etapa 2b) e legenda cinética automática;
  - texto atrás da pessoa com `recortar.mjs`: é caro, então só nos momentos-chave e nunca junto com um render;
  - referência de qualidade: o piloto SONO X IMUNIDADE.
- **YOUTUBE - MIX EDIT** (motor de camadas, 16:9 a 30 fps):
  - **Montagem:** copie e adapte o gerador do piloto (`%SOUTO_VIDEO_PROJETOS%/2026-10-05_sono-x-emagrecimento/03_roteiro/montar_edicao.mjs`). Ele faz o aperto sem respiro, a análise de coerência (`REMOVER`), o rodízio de zoom com plano ≥ 1 s, o rosto desfocado em bloco sem corte, os capítulos e o rodapé de fonte a 26 px.
  - **Antes da prévia:** `node scripts/checar-mix.mjs <proj>` (ERRO trava). Para conferir pontos sem renderizar: `node scripts/quadros.mjs <proj> <t1> <t2> …`.
  - **Final:** `node scripts/vez.mjs node scripts/render.mjs <proj> --partes auto --manter-partes --concurrency 3` (retomável: se cair, rode o mesmo comando).
  - **Antes de entregar:** `node scripts/checar-mix.mjs <proj> --video <final.mp4>` (nenhuma piscada) e `node scripts/srt-saida.mjs <proj>` (legenda .srt + capítulos para a descrição do YouTube).
  - Versões antigas do final fora de `07_final/` (o render copia a pasta do projeto inteira).
- **INSTAGRAM - PAPER VOX ANIMATION** (`paper-vox-instagram`, composição `PaperVox`, 9:16 a 24 fps; fixo desde 2026-10-20). Só a partir de um **áudio** do Jorge narrando; ele não aparece. Fluxo próprio, P0–P9, no lugar das etapas 1–7c:
  - **Molde:** o piloto `%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece`. Copie os geradores dele (`03_roteiro/montar_shotlist.mjs` e `03_roteiro/montar_quadro.mjs`) para o projeto novo e adapte. O genérico mora em `scripts/lib/mural.mjs`.
  - **Agente do formato:** `diretor-paper-vox` (`.claude/agents/04-video/diretor-paper-vox.md`), nos modos "cenas", "prompts" e "mural". Se ele não estiver na lista, rode um general-purpose com as instruções desse arquivo.
  - **Não se aplica:** `edicao.json`, agente `montador`, `validar-edicao.mjs` (nem o hook), ilha (`preview_start ilha` e `ilha.mjs` pedem `edicao.json`), `render.mjs`, `assistir.mjs`, decupagem, cor (1b), `sfx-variado.mjs`, `normalizar-broll.mjs`. O arquivo do vídeo é o `03_roteiro/quadro.json` (escrito pelo gerador) e a conferência é por prévia renderizada.
  - **P0 Entrada:**
    - áudio do WhatsApp (.oga) → mp3 com FFmpeg (`ffmpeg -i "<áudio>.oga" "<áudio>.mp3"`); mp3, wav ou m4a entram direto;
    - `node scripts/novo-projeto.mjs "<nome>" "<áudio>"` → `01_bruto/bruto.mp3` (ou `.wav`/`.m4a`: o gerador aceita os três; troque a extensão no P1);
    - na Etapa 0, "Ajustar o áudio?" no lugar da 7b (o volume da trilha e dos SFX é medido sobre a voz). Se **sim**: `tratar-voz.mjs` / `estudio-audio.mjs` como na 7b, e a voz escolhida entra no gerador (`criarMural(PROJ, {celulas: CELULA, voz: '05_audio/<voz escolhida>.wav'})`), não num campo `voz`. Sem o `voz`, o mural volta para o `01_bruto/bruto.*` sem avisar. Passe o arquivo ao `diretor-paper-vox` no modo "mural".
  - **P1 Transcrição** (nesta ordem; os dois arquivos marcados "à mão" não têm script: escreve a conversa principal):
    1. `node scripts/transcrever.mjs <proj>/01_bruto/bruto.mp3 <proj>/02_analise --principal` → `palavras.json`, `transcricao_turbo.md` e `suspeitos_turbo.json`;
    2. **à mão:** `02_analise/correcoes.json`, a partir da `transcricao_turbo.md` + `suspeitos_turbo.json` (áudio de roteiro aprovado: ver "Integração"). Molde: o do piloto (`%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece/02_analise/correcoes.json`). Uma lista com dois tipos de regra (formato completo no cabeçalho do `corrigir-palavras.mjs`):
       - troca: `{"t": 62.85, "de": "umbriando", "para": "humilhando"}` (`t` ±2 s; `de` como está no `palavras.json`; `"para": ""` apaga);
       - inserção num vão sem palavras: `{"t": 44.9, "inserir": "social.", "ini": 44.90, "fim": 45.52}`;
    3. `node scripts/corrigir-palavras.mjs <proj> <proj>/02_analise/correcoes.json`;
    4. `node scripts/vez.mjs node scripts/alinhar-palavras.mjs <proj>` (~2 min para 142 s na placa de vídeo). Corrigiu de novo? Alinhe de novo;
    5. **à mão:** `02_analise/transcricao_corrigida.md`, no molde do piloto (mesma pasta): cabeçalho curto (áudio, passadas, nº de correções) e uma linha `- [m:ss.d] frase` por frase, com os tempos do `palavras.json` já alinhado; embaixo de cada dúvida, `⚠ "o que se ouviu"; "alternativa"?`. O `diretor-paper-vox` para sem esse arquivo. Palavra em dúvida fica FORA da tela até o Jorge responder (por texto). ⏸ dúvidas.
  - **P2 Proposta de cenas:**
    - `diretor-paper-vox` modo "cenas" → `node <proj>/03_roteiro/montar_shotlist.mjs` → `shotlist.json`/`shotlist.md` (estações em blocos, chegadas de câmera, peças, montagens nos silêncios, SFX candidatos);
    - `node scripts/validar-shotlist.mjs <proj>` até 0 ERRO;
    - **objeto novo:** cena que pede objeto fora do catálogo do `objetos.tsx` é peça nova num modelo fixo. O `diretor-paper-vox` o propõe na shot list marcado "objeto novo", e você pede o ⏸ do Jorge junto com a shot list. Aprovado, quem implementa é você (conversa principal), antes do P5: componente + linha no `MAPA` de `src/modelos/paper-vox/objetos.tsx`, depois `node scripts/vez.mjs node scripts/regressao-paper-vox.mjs`. O gerador do mural PARA com erro se usar objeto que não está no `MAPA` (antes a peça sumia calada);
    - `checador-de-afirmacoes` com o texto de tela e a fala de cada estação, avisando: a fala está gravada, então correção só com palavras da própria fala ou no visual. O checador só lê: você grava o resultado em `03_roteiro/checagem-texto-tela.md` (molde: o do piloto). ⏸ Jorge.
  - **P3 Prompts do Flow:** modo "prompts" → `03_roteiro/prompts_flow.md`/`.json` (blocos FOTO, RECORTE em fundo azul #0000FF, MONT 9:16 P&B; Nano Banana 2.1 = 0 crédito). ⏸ Jorge.
  - **P4 Imagens:**
    - geração no Flow pelo Chrome do Jorge (regras do `CLAUDE.md`; 0 crédito; download por "Baixar lote"; a escolhida em 2K) → `04_broll/ia_flow/`;
    - `diretor-de-arte` escolhe;
    - recortes: `node scripts/recorte-chroma.mjs <entrada> <saida.png> --pb --aparar [--choke 1|2]` → folha de contato. ⏸ Jorge.
  - **P5 Mural:** modo "mural" → `node <proj>/03_roteiro/montar_quadro.mjs` → `03_roteiro/quadro.json`:
    - cada SFX ancorado no instante visual com `M.ev.*` e `M.sfx(plano, {naMixagem: true})`;
    - cortes de trilha (só voz nos momentos tensos ou de ênfase);
    - 2 opções de trilha da biblioteca (`%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/`) em `M.trilha({cortes, opcoes, escolhida})`;
    - sem 2 opções adequadas no `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/catalogo.md` (evite as do vídeo anterior)? Busque no Pixabay Music pelo arco do vídeo, ⏸ apresente 2–3 com link, duração e Content ID, baixe só as aprovadas direto em `%SOUTO_VIDEO_PROJETOS%/_biblioteca/musicas/` (o `lib/mural.mjs` recusa trilha fora de lá; não use `05_audio/musica`) e acrescente a linha no `catalogo.md`. Depois, o modo "mural" de novo.
  - **P6 Prévia:** avise o tempo (≈ 4,2 s/s: ~10 min para 144 s) → `node scripts/vez.mjs node scripts/render-paper-vox.mjs <proj> --previa --manter-base`:
    - sai uma versão por trilha (`06_previas/previa_<AAAAMMDDHHMM>_paper_trilha-A.mp4` e `_trilha-B.mp4`) + a base sem trilha `06_previas/previa_<AAAAMMDDHHMM>_paper.base.mp4` (com `--manter-base`);
    - folha de quadros + `revisor-de-video`. ⏸ Jorge (a trilha que ele escolher vai em `escolhida`);
    - ajuste pontual: corrija o gerador, rode-o e confira com `--trecho a b`.
  - **P7 Refino milimétrico dos SFX** (calibração original, 2026-10-20, para todo vídeo novo):
    - `node scripts/refinar-sfx.mjs <proj> --video 06_previas/previa_<AAAAMMDDHHMM>_paper_trilha-<X>.mp4` (a prévia COM trilha e SFX, nunca a base) → `03_roteiro/sfx_refino.md` (cada SFX: evento visual, ponto do som, desvio em ms, quadro) + carretel `06_previas/sfx-refino_<data>.mp4` (1 clipe de 1,5 s por SFX, número e evento escritos, barra azul elétrico no quadro exato). ⏸ Jorge;
    - ele pede por número ("o 7 entra 2 quadros antes") → `{ajuste: -83}` (ms) na linha do plano do gerador → `node <proj>/03_roteiro/montar_quadro.mjs`;
    - `node scripts/mixar-audio.mjs <proj> --video 06_previas/previa_<AAAAMMDDHHMM>_paper.base.mp4 --props 03_roteiro/quadro.json --trilha <X> --saida 06_previas/<nome>.mp4` (segundos, sem render) → `refinar-sfx.mjs` de novo com `--video 06_previas/<nome>.mp4` (já com trilha e SFX) → novo carretel. ⏸ Jorge.
  - **P8 Final:** ⏸ render longo (≈ 12,4 s/s: ~30 min para 144 s) → `node scripts/vez.mjs node scripts/render-paper-vox.mjs <proj>` → `07_final/<proj>_final.mp4` com a trilha escolhida → folha de quadros + loudness (−14 LUFS, pico ≤ −1 dB). Informe o caminho, a duração e os créditos de terceiros, se houver.
  - **P9 Fechamento:** `legendista` (fonte: `02_analise/transcricao_corrigida.md` + `03_roteiro/shotlist.md`) → `Publicados.md` ("Reels · PAPER VOX ANIMATION").
- **INSTAGRAM - VOX - B-ROLLs** (`vox-broll-instagram`, composição `VoxBroll`, 9:16 a 24 fps; fixo desde 2026-10-30). Colagens animadas no estilo Vox sobre o vídeo do Jorge falando. Guia: `referencias/modelos/vox-broll-instagram/guia-de-estilo.md`. Fluxo próprio, V0–V11, no lugar das etapas 2–7c:
  - **Molde:** o piloto `%SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino` (gerador `03_roteiro/montar_creatina.mjs` → `vox.json` + `plano-de-batidas.md`). O genérico mora em `scripts/lib/vox.mjs` e `scripts/lib/vox-mural.mjs`. Nunca rode o gerador do piloto sem `--saida`: grava em cima da referência da regressão.
  - **Agente do formato:** `diretor-vox` (`.claude/agents/04-video/diretor-vox.md`), nos modos "plano", "prompts" e "gerador". Se ele não estiver na lista, rode um general-purpose com as instruções desse arquivo.
  - **Não se aplica:** `edicao.json`, agente `montador`, `validar-edicao.mjs` (nem o hook), ilha (`preview_start ilha` e `ilha.mjs` pedem `edicao.json`), `render.mjs`, `sfx-variado.mjs`, `normalizar-broll.mjs`. O arquivo do vídeo é o `03_roteiro/vox.json` (escrito pelo gerador); a conferência é pelo `validar-vox.mjs` e por prévia renderizada.
  - **V0 Entrada:** etapa 0 (plataforma, formato e a pergunta do bruto) → `node scripts/novo-projeto.mjs "<nome>" "<caminho>"`. Dê logo a estimativa honesta (~2–3 h de máquina; pesam o Flow, a RAM e as aprovações) e pergunte se ele quer **direto** (sem as paradas ⏸; a liberação vale só para aquele vídeo) ou com as paradas. Bruto de câmera (1b): `preparar.mjs <proj> --modelo vox-broll-instagram`. Bruto fora de 1080×1920 a 24 fps: o bruto de trabalho do guia (Pipeline, etapa 0), pela fila. Antes de Flow, recorte ou render: ≥ 2 GB livres; se faltar, peça ao Jorge para fechar programas.
  - **V1 Decupagem** (só se ele marcar): etapa 2b (`decupar-inteligente.mjs` + `decupador` + `--render`); depois, o `alinhar-palavras.mjs` com `--audio 01_bruto/bruto_decupado.mp4` e a prop `bruto` no decupado (guia, Pipeline, etapa 1).
  - **V2 Palavras** (nesta ordem; os arquivos marcados "à mão" são da conversa principal):
    1. `node scripts/assistir.mjs <proj>/01_bruto/bruto.mp4 <proj>/02_analise` (folhas de quadros: rosto e enquadramento);
    2. `node scripts/transcrever.mjs <proj>/01_bruto/bruto.mp4 <proj>/02_analise --principal`;
    3. **à mão:** `02_analise/correcoes.json` (molde: o do piloto) → `node scripts/corrigir-palavras.mjs <proj> <proj>/02_analise/correcoes.json`;
    4. `node scripts/vez.mjs node scripts/alinhar-palavras.mjs <proj>`. **Bruto sem pausa** (o Jorge já aperta os cortes; no piloto, o padrão cortou trechos de 89 s): `--limiar -30 --min 0.15` e confira o `02_analise/alinhamento.md`. Esse limiar marca fala baixa como silêncio: a corrida de palavras com erro ≥ 0,45 s ou espremida volta para a média do turbo longo com o small, quando os dois concordam (molde: `02_analise/transcricao_corrigida.md` do piloto, "Tempo das palavras");
    5. **à mão:** `02_analise/transcricao_corrigida.md` (molde: o do piloto), com as dúvidas ⚠. Palavra em dúvida fica FORA da tela até ele responder (por texto). ⏸ dúvidas.
  - **V3 Plano de batidas:** `diretor-vox` modo "plano" → `03_roteiro/plano-de-batidas.md` (espinha nos fins de frase, 2 atos acima de 75 s, fichas das animações, imagens por origem e nº de stills do Flow, cards de contexto com a fonte, recorte da cabeça, SFX, trilha, opções marcadas e render estimado) → `checador-de-afirmacoes` no texto de tela e nos cards, avisando que a fala está gravada: correção só no visual ou num card "Obs." depois da frase (Decisões 2026-10-29). O checador só lê: você grava o resultado em `03_roteiro/checagem-texto-tela.md` (molde: o do piloto). ⏸ Jorge (por número).
  - **V4 Prompts do Flow:** modo "prompts" → `03_roteiro/prompts_flow.md`/`.json` (FOTO e RECORTE em fundo azul, look C; Nano Banana 2.1 = 0 crédito). ⏸ Jorge.
  - **V5 Imagens:** Flow pelo Chrome do Jorge (regras do `CLAUDE.md`; 1 ou 2 gerações por disparo, com pausa; ≥ 2 GB livres e nada renderizando) → `04_broll/ia_flow/` → `diretor-de-arte` escolhe (`escolhas.json`) → `node scripts/recorte-chroma.mjs <entrada> <saida.png> --pb --aparar [--choke 1|2]` → folha de contato. Trilha nova, se faltar no catálogo: como no P5 do PAPER VOX. ⏸ Jorge.
  - **V6 Recorte da cabeça** (só a moldura): pela fila e só com o cache, `npm_config_offline=true node scripts/vez.mjs node scripts/recortar.mjs <proj> <ini> <fim> <nome>` (no PowerShell, `$env:npm_config_offline='true'` antes): online, o `npx` baixaria uma versão nova sozinho. Ele imprime o JSON do recorte e não grava: grave à mão em `04_broll/recortes/<nome>.json`. Falhou por falta de pacote ou modelo? ⏸ com fonte e tamanho antes de liberar a rede (plano B: moldura sem recorte).
  - **V7 Montagem:** modo "gerador" → `03_roteiro/montar_<slug>.mjs` → `vox.json` + `plano-de-batidas.md` regravado; `node scripts/validar-vox.mjs <proj>` até 0 ERRO; `node scripts/refinar-sfx.mjs <proj> --props 03_roteiro/vox.json` até "Avisos: nenhum". A 1ª rodada do gerador mede o banco de SFX e é lenta (no piloto, com pouca RAM, passou de 1 h); as seguintes reaproveitam a escolha (~3 min).
  - **V8 Prévia:** avise o tempo → `node scripts/vez.mjs node scripts/render-vox.mjs <proj> --previa --manter-base` (meia resolução; uma versão por trilha de `musicas` + a base sem trilha) → folha de quadros pelo ffmpeg, brilho quadro a quadro (YAVG: Y < 10 só no preto final) e `revisor-de-video`. Área segura do Reels: confira na folha de quadros da prévia (legenda e textos fora da faixa de baixo e da coluna de ícones da direita; a ferramenta de conferência do lab não vem no repositório). ⏸ Jorge (a trilha que ele escolher vai em `musica`). Ajuste pontual: corrija o gerador e confira com `--trecho a b`.
  - **V9 Refino milimétrico dos SFX** (calibração original, 2026-10-20, para todo vídeo novo): `node scripts/refinar-sfx.mjs <proj> --props 03_roteiro/vox.json --video 06_previas/<prévia com trilha>.mp4` → `sfx_refino.md` + carretel. ⏸ Jorge. Ele pede por número ("o 7 entra 2 quadros antes") → `{ajuste: -83}` como 5º item da linha do `PLANO_SFX` → gerador → `node scripts/mixar-audio.mjs <proj> --video 06_previas/<base>.mp4 --props 03_roteiro/vox.json --trilha <X> --saida <caminho absoluto>` (segundos, sem render) → carretel novo.
  - **V10 Final:** ⏸ render longo (≈ 5,6 s/s + ~75 s de mixagem: ~12 min para 112 s) → `node scripts/vez.mjs node scripts/render-vox.mjs <proj>` (resolução cheia, concurrency 1, sem angle; no fim, o custo de cada bloco) → `07_final/<proj>_final.mp4` com a trilha escolhida → folha de quadros, YAVG e loudness (−14 LUFS, pico ≤ −1 dB). Informe o caminho, a duração e os créditos de terceiros, se houver.
  - **V11 Fechamento:** `legendista` (fonte: `02_analise/transcricao_corrigida.md` + `03_roteiro/plano-de-batidas.md`) → `Publicados.md` ("Reels · VOX - B-ROLLs"); as stills do Flow para a biblioteca (etapa 8).
- **Os 5 formatos são FIXOS (usuário, 06/10/2026; o PAPER VOX desde 2026-10-20; o VOX - B-ROLLs desde 2026-10-30):** formato, estilo e guia só mudam a pedido dele. **Mexeu no motor?** Antes de entregar, as 6 regressões, uma por vez:
  - `node scripts/regressao.mjs` (TELA DIVIDIDA clássico; precisa sair IDÊNTICO);
  - `node scripts/regressao.mjs --cut` (precisa sair EQUIVALENTE);
  - MIX: `node scripts/vez.mjs node scripts/regressao.mjs --mix` (precisa sair EQUIVALENTE);
  - TELA DIVIDIDA atual: `node scripts/vez.mjs node scripts/regressao.mjs --td2` (IDÊNTICO, ou EQUIVALENTE com PSNR ≥ 40 dB);
  - `node scripts/vez.mjs node scripts/regressao-paper-vox.mjs` (IDÊNTICO, ou EQUIVALENTE com PSNR ≥ 40 dB a 135×240). Script próprio (o render e o áudio do Paper Vox são outros). Obrigatória depois de qualquer mudança em `src/modelos/paper-vox/`, `src/kit/`, `Root.tsx`, `scripts/render-paper-vox.mjs`, `scripts/lib/mural.mjs` ou pacotes;
  - mudou `scripts/lib/mural.mjs`? Confira também que o gerador do piloto gera o mesmo `quadro.json`, sem sobrescrever a referência: de dentro do piloto, `node 03_roteiro/montar_quadro.mjs --saida <arquivo no scratchpad>` e compare (md5) com o `03_roteiro/quadro.json`. Nunca rode o gerador do piloto sem `--saida`;
  - `node scripts/vez.mjs node scripts/regressao-vox.mjs` (EQUIVALENTE com PSNR ≥ 45 dB a 135×240, contra 3 trechos do final aprovado do piloto do VOX). Script próprio. Obrigatória depois de qualquer mudança em `src/modelos/vox/`, `src/kit/`, `src/legendas.ts`, `Root.tsx`, `scripts/render-vox.mjs` ou pacotes;
  - mudou `scripts/lib/vox.mjs`, `scripts/lib/vox-mural.mjs` ou `scripts/lib/mural.mjs`? Confira também que o gerador do piloto do VOX grava o mesmo `vox.json`: de dentro do motor, `node %SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino/03_roteiro/montar_creatina.mjs --saida <arquivo no scratchpad>` e compare (md5) com o `03_roteiro/vox.json`.

## Sem repetição visual (diretriz do usuário)
- No plano (etapa 3), liste os **termos recorrentes** e o número de aparições; cada aparição ganha uma visual diferente (3–5 variações por termo: foto, vídeo, ilustração, 3D, gráfico, ângulos diferentes). Nunca o mesmo arquivo — nem variações quase idênticas — duas vezes no mesmo vídeo.
- Antes da prévia, confira no `edicao.json` se algum `broll` se repete.
- No PAPER VOX (sem `edicao.json`), confira na `shotlist.json` se alguma `fonte` (`flow:Fnn`, `biblioteca:<arquivo>`) aparece em duas estações ou planos de montagem: o `validar-shotlist.mjs` só conta o teto.
- No VOX - B-ROLLs (sem `edicao.json`), o `validar-vox.mjs` avisa imagem repetida no `vox.json`; o `plano-de-batidas.md` lista a origem de cada uma.

## Revisão antes de entregar (aprendido no 1º vídeo)
- Clipes de animação (ícones, UI, 3D) costumam começar vazios: confira o quadro inicial e ajuste `brollIni` para que o momento-chave coincida com a palavra.
- Bancos erram objetos específicos: sempre revise candidatos numa folha de miniaturas; se falhar, gere **imagem** no Flow (0 créditos).
- Confira a folha de quadros da prévia completa (1 quadro/s) antes de mostrar ao usuário.

## Regras
- Nunca invente fatos no B-roll: se a fala cita uma pessoa/marca real, peça a imagem ao usuário ou use material com licença; não gere pessoas reais por IA.
- Sempre informe tempo estimado de render antes de renders longos (medidos no `CLAUDE.md`: prévia ≈ 3,2 s de render por segundo de vídeo, final 9:16 ≈ 7,1 s por segundo, final do MIX ≈ 5–6,5 s por segundo; PAPER VOX: prévia ≈ 4,2 s por segundo e final ≈ 12,4 s por segundo, medidos no piloto de 144 s; VOX - B-ROLLs: final ≈ 5,6 s por segundo, medido no piloto de 112 s, com a moldura a ~14 s/s; cenas com 3D/efeitos custam mais). Anote tempos novos no `CLAUDE.md`.
- Se algo falhar, diga o que falhou e a alternativa; não troque silenciosamente de ferramenta.

## Integração com o resto do repositório souto-treinador
- **Roteiro:** se o vídeo tiver roteiro em `02 - ROTEIROS/Roteiros/`, use-o no plano (cards, gráficos, fontes e B-roll saem dele). As fontes citadas na tela vêm da seção **Fontes** do roteiro. No PAPER VOX (sem `plano.md`): se o áudio veio de um roteiro, o texto aprovado é a referência das correções do P1 (`correcoes.json`), e as dúvidas ⚠ ficam só para o que diverge dele; as Fontes vão para a legenda (P9).
- **Agentes:** `revisor-de-video` roda as checagens (`checar-mix.mjs`, regressões) e confere as prévias quadro a quadro, devolvendo só a lista de problemas. Use-o em vez de abrir dezenas de quadros na conversa principal.
- **Fechamento:** depois do final aprovado, gere a legenda com o agente `legendista` e registre o vídeo em `05 - PUBLICAÇÃO E CRESCIMENTO/Publicados.md` (status `pronto`).
