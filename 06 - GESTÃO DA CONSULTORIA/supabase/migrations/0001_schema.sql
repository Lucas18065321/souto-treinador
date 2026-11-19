-- =====================================================================================================
-- Souto Treinador · gestão da consultoria · esquema do banco (Supabase / PostgreSQL 15+)
-- 0001_schema.sql — rode UMA vez num projeto novo (SQL Editor → cole tudo → Run, ou: npx supabase db push)
--
-- O que este arquivo cria:
--   * os tipos (status e listas fixas), incluindo a etapa APROVACAO_RT (aprovação do Responsável Técnico,
--     o nutricionista, obrigatória antes de enviar dieta, suplementação ou receituário);
--   * as tabelas espelhando os bancos do sistema anterior: alunos, dietas, refeições, suplementos, entregas,
--     check-ins, medidas, diário, treino (prescrições, itens, semanas, sessões, séries), lembretes, consultas,
--     leads, contratos, pagamentos, despesas, mensagens prontas, envios, recebidos, exames, relatórios...;
--   * travas no próprio banco: transições de status permitidas e "dieta só vai para ENVIAR depois do RT";
--   * segurança por linha (RLS) LIGADA em todas as tabelas: o anônimo (chave anon) não lê nem grava nada;
--     só a chave service_role (o Painel ST, no PC do Jorge, e a função do Tally) e usuários logados que
--     estejam na tabela "equipe" (o dono e o RT) têm acesso;
--   * o bucket PRIVADO "entregas" para os PDFs (acesso só por link assinado, que expira).
--
-- Notas de migração (do sistema anterior, que rodava no Notion): cada "banco" virou uma tabela; relações
-- viraram chaves estrangeiras (*_id); fórmulas simples viraram colunas geradas ou visões (v_*); o número
-- PAC-n virou o código AL-n do aluno.
-- =====================================================================================================

begin;

-- ---------------------------------------------------------------- tipos
create type public.aluno_status      as enum ('entrada', 'ativo', 'pausado', 'renovacao', 'encerrado');
create type public.aluno_etapa       as enum ('aceite', 'pagamento', 'anamnese', 'consulta_marcada', 'consulta_realizada',
                                              'plano_em_preparo', 'plano_enviado');
create type public.aluno_linha       as enum ('emagrecimento', 'hipertrofia', 'saude', 'performance', 'gastro');
create type public.sexo_calculo      as enum ('F', 'M');
create type public.entrega_status    as enum ('RASCUNHO', 'APROVACAO_RT', 'ENVIAR', 'ENVIADO', 'DESCARTADO');
create type public.entrega_tipo      as enum ('dieta', 'treino', 'suplementacao', 'receituario', 'relatorio', 'material',
                                              'recibo', 'outro');
create type public.diario_status     as enum ('RASCUNHO', 'EM_REVISAO', 'REFAZER', 'APROVADO');
create type public.envio_status      as enum ('PARA_APROVAR', 'APROVADO', 'ENVIADO', 'DESFEITO', 'DESCARTADO');
create type public.mensagem_status   as enum ('RASCUNHO', 'APROVADO', 'REVISAR', 'ARQUIVADO');
create type public.recebido_status   as enum ('NOVO', 'SEM_DONO', 'AGUARDANDO_ALUNO', 'EM_ANALISE', 'PARA_REVISAO',
                                              'ANALISADO', 'SO_REGISTRO', 'SUBSTITUIDO');
create type public.recebido_tipo     as enum ('anamnese', 'anamnese_treino', 'checkin_semanal', 'checkin_quinzenal',
                                              'checkin_cargas', 'exame', 'foto', 'mensagem', 'outro');
create type public.consulta_tipo     as enum ('primeira', 'retorno', 'renovacao', 'avaliacao', 'treino_presencial');
create type public.consulta_status   as enum ('agendada', 'confirmada', 'realizada', 'faltou', 'remarcada', 'cancelada');
create type public.lembrete_secao    as enum ('urgente', 'para_hoje', 'proximos_dias');
create type public.lead_etapa        as enum ('novo', 'em_conversa', 'proposta', 'fechou', 'perdido');
create type public.lead_temperatura  as enum ('quente', 'morno', 'frio');
create type public.contrato_status   as enum ('vigente', 'pausado', 'em_renovacao', 'renovado', 'encerrado');
create type public.pagamento_situacao as enum ('previsto', 'pago', 'vencido', 'cancelado', 'estornado');
create type public.dieta_fase        as enum ('deficit', 'manutencao', 'pausa', 'superavit');
create type public.dieta_tipo_versao as enum ('primeiro', 'ajuste', 'repeticao', 'pausa', 'mudanca_fase');
create type public.sessao_status     as enum ('completa', 'parcial', 'nao_feita');
create type public.equipe_papel      as enum ('dono', 'rt', 'assistente');

-- ---------------------------------------------------------------- funções de apoio
create or replace function public.tocar_atualizado_em() returns trigger
language plpgsql as $$
begin
  new.atualizado_em := now();
  return new;
end $$;

-- ---------------------------------------------------------------- base
create table public.equipe (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  nome        text not null,
  papel       public.equipe_papel not null default 'dono',
  criado_em   timestamptz not null default now()
);
comment on table public.equipe is 'Quem pode entrar logado (Supabase Auth) e ver tudo: o dono (Jorge) e o RT (nutricionista). Sem linha aqui, um usuário logado não vê nada.';

-- "Está na equipe?" (security definer: a política de cada tabela chama esta função sem dar acesso à tabela equipe)
create or replace function public.e_da_equipe() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.equipe where user_id = auth.uid());
$$;

create or replace function public.e_rt() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.equipe where user_id = auth.uid() and papel = 'rt');
$$;

create table public.configuracoes (
  id            uuid primary key default gen_random_uuid(),
  chave         text not null unique,
  valor         text,
  descricao     text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table public.metas (
  id            uuid primary key default gen_random_uuid(),
  nome          text not null,
  alvo          integer not null check (alvo > 0),
  observacao    text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table public.tabela_precos (
  id             uuid primary key default gen_random_uuid(),
  nome           text not null,
  periodicidade  text,
  valor          numeric(10, 2) not null check (valor >= 0),
  duracao_dias   integer check (duracao_dias > 0),
  inclui_dieta   boolean not null default false,
  oferecer       boolean not null default true,
  observacao     text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

-- ---------------------------------------------------------------- comercial
create table public.leads (
  id                uuid primary key default gen_random_uuid(),
  nome              text not null,
  telefone          text,
  perfil            text,
  entrou_em         date not null default current_date,
  origem            text,
  temperatura       public.lead_temperatura,
  problema          text,
  linha_provavel    public.aluno_linha,
  etapa             public.lead_etapa not null default 'novo',
  motivo_perda      text,
  proximo_followup  date,
  valor_fechado     numeric(10, 2),
  aluno_id          uuid,          -- ligado depois de alunos existir (ver abaixo)
  observacao        text,
  criado_em         timestamptz not null default now(),
  atualizado_em     timestamptz not null default now()
);

-- ---------------------------------------------------------------- alunos
create table public.alunos (
  id                      uuid primary key default gen_random_uuid(),
  numero                  bigint generated always as identity,
  codigo                  text generated always as ('AL-' || numero::text) stored,
  nome                    text not null,
  primeiro_nome           text,
  telefone                text,             -- com DDI e DDD, só números (ex.: 5584999999999), para o link do WhatsApp
  email                   text,
  sexo                    public.sexo_calculo,
  nascimento              date,
  altura_cm               numeric(5, 1) check (altura_cm is null or altura_cm between 100 and 250),
  cidade                  text,
  status                  public.aluno_status not null default 'entrada',
  etapa_entrada           public.aluno_etapa,
  linha                   public.aluno_linha not null default 'emagrecimento',
  objetivo                text,
  tem_dieta               boolean not null default false,
  tem_treino              boolean not null default true,
  dia_checkin             text check (dia_checkin is null or dia_checkin in
                            ('segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo')),
  mostrar_numeros_pdf     boolean not null default true,
  modelo_pdf              text not null default 'a' check (modelo_pdf in ('a', 'b')),
  dieta_em_uso_id         uuid,             -- FK ligada depois de dietas existir
  treino_em_uso_id        uuid,             -- FK ligada depois de prescricoes_treino existir
  lead_id                 uuid references public.leads (id) on delete set null,
  meta_id                 uuid references public.metas (id) on delete set null,
  anamnese_recebida_em    date,
  consentimento_lgpd_em   timestamptz,      -- aceite do termo de consentimento de dados (LGPD art. 7º e 11)
  consentimento_versao    text,
  observacoes             text,
  criado_em               timestamptz not null default now(),
  atualizado_em           timestamptz not null default now(),
  constraint alunos_codigo_unico unique (codigo)
);
comment on column public.alunos.consentimento_lgpd_em is 'Quando o aluno aceitou o termo de consentimento (dados de saúde são sensíveis: LGPD art. 11).';

alter table public.leads add constraint leads_aluno_fk foreign key (aluno_id) references public.alunos (id) on delete set null;

create table public.contratos (
  id               uuid primary key default gen_random_uuid(),
  aluno_id         uuid not null references public.alunos (id) on delete cascade,
  plano_id         uuid references public.tabela_precos (id) on delete set null,
  valor            numeric(10, 2) check (valor is null or valor >= 0),
  inicio           date not null,
  duracao_dias     integer not null default 30 check (duracao_dias > 0),
  fim              date generated always as (inicio + duracao_dias) stored,
  status           public.contrato_status not null default 'vigente',
  forma_cobranca   text,
  parcelas         integer check (parcelas is null or parcelas > 0),
  observacao       text,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.pagamentos (
  id             uuid primary key default gen_random_uuid(),
  contrato_id    uuid references public.contratos (id) on delete set null,
  aluno_id       uuid references public.alunos (id) on delete set null,
  descricao      text not null,
  situacao       public.pagamento_situacao not null default 'previsto',
  vencimento     date,
  pago_em        date,
  valor_bruto    numeric(10, 2) not null check (valor_bruto >= 0),
  taxa           numeric(10, 2) not null default 0 check (taxa >= 0),
  valor_liquido  numeric(10, 2) generated always as (valor_bruto - taxa) stored,
  forma          text,
  parcela        text,
  observacao     text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now(),
  constraint pagamentos_pago_tem_data check (situacao <> 'pago' or pago_em is not null)
);

create table public.despesas (
  id             uuid primary key default gen_random_uuid(),
  descricao      text not null,
  categoria      text,
  mes            date not null,
  valor          numeric(10, 2) not null check (valor >= 0),
  pago           boolean not null default false,
  pago_em        date,
  observacao     text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

-- ---------------------------------------------------------------- agenda e comunicação
create table public.consultas (
  id             uuid primary key default gen_random_uuid(),
  aluno_id       uuid references public.alunos (id) on delete cascade,
  titulo         text,
  data_hora      timestamptz not null,
  duracao_min    integer not null default 45 check (duracao_min > 0),
  tipo           public.consulta_tipo not null default 'retorno',
  status         public.consulta_status not null default 'agendada',
  link_reuniao   text,
  alerta         text,
  observacao     text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

create table public.mensagens_prontas (
  id             uuid primary key default gen_random_uuid(),
  codigo         text unique,
  nome           text not null,
  texto          text not null,
  dono           text,                       -- Operação · Dieta · Treino
  canal          text not null default 'WhatsApp',
  status         public.mensagem_status not null default 'RASCUNHO',
  versao         integer not null default 1,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

create table public.envios (
  id                   uuid primary key default gen_random_uuid(),
  aluno_id             uuid references public.alunos (id) on delete cascade,
  mensagem_pronta_id   uuid references public.mensagens_prontas (id) on delete set null,
  titulo               text not null,
  texto_final          text not null,
  telefone             text,
  status               public.envio_status not null default 'PARA_APROVAR',
  aprovado_em          timestamptz,
  enviado_em           timestamptz,
  origem               text not null default 'manual',
  criado_em            timestamptz not null default now(),
  atualizado_em        timestamptz not null default now()
);

-- ---------------------------------------------------------------- clínico (check-ins, medidas, diário, exames)
create table public.recebidos (
  id                     uuid primary key default gen_random_uuid(),
  aluno_id               uuid references public.alunos (id) on delete cascade,
  tipo                   public.recebido_tipo not null,
  status                 public.recebido_status not null default 'NOVO',
  origem                 text not null default 'tally',
  titulo                 text not null,
  recebido_em            timestamptz not null default now(),
  semana_inicio          date,
  aluno_codigo_informado text,               -- o aluno_id que veio no link do formulário (para casar depois, se SEM_DONO)
  tally_form_id          text,
  tally_resposta_id      text unique,        -- evita gravar a mesma resposta duas vezes (o Tally pode reenviar)
  urgente                boolean not null default false,
  respostas              jsonb not null default '{}'::jsonb,
  respostas_texto        text,
  criado_em              timestamptz not null default now(),
  atualizado_em          timestamptz not null default now()
);

create table public.checkins (
  id                 uuid primary key default gen_random_uuid(),
  aluno_id           uuid references public.alunos (id) on delete cascade,
  recebido_id        uuid references public.recebidos (id) on delete set null,
  dieta_id           uuid,                    -- dieta em uso na semana (FK ligada depois)
  semana_inicio      date not null,
  quinzenal          boolean not null default false,
  peso_semana        numeric(5, 2) check (peso_semana is null or peso_semana between 25 and 350),
  dias_no_plano      smallint check (dias_no_plano between 0 and 7),
  dias_leve          smallint check (dias_leve between 0 and 7),
  dias_grande        smallint check (dias_grande between 0 and 7),
  dias_nao_lembro    smallint check (dias_nao_lembro between 0 and 7),
  score              smallint generated always as (
                       case when coalesce(dias_no_plano, 0) + coalesce(dias_leve, 0) + coalesce(dias_grande, 0) = 0 then null
                            else round((coalesce(dias_no_plano, 0) * 100 + coalesce(dias_leve, 0) * 50)::numeric
                                       / (coalesce(dias_no_plano, 0) + coalesce(dias_leve, 0) + coalesce(dias_grande, 0)))::smallint
                       end) stored,
  treinos_feitos     smallint check (treinos_feitos between 0 and 14),
  fome               smallint check (fome between 0 and 10),
  saciedade          smallint check (saciedade between 0 and 10),
  sono_horas         numeric(3, 1) check (sono_horas between 0 and 16),
  sono_qualidade     smallint check (sono_qualidade between 0 and 10),
  estresse           smallint check (estresse between 0 and 10),
  agua_l             numeric(3, 1) check (agua_l between 0 and 10),
  cintura_cm         numeric(5, 1),
  quadril_cm         numeric(5, 1),
  dor_lesao_nova     boolean not null default false,
  troca_pedida       text,
  dificuldade        text,
  pergunta           text,
  nivel              text,                     -- leitura do formulário: ok · revisar · urgente
  alertas            text[] not null default '{}',
  respostas          jsonb not null default '{}'::jsonb,
  criado_em          timestamptz not null default now(),
  atualizado_em      timestamptz not null default now(),
  constraint checkins_uma_por_semana unique (aluno_id, semana_inicio, quinzenal)
);

create table public.medidas (
  id             uuid primary key default gen_random_uuid(),
  aluno_id       uuid not null references public.alunos (id) on delete cascade,
  checkin_id     uuid references public.checkins (id) on delete set null,
  data           date not null,
  peso_kg        numeric(5, 2) check (peso_kg is null or peso_kg between 25 and 350),
  cintura_cm     numeric(5, 1),
  quadril_cm     numeric(5, 1),
  origem         text not null default 'checkin',
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

create table public.diario (
  id                uuid primary key default gen_random_uuid(),
  aluno_id          uuid not null references public.alunos (id) on delete cascade,
  checkin_id        uuid references public.checkins (id) on delete set null,
  data              date not null default current_date,
  tipo              text not null default 'Análise do check-in',
  status            public.diario_status not null default 'RASCUNHO',
  conduta_proposta  text,
  conduta_decidida  text,
  texto_proposto    text,
  texto_final       text,
  envolve_dieta     boolean not null default false,   -- conduta que mexe na dieta: a decisão é do RT
  aprovado_em       timestamptz,
  aprovado_por      text,
  criado_em         timestamptz not null default now(),
  atualizado_em     timestamptz not null default now()
);

create table public.exames (
  id             uuid primary key default gen_random_uuid(),
  aluno_id       uuid not null references public.alunos (id) on delete cascade,
  recebido_id    uuid references public.recebidos (id) on delete set null,
  data_coleta    date,
  arquivo_path   text,
  status         text not null default 'NOVO',
  resumo         text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

create table public.marcadores (
  id             uuid primary key default gen_random_uuid(),
  aluno_id       uuid not null references public.alunos (id) on delete cascade,
  exame_id       uuid references public.exames (id) on delete cascade,
  nome           text not null,
  valor          numeric,
  unidade        text,
  faixa_texto    text,
  situacao       text check (situacao is null or situacao in ('abaixo', 'dentro', 'acima')),
  data_coleta    date,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

-- ---------------------------------------------------------------- dieta (prescrição do RT)
create table public.dietas (
  id                     uuid primary key default gen_random_uuid(),
  aluno_id               uuid not null references public.alunos (id) on delete cascade,
  versao                 integer not null check (versao > 0),
  tipo_versao            public.dieta_tipo_versao not null,
  plano_anterior_id      uuid references public.dietas (id) on delete set null,
  fase                   public.dieta_fase not null,
  get_kcal               integer,
  get_metodo             text,
  get_calibrado_kcal     integer,
  fator_atividade        numeric(4, 3),
  peso_usado_kg          numeric(5, 2),
  data_peso              date,
  kcal_dia               integer not null check (kcal_dia > 0),
  proteina_g             numeric(6, 1) not null,
  carboidrato_g          numeric(6, 1) not null,
  gordura_g              numeric(6, 1) not null,
  fibra_g                numeric(6, 1),
  meta_agua_l            numeric(3, 1),
  agua_ml_por_kg         numeric(5, 1),
  livre_prevista         boolean not null default false,
  livre_por_semana       numeric(3, 1),
  livre_teto_kcal        integer,
  o_que_muda             text,
  conferencia            text check (conferencia is null or conferencia in ('ok', 'aviso', 'erro', 'trava')),
  mensagens_conferencia  text,
  justificativa_rt       text,                  -- obrigatória na trava (< 800 kcal)
  mostrar_numeros        boolean not null default true,
  plano_json             jsonb,                 -- o JSON completo que gerou o PDF
  json_path              text,                  -- cópia no bucket
  entrega_id             uuid,                  -- FK ligada depois de entregas existir
  diario_id              uuid references public.diario (id) on delete set null,
  gerado_por             text,
  criado_em              timestamptz not null default now(),
  atualizado_em          timestamptz not null default now(),
  constraint dietas_versao_unica unique (aluno_id, versao),
  constraint dietas_trava_800 check (kcal_dia >= 800 or justificativa_rt is not null)
);

create table public.refeicoes (
  id                uuid primary key default gen_random_uuid(),
  dieta_id          uuid not null references public.dietas (id) on delete cascade,
  ordem             integer not null,
  nome_exibicao     text not null,
  refeicao_padrao   text,
  horario           text,
  kcal              numeric(6, 1),
  proteina_g        numeric(6, 1),
  carboidrato_g     numeric(6, 1),
  gordura_g         numeric(6, 1),
  itens             text,
  substituicoes     text,
  tipo_dia          text not null default 'todos' check (tipo_dia in ('todos', 'treino', 'descanso')),
  criado_em         timestamptz not null default now(),
  atualizado_em     timestamptz not null default now()
);

create table public.relatorios (
  id                uuid primary key default gen_random_uuid(),
  aluno_id          uuid not null references public.alunos (id) on delete cascade,
  dieta_id          uuid references public.dietas (id) on delete cascade,
  tipo              text not null default 'Abertura do plano',
  status            text not null default 'RASCUNHO' check (status in ('RASCUNHO', 'APROVADO', 'DESCARTADO')),
  titulo            text not null,
  acertos           text,
  atencao           text,
  melhorar          text,
  resumo            text,
  proximos_passos   text,
  numeros           jsonb,
  criado_em         timestamptz not null default now(),
  atualizado_em     timestamptz not null default now()
);

-- ---------------------------------------------------------------- treino
create table public.exercicios (
  id               uuid primary key default gen_random_uuid(),
  nome_tecnico     text not null unique,
  nome_aluno       text,
  grupo            text,
  equipamento      text,
  unidade_padrao   text not null default 'kg total'
                     check (unidade_padrao in ('kg total', 'kg por halter', 'placa', 'nível do elástico', 'peso do corpo')),
  video_url        text,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.prescricoes_treino (
  id                   uuid primary key default gen_random_uuid(),
  aluno_id             uuid not null references public.alunos (id) on delete cascade,
  versao               integer not null default 1,
  objetivo             text,
  nivel                text,
  local_treino         text,
  sessoes_por_semana   smallint check (sessoes_por_semana between 1 and 14),
  inicio               date,
  validade             date,
  entrega_id           uuid,                    -- FK ligada depois
  observacao           text,
  criado_em            timestamptz not null default now(),
  atualizado_em        timestamptz not null default now(),
  constraint prescricoes_versao_unica unique (aluno_id, versao)
);

create table public.itens_prescricao (
  id               uuid primary key default gen_random_uuid(),
  prescricao_id    uuid not null references public.prescricoes_treino (id) on delete cascade,
  dia              text not null check (dia ~ '^[A-F]$'),
  ordem            smallint not null,
  exercicio_id     uuid references public.exercicios (id) on delete set null,
  series           smallint,
  repeticoes       text,                        -- faixa: "8 a 12"
  descanso_s       smallint,
  observacao       text,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.semanas_treino (
  id               uuid primary key default gen_random_uuid(),
  aluno_id         uuid not null references public.alunos (id) on delete cascade,
  prescricao_id    uuid references public.prescricoes_treino (id) on delete set null,
  recebido_id      uuid references public.recebidos (id) on delete set null,
  semana_inicio    date not null,
  planejadas       smallint,
  completas        smallint not null default 0,
  parciais         smallint not null default 0,
  adesao_pct       smallint generated always as (
                     case when coalesce(planejadas, 0) = 0 then null
                          else least(100, round(((completas + parciais) * 100)::numeric / planejadas))::smallint end) stored,
  esforco          smallint check (esforco between 0 and 10),
  dor              smallint check (dor between 0 and 10),
  leitura          text,
  alertas          text[] not null default '{}',
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.sessoes (
  id               uuid primary key default gen_random_uuid(),
  aluno_id         uuid not null references public.alunos (id) on delete cascade,
  prescricao_id    uuid references public.prescricoes_treino (id) on delete set null,
  semana_id        uuid references public.semanas_treino (id) on delete cascade,
  data             date not null,
  dia_treino       text,
  status           public.sessao_status not null default 'completa',
  origem           text not null default 'lançado depois',
  observacao       text,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.series (
  id               uuid primary key default gen_random_uuid(),
  sessao_id        uuid not null references public.sessoes (id) on delete cascade,
  aluno_id         uuid not null references public.alunos (id) on delete cascade,
  exercicio_id     uuid references public.exercicios (id) on delete set null,
  exercicio_nome   text not null,
  unidade          text not null default 'kg total',
  s1_rep smallint, s2_rep smallint, s3_rep smallint, s4_rep smallint, s5_rep smallint, s6_rep smallint,
  s1_carga numeric(6, 2), s2_carga numeric(6, 2), s3_carga numeric(6, 2),
  s4_carga numeric(6, 2), s5_carga numeric(6, 2), s6_carga numeric(6, 2),
  maior_carga      numeric(6, 2) generated always as (greatest(s1_carga, s2_carga, s3_carga, s4_carga, s5_carga, s6_carga)) stored,
  reps_total       smallint generated always as (
                     (coalesce(s1_rep, 0) + coalesce(s2_rep, 0) + coalesce(s3_rep, 0)
                      + coalesce(s4_rep, 0) + coalesce(s5_rep, 0) + coalesce(s6_rep, 0))::smallint) stored,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

-- ---------------------------------------------------------------- entregas (fila única do que vai ao aluno)
create table public.entregas (
  id                     uuid primary key default gen_random_uuid(),
  aluno_id               uuid not null references public.alunos (id) on delete cascade,
  tipo                   public.entrega_tipo not null,
  status                 public.entrega_status not null default 'RASCUNHO',
  titulo                 text not null,
  versao                 integer,
  dieta_id               uuid references public.dietas (id) on delete set null,
  prescricao_treino_id   uuid references public.prescricoes_treino (id) on delete set null,
  relatorio_id           uuid references public.relatorios (id) on delete set null,
  inicio                 date,
  dias_validade          integer not null default 30 check (dias_validade > 0),
  validade               date generated always as (inicio + dias_validade) stored,
  fim_real               date,
  pdf_path               text,                  -- caminho no bucket "entregas" (privado)
  pdf_nome               text,
  pdf_sha256             text,                  -- impressão digital do PDF: se mudar depois do RT, volta para o RT
  json_path              text,
  texto_envio            text,
  link_whatsapp          text,
  origem                 text not null default 'manual',
  pdf_gerado_em          timestamptz,
  aprovado_em            timestamptz,           -- revisão do Jorge (RASCUNHO → próximo passo)
  aprovado_por           text,
  rt_aprovado_em         timestamptz,           -- aprovação do Responsável Técnico (nutricionista)
  rt_aprovado_por        text,
  rt_pdf_sha256          text,                  -- o PDF exato que o RT aprovou
  rt_observacao          text,
  enviado_em             timestamptz,
  criado_em              timestamptz not null default now(),
  atualizado_em          timestamptz not null default now(),
  -- trava de ouro: dieta, suplementação e receituário só vão para ENVIAR/ENVIADO com a aprovação do RT
  constraint entregas_rt_obrigatorio check (
    not (tipo in ('dieta', 'suplementacao', 'receituario')
         and status in ('ENVIAR', 'ENVIADO')
         and (rt_aprovado_em is null or rt_aprovado_por is null))),
  constraint entregas_enviado_tem_data check (status <> 'ENVIADO' or enviado_em is not null)
);
comment on column public.entregas.status is 'RASCUNHO → (dieta/suplementação/receituário: APROVACAO_RT →) ENVIAR → ENVIADO; DESCARTADO a qualquer momento antes de ENVIADO.';

create table public.itens_suplementacao (
  id               uuid primary key default gen_random_uuid(),
  dieta_id         uuid not null references public.dietas (id) on delete cascade,
  entrega_id       uuid references public.entregas (id) on delete set null,
  suplemento       text not null,
  dose             numeric(8, 2),
  unidade          text,
  medida_caseira   text,
  quando           text,
  para_que         text,
  motivo_tecnico   text,
  situacao         text check (situacao is null or situacao in ('novo', 'mantido', 'ajustado', 'suspenso')),
  desde            date,
  cuidados         text,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);

create table public.aprovacoes_rt (
  id            uuid primary key default gen_random_uuid(),
  entrega_id    uuid not null references public.entregas (id) on delete cascade,
  decisao       text not null check (decisao in ('aprovado', 'devolvido')),
  por           text not null,
  em            timestamptz not null default now(),
  pdf_sha256    text,
  observacao    text
);
comment on table public.aprovacoes_rt is 'Histórico de cada decisão do RT (aprovou ou devolveu), com a impressão digital do PDF.';

create table public.lembretes (
  id                 uuid primary key default gen_random_uuid(),
  aluno_id           uuid references public.alunos (id) on delete cascade,
  titulo             text not null,
  secao              public.lembrete_secao not null default 'proximos_dias',
  motivo             text,
  prazo              date,
  texto_pronto       text,
  minutos_estimados  smallint,
  feito              boolean not null default false,
  feito_em           timestamptz,
  origem             text,
  consulta_id        uuid references public.consultas (id) on delete set null,
  pagamento_id       uuid references public.pagamentos (id) on delete set null,
  lead_id            uuid references public.leads (id) on delete set null,
  entrega_id         uuid references public.entregas (id) on delete set null,
  recebido_id        uuid references public.recebidos (id) on delete set null,
  criado_em          timestamptz not null default now(),
  atualizado_em      timestamptz not null default now(),
  constraint lembretes_feito_tem_data check (not feito or feito_em is not null)
);

create table public.historico (
  id           bigint generated always as identity primary key,
  tabela       text not null,
  registro_id  uuid not null,
  campo        text not null default 'status',
  de           text,
  para         text,
  por          text,
  em           timestamptz not null default now()
);
comment on table public.historico is 'Trilha de auditoria das mudanças de status (quem e quando). Não guarda conteúdo clínico.';

-- ---------------------------------------------------------------- chaves estrangeiras "em círculo" (ligadas no fim)
alter table public.alunos    add constraint alunos_dieta_em_uso_fk  foreign key (dieta_em_uso_id)  references public.dietas (id) on delete set null;
alter table public.alunos    add constraint alunos_treino_em_uso_fk foreign key (treino_em_uso_id) references public.prescricoes_treino (id) on delete set null;
alter table public.checkins  add constraint checkins_dieta_fk       foreign key (dieta_id)         references public.dietas (id) on delete set null;
alter table public.dietas    add constraint dietas_entrega_fk       foreign key (entrega_id)       references public.entregas (id) on delete set null;
alter table public.prescricoes_treino add constraint prescricoes_entrega_fk foreign key (entrega_id) references public.entregas (id) on delete set null;

-- ---------------------------------------------------------------- índices
create index alunos_status_idx           on public.alunos (status);
create index alunos_nome_idx             on public.alunos (lower(nome));
create index leads_etapa_idx             on public.leads (etapa);
create index contratos_aluno_idx         on public.contratos (aluno_id);
create index pagamentos_aluno_idx        on public.pagamentos (aluno_id);
create index pagamentos_situacao_idx     on public.pagamentos (situacao, vencimento);
create index pagamentos_contrato_idx     on public.pagamentos (contrato_id);
create index consultas_data_idx          on public.consultas (data_hora);
create index consultas_aluno_idx         on public.consultas (aluno_id);
create index envios_status_idx           on public.envios (status);
create index envios_aluno_idx            on public.envios (aluno_id);
create index recebidos_status_idx        on public.recebidos (status, recebido_em desc);
create index recebidos_aluno_idx         on public.recebidos (aluno_id);
create index checkins_aluno_semana_idx   on public.checkins (aluno_id, semana_inicio desc);
create index medidas_aluno_data_idx      on public.medidas (aluno_id, data);
create index diario_aluno_idx            on public.diario (aluno_id, data desc);
create index diario_status_idx           on public.diario (status);
create index exames_aluno_idx            on public.exames (aluno_id);
create index marcadores_aluno_idx        on public.marcadores (aluno_id, nome);
create index dietas_aluno_idx            on public.dietas (aluno_id, versao desc);
create index refeicoes_dieta_idx         on public.refeicoes (dieta_id, ordem);
create index relatorios_aluno_idx        on public.relatorios (aluno_id);
create index itens_supl_dieta_idx        on public.itens_suplementacao (dieta_id);
create index entregas_status_idx         on public.entregas (status);
create index entregas_aluno_idx          on public.entregas (aluno_id, criado_em desc);
create index aprovacoes_rt_entrega_idx   on public.aprovacoes_rt (entrega_id);
create index lembretes_abertos_idx       on public.lembretes (feito, prazo);
create index lembretes_aluno_idx         on public.lembretes (aluno_id);
create index prescricoes_aluno_idx       on public.prescricoes_treino (aluno_id);
create index itens_prescricao_idx        on public.itens_prescricao (prescricao_id, dia, ordem);
create index semanas_aluno_idx           on public.semanas_treino (aluno_id, semana_inicio desc);
create index sessoes_aluno_idx           on public.sessoes (aluno_id, data);
create index sessoes_semana_idx          on public.sessoes (semana_id);
create index series_sessao_idx           on public.series (sessao_id);
create index series_aluno_idx            on public.series (aluno_id, exercicio_nome);
create index historico_registro_idx      on public.historico (tabela, registro_id);

-- ---------------------------------------------------------------- travas de status (no próprio banco)
create or replace function public.quem_mudou() returns text
language sql stable as $$
  select coalesce((select nome from public.equipe where user_id = auth.uid()),
                  nullif(current_setting('request.jwt.claims', true), '')::json ->> 'role',
                  current_user::text);
$$;

create or replace function public.entregas_transicao() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  requer_rt boolean := new.tipo in ('dieta', 'suplementacao', 'receituario');
  permitido boolean;
begin
  -- 1) o PDF mudou depois de o RT aprovar: a aprovação cai e a entrega volta para o RT
  if tg_op = 'UPDATE' and requer_rt and old.rt_aprovado_em is not null
     and new.pdf_sha256 is distinct from old.pdf_sha256 then
    new.rt_aprovado_em := null;
    new.rt_aprovado_por := null;
    new.rt_pdf_sha256 := null;
    if new.status in ('ENVIAR') then
      new.status := 'APROVACAO_RT';
    end if;
  end if;

  if tg_op = 'UPDATE' and new.status is distinct from old.status then
    permitido := case
      when old.status = 'RASCUNHO'     and new.status = 'APROVACAO_RT' then requer_rt
      when old.status = 'RASCUNHO'     and new.status = 'ENVIAR'       then not requer_rt
      when old.status = 'APROVACAO_RT' and new.status = 'ENVIAR'       then requer_rt
      when old.status = 'APROVACAO_RT' and new.status = 'RASCUNHO'     then true   -- RT devolveu com nota
      when old.status = 'ENVIAR'       and new.status = 'APROVACAO_RT' then requer_rt  -- PDF trocado (regra 1)
      when old.status = 'ENVIAR'       and new.status = 'RASCUNHO'     then true   -- voltou para corrigir
      when old.status = 'ENVIAR'       and new.status = 'ENVIADO'      then true
      when new.status = 'DESCARTADO'   and old.status <> 'ENVIADO'     then true
      else false
    end;
    if not permitido then
      raise exception 'Transição não permitida na entrega: % → % (tipo %)', old.status, new.status, new.tipo
        using errcode = 'check_violation';
    end if;

    -- quem aprova pelo RT, quando logado pelo Supabase Auth, precisa ter o papel "rt"
    -- (o Painel ST usa a chave service_role, sem usuário: lá a trava é o PIN do RT e o segundo toque)
    if old.status = 'APROVACAO_RT' and new.status = 'ENVIAR' then
      if auth.uid() is not null and not public.e_rt() then
        raise exception 'Só o RT (nutricionista) aprova dieta, suplementação ou receituário.' using errcode = 'insufficient_privilege';
      end if;
      if new.rt_aprovado_em is null then new.rt_aprovado_em := now(); end if;
      if new.rt_aprovado_por is null then new.rt_aprovado_por := public.quem_mudou(); end if;
      new.rt_pdf_sha256 := new.pdf_sha256;
    end if;

    if new.status = 'ENVIADO' then
      if requer_rt and new.rt_pdf_sha256 is distinct from new.pdf_sha256 then
        raise exception 'O PDF mudou depois da aprovação do RT: mande de novo para o RT.' using errcode = 'check_violation';
      end if;
      if new.enviado_em is null then new.enviado_em := now(); end if;
    end if;

    if old.status = 'APROVACAO_RT' and new.status = 'RASCUNHO' then
      new.rt_aprovado_em := null; new.rt_aprovado_por := null; new.rt_pdf_sha256 := null;
    end if;

    insert into public.historico (tabela, registro_id, campo, de, para, por)
    values ('entregas', new.id, 'status', old.status::text, new.status::text, public.quem_mudou());
  end if;
  return new;
end $$;

create trigger entregas_transicao_trg before update on public.entregas
  for each row execute function public.entregas_transicao();

create or replace function public.envios_transicao() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.status is distinct from old.status then
    if not ((old.status = 'PARA_APROVAR' and new.status in ('APROVADO', 'DESCARTADO'))
         or (old.status = 'APROVADO' and new.status in ('ENVIADO', 'PARA_APROVAR', 'DESCARTADO'))
         or (old.status = 'ENVIADO' and new.status = 'DESFEITO')) then
      raise exception 'Transição não permitida na mensagem: % → %', old.status, new.status using errcode = 'check_violation';
    end if;
    if new.status = 'APROVADO' and new.aprovado_em is null then new.aprovado_em := now(); end if;
    if new.status = 'ENVIADO' and new.enviado_em is null then new.enviado_em := now(); end if;
    insert into public.historico (tabela, registro_id, campo, de, para, por)
    values ('envios', new.id, 'status', old.status::text, new.status::text, public.quem_mudou());
  end if;
  return new;
end $$;

create trigger envios_transicao_trg before update on public.envios
  for each row execute function public.envios_transicao();

create or replace function public.diario_transicao() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.status is distinct from old.status then
    if old.status = 'APROVADO' then
      raise exception 'Diário aprovado não muda de status (crie uma nova entrada).' using errcode = 'check_violation';
    end if;
    if new.status = 'APROVADO' and new.aprovado_em is null then new.aprovado_em := now(); end if;
    insert into public.historico (tabela, registro_id, campo, de, para, por)
    values ('diario', new.id, 'status', old.status::text, new.status::text, public.quem_mudou());
  end if;
  return new;
end $$;

create trigger diario_transicao_trg before update on public.diario
  for each row execute function public.diario_transicao();

-- atualizado_em em toda tabela que tem a coluna
do $$
declare t text;
begin
  for t in
    select c.table_name from information_schema.columns c
    join information_schema.tables tb on tb.table_schema = c.table_schema and tb.table_name = c.table_name
    where c.table_schema = 'public' and c.column_name = 'atualizado_em' and tb.table_type = 'BASE TABLE'
  loop
    execute format('create trigger %I before update on public.%I for each row execute function public.tocar_atualizado_em()',
                   t || '_atualizado_em_trg', t);
  end loop;
end $$;

-- ---------------------------------------------------------------- visões (respeitam a RLS de quem consulta)
create view public.v_alunos_resumo with (security_invoker = true) as
select a.id, a.codigo, a.nome, a.status, a.linha, a.tem_dieta, a.tem_treino,
       ck.semana_inicio as ultimo_checkin, ck.score as ultimo_score, ck.peso_semana as ultimo_peso,
       case
         when a.status not in ('ativo', 'renovacao') then null
         when ck.semana_inicio is null or ck.semana_inicio < current_date - 14 then 'mais de 14 dias'
         when ck.semana_inicio < current_date - 8 then 'mais de 8 dias'
       end as checkin_faltando
from public.alunos a
left join lateral (
  select c.semana_inicio, c.score, c.peso_semana from public.checkins c
  where c.aluno_id = a.id order by c.semana_inicio desc limit 1
) ck on true;

create view public.v_entregas_etiqueta with (security_invoker = true) as
select e.*,
       case
         when e.status <> 'ENVIADO' then null
         when e.fim_real is not null then 'substituído'
         when e.validade < current_date then 'vencido'
         when e.validade - current_date <= 5 then 'vencendo'
         else 'vigente'
       end as etiqueta,
       (e.validade - current_date) as dias_para_vencer
from public.entregas e;

-- ---------------------------------------------------------------- segurança por linha (RLS)
-- Liga a RLS em todas as tabelas e dá acesso total só a quem está na equipe (logado).
-- A chave service_role (Painel ST e função do Tally) passa por cima da RLS por definição do Supabase.
-- Nenhuma política para "anon": sem login, nada é lido nem gravado.
do $$
declare t text;
begin
  for t in select tablename from pg_tables where schemaname = 'public' loop
    execute format('alter table public.%I enable row level security', t);
    execute format('revoke all on table public.%I from anon', t);
    if t <> 'equipe' then
      execute format('create policy %I on public.%I for all to authenticated using (public.e_da_equipe()) with check (public.e_da_equipe())',
                     t || '_equipe', t);
    end if;
  end loop;
end $$;

-- a tabela equipe: cada um vê só a própria linha; ninguém logado se promove (só a service_role ou o SQL Editor gravam)
create policy equipe_ve_a_si on public.equipe for select to authenticated using (user_id = auth.uid());

revoke all on all sequences in schema public from anon;
revoke execute on function public.e_da_equipe() from anon;
revoke execute on function public.e_rt() from anon;
revoke all on public.v_alunos_resumo, public.v_entregas_etiqueta from anon;

-- ---------------------------------------------------------------- armazenamento dos PDFs (bucket privado)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('entregas', 'entregas', false, 52428800, array['application/pdf', 'application/json'])
on conflict (id) do update set public = false;

create policy entregas_equipe_le on storage.objects for select to authenticated
  using (bucket_id = 'entregas' and public.e_da_equipe());
create policy entregas_equipe_grava on storage.objects for insert to authenticated
  with check (bucket_id = 'entregas' and public.e_da_equipe());
create policy entregas_equipe_atualiza on storage.objects for update to authenticated
  using (bucket_id = 'entregas' and public.e_da_equipe());
create policy entregas_equipe_apaga on storage.objects for delete to authenticated
  using (bucket_id = 'entregas' and public.e_da_equipe());

-- ---------------------------------------------------------------- configurações iniciais
insert into public.configuracoes (chave, valor, descricao) values
  ('validade_plano_dias',     '30',  'Validade padrão de dieta e treino (dias)'),
  ('aviso_vencendo_dias',     '5',   'A etiqueta vira "vencendo" com esta quantidade de dias ou menos'),
  ('teto_deficit_kcal',       '750', 'Déficit acima disso só com o ok do RT (500 com treino)'),
  ('trava_kcal_minima',       '800', 'Abaixo disso a dieta só sai com justificativa escrita do RT'),
  ('checkin_atrasado_dias',   '8',   'Check-in faltando: amarelo com mais de 8 dias, vermelho com mais de 14'),
  ('rt_obrigatorio_tipos',    'dieta,suplementacao,receituario', 'Tipos de entrega que exigem a aprovação do RT antes do envio')
on conflict (chave) do nothing;

commit;
