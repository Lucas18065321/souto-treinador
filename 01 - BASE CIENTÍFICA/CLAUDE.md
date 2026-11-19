# Frente 01: Base científica (o cérebro do sistema)

Base única de evidência do Jorge Souto. Tudo sai daqui: a ficha de treino do aluno, os roteiros, os carrosséis, as referências na tela dos vídeos e o contexto da parte alimentar (que é prescrita pelo nutricionista Responsável Técnico). Por tema: **Protocolo** (diretriz, prescrição, monitoramento e progressão do aluno) + **Ficha** (frases prontas, calibradas, para conteúdo). Nada daqui é publicado direto; o que for publicado sai da Ficha, em linguagem leiga.
**Nichos:** treino de força e hipertrofia (1º), composição corporal e emagrecimento com treino, nutrição esportiva (como contexto), populações especiais (idosos, iniciantes, mulheres, condições crônicas controladas).

## Estrutura
```
00 - ÍNDICE.md                 gerado por _MÁQUINA/scripts/gerar_indice.py (não edite)
ENTRADA/                       o Jorge solta PDFs aqui (uma pasta só)
Treino de força/  Composição corporal e emagrecimento/  Nutrição esportiva/  Populações especiais/  Transversais/
   <Tema> - Protocolo.md   <Tema> - Ficha.md      (Transversais: só Ficha)
_MÁQUINA/  (escondida do Obsidian)
   scripts/    biblioteca.py · edison.py · gerar_indice.py · texto_aberto.py · baixar_colecao.py
               biblioteca_eixos.json (eixos e sinônimos) · colecao-treino.jsonl (artigos de treino de força)
   artigos/<id>.json   ficha automática (Vancouver, tipo, teto de certeza, achados com página)
   texto/ pdf/ fontes_fila/ fontes-processadas/ catalogo.jsonl fila.jsonl para-baixar.md registro.md
   modelos/    Protocolo.md (de treino) · Ficha.md
   edison/     <tema>/ (respostas e candidatos da Edison) · creditos.jsonl · config.json  (gerado por edison.py)
```
`pdf/`, `texto/`, `fontes_fila/` e `ENTRADA/` não vão para o GitHub (direito autoral): cada instalação baixa a própria cópia com `baixar_colecao.py`.

## Fluxo (3 passos)
1. **Soltar:** o Jorge põe PDFs em `ENTRADA/` (ou aprova o download de acesso aberto) → `biblioteca.py catalogar`.
2. **Montar:** `/montar-condicao <tema>` → **Edison acha os artigos (1º passo)**, catálogo/fila/Europe PMC complementam → o Jorge aprova de 3 a 10 fontes ⏸ → download e `catalogar` → agente `fichador` escreve Protocolo + Ficha → `conferir-ficha` zera os erros.
3. **Usar:** `/treino` (ficha de treino e controle de volume), `/roteiro`, `/carrossel` e legendas leem a Ficha e o Protocolo; o validador confere cada `[#n]` contra a Ficha.

## Regras de evidência
- **Hierarquia:** posicionamento/diretriz vigente (ACSM, NSCA…) > meta-análise/revisão sistemática (≤ 5 anos) > ensaio clínico > observacional (contexto, nunca decide conduta) > mecanismo (explica, não prescreve). Revisão narrativa = contexto, não prova. Consenso Delphi = opinião organizada de especialistas. Documentos em conflito: mostrar os dois lados com data e grau.
- **Verbo × certeza** (o verbo nunca passa da certeza; o teto vem do tipo de estudo):

| Certeza | Como dizer |
|---|---|
| Alta | "X aumenta Y" |
| Moderada | "X provavelmente aumenta Y" |
| Baixa | "X pode aumentar Y" |
| Muito baixa | "não se sabe se X aumenta Y" |
- Observacional: "está associado a", nunca "causa". Efeito relativo **sempre** com o absoluto.
- **Estudos de treino:** amostras pequenas e curtas são a regra. Olhe a população (treinados × destreinados), a duração e como mediram o músculo antes de generalizar.
- **Edison e IA de busca:** resposta de agente nunca é fonte e pode inventar referência. Só vale o artigo baixado, catalogado e aprovado; todo candidato é conferido no Europe PMC (`edison.py candidatos`).
- **Sem fonte processada, não afirma:** diga "não temos isso processado" e ofereça `/montar-condicao`. **Nunca inventar** estudo, número, história ou personagem.
- **Texto publicado em linguagem leiga, com analogia:** sem sigla (RIR, RPE, 1RM ficam no Protocolo), número simples e comparativo.
- **Ética do CONFEF** (Res. 307/2015; detalhes em `../00 - MARCA E ESTRATÉGIA/Ética profissional - CONFEF.md`): sem promessa de resultado, antes/depois, depoimento ou resultado de aluno, prescrição individual nem preço em conteúdo aberto.
- **Dieta é ato do nutricionista** (Lei 8.234/1991): a base pode ter artigos de nutrição para educar e dar contexto ao treino; quem prescreve a dieta do aluno é o nutricionista Responsável Técnico (frente 06).

## Leitura para agentes (economia de contexto)
`00 - ÍNDICE.md` → Ficha → Protocolo → `biblioteca.py buscar/ver/trecho`. Nunca varrer a base, nunca abrir PDF nem `texto/` inteiro, nunca tratar `fila.jsonl` como evidência. Leitura pesada vai para o agente `pesquisador-de-evidencia`.

## Comandos
`python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/biblioteca.py" <cmd>`:
- `catalogar` · `buscar "tema" [--tipo diretriz|meta-analise|revisao-sistematica] [--desde AAAA]` · `ver "<id>"` · `trecho "<id>" "termo"` · `conferir-ficha "<Ficha.md>"` · `importar-fila [--baixar]` (⏸) · `panorama`
- `baixar_colecao.py`: baixa o texto aberto da coleção de treino de força (primeira instalação) e roda o `catalogar`.
- `gerar_indice.py`, no mesmo caminho `scripts/`.
- **Edison Scientific** (motor principal de **descoberta**), `scripts/edison.py <cmd>`: `perguntar "<tema>" "<pergunta>" [--agente literature|high|precedent]` · `coletar` · `candidatos "<tema>"` · `creditos` · `plano` · `chave --abrir`. A chave fica em `%USERPROFILE%\.edison-key` (fora do repositório; o Jorge cola pelo Bloco de Notas, nunca no chat). **Plano grátis com limite de créditos por mês: passar disso só com ⏸ do Jorge.**
- Agentes: `fichador` (escreve), `pesquisador-de-evidencia` (consulta), `prescritor-de-treino` (ficha de treino e volume). Modelos em `_MÁQUINA/modelos/`.

## Regras da pasta
- **Nada de arquivo residual:** só scripts geram dentro de `_MÁQUINA/` (exceções escritas à mão: `modelos/` e `registro.md`). Ficha, Protocolo e PDF não se apagam.
- Download de arquivo, sempre ⏸. Datas em `AAAA-MM-DD`. Refazer uma Ficha: atualize, não duplique, e não renumere as afirmações (roteiros citam `[#n]`).
- Preferências de curadoria: `../00 - MARCA E ESTRATÉGIA/Preferências do Jorge.md`.
