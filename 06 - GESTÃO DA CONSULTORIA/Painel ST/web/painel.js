/* Painel ST · interface. Fala só com o servidor local (127.0.0.1) pelas rotas /api. Nenhuma chave chega aqui. */
(function () {
  "use strict";

  // ---------- utilidades ----------
  const $ = (s, el = document) => el.querySelector(s);
  const h = (v) => String(v == null ? "" : v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const brl = (v) => (v == null ? "—" : new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 }).format(v));
  const num = (v, c = 1) => (v == null ? "—" : Number(v).toLocaleString("pt-BR", { maximumFractionDigits: c }));
  const iso = (v) => (v && typeof v === "object" ? v.start : v) || "";
  const dm = (v) => { const s = iso(v); return s ? `${s.slice(8, 10)}/${s.slice(5, 7)}` : "—"; };
  const PALETA = ["#B9C7FF", "#C9D3F0", "#C9B6E8", "#A9D8C9", "#F2D58A", "#9FD3E8", "#D6DCEF", "#B8E0D2"];
  const cor = (s) => { let n = 0; for (const c of String(s || "")) n = (n * 31 + c.charCodeAt(0)) >>> 0; return PALETA[n % PALETA.length]; };
  const av = (p, cls = "av") => `<span class="${cls}" style="background:${cor(p && p.nome)}">${h(p ? p.iniciais : "?")}</span>`;
  const AZUL = "#6F89F5";

  const I = {
    inicio: '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>',
    hoje: '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/>',
    aprovacoes: '<rect x="4" y="3.5" width="16" height="17" rx="3"/><path d="m8.5 12 2.4 2.4 4.6-4.9"/>',
    alunos: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.8c1.9.7 3.1 2.4 3.5 5.2"/>',
    agenda: '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    leads: '<path d="M3.5 4.5h17l-6.5 8v6l-4 2v-8z"/>',
    financeiro: '<rect x="3" y="6" width="18" height="13" rx="3"/><path d="M3 10h18"/><circle cx="16.5" cy="14.5" r="1.3"/>',
    sistema: '<path d="M3 12h4l2.5-6 5 12 2.5-6h4"/>',
    zap: '<path d="M20.5 11.6a8.4 8.4 0 0 1-12.4 7.4L3.5 20.5l1.6-4.4A8.4 8.4 0 1 1 20.5 11.6z"/>',
    pdf: '<path d="M14 3.5H7a2.5 2.5 0 0 0-2.5 2.5v12A2.5 2.5 0 0 0 7 20.5h10a2.5 2.5 0 0 0 2.5-2.5V9z"/><path d="M14 3.5V9h5.5"/>',
    pasta: '<path d="M3.5 7.5a2 2 0 0 1 2-2h4l2 2.5h7a2 2 0 0 1 2 2v7.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"/>',
    ok: '<path d="M4 12.5 9 17.5 20 6.5"/>',
    seta: '<path d="m9 6 6 6-6 6"/>',
    escudo: '<path d="M12 3 5 6v5.5c0 4.4 3 8.2 7 9.5 4-1.3 7-5.1 7-9.5V6z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
  };
  const ic = (n, w = 1.9) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${I[n] || ""}</svg>`;
  const MENU = [["inicio", "Início"], ["hoje", "Hoje"], ["aprovacoes", "Aprovações"], ["alunos", "Alunos"], ["agenda", "Agenda"], ["leads", "Leads"], ["financeiro", "Financeiro"], ["sistema", "Sistema"]];
  const estado = { contadores: {}, busca: "", filtro: "todos", config: null };
  if (new URLSearchParams(location.search).has("estatico")) document.documentElement.classList.add("estatico");

  // ---------- conversa com o servidor ----------
  const DESLIGADO = "O painel está desligado. Abra de novo pelo atalho Painel ST da área de trabalho.";
  async function api(nome, params = {}) {
    const q = new URLSearchParams(params).toString();
    const r = await fetch(`/api/${nome}${q ? "?" + q : ""}`, { cache: "no-store" }).catch(() => { throw new Error(DESLIGADO); });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.erro || `erro ${r.status}`);
    return j;
  }
  async function post(rota, corpo) {
    const r = await fetch(rota, { method: "POST", headers: { "Content-Type": "application/json", "X-Painel": "1" }, body: JSON.stringify(corpo || {}) })
      .catch(() => { throw new Error(DESLIGADO); });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || j.ok === false) throw new Error(j.erro || `erro ${r.status}`);
    return j;
  }
  let avisoT;
  function aviso(txt, erro) {
    const a = $("#aviso");
    a.textContent = txt; a.classList.toggle("erro", !!erro); a.classList.add("ver");
    clearTimeout(avisoT); avisoT = setTimeout(() => a.classList.remove("ver"), 3600);
  }

  // ---------- desenhos ----------
  function spark(vals, cor1 = AZUL) {
    const v = (vals || []).filter((x) => x != null);
    if (v.length < 2) return '<svg class="spark" viewBox="0 0 200 46" aria-hidden="true"><line x1="0" y1="23" x2="200" y2="23" stroke="rgba(220,228,255,.25)" stroke-dasharray="4 5"/></svg>';
    const mn = Math.min(...v), mx = Math.max(...v), am = mx - mn || 1;
    const pts = v.map((x, i) => [Math.round((i / (v.length - 1)) * 200), Math.round(6 + (1 - (x - mn) / am) * 32)]);
    const linha = pts.map((p) => p.join(",")).join(" ");
    const area = `M${pts[0][0]} ${pts[0][1]} L${pts.map((p) => p.join(" ")).join(" L")} L200 46 L0 46 Z`;
    const id = "g" + Math.random().toString(36).slice(2, 8);
    const u = pts[pts.length - 1];
    return `<svg class="spark" viewBox="0 0 200 46" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="${id}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="${cor1}" stop-opacity=".4"/><stop offset="1" stop-color="${cor1}" stop-opacity="0"/></linearGradient></defs><path d="${area}" fill="url(#${id})"/><polyline points="${linha}" fill="none" stroke="${cor1}" stroke-width="2.2" stroke-linejoin="round" vector-effect="non-scaling-stroke"/><circle cx="${u[0]}" cy="${u[1]}" r="3.6" fill="#F2F4F8"/></svg>`;
  }
  function anel(pct) {
    const c = 301.6, off = c * (1 - Math.max(0, Math.min(100, pct || 0)) / 100);
    return `<svg viewBox="0 0 120 120" aria-hidden="true"><defs><linearGradient id="gr" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#A9B9FF"/><stop offset=".5" stop-color="#5C78EE"/><stop offset="1" stop-color="#1F33A3"/></linearGradient></defs><circle cx="60" cy="60" r="48" fill="none" stroke="rgba(220,228,255,.1)" stroke-width="11"/><circle class="arco" cx="60" cy="60" r="48" fill="none" stroke="url(#gr)" stroke-width="11" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c}" data-off="${off}"/></svg>`;
  }
  function grafico(meds, o = {}) {
    const un = o.un || "kg", rotulo = o.rotulo || "Peso";
    const v = (meds || []).filter((m) => m.peso != null);
    if (v.length < 2) return vazio(o.vazio || "Poucas pesagens para o gráfico.");
    const W = 560, H = 190, P = 34;
    const ps = v.map((m) => m.peso), mn = Math.min(...ps) - 0.5, mx = Math.max(...ps) + 0.5;
    const x = (i) => P + (i / (v.length - 1)) * (W - P - 10), y = (p) => 12 + (1 - (p - mn) / (mx - mn)) * (H - 40);
    const linha = v.map((m, i) => `${x(i).toFixed(1)},${y(m.peso).toFixed(1)}`).join(" ");
    const area = `M${x(0)} ${y(v[0].peso)} L${v.map((m, i) => `${x(i).toFixed(1)} ${y(m.peso).toFixed(1)}`).join(" L")} L${x(v.length - 1)} ${H - 28} L${x(0)} ${H - 28} Z`;
    const grade = [mx, (mx + mn) / 2, mn].map((g) => `<line x1="${P}" x2="${W - 10}" y1="${y(g)}" y2="${y(g)}" stroke="rgba(220,228,255,.08)"/><text x="${P - 6}" y="${y(g) + 4}" text-anchor="end" fill="rgba(222,228,242,.55)" font-size="10.5">${num(g)}</text>`).join("");
    const pontos = v.map((m, i) => `<circle cx="${x(i)}" cy="${y(m.peso)}" r="${i === v.length - 1 ? 4.5 : 3}" fill="${i === v.length - 1 ? "#F2F4F8" : AZUL}"><title>${dm(m.data)}: ${num(m.peso)} ${un}</title></circle>`).join("");
    const gid = "gp" + Math.random().toString(36).slice(2, 7);
    return `<svg class="grafico" viewBox="0 0 ${W} ${H}" role="img" aria-label="${h(rotulo)} de ${num(v[0].peso)} para ${num(v[v.length - 1].peso)} ${un}"><defs><linearGradient id="${gid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="${AZUL}" stop-opacity=".38"/><stop offset="1" stop-color="${AZUL}" stop-opacity="0"/></linearGradient></defs>${grade}<path d="${area}" fill="url(#${gid})"/><polyline points="${linha}" fill="none" stroke="${AZUL}" stroke-width="2.4" stroke-linejoin="round"/>${pontos}<text x="${x(0)}" y="${H - 8}" fill="rgba(222,228,242,.55)" font-size="10.5">${dm(v[0].data)}</text><text x="${x(v.length - 1)}" y="${H - 8}" text-anchor="end" fill="rgba(222,228,242,.55)" font-size="10.5">${dm(v[v.length - 1].data)}</text></svg>`;
  }
  const semana = (d) => { const [no, lv, gr] = d || [0, 0, 0]; const c = []; for (let i = 0; i < 7; i++) c.push(i < no ? "on" : i < no + lv ? "meio" : i < no + lv + gr ? "fora" : ""); return `<div class="semana" aria-label="${no} de 7 dias no plano">${c.map((k) => `<i class="${k}"></i>`).join("")}</div>`; };
  const chipScore = (s) => (s == null ? '<span class="chip c-neutro">sem score</span>' : s >= 80 ? `<span class="chip c-ok">score ${s}</span>` : s >= 60 ? `<span class="chip c-rev">score ${s}</span>` : `<span class="chip c-urg">score ${s}</span>`);
  const icoTipo = { diario: ["D", "i-diario"], entrega: ["E", "i-entrega"], envio: ["M", "i-envio"], rt: ["RT", "i-rt"] };
  const ROT_ACAO = {
    diario_aprovar: "Aprovar", diario_aprovar_rt: "Aprovar como RT", entrega_para_rt: "Revisado: mandar para o RT",
    entrega_aprovar: "Aprovar", entrega_aprovar_rt: "Aprovar como RT", entrega_devolver_rt: "Devolver com nota",
    entrega_enviada: "Marcar enviado", envio_aprovar: "Aprovar", envio_enviado: "Marcar enviado", lembrete_feito: "Feito",
  };
  const DO_RT = new Set(["diario_aprovar_rt", "entrega_aprovar_rt", "entrega_devolver_rt"]);
  const botaoAcao = (acao, id, cls) => `<button class="${cls || (acao === "entrega_devolver_rt" ? "btn btn-vidro" : "btn btn-azul")}" data-acao="${h(acao)}" data-id="${h(id)}">${DO_RT.has(acao) ? ic("escudo") + " " : ""}${h(ROT_ACAO[acao] || "Ok")}</button>`;
  const vazio = (t) => `<p class="vazio">${h(t)}</p>`;
  const chipStatus = (st, txt) => `<span class="chip ${st === "APROVACAO_RT" ? "c-rt" : st === "RASCUNHO" || st === "PARA_APROVAR" || st === "EM_REVISAO" ? "c-rev" : "c-azul"}">${h(txt || st)}</span>`;

  // ---------- telas ----------
  async function tInicio(fresco) {
    const d = await api("inicio", fresco ? { fresco: 1 } : {});
    estado.contadores = d.contadores; menu();
    const ds = d.destaque || {};
    const destaque = `<article class="destaque ${ds.tipo === "calmo" ? "calmo" : ""}" style="--i:0">
      <div style="position:relative;z-index:1">
        <div class="etq">${ds.tipo === "urgente" ? "<span>● Urgente</span>" : ds.tipo === "consulta" ? "<span>Agenda</span>" : "<span>Tudo em ordem</span>"}${ds.aluno ? `<span class="vid">${h(ds.aluno.nome)}</span>` : ""}</div>
        <h3>${h(ds.titulo)}</h3><p>${h(ds.texto)}</p>
        <div class="botoes">${ds.aluno ? `<a class="btn btn-claro" href="#aluno/${h(ds.aluno.id)}">Abrir ficha</a>` : '<a class="btn btn-claro" href="#aprovacoes">Ir para aprovações</a>'}${ds.acao ? botaoAcao(ds.acao.acao, ds.acao.id, "btn btn-vidro") : '<a class="btn btn-vidro" href="#hoje">Ver o dia</a>'}</div>
      </div>
      <div class="contador"><div class="n">${h(d.contadores.aprovar)}</div><div class="l">${d.contadores.aprovar === 1 ? "item para aprovar" : "itens para aprovar"}</div>
        <div class="s"><span>${h(d.contadores.rt)} com o RT</span><span>${h(d.contadores.urgentes)} urgente${d.contadores.urgentes === 1 ? "" : "s"}</span><span>${h(d.contadores.hoje)} para hoje</span><span>${h(d.contadores.recebidos)} recebido${d.contadores.recebidos === 1 ? "" : "s"}</span></div></div>
    </article>`;
    const aprovar = d.aprovar.length ? d.aprovar.map((x, i) => `<div class="linha vidro erguer" style="--i:${i + 1}"><span class="ico ${icoTipo[x.tipo][1]}">${icoTipo[x.tipo][0]}</span><div style="min-width:0"><div class="tit">${h(x.titulo)}</div><div class="sub">${h(x.aluno ? x.aluno.primeiro + " · " : "")}${h(x.sub)}</div></div><a class="btn btn-vidro" href="#aprovacoes">Ver</a></div>`).join("") : vazio("Nada esperando a sua aprovação.");
    const cks = d.checkins.length ? d.checkins.map((c, i) => `<a class="ck vidro erguer" style="--i:${i + 2};text-decoration:none" href="#aluno/${h(c.aluno.id)}">
        <div class="ck-topo">${av(c.aluno)}<div style="min-width:0"><div class="ck-nome">${h(c.aluno.nome)}</div><div class="ck-sub">${h(c.linha || "")} · semana de ${dm(c.semana)}</div></div>${chipScore(c.score)}</div>
        ${semana(c.dias)}${spark(c.pesos)}<div class="num-linha"><b>${c.peso != null ? num(c.peso) + " kg" : "—"}</b><span>${c.treinos != null ? h(c.treinos) + " treino" + (c.treinos === 1 ? "" : "s") : h(c.nivel || "")}</span></div></a>`).join("") : vazio("Nenhum check-in ainda.");
    const op = d.operacao;
    const agenda = d.agenda.length ? d.agenda.map((e) => `<div class="evento vidro erguer"><div class="hora">${h(e.hora)}<small>${h(e.dia)}</small></div><div style="min-width:0"><div class="tit">${h(e.tipo_txt)} · ${h(e.aluno ? e.aluno.primeiro : "")}</div><div class="sub">${h(e.alerta || e.status || "")}</div></div>${e.link ? `<a class="circ" href="${h(e.link)}" target="_blank" rel="noopener" aria-label="Abrir a reunião">${ic("seta", 2.4)}</a>` : ""}</div>`).join("") : vazio("Nenhum horário marcado nos próximos dias.");
    const f = d.financeiro, mx = Math.max(1, ...f.meses.map((m) => m.valor));
    const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
    const barras = f.meses.map((m, i) => `<div><i class="${i === f.meses.length - 1 ? "atual" : ""}" style="height:${Math.max(4, Math.round((m.valor / mx) * 100))}%;animation-delay:${i * 70}ms" title="${brl(m.valor)}"></i><span>${MESES[+m.mes.slice(5, 7) - 1]}</span></div>`).join("");
    $("#tela").innerHTML = `<div class="grade cascata">
      <div class="col">${destaque}
        <section style="--i:2"><div class="cab"><h2>Check-ins da semana</h2><a href="#alunos">ver todos</a></div><div class="cards cascata">${cks}</div></section>
        <section style="--i:3"><div class="cab"><h2>Agenda</h2><a href="#agenda">abrir agenda</a></div><div class="linhas">${agenda}</div></section>
      </div>
      <div class="col">
        <section style="--i:1"><div class="cab"><h2>Para aprovar</h2><a href="#aprovacoes">ver todos</a></div><div class="linhas cascata">${aprovar}</div></section>
        <section class="stat vidro" style="--i:2"><div class="cab" style="width:100%;margin:0"><h2>Sua operação</h2><a href="#sistema">sistema</a></div>
          <div class="anel">${anel(op.adesao || 0)}<div class="centro"><small>adesão média</small><b>${op.adesao == null ? "—" : op.adesao + "%"}</b><span>${h(op.ativos)} ativo${op.ativos === 1 ? "" : "s"}${op.meta_alvo ? " · meta " + h(op.meta_alvo) : ""}</span></div></div>
          <div class="mini"><div><span class="bola" style="color:var(--lead)">${ic("leads", 2)}</span><b>${h(op.leads)}</b><span>leads no funil</span></div><div><span class="bola" style="color:var(--ok)">${ic("alunos", 2)}</span><b>${h(op.alunos)}</b><span>alunos na base</span></div><div><span class="bola" style="color:var(--atencao)">${ic("hoje", 2)}</span><b>${h(op.renovacoes)}</b><span>renovações chegando</span></div></div>
        </section>
        <section class="vidro bloco" style="--i:3"><div class="cab"><h2>Financeiro</h2><a href="#financeiro">abrir</a></div><div class="barras">${barras}</div>
          <div class="kpis" style="margin-top:12px"><div class="kpi vidro"><small>recebido no mês</small><b>${brl(f.recebido_mes)}</b></div><div class="kpi vidro"><small>vencidos</small><b class="${f.vencidos ? "alerta" : ""}">${brl(f.vencidos)}</b></div></div>
        </section>
      </div></div>`;
    $("#gente").innerHTML = `<div class="bloco-gente vidro"><span class="avg eu">ST</span><span class="r">alunos</span>${d.gente.alunos.map((p) => `<a class="avg ${p.estado}" href="#aluno/${h(p.id)}" style="background:${cor(p.nome)}" title="${h(p.nome)} · ${h(p.status || "")}">${h(p.iniciais)}</a>`).join("")}</div>
      ${d.gente.leads.length ? `<div class="bloco-gente vidro"><span class="r">leads<br>no funil</span>${d.gente.leads.map((l) => `<a class="avg lead" href="#leads" style="background:${cor(l.nome)}" title="${h(l.nome)} · ${h(l.etapa)}">${h(l.iniciais)}</a>`).join("")}</div>` : ""}`;
    requestAnimationFrame(() => document.querySelectorAll(".arco").forEach((a) => { a.style.strokeDashoffset = a.dataset.off; }));
  }

  async function tHoje(fresco) {
    const d = await api("hoje", fresco ? { fresco: 1 } : {});
    const lem = (l) => `<div class="linha vidro erguer"><span class="ico ${l.atrasado ? "i-envio" : "i-diario"}">${l.minutos ? h(l.minutos) + "′" : "•"}</span><div style="min-width:0"><div class="tit">${h(l.titulo)}</div><div class="sub">${h(l.motivo || "")}${l.aluno ? " · " + h(l.aluno.primeiro) : ""} · prazo ${dm(l.prazo)}${l.atrasado ? " · atrasado" : ""}</div></div>${botaoAcao("lembrete_feito", l.id, "btn btn-ok")}</div>`;
    const sec = (nome, cls) => { const l = d.secoes[nome] || []; return `<section><div class="cab"><h2><span class="chip ${cls}">${h(nome)}</span></h2><span class="link">${l.length}</span></div><div class="linhas cascata">${l.length ? l.map(lem).join("") : vazio("Nada aqui.")}</div></section>`; };
    const recs = d.recebidos.length ? d.recebidos.map((r) => `<div class="linha vidro erguer"><span class="ico i-entrega">${h((r.tipo || "?")[0])}</span><div style="min-width:0"><div class="tit">${h(r.titulo)}</div><div class="sub">${h(r.status)} · analisar até ${dm(r.prazo)}${r.atrasado ? " · atrasado" : ""}</div></div>${r.aluno ? `<a class="btn btn-vidro" href="#aluno/${h(r.aluno.id)}">Ficha</a>` : '<span class="chip c-rev">sem aluno</span>'}</div>`).join("") : vazio("Nada novo chegou.");
    const cons = d.consultas.length ? d.consultas.map((e) => `<div class="evento vidro"><div class="hora">${h(e.hora)}</div><div><div class="tit">${h(e.tipo_txt)} · ${h(e.aluno ? e.aluno.primeiro : "")}</div><div class="sub">${h(e.alerta || e.status || "")}</div></div>${e.link ? `<a class="circ" href="${h(e.link)}" target="_blank" rel="noopener" aria-label="Abrir a reunião">${ic("seta", 2.4)}</a>` : ""}</div>`).join("") : vazio("Nenhum horário hoje.");
    $("#tela").innerHTML = `<h1>Hoje</h1><div class="grade"><div class="col">${sec("Urgente", "c-urg")}${sec("Para hoje", "c-azul")}${sec("Próximos dias", "c-neutro")}</div>
      <div class="col"><section><div class="cab"><h2>Horários de hoje</h2><a href="#agenda">agenda</a></div><div class="linhas">${cons}</div></section>
      <section><div class="cab"><h2>Recebidos para analisar</h2></div><div class="linhas cascata">${recs}</div></section></div></div>`;
  }

  async function tAprovacoes(fresco) {
    const d = await api("aprovacoes", fresco ? { fresco: 1 } : {});
    const nomes = { todos: "Todos", rt: "Aprovação do RT", entrega: "Planos e entregas", diario: "Diários", envio: "Mensagens" };
    const itens = d.itens.filter((x) => estado.filtro === "todos" || x.tipo === estado.filtro);
    const rtNome = `${d.rt.nome} · ${d.rt.profissao} · ${d.rt.registro}`;
    const blocoRT = (x) => (x.tipo !== "rt" ? "" : `<div class="rt-faixa"><b>Decisão do RT (${h(rtNome)}).</b> Prescrição dietética é ato privativo do nutricionista: só o RT aprova ou devolve. Abra o PDF, confira e decida.${d.pin_rt ? " Digite o PIN do RT para confirmar." : ""}</div>
        <div class="pin">${d.pin_rt ? `<input type="password" inputmode="numeric" autocomplete="off" placeholder="PIN do RT" data-pin="${h(x.id)}" aria-label="PIN do RT">` : ""}<input class="nota" type="text" maxlength="500" placeholder="Nota do RT (obrigatória para devolver)" data-nota="${h(x.id)}" aria-label="Nota do RT"></div>`);
    const card = (x, i) => `<details class="aprov vidro" style="--i:${i}" ${x.tipo === "rt" && i === 0 ? "open" : ""}><summary><span class="ico ${icoTipo[x.tipo][1]}">${icoTipo[x.tipo][0]}</span><div style="min-width:0"><div class="tit">${h(x.titulo)}</div><div class="sub">${h(x.aluno ? x.aluno.nome + " · " : "")}${h(x.sub)}</div></div>${chipStatus(x.status, x.status_txt)}</summary>
      <div class="corpo">${x.texto ? `<div class="texto-longo">${h(x.texto)}</div>` : '<p class="vazio">Sem texto.</p>'}
        ${blocoRT(x)}
        <div class="botoes">${x.acoes.map((a) => botaoAcao(a, x.id)).join("")}${x.whatsapp && (x.status === "ENVIAR" || x.status === "APROVADO") ? `<a class="btn btn-vidro" href="${h(x.whatsapp)}" data-texto="${h(x.texto)}" target="_blank" rel="noopener">${ic("zap")} 1 · Abrir no WhatsApp</a>${x.tem_pdf && x.status === "ENVIAR" ? `<button class="btn btn-vidro" data-pdf="abrir_pasta" data-id="${h(x.id)}">${ic("pasta")} 2 · Abrir na pasta</button><button class="btn btn-vidro" data-pdf="copiar_pdf" data-id="${h(x.id)}" title="Põe o PDF na área de transferência: Ctrl+V na conversa anexa">Copiar PDF</button>` : ""}` : ""}${x.tem_pdf ? `<a class="btn btn-vidro" href="/api/pdf?id=${h(x.id)}" target="_blank" rel="noopener">${ic("pdf")} Ver PDF</a>` : ""}${x.aluno ? `<a class="btn btn-vidro" href="#aluno/${h(x.aluno.id)}">Ficha</a>` : ""}</div>
        ${x.acoes.includes("entrega_enviada") || x.acoes.includes("envio_enviado") ? '<p class="sub" style="white-space:normal">1 · Abrir no WhatsApp: a conversa abre com o texto, que também fica copiado (se não aparecer, Ctrl+V). 2 · Abrir na pasta: o PDF aparece selecionado, é só arrastar para a conversa (ou use Copiar PDF e Ctrl+V). Mande e toque em "Marcar enviado".</p>' : ""}
        ${x.acoes.includes("entrega_para_rt") ? '<p class="sub" style="white-space:normal">Depois da sua revisão, o plano vai para a APROVAÇÃO DO RT. Só com a aprovação dele ele pode ser enviado ao aluno.</p>' : ""}</div></details>`;
    $("#tela").innerHTML = `<div class="cab"><h1>Aprovações</h1><span class="link">${d.itens.length} no total</span></div>
      <div class="filtros">${Object.entries(nomes).map(([k, v]) => `<button class="filtro vidro ${estado.filtro === k ? "ativo" : ""}" data-filtro="${k}">${v} <span style="opacity:.7">${k === "todos" ? d.itens.length : d.itens.filter((x) => x.tipo === k).length}</span></button>`).join("")}</div>
      <div class="linhas cascata">${itens.length ? itens.map(card).join("") : vazio("Nada esperando aprovação aqui.")}</div>`;
  }

  async function tAlunos(fresco) {
    const d = await api("alunos", fresco ? { fresco: 1 } : {});
    const b = estado.busca.trim().toLowerCase();
    const lista = d.alunos.filter((p) => !b || `${p.nome} ${p.codigo || ""}`.toLowerCase().includes(b));
    const chipSt = (s) => `<span class="chip ${s === "Ativo" ? "c-ok" : s === "Renovação" ? "c-azul" : s === "Encerrado" ? "c-neutro" : "c-rev"}">${h(s || "—")}</span>`;
    $("#tela").innerHTML = `<div class="cab"><h1>Alunos</h1><span class="link">${lista.length} de ${d.alunos.length}${b ? ` · busca: "${h(estado.busca)}"` : ""}</span></div>
      <div class="lista-pac cascata">${lista.length ? lista.map((p, i) => `<a class="pac vidro erguer" style="--i:${i}" href="#aluno/${h(p.id)}"><div class="ck-topo">${av(p)}<div style="min-width:0"><div class="ck-nome">${h(p.nome)}</div><div class="ck-sub">${h(p.linha || "")}${p.tem_dieta ? " · com dieta" : ""}</div></div>${chipSt(p.status)}</div>
        <div class="dados"><span>último check-in<b>${dm(p.ultimo_checkin)}</b></span><span>score<b>${p.score == null ? "—" : h(p.score)}</b></span><span>peso<b>${p.peso == null ? "—" : num(p.peso)}</b></span></div>${p.faltando ? `<span class="chip c-rev">${h(p.faltando)}</span>` : ""}</a>`).join("") : vazio("Nenhum aluno com esse nome.")}</div>`;
  }

  async function tAluno(id, fresco) {
    const p = await api("aluno", fresco ? { id, fresco: 1 } : { id });
    const ult = p.medidas.filter((m) => m.peso != null);
    const var_ = ult.length > 1 ? ult[ult.length - 1].peso - ult[0].peso : null;
    const versoes = p.dietas.length ? p.dietas.map((x) => `<div class="versao vidro ${x.em_uso ? "em-uso" : ""}"><span class="v">v${h(x.versao)}</span><div style="min-width:0"><div class="tit">${h(x.fase || "")} · ${num(x.kcal, 0)} kcal ${x.em_uso ? '<span class="chip c-azul">em uso</span>' : ""}</div><div class="sub">P ${num(x.p, 0)} · C ${num(x.c, 0)} · G ${num(x.g, 0)} · ${h(x.status || "")} ${x.inicio ? "· " + dm(x.inicio) + " a " + dm(x.validade) : ""}</div></div><span></span></div>`).join("") : vazio(p.tem_dieta ? "Nenhuma dieta ainda." : "Aluno sem dieta (só treino).");
    const entregas = p.entregas.length ? p.entregas.map((e) => `<div class="linha vidro"><span class="ico ${e.status === "APROVACAO_RT" ? "i-rt" : "i-entrega"}">${e.status === "APROVACAO_RT" ? "RT" : h((e.tipo || "?")[0])}</span><div style="min-width:0"><div class="tit">${h(e.titulo)}</div><div class="sub">${h(e.status_txt)}${e.etiqueta ? " · " + h(e.etiqueta) : ""}${e.rt ? " · aprovado pelo RT" : ""}</div></div><div class="botoes" style="margin:0">${e.whatsapp && e.status === "ENVIAR" ? `<a class="btn btn-vidro" href="${h(e.whatsapp)}" data-texto="${h(e.texto)}" target="_blank" rel="noopener" title="Abrir no WhatsApp com o texto">${ic("zap")}</a>` : ""}${e.tem_pdf ? `<button class="btn btn-vidro" data-pdf="abrir_pasta" data-id="${h(e.id)}" title="Abrir a pasta com o PDF selecionado (arraste para o WhatsApp)">${ic("pasta")}</button><a class="btn btn-vidro" href="/api/pdf?id=${h(e.id)}" target="_blank" rel="noopener" title="Ver o PDF">${ic("pdf")}</a>` : ""}</div></div>`).join("") : vazio("Nenhuma entrega.");
    const cks = p.checkins.length ? `<div class="tabela"><table><thead><tr><th>Semana</th><th>Score</th><th>Dias no plano</th><th>Treinos</th><th>Peso</th></tr></thead><tbody>${p.checkins.map((c) => `<tr><td>${dm(c.semana)}</td><td class="n">${c.score == null ? "—" : h(c.score)}</td><td class="n">${c.dias_no_plano == null ? "—" : h(c.dias_no_plano) + " de 7"}</td><td class="n">${c.treinos == null ? "—" : h(c.treinos)}</td><td class="n">${c.peso == null ? "—" : num(c.peso)}</td></tr>`).join("")}</tbody></table></div>` : vazio("Nenhum check-in.");
    const lems = p.lembretes.length ? p.lembretes.map((l) => `<div class="linha vidro"><span class="ico i-envio">!</span><div style="min-width:0"><div class="tit">${h(l.titulo)}</div><div class="sub">${h(l.secao || "")} · ${dm(l.prazo)}</div></div>${botaoAcao("lembrete_feito", l.id, "btn btn-ok")}</div>`).join("") : vazio("Nenhum lembrete aberto.");
    const cargas = p.cargas || {};
    const exs = Object.keys(cargas).sort((a, b) => (cargas[a][0].un === "kg" ? 0 : 1) - (cargas[b][0].un === "kg" ? 0 : 1) || a.localeCompare(b, "pt"));
    const grafCarga = (n) => { const l = cargas[n], u = l[l.length - 1];
      return grafico(l.map((x) => ({ data: x.data, peso: x.valor })), { un: u.un, rotulo: n, vazio: "Só 1 semana registrada: a linha aparece a partir da 2ª." })
        + `<p class="sub" style="margin-top:6px">semana de ${dm(u.data)}: ${num(u.valor)} ${h(u.un)}${u.reps && u.un === "kg" ? " · repetições " + h(u.reps) : ""}</p>`; };
    const treino = p.tem_treino ? `<section class="vidro bloco" style="--i:1"><div class="cab"><h2>Cargas do treino</h2>${exs.length ? `<select id="sel-carga" class="sel-carga" aria-label="Exercício">${exs.map((n) => `<option>${h(n)}</option>`).join("")}</select>` : ""}</div><div id="graf-carga">${exs.length ? grafCarga(exs[0]) : vazio("As cargas aparecem aqui depois do 1º check-in de cargas.")}</div></section>` : "";
    const diario = p.diario.length ? p.diario.map((x) => `<div class="linha vidro"><span class="ico i-diario">D</span><div style="min-width:0"><div class="tit">${dm(x.data)} · ${h(x.tipo || "")}</div><div class="sub">${h(x.status || "")} · ${h(x.conduta || "")}</div></div><span></span></div>`).join("") : vazio("Nenhuma entrada no Diário.");
    $("#tela").innerHTML = `<a class="link" href="#alunos">← Alunos</a>
      <div class="ficha-topo vidro">${av(p)}<div class="info"><h1>${h(p.nome)}</h1><div class="tags"><span class="chip c-neutro">${h(p.codigo || "")}</span><span class="chip c-neutro">${h(p.status || "")}</span>${p.linha ? `<span class="chip c-neutro">${h(p.linha)}</span>` : ""}${p.tem_treino ? '<span class="chip c-ok">treino</span>' : ""}${p.tem_dieta ? '<span class="chip c-azul">dieta (RT)</span>' : ""}${p.dia_checkin ? `<span class="chip c-neutro">check-in: ${h(p.dia_checkin)}</span>` : ""}${p.consentimento ? '<span class="chip c-ok">termo LGPD aceito</span>' : '<span class="chip c-urg">falta o termo LGPD</span>'}</div>${p.objetivo ? `<p class="sub" style="white-space:normal;margin-top:8px">${h(p.objetivo)}</p>` : ""}</div>
        <div class="botoes" style="margin:0">${p.whatsapp ? `<a class="btn btn-azul" href="${h(p.whatsapp)}" target="_blank" rel="noopener" title="Abre a conversa, sem texto. Para mandar um plano, use os botões da entrega.">${ic("zap")} Conversa</a>` : ""}</div></div>
      <div class="grade cascata"><div class="col">
        <section class="vidro bloco" style="--i:0"><div class="cab"><h2>Peso</h2><span class="link">${var_ == null ? "" : (var_ > 0 ? "+" : "") + num(var_) + " kg no período"}</span></div>${grafico(p.medidas)}</section>
        ${treino}
        <section class="vidro bloco" style="--i:1"><div class="cab"><h2>Check-ins</h2></div>${cks}</section>
      </div><div class="col">
        <section style="--i:1"><div class="cab"><h2>Planos alimentares</h2><span class="link">prescrição do RT</span></div><div class="linhas">${versoes}</div></section>
        <section style="--i:2"><div class="cab"><h2>Entregas</h2></div><div class="linhas">${entregas}</div></section>
        <section style="--i:3"><div class="cab"><h2>Lembretes</h2></div><div class="linhas">${lems}</div></section>
        <section style="--i:4"><div class="cab"><h2>Diário</h2></div><div class="linhas">${diario}</div></section>
      </div></div>`;
    const sel = $("#sel-carga");
    if (sel) sel.addEventListener("change", () => { $("#graf-carga").innerHTML = grafCarga(sel.value); });
  }

  async function tLeads(fresco) {
    const d = await api("leads", fresco ? { fresco: 1 } : {});
    const temp = (t) => `<span class="chip ${t === "Quente" ? "c-urg" : t === "Morno" ? "c-rev" : "c-neutro"}">${h(t || "—")}</span>`;
    $("#tela").innerHTML = `<div class="cab"><h1>Leads</h1><span class="link">funil comercial</span></div>
      <div class="quadro cascata">${Object.entries(d.etapas).map(([etapa, ls], i) => `<div class="coluna vidro" style="--i:${i}"><h3>${h(etapa)} <span>${ls.length}</span></h3>${ls.length ? ls.map((l) => `<div class="lead-card vidro erguer"><div class="ck-topo">${av(l)}<div style="min-width:0"><div class="ck-nome">${h(l.nome)}</div><div class="ck-sub">${h(l.origem || "")}${l.linha ? " · " + h(l.linha) : ""}</div></div></div>${l.problema ? `<div class="sub" style="white-space:normal">${h(l.problema)}</div>` : ""}<div class="ck-topo">${temp(l.temperatura)}${l.followup ? `<span class="chip ${l.atrasado ? "c-urg" : "c-neutro"}" style="margin-left:0">follow-up ${dm(l.followup)}</span>` : ""}</div>${l.whatsapp ? `<div class="botoes" style="margin:0"><a class="btn btn-vidro" href="${h(l.whatsapp)}" target="_blank" rel="noopener">${ic("zap")} Conversa</a></div>` : ""}</div>`).join("") : '<p class="vazio">—</p>'}</div>`).join("")}</div>`;
  }

  async function tFinanceiro(fresco) {
    const f = await api("financeiro", fresco ? { fresco: 1 } : {});
    const mx = Math.max(1, ...f.meses.map((m) => m.valor));
    const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
    const lin = (p) => `<div class="linha vidro"><span class="ico ${p.situacao === "Pago" ? "i-diario" : p.situacao === "Previsto" ? "i-entrega" : "i-envio"}">R$</span><div style="min-width:0"><div class="tit">${h(p.titulo)}</div><div class="sub">${h(p.situacao)} · ${p.pago_em ? "pago " + dm(p.pago_em) : "vence " + dm(p.vencimento)} ${p.forma ? "· " + h(p.forma) : ""}</div></div><b style="font-family:var(--display);font-variant-numeric:tabular-nums">${brl(p.valor)}</b></div>`;
    $("#tela").innerHTML = `<h1>Financeiro</h1>
      <div class="kpis cascata"><div class="kpi vidro" style="--i:0"><small>recebido no mês</small><b>${brl(f.recebido_mes)}</b></div><div class="kpi vidro" style="--i:1"><small>a receber em 7 dias</small><b>${brl(f.a_receber_7d)}</b></div><div class="kpi vidro" style="--i:2"><small>vencidos</small><b class="${f.vencidos ? "alerta" : ""}">${brl(f.vencidos)}</b></div></div>
      <section class="vidro bloco"><div class="cab"><h2>Recebido por mês</h2></div><div class="barras" style="height:160px">${f.meses.map((m, i) => `<div><i class="${i === f.meses.length - 1 ? "atual" : ""}" style="height:${Math.max(3, Math.round((m.valor / mx) * 100))}%;animation-delay:${i * 70}ms" title="${brl(m.valor)}"></i><span>${MESES[+m.mes.slice(5, 7) - 1]} · ${brl(m.valor)}</span></div>`).join("")}</div></section>
      <div class="grade"><div class="col"><section><div class="cab"><h2>Vencidos</h2></div><div class="linhas">${f.vencidos_lista.length ? f.vencidos_lista.map(lin).join("") : vazio("Nenhum pagamento vencido.")}</div></section>
        <section><div class="cab"><h2>Próximos</h2></div><div class="linhas">${f.proximos.length ? f.proximos.map(lin).join("") : vazio("Nenhum pagamento previsto.")}</div></section></div>
        <div class="col"><section><div class="cab"><h2>Últimos recebidos</h2></div><div class="linhas">${f.pagos.length ? f.pagos.map(lin).join("") : vazio("Nenhum pagamento recebido ainda.")}</div></section></div></div>`;
  }

  async function tAgenda(fresco) {
    const d = await api("agenda", fresco ? { fresco: 1 } : {});
    const dias = {};
    d.consultas.forEach((c) => (dias[c.data || "sem data"] = dias[c.data || "sem data"] || []).push(c));
    $("#tela").innerHTML = `<h1>Agenda</h1>${Object.keys(dias).length ? Object.entries(dias).map(([dia, cs]) => `<section><div class="cab"><h2>${h(cs[0].dia === "hoje" || cs[0].dia === "amanhã" ? cs[0].dia : dm(dia))}</h2><span class="link">${cs.length}</span></div><div class="linhas">${cs.map((e) => `<div class="evento vidro erguer"><div class="hora">${h(e.hora)}</div><div style="min-width:0"><div class="tit">${h(e.tipo_txt)} · ${h(e.aluno ? e.aluno.nome : "")}</div><div class="sub">${h(e.status || "")} ${e.alerta ? "· " + h(e.alerta) : ""}</div></div>${e.link ? `<a class="circ" href="${h(e.link)}" target="_blank" rel="noopener" aria-label="Abrir a reunião">${ic("seta", 2.4)}</a>` : ""}</div>`).join("")}</div></section>`).join("") : vazio("Nenhum horário marcado. Cadastre na tabela consultas do Supabase e ele aparece aqui.")}`;
  }

  async function tSistema() {
    const s = await api("sistema", { fresco: 1 });
    const pt = (ok) => `<span class="ponto ${ok ? "" : "mal"}"></span>`;
    $("#tela").innerHTML = `<h1>Sistema</h1>
      <div class="kpis"><div class="kpi vidro"><small>${s.modo === "demo" ? "modo" : "Supabase · " + h(s.projeto)}</small><b>${pt(s.supabase_ok)}${s.modo === "demo" ? "demonstração" : s.supabase_ok ? "conectado" : "sem conexão"}</b></div>
        <div class="kpi vidro"><small>formulários do Tally · última resposta</small><b style="font-size:17px">${s.ultimo_tally ? dm(s.ultimo_tally) + " " + h(String(s.ultimo_tally).slice(11, 16)) : "nenhuma ainda"}</b></div>
        <div class="kpi vidro"><small>assinatura do RT (pasta privada)</small><b>${pt(s.assinatura_rt)}${s.assinatura_rt ? "encontrada" : "falta"}</b></div>
        <div class="kpi vidro"><small>PIN do RT</small><b>${pt(s.pin_rt)}${s.pin_rt ? "ligado" : "desligado"}</b></div></div>
      ${s.erro ? `<section class="vidro bloco"><h2>Erro de conexão</h2><div class="log">${h(s.erro)}</div><p class="sub" style="white-space:normal;margin-top:8px">Confira a internet e o arquivo supabase.env (guia 05, passo 4).</p></section>` : ""}
      <section class="vidro bloco"><h2>Como funciona</h2><p class="sub" style="white-space:normal;margin-top:8px">O painel roda só no seu PC (endereço 127.0.0.1) e lê o Supabase ao vivo; os dados ficam 1 minuto na memória e o botão de atualizar busca de novo. Nada de aluno é gravado em arquivo, fora os PDFs na pasta de cada aluno (${h(s.pasta_alunos)}). As respostas do Tally entram sozinhas pela função tally-webhook do Supabase, mesmo com o PC desligado.</p>
        <p class="sub" style="white-space:normal;margin-top:8px"><b>Dieta tem Responsável Técnico:</b> ${h(s.rt.linha_documento)}. Todo plano alimentar passa pela APROVAÇÃO DO RT antes de ir para ENVIAR; o banco trava o envio sem ela, e se o PDF mudar depois da aprovação ele volta para o RT.</p></section>`;
  }

  // ---------- navegação ----------
  function menu() {
    const rota = (location.hash.slice(1) || "inicio").split("/")[0];
    const conta = { aprovacoes: estado.contadores.aprovar, hoje: estado.contadores.urgentes };
    const ativo = (k) => rota === k || (rota === "aluno" && k === "alunos");
    $("#nav").innerHTML = MENU.map(([k, v]) => `<a href="#${k}" class="${ativo(k) ? "ativo" : ""}" aria-label="${v}">${ic(k)}${conta[k] ? `<span class="conta">${conta[k]}</span>` : ""}<span class="dica">${v}</span></a>`).join("");
    $("#doca").innerHTML = MENU.map(([k, v]) => `<a href="#${k}" class="${ativo(k) ? "ativo" : ""}">${ic(k)}${v}${conta[k] ? '<span class="conta"></span>' : ""}</a>`).join("");
  }
  const TELAS = { inicio: tInicio, hoje: tHoje, aprovacoes: tAprovacoes, alunos: tAlunos, leads: tLeads, financeiro: tFinanceiro, agenda: tAgenda, sistema: tSistema };
  async function abrir(fresco) {
    const [rota, id] = (location.hash.slice(1) || "inicio").split("/");
    menu();
    $("#app").classList.toggle("sem-gente", rota !== "inicio");
    if (rota !== "inicio") $("#gente").innerHTML = "";
    const tela = $("#tela");
    tela.classList.remove("tela"); void tela.offsetWidth; tela.classList.add("tela");
    if (!tela.innerHTML.trim() || !fresco) tela.innerHTML = '<div class="grade"><div class="col"><div class="esqueleto" style="min-height:230px"></div><div class="esqueleto"></div></div><div class="col"><div class="esqueleto"></div><div class="esqueleto" style="min-height:260px"></div></div></div>';
    try {
      if (!estado.config) {
        estado.config = await api("config");
        $("#selo-demo").hidden = estado.config.modo !== "demo";
      }
      if (rota === "aluno" && id) await tAluno(id, fresco);
      else await (TELAS[rota] || tInicio)(fresco);
    } catch (e) {
      tela.innerHTML = `<section class="vidro bloco"><h2>Não deu para carregar</h2><p class="sub" style="white-space:normal;margin-top:8px">${h(e.message)}. Confira a internet e toque em atualizar.</p></section>`;
    }
    const hr = new Date().getHours();
    $("#ola").innerHTML = `${hr < 12 ? "Bom dia" : hr < 18 ? "Boa tarde" : "Boa noite"}, <b>${h(estado.config ? estado.config.saudacao : "")}</b>`;
  }

  // ---------- eventos ----------
  window.addEventListener("hashchange", () => { window.scrollTo({ top: 0, behavior: "smooth" }); abrir(false); });
  document.addEventListener("click", async (ev) => {
    const f = ev.target.closest("[data-filtro]");
    if (f) { estado.filtro = f.dataset.filtro; return tAprovacoes(false); }
    const z = ev.target.closest("a[data-texto]");  // o WhatsApp do Windows às vezes descarta o texto do link: vai copiado junto
    if (z) {
      if (z.dataset.texto) navigator.clipboard.writeText(z.dataset.texto).then(() => aviso("Texto copiado: se não aparecer no WhatsApp, cole com Ctrl+V"), () => {});
      return;
    }
    const pdf = ev.target.closest("[data-pdf]");
    if (pdf) {
      ev.preventDefault(); pdf.disabled = true; const antes = pdf.innerHTML; pdf.textContent = "…";
      try { const r = await post(`/api/${pdf.dataset.pdf}`, { id: pdf.dataset.id }); aviso(r.mensagem); } catch (e) { aviso(e.message, true); }
      pdf.disabled = false; pdf.innerHTML = antes;
      return;
    }
    const b = ev.target.closest("[data-acao]");
    if (!b) return;
    ev.preventDefault();
    const nome = b.dataset.acao, id = b.dataset.id;
    const corpo = { acao: nome, id };
    if (DO_RT.has(nome)) {
      const pin = document.querySelector(`[data-pin="${CSS.escape(id)}"]`), nota = document.querySelector(`[data-nota="${CSS.escape(id)}"]`);
      corpo.pin = pin ? pin.value : ""; corpo.nota = nota ? nota.value.trim() : "";
      if (pin && !corpo.pin) { aviso("Digite o PIN do RT", true); pin.focus(); return; }
      if (nome === "entrega_devolver_rt" && !corpo.nota) { aviso("Escreva a nota do RT: o que precisa mudar", true); if (nota) nota.focus(); return; }
    }
    if (nome !== "lembrete_feito" && b.dataset.confirmar !== "1") {  // toda ação clínica pede um segundo toque
      b.dataset.confirmar = "1"; const antes = b.innerHTML; b.textContent = "Confirmar?";
      setTimeout(() => { if (b.isConnected && b.dataset.confirmar === "1") { b.dataset.confirmar = ""; b.innerHTML = antes; } }, 3500);
      return;
    }
    b.disabled = true; b.textContent = "…";
    try {
      const r = await post("/api/acao", corpo);
      aviso(r.mensagem || "feito");
      await abrir(true);
    } catch (e) { aviso(e.message, true); b.disabled = false; b.dataset.confirmar = ""; b.textContent = ROT_ACAO[nome] || "Ok"; }
  });
  $("#atualizar").addEventListener("click", async () => {
    const b = $("#atualizar"); b.classList.add("girando");
    try { await post("/api/atualizar"); await abrir(true); aviso("dados atualizados"); } catch (e) { aviso(e.message, true); }
    b.classList.remove("girando");
  });
  let buscaT;
  $("#busca").addEventListener("input", (e) => {
    estado.busca = e.target.value; clearTimeout(buscaT);
    buscaT = setTimeout(() => { if (!location.hash.startsWith("#alunos")) location.hash = "#alunos"; else tAlunos(false); }, 250);
  });
  // sinal de vida: aberto pelo atalho, o servidor desliga sozinho ~1,5 min depois de a última janela fechar
  setInterval(() => fetch("/api/vivo", { cache: "no-store" }).catch(() => {}), 30000);
  window.addEventListener("pagehide", () => {
    fetch("/api/fechei", { method: "POST", keepalive: true, headers: { "X-Painel": "1" } }).catch(() => {});
  });
  abrir(false);
})();
