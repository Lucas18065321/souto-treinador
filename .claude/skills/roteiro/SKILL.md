---
name: roteiro
description: "Cria ou adapta roteiros falados de Reels e YouTube (só o texto, sem corte de cena) para o Jorge Souto (SOUTO TREINADOR, treino de força baseado em evidência). Padrão: adaptar um roteiro viral de referência no formato escolhido pelo Jorge, perguntando os insumos antes. Segue o Briefing de roteiro e os 6 mecanismos (RELEVÂNCIA EMOCIONAL, CURIOSIDADE & EFEITO AHAA, CONTRASTE, CONFLITO & MUDANÇA, TEMA & MORAL DA HISTÓRIA, LINGUAGEM FAMILIAR & IMAGENS MENTAIS), em linguagem leiga com analogias, com fatos só da Ficha do tema e fontes montadas por script. Vídeo animado com voz de IA usa a estrutura viral de 8 partes. Use quando o usuário digitar /roteiro, pedir um roteiro de Reels ou vídeo, ou mandar um roteiro para adaptar."
---

# /roteiro: frente 02 - ROTEIROS

> Caminhos relativos à **raiz do repositório** (o diretório de trabalho da sessão). Manual da frente: `02 - ROTEIROS/CLAUDE.md`. Guia para humanos: `docs/guias/02-roteiros.md`.
> **Regra principal:** `02 - ROTEIROS/Referências/Briefing - roteiro.md`, os 6 mecanismos em `Referências/Mecanismos/`, `Formatos.md` e `Identidade verbal - Jorge.md`.
> **Entrega:** roteiro falado, numerado por mecanismo, mais a análise curta. Nada de corte de cena, plano de cena ou instrução de gravação.

## 0. Entrada: sempre perguntar os insumos antes de gerar
Mande **uma mensagem só**, com tudo o que ainda não veio no pedido (o que já veio, mesmo com outro nome, não se pergunta):
1. **Roteiro de referência para adaptar:** um viral de qualquer nicho, colado (texto ou transcrição), com a análise original se houver. Pode vir como vídeo (caminho C) ou "do zero" (só a Ficha).
2. **Formato** (o Jorge escolhe; nunca escolha por ele): Tela dividida, Tela verde, Palestrinha, Narrado, Cine, Storytelling visual, Experimento social, Conflito situacional, Caixinha de perguntas, Dinamismo, Comparação, Diálogo, Trivial, The Office, Lo-fi ou Bastidores (`02 - ROTEIROS/Referências/Formatos.md`).
3. **Tema** da base (a Ficha) ou pauta do Banco de pautas (`05 - PUBLICAÇÃO E CRESCIMENTO/Banco de pautas.md`, se existir).
4. **Reels ou YouTube.** No YouTube, a duração.
5. **Quem fala:** o Jorge gravando ou **voz de IA em vídeo animado**? Na animação, sugira a estrutura viral (caminho D) e não pergunte o formato de gravação.

O nicho já é conhecido (treino de força baseado em evidência; ver `00 - MARCA E ESTRATÉGIA/Linha editorial.md`): nunca pergunte.

**Caminhos:**
- **A. Adaptação (padrão):** a referência dá estrutura, mecanismos e ritmo; os fatos vêm da Ficha. Orçamento: caracteres do roteiro + análise de referência + 250.
- **B. Do zero:** só a Ficha, com 3 ângulos (passo 1).
- **C. Vídeo de outra pessoa para responder:** passo 5.
- **D. Vídeo animado com voz de IA:** `02 - ROTEIROS/Referências/Estrutura viral - vídeo animado.md`. Frontmatter `estrutura: viral`, `formato: animacao`, `palavra`. Sem Análise: `## Ganchos` com 3 opções e a `(recomendado)`. Arquivo `Roteiros/AAAA-MM-DD - <tema> - animação.md`. Nada de relato em 1ª pessoa.

## 1. Ficha e ângulo
1. Matéria-prima: a **Ficha** do tema, `01 - BASE CIENTÍFICA/<Área>/<Tema> - Ficha.md` (ache em `01 - BASE CIENTÍFICA/00 - ÍNDICE.md`). **Tema sem Ficha → ofereça `/montar-condicao <tema>` (⏸).** Nunca escreva de memória.
2. Leia só o necessário (Grep nas seções "Ângulos", "Mitos" e "Pautas") e proponha **3 ângulos** pela preocupação humana por trás do assunto, não pela informação técnica. O Jorge escolhe.
3. **Caminho A:** pule os 3 ângulos; o ângulo sai do encaixe entre a referência e a Ficha.
4. Faltou algo na Ficha: `pesquisador-de-evidencia`. Se a base sustentar, o `fichador` acrescenta a linha antes do roteiro. Se não, diga.

## 1b. História real (opcional)
Só quando fortalecer a RELEVÂNCIA EMOCIONAL.
1. Busque 1 ou 2 casos públicos (WebSearch; link que abre; cada fato em 2 fontes quando der) e ofereça ao Jorge com o link. **Nunca aluno do Jorge** (sigilo, CONFEF).
2. Se ele quiser, grave na Ficha, seção `## Histórias reais (verificáveis)` (`| # | Fato (como pode ser contado) | Fonte (link) |`, ids H1…).
3. Nunca invente personagem nem cena.

## 2. Escrever: agente `roteirista` (Sonnet)
Passe: caminho da Ficha; ângulo; formato (ou `estrutura: viral` + palavra); Reels ou YouTube e duração; ids H (se houver); no caminho A, a referência e o total de caracteres; caminho `02 - ROTEIROS/Roteiros/AAAA-MM-DD - <tema>.md`; data.
Ele escreve e corrige até o hook não acusar ERRO. (Se o agente não aparecer: leia `.claude/agents/02-roteiros/roteirista.md` e rode um general-purpose com `model: sonnet` e essas instruções.)

## 3. Conferir e montar as fontes (script, zero token)
```
python "02 - ROTEIROS/_SISTEMA/validar_roteiro.py" "<roteiro.md>" --montar-fontes
```
- **Confere:** rótulos; placeholders, expressões proibidas e corte de cena; cada `[#n]` (verbo × certeza, número × linha da Ficha); promessa de resultado; ética (antes/depois, depoimento de aluno, preço, prescrição de dieta/suplemento, remédio/hormônio); sigla e jargão; frase longa; duração; Análise com 6 a 8 bullets.
- **Escreve:** `## Texto para gravar`, `## Fontes`, `## Nível de certeza` e o `fontes:` do frontmatter.

## 4. Mostrar ao Jorge (exatamente assim)
1. **ROTEIRO LIMPO:** as partes numeradas, com o rótulo do mecanismo e sem as referências `[#…]`.
2. **ANÁLISE CURTA:** os 6 a 8 bullets. No caminho D: os **3 GANCHOS** e qual o roteirista usaria.
3. Uma linha com o link do arquivo (onde ficam o texto para gravar e as fontes).

Se o texto ficou longe da fala natural do Jorge: "Adapte para sua fala natural na gravação."
**Microajustes:** no máximo 2 ou 3 perguntas objetivas ("Entendi assim: … confere?"). Não gostou: "o que não funcionou?" + 2 ou 3 perguntas; ajuste sem recomeçar.

## 5. Caminho C: vídeo de outra pessoa
1. Transcreva (skill `watch`, se disponível, ou transcrição colada pelo Jorge).
   - **Um mito = um roteiro.** Vídeo com vários mitos vira várias pautas.
   - **Extraia os artigos citados** (título, autor, revista, ano, DOI, minuto do vídeo). Eles entram na base pelo `/montar-condicao` (o Jorge aprova). Print de artigo só do PDF oficial, nunca do vídeo do outro.
2. Mande o `checador-de-afirmacoes` confrontar cada afirmação com a base.
3. O roteiro novo responde sem copiar o autor e sem atacar a pessoa (critique a ideia; ética CONFEF), e só afirma o que está numa Ficha. Daí, passos 2 a 4.

## 6. Fechamento
- Pauta do Banco de pautas: marque `roteirizada`, com link.
- `status`: rascunho → aprovado (Jorge) → gravado.

## 7. Regras invioláveis
- **PROIBIDO inventar** números, estudos, nomes, casos, alunos ou citações. Fato só da Ficha.
- Verbo nunca mais forte que a certeza. Relativo nunca sem o absoluto.
- Ética (`00 - MARCA E ESTRATÉGIA/Ética profissional - CONFEF.md`): sem promessa de resultado com número nem garantia (o CTA pode prometer o que o produto entrega), sem antes/depois, sem depoimento de aluno, sem prescrição individual, sem preço. **Dieta e suplemento com dose: nunca** (nutricionista, Lei 8.234/1991). Remédio/hormônio: médico.
- Nunca escreva as Fontes à mão nem burle um ERRO do validador. Se a regra travar algo legítimo, avise o Jorge.
- Economia: nada de varrer a base.
