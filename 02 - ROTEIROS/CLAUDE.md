# Frente 02: Roteiros

Roteiros **falados** de Reels (45–75 s) e de YouTube: só o texto, sem corte de cena. Seguem o **Briefing de roteiro** e os **6 mecanismos**. Um roteiro aprovado vira Reels e trecho de YouTube. O carrossel tem texto próprio (no `/carrossel`): o roteiro pode entrar lá como insumo, mas não vira slide direto.

**Entrada padrão:** antes de gerar, o `/roteiro` pergunta numa mensagem só o roteiro viral de referência (ou "do zero"), o formato (um dos 16 de `Referências/Formatos.md`, o Jorge escolhe), o tema e se é Reels ou YouTube. A referência dá estrutura e ritmo; **os fatos vêm só da Ficha**.

**Estrutura viral (só vídeo animado com voz de IA):** 8 partes (GANCHO · RETENÇÃO · DESENVOLVIMENTO e REENGAJAMENTO alternados · ENCERRAMENTO · CHAMADA PRA AÇÃO), `estrutura: viral` no frontmatter e `## Ganchos` (3 opções) no lugar da Análise. Sem relato em 1ª pessoa. Regras: `Referências/Estrutura viral - vídeo animado.md`.

## Comando
`/roteiro`:
1. entrada: perguntas (referência, formato, tema, Reels ou YouTube, quem fala) ou vídeo de terceiros;
2. 3 ângulos tirados da Ficha (só quando é do zero);
3. história real verificável (opcional);
4. agente `roteirista` escreve;
5. hook valida a cada gravação;
6. script monta o texto para gravar, as fontes e a certeza;
7. o Jorge vê o **roteiro limpo** e a **análise curta**.

Tema sem Ficha: `/montar-condicao <tema>` (⏸) antes de escrever.

## Formato (o validador confere)
```
## Roteiro
1. RELEVÂNCIA EMOCIONAL — fala… [#n]
2. CONTRASTE — fala… [#M2]
...
## Análise
- CONTRASTE — por que foi usado (6 a 8 bullets)
```
- **Rótulos:** só os 6 mecanismos, na ordem escolhida para o roteiro (sequência fixa é proibida). A chamada para ação fica dentro de uma parte.
- **Referências:** `[#n]` = linha n de "Afirmações prontas" da Ficha; `[#N1]` = Números de impacto; `[#M2]` = Mitos; `[#H1]` = Histórias reais. Ficam no arquivo para o script; o Jorge vê o roteiro sem elas.
- **Proibido:** `> tela:`, plano de cena, "gancho visual", B-roll; placeholders (`[CTA]`, `[GANCHO]`…); expressões proibidas do briefing (seção 9). O apoio visual aparece só na Análise.
- **Validador:** `python "02 - ROTEIROS/_SISTEMA/validar_roteiro.py" "<roteiro.md>" [--montar-fontes]` (de qualquer pasta).
  - Confere: rótulos; placeholders; `[#n]` existe; verbo × certeza; número × linha da Ficha; palavras proibidas; promessa de resultado com número; ética (antes/depois, depoimento de aluno, preço, prescrição de dieta/suplemento, ordem sobre remédio/hormônio = ERRO; ordem de treino com número = AVISO); sigla e jargão (aviso de linguagem leiga); frase longa; duração (2,5 palavras/s); Análise com 6 a 8 bullets.
  - `--montar-fontes` escreve `## Texto para gravar`, `## Fontes` e `## Nível de certeza`. **Nunca escreva essas seções à mão.**
- **Hook:** `.claude/hooks/validar_peca.py` roda em todo Write/Edit em `Roteiros/*.md` (e em `_SISTEMA/teste/Roteiro*.md`). Com ERRO, devolve o relatório e o agente corrige.

## Arquivos
- `Referências/Briefing - roteiro.md`: a regra principal.
- `Referências/Mecanismos/`: os 6 mecanismos (resumo operacional de cada um).
- `Referências/Formatos.md`: os 16 formatos de gravação e o que faz cada um funcionar.
- `Referências/Identidade verbal - Jorge.md`: a voz do Jorge (**modelo a preencher**).
- `Referências/Estrutura viral - vídeo animado.md`: as 8 partes do vídeo animado.
- `Referências/Fontes por tema/<Tema>/`: kit de fontes para vídeo e carrossel (modelo em `_MODELO - Fontes - Tema.md`).
- `Roteiros/AAAA-MM-DD - <tema>.md`: um arquivo por roteiro. Frontmatter: `tipo: roteiro`, `status: rascunho|aprovado|gravado`, `formato`, `ficha`, `eixos`, `fontes` (preenchido pelo script).
- `_SISTEMA/validar_roteiro.py`: validador e montador de fontes (também usado pelo validador de carrossel).
- `_SISTEMA/teste/`: Ficha, nota e roteiro **fictícios** para testar o motor (ver o LEIA-ME de lá). Nunca publicar.

## De onde vem o conteúdo
1. A **Ficha** do tema em `01 - BASE CIENTÍFICA/<Área>/<Tema> - Ficha.md` (ache no `00 - ÍNDICE.md`). Só o que está na Ficha vira fato no roteiro.
2. `05 - PUBLICAÇÃO E CRESCIMENTO/Banco de pautas.md` (se existir).
3. **História real verificável** (opcional): link que abre, gravada na Ficha e citada com `[#H1]`. Nunca inventada.
4. Faltou evidência: `pesquisador-de-evidencia`; se a base sustentar, o `fichador` acrescenta a linha na Ficha antes do roteiro.

## Agentes
- `roteirista` (Sonnet): lê o briefing, os mecanismos e a Ficha; escreve e corrige até o hook não acusar ERRO.
- `gerador-de-ganchos`: aberturas alternativas, quando o Jorge pedir.
- `checador-de-afirmacoes`: obrigatório com conteúdo de terceiros.
- Da frente 01: `pesquisador-de-evidencia` e `fichador`.

## Regras
- Nada inventado. Verbo calibrado pela certeza. Relativo sempre com absoluto.
- Ética do profissional de Educação Física (CONFEF) e limite com a nutrição (Lei 8.234/1991): `00 - MARCA E ESTRATÉGIA/Ética profissional - CONFEF.md`.
- Linguagem leiga com analogia.
- Tom e pilares: `00 - MARCA E ESTRATÉGIA/Linha editorial.md`.
