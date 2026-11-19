# Frente 05: Treino (prescrição e volume × desempenho)

Motor de prescrição de treino de força do Jorge Souto. Calcula 1RM estimado, tabela de cargas, volume semanal (séries por grupo e volume load), decide a progressão (PROGREDIR / MANTER / REDUZIR VOLUME / DELOAD) e monta a ficha de treino em PDF na identidade azul. **Toda regra tem uma linha no Protocolo** `01 - BASE CIENTÍFICA/Treino de força/Hipertrofia e força - Protocolo.md` (códigos `[A1]`…`[E4]`).

## Arquivos
```
calcular_treino.py   motor (só biblioteca padrão): 1rm · tabela · volume · decidir · mesociclo · regras
montar_ficha.py      ficha HTML + PDF A4 (Chrome sem janela): capa, plano da semana, mesociclo/regras, painel de volume, decisão
treino_supabase.py   ponte com o banco (06 - GESTÃO DA CONSULTORIA/supabase): prescricao · registro · baixar · saude
exemplo/             aluno FICTÍCIO: aluno-exemplo.json, mesociclo-exemplo.json, registro-cargas-exemplo.json/.csv,
                     checkin-exemplo.json, checkin-cansado-exemplo.json
```
Comando do Claude: `/treino` (skill em `.claude/skills/treino/`). Agente: `prescritor-de-treino` (`.claude/agents/05-treino/`). Guia para humanos: `docs/guias/06-treino.md`.

## Regras da pasta
- **Dados de aluno nunca aqui.** Tudo de aluno real vai para `%USERPROFILE%\SoutoTreinador\Alunos\<nome>\Treinos\` (LGPD). Em `exemplo/` só o aluno fictício.
- **Mudou um número do motor?** Ele mora no bloco `REGRAS` de `calcular_treino.py` e na linha correspondente do Protocolo: mude os dois e a data do Protocolo.
- Limiar "operacional" = regra do sistema, sem fonte direta (está nas Lacunas do Protocolo). Nunca vira afirmação de conteúdo.
- Tabela repetições × %1RM: só os pontos escritos no texto de Nuzzo 2024 (geral, supino, leg press); abaixo de 70% 1RM é extrapolação e o motor avisa. Epley/Brzycki são só conferência.
- **Um render de PDF por vez** (pouca RAM). Banco: conferência por padrão; `--enviar` só com o "sim" do Jorge.
- Dieta não entra: dúvida de alimentação vai para o nutricionista RT.

## Contrato de dados (JSON)
- `aluno.json`: `aluno{nome,nivel,objetivo,...}`, `testes[{exercicio,carga,reps,rir}]`, `exercicios[{nome,grupo,secundarios,tabela,principal,isolado,incremento_kg,obs}]`, `divisao{A..F:[nomes]}`, `nomes_dias`, `volume_inicial{grupo:séries}`, `check_in_cargas_url`.
- `mesociclo.json` (saída do motor): `semanas[{semana,inicio,tipo,fase,series_por_grupo,sessoes{A:[{exercicio,series,reps,reps_min,reps_max,rir,pct_1rm,carga_kg,descanso_s,obs}]}}]`, `exercicios`, `avisos`.
- Registro de cargas: `{"sessoes":[{semana,data,dia,exercicios:[{nome,series:[{carga,reps,rir}]}]}]}` ou CSV `semana,data,dia,exercicio,serie,carga,reps,rir`.
- Check-in: `{"semanas":[{semana,sono,fadiga,dor_muscular,estresse,esforco,dor_treino,dor_local,lesao_nova}]}` (0–10).
- Mapeamento no Supabase: ver o cabeçalho de `treino_supabase.py` (RIR vai em `sessoes.observacao`; até 6 séries por exercício em `series`).
