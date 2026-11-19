---
name: "treino"
description: "Prescreve e acompanha o treino de força de um aluno do Jorge Souto (SOUTO TREINADOR): anamnese de treino, 1RM estimado, objetivo e nível, escolha do modelo de periodização (linear, ondulatória, blocos), mesociclo com rampa de volume e deload, ficha de treino em PDF na identidade azul e acompanhamento semanal (registro de cargas + check-in → PROGREDIR / MANTER / REDUZIR VOLUME / DELOAD). Cada decisão cita a linha do Protocolo 'Hipertrofia e força'. Não prescreve dieta (encaminha ao nutricionista RT). Use quando o Jorge digitar /treino, pedir ficha de treino, montar ou ajustar treino, calcular carga ou 1RM, ver o volume da semana ou decidir a progressão de um aluno."
argument-hint: "<nome do aluno> [novo | semana N | ficha]"
---

# /treino: frente 05 - TREINO

> Caminhos relativos à **raiz do repositório**. Manual da pasta: `05 - TREINO/CLAUDE.md`. Guia para humanos: `docs/guias/06-treino.md`.
> Evidência: `01 - BASE CIENTÍFICA/Treino de força/Hipertrofia e força - Protocolo.md` (códigos `[A1]`… `[E4]`). Conteúdo público sai da Ficha, nunca daqui.
> Scripts (só biblioteca padrão; rode da raiz):
> - `MOTOR` = `python "05 - TREINO/calcular_treino.py"` → `1rm`, `tabela`, `volume`, `decidir`, `mesociclo`, `regras`
> - `FICHA` = `python "05 - TREINO/montar_ficha.py"` → HTML + PDF A4 (Chrome sem janela; **um render por vez**)
> - `BANCO` = `python "05 - TREINO/treino_supabase.py"` → `prescricao`, `registro`, `baixar`, `saude` (conferência por padrão; `--enviar` só com ⏸)
> **Princípios:** o script calcula (0 token); o agente `prescritor-de-treino` (Sonnet) interpreta e redige, sempre citando a linha do Protocolo. Dados do aluno só em `%USERPROFILE%\SoutoTreinador\Alunos\<nome>\Treinos\` (LGPD), nunca no repositório. Toda proposta é **proposta**: o Jorge aprova (⏸) antes de virar ficha ou ir ao banco.
> **Nunca:** prescrever dieta, suplemento ou dose (→ nutricionista RT); prometer resultado; tratar estimativa de 1RM como medida; seguir com progressão quando houver dor ≥5/10 ou lesão nova (`[E1]`).

## 0. Qual caminho
- Aluno novo ou ciclo novo → passos 1 a 6.
- "Semana N" / chegou check-in de cargas → passo 7.
- Só refazer o PDF → passo 6.
- Pergunta solta de carga ("quanto ponho no supino se fiz 80×6?") → `MOTOR 1rm` / `MOTOR tabela` e responda com o aviso de estimativa.

## 1. Anamnese de treino
Pasta do aluno: `%USERPROFILE%\SoutoTreinador\Alunos\<nome>\Treinos\` (crie se faltar). Se a anamnese veio pelo Tally, ela está no Supabase (`recebidos` tipo `anamnese_treino`) ou no Painel ST: peça ao Jorge o resumo ou a exportação, não invente.
Pergunte só o que falta, em uma mensagem: objetivo (hipertrofia/força), experiência (anos de treino regular), dias e tempo por sessão, local e equipamentos, exercícios que não pode ou não gosta, dor/lesão/doença/remédio, sono e rotina.
**Triagem `[E1]`–`[E2]`:** dor que piora, lesão recente, sintoma cardiovascular ou doença não controlada → pare e oriente encaminhamento antes de prescrever. Dúvida de alimentação → nutricionista RT (`[E3]`).

## 2. Avaliação (1RM estimado) `[A1]`–`[A4]`
- Para cada exercício principal: carga × repetições até perto da falha (3 a 10) + RIR. `MOTOR 1rm --carga 100 --reps 8 --rir 2 [--tabela supino|legpress]`.
- Mostre ao Jorge: 1RM estimado (tabela de Nuzzo 2024), a faixa entre pessoas e Epley/Brzycki como conferência. Diga que é estimativa de grupo (`[A1]`, `[A2]`).
- Nível: iniciante (<1 ano) / intermediário / avançado (`[A3]`; os cortes acima de 1 ano são operacionais). Iniciante: o RIR é só anotado (`[A4]`).
- Monte `aluno.json` na pasta do aluno, no formato de `05 - TREINO/exemplo/aluno-exemplo.json` (aluno, testes, exercicios com grupo/secundarios/tabela/principal/incremento_kg/obs, divisao A–F, nomes_dias, volume_inicial opcional, check_in_cargas_url).

## 3. Objetivo e nível → volume e intensidade
Resuma em 5 linhas com os códigos: séries/grupo/semana de partida e teto (`[V1]`–`[V4]`), faixa de repetições e RIR (`[I1]`–`[I5]`), frequência e descanso (`[F1]`, `[F2]`).

## 4. Modelo de periodização ⏸ Jorge
Ofereça as 3 opções com o "quando escolher" do Protocolo (`[Z1]` linear, `[Z2]` ondulatória, `[Z3]` blocos; `[Z4]` autorregulação vale em qualquer um; `[Z5]` periodizar não é superior com sobrecarga progressiva: escolha pela adesão e pelo objetivo). **Espere o Jorge escolher** modelo e número de semanas (padrão 6, com deload na última, `[D1]`).

## 5. Mesociclo
`MOTOR mesociclo --aluno "<pasta>/aluno.json" --modelo <linear|ondulatoria|blocos> --semanas 6 --inicio AAAA-MM-DD`
Grava `mesociclo-<modelo>-<data>.json` na pasta do aluno. Leia a saída: tabela de séries por grupo por semana, semana 1 com cargas e os **AVISOS** (ex.: grupo que não cabe em um exercício só → sugira acrescentar exercício). Peça ao `prescritor-de-treino` a revisão (coerência com o Protocolo, exercícios, observações de técnica). Ajustes de exercício: edite o `aluno.json` e gere de novo.

## 6. Ficha PDF ⏸
`FICHA --plano "<mesociclo.json>" --semana 1` (com acompanhamento: `--registro <registro> --checkin <checkin> --decisao-semana N`). Sai HTML + PDF na pasta do aluno. Abra o PDF, confira com o Jorge (nome, cargas, observações, link do check-in de cargas: troque `https://tally.so/r/TROCAR` no `aluno.json`). **Envio ao aluno e gravação no banco só com o "sim" do Jorge** (`BANCO prescricao --plano ... --aluno-id <uuid>` mostra o que vai; `--enviar` grava).

## 7. Acompanhamento semanal ⏸
1. **Dados:** registro de cargas e check-in da semana. Vindo do Tally/Supabase: `BANCO baixar --aluno-id <uuid> --plano <mesociclo.json> --saida "<pasta do aluno>"` (gera `registro-supabase.json` e `checkin-supabase.json`). Vindo de planilha: CSV `semana,data,dia,exercicio,serie,carga,reps,rir`.
2. **Volume:** `MOTOR volume --registro <registro> --plano <mesociclo.json>` (séries por grupo, volume load e 1RM estimado por semana; `[M1]`, `[M2]`).
3. **Decisão:** `MOTOR decidir --plano <mesociclo.json> --registro <registro> --checkin <checkin> --semana N --semana-plano N --saida "<pasta>/decisao-semN.json"`.
4. **Alertas primeiro:** dor ≥5/10 ou lesão nova (`[E1]`) → fale disso antes de qualquer progressão.
5. Mande a decisão ao `prescritor-de-treino` para virar proposta em linguagem do Jorge: por exercício, PROGREDIR / MANTER / REDUZIR VOLUME / DELOAD + a linha do Protocolo + o que muda na próxima semana. **⏸ o Jorge aprova, edita ou recusa.**
6. Aprovado: atualize o `aluno.json`/mesociclo se a carga ou as séries mudaram e refaça a ficha (passo 6) com o painel (`--registro --checkin --decisao-semana N`). Banco: `BANCO registro ... --decisao <decisao.json>` (conferência; `--enviar` com ⏸).

## Regras de resposta
- Toda decisão: **verbo + código do Protocolo + motivo em uma linha** (ex.: "REDUZIR VOLUME na remada: 1RM estimado caiu 9% em 2 semanas e RIR 0 abaixo do alvo 2 → `[P3]`").
- Limiares marcados "operacional" no Protocolo são regra do sistema, não ciência: diga isso se o Jorge perguntar "por que 2%?".
- Sem fonte no Protocolo para algo que o Jorge pediu → "não temos isso processado" e ofereça `/montar-condicao`.
- Nada de dado de aluno em conteúdo público (CONFEF; LGPD).
