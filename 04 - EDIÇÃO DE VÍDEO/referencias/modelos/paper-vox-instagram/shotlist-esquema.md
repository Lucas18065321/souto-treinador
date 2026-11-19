# Esquema da shot list: INSTAGRAM - PAPER VOX ANIMATION (apoio do guia de estilo)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


A shot list é a proposta de cenas da etapa P2 (`guia-de-estilo.md`): um mural só, com estações em blocos, montagens nos silêncios e o card. Esquema **real**, lido do piloto (`%SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece/03_roteiro/shotlist.json` e `montar_shotlist.mjs`), do `scripts/validar-shotlist.mjs` e do `scripts/lib/mural.mjs`.
- **Nunca se digita tempo à mão.** O `03_roteiro/montar_shotlist.mjs` (copiado do piloto) gera `shotlist.json` (máquina) e `shotlist.md` (leitura do Jorge) a partir do `02_analise/palavras.json` travado e alinhado. Mudou a transcrição ou o alinhamento? Rode o gerador de novo.
- **Quem lê a `shotlist.json`:** o `validar-shotlist.mjs` (regras) e o `lib/mural.mjs` (faixa de palavras de cada estação, chegada, punch-in, SFX candidatos, montagens).
- Substitui o `05_LAB/formatos/4-paper-vox-animation/shot-list-esquema.json`, que está velho (ver o fim deste arquivo).

## Chaves do topo
| Chave | Piloto | Para que serve |
|---|---|---|
| `formato` | `"paper-vox-animation"` | rótulo (o id do modelo, `paper-vox-instagram`, vai no `quadro.json`) |
| `versao` | `"quadro-continuo"` | rótulo |
| `fps`, `w`, `h` | `24`, `1080`, `1920` | rótulo |
| `voz` | `"01_bruto/bruto.mp3"` | o áudio (o mural acha sozinho `bruto.mp3`, `.wav` ou `.m4a`) |
| `palavras` | `"02_analise/palavras.json"` | o validador lê as palavras daqui |
| `musica` | `null` | a trilha não se decide aqui: fica no gerador do mural (`M.trilha`) |
| `duvidas` | `[{"palavra": "humilhando", "seg": 63.11}, {"palavra": "era", "seg": 14.53, "nota": "\"já era culpa\" × \"já é culpa\""}]` | palavra em dúvida na tela = ERRO, até o Jorge responder |
| `termos_recorrentes` | `{"sociedade": 3, "saúde": 4, …}` | termo que volta na fala ganha variação visual (sem repetição) |
| `estacoes` | 36 | ver abaixo |
| `montagens` | 5 | ver abaixo |
| `card` | 1 | registro do card (o card real é o fixo do `M.card()`) |

## Estação (`estacoes[]`)
| Chave | Tipo | O que é | Quem usa |
|---|---|---|---|
| `id` | `"E01"`… | nome da estação (o mesmo no gerador do mural) | todos |
| `bloco` | número | coluna do mural (um look por bloco) | leitura |
| `ini`, `fim` | s (gerados) | faixa da estação: a palavra pertence a ela se o meio da palavra cai em `[ini, fim)` | validador, mural |
| `fala` | texto | as palavras da faixa, exatas (o validador compara sem acento e sem pontuação) | validador |
| `look` | `editorial` · `colagem` · `marmore` | o papel de base | leitura; quem escreve o gerador do mural repete no `base(c, look)` |
| `receita` | nome | `jornal-vivo`, `tipo-escala`, `objeto-papel`, `estatua-sanduiche`, `mesa-escura`, `interface-palco`, `colagem-vox`, `cena-em-camadas`, `capitulo-vox`, `silhueta-gradiente`, `colagem-monta`, `icone-orbital` | validador (nunca 3 iguais seguidas) |
| `chegada` | `{"tipo": "…"}` | como a câmera chega (ver "Chegada") | mural, validador |
| `camera` | texto ou `null` | movimento próprio, descrito (ex.: "na pausa depois de \"exercitar\", chicote ↘ para o celular") | leitura; quem escreve o gerador do mural traduz em `extraCam` |
| `acento` | `"azul elétrico"` ou `null` | 1 acento azul elétrico por estação, no máximo | leitura |
| `respiro` | bool | frase delicada, câmera quase parada | validador (não acusa buraco sem evento) |
| `rajada` | bool (opcional) | estação curta de propósito | validador (não acusa estação < 1 s) |
| `camadas` | `[{fonte, o}]` | `fonte`: `"codigo"`, `"flow:Fnn"` ou `"biblioteca:%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel/<arquivo>"`; `o`: o que se vê | validador (conta imagens) |
| `texto` | `[{t, escala, ancora, truque?}]` | texto de tela: `t` da fala, `escala` `apoio` ou `chave`, `ancora` = 1ª palavra | validador; mural (a âncora da `chave` = instante do punch-in) |
| `eventos` | `[{ancora \| seg, o}]` | o que acontece a cada palavra | validador (conta eventos) |
| `sfx` | `[{ancora \| seg, cat}]` | SFX candidatos (o plano curado fica no gerador do mural) | validador; mural (`M.S(id, cat, n)` devolve o instante da âncora) |

**Âncora:** `"palavra@segundo"`, com a palavra como está no `palavras.json` (inclusive pontuação: `"exercitar.@22.45"`) e o `ini` dela com 2 casas. O validador acha a palavra com esse texto mais perto do segundo (até 1,0 s), dentro da faixa da estação (±0,05 s; eventos ±0,5 s). `seg` = instante direto, para evento na pausa.

**Chegada:** o `tipo` é texto livre, mas o mural só entende o nome de código que encontrar nele, nesta ordem: `chicote`, `deslize`, `snap-zoom`, `snap`, `giro`, `queda`, `recuo`, `recursão`, `emerge`, `abre` (sem nenhum = `deslize`). Escreva o nome exato primeiro: "giro 8° + deslize ←" vira `deslize`. A 1ª estação é sempre `abre`, e a que vem depois de uma montagem é sempre `emerge`.

**Exemplo** (E10 do piloto):
```json
{
 "id": "E10", "bloco": 2, "ini": 20.66, "fim": 24.3,
 "fala": "sem energia nem pra se exercitar.",
 "look": "colagem", "receita": "objeto-papel",
 "chegada": {"tipo": "deslize ←"},
 "camera": "na pausa depois de \"exercitar\", chicote ↘ para o celular",
 "acento": "azul elétrico", "respiro": false,
 "camadas": [
  {"fonte": "codigo", "o": "bateria de papel recortado"},
  {"fonte": "biblioteca:%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel/conceitos/tenis-gastos-papel-pb.jpg", "o": "foto: tênis gastos parados"}
 ],
 "texto": [
  {"t": "sem energia", "escala": "apoio", "ancora": "sem@20.70"},
  {"t": "exercitar", "escala": "chave", "ancora": "exercitar.@22.45"}
 ],
 "eventos": [
  {"ancora": "energia@20.93", "o": "bateria esvazia barra por barra (12 fps), a última em azul elétrico"},
  {"ancora": "nem@21.48", "o": "bateria pisca vazia"},
  {"ancora": "exercitar.@22.45", "o": "foto dos tênis pousa ao lado"},
  {"seg": 23.6, "o": "chicote ↘ até o celular (na pausa)"}
 ],
 "sfx": [{"ancora": "energia@20.93", "cat": "ui"}, {"ancora": "exercitar.@22.45", "cat": "papel"}]
}
```
No mural, a foto acabou entrando com `voa` (padrão de foto) e só o `ui` ficou no plano curado: a shot list propõe, o gerador do mural decide.

## Montagem (`montagens[]`)
| Chave | Tipo | O que é | Quem usa |
|---|---|---|---|
| `id` | `"M1"`… | nome da montagem (o mesmo no `mergulho` do gerador do mural) | todos |
| `tema` | texto | o assunto dos planos | leitura |
| `pausa` | `[a, b]` s | o silêncio: `a` = `fim` da estação de antes, `b` = `ini` da seguinte | validador; mural (casa com as estações por esses tempos, ±0,02 s) |
| `entrada` | `{dur, o}` | o mergulho (0,25–0,4 s no piloto) e onde a câmera some | validador, mural |
| `saida` | `{dur, o}` | a emergência (0,1–0,3 s) e onde a câmera reaparece | validador, mural |
| `planos` | `[{dur, fonte, o}]` | `dur` 0,12–0,4 s; `fonte` `"flow:Mnn"` → `04_broll/ia_flow/Mnn.jpg` | validador, mural |
| `sfx` | `[{seg, cat}]` | candidatos (no plano curado, o plano de montagem não tem som) | validador |

- **Onde a câmera mergulha** não fica na shot list: é o `mergulho: {M1: ['E06', 40, 170]}` do gerador do mural.

**Exemplo** (M1 do piloto):
```json
{
 "id": "M1", "tema": "a correria de hoje", "pausa": [15.13, 16.21],
 "entrada": {"dur": 0.25, "o": "mergulho na tinta do carimbo"},
 "saida": {"dur": 0.1, "o": "emerge na mesa de papelão (E07)"},
 "planos": [
  {"dur": 0.2, "fonte": "flow:M01", "o": "ônibus lotado à noite, gente de pé de costas segurando a barra"},
  {"dur": 0.2, "fonte": "flow:M02", "o": "engarrafamento à noite visto de dentro do carro, luzes de freio"},
  {"dur": 0.2, "fonte": "flow:M03", "o": "copo de café de papel ao lado do laptop, mão pegando às pressas"},
  {"dur": 0.2, "fonte": "flow:M04", "o": "mãos com o celular andando rápido na rua à noite (tela ilegível)"}
 ],
 "sfx": [{"seg": 15.13, "cat": "whoosh"}, {"seg": 15.38, "cat": "clique (1 por plano, rodízio)"}]
}
```
O `clique` por plano é sobra da proposta do piloto: no plano curado, o plano de montagem ficou sem som (correção da prévia 1). Não proponha mais.

## Card (`card`)
```json
{"id": "CARD", "ini": 141.19, "fim": 144.19, "receita": "colagem-monta",
 "texto_fixo": ["Jorge Souto", "educador físico", "CREF 000000-G/UF", "@soutotreinador"],
 "icones": ["Instagram", "YouTube"], "o": "peças de papel escuro montam e travam (ref-02); único lugar com o @",
 "sfx": [{"seg": 141.29, "cat": "papel"}]}
```
É só registro: o card real (tempos, tamanhos, degradê) sai fixo do `M.card()`.

## Como o `montar_shotlist.mjs` monta (o que se reescreve a cada vídeo)
- **`EST`** (uma linha por estação): `{id, bloco, de, look, receita, chegada, camera?, acento?, respiro?, camadas: [{fonte, o}], texto: [{t, escala, a?, truque?}], eventos: [{a | s, o}], sfx: [{a, cat}]}`.
  - `de` = as primeiras palavras da estação (procuradas depois da estação anterior).
  - `a` = frase-âncora dentro da estação; `"frase#n"` = n-ésima ocorrência. Sem `a`, a âncora do texto é o próprio `t`. `s` = segundo direto.
- **Tempos** (gerados): `ini` = 1ª palavra − 0,04 s (0 na 1ª estação); `fim` = 1ª palavra da seguinte − 0,04 s; com montagem depois, `fim` = fim da fala + 0,03 s; a última, fim da fala + 0,1 s.
- **`MONT`**: `{id, depois, antes, entrada: {dur, o}, saida: {dur, o}, tema, planos: [{dur, o}]}`. A `pausa` sai de `depois.fim` e `antes.ini`; as fontes são numeradas `M01…` em sequência.
- **À mão:** `duvidas` (com `seg(...)` da palavra; as mesmas ⚠ da `02_analise/transcricao_corrigida.md`), `termos_recorrentes` e o texto do `shotlist.md`.
- **Ao copiar o do piloto, troque os textos fixos que ficaram velhos:** o cabeçalho ("formato 4", caminho `scripts/lab/validar-shotlist.mjs`, hoje `scripts/validar-shotlist.mjs`) e as linhas do `shotlist.md` "Acento só azul elétrico", "Sem música (padrão do guia)… 6–9 dB" e "Mixkit quando você baixar". O certo hoje está no `guia-de-estilo.md` (degradês, trilha a 1/4 com cortes, SFX 12–17 dB abaixo da voz).
- **`shotlist.md`:** cabeçalho com o resumo, uma tabela por bloco (`tempo | fala | o que se vê | a cada palavra | imagem | SFX`), uma linha por montagem logo depois da estação de antes, o card, a seção Imagens (Flow + biblioteca, "Omni: 0") e a seção Som.

## O que o `validar-shotlist.mjs` confere
Uso (de dentro do motor): `node scripts/validar-shotlist.mjs <proj> [--shotlist 03_roteiro/shotlist.json]`. Precisa de **0 ERRO** antes de mostrar ao Jorge.

**ERRO (código 1)**
1. Palavra da fala fora de qualquer estação, ou em duas.
2. `fala` diferente da transcrição do intervalo.
3. Montagem por cima da fala (palavra cujo meio cai dentro da pausa, a mais de 0,05 s das bordas).
4. Planos + entrada + saída maiores que a pausa + 0,3 s; plano fora de 0,12–0,4 s.
5. Texto de tela que não está na fala da estação; âncora de texto ou de evento que não acha a palavra.
6. Palavra vetada na tela: promessa, cura, curar, garantia, garantido, garantida, 100%, milagre, definitivo, definitiva.
7. Palavra em dúvida (`duvidas`) na tela.
8. Menos de 4 eventos nos 3 primeiros segundos.
9. 3 receitas iguais seguidas.
10. O mesmo arquivo de SFX duas vezes seguidas (campo `som`, quando houver).
11. Imagens acima do teto: 25 por minuto de fala (conta `flow:` e `biblioteca:` das camadas + os planos de montagem).

**Não confere (à mão, antes de mostrar ao Jorge)**
- **Repetição visual:** o validador junta as fontes num conjunto e só conta o teto. Confira que nenhuma `fonte` (`flow:Fnn`, `flow:Mnn`, `biblioteca:<arquivo>`) aparece em duas estações ou planos de montagem (rima entre montagens só de propósito).
- **Objeto que não existe no motor:** só o gerador do mural acusa (ver "Campos livres").

**AVISO**
- Buraco > 1,5 s sem evento (fora de `respiro`).
- Estação < 1 s (fora de `rajada`).
- A mesma chegada 3× seguidas.
- A mesma categoria de SFX 3× seguidas (o gerador do mural é mais duro: para com 2× seguidas).
- Menos de 35% das estações sem imagem.

**Evento** (para o gancho e para os buracos) = a chegada de cada estação (`ini`), cada palavra de cada texto de tela, cada evento e o início de cada plano de montagem. Piloto: 328 eventos, 1 a cada 0,43 s.

## Campos livres: o que o motor faz com eles
- `camera`, `camadas[].o`, `eventos[].o`, `truque`, `tema`, `o`: descrição para o Jorge aprovar e guia para quem escreve o gerador do mural. O motor não lê.
- **`truque`:** nunca proponha texto atrás de uma peça. O Jorge reprovou ("polêmica" ficou atrás da estátua): o texto fica sempre por cima. A E14 do piloto ainda traz "atrás do busto" no json (histórico); o motor ignora e pôs o texto por cima.
- `sfx`: só candidatos. O plano curado, com o instante visual de cada som (`M.ev.*`), mora no gerador do mural.
- **Objeto fora do catálogo** (o `MAPA` do `objetos.tsx`; lista em "Objetos de papel" do guia): marque "objeto novo" na `o` da camada e peça o ⏸ do Jorge junto com a shot list. É peça nova num modelo fixo: a conversa principal implementa antes do mural, e o gerador do mural para com erro se o nome não existir.

## O que mudou em relação ao esquema velho do lab (`shot-list-esquema.json`)
- `cenas` virou `estacoes` (o mural contínuo), mais `montagens` e `card`.
- `voz` era `bruto.wav`; hoje é `bruto.mp3` (ou `.wav`/`.m4a`).
- `palavra_idx` virou âncora `"palavra@segundo"` gerada das palavras.
- `"truque": "atras"` saiu (reprovado).
- Saíram `variacao_de`, `luz`, `fundo`, `entrada` da cena, `flow` dentro da cena e `render`: luz, fundo e entrada são do código e do gerador do mural; prompts ficam em `prompts_flow.json`; `musica` agora é `null` (trilha no gerador do mural).
