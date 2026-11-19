# SFX do lab: fontes verificadas e plano da correção do TELA DIVIDIDA

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Status (2026-10-19): **download aprovado pelo Jorge.** Glitch Noises catalogado; Mixkit e 99Sounds com o Jorge.
2026-10-20: categoria nova `papel` (6 sons sintetizados), usada pelo INSTAGRAM - PAPER VOX ANIMATION.

## Para o Jorge: o que vem aqui e o que você baixa
- **Vem no repositório:** os 133 sons Glitch Noises (CC0, prova em `licencas/`), os 6 de papel e o `catalogo.tsv`.
- **Você baixa à mão (licença proíbe redistribuir):** Mixkit pela `lista-mixkit.html` → `node scripts/sfx/sfx-importar-mixkit.mjs` (de dentro de `motor`); 99Sounds → lote JSON + `node scripts/sfx/sfx-catalogar.mjs <lote.json>`. Passo a passo: `docs/guias/04-video.md`, seção 10. Esses arquivos ficam só no seu PC (o `.gitignore` barra).
- O texto abaixo é o histórico da curadoria original (datas e aprovações da calibração do motor).

## 0. O que já está na biblioteca do lab
- **Glitch Noises: 133 sons** escolhidos dos 1.101 sem ouvir.
  - Em cada grupo do `Metadata.csv`: tirei os 20% mais ásperos (planicidade espectral) e espalhei o resto do grave ao agudo (centroide).
  - Categorias: glitch 55, futurista 37, clique 16, scroll-ui 10, ding 6, whoosh 6 (com "wind up" ≤ 1 s), impacto 3.
  - Ficou de fora: alarmes, buzzers, ambiências, risers ásperos, intercom e as leituras longas de dados.
  - Prova de licença: `licencas/glitch-noises_read-me_2026-10-19.pdf` ("marked with CC0 1.0 Universal"). O zip e a extração foram apagados.
- **Papel ("pestana"): 6 sons**, 2026-10-20.
  - `papel/papel_01…06_pestana-N.wav`: virar e assentar página de papel, sintetizados por FFmpeg no piloto do INSTAGRAM - PAPER VOX ANIMATION.
  - Licença própria (feitos por código, sem Content ID). Catalogados no `catalogo.tsv`.
  - Uso: o PAPER VOX ANIMATION lê esta pasta pelo `motor/scripts/lib/mural.mjs` (o piloto usa a cópia dele, em `05_audio/sfx/lab/papel/`). Valem até chegar o papel do Mixkit.
  - Por isso a `sfx/lab/` não se move nem se renomeia sem ok do Jorge e sem atualizar o `/editar` 5b e o `lib/mural.mjs`.
- **Formato:** `sfx/lab/<categoria>/<categoria>_NN_<origem>-<nome>.wav`, em 48 kHz e 16 bits, sem metadados.
- **`catalogo.tsv`**, um som por linha:
  - `dur`;
  - `pico_dbtp` (pico verdadeiro);
  - `m_max_lufs` (loudness momentâneo máximo, o que o `sfx-variado` usa para nivelar contra a voz);
  - `t_m_max` (onde cai o pico; é o ponto que se alinha ao corte);
  - origem, original, licença e descrição.
- **Atenção:** os 6 whooshes e os 3 booms passam de 2,4 s. O `Edicao.tsx` corta o som em 2,5 s, então eles precisam da cópia aparada com fade.
- **Scripts** (em `motor/scripts/lab/`):
  - `sfx-catalogar.mjs <lote.json>` importa e mede qualquer lote. É idempotente.
  - `sfx-importar-mixkit.mjs` acha em Downloads os `mixkit-*-<id>.wav` da seleção (`selecao-mixkit.json`), cataloga e manda os originais para a Lixeira.
- **Mixkit (com o Jorge):**
  - Ele abre `lista-mixkit.html` no Chrome: 184 sons, 83 essenciais ★, com prévia ▶ e marcação do que já baixou.
  - Depois, de dentro do motor: `node scripts/sfx/sfx-importar-mixkit.mjs`.
- **99Sounds (com o Jorge):** ele baixa; depois, curadoria igual à do Glitch Noises, com lote + `sfx-catalogar.mjs`.

## 1. Fontes (pesquisa + checagem adversarial de licença, conteúdo e alternativas)
| Fonte | Licença (conferida na página oficial) | O que tem | Tamanho | Como baixa |
|---|---|---|---|---|
| **Mixkit** (mixkit.co/free-sound-effects) | Licença Mixkit SFX Free: projetos comerciais, YouTube, redes sociais e anúncios online, sem crédito. Proíbe redistribuir o som avulso ou dentro de ferramenta/template e registrá-lo em serviço de gestão de direitos. | Tags: glitch 67, teclado 22, máquina de escrever 24, papel 30, caneta/escrita 13, sci-fi 122, zoom 15, whoosh 20, swoosh 57, click 56, impacto 68, riser 7, chime 9, bell 62, transition 42, interface 15 (as tags se sobrepõem) | ~80–120 sons escolhidos: estimativa de 50–150 MB (a taxa do WAV não é publicada) | Sem login, WAV ou MP3, **um a um**. Os Termos (cláusula 9.10) proíbem baixar em massa com script ou bot, então quem clica é o Jorge. |
| **Glitch Noises** (Vladislav Zharkov, vladislavzh.itch.io/glitch-noises, abr/2025) | CC0 1.0 | 1.101 WAV 24 bits/48 kHz: UI 280, glitch 310, glitch bits 150, crackles 80, data 65, telemetria 45, intercom 45, bônus 56 (whoosh, riser) | zip de 606 MB | "Name your own price", sem mínimo declarado (US$ 0 a confirmar no botão) |
| **99Sounds Sci-Fi Sound Effects** (99sounds.org, 2023, Rescopic Sound) | Royalty-free para uso pessoal e comercial, crédito opcional, proíbe redistribuir | 90 sons sci-fi, 24 bits/96 kHz | 414 MB | Gumroad, que pode pedir e-mail (aí quem baixa é o Jorge) |

- **Descartado:**
  - **Sonniss GDC 2026** (7,47 GB em 5 zips): é um amostrador de 347 arquivos, e só uns 35–40 servem (2 glitches, nenhum teclado nem caneta). Não dá para baixar uma biblioteca só, e a licença proíbe usar os sons com IA ("developing, training, or enhancing").
  - Sem plano grátis que sirva: ZapSplat (exige crédito), Uppbeat (3 downloads por mês), YouTube Audio Library e BBC.
- **Plano B:** Pixabay SFX (MP3, risco de Content ID) e Freesound CC0 (exige conta, qualidade irregular), só para buracos pontuais.
- **Atenção:**
  - Nenhuma fonte protege contra um terceiro registrar o mesmo som no Content ID.
  - Guardar print da página da licença no dia do download.
  - O motor com a biblioteca dentro não pode ser compartilhado com terceiros nem virar template.
- **Depois do download:** catalogar em `sfx/lab/<categoria>/` em WAV 48 kHz, com os nomes do Motionix e um `catalogo.tsv` (categoria, arquivo, duração, pico, origem, licença). Os zips e as sobras vão para a Lixeira. Fica em `sfx/lab/` (já é de produção: `/editar` 5b e `scripts/lib/mural.mjs`). Mover só com ok do Jorge e atualizando esses dois.

## 2. Correção 1b: SFX alto e repetitivo no TELA DIVIDIDA
**Medido (2026-10-19):**
- `criativo-3` (132 s): 35 transições com som + 26 pops = 61 sons automáticos, 1 a cada 2,2 s. `whoosh_soft` sozinho cobre 30 das 35 transições.
- `criativo-1` (87 s): 13 + 24 = 37 sons, 1 a cada 2,4 s.
- `restricao-alimentar` (128 s): 25 + 14 = 39 sons.
- Voz do `criativo-1`: −15,9 LUFS. O `whoosh_soft.wav` tem −17,7 LUFS e entra a 0,45.
- O `Edicao.tsx` corta todo SFX em 2,5 s (`durationInFrames` fixo). Um som mais longo termina seco.

**APROVADO pelo Jorge em 2026-10-19 e em uso no `/editar` (etapa 5b, só TELA DIVIDIDA).**
- Script: `scripts/sfx/sfx-variado.mjs`. As regras finais estão no cabeçalho dele.
- Testado numa cópia do criativo 1 (já na Lixeira). Comparativo aprovado: `sfx/lab/previas/sfx-variado_criativo-1_antes-x-depois_0-30.mp4` (a cópia de teste foi para a Lixeira).
- **Resultado no criativo-1 (87 s):**

  | | Antes | Depois |
  |---|---|---|
  | Sons | 40 (27,6 por minuto) | 22 (15,2 por minuto) |
  | Sons diferentes | 6 | 21 |
  | Repetição máxima | pop_soft 24× | impacto manual 2× |
  | Pops | 24 | 8 |
  | Whoosh em relação à voz | −8 dB | −12 dB, ±1,5 |
  | Pop em relação à voz | −14 dB | −17 dB |

- **O que ficou provado:**
  - A imagem das prévias é idêntica: 720 de 720 quadros, PSNR infinito. O loudness final é o mesmo, −14 LUFS.
  - O `validar-edicao` dá 0 ERRO.
- **Revisão adversarial (2 revisores), tudo corrigido:**
  - Os sons manuais podiam se perder.
    - Agora há backup `<json>.antes-sfx.json` e um arquivo `sfx-variado.<json>.json` com manuais, gerados e a assinatura.
    - Som posto à mão vira manual; manual apagado sai.
    - Um json ambíguo para com aviso.
  - **Falha do ffmpeg** agora para tudo, e a medição ruim não entra no cache.
  - **Pop:** sai só na 1ª ocorrência. A regra dos 0,6 s também olha o pico dos manuais.
  - **Sorteio:** usa uma semente por evento. Tirar uma transição mantém o som dos outros 18 eventos.
  - **Banco:**
    - perdeu o Motionix 17 (cópia idêntica do 15) e 2 cliques baixos demais para o alvo;
    - o RMS agora é medido em estéreo;
    - o pico fica onde o automático punha o dele (blur ≈ corte + 0,1 s).
- `--conferir` avisa quando cenas ou destaques mudaram depois da rodada. Rode de novo antes do render.
- Cache das medições: `sfx/lab/medidas.tsv`.

**Plano original (mantido como registro):**
**Script `motor/scripts/sfx/sfx-variado.mjs <proj> [--edicao <json>]`** (não toca no `Edicao.tsx`):
1. Lê o `edicao.json` (só o modelo TELA DIVIDIDA) e recalcula os mesmos pontos do automático: transições blur, whip, flash e glitch, e palavras destacadas, com a mesma normalização da legenda.
2. **Transições em rodízio:**
   - Cada tipo tem seu banco de sons: blur → whooshes suaves; whip → whooshes rápidos e swooshes; flash → brilho e chime; glitch → glitches.
   - O mesmo som nunca aparece em duas transições seguidas nem entre os 3 últimos da categoria.
   - Até chegar a biblioteca nova, usa Motionix + os sintetizados.
3. **Menos pops:**
   - Só a 1ª ocorrência de cada palavra destacada.
   - No mínimo 5 s entre pops e nenhum a menos de 0,6 s de uma transição.
   - Sai de ~24 para ~8–10 por vídeo, com cliques variados.
4. **Volume medido, não fixo:**
   - Mede o pico momentâneo (`ebur128`) de cada som e a voz.
   - Transição fica ~10 dB abaixo da voz e clique ~14 dB abaixo (proposta, ajusta na prévia), com ±1,5 dB de variação.
   - Os sons manuais (riser, impacto) seguem a mesma regra.
5. **Sincronia:** alinha o pico do whoosh ao corte, em vez do deslocamento fixo de −0,22 s.
6. **Saída:**
   - Grava `"sfxAuto": false` + a lista `sfx` no json.
   - Copia os `.wav` para `05_audio/sfx/lab/` do projeto. O que passar de 2,4 s ganha uma cópia aparada com fade.
   - Imprime o antes × depois: sons por minuto, sons distintos, maior repetição e volumes.
7. **Teste:**
   - Numa cópia do `criativo-1` em `05_LAB/testes/`, só com o necessário: bruto, análise, roteiro, B-roll usado e áudio (~0,7 GB).
   - Prévia ⏸ de 30 s antes × depois, ~2 min de render cada.
   - Com o ok, o `/editar` ganha 1 passo que chama o script.
