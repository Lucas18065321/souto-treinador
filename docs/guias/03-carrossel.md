# Guia 03 — Carrosséis (passo a passo para quem não programa)

> Para: Jorge Souto (SOUTO TREINADOR) ou quem opera o sistema com ele.
> Pré-requisitos: **Guia 00 — Instalação geral** (Python, Node, Chrome, Claude Code) e **Guia 01 — Base científica** (pelo menos uma Ficha pronta). O **Guia 02 — Roteiros** explica o hook, que também serve aos carrosséis.
> Sistema: Windows 10/11, PowerShell, Claude Code aberto na raiz do repositório (`souto-treinador`).
> Testado em 2026-11-19 com: Windows 11, Python 3.12.10, Pillow 12.3.0, numpy 2.5.3, scipy 1.18.1, Google Chrome 157, Node 24.19.

---

## 1. O que é o motor de carrosséis

É a parte do sistema que transforma um tema da base científica em um **carrossel pronto para o Instagram** (9 slides de 1080×1350, exportados em alta, 2160×2700), na identidade azul da SOUTO TREINADOR.

Você conversa com o Claude (`/carrossel volume de treino`), aprova as escolhas nos pontos certos, e o sistema:

| Peça | O que faz |
|---|---|
| **Ficha** (da base científica) | a única fonte de fatos. Cada fato do carrossel aponta para uma linha da Ficha |
| **Agentes** | "assistentes especializados": um faz a pauta e as manchetes, outro escreve, outro revisa, outro cuida das imagens, outro escreve a legenda |
| **Validador** (`validar_carrossel.py` + `editorial.py`) | confere sozinho o texto: limite de caracteres, número × Ficha, verbo × certeza, ética do CONFEF, nutrição fora da competência, linguagem leiga, vícios de texto de IA |
| **Gerador** (`render_carrossel.py`) | desenha cada slide em HTML (editável) e fotografa em PNG pelo Google Chrome, conferindo a diagramação (texto sobreposto, cortado, colado na borda…) |
| **Editor visual** | uma página no navegador para ajustar à mão qualquer elemento do slide antes de exportar |
| **Imagens** | fotos realistas geradas no Gemini/Google Flow (navegador) ou no Higgsfield (pelo Claude), ou tiradas de bancos grátis (Pixabay, Pexels) |

**5 formatos visuais** (o mesmo texto pode sair em qualquer um):

| Formato | Cara | Teste pronto (para ver) |
|---|---|---|
| **M1 Mangá Dark** | slides escuros e claros, pessoa recortada, destaques em degradê azul, CTA dividido | `03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo1\` |
| **M2 Editorial Clean** | fundo claro quadriculado, título serifado em degradê azul, números #01 esbatidos | `…\_testes\_teste-modelo2\` |
| **M3 Dossiê** | manchetes grandes condensadas, fotos emolduradas, fundos azul/noite/branco | `…\_testes\_teste-modelo3\` |
| **M4 Cinema** | storytelling escuro, barra de busca, janela, vidro fosco | `…\_testes\_teste-modelo4\` |
| **M5 BrandsDecoded** | alternado escuro/claro, título em caixa-alta, barra da marca e barra de progresso | `…\_testes\_teste-modelo5\` |

Cada pasta de teste tem os PNGs (`slide-01.png`…) e a folha de contato (`folha.jpg`). A folha dos modelos 1, 3 e 4 juntos está em `…\_testes\_folha-modelos-1-3-4.jpg`. **O texto dos testes é fictício** (a Ficha "TESTE Volume de treino" é inventada para testar o motor) e os quadros cinza "ARTE DO TEMA" são o lugar das fotos: nunca publique os testes.

---

## 2. Onde fica cada coisa

```
03 - CARROSSÉIS E ARTE/
├─ CLAUDE.md                                 manual da frente (para a IA)
├─ Abrir editor de carrossel.bat             dois cliques = editor visual no navegador
├─ requirements.txt                          pacotes Python do gerador
├─ Referências/Método BrandsDecoded/
│  └─ Método de texto - carrossel.md         as regras de escrita (resumo próprio)
├─ Gerador/
│  ├─ marca.json                             CORES, LOGO, @ e CREF  ← o único lugar para trocar a marca
│  ├─ logo.png                               logo branca transparente
│  ├─ render_carrossel.py                    gera HTML + PNG + alertas (M1 e todos os outros)
│  ├─ modelo_editorial.py · modelo_dossie.py · modelo_cinema.py · modelo_brandsdecoded.py   M2 · M3 · M4 · M5
│  ├─ validar_carrossel.py · editorial.py    validador do texto
│  ├─ editor.py · editor.html                editor visual
│  ├─ folha.py                               folha de contato (todos os slides numa imagem)
│  ├─ conferir_recortes.py                   prévia dos recortes antes do render
│  ├─ comum.py                               recorte de fundo e posicionamento
│  └─ _marcadores/                           quadros cinza usados quando falta a foto
└─ Carrosséis/
   ├─ AAAA-MM-DD - tema/                     um carrossel por pasta (criada pelo /carrossel)
   └─ _testes/                               os testes dos 5 formatos

.claude/skills/carrossel/SKILL.md            o comando /carrossel
.claude/agents/03-carrosseis/                chefe-de-pauta · redator-de-carrossel · editor-de-texto · diretor-de-arte · revisor-de-diagramacao
.claude/agents/05-publicacao/legendista.md   a legenda
.claude/hooks/validar_peca.py                hook (roteiro, carrossel e vídeo) — vem da frente de roteiros
.env (na raiz)                               chaves do Pixabay e do Pexels (nunca sobe para o GitHub)
```

Dentro de cada carrossel pronto:
```
Carrosséis/2026-11-20 - volume de treino/
├─ carrossel.json      o texto de cada slide (o que a IA escreve e o validador confere)
├─ carrossel.md        o "relatório": tipo, headline, texto aprovado, QA, fontes, legenda
├─ prompts_arte.md     os pedidos de imagem
├─ artes/              as fotos (slide-01.png, slide-02.png…)
├─ html/               cada slide em HTML (o editor visual abre daqui)
├─ slide-01.png …      os slides prontos para postar (2160×2700)
└─ folha.jpg           todos os slides numa imagem só, para conferir
```

---

## 3. Pré-requisitos

| O quê | Para quê | Como conferir |
|---|---|---|
| **Python 3.12** (testado 3.12.10) | rodar o gerador e o validador | `python --version` |
| **Pillow 12.3.0, numpy 2.5.3, scipy 1.18.1** | imagens, recortes de fundo, folha de contato | `python -m pip show pillow numpy scipy` |
| **Google Chrome** (testado 157) | o gerador "fotografa" os slides com o Chrome, sem abrir janela | abra o Chrome; ou `Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"` |
| **Node.js 24** (testado 24.19) | só para buscar fotos no banco (Pixabay/Pexels) pelo motor de vídeo | `node --version` |
| **Claude Code** aberto na pasta `souto-treinador` | conduzir o `/carrossel` | — |
| **Pelo menos uma Ficha** na base (Guia 01) | o carrossel só afirma o que a Ficha sustenta | `01 - BASE CIENTÍFICA\00 - ÍNDICE.md` |
| **Conta no Google** (Gemini/Flow) e/ou **conta paga no Higgsfield** | gerar as fotos | seção 8 |
| **Extensão "Claude in Chrome"** (Guia 00, seção 7) | para o Claude operar o Gemini/Flow no seu Chrome | ícone do Claude na barra do Chrome |

> O Microsoft Edge **não** serve como substituto do Chrome: no teste de 2026-11-19 ele não gerou os PNGs em modo invisível. Instale o Chrome.

---

## 4. Instalação (uma vez só, 5 minutos)

Abra o **PowerShell** (tecla Windows → digite "PowerShell" → Enter) e vá para a pasta do repositório. Exemplo, se você clonou em Documentos:

```powershell
cd "$env:USERPROFILE\Documents\souto-treinador"
```

> Se o seu Windows estiver em português, a pasta pode aparecer como "Documentos", mas o caminho real continua `Documents`. Se der erro, abra a pasta no Explorador de Arquivos, clique na barra de endereço, copie o caminho e cole depois do `cd` entre aspas.

**4.1 Instalar os pacotes Python** (versões exatas, testadas):
```powershell
python -m pip install -r "03 - CARROSSÉIS E ARTE\requirements.txt"
```
Esperado no fim: `Successfully installed …` ou `Requirement already satisfied …`.

**4.2 Conferir o Chrome:**
```powershell
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```
Esperado: `True`. Se der `False`, instale em https://www.google.com/chrome/ . Se o Chrome estiver em outro lugar (ex.: instalado só para o seu usuário), o gerador também procura em `%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe`. Em último caso, aponte o caminho (vale só para a janela aberta do PowerShell):
```powershell
$env:CHROME = "C:\caminho\para\chrome.exe"
```

**4.3 (Opcional) Pacotes do motor de vídeo**, só se for usar o banco de fotos (seção 8.3): siga o Guia 04 (`npm install` em `04 - EDIÇÃO DE VÍDEO\motor`).

**4.4 Trocar o @ e o CREF (obrigatório antes de publicar).** Abra a marca no Bloco de Notas:
```powershell
notepad "03 - CARROSSÉIS E ARTE\Gerador\marca.json"
```
Troque só os dois valores marcados no campo `"_TROCAR"`:
```json
 "nome": "@soutotreinador",          ← o @ real do Instagram do Jorge
 "registro": "CREF 000000-G/UF",     ← o CREF real, no formato "CREF 012345-G/SP"
```
Salve (Ctrl+S). Mantenha as aspas e as vírgulas. Enquanto estiverem provisórios, o gerador avisa em toda geração: `LEMBRETE: o @ ("nome") e o CREF ("registro") no Gerador/marca.json ainda são provisórios (TROCAR antes de publicar).`

---

## 5. Teste rápido (2 minutos): o motor funciona?

Na raiz do repositório, no PowerShell:

```powershell
[Console]::OutputEncoding = [Text.Encoding]::UTF8
python "03 - CARROSSÉIS E ARTE\Gerador\validar_carrossel.py" "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo5.json"
```
Esperado:
```
validar_carrossel · _testes/_teste-modelo5.json · TESTE Volume de treino - Ficha
0 erro(s), 0 aviso(s) · 9 slides · refs: #1, #2, #3
```

Agora o desenho (leva ~1 a 2 minutos para 9 slides):
```powershell
python "03 - CARROSSÉIS E ARTE\Gerador\render_carrossel.py" "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo5.json"
python "03 - CARROSSÉIS E ARTE\Gerador\folha.py" "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo5"
```
Esperado: nove linhas `OK …slide-0N.png`, depois `0 alerta(s). Layout aprovado na verificação automática — ainda confira a olho.` e o caminho da `folha.jpg`. Abra a folha (dois cliques no arquivo) e confira: fundos azuis e pretos, logo SOUTO TREINADOR, quadros cinza no lugar das fotos.

Resultado dos testes em 2026-11-19 (todos com **0 ERRO, 0 AVISO no validador e 0 ALERTA no render**):

| Teste | Slides | Validador | Render |
|---|---|---|---|
| `_teste-modelo1.json` (M1) | 5 | 0 erro · 0 aviso | 0 alerta |
| `_teste-modelo2.json` (M2) | 9 | 0 erro · 0 aviso | 0 alerta |
| `_teste-modelo3.json` (M3) | 5 | 0 erro · 0 aviso | 0 alerta |
| `_teste-modelo4.json` (M4) | 5 | 0 erro · 0 aviso | 0 alerta |
| `_teste-modelo5.json` (M5) | 9 | 0 erro · 0 aviso | 0 alerta · 0 aviso |

---

## 6. Fazer um carrossel: `/carrossel`, passo a passo

O fluxo tem **paradas de aprovação** (⏸): o Claude espera a sua resposta antes de seguir. Você pode responder curto ("ok", "2", "M5").

### Passo 1 — Pedir
No Claude Code:
```
/carrossel volume de treino
```
Ou, já com o formato (economiza uma volta):
```
/carrossel volume de treino, M5, 9 slides
```
Também dá para partir de um conteúdo existente: "transforma o roteiro de ontem em carrossel", ou cole o link/texto. Conteúdo de terceiros é só matéria-prima: os fatos têm de estar na Ficha.

> **Sem Ficha do tema, o sistema para** e oferece `/montar-condicao <tema>` (Guia 01). Isso é de propósito: sem Ficha, não há fato para afirmar.

### Passo 2 — Triagem e TIPO (⏸)
O agente `chefe-de-pauta` lê a Ficha e devolve um bloco assim:
```
**Triagem:** o cansaço da academia não mede o crescimento do músculo
| Campo | Extrato |
| Transformação | … |
| Fricção central | … |
| Ângulo dominante | … |
**Eixo:** Cultura · **Funil:** Meio
**Evidências:** A) … [#1] · B) … [#2] · C) … [#M1]
**Tipo recomendado:** Mito × evidência (`tese-mito`) — …
**Alternativa:** Tese (`tese`) — …
**CTA:** consultoria — "Quer um treino para a sua rotina? …"
Confirma o tipo? (ok, ou 1 Tendência · 2 Tese [2b Mito × evidência] · 3 Case · 4 Previsão)
```
**Você responde:** `ok` (ou o número de outro tipo).

Os 4 tipos, em uma linha cada:
- **Tendência** — algo mudando agora, com data (estudo novo, moda nova).
- **Tese** — uma crença comum que a ciência contradiz ("treino bom é treino até a falha").
  - **2b Mito × evidência** — quando alguém **vende** a crença (suplemento que "seca", aparelho milagroso).
- **Case** — uma história real e verificável (atleta, pessoa pública), com link.
- **Previsão** — só há sinais apontando para algum lado ("o que ainda não se sabe sobre…").

### Passo 3 — FORMATO e nº de slides (⏸)
Escolha **M1 a M5** (veja os testes) e o nº de slides (**9** é o padrão; 5, 7 ou 12 também valem). No M1, o Claude pergunta também o estilo da capa: 1 fundo preto · 2 fundo branco · 3 quadriculado · 4 fundo desfocado.

### Passo 4 — Headlines (⏸)
Vêm **10 manchetes** numa tabela (1–5 com dois-pontos; 6–10 em 3 frases) e a **versão de capa** das 3 melhores, já no tamanho do formato. **Você responde:** o número (`3`), ou pede ajuste: `a 3 mais provocativa`, `mistura a 2 com a 7`, `refazer headlines`.

### Passo 5 — Texto e validação (automático)
O `redator-de-carrossel` escreve o texto de cada slide no `carrossel.json`; o validador confere; o `editor-de-texto` dá nota de 0 a 10 em 7 critérios por slide e reescreve o que ficou abaixo de 8. Você não precisa fazer nada aqui.

### Passo 6 — Aprovação do texto (⏸, nunca é pulada)
Você recebe o **TEXTO FINAL** slide por slide. Leia em voz alta. Peça ajustes à vontade ("no slide 4, mais curto", "troca o título do 8"). **Quando estiver bom, digite:** `aprovado`.

### Passo 7 — Imagens (⏸ créditos)
1. O Claude pergunta, slide a slide, como quer a foto (inteira com cenário, ou pessoa/objeto recortado sobre fundo branco, preto, quadriculado ou desfocado) e recomenda uma opção.
2. O `diretor-de-arte` escreve os pedidos de imagem (`prompts_arte.md`) e diz por qual rota cada um sai: **banco** (grátis), **Gemini/Flow** ou **Higgsfield**.
3. O Claude mostra quantas imagens e variações vão ser geradas e **espera o seu ok** antes de gastar créditos.
4. As imagens são geradas, conferidas (mãos, rostos, equipamento deformado, resolução) e salvas em `artes/`.
Detalhes de cada rota na seção 8.

### Passo 8 — Render e conferência
O Claude gera os PNGs, monta a `folha.jpg` e confere. Só entrega com **0 ALERTA**. Você recebe os slides prontos.

### Passo 9 — Ajuste fino no editor visual (opcional)
Seção 9.

### Passo 10 — Fechamento
O Claude monta as **Fontes** por script (nunca à mão), o `legendista` escreve a **legenda** (gancho, contexto, análise, fontes, CTA, 5 a 12 hashtags) e tudo fica no `carrossel.md` da pasta. **Você publica** no Instagram (o sistema nunca publica sozinho).

### Comandos úteis no meio do fluxo
`refazer headlines` · `ajusta a 3` · `aprovado` · `trocar slide 4` · `trocar imagem da capa` · `usar Higgsfield` / `usar Gemini` · `reiniciar`.

---

## 7. O que o validador cobra (e por quê)

**ERRO (bloqueia — o texto não segue até corrigir):**
- **Ética do profissional de Educação Física (Código de Ética do CONFEF) + regras da marca:** foto/texto de "antes e depois", depoimento ou resultado de aluno ("meus alunos perderam…"), preço ou promoção, promessa de resultado no corpo do leitor ("perca 5 kg em 30 dias", "ganhe 3 kg de músculo"), "resultado garantido".
- **Nutrição fora da competência:** mandar o leitor seguir dieta, cardápio, calorias ou tomar suplemento com dose ("tome 5 g de creatina", "dieta de 1800 kcal", "monte sua dieta") — isso é atividade do nutricionista (Lei 8.234/1991).
- **Remédio e hormônio:** "pare o remédio", "use testosterona" — assunto do médico.
- **Evidência:** número que não está na linha da Ficha; verbo mais forte que a certeza ("aumenta" quando a Ficha diz "provavelmente"); id que não existe na Ficha.
- **Palavras proibidas:** cura, milagre, garantido, segredo, nunca mais, 100%, sem esforço.
- **Vícios de texto de IA:** "não é X, é Y", "Menos X. Mais Y.", "e isso muda tudo", "estudos mostram", "5x", "neste carrossel", "arraste para o lado", "espero que tenha gostado"…
- **Tamanho:** campo com mais caracteres que o formato aguenta.

**AVISO (o Claude confere e corrige quando faz sentido):**
- Slide que fala de dieta, proteína, caloria ou suplemento **sem a linha da Ficha** — nutrição só como educação geral, com fonte.
- "Coma mais proteína", "tome creatina" (ordem sem dose) — soa como prescrição.
- "Faça 4 séries de 12" — em conteúdo aberto, o certo é a faixa da evidência ("de 10 a 20 séries por semana, segundo a revisão") e lembrar que a dose é individual.
- "Exercício que seca a barriga" — a ciência não mostra queima localizada.
- "Você" fora do slide de aplicação e do CTA; siglas (RM, RIR, RPE, VO2, HIIT), termos técnicos e %; tom de coach ("sem desculpas", "você precisa"); CTA de consultoria sem o CREF (M1–M4).

Para citar um mito sem levar erro, ponha entre aspas: `Dizem que "treino em jejum queima mais gordura".`

---

## 8. Imagens: as três rotas

Estilo da casa: **foto realista**, com cara de revista, sóbria, um ponto de foco, sem texto ou marca na imagem, sem pessoa famosa ou reconhecível, **sem corpo de "antes e depois"**, com técnica de treino correta e segura. Nada de desenho, anime ou 3D. A paleta azul é obrigatória só nos elementos gráficos (o gerador cuida); a foto pode ter outras cores.

Regras práticas:
- **Recorte** (pessoa ou objeto que "entra" no slide): peça a imagem em **fundo branco puro**, sem sombra no chão e sem degradê. Prefira roupa e objeto de cor média ou escura (garrafa transparente, água e roupa branca somem no recorte).
- **Foto inteira**: deixe espaço vazio onde vai o texto (o pedido já diz onde).
- **Nenhuma foto se repete** no mesmo carrossel.
- Nome dos arquivos: `artes/slide-01.png`, `artes/slide-02.png`… (o pedido de imagem já traz o nome certo).

### 8.1 Rota A — Gemini / Google Flow no navegador (padrão)
É o mesmo jeito que funciona hoje: o Claude opera o seu Chrome pela extensão **Claude in Chrome**.
1. Deixe o **Chrome aberto e visível** (minimizado ou coberto, ele não consegue ver nem baixar).
2. Esteja logado na sua conta Google em **Google Flow** (https://flow.google.com) ou no **Gemini** (https://gemini.google.com).
3. No `/carrossel`, na etapa das imagens, diga `usar Gemini` (é o padrão).
4. O Claude abre um projeto, escolhe o modelo de imagem, a proporção e o número de variações, cola o pedido e gera **no máximo 1 ou 2 por vez, com pausa** — disparar muitas em sequência pode fazer o Google bloquear por "atividade incomum".
5. Se aparecer uma verificação ("não sou um robô"), o Claude **para e chama você**: resolva você mesmo e mande seguir.
6. As escolhidas são baixadas em alta (2K quando houver) e salvas em `artes/`.
> Os planos e limites do Gemini/Flow mudam com frequência; confira na tela "A geração vai usar N créditos" antes de aprovar.

### 8.2 Rota B — Higgsfield pelo MCP (dentro do Claude)
O Higgsfield tem um **conector oficial (MCP)**: o Claude gera as imagens direto na sua conta Higgsfield, sem abrir o navegador.

**O que você precisa:** uma **assinatura paga** do Higgsfield (https://higgsfield.ai). Toda geração pelo conector **gasta créditos**, mesmo em planos com geração "ilimitada" no site (o ilimitado vale só no site). Não precisa de chave de API.

**Ligar no app Claude (claude.ai no navegador ou Claude Desktop)** — passo a passo oficial do Higgsfield:
1. Abra **Configurações → Conectores** (Settings → Connectors).
2. Clique em **Adicionar conector personalizado** (Add custom connector).
3. Nome: `Higgsfield`. URL do servidor MCP: `https://mcp.higgsfield.ai/mcp`
4. Clique em **Conectar** (Connect). Abre a janela de login do Higgsfield: entre na sua conta e autorize (se já estiver logado no site, é automático).
5. Volte ao Claude: o Higgsfield aparece na lista de conectores ativos.

**Ligar no Claude Code** (onde roda o `/carrossel`) — escolha um caminho:
- **Caminho 1 (MCP, recomendado):** no PowerShell, na pasta do repositório:
  ```powershell
  claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp
  ```
  Depois, dentro do Claude Code, digite `/mcp` → `higgsfield` → **Authenticate** e faça o login no navegador que abrir.
  > ⚠ **A VERIFICAR:** este comando é a sintaxe padrão do Claude Code para servidores MCP remotos e aparece em guias de terceiros, mas **não** está na página oficial do Higgsfield (2026-11-19). Se não funcionar, use o Caminho 2. Se você estiver logado no Claude Code com a mesma conta do claude.ai, o conector criado no app também pode aparecer sozinho no `/mcp` (confira).
- **Caminho 2 (oficial do Higgsfield para agentes de terminal):** a CLI do Higgsfield.
  ```powershell
  npm i -g @higgsfield/cli
  higgsfield auth login
  npx skills add higgsfield-ai/skills
  ```
  (o segundo comando abre o navegador para o login). Depois o Claude usa a CLI para gerar.

**Usar no `/carrossel`:** na etapa das imagens, diga `usar Higgsfield`. O Claude confere o saldo de créditos, mostra a conta (quantas imagens × variações) e espera o seu ok. As imagens ficam também na sua biblioteca (Assets) do Higgsfield.

**Personagem recorrente:** o Higgsfield permite treinar um personagem (Soul) a partir de fotos para manter o mesmo rosto em vários slides. Use só com pessoa fictícia ou com **fotos suas**, com a sua autorização.

> Fontes consultadas em 2026-11-19: "What is Higgsfield MCP?" e "How do I connect Higgsfield to Claude, ChatGPT, or another AI agent?" no Creator Hub do Higgsfield (https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp e https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent). Os nomes exatos das ferramentas e dos modelos do conector podem mudar: o Claude lê a lista na hora.

### 8.3 Rota C — Banco de imagens grátis (Pixabay e Pexels)
Bom para **fundo, textura e cena inteira** (academia vazia, anilhas, corda, pista). Quase nunca tem objeto isolado em fundo branco: para recorte, use as rotas A ou B. O sistema usa o script do motor de vídeo (`04 - EDIÇÃO DE VÍDEO\motor\scripts\stock.mjs`), que precisa do **Node.js** e do `npm install` do motor (Guia 04). Sem chave, ele ainda busca no Openverse/Wikimedia.

**Chave do Pixabay (grátis):**
1. Crie uma conta em https://pixabay.com (botão **Join** / Cadastrar) e confirme o e-mail.
2. Logado, abra https://pixabay.com/api/docs/
3. Na seção **Parameters**, na linha do parâmetro `key`, aparece a **sua chave** (uma sequência de números e letras). Copie.
4. Limite: 100 buscas por minuto. As imagens têm de ser baixadas (não usar o link direto do Pixabay) e a origem deve ser mostrada.

**Chave do Pexels (grátis):**
1. Crie uma conta em https://www.pexels.com (Join) e confirme o e-mail.
2. Abra https://www.pexels.com/api/ e clique em **Get Started** / **Your API Key**.
3. Preencha o formulário curto (nome do projeto, ex.: "Conteúdo SOUTO TREINADOR"; uso: conteúdo próprio de redes sociais) e aceite os termos. A chave aparece na hora. Copie.
4. Limite: 200 buscas por hora / 20 mil por mês. O Pexels pede crédito ao fotógrafo ("Foto de Fulano no Pexels") sempre que possível.

**Onde colocar as chaves** — no arquivo `.env` da **raiz** do repositório:
1. Se ainda não existe, crie a partir do modelo:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Abra:
   ```powershell
   notepad .env
   ```
3. Cole cada chave depois do `=`, sem espaço e sem aspas:
   ```
   PIXABAY_API_KEY=cole-aqui-a-chave-do-pixabay
   PEXELS_API_KEY=cole-aqui-a-chave-do-pexels
   ```
   (troque o texto depois do `=` pela chave copiada). Salve.
4. **Nunca** mande uma chave pelo chat do Claude, WhatsApp ou e-mail. O `.env` não sobe para o GitHub (está no `.gitignore`); só o `.env.example`, sem as chaves, sobe.

Teste (busca 4 fotos de "empty gym" para uma pasta de rascunho):
```powershell
node "04 - EDIÇÃO DE VÍDEO\motor\scripts\stock.mjs" "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_banco" teste "empty gym dark" --image --n 4
```
As fotos saem em `…\_banco\04_broll\fotos\` e os créditos em `…\_banco\04_broll\creditos.json`. Apague a pasta `_banco` depois do teste.

### 8.4 Quando nenhuma rota funcionar
Peça: `me passa os prompts`. O Claude entrega o `prompts_arte.md`; você gera onde quiser e salva as imagens em `artes/` com os nomes da tabela (`slide-01.png`…). Depois diga `as artes estão na pasta`.

---

## 9. Editor visual (ajuste fino)

1. Dê **dois cliques** em `03 - CARROSSÉIS E ARTE\Abrir editor de carrossel.bat`. Abre uma janela preta (deixe aberta) e o navegador em http://localhost:8765/editor
   - Pelo PowerShell: `python "03 - CARROSSÉIS E ARTE\Gerador\editor.py" --abrir`
2. Escolha o carrossel na lista e o slide.
3. **Clique** num elemento para selecionar (Alt+clique pega o de baixo); **arraste** para mover (aparecem guias); use as **alças** para mudar o tamanho; **duplo clique** edita o texto (negrito, itálico, destaque).
4. No painel lateral: fonte, cor, alinhamento, entrelinha, opacidade, camadas, trocar/enquadrar/zoom da foto e "Recortar fundo".
5. **Salvar** grava o slide; **Gerar PNG** fotografa com o mesmo Chrome e mostra os ALERTAS; **Baixar PNG** ou **Baixar todos (.zip)**.
6. Para desligar, feche a janela preta.

Importante:
- Slide salvo no editor **não é sobrescrito** pelo gerador depois (só com `--refazer`).
- **Mudança de conteúdo** (um número, uma afirmação) deve ir pelo Claude, no `carrossel.json`, para passar pelo validador. O editor é para ajuste visual.
- O editor só funciona no seu computador (não fica acessível na internet).

---

## 10. Comandos à mão (para quem quiser)

Todos na raiz do repositório, no PowerShell. Troque `<pasta>` pela pasta do carrossel.

| Para… | Comando |
|---|---|
| validar o texto | `python "03 - CARROSSÉIS E ARTE\Gerador\validar_carrossel.py" "<pasta>\carrossel.json"` |
| montar Fontes e Nível de certeza no `carrossel.md` | o mesmo, com `--montar-fontes` no fim |
| conferir os recortes antes do render | `python "03 - CARROSSÉIS E ARTE\Gerador\conferir_recortes.py" "<pasta>\carrossel.json"` |
| gerar os slides | `python "03 - CARROSSÉIS E ARTE\Gerador\render_carrossel.py" "<pasta>\carrossel.json"` |
| gerar só os slides 4 e 6 | o mesmo, com `--slides=4,6` |
| ver a zona onde a foto entra | o mesmo, com `--guias` (nunca publique com guias) |
| regerar slides salvos no editor | o mesmo, com `--refazer` |
| folha de contato | `python "03 - CARROSSÉIS E ARTE\Gerador\folha.py" "<pasta>"` |

---

## 11. Hook: o validador rodando sozinho

O hook `.claude\hooks\validar_peca.py` (da frente de roteiros) também valida os carrosséis: toda vez que a IA salva um `Carrosséis\…\carrossel.json`, o validador roda e, se tiver ERRO, a IA é obrigada a corrigir. O registro é **o mesmo do Guia 02, seção 9** — se já fez lá, não precisa fazer de novo. Se ainda não fez, o `.claude\settings.json` da raiz precisa ter:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/validar_peca.py\"",
            "timeout": 120,
            "statusMessage": "Validando roteiro/carrossel/edição contra a ficha"
          }
        ]
      }
    ]
  }
}
```
Testar à mão (o hook só olha arquivos chamados `carrossel.json` dentro de `Carrosséis\`; por isso o teste copia um JSON de teste para uma pasta temporária):
```powershell
New-Item -ItemType Directory -Force "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_hook" | Out-Null
Copy-Item "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo5.json" "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_hook\carrossel.json"
'{"tool_input":{"file_path":"03 - CARROSSÉIS E ARTE/Carrosséis/_testes/_hook/carrossel.json"}}' | python ".claude\hooks\validar_peca.py"
Remove-Item -Recurse "03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_hook"
```
Esperado (testado em 2026-11-19): uma linha com `"additionalContext": "validar_carrossel: 0 erro(s), 0 aviso(s) · 9 slides · refs: #1, #2, #3"`. Sem hook, tudo funciona igual; o Claude roda o validador à mão.

---

## 12. Problemas comuns (FAQ)

**1. `Chrome não encontrado. Instale o Google Chrome…`**
Instale o Chrome (https://www.google.com/chrome/). Se ele estiver num lugar diferente, rode antes `$env:CHROME = "C:\caminho\chrome.exe"` na mesma janela do PowerShell.

**2. `ModuleNotFoundError: No module named 'PIL'` (ou `numpy`, `scipy`).**
Faltou a instalação: `python -m pip install -r "03 - CARROSSÉIS E ARTE\requirements.txt"`.

**3. `'python' não é reconhecido como um comando…`**
O Python não está no PATH. Tente `py -3` no lugar de `python`. Se não der, reinstale o Python marcando **"Add python.exe to PATH"** (Guia 00, seção 3.2). O `.bat` do editor já tenta `py` sozinho.

**4. `validar_carrossel: falta o módulo de evidência …validar_roteiro.py`.**
O validador do carrossel usa o conferidor de Ficha da frente de roteiros (`02 - ROTEIROS\_SISTEMA\validar_roteiro.py`). Baixe o repositório inteiro (`git pull`), não só a pasta 03.

**5. `ficha 'X - Ficha' não encontrada em 01 - BASE CIENTÍFICA`.**
O nome no `"ficha"` do JSON precisa bater com o arquivo `<Tema> - Ficha.md`. Confira no `00 - ÍNDICE.md`. Se a Ficha não existe, rode `/montar-condicao <tema>`.

**6. `FALHOU …slide-03.png` / `o PNG não saiu (o Chrome travou ou demorou demais)`.**
Normalmente é internet lenta para baixar as fontes (Google Fonts) ou o computador sem memória. Feche programas pesados e rode de novo só esse slide: `--slides=3`.

**7. Os slides saíram com letra "padrão" (sem as fontes bonitas).**
As fontes vêm do Google Fonts pela internet. Sem internet, o Chrome usa uma fonte genérica. Conecte e gere de novo.

**8. `ALERTA … falta a arte em 'imagem' (marcador cinza no lugar)` ou `arquivo da arte não encontrado`.**
Antes das imagens, é o esperado. Depois, confira se o arquivo está em `artes\` com o nome exato do JSON (`slide-03.png`, não `slide-3.png` nem `.jpg` se o JSON diz `.png`).

**9. `ALERTA … 'texto' com 312 caracteres (máx. 300) — sintetize` / `texto não coube na área`.**
O texto passou do que o formato aguenta. Peça ao Claude "sintetiza o slide N" — nunca diminua a fonte para caber.

**10. `ALERTA … texto sobre a arte recortada`.**
A pessoa/objeto recortado ficou em cima do texto. Peça "diminui a foto do slide N" ou troque a arte por uma com o sujeito menor ou mais para o lado.

**11. O recorte ficou com contorno branco, comeu um pedaço ou deixou fundo dentro (entre braço e corpo).**
Gere de novo com fundo branco puro e sujeito de cor média/escura. Para vãos (braço na cintura, alça), o Claude pode ligar `"recorte_buracos": true`. No editor, "Recortar fundo · traço/foto" refaz em outro modo.

**12. O validador acusou "prescrição de dieta" ou "prescrição com dose".**
O texto mandou o leitor comer/tomar algo com quantidade. Reescreva como educação, com a fonte: "a revisão de 2024 encontrou que quem consumiu X…" e encaminhe ao nutricionista. Treinador não prescreve dieta nem suplemento.

**13. O validador acusou "promessa de resultado".**
Nada de "X kg em N dias" ou "ganhe X de músculo" para o leitor. Se for o resultado de um estudo, deixe claro que é **do grupo estudado** ("os participantes ganharam…"), com a linha da Ficha.

**14. `LEMBRETE: o @ ("nome") e o CREF ("registro") … ainda são provisórios`.**
Não é erro: é para lembrar de trocar no `Gerador\marca.json` (seção 4.4). Some quando você trocar.

**15. Letras estranhas na saída do PowerShell (Ã©, â€").**
Rode antes: `[Console]::OutputEncoding = [Text.Encoding]::UTF8`.

**16. O editor não abre / "endereço já em uso".**
Já tem um editor aberto (outra janela preta). Feche-a e abra de novo, ou use outra porta: `python "03 - CARROSSÉIS E ARTE\Gerador\editor.py" --porta 8766 --abrir`.

**17. O Google bloqueou por "atividade incomum" no Flow/Gemini.**
Foram geradas muitas imagens seguidas. Espere algumas horas, gere 1 ou 2 por vez, ou use o Higgsfield. Nunca tente contornar a verificação.

**18. O Higgsfield não aparece no Claude Code (`/mcp` não lista).**
Refaça a seção 8.2 (Caminho 1) e o **Authenticate**; confira se a assinatura está ativa e se há créditos. Se não resolver, use o Caminho 2 (CLI) ou gere pelo app Claude (claude.ai) e salve as imagens em `artes\`.

**19. `Nenhum resultado (verifique a query em inglês e as chaves no .env)` no banco.**
A busca precisa ser em inglês ("empty gym", não "academia vazia"), e as chaves precisam estar no `.env` da **raiz** (seção 8.3).

**20. Mudei um texto no editor e o validador não reclamou.**
O editor não passa pelo validador. Mudança de conteúdo vai pelo Claude, no `carrossel.json`.

---

## 13. Boas práticas

- **Ficha primeiro, carrossel depois.** Sem Ficha, é opinião; com Ficha, é autoridade.
- **Capa ampla, miolo técnico:** a capa fala da vida de quem treina (cansaço, rotina, mito da academia); a fisiologia vai para os slides 3 a 5.
- **Leia o texto final em voz alta** antes de digitar `aprovado`. Se travar, peça "mais falado".
- **Nutrição com cuidado:** pode educar ("a revisão mostrou que…"), nunca prescrever. Na dúvida, encaminhe ao nutricionista no próprio texto.
- **Treino em conteúdo aberto é educação:** a faixa da evidência e o lembrete de que a dose é individual. A prescrição fica para o treino individualizado (o seu CTA).
- **Gere poucas imagens por vez** e escolha com calma; uma boa capa vale mais que nove fotos médias.
- **Fotos suas** funcionam muito bem no CTA e em bastidores — só você decide quando usar o seu rosto.
- **Olhe a folha de contato inteira** antes de postar, mesmo com 0 ALERTA.
- **Não publique os testes** (`_testes`): o texto é fictício.
- **Troque o @ e o CREF** no `marca.json` antes da primeira publicação.

---

## 14. Imagens deste guia (para o PDF)

| Figura | Arquivo |
|---|---|
| Folha de contato M5 (9 slides) | `03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo5\folha.jpg` |
| Folha de contato M2 (9 slides) | `03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_teste-modelo2\folha.jpg` |
| Folha M1 + M3 + M4 (5 slides cada) | `03 - CARROSSÉIS E ARTE\Carrosséis\_testes\_folha-modelos-1-3-4.jpg` |
| Capas dos 5 formatos | `…\_testes\_teste-modeloN\slide-01.png` (N = 1 a 5) |
| CTA com nome e CREF | `…\_teste-modelo2\slide-09.png` e `…\_teste-modelo5\slide-09.png` |
