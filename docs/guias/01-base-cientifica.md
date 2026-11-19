# Guia 01 — Base científica (passo a passo para quem não programa)

> Para: Jorge Souto (SOUTO TREINADOR) ou quem opera o sistema com ele.
> Sistema: Windows 10/11, PowerShell, Claude Code.
> Tempo da primeira instalação: 20 a 40 minutos. Depois disso, montar um tema leva de 15 minutos a 1 hora (a maior parte é você escolhendo fontes e baixando PDFs).

---

## 1. O que é a base científica (e por que ela existe)

A base científica é a **memória de evidência** do perfil. Todo número, todo "a ciência mostra", todo mito desmentido que aparece num Reels, carrossel ou legenda **sai daqui** — nunca da memória da IA e nunca de "vi num vídeo".

Ela tem três camadas:

| Camada | O que é | Quem lê |
|---|---|---|
| **PDFs e catálogo** (`_MÁQUINA/`) | os artigos (PDF), o texto extraído e uma "ficha automática" em JSON de cada artigo (referência, tipo de estudo, achados com página) | só os scripts e os agentes |
| **Protocolo** (`<Tema> - Protocolo.md`) | síntese técnica para o Jorge: o que os posicionamentos e as meta-análises dizem sobre conduta (volume, carga, progressão…) | o Jorge |
| **Ficha** (`<Tema> - Ficha.md`) | frases prontas, em linguagem leiga, **com o verbo do tamanho da certeza**, número absoluto e fonte. É o que o roteiro e o carrossel citam (`[#3]`) | os agentes de conteúdo e o validador |

O fluxo inteiro em uma linha:

```
PDF em ENTRADA/  →  catalogar  →  /montar-condicao <tema>  →  Ficha pronta  →  /roteiro e /carrossel citam a Ficha
```

**Por que tanta regra?** Porque o perfil vai crescer apoiado em confiança. Uma afirmação exagerada ("treino X dobra o ganho de músculo") destrói a credibilidade e pode ferir a ética profissional. O sistema deixa o exagero **impossível de passar**: o validador recusa verbo mais forte que a evidência e número que não está na Ficha.

---

## 2. Onde fica cada coisa

```
souto-treinador/                         (a raiz do repositório)
├─ 01 - BASE CIENTÍFICA/
│  ├─ CLAUDE.md                          manual da frente (para a IA)
│  ├─ 00 - ÍNDICE.md                     gerado por script: o que existe na base (não edite)
│  ├─ ENTRADA/                           VOCÊ solta os PDFs aqui
│  ├─ <Área>/<Tema> - Ficha.md           Fichas (e Protocolos) por área
│  └─ _MÁQUINA/                          a "casa de máquinas" (não precisa abrir)
│     ├─ scripts/  biblioteca.py · edison.py · gerar_indice.py
│     ├─ modelos/  Ficha.md · Protocolo.md
│     ├─ pdf/  artigos/  texto/  edison/ ...   (gerados pelos scripts)
├─ .claude/skills/montar-condicao/       o comando /montar-condicao
└─ .claude/agents/01-base/               fichador · pesquisador-de-evidencia
```

---

## 3. Pré-requisitos (instalar uma vez)

### 3.1 Python 3.12
Os scripts são em Python e usam **só a biblioteca padrão** (não precisa instalar pacote nenhum com `pip`).

1. Abra o **PowerShell** (tecla Windows → digite "PowerShell" → Enter).
2. Instale pelo winget (vem no Windows 11):
   ```powershell
   winget install -e --id Python.Python.3.12
   ```
   Ou baixe em https://www.python.org/downloads/ e, **na primeira tela do instalador, marque "Add python.exe to PATH"**.
3. **Feche e abra o PowerShell de novo** e confira:
   ```powershell
   python --version
   ```
   Deve aparecer `Python 3.12.x`. Se aparecer "Python não encontrado" ou abrir a Microsoft Store, veja o FAQ (item 1).

### 3.2 pdftotext (o "leitor de PDF" dos scripts)
O `biblioteca.py` extrai o texto dos PDFs com o programa `pdftotext`. Ele procura em dois lugares (função `pdftotext_bin()`):
1. em qualquer pasta do PATH do Windows;
2. em `C:\Program Files\Git\mingw64\bin\pdftotext.exe` — **que já vem com o Git for Windows**.

**Caminho mais fácil: instalar o Git for Windows** (você vai precisar dele de qualquer jeito para baixar o repositório do GitHub):
```powershell
winget install -e --id Git.Git
```
Feche e abra o PowerShell e confira:
```powershell
& "C:\Program Files\Git\mingw64\bin\pdftotext.exe" -v
```
Deve aparecer algo como `pdftotext version 4.x`.

**Alternativa (sem Git): Poppler para Windows.**
1. Baixe o `.zip` mais recente em https://github.com/oschwartz10612/poppler-windows/releases
2. Extraia, por exemplo, em `C:\poppler`.
3. Ponha `C:\poppler\Library\bin` no PATH: tecla Windows → "variáveis de ambiente" → **Editar as variáveis de ambiente do sistema** → **Variáveis de Ambiente…** → em "Variáveis de usuário", selecione `Path` → **Editar** → **Novo** → cole `C:\poppler\Library\bin` → OK, OK, OK.
4. Feche e abra o PowerShell: `pdftotext -v`.

### 3.3 Claude Code
O sistema roda dentro do Claude Code aberto **na raiz do repositório** (a pasta `souto-treinador`). É ali que os comandos `/montar-condicao` e `/roteiro` aparecem.

### 3.4 Chave da Edison Scientific (opcional, mas recomendada)
A **Edison Scientific** (antiga FutureHouse) é uma IA que lê a literatura científica e devolve artigos candidatos. O sistema usa ela como **primeiro passo da busca**. Sem chave, tudo funciona, só que a busca fica limitada ao catálogo e ao Europe PMC.

**Regra de ouro: a chave NUNCA vai no chat nem no repositório.** O repositório é público no GitHub; uma chave lá vira chave de qualquer pessoa. Ela fica num arquivo fora do repositório: `%USERPROFILE%\.edison-key` (a pasta do seu usuário do Windows, `C:\Users\<seu-usuário>\.edison-key`). O script nunca imprime a chave.

Passo a passo:
1. Crie uma conta na plataforma da Edison Scientific (platform.edisonscientific.com) e gere uma **API key** na área da sua conta. (A tela da plataforma pode mudar; procure por "API key" ou "API".)
2. No PowerShell, na raiz do repositório:
   ```powershell
   python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\edison.py" chave --abrir
   ```
   O script cria o arquivo `.edison-key` vazio na sua pasta de usuário e abre o **Bloco de Notas**.
3. **Cole a chave** no Bloco de Notas (só a chave, numa linha), aperte **Ctrl+S** e feche.
4. Teste:
   ```powershell
   python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\edison.py" chave --testar
   ```
   Esperado: `Chave encontrada (não é mostrada).` e `Login na Edison: OK.`
5. Ajuste o plano de créditos ao seu plano real (o padrão do script é uma **estimativa**: 10 créditos/mês, Literature = 1, Literature High = 5, Precedent = 1):
   ```powershell
   python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\edison.py" plano --mes 10 --literature 1 --high 5 --precedent 1
   python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\edison.py" creditos
   ```
   O script **se recusa** a passar do limite do mês. Para passar, é preciso rodar com `--autorizado` — e o sistema só faz isso com o seu "sim".

> Alternativa avançada: a variável de ambiente `EDISON_PLATFORM_API_KEY` também funciona. Não a coloque em nenhum arquivo do repositório.

---

## 4. Primeira vez: abrir a pasta certa

Todos os comandos deste guia são rodados **a partir da raiz do repositório**. No PowerShell:
```powershell
cd "C:\caminho\para\souto-treinador"
```
(troque pelo caminho real; dica: no Explorador, clique na barra de endereço da pasta `souto-treinador`, copie e cole entre aspas).

Confira se está no lugar certo:
```powershell
dir
```
Você deve ver `01 - BASE CIENTÍFICA`, `02 - ROTEIROS`, `.claude`…

> **Aspas sempre.** Os nomes de pasta têm espaço e acento ("01 - BASE CIENTÍFICA"). Sem aspas, o PowerShell quebra o caminho no meio.

---

## 5. Colocar artigos na base

### 5.1 De onde vêm os PDFs
- **Acesso aberto:** o próprio sistema baixa (com o seu ok) pelo comando `importar-fila --baixar`.
- **Artigo pago (atrás de paywall):** precisa vir pelo **seu acesso legítimo** — Portal de Periódicos **CAPES** (pelo CAFe da sua universidade, se tiver vínculo), biblioteca da universidade, assinatura de revista, ou pedir o PDF ao autor (ResearchGate/e-mail). Baixe o PDF e solte em `01 - BASE CIENTÍFICA\ENTRADA\`. **Nunca** use site pirata.
- **Lista do que falta:** os scripts mantêm `01 - BASE CIENTÍFICA\_MÁQUINA\para-baixar.md` com link de cada fonte paga pendente. A curadoria inicial está em `01 - BASE CIENTÍFICA\Curadoria inicial - treino de força.md` (ABERTO = o script baixa; pago = você baixa).

> **Repositório público:** PDFs de artigos pagos não podem ir para o GitHub (direito autoral). Confira se o `.gitignore` da raiz exclui `ENTRADA/`, `_MÁQUINA/pdf/` e `_MÁQUINA/texto/` antes de fazer `git push`.

### 5.2 Catalogar
Com os PDFs em `ENTRADA\`:
```powershell
python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\biblioteca.py" catalogar
```
O que acontece: cada PDF é lido, vira um JSON em `_MÁQUINA\artigos\` (referência Vancouver, tipo de estudo, teto de certeza, achados com página) e é **movido** para `_MÁQUINA\pdf\`. Duplicata exata some da ENTRADA. No fim, o índice é refeito.

Conferir um artigo:
```powershell
python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\biblioteca.py" buscar "hypertrophy volume"
python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\biblioteca.py" ver "Schoenfeld 2017"
```

### 5.3 Outros comandos úteis
| Comando | Para quê |
|---|---|
| `biblioteca.py buscar "termo" --tipo meta-analise --desde 2020` | acha artigos no catálogo (tipos: `diretriz`, `meta-analise`, `revisao-sistematica`) |
| `biblioteca.py ver "<id>"` | a ficha automática de um artigo |
| `biblioteca.py trecho "<id>" "termo"` | o parágrafo do artigo onde o termo aparece, com a página |
| `biblioteca.py conferir-ficha "<Ficha.md>"` | confere os números e as fontes de uma Ficha |
| `biblioteca.py importar-fila` | mostra o plano da fila (o que dá para baixar aberto) |
| `biblioteca.py importar-fila --baixar` | baixa o que é aberto (**só com o seu ok**) |
| `biblioteca.py panorama` | resumo do catálogo |
| `gerar_indice.py` | refaz `00 - ÍNDICE.md` |

(Todos com `python "01 - BASE CIENTÍFICA\_MÁQUINA\scripts\<script>"` na frente.)

---

## 6. Montar um tema: `/montar-condicao`

No Claude Code (aberto na raiz), digite:
```
/montar-condicao volume de treino e hipertrofia
```

O que vai acontecer, etapa por etapa (⏸ = o sistema para e espera você):

1. **Tipo e área.** O sistema decide se o tema tem Protocolo + Ficha (conduta técnica) ou só Ficha (tema transversal, ex.: "mitos de academia"), e em que pasta (área) fica. Se tiver dúvida, pergunta.
2. **Busca na Edison** (se houver chave). Mostra quantos créditos vai gastar. Pode demorar mais de 2 minutos. A IA da Edison **só sugere** artigos; cada sugestão é conferida no Europe PMC — artigo marcado com ⚠ pode ter sido **inventado pela IA** e não entra.
3. **Busca no catálogo e na fila** com sinônimos em português e inglês.
4. ⏸ **Você aprova de 3 a 10 fontes.** O sistema sugere: pelo menos 1 posicionamento/diretriz (ACSM, NSCA, OMS…), a meta-análise mais recente de cada desfecho e 1 ou 2 ensaios. Também mostra o que falta baixar: aberto (ele baixa com seu ok) e pago (você baixa pelo seu acesso e solta em `ENTRADA\`).
5. **Catalogar** (script).
6. **O agente `fichador` escreve** a Ficha (e o Protocolo). Ele lê só as fichas automáticas dos artigos e trechos com página — nunca o PDF inteiro (economia).
7. **Conferência** com `conferir-ficha`: todo número de 2 ou mais dígitos precisa estar escrito no artigo citado. Tem de dar 0 erro.
8. **Índice** atualizado.
9. **Resumo para você:** links, quantas afirmações, as 3 melhores pautas, lacunas e fontes pagas pendentes.

Atualizar um tema que já existe: o mesmo comando. O sistema percebe e só **acrescenta** — nunca renumera as afirmações (roteiros antigos citam `[#n]`).

---

## 7. As regras de evidência (o coração do sistema)

### 7.1 Hierarquia das fontes
1. **Posicionamento/diretriz vigente** (ACSM, NSCA, OMS, sociedades) — o norte.
2. **Meta-análise e revisão sistemática** recentes.
3. **Ensaio clínico** (estudo com sorteio).
4. **Observacional** — mostra associação, nunca causa.
5. **Mecanismo** (fisiologia, célula, animal) — explica, não prova.

Revisão narrativa (opinião organizada de especialista) = contexto, não prova.

### 7.2 Verbo × certeza (o validador confere)
| Certeza | Como dizer | Exemplo |
|---|---|---|
| **Alta** | verbo direto | "treino de força **aumenta** a força" |
| **Moderada** | "provavelmente" | "mais séries por semana **provavelmente aumentam** o ganho de músculo" |
| **Baixa** | "pode" | "treinar perto da falha **pode ajudar**" |
| **Muito baixa** | "não se sabe se" | "**não se sabe se** treinar em jejum muda o ganho de músculo" |

- Estudo observacional: "**está associado a**", nunca "causa".
- **Efeito relativo sempre com o absoluto:** "40% a mais" sozinho engana; diga "de 4 para 10 séries", "9 em cada 10".
- O teto da certeza vem do **tipo de estudo**: um estudo único não passa de "baixa"; amostra pequena, pouco tempo ou população muito específica rebaixam um nível.
- Financiamento da indústria **não** rebaixa sozinho; rebaixa a falha concreta que se achar no estudo.

### 7.3 Sem fonte, não afirma
Se a base não tem, a resposta é "não temos isso processado" + `/montar-condicao`. Nada de memória da IA, nada de número "aproximado de cabeça".

### 7.4 Nutrição e medicina
A Ficha pode registrar o que os estudos mostram sobre alimentação e suplemento, **como informação**. Prescrever dieta, cardápio, calorias ou suplemento com dose é atividade do **nutricionista** (Lei 8.234/1991). Remédio e hormônio, do **médico**. Detalhes em `00 - MARCA E ESTRATÉGIA\Ética profissional - CONFEF.md`.

---

## 8. Perguntas frequentes e problemas comuns

**1. `python` não é reconhecido / abre a Microsoft Store.**
O Python não está no PATH, ou o Windows está usando o "atalho" da Store. Reinstale marcando **"Add python.exe to PATH"**. Depois: tecla Windows → "Gerenciar aliases de execução de aplicativo" → **desligue** "python.exe" e "python3.exe" (Instalador de Aplicativo). Feche e abra o PowerShell.

**2. `pdftotext não encontrado (vem com o Git for Windows).`**
Instale o Git for Windows (seção 3.2) ou o Poppler e ponha no PATH. Confira com `& "C:\Program Files\Git\mingw64\bin\pdftotext.exe" -v`.

**3. O catalogar diz "só na nuvem (OneDrive)".**
A pasta está no OneDrive e o PDF ainda não foi baixado para o computador. Clique com o botão direito em `01 - BASE CIENTÍFICA` → **"Sempre manter neste dispositivo"**, espere o ícone virar verde cheio e rode `catalogar` de novo.

**4. O PDF foi catalogado como "sem texto".**
É um PDF escaneado (imagem). O pdftotext não lê imagem. Procure a versão digital no site da revista ou na CAPES. Se não houver, a fonte fica de fora (ou alguém passa OCR antes).

**5. `Chave ainda vazia` na Edison.**
O arquivo `.edison-key` existe mas está vazio. Rode `edison.py chave --abrir`, cole a chave, **Ctrl+S**. Confira que não colou espaço nem aspas.

**6. `Login na Edison` falhou.**
Chave errada, expirada ou copiada pela metade. Gere outra na plataforma e cole de novo. Se a Edison estiver fora do ar, o `/montar-condicao` segue só com catálogo e Europe PMC.

**7. `PARE: passaria do plano grátis`.**
Os créditos do mês acabaram (pela conta do script). Espere o mês virar, ou ajuste o plano real com `edison.py plano --mes N`, ou autorize o gasto extra (o sistema só roda `--autorizado` depois do seu "sim").

**8. A Edison sugeriu um artigo com ⚠.**
O DOI/PMID não foi achado no Europe PMC: **pode ter sido inventado pela IA**. Não aprove. Procure o título manualmente; se não existir, descarte.

**9. O artigo que eu quero é pago e eu não tenho CAPES.**
Opções legais: biblioteca de uma universidade (muitas têm acesso no local), pedir ao autor pelo ResearchGate ou e-mail (autores costumam mandar), procurar versão aceita (preprint/author manuscript) no PubMed Central ou no repositório da universidade do autor. Sem PDF, a fonte fica de fora — nunca "de memória".

**10. `conferir-ficha` acusa "número não aparece no texto do artigo".**
O fichador escreveu um número que não está no artigo citado (ou está numa tabela que o pdftotext leu torto). O sistema devolve ao fichador para corrigir. Se insistir, confira à mão com `biblioteca.py trecho "<id>" "<número>"`.

**11. `notas_base: '…' não existe no catálogo`.**
O id na Ficha não bate com o id do catálogo. Use o id exato que o `buscar` mostra.

**12. O índice não mostra a minha Ficha nova.**
A pasta da Ficha não está na lista de áreas (`AREAS` em `_MÁQUINA\scripts\gerar_indice.py`) ou o nome não termina em ` - Ficha.md`. Rode `gerar_indice.py` de novo depois de corrigir.

**13. Erro com acento no caminho ("CIENTÃFICA", caracteres estranhos).**
Use o PowerShell (não o Prompt de Comando antigo) e sempre aspas. Se aparecerem letras estranhas na saída, rode antes: `[Console]::OutputEncoding = [Text.Encoding]::UTF8`.

**14. Posso apagar arquivos de `_MÁQUINA`?**
Não à mão. Só os scripts escrevem lá (exceções: `modelos/` e `registro.md`). Ficha, Protocolo e PDF não se apagam.

**15. A IA colou minha chave no chat / num arquivo. E agora?**
Gere uma chave nova na plataforma da Edison (revogando a antiga) e cole a nova só no `.edison-key`. Se a chave foi para o GitHub, considere-a vazada mesmo que você apague o commit.

---

## 9. Boas práticas

- **Um tema por vez.** Termine a Ficha antes de começar outra.
- **Comece pelos posicionamentos** (ACSM, NSCA, OMS): eles dão o norte e evitam Ficha baseada em estudo isolado.
- **Prefira meta-análises recentes** (últimos 5 anos) para cada desfecho.
- **Aprove poucas fontes boas** (3 a 10) em vez de muitas medianas: o custo do fichador cresce com o número de fontes.
- **Olhe as Lacunas** de cada Ficha: elas viram a lista do que buscar depois.
- **Nunca edite número na Ficha à mão** sem conferir no artigo (`trecho`).
- **Não renumere afirmações**: roteiros publicados citam `[#n]`.
- **Créditos da Edison:** confira `creditos` antes de perguntar; uma pergunta bem feita em inglês técnico rende mais que três vagas.
- **OneDrive:** mantenha a base "sempre neste dispositivo" para os scripts lerem os PDFs.
- **GitHub:** antes de cada `git push`, confira que nenhum PDF pago, texto de artigo ou chave está indo junto (`git status`).
