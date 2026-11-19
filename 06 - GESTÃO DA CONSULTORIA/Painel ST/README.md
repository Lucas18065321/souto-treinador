---
tipo: manual
atualizada: 2026-11-19
status: pronto para uso local (Supabase) e com modo de demonstração
---
# Painel ST

O painel da consultoria Souto Treinador rodando **no seu PC**. Ele lê e grava no **Supabase** (o banco na nuvem) com a chave que fica na sua pasta privada, e as respostas dos formulários do Tally entram sozinhas no banco pela função `tally-webhook` (mesmo com o PC desligado). Passo a passo completo, para quem não programa: `docs/guias/05-dieta-e-painel-st.md`.

## Como abrir e fechar
- **Criar o atalho (uma vez):** botão direito em `criar_atalho.ps1` → "Executar com o PowerShell". Aparece **Painel ST** na área de trabalho (ícone ST azul). Com `-Demo`, cria também o atalho da demonstração.
- **Abrir:** duplo clique no atalho. O servidor liga escondido (sem janela preta) e o painel abre numa janela própria, como um aplicativo (Chrome no seu perfil: o WhatsApp Web continua logado).
- `Abrir Painel ST.bat` faz o mesmo, de dentro da pasta.
- **Fechar:** feche a janela. O servidor desliga sozinho cerca de 1,5 min depois. Recarregar a página não desliga. Se já estiver aberto, o atalho só abre outra janela.
- **Demonstração (sem Supabase):** `python painel_st.py --demo` abre com os dados fictícios de `demo/dados-demo.json` (gerados por `../supabase/gerar_dados_ficticios.py`). O que você clicar na demonstração fica só na memória e some ao fechar.
- Para testes: `python painel_st.py [--porta 8787] [--sem-abrir] [--demo]`. Com `?estatico` no endereço, a tela abre sem animação (útil para prints).

## O que tem
| Tela | O que faz |
|---|---|
| Início | o urgente ou o próximo horário, os itens para aprovar (com quantos estão com o RT), os check-ins da semana, a adesão média, a agenda, o financeiro e a coluna de alunos com o estado de cada um |
| Hoje | lembretes por seção (Urgente, Para hoje, Próximos dias) com "Feito", os horários de hoje e os recebidos para analisar |
| Aprovações | filtros **Aprovação do RT**, Planos e entregas, Diários, Mensagens. Ler o texto, aprovar, **Aprovar como RT / Devolver com nota** (o RT), **1 · Abrir no WhatsApp**, **2 · Abrir na pasta**, Copiar PDF, Ver PDF e Marcar enviado |
| Alunos e ficha | lista com busca; a ficha tem o peso em gráfico, as **cargas do treino** em gráfico (um exercício por vez, a maior carga de cada semana), as versões do plano alimentar (a em uso destacada), check-ins, entregas, lembretes, diário e o aviso se falta o termo de consentimento (LGPD) |
| Agenda, Leads, Financeiro | horários dos próximos dias, o funil em colunas e o mês com 6 meses de barras |
| Sistema | conexão com o Supabase, a última resposta do Tally, se a assinatura do RT está na pasta privada, se o PIN do RT está ligado |

## Regras
- **Só escuta no próprio PC** (127.0.0.1). Os pedidos que gravam exigem um cabeçalho próprio, e o endereço precisa ser local.
- **Dado de aluno só passa pela memória:** 1 minuto de cache, nada vai para arquivo nem para o console. A exceção é o PDF da entrega, que fica na pasta do aluno (`%USERPROFILE%\SoutoTreinador\Alunos\<nome>`), fora do repositório.
- **A chave do Supabase** (service_role) fica em `%USERPROFILE%\SoutoTreinador\privado\supabase.env` e nunca chega ao navegador.
- **Os botões só fazem as transições combinadas** (o banco também trava):
  - Entrega de **dieta, suplementação ou receituário**: RASCUNHO → (Jorge revisa) → **APROVAÇÃO DO RT** → (o RT aprova) → ENVIAR → ENVIADO. O RT também pode **devolver com nota** (volta para RASCUNHO). Se o PDF mudar depois da aprovação, a entrega volta para o RT.
  - Entrega de treino e outros: RASCUNHO → ENVIAR → ENVIADO.
  - No ENVIADO de uma dieta (ou treino), troca a "dieta em uso" (ou "treino em uso") do aluno e fecha o plano anterior com o fim real.
  - Diário: RASCUNHO ou EM REVISÃO → APROVADO (se a conduta mexe na dieta, quem aprova é o RT).
  - Mensagem: PARA APROVAR → APROVADO → ENVIADO. Lembrete: Feito.
- **Toda ação pede um segundo toque** ("Confirmar?"). Transição fora da ordem não faz nada e avisa.
- **PIN do RT (opcional, recomendado):** com `RT_PIN_HASH` no `supabase.env`, "Aprovar como RT" e "Devolver com nota" pedem o PIN do RT. Cada decisão do RT fica registrada na tabela `aprovacoes_rt`, com a impressão digital do PDF aprovado.
- **WhatsApp (entrega em ENVIAR):** 1 · Abrir no WhatsApp (o texto vai no link e fica copiado); 2 · Abrir na pasta (o PDF aparece selecionado: arraste para a conversa) ou Copiar PDF (Ctrl+V anexa). O link do WhatsApp só leva texto. Mande e toque em "Marcar enviado". Se o PDF não estiver no PC, o painel baixa do bucket privado.

## Arquivos
- `painel_st.py`: o servidor (Python, só a biblioteca padrão). Usa `../comum/config_st.py` e `../comum/supabase_st.py`.
- `web/`: a interface (`index.html`, `painel.css`, `painel.js`, `icone.png`), com as fontes servidas de `../Agente de dieta/template/fontes`.
- `icone.ico` (atalho) e `web/icone.png` (janela): o monograma ST branco num quadrado arredondado com o degradê azul (`#2E49CE → #1F33A3 → #141A3D`), gerados por `gerar_icone.py` (precisa do Pillow só para regerar).
- `demo/dados-demo.json`: dados fictícios da demonstração.
- `criar_atalho.ps1` e `Abrir Painel ST.bat`.
