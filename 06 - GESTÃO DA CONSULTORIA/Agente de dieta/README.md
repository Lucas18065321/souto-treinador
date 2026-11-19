---
tipo: manual
atualizada: 2026-11-19
---
# Agente de dieta

Tudo o que o `/montar-dieta` (`.claude/skills/montar-dieta/SKILL.md`) usa para montar a nova versão do plano alimentar de um aluno e gravá-la no Supabase.

> **Prescrição dietética é ato privativo do nutricionista** (Lei 8.234/1991). Na consultoria Souto Treinador, o **Responsável Técnico (RT) pela dieta é o nutricionista Lucas Melo (CRN6 - 50479-P)**. O agente monta a proposta no método dele (`Método do RT (Lucas Melo).md`), o Jorge revisa, e **o plano só pode ser enviado depois da APROVAÇÃO DO RT** no Painel ST. O PDF leva a marca e o rodapé do Jorge e termina com o bloco "Prescrição dietética" + a assinatura do RT.

## Arquivos
| Arquivo | O que é |
|---|---|
| `Método do RT (Lucas Melo).md` | as regras de prescrição do RT (gasto, gordura corporal, déficit, macros, cardápio, refeição livre, suplementos, o que nunca fazer sozinho) |
| `dieta_supabase.py` | `pacote`: lê o aluno do Supabase · `salvar`: grava Dieta, Refeições, Suplementos, Relatório de abertura e a Entrega em RASCUNHO, com o PDF no bucket privado |
| `calcular_plano.py` | `energia`: gasto e macros · `conferir`: calcula cada alimento e confere o plano |
| `alimentos.py` · `alimentos/` | banco de alimentos por 100 g: TACO 4ª ed. (planilha oficial em `alimentos/taco_4ed.xlsx`, 597 itens), TBCA 7.3 (42, pelo comando `tbca`), rótulos oficiais de marca (296) e receitas do RT (15). Em `alimentos/Marcas sem tabela pública.md`, o que foi procurado e ficou de fora |
| `template/` | o PDF da marca (`montar_plano.py`, modelos A e B) |
| `receituario/` | a receita de manipulação (prescritor: o RT) |

Configuração comum (marca, CREF, @, RT, pastas): `../config-st.json`. Código comum: `../comum/` (`config_st.py` e o cliente do Supabase `supabase_st.py`, só com a biblioteca padrão do Python).

## Onde ficam os dados do aluno
**Dado de aluno nunca entra nesta pasta nem no repositório.** O pacote, o JSON e o PDF de cada aluno ficam em `%USERPROFILE%\SoutoTreinador\Alunos\<nome do aluno>` (fora do OneDrive e do GitHub). No Supabase, o PDF e o JSON vão para o bucket **privado** `entregas`, em `alunos/<id do aluno>/`.

## O fluxo, de ponta a ponta
1. `python dieta_supabase.py pacote "Ana Exemplo"` (ou `AL-1`): grava `pacote.json` na pasta do aluno, com `documento` e `evolucao` prontos para o PDF.
2. Números e cardápio, com o Claude, no método do RT (paradas ⏸ para decidir).
3. `python calcular_plano.py conferir "<json>" --gravar` até zerar os erros.
4. `python template/montar_plano.py "<json>"`: PDF e HTML na pasta do aluno (com a assinatura do RT, se a imagem estiver na pasta privada).
5. `python dieta_supabase.py salvar "<json>"`: confere de novo, sobe o PDF e o JSON, guarda a impressão digital (SHA-256) do PDF e cria a Entrega em **RASCUNHO**.
6. No **Painel ST → Aprovações**: o Jorge revisa ("Revisado: mandar para o RT") → **APROVAÇÃO DO RT** → o RT aprova ("Aprovar como RT", com PIN se configurado) ou devolve com nota → **ENVIAR** → WhatsApp + PDF → **ENVIADO** (a dieta em uso do aluno troca sozinha).
   - O banco trava: dieta sem aprovação do RT não vai para ENVIAR. Se o PDF mudar depois da aprovação, a entrega volta para o RT.

## Campos que o fluxo acrescenta ao `plano.json`
- **Em cada item, base ou equivalente:** `ref`, o id do banco de alimentos (`taco:410`, `tbca:...`, `marca:...`, `receita:...`). O `conferir --gravar` escreve `kcal`, `proteina_g`, `carboidrato_g`, `gordura_g`, `fibra_g` e `saturada_g` de cada item, e os totais de cada refeição.
- **No `plano`:** `aluno_id` (AL-n), `fibra_g_por_1000kcal` (padrão 15) e `limite_saturada_pct` (padrão 10); `get_calibrado_kcal`; `diario_id`; `justificativa_rt` (obrigatória na trava de menos de 800 kcal, escrita pelo RT); `texto_envio` (opcional); `conferencia` {resultado, mensagens, em}; `plano_anterior_id` (id da dieta em uso no Supabase).
- **No `documento`:** `aluno_nome` e `sexo` (F ou M).

## Banco de alimentos
- `alimentos.py buscar frango grelhado` mostra o id e os valores por 100 g.
- **TBCA:** `alimentos.py tbca peixe assado` busca no site da TBCA e numera os achados. `--gravar 1 3` (ou os códigos BRC..., ou `todos`) grava com o id `tbca:<código>`. Prefira as versões "s/ óleo, s/ sal" e "no vapor".
- **Rótulo de marca:** só vale o rótulo **oficial** (site do fabricante ou foto da embalagem); tabela digitada por loja ou app de dieta não entra. Monte a lista no formato do cabeçalho do `alimentos.py`, confira com `conferir` e grave com `adicionar`. Id `marca:<slug>`, por 100 g mais a porção do rótulo, com a fonte e a data. Líquidos por 100 mL. **Fotos de rótulo não vão para o repositório** (podem ter algo pessoal ao fundo): guarde na pasta privada e cite no `obs`.
- **Carboidrato:** `carboidrato_g` é sempre o total, com a fibra, como na TACO; o disponível vai em `carboidrato_disponivel_g`.
- **Valores especiais:** na TACO, "Tr" e "NA" viram 0, e "*" fica vazio. Na TBCA, "tr" vira 0, e "NA" e "-" ficam vazios.
- TACO (NEPA/UNICAMP) e TBCA (USP/FoRC) são tabelas públicas; cite a fonte, como já está em cada item.
