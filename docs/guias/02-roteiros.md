# Guia 02 — Roteiros (passo a passo para quem não programa)

> Para: Jorge Souto (SOUTO TREINADOR) ou quem opera o sistema com ele.
> Pré-requisito: o **Guia 01 — Base científica** (Python instalado; de preferência ao menos uma Ficha pronta).
> Sistema: Windows 10/11, PowerShell, Claude Code aberto na raiz do repositório.

---

## 1. O que é o motor de roteiros

É a parte do sistema que escreve **roteiros falados** de Reels (45 a 75 segundos) e de YouTube. Só o texto que o Jorge fala — sem plano de câmera, sem corte, sem instrução de edição.

O que o torna diferente de "pedir um roteiro para a IA":

| Peça | O que faz |
|---|---|
| **Briefing de roteiro** | as regras de como escrever (tom, ordem, o que é proibido) |
| **6 mecanismos** | as "ferramentas" de retenção que rotulam cada parte do roteiro |
| **16 formatos** | o jeito de gravar (Tela dividida, Palestrinha, Comparação…), que o Jorge escolhe |
| **Ficha** (da base científica) | a **única** fonte de fatos. Cada fato no roteiro leva a etiqueta da linha da Ficha: `[#3]` |
| **Validador** (`validar_roteiro.py`) | um script que confere tudo sozinho: verbo × certeza, número × Ficha, ética, linguagem, duração |
| **Hook** | faz o validador rodar **automaticamente** toda vez que um roteiro é salvo; se tiver erro, a IA é obrigada a corrigir |
| **Montador de fontes** (`--montar-fontes`) | escreve o texto limpo para gravar, a lista de fontes e a tabela de certeza — nunca à mão |

Resultado: o Jorge recebe um roteiro **limpo**, com análise curta, e um arquivo com o texto para gravar e as fontes para a legenda.

---

## 2. Onde fica cada coisa

```
02 - ROTEIROS/
├─ CLAUDE.md                                manual da frente (para a IA)
├─ Roteiros/AAAA-MM-DD - <tema>.md          um arquivo por roteiro
├─ Referências/
│  ├─ Briefing - roteiro.md                 a regra principal
│  ├─ Mecanismos/                           os 6 mecanismos (1 arquivo cada)
│  ├─ Formatos.md                           os 16 formatos de gravação
│  ├─ Identidade verbal - Jorge.md          a voz do Jorge (MODELO: preencher)
│  ├─ Estrutura viral - vídeo animado.md    as 8 partes do vídeo com voz de IA
│  └─ Fontes por tema/                      kit de prints de artigos para vídeo/carrossel
└─ _SISTEMA/
   ├─ validar_roteiro.py                    validador + montador de fontes
   └─ teste/                                Ficha e roteiro FICTÍCIOS para testar o motor

.claude/skills/roteiro/SKILL.md             o comando /roteiro
.claude/agents/02-roteiros/                 roteirista · gerador-de-ganchos · checador-de-afirmacoes
.claude/hooks/validar_peca.py               o hook (roteiro, carrossel e vídeo)
00 - MARCA E ESTRATÉGIA/                    linha editorial, ética, identidade (lidos pelo roteirista)
```

---

## 3. Pré-requisitos

1. **Python 3.12** (ver Guia 01, seção 3.1). O validador usa só a biblioteca padrão — nada de `pip install`.
2. **Claude Code** aberto na pasta `souto-treinador`.
3. **Hook registrado** no `.claude/settings.json` da raiz (seção 9 deste guia). Sem ele, o validador não roda sozinho (você pode rodar à mão).
4. **Pelo menos uma Ficha** na base (`/montar-condicao`, Guia 01). Sem Ficha, o sistema não escreve roteiro com fatos — e isso é de propósito.
5. **Preencher os modelos** (uma vez): `00 - MARCA E ESTRATÉGIA\Linha editorial.md`, `Identidade da marca.md` e `02 - ROTEIROS\Referências\Identidade verbal - Jorge.md`. Procure por **TROCAR** (o @ e o CREF estão provisórios: `@soutotreinador` e `CREF 000000-G/UF`).

### 3.1 Teste rápido do motor (2 minutos)
No PowerShell, na raiz do repositório:
```powershell
python "02 - ROTEIROS\_SISTEMA\validar_roteiro.py" "02 - ROTEIROS\_SISTEMA\teste\Roteiro teste - mais séries mais músculo.md" --montar-fontes
```
Esperado:
```
validar_roteiro · Roteiro teste - mais séries mais músculo.md · TESTE Volume de treino - Ficha
0 erro(s), 0 aviso(s) · 6 partes · 132 palavras ≈ 53 s · refs: #1, #2

Texto para gravar, Fontes e Nível de certeza montados a partir da ficha (1 nota(s)-base).
```
A Ficha desse teste é **fictícia** (o estudo "TESTE-Ficticio 2099" não existe). Serve só para ver o motor funcionando. **Nunca publique nada dela.**

---

## 4. Fazer um roteiro: `/roteiro`, passo a passo

### Passo 1 — Pedir
No Claude Code, digite `/roteiro` (ou "quero um roteiro sobre…"). Você pode já mandar tudo junto:
```
/roteiro sobre volume de treino. Formato: Tela dividida. Reels. Eu gravo. Do zero.
```

### Passo 2 — Responder as perguntas (uma mensagem só)
O sistema pergunta só o que faltou:
1. **Roteiro de referência** para adaptar (cole o texto ou a transcrição de um viral de qualquer nicho) — ou "do zero".
2. **Formato** (você escolhe; ele nunca escolhe por você): Tela dividida, Tela verde, Palestrinha, Narrado, Cine, Storytelling visual, Experimento social, Conflito situacional, Caixinha de perguntas, Dinamismo, Comparação, Diálogo, Trivial, The Office, Lo-fi, Bastidores. (O que é cada um: `Referências\Formatos.md`.)
3. **Tema** — precisa ter Ficha. Se não tiver, ele oferece `/montar-condicao`.
4. **Reels ou YouTube** (no YouTube, a duração).
5. **Quem fala:** você gravando, ou voz de IA em vídeo animado (aí ele usa a estrutura viral de 8 partes).

**Dica:** a referência dá **estrutura e ritmo**, nunca fatos. Pode ser um viral de culinária, de finanças, de qualquer coisa: o sistema copia o "esqueleto", não as frases.

### Passo 3 — Escolher o ângulo
"Do zero": ele propõe **3 ângulos** tirados da Ficha, pela preocupação humana ("treino muito e o espelho não muda") e não pela informação técnica ("10 séries por semana"). Você escolhe.

### Passo 4 — História real (opcional)
Se um caso público verificável deixar o vídeo mais forte, ele busca e mostra com o link. Só entra com o seu ok. **Nunca** caso de aluno seu (sigilo, ética CONFEF) e **nunca** inventado.

### Passo 5 — O roteirista escreve
O agente `roteirista` escreve o arquivo `02 - ROTEIROS\Roteiros\AAAA-MM-DD - <tema>.md`. A cada gravação, o **hook** roda o validador. Se houver ERRO, o agente recebe a lista e corrige sozinho até zerar.

### Passo 6 — Fontes montadas por script
O sistema roda:
```powershell
python "02 - ROTEIROS\_SISTEMA\validar_roteiro.py" "02 - ROTEIROS\Roteiros\<arquivo>.md" --montar-fontes
```
Isso escreve no arquivo: **Texto para gravar** (só a fala, sem rótulos), **Fontes** (referência completa de cada artigo, tirada da base — nunca digitada por IA) e **Nível de certeza** (tabela com a certeza de cada afirmação usada).

### Passo 7 — Você recebe
1. **ROTEIRO LIMPO** — partes numeradas, cada uma com o nome do mecanismo, sem as etiquetas `[#n]`.
2. **ANÁLISE CURTA** — 6 a 8 linhas explicando as escolhas (inclusive o que vai na outra metade da tela, na tela dividida).
3. O link do arquivo.

Não gostou? Diga o que não funcionou. Ele faz 2 ou 3 perguntas e ajusta **sem recomeçar**. Mudou o status? `rascunho` → `aprovado` → `gravado` no topo do arquivo.

### Caminho "responder vídeo de outra pessoa"
Mande o vídeo (ou a transcrição). O sistema separa **um mito por roteiro**, lista os artigos que o vídeo citou (eles entram na base pelo `/montar-condicao`), e o `checador-de-afirmacoes` confere cada afirmação contra a base. O roteiro novo corrige a **ideia**, nunca ataca a **pessoa** (ética CONFEF).

### Caminho "vídeo animado com voz de IA"
8 partes fixas: GANCHO · RETENÇÃO · DESENVOLVIMENTO · REENGAJAMENTO (alternados) · ENCERRAMENTO · CHAMADA PRA AÇÃO (com uma PALAVRA para comentar). Em vez da análise, você recebe **3 ganchos** com o recomendado. A voz de IA nunca fala em 1ª pessoa ("eu ganhei…", "meus alunos…").

---

## 5. Como o roteiro fica no arquivo

```
---
tipo: roteiro
status: rascunho
formato: tela-dividida
ficha: "Volume de treino - Ficha"
eixos: [treino-forca]
angulo: "mais séries sempre dão mais músculo?"
data: 2026-11-19
---
# Mais séries, mais músculo?

## Roteiro
1. RELEVÂNCIA EMOCIONAL — Você sai da academia destruído e o espelho não muda.
2. CURIOSIDADE & EFEITO AHAA — Será que o problema é treinar pouco? Ou demais?
3. CONTRASTE — Sair de umas 4 para umas 10 séries por semana provavelmente aumenta o ganho. [#1]
...
## Análise
- CONTRASTE — 4 contra 10 séries; na tela, duas fichas de treino lado a lado.
...
```
- As etiquetas `[#1]`, `[#N1]`, `[#M2]`, `[#H1]` apontam para linhas da Ficha (Afirmações, Números de impacto, Mitos, Histórias reais).
- As seções **Texto para gravar**, **Fontes** e **Nível de certeza** aparecem depois do `--montar-fontes`. Nunca escreva nelas à mão: rode o comando de novo.

---

## 6. As regras de evidência (o que o validador cobra)

### 6.1 Verbo × certeza
| Certeza da linha da Ficha | Verbo permitido | Exemplo |
|---|---|---|
| **Alta** | direto | "treino de força **aumenta** a força" |
| **Moderada** | "provavelmente" | "mais séries **provavelmente aumentam** o ganho" |
| **Baixa** | "pode" | "treinar perto da falha **pode ajudar**" |
| **Muito baixa** | "não se sabe se" | "**não se sabe se** treinar em jejum muda alguma coisa" |

Se o roteiro disser "aumenta" para uma linha de certeza moderada, o validador dá **ERRO** e mostra a redação certa da Ficha.

### 6.2 Números
- Só o número que está na linha citada. Pode arredondar com a palavra certa ("quase", "mais de", "cerca de"), até 10% de diferença. "1 em cada 3" vale para 33%.
- Número sem `[#n]` = ERRO.
- Porcentagem de risco sem o número absoluto = AVISO.

### 6.3 Linguagem
- Sigla e jargão (RIR, RPE, 1RM, VO2máx, HIIT, %, "tamanho de efeito") = AVISO: explique com palavras do dia a dia.
- Frase com mais de 22 palavras = AVISO.
- Clichês ("você não vai acreditar", "sem desculpas", "no pain, no gain") = AVISO.
- Expressões proibidas ("a verdade que dói", "não é sobre X, é sobre Y", "o resultado?", "hook", "B-roll"…) = ERRO.

### 6.4 Ética (resumo de `00 - MARCA E ESTRATÉGIA\Ética profissional - CONFEF.md`)
| Situação | Validador |
|---|---|
| Promessa com número no corpo de quem assiste ("ganhe 5 kg de músculo", "10 cm de cintura em 30 dias") | ERRO |
| Antes e depois de aluno | ERRO |
| Depoimento/resultado de aluno ("meu aluno perdeu 12 kg") | ERRO |
| Preço, cupom, "por apenas" | ERRO |
| Mandar comer X gramas, montar dieta, suplemento com dose ("tome 5 g de creatina") — **é do nutricionista, Lei 8.234/1991** | ERRO |
| Mandar parar/trocar remédio, usar hormônio — **é do médico** | ERRO |
| Palavras: cura, milagre, garantido, segredo, nunca mais, 100%, sem esforço | ERRO (AVISO em desmentido) |
| Ordem de treino com número ("faça 4 séries de 12") | AVISO: fale da faixa da evidência; a dose é individual |

O mito pode ser **citado entre aspas** para ser desmentido: o que está entre aspas não conta como afirmação do Jorge.

### 6.5 Forma e tamanho
- Rótulo de parte que não é um dos 6 mecanismos = ERRO ("CTA" não é parte: a chamada fica dentro de uma parte).
- Placeholder (`[GANCHO]`, `[CTA]`) e instrução de cena (`> tela:`, "gancho visual") = ERRO.
- Reels fora de 45–75 s (calculado a 2,5 palavras por segundo) = ERRO.
- Análise fora de 6 a 8 linhas = AVISO.

---

## 7. Comandos úteis (PowerShell, na raiz)

| Para | Comando |
|---|---|
| Validar um roteiro | `python "02 - ROTEIROS\_SISTEMA\validar_roteiro.py" "02 - ROTEIROS\Roteiros\<arquivo>.md"` |
| Validar e montar fontes | o mesmo + ` --montar-fontes` |
| Ver a ajuda do validador | `python "02 - ROTEIROS\_SISTEMA\validar_roteiro.py"` (sem argumentos) |
| Testar o motor | ver seção 3.1 |
| Testar o hook à mão | ver seção 9.2 |

O validador sai com código **0** sem erro e **1** com erro (útil se um dia alguém automatizar).

---

## 8. Perguntas frequentes e problemas comuns

**1. `ficha '…' não encontrada em 01 - BASE CIENTÍFICA`.**
O `ficha:` do topo do roteiro não bate com o nome de nenhuma Ficha. Use exatamente `"<Tema> - Ficha"` (o nome do arquivo sem `.md`). A mensagem lista as Fichas disponíveis.

**2. "Não tenho nenhuma Ficha ainda."**
Rode `/montar-condicao <tema>` (Guia 01). Enquanto isso, use o teste fictício (seção 3.1) só para conhecer o motor.

**3. `[#5] não existe na …`.**
A etiqueta aponta para uma linha que não existe. Confira o número na tabela "Afirmações prontas" da Ficha (ou use `N1`, `M2`, `H1` para as outras seções).

**4. `'aumenta' sem calibrador é forte demais`.**
A linha da Ficha tem certeza menor que o verbo. Use o verbo que o erro sugere ("provavelmente", "pode") ou copie a redação da Ficha.

**5. `número '15' não está na linha #1 da ficha`.**
O roteiro usou um número que não está na linha citada. Copie o número da Ficha ou arredonde com "quase/mais de/cerca de" (até 10%).

**6. `[#n] está marcado '(conferir)' na ficha`.**
A linha depende de uma fonte que ainda não foi conferida. Não use até alguém conferir (o `fichador` ou você, com `biblioteca.py trecho`).

**7. `duração estimada 32 s … alvo 45–75 s`.**
O roteiro está curto (ou longo) demais. Reels: 112 a 187 palavras. YouTube: ponha `duracao: "480-720"` (segundos) no topo do arquivo.

**8. O hook não rodou quando salvei.**
Confira: (a) o hook está no `.claude/settings.json` da raiz (seção 9); (b) o arquivo está em `02 - ROTEIROS\Roteiros\` diretamente (subpastas não são validadas); (c) o Claude Code foi aberto na raiz; (d) `python --version` funciona. Teste à mão (seção 9.2).

**9. O hook diz `validar_roteiro.py falhou (…)`.**
O validador quebrou num caso que não previa. O trabalho não trava; rode o validador à mão para ver o erro completo e avise quem mantém o sistema.

**10. "Fontes NÃO montadas: corrija os erros primeiro."**
O `--montar-fontes` só escreve quando há 0 ERRO. Corrija e rode de novo.

**11. `seção Fontes desatualizada`.**
Você (ou a IA) mexeu nas etiquetas depois de montar as fontes. Rode `--montar-fontes` de novo.

**12. `nota-base de '…' não identificada` ao montar fontes.**
A coluna Fonte da Ficha não bate com nenhum id de `notas_base`. É aviso: a fonte sai como está na Ficha. Peça ao `fichador` para corrigir a Ficha.

**13. O validador reclamou de "promessa" num resultado de estudo.**
Se a frase descreve o estudo ("o grupo ganhou 1 kg de massa magra em 8 semanas"), ele dá só AVISO; deixe claro que é o resultado **do grupo estudado**. Se a frase fala com quem assiste ("você vai ganhar…"), é ERRO de verdade.

**14. Quero citar o mito sem levar ERRO.**
Ponha o mito entre aspas: `Dizem que "treino em jejum queima mais gordura".` O trecho entre aspas fica fora do verbo × certeza e da checagem de ética.

**15. Letras estranhas na saída do PowerShell (Ã©, â€").**
Rode antes: `[Console]::OutputEncoding = [Text.Encoding]::UTF8`.

**16. Posso falar de proteína, creatina, dieta?**
Pode **educar** com o que a Ficha mostra, com `[#n]` ("a revisão mostrou que…"). Não pode **prescrever** para quem assiste (quantidade, cardápio, dose). Para isso: "converse com um nutricionista".

---

## 9. Hook: registro e teste

### 9.1 Registro no `.claude/settings.json` da raiz
O hook precisa estar registrado como `PostToolUse` para `Write|Edit`:
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
Um hook só cuida dos roteiros, dos carrosséis (`carrossel.json`) e das edições de vídeo (`03_roteiro/edicao.json`, repassado ao validador do motor de vídeo se o Node estiver instalado). Frente que não existe: ele fica calado.

### 9.2 Testar o hook à mão
```powershell
'{"tool_input":{"file_path":"02 - ROTEIROS/_SISTEMA/teste/Roteiro teste - mais séries mais músculo.md"}}' | python ".claude\hooks\validar_peca.py"
```
Esperado: uma linha com `"additionalContext": "validar_roteiro: 0 erro(s), 0 aviso(s) …"`. Arquivo fora do escopo: nenhuma saída (é o comportamento certo).

---

## 10. Boas práticas

- **Ficha primeiro, roteiro depois.** Roteiro sem Ficha é opinião; com Ficha é autoridade.
- **Escolha o formato antes de pedir** — ele muda o roteiro (Palestrinha pede passos; Comparação pede dois lados).
- **Guarde bons virais de referência** (de qualquer nicho) numa nota sua: adaptar é mais rápido e rende melhor que "do zero".
- **Um mito por vídeo.** Vídeo com três mitos vira três roteiros.
- **Leia o roteiro em voz alta** antes de aprovar. Se travar, peça "deixa mais falado".
- **Preencha a sua voz** (`Identidade verbal - Jorge.md`) com falas reais: é o que mais aproxima o texto do seu jeito.
- **Nunca edite Fontes nem Nível de certeza à mão.** Rode `--montar-fontes`.
- **Não burle o validador.** Se uma regra travar algo legítimo, anote e peça para ajustar a regra — não reescreva por extenso para "passar".
- **Legenda:** use a seção Fontes do arquivo para pôr a referência na legenda; o vídeo mostra só a fonte curta.
- **Antes do `git push`:** os roteiros são públicos no GitHub se ficarem no repositório. Se algum roteiro tiver informação que não deve ser pública, guarde fora do repositório.
