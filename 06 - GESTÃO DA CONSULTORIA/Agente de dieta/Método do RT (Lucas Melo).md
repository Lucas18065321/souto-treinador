---
tipo: metodo-de-prescricao
atualizada: 2026-10-27
origem: método do RT (entrevista de 2026-10-23), diretrizes clínicas do RT, contrato do plano.json e ficha "Gordura corporal sem dobra cutânea" (2026-10-23)
adaptado: 2026-11-19, para a consultoria Souto Treinador (o RT assina a dieta)
---
# Método do RT (Lucas Melo) para prescrever a dieta

O método clínico do nutricionista **Lucas Melo (CRN6 - 50479-P)**, Responsável Técnico (RT) pela parte de dieta da consultoria Souto Treinador. A prescrição dietética é ato privativo do nutricionista (Lei 8.234/1991): o Jorge (educador físico) acompanha o treino e a rotina, e **toda dieta sai só com a aprovação do RT** (etapa APROVAÇÃO DO RT no Painel ST).

O que o `/montar-dieta` segue. **O agente propõe e o RT decide**: nada sai sem a aprovação dele, e cada regra nova que ele der numa sessão entra aqui, com data. Marcas: **RT** = regra do RT · **Diretrizes** = diretrizes clínicas do RT (documento dele, fora deste repositório) · **proposta** = ponto de partida do Claude, a confirmar.

## 1. Gasto do dia
- **Equação:** Mifflin-St Jeor × fator de atividade, para todos. Foi a mais confiável na revisão das equações (Diretrizes 2.4, fonte [6], moderada). Harris-Benedict, que o RT usava, aparece só para comparar. Fórmulas com massa magra (Katch, Cunningham) ficam fora: pedem dobra ou bioimpedância, e o atendimento é online. **RT + Diretrizes, 2026-10-23.**
- **Fator de atividade sempre conservador.** O aluno superestima o próprio esforço. Leia a jornada (T11) e o treino (T21) e, na dúvida entre dois degraus, fique com o menor. **RT.** Degraus de partida (**proposta**):
  | Rotina | Fator |
  |---|---|
  | trabalho sentado, sem treino | 1,2 |
  | trabalho sentado + treino 2 a 3 vezes, ou trabalho em pé sem treino | 1,375 |
  | trabalho sentado + treino 4 a 5 vezes, ou em pé + treino 3 vezes | 1,55 |
  | trabalho braçal + treino quase todo dia | 1,725 (raro) |
- **Peso usado:** o de tendência (média das duas últimas pesagens semanais, Diretrizes 2.9).
- **Do 2º plano em diante:** com 4 semanas ou mais de check-in, fora das semanas 1 e 2, o agente mostra o GET calibrado pelo peso (Diretrizes 2.5) ao lado da fórmula. É ele que corrige quem superestima o esforço.

## 2. Gordura corporal (sem dobra, atendimento online)
O déficit e a proteína dependem dela. O agente estima uma **faixa** (muito baixa · baixa · média · alta · muito alta), nunca um número, juntando:
1. as fotos mais recentes (check-in: frente, lados e costas; anamnese E12 no emagrecimento);
2. o IMC, a cintura em relação à altura e o RFM;
3. a história (objetivo, treino, peso máximo e mínimo).

Ele mostra a leitura ao RT, que confirma. **RT, 2026-10-23.**

**Como pesar cada sinal** (`Gordura corporal sem dobra cutânea - Ficha`). Quase tudo tem certeza muito baixa, e os estudos medem só a concordância com o DXA, sem desfecho de saúde.
- **O IMC só empurra para cima.**
  - IMC ≥ 30 quase nunca é alarme falso (especificidade de 95 a 97%, certeza moderada, #2).
  - Acima de 40, o excesso de gordura pode ser presumido (consenso do Lancet 2025, #13).
  - Abaixo de 30, não descarta gordura alta: deixou passar cerca de metade de quem tinha excesso (#1). IMC normal nunca baixa a faixa sozinho.
- **A cintura confirma.**
  - O consenso do Lancet (#13) e a diretriz brasileira de 2025 (#14) pedem somar ao IMC ao menos uma medida de cintura. Nenhuma provou ser melhor que as outras (#4).
  - Num estudo de 81 adultos, cintura/altura a partir de 0,53 (homem) e 0,54 (mulher) indicou gordura de obesidade (#5).
  - O corte de 0,5 não está validado na base.
- **RFM** = 64 − (20 × altura ÷ cintura), mais 12 se for mulher, em % de gordura.
  - Nos EUA, o desvio mediano contra o DXA ficou abaixo de 1 ponto; o do IMC foi de 10,9 pontos para menos nas mulheres (#6). No México, o erro caiu pela metade em relação ao IMC (#8).
  - Deu mais alarme falso nas mulheres (#7).
  - Não foi validado em brasileiros, atletas, asiáticos nem crianças.
  - **Proposta:** o agente calcula e mostra só ao RT, como mais um sinal. Não entra no PDF.
- **Foto.** Os estudos de IA testaram 2 aplicativos próprios, com 1 estudo cada, um deles patrocinado. O erro médio foi de cerca de 2 pontos, e chegou a cerca de 5 numa pessoa (#10, #11). Isso **não** vale para a leitura das fotos pelo agente.
- **Até o DXA erra:** no México, ele leu mais gordura que outros 3 métodos (#9).
- **Sinais em conflito** (a foto aponta uma faixa e as medidas, outra): o agente mostra a discordância ao RT e não escolhe sozinho. **Proposta.**

**Lacuna:** a estimativa visual por profissional, olhando a pessoa ou as fotos, não está processada. A única fonte achada é o Eckerson 1992 (2 avaliadores experientes contra a pesagem hidrostática), que é pago e aguarda o PDF na `01 - BASE CIENTÍFICA/ENTRADA/`. A leitura das fotos segue como juízo clínico do RT. **Base, 2026-10-23.**

## 3. Calorias e fase
| Situação | Fase e déficit |
|---|---|
| padrão | déficit de 500 kcal/dia |
| gordura alta ou muito alta | déficit maior, até 700 |
| quer perder pouca gordura e "definir" | manutenção ou déficit de 300, com proteína mais alta |

**RT, 2026-10-23.** kcal arredondadas de 50 em 50.
- **Teto:** déficit acima de 750 kcal/dia (500 com treino, Diretrizes 3.4 e 7.3) **só com o ok do RT**, mesmo com gordura alta.
- **Mudar a fase** (déficit, manutenção, pausa, superávit): o agente pode propor e já montar assim, desde que os check-ins estejam em dia, a mudança tenha coerência clínica e caiba nas Diretrizes. **Sempre em destaque** para o RT ("mudei a fase porque..."). Pausa: 1 a 2 semanas em manutenção (Diretrizes 3.5).
- Abaixo de 1.200 kcal (mulher) ou 1.500 (homem): aviso. Abaixo de 800: trava, só com justificativa escrita do RT (contrato 1.7.4).

## 4. Macros
- **Proteína, em g/kg do peso atual, pela gordura corporal:** quanto mais gordura, menos proteína por kg. Vai de 2,2 g/kg em quem tem gordura bem baixa até cerca de 1,0 g/kg em quem tem gordura muito alta. Em quem quer "definir", fica mais alta. **RT, 2026-10-23.** Pontos de partida (**proposta**):
  | Gordura | g/kg |
  |---|---|
  | muito baixa | 2,0 a 2,2 |
  | baixa | 1,8 a 2,0 |
  | média | 1,6 a 1,8 |
  | alta | 1,2 a 1,6 |
  | muito alta | 1,0 a 1,2 |

  Com treino e abaixo de 1,6 g/kg, a conferência dá **aviso** (Diretrizes 4.7). Com gordura alta, isso é esperado: o agente explica e segue.
- **Gordura:** 0,8 a 1,0 g/kg. **RT, 2026-10-23.**
- **Saturada:** até 10% das kcal, sempre. Mais baixa quando a condição pede: na dislipidemia, menos de 7% (SBC 2025, `Dislipidemia - Ficha`). No JSON, `plano.limite_saturada_pct`. **RT.**
- **Carboidrato:** fecha as calorias.
- **Fibra:** 15 g por 1.000 kcal (`plano.fibra_g_por_1000kcal`). **RT.**
  - Na linha gastro, a meta depende da fase da doença (Diretrizes 5.7: padrão SOLTO → não aumentar fibra, como sugestão).
  - **Plano que sobe a fibra avisa o aluno** (no PDF, em `plano.avisos`): no começo, o desconforto e os gases podem aumentar; não é sinal de inflamação, é a fibra, e até o prazo que o RT define é esperado; se a dor piorar a ponto de ficar insuportável, chamar o RT na hora. **RT, 2026-10-27.**
  - SII com SIBO em fase 1 do low FODMAP (1º caso, 2026-10-27): 17 g por 1.000 kcal, com prioridade para a fibra solúvel e sem farelo de trigo. A base não tem número por 1.000 kcal (a BSG cita 20 a 30 g/dia, sem dizer se é total). **RT.**
  - O RT quer ver quanto dessa fibra é solúvel e quanto é insolúvel. A TACO só traz a fibra total. **Lacuna:** falta fonte com a divisão, então o agente equilibra as fontes no cardápio sem pôr número de solúvel e insolúvel no PDF.
- Quando o RT quiser outra distribuição, o agente pergunta: "quer algo mais específico ou sigo o que sugeri pela anamnese e pelas fotos?"

## 5. Cardápio
- **Tabelas:** TACO 4ª ed. como base, e TBCA para o que faltar. O RT informa que a nova resolução do CFN libera o uso da TBCA por profissionais (2026-10-23; fonte a anexar). Produtos de marca entram pelo rótulo, com data. Tudo vai para `alimentos/alimentos.json` com a fonte: o agente nunca põe número de cabeça.
  - O RT pediu o banco de marcas completo (2026-10-23):
    - Rap10, whey em caixinha, Magic Toast, biscoito e farinha de arroz, leite condensado;
    - os sem lactose e os sem glúten mais fáceis de achar;
    - pastas de amendoim (Dr. Peanut, Vitapower), VidaVeg e veganos nacionais;
    - laticínios e iogurtes "triplo zero", nacionais e regionais.
  - Açaí: as marcas de todas as capitais que vendem ao consumidor final, por delivery ou no supermercado (pote até 5 L). As cidades ficam em `obs`. **RT.**
- **Peso do alimento pronto**, com o preparo escrito:
  - métodos: airfryer, cozido, assado ou grelhado;
  - para untar, só azeite ou óleo vegetal (melhor que manteiga: trocar gordura saturada por insaturada pode ajudar a baixar o colesterol, `Dislipidemia - Ficha` #2);
  - legumes sempre no vapor. **RT.**
- **3 a 4 opções de proteína e de carboidrato por refeição**, de acordo com a região, a estação e a cultura do aluno (cidade na ficha e na anamnese T9). Cuscuz é sempre opção ao arroz: mesma quantidade de carboidrato e kcal por grama muito parecidas. Para o nordestino, cuscuz é ótimo; para o sulista, talvez não. **RT.**
- **Harmonia do prato**, sempre.
- **Legumes e folhas no almoço e no jantar:** no mínimo 150 a 250 g, cada um especificado (rúcula, couve, cenoura, acelga, abobrinha, chuchu...). Nunca "salada livre". O PDF lembra como higienizar as folhas cruas. **RT.**
- **Densidade calórica baixa para quem quer emagrecer.** Se o aluno precisa de doce no dia a dia (pergunta nova da anamnese), um ou os dois lanches podem ser doces e de baixíssima densidade calórica. Exemplo: "sorvete" de morango com leite em pó (ou whey de morango, conforme o objetivo) e gelatina em pó hidratada; bata tudo e depois aere na batedeira, ou com o fuê por 10 minutos, até ficar com consistência de sorvete. **RT.**
- **Receitas:** o agente pode propor receitas para os lanches, e o RT guarda as dele no portfólio (banco Modelos, tipo Receita), que o agente reaproveita para variar. Café da manhã, almoço e jantar seguem o padrão. Receita usada no plano vira item `receita:` no banco de alimentos, com kcal por 100 g calculada pelos ingredientes.

## 6. Refeição livre
- **Decidida por aluno. RT, 2026-10-23.**
- **Gastro sensível:** não tem.
- **Emagrecimento:** entra se o aluno sente necessidade (anamnese), sem contraindicação e numa porção realista que o ajude a manter o resto da semana. A quantidade é especificada: "3 fatias de pizza no sábado (cerca de 900 kcal)", não "pizza à vontade".
- **Diluída no déficit da semana.** O agente monta os dias comuns um pouco abaixo, para a média da semana fechar no alvo. Conta exata: dias comuns = alvo − (kcal da livre − kcal da refeição que ela substitui) ÷ 7.
  - Exemplo: livre de 900 kcal no lugar de um jantar de 450, déficit de 500. Os dias comuns ficam cerca de 64 kcal mais baixos, e a semana fecha nos 500 de déficit.
  - **Vale a conta exata. RT, 2026-10-23.** A conta antiga dele (900 ÷ 6 = 150 a menos por dia) deixava a semana com cerca de 86 kcal/dia de déficit além do combinado.

- **Livre "de bebida" a cada 15 dias** (1º caso, 2026-11-15): até 3 cervejas com petisco magro (grelhado, cozido ou assado, sem fritura). No dia, faz café, almoço e jantar normalmente, sem passar o dia só beliscando e bebendo, e tira só os lanches da manhã e da tarde. No JSON: `livre_por_semana: 0.5` (o PDF escreve "1 a cada 15 dias"), `livre_substitui` = uma das refeições do check-in para a conta e `livre_substitui_texto` para o que o aluno lê. **RT.**

## 7. Suplementação
O agente **sugere com motivo** (exame baixo, treino, intestino), com a dose e a fonte da base, e o RT decide. O que o aluno já usa (anamnese T12) aparece para manter, ajustar ou suspender. **RT, 2026-10-23.**
- Intolerante à lactose: suplemento sem lactose entre os excipientes (ex.: B12 sublingual), escrito nos cuidados do item. **RT, 2026-10-27.**

## 8. O que o agente nunca faz sozinho
- **Cortar grupo alimentar** sem alergia ou intolerância registrada, ou sem ordem do RT.
- **Passar do teto de déficit** (seção 3).
- **Mudar a fase sem avisar** (pode propor; seção 3).
- **Dieta de exclusão:** pode propor quando couber, dentro das travas das Diretrizes 5.9 (low FODMAP em 3 fases; na DII, só em remissão; rastrear comer transtornado antes). Sempre com a nota no contexto do aluno. Na reavaliação, com melhora estável de 15 a 30 dias sem crise e sem dor aguda, monta-se um diário alimentar com rodízio semanal para mapear a tolerância. **RT, 2026-10-23.** O material do rodízio e o check-in próprio dele ainda não existem.

## 9. Textos do PDF
- **"Como foi o último mês"** (da v2 em diante): o agente rascunha a partir dos check-ins e do Diário, em linguagem leiga, sem culpa e com números simples, e o RT aprova junto com o plano. No 1º plano entra "Como usar o seu plano". **RT, 2026-10-23.**
- **Água:** a fórmula (mL por kg) é escolhida pelo RT no 1º plano de cada aluno e repetida nos seguintes (`agua_ml_por_kg`).
