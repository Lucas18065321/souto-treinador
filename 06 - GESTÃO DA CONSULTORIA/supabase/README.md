---
tipo: manual
atualizada: 2026-11-19
---
# Supabase (banco, arquivos e a ponte do Tally)

| Arquivo | O que é |
|---|---|
| `migrations/0001_schema.sql` | o banco inteiro: tipos, tabelas, travas de status (incluindo a **APROVAÇÃO DO RT**), índices, visões, segurança por linha (RLS) e o bucket privado `entregas` |
| `seed_ficticio.sql` | dados **fictícios** de demonstração (só para um projeto de teste) |
| `gerar_dados_ficticios.py` | gera o `seed_ficticio.sql` e o `../Painel ST/demo/dados-demo.json` da mesma fonte |
| `functions/tally-webhook/index.ts` | a Edge Function que recebe os formulários do Tally, confere a assinatura e grava no banco |

Passo a passo completo, para quem não programa: `docs/guias/05-dieta-e-painel-st.md`. Resumo técnico:

## Banco
- **Pelo painel do Supabase:** SQL Editor → New query → cole `migrations/0001_schema.sql` → Run.
- **Pela linha de comando:** `npx supabase login` → `npx supabase link --project-ref <ref>` → `npx supabase db push` (rode na pasta `06 - GESTÃO DA CONSULTORIA`, que contém `supabase/migrations`).
- **Segurança:** RLS ligada em todas as tabelas, sem nenhuma política para `anon`. Lê e grava: a chave `service_role` (Painel ST e a função do Tally, que passam por cima da RLS) e usuários logados que estejam na tabela `equipe` (o dono e o RT). Para dar acesso ao RT pelo painel do Supabase: crie o usuário em Authentication e rode `insert into public.equipe (user_id, nome, papel) values ('<uuid>', 'Lucas Melo', 'rt');`. Só quem tem papel `rt` aprova dieta logado.
- **Travas no banco:** `entregas_transicao` (só as transições combinadas; dieta, suplementação e receituário não passam de APROVACAO_RT para ENVIAR sem o RT; PDF trocado depois da aprovação volta para o RT; ENVIADO exige o PDF aprovado), `envios_transicao`, `diario_transicao` e a tabela `historico` (quem mudou o quê e quando).
- **Arquivos:** bucket `entregas`, **privado**. O painel sobe o PDF em `alunos/<id>/dieta-v{n}-{início}.pdf` e abre por **link assinado** de 10 minutos.

## Função do Tally
```
npx supabase functions deploy tally-webhook --no-verify-jwt
npx supabase secrets set TALLY_SIGNING_SECRET=<o signing secret do webhook no Tally>
```
- Endereço para o Tally: `https://<ref>.supabase.co/functions/v1/tally-webhook?tipo=anamnese` (ou `checkin`, `cargas`, `anamnese_treino`).
- O formulário precisa do campo escondido `aluno_id` (o código AL-n do aluno, que vai no link: `https://tally.so/r/<id>?aluno_id=AL-3`).
- `--no-verify-jwt` porque o Tally não manda login do Supabase; quem garante que o pedido veio do Tally é a assinatura HMAC (`tally-signature`), conferida a cada pedido. Sem o segredo configurado, a função recusa tudo.
- A mesma resposta reenviada não duplica (`tally_resposta_id` único). Se der erro no meio, o recebido é desfeito e o Tally tenta de novo.

## Teste feito na construção (2026-11-19)
- O SQL **não foi executado** num Postgres de verdade (não havia Postgres nem Docker no PC da construção): foi revisado à mão e por um verificador simples (parênteses, aspas e blocos). Rode primeiro num projeto de teste.
- A função do Tally foi testada no Node 24 com o Deno e o banco simulados: assinatura inválida recusada (401), check-in (check-in + medida + lembrete de dor), resposta repetida ignorada, check-in de cargas (semana, sessões, séries com carga e de peso do corpo), anamnese sem aluno (ficha nova com o aceite da LGPD) e aluno desconhecido (SEM_DONO). Não foi publicada num Supabase real.
