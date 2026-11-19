---
tipo: manual
atualizada: 2026-11-19
---
# 06 · Gestão da consultoria

O sistema que gere a consultoria Souto Treinador: alunos, check-ins, cargas do treino, dieta (com Responsável Técnico), entregas, agenda, leads e financeiro. Roda no PC do Jorge (Painel ST) com o banco no Supabase.

| Pasta / arquivo | O que é |
|---|---|
| `config-st.json` | **a única configuração da marca**: Jorge Souto, CREF e @ (com TROCAR), o RT da dieta e as pastas fora do repositório |
| `comum/` | código comum (configuração e cliente do Supabase, só com a biblioteca padrão do Python) |
| `Agente de dieta/` | o motor da dieta: banco de alimentos (TACO, TBCA, rótulos), contas e conferência, o PDF da marca e o receituário |
| `Painel ST/` | o painel local (Início, Hoje, Aprovações com a do RT, Alunos e ficha, Agenda, Leads, Financeiro, Sistema), com modo de demonstração |
| `supabase/` | o banco (migração SQL), os dados fictícios e a função que recebe os formulários do Tally |
| `requirements.txt` | o que instalar com o pip (quase nada: o sistema usa só a biblioteca padrão) |

Guia completo, passo a passo: `docs/guias/05-dieta-e-painel-st.md`.

## Regras
- **Prescrição dietética é ato privativo do nutricionista.** O RT da dieta é **Lucas Melo (CRN6 - 50479-P)**. Todo plano alimentar, suplementação ou receituário passa pela **APROVAÇÃO DO RT** antes do envio; o banco trava o envio sem ela. O PDF da dieta leva a marca do Jorge e termina com "Prescrição dietética: Lucas Melo · Nutricionista · CRN6 - 50479-P" + a assinatura do RT.
- **Dados de alunos são dados de saúde (LGPD, dado sensível).** Nunca entram no repositório: ficam no Supabase (com RLS) e na pasta `%USERPROFILE%\SoutoTreinador\Alunos\<nome>`. Exemplos e testes usam só dados fictícios ("Ana Exemplo", "Bruno Fictício"...).
- **Segredos nunca entram no repositório:** a chave do Supabase (`supabase.env`), a imagem da assinatura do RT (`assinatura-rt.png`) e o contato do prescritor ficam em `%USERPROFILE%\SoutoTreinador\privado\`. O `.gitignore` desta pasta reforça isso.
- **Histórico:** este sistema foi portado de uma versão anterior que rodava no Notion; cada banco do Notion virou uma tabela do Supabase (`supabase/migrations/0001_schema.sql`).
