# Método de texto: carrossel (Souto Treinador)

> **O que é este arquivo.** Um resumo operacional, escrito com palavras próprias, do jeito de escrever carrossel que este sistema usa, inspirado no método de carrossel da BrandsDecoded (curso pago, que **não** faz parte deste repositório e não deve ser copiado para cá). Aqui ficam só as regras de trabalho de que os agentes precisam, já adaptadas ao conteúdo de treino do Jorge Souto. Se quiser estudar o método completo, compre o curso na fonte oficial.
>
> Quem lê: `chefe-de-pauta` (seções 3, 4, 5 e 11), `redator-de-carrossel` (4, 6, 7, 8, 9, 11 e 12), `editor-de-texto` (8, 9 e 10), `legendista` (13). A skill `/carrossel` resume o fluxo (seção 2). Se uma regra deste arquivo divergir de um agente, vale este arquivo; se divergir do validador (`Gerador/validar_carrossel.py` + `Gerador/editorial.py`), vale o validador.

---

## 0. Ideias centrais
1. **Carrossel nasce como carrossel**, não como roteiro de Reels recortado: cada slide tem uma ideia, traz informação nova e deixa uma pergunta que o próximo responde.
2. **Tipo antes do formato.** Tipo = a linha narrativa (seção 4). Formato = o design (M1 a M5). Qualquer tipo sai em qualquer formato. Decide-se o tipo primeiro.
3. **Tema amplo na capa, especialidade no miolo.** A capa fala de comportamento, cultura, geração, Brasil, a vida de quem treina; a fisiologia e os números vão para os slides 3 a 5.
4. **Só a Ficha vira fato.** Todo número, estudo, pessoa ou caso sai de uma linha da Ficha do tema (`01 - BASE CIENTÍFICA/.../<Tema> - Ficha.md`), citada pelo id em `"afirmacoes"`. Nada inventado.
5. **Texto aprovado antes de gastar arte.** A aprovação do texto nunca é pulada.

## 1. Regras fixas (não negociáveis)
- **Voz mista:** o corpo é reportagem (sem "você/seu/sua"); a 2ª pessoa só no slide de aplicação e no CTA.
- **Linguagem leiga:** sem sigla, sem jargão de academia ou de estatística; número simples e comparativo ("1 em cada 4", "de 4 para 10 séries por semana"). Fonte simples no slide ("segundo uma revisão de 2024 com 15 estudos"); a referência completa vai para a legenda e para o `carrossel.md`, montada por script.
- **Verbo pela certeza da linha:** alta "aumenta"; moderada "provavelmente aumenta"; baixa "pode aumentar"; muito baixa "não se sabe se". Efeito relativo sempre com o absoluto.
- **Ética do profissional de Educação Física (Código de Ética do CONFEF) + regras da marca:** sem promessa de resultado no corpo do leitor (quilos, centímetros, % de gordura com prazo), sem antes/depois, sem depoimento ou resultado de aluno, sem preço ou promoção, sem "garantido", "milagre", "segredo", "cura", "nunca mais", "100%".
- **Nutrição é do nutricionista.** O Jorge não prescreve dieta, cardápio, calorias nem suplemento com dose (Lei 8.234/1991). Nutrição só entra como **educação geral**, com a linha da Ficha que a sustenta ("a revisão encontrou que…"), e o leitor é encaminhado ao nutricionista. Remédio e hormônio são assunto do médico.
- **Treino em conteúdo aberto também é educação, não prescrição:** fale da faixa que a evidência mostra ("de 10 a 20 séries por semana, segundo a revisão") e lembre que a dose é individual; ordem com número para o leitor ("faça 4 séries de 12") o validador marca como AVISO.
- **Um CTA só**, diretivo, pelo conteúdo (seção 11).

## 2. Fluxo e pontos de aprovação (⏸ = espera o "ok" do Jorge)
Entrada + Ficha → triagem recomenda o **tipo** ⏸ → Jorge escolhe o **formato** e o nº de slides ⏸ → 10 headlines + versão de capa ⏸ → espinha dorsal (por padrão montada por dentro; mostrada só se o Jorge pedir) → texto por slide com validador até 0 ERRO → revisão editorial (7 parâmetros ≥ 8) → **aprovação do texto** ⏸ → artes (Gemini/Flow no navegador ou Higgsfield pelo MCP) ⏸ créditos → render com 0 ALERTA + folha de contato → editor visual (opcional) → fontes por script, legenda, entrega.
Pular etapa só com pedido explícito do Jorge ("pula a espinha"), registrado no `carrossel.md`. A aprovação do texto nunca é pulada.

---

## 3. Triagem (chefe-de-pauta)
### 3.1 Os 4 campos
| Campo | O que escrever |
|---|---|
| Transformação | o que mudou ou o que a evidência mostra, com a consequência para quem treina (antes → agora → e daí) |
| Fricção central | o choque entre o que as pessoas acreditam/fazem na academia e o que a evidência mostra; ou entre o que se vende e o que se entrega |
| Ângulo dominante | a leitura mais forte, em 1 frase; dela sai o tipo |
| Evidências A/B/C | três fatos da Ficha em linguagem leiga, cada um com o id (`7`, `N1`, `M2`, `H1`). Pelo menos um com número simples, para o slide de prova |

Partes da Ficha que ajudam: Mitos (Mito × evidência), Divergências (Tese), Lacunas (Previsão), Ângulos de conteúdo, O que NÃO dizer, Histórias reais.

### 3.3 Eixo (valor exato no JSON)
| Eixo | Em treino |
|---|---|
| Mercado | suplemento, "treino da moda", aparelho milagroso, app, programa pago, promessa da indústria fitness |
| Cases | história real verificável (atleta, pessoa pública, instituição), sempre com ids H |
| Notícias | posicionamento novo de entidade, estudo grande recém-publicado, mudança de recomendação |
| Cultura | crenças de academia, modas das redes, hábitos de uma geração, "no pain no gain" |
| Produto | o problema que o treino individualizado do Jorge resolve (sem promessa) |

### 3.4 Funil (contexto; não decide o CTA)
Topo = alcançar gente nova (mito viral, crença comum, tema amplo) · Meio = aprofundar para quem já segue (como funciona, nuances, quem se beneficia) · Fundo = mostrar por que o caminho é individual (lesão, retorno, idade, rotina apertada), sem venda agressiva.

### 3.5 O que o funil muda
Topo: 1 ideia central e analogia forte · Meio: mecanismo em 2 slides, com a certeza · Fundo: o problema real e por que precisa de acompanhamento. Vocabulário leigo nos três. Tipos que combinam: topo (Mito × evidência, Tendência, Case), meio (Tese, Previsão, Tendência), fundo (Tese, Case, Tendência).

### 3.6 Saída da triagem
O bloco exato está no agente `chefe-de-pauta` e na skill (seção 1). A skill mostra como veio, sem reescrever.

---

## 4. Os 4 tipos
### 4.1 Visão geral
| Tipo (`tipo_carrossel`) | Quando | Arco | Mínimo na Ficha |
|---|---|---|---|
| Tendência interpretada (`tendencia`) | algo mudando agora, com data | Hook → Contexto → Mudança → Impacto → Ação → CTA | 1 âncora com data + 2 apoios |
| Tese contraintuitiva (`tese`) | crença de senso comum, sem vendedor, que a evidência contradiz | Crença comum → Dados que desafiam → Verdade → Novo modelo → Aplicação → CTA | 1 Afirmação de certeza moderada/alta contra a crença |
| ↳ Mito × evidência (`tese-mito`) | alguém vende a crença (suplemento, método milagroso, guru) | A crença → Quem vende e por que pega → O que a evidência diz → Por que a crença engana → O que fazer no lugar → CTA | linha em Mitos (M) + 1 Afirmação |
| Case (`case`) | história real verificável que ensina um princípio | Resultado → Quem fez → Como → Princípio → O que dá para levar → CTA | 2 ids H com link + 1 Afirmação. Sem H, não é opção |
| Previsão (`previsao`) | só há sinais apontando uma direção | Sinais → Padrão → Direção → Quem se adianta → Ações → CTA | 2 sinais verificáveis + Lacunas; verbos "pode"/"não se sabe" |

Adaptações: case nunca é aluno do Jorge (sigilo; sem antes/depois); no mito, ataque a alegação e o jeito de vender, nunca uma pessoa, colega ou marca; previsão nunca vira promessa.

### 4.2 Do arco aos slides (9 slides)
Capa (1), direção (8) e CTA (9) são fixos. Passos 1, 2 e 3 do arco nos slides 2, 3 e 4; o 5 traz os números (prova); passos 4 e 5 nos slides 6 e 7. O mecanismo com analogia entra: Tendência e Tese no slide 4; Mito × evidência e Case no 6; Previsão no 3.

### 4.3 Como escolher (nesta ordem)
1. Pessoa/instituição real com história documentada (H)? → Case. 2. Alguém vende a crença e há linha em Mitos? → Mito × evidência. 3. Crença comum contradita com certeza moderada/alta? → Tese. 4. Mudou recentemente, com data? → Tendência. 5. Só sinais? → Previsão. 6. Nenhum: pedir material ou `/montar-condicao`.
Desempate: evidências mais fortes · combinação com o funil · alternar com os últimos publicados.

### 4.5 Outros tamanhos
5 slides: capa · hook+contexto · prova · aplicação+direção · CTA. 7: capa · hook · mecanismo · prova · expansão · direção · CTA (sem aplicação: 2ª pessoa só no CTA). 12: capa · hook · contexto · mecanismo ×2 · prova principal · dados secundários · expansão · caso prático · aplicação · direção · CTA. Em qualquer tamanho, os 3 últimos slides preparam o CTA.

---

## 5. Headlines (chefe-de-pauta)
### 5.1 Sempre 10
1–5 **Investigação** (`[Reenquadramento]: [gancho de curiosidade]`, com dois-pontos, ~20 palavras; no M5, até 120 caracteres) · 6–10 **Narrativa** (`[Cenário concreto]. [Mecanismo]. [Tensão aberta].`, exatamente 3 frases, até ~45 palavras). Ângulos: 1 reenquadramento · 2 conflito oculto · 3 consequência maior · 4 contradição · 5 ameaça ou oportunidade (calibrada) · 6 nomear o que as pessoas vivem · 7 o comportamento por trás · 8 inversão · 9 o que a indústria fitness quer vender · 10 como a crença se espalha. Headline que falha é reescrita, nunca removida.

### 5.4–5.5 Padrões que funcionam e que falham
Funcionam: "O fim de X: …", "A morte de X: …", "Investigando X", pergunta sobre um grupo ("Por que [grupo] está [comportamento]?", só se o comportamento for verificável), dois-pontos com reenquadramento, contexto brasileiro (com dado brasileiro da Ficha), novidade, crise, geração. Falham: declaração direta, "descubra/saiba/conheça", lista ("5 exercícios que…"), motivacional vazio ("seu corpo merece").

### 5.6 Gatilhos (mínimo 2 por headline)
Medo/Alerta (só calibrado pela evidência; nada de "destrói seu joelho" sem dado) · Indignação (contra a alegação ou o mercado, nunca contra pessoa) · Curiosidade (fechada dentro do carrossel) · Identidade ("quem treina há anos e travou") · Nostalgia · Aspiração (entender, treinar com clareza; **nunca** resultado corporal prometido).

### 5.8 Checklist de rejeição
Declaração direta · revelação genérica · lista · motivacional · tom de IA · "quando X vira Y", "a ascensão de", "o impacto de", "por que X está mudando", "tudo que você precisa saber", "o guia definitivo", "mudou para sempre", "revelamos", "não é X, é Y", "virou" como verbo principal · palavra proibida, promessa, número fora da Ficha, sigla, 2ª pessoa na capa.

### 5.9 Veredito interno (não mostrar)
Padrões ativos (≥ 1) · gatilhos (≥ 2) · anti-padrões · formato (dois-pontos / 3 frases) · evidência (ids) · ética. Reprovada é reescrita.

### 5.12 Versão de capa
1. Headline inteira se couber no formato. 2. Senão, versão curta **mantendo o padrão** (dois-pontos continua dois-pontos, pergunta continua pergunta). 3. Narrativa na capa: frase 1 + frase 3 encurtadas; a 2 abre o slide 2. 4. Nunca virar declaração genérica. 5. Destaque em até 3 palavras. 6. Capa chamativa (dúvida, curiosidade, alerta) desde que o carrossel entregue o que promete. Número na capa nunca solto: diga o que ele conta. O `chefe-de-pauta` entrega a versão de capa das 3 melhores junto com as 10.

---

## 6. Espinha dorsal
Uma linha por slide, seguindo o arco (tabela 4.2): slide · função · passo do arco · conteúdo · ids. Marque **(analogia)** na linha do mecanismo. Na Tese, o slide 3 traz um fato que contradiz a crença e o 5 traz os números, sem repetir.

## 7. Encaixe por formato
### 7.1 Anatomia (9 slides; o `funcao` de cada slide)
| Função | M5 | M1 | M2 | M3 | M4 |
|---|---|---|---|---|---|
| capa | capa | capa | capa2 | capa (ou capa2) | capa (ou capa2) |
| hook | dark | texto | topico 01 | manchete | busca |
| mecanismo | light | texto | topico 02 | foto | lateral |
| mecanismo | dark | texto | topico 03 | manchete | texto |
| prova | light | texto | topico 04 | foto | vidro |
| expansao | dark | texto | topico 05 | manchete | lateral |
| aplicacao | light | texto | topico 06 | manchete | texto |
| direcao | grad | texto | resumo | foto | janela |
| cta | cta | cta | cta | cta | pergunta |

### 7.2 Metas de palavras
Até 2 blocos por slide (o 1º contextualiza, o 2º aprofunda), 18 a 34 palavras por bloco; slide escuro ≤ 80 palavras, claro ≤ 100. Em M1–M4, mandam os limites de caracteres do campo (tabela `LIMITES` do `render_carrossel.py`).

### 7.8 Marcação (não misturar)
M1 `**negrito**` `==destaque==` `_itálico_` `<br>` · M2 `**` `==degradê==` `_itálico_` `~~sublinhado~~` `{{caixa}}` `\n` · M3 `**pesado**` `_leve_` `{{tarja}}` `<br>` · M4 `**` `==degradê==` `_itálico_` `!!marca-texto!!` `<small>` `<br>` · M5 `**negrito**` `*destaque*` `<br>`. Destaque em até 3 palavras por slide.

---

## 8. Regras de copy
1. Uma ideia por slide; informação nova; termina abrindo a próxima pergunta, sem anunciar.
2. Artigo em todo substantivo; frase com verbo; conectivos naturais (porque, só que, por isso, enquanto, quando, mas, então). Duas frases curtas valem mais que uma longa com vírgulas.
3. Densidade: cada bloco tem uma âncora concreta (número da Ficha, mecanismo específico, analogia). Teste da substituição: se o bloco funciona trocando "agachamento" por "corrida", está genérico.
4. O slide 2 conversa com a capa; tudo o que a capa promete é cumprido antes da direção.
5. Fechamento com virada genuína: nada de resumo ("em resumo…"), cena cinematográfica ou pergunta retórica sem resposta.
6. Passou do limite: sintetize a ideia; nunca corte artigo ou conectivo.

### 8.1 Trocas típicas (técnico → leigo)
| Técnico | Leigo |
|---|---|
| hipertrofia (para público iniciante) | ganho de músculo |
| RIR / repetições em reserva | repetições que ainda sobravam |
| RPE / percepção de esforço | o quanto a série pareceu pesada, de 0 a 10 |
| 1RM | o peso máximo para uma repetição |
| falha concêntrica | até não conseguir mais nenhuma repetição |
| fase excêntrica / concêntrica | a descida / a subida do movimento |
| isometria | segurar parado na posição |
| síntese proteica | a construção de músculo |
| sarcopenia | a perda de músculo com a idade |
| VO2 máximo | o fôlego máximo do corpo |
| HIIT | treino intervalado (tiros fortes com pausa) |
| DOMS | a dor muscular dos dias seguintes |
| meta-análise / revisão sistemática | um estudo que juntou N estudos |
| ensaio randomizado | um teste em que metade fez X e metade não |
| placebo | um grupo que achava que fazia X, mas não fazia |
| % | o comparativo simples ("o dobro", "1 em cada 4") |

## 9. Anti-slop (o validador bloqueia a maior parte)
- Estruturas binárias: "não é X, é Y" · "não é sobre X, é sobre Y" · "deixa de ser X para ser Y" · "Menos X. Mais Y." · "Sem X. Sem Y." · "Antes: X. Agora: Y." · "Y, não X".
- Cacoetes: "e isso muda tudo", "no fim das contas", "ao final do dia", "a pergunta que fica", "a questão é:", "o ponto é:", "o mecanismo funciona assim", "em um mundo onde", "vivemos em uma era", "cada vez mais", "simplesmente", "basicamente", "de forma X", "é claro que".
- Dados vagos: "estudos mostram", "especialistas dizem", "a maioria das pessoas", "recentemente". Nomeie a fonte e dê o número.
- Anglicismo numérico: "5x", "10+", "2-3 séries" → "cinco vezes", "mais de 10", "duas ou três séries".
- Aberturas e fechos de slide: "hoje vamos falar", "neste carrossel", "arraste para o lado", "mas tem mais". CTA cordial: "espero que tenha gostado", "obrigado por", "não esqueça de seguir".
- Bordões de academia e coach: "sem desculpas", "no pain no gain", "foco, força e fé", "é preciso", "você deve".
- Jargão: ecossistema, sinergia, mindset, storytelling, shape, benchmark.

## 10. Validação editorial (editor-de-texto)
### 10.1 Os 7 parâmetros (nota por slide; mínimo 8 em cada)
Gramática · Fluidez · AI Slop · Fatos verificados · Estrutura · Densidade · Tom editorial. Detalhe e tetos no agente `editor-de-texto`. Texto só vai para aprovação com todos ≥ 8 (ou com a pendência aceita pelo Jorge).
### 10.2 Os 5 testes
Jornal (soaria natural num jornal brasileiro?) · Substituição · Promessa (a capa foi cumprida?) · Artigo · Binário. Mais: Fechamento (virada, não resumo), Leigo, Ética (CONFEF + nutrição).
### 10.4 Tabela QA
Formato exato no agente `editor-de-texto`.

## 11. CTA pelo conteúdo
| Conteúdo | `cta.tipo` | Texto (adaptar ao tema) |
|---|---|---|
| Qualquer tema (padrão) | `consultoria` | "Quer um treino para a sua rotina? Treino individualizado com Jorge Souto, treinador, CREF … · link na bio" (nome + CREF do `Gerador/marca.json`) |
| Material próprio do Jorge (se existir) | `ebook` | "<nome do material> · link na bio" |
Regras: um só, diretivo, sem agradecimento, sem preço, sem promessa de resultado. A **frase-ponte** é obrigatória: fecha o raciocínio com virada e liga ao CTA. "Salvar" e "Comenta PALAVRA" não são o padrão (o validador avisa).

## 12. Aprovação do texto
Formato exato no agente `redator-de-carrossel` ("TEXTO FINAL — revisão antes das artes"): tipo, formato, funil, CTA, headline completa e de capa, cada slide com função e campos, QA editorial e linha do validador. Fecho: "Revisa o texto de cada slide. Quando estiver tudo ok, digita 'aprovado' e eu parto para as artes."

## 13. Legenda (legendista)
Gancho (até 125 caracteres) · contexto (2–3 frases) · análise (2–3 frases) · Fontes (copiadas da seção `## Fontes` que o script montou) · CTA (o mesmo do slide) · 5 a 12 hashtags específicas. Linguagem leiga, sem 2ª pessoa fora do CTA, mesma ética dos slides.
