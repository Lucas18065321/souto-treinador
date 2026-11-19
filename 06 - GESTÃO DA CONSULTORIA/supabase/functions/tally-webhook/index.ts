// Souto Treinador · Edge Function "tally-webhook"
// Recebe as respostas dos formulários do Tally (anamnese, check-in semanal, check-in de cargas), confere a assinatura
// do Tally (HMAC SHA-256 com o "signing secret") e grava no banco:
//   - sempre: uma linha em `recebidos` (todas as respostas, em JSON e em texto);
//   - anamnese: completa a ficha do aluno (ou cria a ficha, se o link não trouxe o aluno_id) e o aceite da LGPD;
//   - check-in semanal: `checkins` + `medidas` (peso, cintura, quadril) e um lembrete se houver dor ou lesão nova;
//   - check-in de cargas: `semanas_treino`, `sessoes` e `series` (o gráfico de cargas do Painel ST).
//
// Endereço para colar no Tally (Integrations → Webhooks):
//   https://<seu-projeto>.supabase.co/functions/v1/tally-webhook?tipo=anamnese      (ou checkin, cargas, anamnese_treino)
// Segredos (Supabase → Edge Functions → Secrets, ou `npx supabase secrets set`):
//   TALLY_SIGNING_SECRET = o "Signing secret" que o Tally mostra no webhook
//   SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY já existem dentro das funções (o Supabase coloca sozinho).
// Publicar SEM verificação de JWT (o Tally não manda login do Supabase; quem protege é a assinatura):
//   npx supabase functions deploy tally-webhook --no-verify-jwt
//
// Nada de dado de aluno vai para o log: só o tipo, o id da resposta e o resultado.

type Campo = {
  key: string;
  label: string | null;
  type: string;
  value: unknown;
  options?: { id: string; text: string }[];
};
type Payload = {
  eventId?: string;
  eventType?: string;
  createdAt?: string;
  data?: {
    responseId?: string;
    submissionId?: string;
    formId?: string;
    formName?: string;
    createdAt?: string;
    fields?: Campo[];
  };
};

const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const SEGREDO = Deno.env.get("TALLY_SIGNING_SECRET") ?? "";

// ---------------------------------------------------------------- utilidades
function resposta(status: number, corpo: Record<string, unknown>): Response {
  return new Response(JSON.stringify(corpo), { status, headers: { "Content-Type": "application/json; charset=utf-8" } });
}

function norm(s: unknown): string {
  return String(s ?? "")
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .toLowerCase().replace(/\s+/g, " ").replace(/[?:]+$/g, "").trim();
}

function iguais(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a[i] ^ b[i];
  return r === 0;
}

async function assinaturaValida(bruto: string, cabecalho: string | null): Promise<boolean> {
  if (!SEGREDO || !cabecalho) return false;
  const chave = await crypto.subtle.importKey("raw", new TextEncoder().encode(SEGREDO), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", chave, new TextEncoder().encode(bruto)));
  let recebida: Uint8Array;
  try {
    recebida = Uint8Array.from(atob(cabecalho.trim()), (c) => c.charCodeAt(0));
  } catch {
    return false;
  }
  return iguais(mac, recebida);
}

async function rest(metodo: string, rota: string, corpo?: unknown, prefer = "return=representation"): Promise<any> {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/${rota}`, {
    method: metodo,
    headers: {
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      "Content-Type": "application/json",
      Prefer: prefer,
    },
    body: corpo === undefined ? undefined : JSON.stringify(corpo),
  });
  const texto = await r.text();
  if (!r.ok) throw new Error(`banco ${r.status} em ${metodo} ${rota.split("?")[0]}: ${texto.slice(0, 300)}`);
  return texto ? JSON.parse(texto) : null;
}

async function inserir(tabela: string, linha: Record<string, unknown>): Promise<any> {
  const r = await rest("POST", tabela, linha);
  return Array.isArray(r) ? r[0] : r;
}

/** Texto legível de cada campo (escolhas viram o texto da opção; arquivos viram os links). */
function valorTexto(c: Campo): unknown {
  const v = c.value;
  if (v === null || v === undefined || v === "") return null;
  if (Array.isArray(v)) {
    if (c.options?.length) {
      const mapa = new Map(c.options.map((o) => [o.id, o.text]));
      return v.map((x) => (typeof x === "string" ? mapa.get(x) ?? x : x));
    }
    return v.map((x: any) => (x && typeof x === "object" && "url" in x ? x.url : x));
  }
  if (c.options?.length && typeof v === "string") {
    return c.options.find((o) => o.id === v)?.text ?? v;
  }
  return v;
}

function numero(v: unknown): number | null {
  const x = Array.isArray(v) ? v[0] : v;
  if (x === null || x === undefined || x === "") return null;
  const n = Number(String(x).replace(",", "."));
  return Number.isFinite(n) ? n : null;
}

function inteiro(v: unknown, min = 0, max = 99): number | null {
  const n = numero(v);
  return n === null ? null : Math.max(min, Math.min(max, Math.round(n)));
}

function simNao(v: unknown): boolean {
  const x = norm(Array.isArray(v) ? v[0] : v);
  return x === "sim" || x === "true" || x.startsWith("sim ");
}

/** Segunda-feira da semana; respostas de sexta a domingo contam para a semana que está acabando. */
function segunda(iso: string): string {
  const d = new Date(iso);
  const dia = d.getUTCDay(); // 0 = domingo
  const voltar = dia === 0 ? 6 : dia - 1;
  d.setUTCDate(d.getUTCDate() - voltar);
  return d.toISOString().slice(0, 10);
}

// ---------------------------------------------------------------- leitura das respostas
type Lido = { porRotulo: Map<string, unknown>; escondidos: Record<string, string>; legivel: Record<string, unknown>; texto: string };

function ler(campos: Campo[]): Lido {
  const porRotulo = new Map<string, unknown>();
  const escondidos: Record<string, string> = {};
  const legivel: Record<string, unknown> = {};
  const linhas: string[] = [];
  for (const c of campos) {
    const v = valorTexto(c);
    if (c.type === "HIDDEN_FIELDS") {
      if (c.label) escondidos[c.label] = String(c.value ?? "");
      continue;
    }
    if (c.type === "CALCULATED_FIELDS") continue;
    const rotulo = c.label ?? c.key;
    porRotulo.set(norm(rotulo), v);
    legivel[rotulo] = v;
    if (v !== null) linhas.push(`${rotulo}: ${Array.isArray(v) ? v.join(", ") : v}`);
  }
  return { porRotulo, escondidos, legivel, texto: linhas.join("\n") };
}

/** Valor do primeiro rótulo que começa com algum dos prefixos (sem acento, minúsculas). */
function pegar(l: Lido, ...prefixos: string[]): unknown {
  for (const p of prefixos.map(norm)) {
    for (const [k, v] of l.porRotulo) if (k.startsWith(p)) return v;
  }
  return null;
}

async function acharAluno(codigo: string | undefined): Promise<any | null> {
  const c = (codigo ?? "").trim();
  if (!c) return null;
  const filtro = /^[0-9a-f-]{36}$/i.test(c) ? `id=eq.${c}` : `codigo=eq.${encodeURIComponent(c.toUpperCase())}`;
  const r = await rest("GET", `alunos?select=id,nome,status,treino_em_uso_id,dieta_em_uso_id&${filtro}`, undefined, "");
  return r?.[0] ?? null;
}

// ---------------------------------------------------------------- processamento por tipo
async function processarAnamnese(l: Lido, aluno: any | null, quando: string, recebidoId: string, treino: boolean) {
  const nome = String(pegar(l, "nome completo") ?? "").trim();
  const telefone = String(pegar(l, "whatsapp", "telefone") ?? "").replace(/\D/g, "") || null;
  const sexoTxt = norm(pegar(l, "sexo biologico", "sexo"));
  const dados: Record<string, unknown> = {
    nome: nome || undefined,
    primeiro_nome: String(pegar(l, "como prefere ser chamado") ?? "").trim() || (nome ? nome.split(" ")[0] : undefined),
    telefone: telefone ?? undefined,
    email: (pegar(l, "e-mail", "email") as string) || undefined,
    nascimento: (pegar(l, "data de nascimento") as string) || undefined,
    sexo: sexoTxt.startsWith("f") ? "F" : sexoTxt.startsWith("m") ? "M" : undefined,
    altura_cm: numero(pegar(l, "altura")) ?? undefined,
    cidade: (pegar(l, "cidade") as string) || undefined,
  };
  if (!treino) dados.anamnese_recebida_em = quando.slice(0, 10);
  const aceite = pegar(l, "li e aceito o termo", "aceito o termo de consentimento");
  if (aceite && (simNao(aceite) || (Array.isArray(aceite) && aceite.length))) {
    dados.consentimento_lgpd_em = quando;
    dados.consentimento_versao = l.escondidos["termo_versao"] || "v1";
  }
  for (const k of Object.keys(dados)) if (dados[k] === undefined) delete dados[k];

  if (aluno) {
    // só completa o que está vazio: o que o Jorge corrigiu na ficha não é sobrescrito
    const atual = (await rest("GET", `alunos?select=*&id=eq.${aluno.id}`, undefined, ""))[0] ?? {};
    const novos: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(dados)) {
      if (k === "anamnese_recebida_em" || k.startsWith("consentimento") || atual[k] === null || atual[k] === "") novos[k] = v;
    }
    if (atual.etapa_entrada === "anamnese" || atual.etapa_entrada === null) novos.etapa_entrada = "consulta_marcada";
    if (Object.keys(novos).length) await rest("PATCH", `alunos?id=eq.${aluno.id}`, novos);
    return { aluno_id: aluno.id, feito: "ficha completada" };
  }
  if (!nome) return { aluno_id: null, feito: "sem nome: ficou SEM_DONO" };
  const novo = await inserir("alunos", { ...dados, nome, status: "entrada", etapa_entrada: "consulta_marcada" });
  await rest("PATCH", `recebidos?id=eq.${recebidoId}`, { aluno_id: novo.id, status: "NOVO" });
  return { aluno_id: novo.id, feito: "ficha nova criada" };
}

async function processarCheckin(l: Lido, aluno: any, quando: string, recebidoId: string) {
  const pesos: number[] = [];
  for (const [k, v] of l.porRotulo) {
    if (k.startsWith("peso") && k.includes("kg")) {
      const n = numero(v);
      if (n !== null && n > 25 && n < 350) pesos.push(n);
    }
  }
  const peso = pesos.length ? Math.round((pesos.reduce((a, b) => a + b, 0) / pesos.length) * 100) / 100 : null;
  const semana = l.escondidos["semana_inicio"] || segunda(quando);
  const dor = simNao(pegar(l, "teve dor ou lesao nova", "dor ou lesao nova"));
  const alerta = pegar(l, "algum destes sinais");
  const urgente = Array.isArray(alerta) ? alerta.some((x) => !norm(x).startsWith("nenhum")) : alerta ? !norm(alerta).startsWith("nenhum") : false;
  const ck = await inserir("checkins", {
    aluno_id: aluno.id,
    recebido_id: recebidoId,
    dieta_id: aluno.dieta_em_uso_id,
    semana_inicio: semana,
    quinzenal: norm(l.escondidos["quinzenal"]) === "sim",
    peso_semana: peso,
    dias_no_plano: inteiro(pegar(l, "dias seguindo o plano alimentar"), 0, 7),
    dias_leve: inteiro(pegar(l, "dias em que saiu um pouco do plano"), 0, 7),
    dias_grande: inteiro(pegar(l, "dias em que saiu bastante do plano"), 0, 7),
    treinos_feitos: inteiro(pegar(l, "treinos feitos na semana"), 0, 14),
    fome: inteiro(pegar(l, "fome"), 0, 10),
    saciedade: inteiro(pegar(l, "saciedade"), 0, 10),
    sono_horas: numero(pegar(l, "sono: horas", "sono horas")),
    sono_qualidade: inteiro(pegar(l, "sono: qualidade", "sono qualidade"), 0, 10),
    estresse: inteiro(pegar(l, "estresse"), 0, 10),
    agua_l: numero(pegar(l, "agua por dia")),
    cintura_cm: numero(pegar(l, "cintura")),
    quadril_cm: numero(pegar(l, "quadril")),
    dor_lesao_nova: dor,
    troca_pedida: pegar(l, "alguma troca", "troca que voce quer") as string,
    dificuldade: pegar(l, "maior dificuldade") as string,
    pergunta: pegar(l, "sua pergunta", "pergunta") as string,
    nivel: urgente ? "urgente" : dor ? "revisar" : "ok",
    alertas: [...(dor ? ["dor ou lesão nova"] : []), ...(urgente ? ["sinal de alerta"] : [])],
    respostas: l.legivel,
  });
  if (peso !== null || ck.cintura_cm !== null || ck.quadril_cm !== null) {
    await inserir("medidas", {
      aluno_id: aluno.id, checkin_id: ck.id, data: quando.slice(0, 10), peso_kg: peso,
      cintura_cm: ck.cintura_cm, quadril_cm: ck.quadril_cm, origem: "checkin",
    });
  }
  if (urgente || dor) {
    await inserir("lembretes", {
      aluno_id: aluno.id, recebido_id: recebidoId, secao: urgente ? "urgente" : "para_hoje",
      titulo: urgente ? "Check-in com sinal de alerta: falar hoje" : "Check-in com dor ou lesão nova",
      motivo: urgente ? "Sinal de alerta" : "Dor no treino", prazo: quando.slice(0, 10), minutos_estimados: 10, origem: "tally",
    });
    if (urgente) await rest("PATCH", `recebidos?id=eq.${recebidoId}`, { urgente: true });
  }
  return { feito: "check-in + medidas" };
}

async function processarCargas(l: Lido, aluno: any, quando: string, recebidoId: string) {
  const semana = segunda(quando);
  let presc: any = null;
  if (aluno.treino_em_uso_id) {
    presc = (await rest("GET", `prescricoes_treino?select=id,sessoes_por_semana&id=eq.${aluno.treino_em_uso_id}`, undefined, ""))[0];
  }
  const feitos = pegar(l, "quais treinos voce fez");
  const lista = (Array.isArray(feitos) ? feitos : feitos ? [feitos] : []).map(String);
  const dias = lista.map((t) => (t.match(/\b([A-F])\b/) ?? [])[1]).filter(Boolean) as string[];
  const esforco = inteiro(pegar(l, "esforco da semana"), 0, 10);
  const dor = inteiro(pegar(l, "dor durante o treino"), 0, 10);
  const recado = pegar(l, "recado") as string | null;
  const sem = await inserir("semanas_treino", {
    aluno_id: aluno.id, prescricao_id: presc?.id ?? null, recebido_id: recebidoId, semana_inicio: semana,
    planejadas: presc?.sessoes_por_semana ?? null, completas: dias.length, parciais: 0, esforco, dor,
    leitura: [esforco !== null ? `esforço ${esforco}/10` : "", dor !== null ? `dor ${dor}/10` : "", recado ? `recado: ${recado}` : ""]
      .filter(Boolean).join(" · "),
    alertas: dor !== null && dor >= 5 ? ["Dor durante"] : [],
  });
  // exercícios: rótulos "Agachamento livre · carga (kg)" e "Agachamento livre · repetições" (com "A · " na frente, opcional)
  const exs = new Map<string, { dia: string | null; carga: number | null; reps: number[] }>();
  for (const [k, v] of Object.entries(l.legivel)) {
    const m = k.match(/^(?:([A-F])\s*·\s*)?(.+?)\s*·\s*(carga|repeti)/i);
    if (!m) continue;
    const nome = m[2].trim();
    const e = exs.get(nome) ?? { dia: m[1] ?? null, carga: null, reps: [] };
    if (m[3].toLowerCase().startsWith("carga")) e.carga = numero(v);
    else e.reps = (String(v ?? "").match(/\d+/g) ?? []).map(Number).slice(0, 6);
    exs.set(nome, e);
  }
  const sessoes = new Map<string, string>();
  const diasSessao = dias.length ? dias : ["A"];
  for (const d of diasSessao) {
    const s = await inserir("sessoes", {
      aluno_id: aluno.id, prescricao_id: presc?.id ?? null, semana_id: sem.id, data: semana, dia_treino: d,
      status: "completa", origem: "lançado depois", observacao: "Lançada pelo check-in de cargas (o dia exato não é perguntado).",
    });
    sessoes.set(d, s.id);
  }
  let n = 0;
  for (const [nome, e] of exs) {
    if (e.carga === null && !e.reps.length) continue;
    const sessao = sessoes.get(e.dia ?? "") ?? [...sessoes.values()][0];
    const linha: Record<string, unknown> = {
      sessao_id: sessao, aluno_id: aluno.id, exercicio_nome: nome, unidade: e.carga === null ? "peso do corpo" : "kg total",
    };
    const reps = e.reps.length ? e.reps : [null];
    reps.forEach((r, i) => {
      if (r !== null) linha[`s${i + 1}_rep`] = r;
      if (e.carga !== null) linha[`s${i + 1}_carga`] = e.carga;
    });
    await inserir("series", linha);
    n++;
  }
  if (dor !== null && dor >= 5) {
    await inserir("lembretes", {
      aluno_id: aluno.id, recebido_id: recebidoId, secao: "para_hoje", titulo: `Dor ${dor}/10 no treino: falar com o aluno`,
      motivo: "Dor no treino", prazo: quando.slice(0, 10), minutos_estimados: 10, origem: "tally",
    });
  }
  return { feito: `semana + ${sessoes.size} sessões + ${n} exercícios` };
}

// ---------------------------------------------------------------- entrada
const TIPOS: Record<string, string> = {
  anamnese: "anamnese", anamnese_treino: "anamnese_treino", checkin: "checkin_semanal", checkin_semanal: "checkin_semanal",
  checkin_quinzenal: "checkin_quinzenal", cargas: "checkin_cargas", checkin_cargas: "checkin_cargas",
};

Deno.serve(async (req) => {
  if (req.method !== "POST") return resposta(405, { erro: "use POST" });
  if (!SUPABASE_URL || !SERVICE_KEY) return resposta(500, { erro: "função sem SUPABASE_URL/SUPABASE_SERVICE_ROLE_KEY" });
  if (!SEGREDO) return resposta(500, { erro: "falta o segredo TALLY_SIGNING_SECRET" });

  const bruto = await req.text();
  if (bruto.length > 2_000_000) return resposta(413, { erro: "resposta grande demais" });
  if (!(await assinaturaValida(bruto, req.headers.get("tally-signature")))) {
    return resposta(401, { erro: "assinatura do Tally inválida" });
  }

  let p: Payload;
  try {
    p = JSON.parse(bruto);
  } catch {
    return resposta(400, { erro: "JSON inválido" });
  }
  if (p.eventType !== "FORM_RESPONSE" || !p.data) return resposta(200, { ok: true, ignorado: p.eventType ?? "sem evento" });

  const d = p.data;
  const l = ler(d.fields ?? []);
  const url = new URL(req.url);
  const pedido = norm(url.searchParams.get("tipo") || l.escondidos["formulario"] || "");
  const tipo = TIPOS[pedido.replace(/[\s-]+/g, "_")] ??
    (norm(d.formName).includes("carga") ? "checkin_cargas" : norm(d.formName).includes("check") ? "checkin_semanal"
      : norm(d.formName).includes("treino") ? "anamnese_treino" : "anamnese");
  const respostaId = d.responseId || d.submissionId || p.eventId || crypto.randomUUID();
  const quando = d.createdAt || p.createdAt || new Date().toISOString();

  let recId: string | null = null;
  try {
    const ja = await rest("GET", `recebidos?select=id&tally_resposta_id=eq.${encodeURIComponent(respostaId)}`, undefined, "");
    if (ja?.length) return resposta(200, { ok: true, repetido: true });

    const codigo = l.escondidos["aluno_id"] || l.escondidos["aluno"] || "";
    const aluno = await acharAluno(codigo);
    const nomeTitulo = aluno?.nome ?? (pegar(l, "nome completo") as string) ?? l.escondidos["nome"] ?? "sem nome";
    const rec = await inserir("recebidos", {
      aluno_id: aluno?.id ?? null,
      tipo: tipo === "checkin_semanal" && norm(l.escondidos["quinzenal"]) === "sim" ? "checkin_quinzenal" : tipo,
      status: aluno ? "NOVO" : "SEM_DONO",
      origem: "tally",
      titulo: `${tipo.replace(/_/g, " ")} · ${nomeTitulo} · ${quando.slice(0, 10)}`,
      recebido_em: quando,
      semana_inicio: tipo.startsWith("checkin") ? segunda(quando) : null,
      aluno_codigo_informado: codigo || null,
      tally_form_id: d.formId ?? null,
      tally_resposta_id: respostaId,
      respostas: { escondidos: l.escondidos, respostas: l.legivel },
      respostas_texto: l.texto,
    });
    recId = rec.id;

    let resultado: Record<string, unknown> = { feito: "recebido" };
    if (tipo === "anamnese" || tipo === "anamnese_treino") {
      resultado = await processarAnamnese(l, aluno, quando, rec.id, tipo === "anamnese_treino");
    } else if (!aluno) {
      resultado = { feito: "aluno não achado pelo aluno_id do link: ficou SEM_DONO no Painel" };
    } else if (tipo === "checkin_cargas") {
      resultado = await processarCargas(l, aluno, quando, rec.id);
    } else {
      resultado = await processarCheckin(l, aluno, quando, rec.id);
    }
    console.log(`tally-webhook ${tipo} ${respostaId}: ${resultado.feito}`);
    return resposta(200, { ok: true, tipo, ...resultado, aluno_id: undefined });
  } catch (e) {
    console.error(`tally-webhook ${tipo} ${respostaId}: ERRO ${(e as Error).message.slice(0, 200)}`);
    // desfaz o recebido para a nova tentativa do Tally processar tudo de novo
    if (recId) await rest("DELETE", `recebidos?id=eq.${recId}`, undefined, "").catch(() => {});
    // 500 faz o Tally tentar de novo mais tarde (e a trava de resposta repetida evita duplicar)
    return resposta(500, { ok: false, erro: "não consegui gravar; o Tally vai tentar de novo" });
  }
});
