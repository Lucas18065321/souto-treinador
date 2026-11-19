---
name: "montar-dieta"
description: "Monta a proposta da nova versão do plano alimentar de um aluno da consultoria Souto Treinador no método do RT (o nutricionista Lucas Melo, Responsável Técnico pela dieta): lê do Supabase a ficha, a anamnese, os check-ins, as medidas, as cargas e a dieta em uso (script, sem token), propõe gasto, fase e macros (⏸), monta o cardápio com a TACO e confere por script (⏸), gera o PDF da marca com o bloco e a assinatura do RT e grava no Supabase a Dieta v{n}, as Refeições, os Suplementos e a Entrega em RASCUNHO, que só vai ao aluno depois da APROVAÇÃO DO RT no Painel ST. Use quando o Jorge ou o RT disserem 'monta a dieta do aluno X', 'novo plano', 'ajusta a dieta' ou chamarem /montar-dieta."
argument-hint: "<nome do aluno>"
---

# /montar-dieta

> Pasta: `06 - GESTÃO DA CONSULTORIA/Agente de dieta` na raiz deste repositório (abaixo, `AD`). Rode os scripts com o caminho completo, entre aspas:
> - `python "AD/dieta_supabase.py" pacote "<nome ou AL-n>"` · `python "AD/dieta_supabase.py" salvar "<json>" [--refazer]`
> - `python "AD/calcular_plano.py" energia ...` · `python "AD/calcular_plano.py" conferir "<json>" --gravar`
> - `python "AD/alimentos.py" buscar <palavras>` · `ver <id>` · `tbca <palavras> --gravar <n>` · `conferir <novos.json>` · `adicionar <novos.json>`
> - `python "AD/template/montar_plano.py" "<json>"` (PDF e HTML na pasta do JSON)
>
> **Leia antes:** `AD/Método do RT (Lucas Melo).md` (as regras do RT, que mandam) e, para o formato do JSON, `AD/template/exemplo-ficticio.json` + `AD/template/README.md`.
>
> **Regras fixas:**
> - **Prescrição dietética é ato privativo do nutricionista (Lei 8.234/1991).** Quem decide números, fase, cortes e suplementos é o **RT (Lucas Melo, CRN6 - 50479-P)**, nunca o Jorge (educador físico) nem o agente. O agente propõe; o Jorge pode conduzir a sessão e revisar a linguagem, mas toda decisão clínica que pede "ok" nas paradas ⏸ é **do RT**. Se o RT não estiver na conversa, monte a proposta, salve em RASCUNHO e deixe claro que ela **espera a APROVAÇÃO DO RT** no Painel ST.
> - **LGPD:** dado de aluno é dado de saúde. Fica no Supabase e na pasta `%USERPROFILE%\SoutoTreinador\Alunos\<nome do aluno>`, **nunca no repositório** (público no GitHub), nem no OneDrive, nem em conteúdo. Não cole dado de aluno em issue, commit ou documento do repositório.
> - **Aluno pelo nome:** pastas, arquivos e respostas usam o nome; o código AL-n fica só como chave interna (`aluno_id` no JSON e no link do Tally).
> - **Evidência sem invenção:** número de alimento só do banco (`alimentos.py`), e afirmação clínica só da base científica ou das diretrizes do RT.
> - **Nada clínico sai sem o RT:** a Entrega nasce em RASCUNHO; o caminho é RASCUNHO → (Jorge revisa) → APROVAÇÃO DO RT → (RT aprova) → ENVIAR → ENVIADO. O banco não deixa pular o RT.
> - **Assinatura do RT:** é uma imagem fora do repositório (`%USERPROFILE%\SoutoTreinador\privado\assinatura-rt.png`). Nunca copie, gere ou desenhe uma assinatura. Se o script avisar que ela falta, pare e avise.
> - **Quem usa não programa:** explique em linguagem simples, sem colar comando.
> - Uma sessão por aluno.

## 0. Aluno e conduta
1. `dieta_supabase.py pacote "<nome>"`. Mais de um nome igual → pergunte qual. Sem anamnese → avise (sem altura não há gasto) e pare.
2. Leia o `pacote.json` (Read) da pasta indicada.
3. **Conduta:** o pedido ("monta a dieta") é a decisão. Se o diário mais recente tiver conduta APROVADA (pelo RT, quando mexe na dieta) de ajuste, plano novo ou repetir o plano, use-a e guarde o id em `plano.diario_id`. Se for outra, mostre e confirme em uma linha.
4. Tipo de versão: `primeiro` (sem dieta em uso) · `ajuste` · `mudanca_fase` · `repeticao` · `pausa`.

## 1. Leitura do aluno (até 12 linhas)
- **Quem e o que quer:** objetivo, linha, rotina e trabalho, treino (a ficha, as cargas e os check-ins de cargas), sono e estresse.
- **Como come:** horários e refeições, quem cozinha, aversões, intolerâncias e alergias, ultraprocessados, doce e refeição livre (respostas da anamnese).
- **Como foi o plano em uso:** adesão (dias no plano, score), peso de tendência, fome e saciedade, "troca pedida", "dificuldade" e pergunta dos check-ins, alertas.
- **Exames:** só os marcadores que mudam a conduta.
- **Gordura corporal (Método §2):** junte o IMC, a cintura em relação à altura e o RFM e, se houver fotos, abra-as (baixe para a pasta do aluno, nunca para o repositório, e apague no fim). Dê a **faixa** e o porquê em uma linha.

## 2. Números (⏸ parada 1 · decisão do RT)
1. `calcular_plano.py energia --sexo F|M --idade N --altura CM --peso <tendência> --fa <fator> --deficit <D> --proteina <g/kg> --gordura <g/kg>`. Fator conservador (Método §1). Do 2º plano em diante, mostre também o GET calibrado, se houver.
2. Mostre numa tabela curta: fator e o porquê; gasto do dia; fase e déficit (pela gordura corporal); kcal; proteína (g e g/kg), gordura, carboidrato; fibra e o limite de saturada; água (no 1º plano, **pergunte ao RT** o mL/kg; depois, repita); refeição livre (Método §6); suplementos sugeridos, com o motivo e a fonte (Método §7).
3. Destaque o que pede o ok do RT: déficit acima do teto; mudança de fase; corte de grupo alimentar; dieta de exclusão; kcal abaixo da faixa típica.
4. Pergunte ao RT: "quer algo mais específico ou sigo assim?" Espere. Regra nova que o RT der → anote em `Método do RT (Lucas Melo).md`, com data.

## 3. Cardápio e conferência (⏸ parada 2 · decisão do RT)
1. Monte o JSON na pasta do aluno, `Plano v{n} - {nome do aluno} - {inicio}.json`, com 4 blocos:
   - **`documento`:** copie do pacote e confirme o **início** (padrão = validade do plano em uso; lembre que o envio depende da aprovação do RT). Validade = início + 30. `treino` {dias, horario} pela ficha.
   - **`plano`:** `aluno_id` = AL-n, `versao` = `proxima_versao`, `plano_anterior_id` = `dieta_em_uso.id`, `get_metodo` `mifflin_fa`, `tmb_kcal`, `fator_atividade_texto` leigo, `gerado_por` = "Claude (/montar-dieta)", `gerado_em`.
   - **`relatorio`** (da v2 em diante): acertos, atenção, melhorar e metas (1 a 3 de comportamento + 1 de resultado, com prazo), e `recapitulacao`. Linguagem leiga, sem culpa e com números simples.
   - **`evolucao`:** copie do pacote; em `planos`, ponha `fim` = início novo no plano em uso.
2. **Alimentos:** `alimentos.py buscar <palavras>`; cada item com gramas leva `ref` e o peso **pronto**, com `preparo`. Procure primeiro no banco (TACO, TBCA, marcas). Se faltar: TBCA por `tbca ... --gravar`, ou rótulo **oficial** por `conferir` + `adicionar`. Nunca invente valor.
3. **Regras do Método §5:** 3 a 4 opções de proteína e de carboidrato por refeição (grupos de troca); cuscuz como opção ao arroz onde fizer sentido; legumes e folhas de 150 a 250 g no almoço e no jantar, um por um; azeite ou óleo só para untar.
4. `calcular_plano.py conferir "<json>" --gravar` até **zerar os erros**. Aviso pode ficar, explicado.
5. Mostre ao RT um quadro por refeição, o total do dia comum e a média da semana, os avisos e o relatório "último mês". Espere o ok. Mudou algo → conferir de novo.

## 4. PDF e Supabase
1. `montar_plano.py "<json>"` gera o PDF e o HTML na pasta do aluno, na marca Souto Treinador, com o rodapé "Prescrição dietética: Lucas Melo · Nutricionista · CRN6 - 50479-P" e o bloco de assinatura do RT. Se aparecer "AVISO: assinatura do RT não encontrada", pare e peça para pôr a imagem na pasta privada. Na 1ª vez do aluno, gere `--png` e olhe a capa e uma página de refeições; apague `png/` depois.
2. `dieta_supabase.py salvar "<json>"`. O script confere de novo (não salva com erro; trava de < 800 kcal só com `plano.justificativa_rt` escrita pelo RT), sobe o PDF e o JSON para o bucket privado, guarda a impressão digital do PDF e cria a Dieta v{n}, as Refeições, os Suplementos, o Relatório de abertura (v2+) e a Entrega em **RASCUNHO**. Refazer uma versão ainda não aprovada pelo RT: `--refazer`.
3. Responda em até 6 linhas: fase, kcal e macros; início e validade; os avisos; e o próximo passo: **Painel ST → Aprovações**: o Jorge toca em "Revisado: mandar para o RT"; o RT abre o PDF e toca em "Aprovar como RT" (ou "Devolver com nota"); depois, "1 · Abrir no WhatsApp", "2 · Abrir na pasta", mandar e "Marcar enviado".

## 5. Fechamento
- O pacote, o JSON, o PDF e o HTML ficam na pasta do aluno (o histórico local). Fotos baixadas e `png/` saem.
- RT devolveu com nota → volte ao passo 3, gere o PDF de novo e rode `salvar --refazer` (a entrega volta para RASCUNHO e passa pelo RT outra vez).
