// Trava do INSTAGRAM - VOX - B-ROLLs (vox-broll-instagram; nasceu no lab, fixo desde 2026-10-30): confere o
// 03_roteiro/vox.json contra o guia (referencias/modelos/vox-broll-instagram/guia-de-estilo.md, "Especificação de
// movimento" e "Texto cinético e legenda").
// Uso (de dentro do motor): node scripts/validar-vox.mjs <proj> [--props 03_roteiro/vox.json] [--vitrine]
//   Espinha: abertura → invasão → split → ele → mural → moldura → split → fecho; depois do 2º split, o par extra ele →
//   split acima de 60 s e o ato 2 (pares ele → split, 2ª moldura, 2º mural) acima de 75 s (creatina, 2026-10-30).
//   ERRO (código 1): mediana de entrada > 0,30 s; rajada < 7 no 1º s em tela cheia ou < 5 no painel; painel < 3
//   entradas/s; buraco > 1,0 s; curva de câmera ou entrada com overshoot; trocas < 0,54/s; plano médio > 2,8 s; texto no
//   resquício; "%" ou "vezes" sem o absoluto; card da moldura sobre o texto de outro card ou fora da faixa dele; texto ou
//   cartão da abertura sobre o rosto; texto ou legenda fora da faixa segura (com a largura estimada e o pico da entrada);
//   SFX a < 1,15 s um do outro ou da mesma categoria em seguida; arquivo que não existe.
//   AVISO: plano médio > 2,4 s; tela cheia < 2,8 peças/s; < 10 elementos no quadro de tela cheia ou < 7 no painel;
//   > 6 peças entrando juntas; duração de bloco fora da faixa do guia; troca de layout fora do fim de frase; imagem
//   repetida; tempo de leitura dos cards; moldura com mais de 0,7 s sem evento.
// --vitrine: vitrine curta (a do lab, 2026-10-29: 7 layouts em 20 s) encolhe os blocos de propósito: as durações viram nota.
// Sem métrica de fonte (opentype/fontkit pediriam instalação): largura = letras × fator da fonte (lib/vox.mjs, POR_LETRA).
import fs from 'node:fs';
import path from 'node:path';
import {AREA, CURVAS_VOX, LEGENDA, POR_LETRA, cameraEm, dentroDaArea, larguraTexto} from './lib/vox.mjs';

const args = process.argv.slice(2);
const proj = path.resolve(args[0] ?? '');
const opcao = (n, d) => (args.includes(n) ? args[args.indexOf(n) + 1] : d);
const vitrine = args.includes('--vitrine');
const arqProps = path.join(proj, opcao('--props', '03_roteiro/vox.json'));
if (!args[0] || !fs.existsSync(arqProps)) {
	console.error('Uso: node scripts/validar-vox.mjs <proj> [--props 03_roteiro/vox.json] [--vitrine]');
	process.exit(1);
}
const P = JSON.parse(fs.readFileSync(arqProps, 'utf8'));
const palavras = Array.isArray(P.palavras) ? P.palavras : JSON.parse(fs.readFileSync(path.join(proj, P.palavras), 'utf8'));
const erros = [], avisos = [], notas = [];
const ERRO = (m) => erros.push(m), AVISO = (m) => avisos.push(m);
const f2 = (v) => Number(v).toFixed(2);
const mediana = (a) => {
	const s = [...a].sort((x, y) => x - y);
	return s.length ? (s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2) : 0;
};

// ---------- estrutura e arquivos ----------
const ESPINHA = ['abertura', 'invasao', 'split', 'ele', 'mural', 'moldura', 'split', 'fecho'];
const FAIXA_DUR = {abertura: [1.5, 2.5], invasao: [6, 9], split: [7, 12], ele: [1.3, 6], mural: [9, 14], moldura: [4, 7], fecho: [1.3, 8]};
const B = P.blocos;
if (B[0]?.layout !== 'abertura') ERRO('o vídeo não começa pela abertura');
if (B.at(-1)?.layout !== 'fecho') ERRO('o vídeo não termina no fecho');
B.forEach((b, i) => {
	if (i && Math.abs(b.ini - B[i - 1].fim) > 1e-6) ERRO(`bloco ${i + 1} (${b.layout}) não começa onde o anterior termina (${f2(B[i - 1].fim)} × ${f2(b.ini)})`);
	const [a, z] = FAIXA_DUR[b.layout] ?? [0, 99];
	const d = b.fim - b.ini;
	if (d < a - 1e-6 || d > z + 1e-6) (vitrine ? notas : avisos).push(`${b.layout} ${f2(b.ini)}–${f2(b.fim)}: ${f2(d)} s (guia: ${a}–${z} s)`);
	for (const id of [b.palco, b.herda, b.moldura?.cards, ...(b.animacoes ?? []).map((x) => x.palco)].filter(Boolean)) if (!P.palcos[id]) ERRO(`bloco ${b.layout}: palco "${id}" não existe`);
	// troca de layout no fim de frase (pontuação ou pausa ≥ 0,12 s)
	if (i) {
		const w = palavras.find((p) => p.fim <= b.ini + 0.02 && p.fim > b.ini - 0.3);
		const prox = palavras.find((p) => p.ini >= b.ini - 0.02);
		const fimFrase = !w || /[.,;:!?…]$/.test(w.w) || (prox && prox.ini - w.fim >= 0.12);
		if (!fimFrase) (vitrine ? notas : avisos).push(`troca para ${b.layout} em ${f2(b.ini)} s fora do fim de frase ("${w?.w} | ${prox?.w}")`);
	}
});
// depois do 2º split: acima de 60 s, o par extra ele → split (opção do plano); acima de 75 s, o ato 2 (padrão desde a
// creatina, aprovada em 2026-10-30), que alterna ele, split, moldura e mural até o fecho
const ATO2 = P.duracao > 75 ? ['ele', 'split', 'moldura', 'mural'] : P.duracao > 60 ? ['ele', 'split'] : [];
let ordem = 0;
for (const b of B) {
	const k = ESPINHA.indexOf(b.layout, ordem);
	if (k >= 0) ordem = k;
	else if (!(ordem >= 6 && ATO2.includes(b.layout))) AVISO(`${b.layout} em ${f2(b.ini)} s fora da ordem da espinha`);
}
if (B.filter((b) => b.layout === 'moldura').length > 2) AVISO('mais de 2 molduras (guia: no máximo 2 trechos e 10 s no total)');
const existe = (rel) => fs.existsSync(path.join(proj, rel));
if (!existe(P.bruto)) ERRO(`bruto não existe: ${P.bruto}`);
const usos = {};
for (const [id, pc] of Object.entries(P.palcos))
	for (const e of pc.elementos) {
		for (const k of ['src', 'srcDesfocado']) if (e[k]) {
			if (!existe(e[k])) ERRO(`${id}/${e.id}: arquivo não existe (${e[k]})`);
			if (k === 'src') (usos[e[k]] ??= new Set()).add(`${id}/${e.id}`);
		}
	}
for (const [src, onde] of Object.entries(usos)) if (onde.size > 1) AVISO(`imagem repetida no vídeo (${src}): ${[...onde].join(', ')}`);
for (const b of B) if (b.moldura?.recorte && !existe(path.join(b.moldura.recorte.arquivo, 'q0001.webp'))) ERRO(`moldura: recorte não existe (${b.moldura.recorte.arquivo})`);

// ---------- entradas e overshoot ----------
const DUR = {voa: 0.3, monta: 0.5, borda: 0.28, pousa: 0.3, cai: 1.63};
const CURVA_OK = new Set(Object.keys(CURVAS_VOX));
for (const [id, pc] of Object.entries(P.palcos)) {
	for (const c of pc.camera) if (c.curva && !CURVA_OK.has(c.curva)) ERRO(`${id}: chave de câmera em ${f2(c.t)} s com curva "${c.curva}" (só curvas sem overshoot: ${[...CURVA_OK].join(', ')})`);
	const posicao = pc.elementos.filter((e) => ['voa', 'monta', 'borda', 'pousa'].includes(e.entra?.tipo)).map((e) => e.entra.dur ?? DUR[e.entra.tipo]);
	if (posicao.length && mediana(posicao) > 0.3 + 1e-6) ERRO(`${id}: mediana das entradas de posição ${f2(mediana(posicao))} s (máx. 0,30)`);
	for (const e of pc.elementos) if (e.entra?.tipo === 'carimbo' && (e.w ?? 0) > 420) ERRO(`${id}/${e.id}: carimbo (2,2×) em peça de ${Math.round(e.w)} px (só até ~400 px de tinta)`);
}

// ---------- animações: rajada, peças/s, buraco, densidade ----------
// peças novas de uma animação = elementos que nascem na janela (silhuetas contam cabeça por cabeça; luz não conta)
const pecas = (pc, filtro = () => true) => pc.elementos.filter((e) => e.tipo !== 'luz' && filtro(e)).flatMap((e) => (e.tipo === 'objeto' && e.nome === 'silhuetas' ? Array.from({length: e.p?.n ?? 7}, (_, i) => (e.ev?.entra ?? e.ini) + (i * 2) / 24) : [e.tipo === 'numero' ? Math.min(e.ini, e.t) : e.tipo === 'texto' ? Math.min(...e.palavras.map((w) => w.t)) : e.ini]));
const animacoes = []; // {nome, tela: 'cheia'|'painel', t0, t1, ts}
for (const b of B) {
	if (b.layout === 'invasao') animacoes.push({nome: `invasão ${f2(b.ini)}`, tela: 'cheia', t0: b.ini, t1: b.fim, pc: P.palcos[b.palco]});
	if (b.layout === 'mural') {
		const pc = P.palcos[b.palco];
		const grupos = [...new Set(pc.elementos.map((e) => e.grupo).filter(Boolean))];
		// estação = janela da 1ª peça do grupo até a 1ª do grupo seguinte; conta tudo o que nasce na janela
		const inicios = grupos.map((g) => ({g, t: Math.min(...pecas(pc, (e) => e.grupo === g).filter((t) => t >= b.ini - 0.06))})).sort((a, z) => a.t - z.t);
		inicios.forEach((x, i) => animacoes.push({nome: `mural ${x.g} ${f2(x.t)}`, tela: 'cheia', t0: Math.max(b.ini, x.t), t1: Math.min(b.fim, inicios[i + 1]?.t ?? b.fim), pc}));
		if (grupos.length < 4) (vitrine ? notas : avisos).push(`mural ${f2(b.ini)}: ${grupos.length} estações (guia: ≥ 4)`);
	}
	if (b.layout === 'split') (b.animacoes ?? []).forEach((a, i) => animacoes.push({nome: `split ${a.palco} ${f2(a.ini)}`, tela: 'painel', t0: a.ini, t1: b.animacoes[i + 1]?.ini ?? b.fim, pc: P.palcos[a.palco]}));
}
for (const a of animacoes) {
	const ts = pecas(a.pc).filter((t) => t >= a.t0 - 0.06 && t < a.t1).sort((x, y) => x - y);
	const jan = Math.min(1, a.t1 - a.t0);
	const n1 = ts.filter((t) => t < a.t0 + jan).length;
	const minimo = a.tela === 'cheia' ? 7 : 5;
	if (n1 < minimo) ERRO(`${a.nome}: rajada de ${n1} peças no 1º ${f2(jan)} s (mín. ${minimo})`);
	const taxa = ts.length / Math.max(0.1, a.t1 - a.t0);
	if (a.tela === 'painel' && taxa < 3) ERRO(`${a.nome}: ${f2(taxa)} entradas/s no painel (mín. 3)`);
	if (a.tela === 'cheia' && taxa < 2.8) AVISO(`${a.nome}: ${f2(taxa)} peças novas/s em tela cheia (guia: ≥ 2,8)`);
	// buraco: peças + chaves de câmera dentro da animação
	const ev = [...ts, ...a.pc.camera.map((c) => c.t)].filter((t) => t >= a.t0 && t <= a.t1).sort((x, y) => x - y);
	let ant = a.t0;
	for (const t of [...ev, a.t1]) {
		if (t - ant > 1.0 + 1e-6) ERRO(`${a.nome}: ${f2(t - ant)} s sem evento (${f2(ant)}–${f2(t)}; máx. 1,0)`);
		ant = Math.max(ant, t);
	}
	const vivos = a.pc.elementos.filter((e) => e.ini < a.t1 && (e.fim ?? Infinity) > a.t1 - 0.3).reduce((s, e) => s + (e.tipo === 'objeto' && e.nome === 'silhuetas' ? 1 : e.tipo === 'luz' ? 0 : 1), 0);
	if (vivos < (a.tela === 'cheia' ? 10 : 7)) AVISO(`${a.nome}: ${vivos} elementos no quadro composto (guia: ≥ ${a.tela === 'cheia' ? 10 : 7})`);
	// mais de 6 peças entrando ao mesmo tempo (poluição)
	for (const t of ts) {
		const juntas = a.pc.elementos.filter((e) => e.entra && e.ini <= t && t < e.ini + (e.entra.dur ?? DUR[e.entra.tipo] ?? 0.15)).length;
		if (juntas > 6) {
			AVISO(`${a.nome}: ${juntas} peças entrando juntas em ${f2(t)} s (guia: 3–6)`);
			break;
		}
	}
}

// ---------- trocas por segundo e plano médio ----------
const trocas = new Set();
const add = (t) => trocas.add(Math.round(t * 24));
B.slice(1).forEach((b) => add(b.ini));
for (const b of B) {
	(b.animacoes ?? []).forEach((a) => add(a.ini));
	(b.punches ?? []).forEach((p) => add(p.t));
	if (b.card) add(b.card.ini);
}
// chegada de câmera: trecho curto (≤ 0,9 s) com zoom ≥ 8% ou ≥ 80 px de tela
for (const b of B) if ((b.layout === 'invasao' || b.layout === 'mural') && b.palco) {
	const cam = P.palcos[b.palco].camera;
	cam.forEach((c, i) => {
		if (!i || c.t < b.ini || c.t > b.fim) return;
		const a = cam[i - 1];
		const dz = Math.abs(Math.log(c.zoom / a.zoom)), dd = Math.hypot(c.x - a.x, c.y - a.y) * c.zoom;
		if (c.t - a.t <= 0.9 && (dz >= Math.log(1.08) || dd >= 80)) add(a.t);
	});
}
const ts = [...trocas].sort((a, z) => a - z).map((q) => q / 24);
const porS = ts.length / P.duracao;
if (porS < 0.54) ERRO(`${ts.length} trocas em ${f2(P.duracao)} s = ${f2(porS)}/s (mín. 0,54)`);
const planos = [0, ...ts, P.duracao].map((t, i, a) => (i ? t - a[i - 1] : null)).filter((d) => d != null && d > 0);
const medio = planos.reduce((s, d) => s + d, 0) / planos.length;
if (medio > 2.8) ERRO(`plano médio ${f2(medio)} s (máx. 2,8)`);
else if (medio > 2.4) AVISO(`plano médio ${f2(medio)} s (guia: ≤ 2,4)`);
for (const b of B) if (b.layout === 'ele' || b.layout === 'fecho') {
	const marcas = [b.ini, ...(b.punches ?? []).map((p) => p.t), b.card?.ini ?? b.fim];
	marcas.forEach((t, i) => i && t - marcas[i - 1] > 2.5 + 1e-6 && AVISO(`${b.layout} ${f2(b.ini)}: ${f2(t - marcas[i - 1])} s sem punch (guia: ≤ 2,5)`));
}

// ---------- texto: resquício, "%"/"vezes", faixa segura ----------
const textoDe = (e) => (e.tipo === 'texto' ? e.palavras.map((w) => w.w).join(' ') : e.tipo === 'numero' ? `${e.prefixo ?? ''}${e.valor}${e.sufixo ?? ''}` : e.tipo === 'etiqueta' || e.tipo === 'card' ? e.texto : '');
for (const [id, pc] of Object.entries(P.palcos))
	for (const e of pc.elementos) {
		const txt = textoDe(e);
		if (!txt) continue;
		if (/%|\bvezes\b/i.test(txt) && !/\bde \d+[\d,.]* para \d|\d+ em cada \d+/i.test(txt)) ERRO(`${id}/${e.id}: "${txt}" com % ou "vezes" sem o absoluto ao lado`);
		for (const f of pc.focos ?? []) if (f.grupo === e.grupo && (e.fim == null || e.fim > f.t + 1e-6)) ERRO(`${id}/${e.id}: texto "${txt}" dentro do resquício (o grupo ${f.grupo} sai de foco em ${f2(f.t)} s)`);
	}
// caixa de texto na tela: largura por quebra de linha estimada; pico da entrada (pedaço 1,3×, carimbo 2,2×)
const linhas = (txt, tam, fonte, larg) => {
	const out = [];
	let atual = '';
	for (const w of txt.split(/\s+/)) {
		const prova = atual ? `${atual} ${w}` : w;
		if (atual && larguraTexto(prova, tam, fonte) > larg) {
			out.push(atual);
			atual = w;
		} else atual = prova;
	}
	if (atual) out.push(atual);
	return out;
};
const caixaTexto = (e) => {
	const fonte = e.tipo === 'numero' ? 'anton' : e.tipo === 'etiqueta' ? (e.fonte ?? 'inter') : e.tipo === 'card' ? 'card' : (e.fonte ?? 'inter');
	const tam = e.tamanho ?? (e.tipo === 'etiqueta' ? 48 : 50);
	const txt = textoDe(e).toUpperCase();
	if (e.tipo === 'card') {
		const ls = linhas(txt, tam, 'card', e.w * 0.86);
		const hTxt = ls.length * tam * 1.08;
		return {w: Math.max(...ls.map((l) => larguraTexto(l, tam, 'card'))), h: hTxt};
	}
	if (e.tipo === 'etiqueta') return {w: e.w, h: e.h ?? tam * 1.9};
	const ls = e.tipo === 'texto' ? linhas(txt, tam, fonte, e.w) : [txt];
	return {w: Math.max(...ls.map((l) => larguraTexto(l, tam, fonte))), h: ls.length * tam * 0.98 + tam * 0.1};
};
const pico = (e) => (e.entra?.tipo === 'carimbo' || e.modo === 'carimbo' ? 2.2 : e.tipo === 'texto' && (e.modo ?? 'pedaco') === 'pedaco' ? 1.3 : 1);
// palco → onde ele aparece na tela em cada instante (tela cheia, painel do split, fundo da moldura)
const vistas = [];
for (const b of B) {
	if ((b.layout === 'invasao' || b.layout === 'mural') && b.palco) vistas.push({id: b.palco, t0: b.ini, t1: b.fim, W: 1080, H: 1920, dy: 0});
	if (b.layout === 'split') (b.animacoes ?? []).forEach((a, i) => vistas.push({id: a.palco, t0: a.ini, t1: b.animacoes[i + 1]?.ini ?? b.fim, W: 1080, H: 960, dy: 0}));
	if (b.layout === 'moldura' && b.moldura?.cards) vistas.push({id: b.moldura.cards, t0: b.ini, t1: b.fim, W: 1080, H: 1920, dy: 0, cards: true});
}
const ruins = new Set();
for (const v of vistas) {
	const pc = P.palcos[v.id];
	for (const e of pc.elementos) {
		if (!textoDe(e)) continue;
		const nasceu = e.tipo === 'texto' ? Math.min(...e.palavras.map((w) => w.t)) : e.ini;
		const entrou = nasceu + (e.entra ? (e.entra.dur ?? DUR[e.entra.tipo] ?? 0.1) * 0.95 : 0.14);
		const ate = Math.min(v.t1, e.fim != null ? e.fim - (e.sai?.tipo === 'corte' ? 0 : 0.2) : v.t1);
		const {w, h} = caixaTexto(e);
		for (let t = Math.max(v.t0, nasceu); t <= ate; t += 1 / 12) {
			const cam = cameraEm(pc.camera, t);
			const z = cam.zoom * (t < entrou ? pico(e) : 1);
			const cx = v.W / 2 + (e.x - cam.x) * cam.zoom, cy = v.H / 2 + (e.y - cam.y) * cam.zoom + v.dy;
			const c = {x0: cx - (w * z) / 2, x1: cx + (w * z) / 2, y0: cy - (h * z) / 2, y1: cy + (h * z) / 2};
			const faixa = v.cards ? c.y0 >= AREA.topo && c.y1 <= 900 && c.x0 >= AREA.xMin && c.x1 <= 850 : dentroDaArea(c);
			if (!faixa && !ruins.has(e.id)) {
				ruins.add(e.id);
				ERRO(`${v.id}/${e.id}: "${textoDe(e)}" fora da faixa segura em ${f2(t)} s (x ${Math.round(c.x0)}–${Math.round(c.x1)}, y ${Math.round(c.y0)}–${Math.round(c.y1)}${v.cards ? '; texto de card só em y 240–900, x 90–850' : ''})`);
			}
		}
	}
}

// ---------- moldura: cards sobre o texto de outro card; eventos; leitura ----------
for (const b of B) if (b.layout === 'moldura' && b.moldura?.cards) {
	const cs = P.palcos[b.moldura.cards].elementos.filter((e) => e.tipo === 'card').sort((a, z) => a.ini - z.ini);
	cs.forEach((c, i) => {
		for (const a of cs.slice(0, i)) {
			const tA = caixaTexto(a), papel = {x0: c.x - c.w / 2, x1: c.x + c.w / 2, y0: c.y - (c.h ?? 260) / 2, y1: c.y + (c.h ?? 260) / 2};
			const txt = {x0: a.x - tA.w / 2, x1: a.x + tA.w / 2, y0: a.y - tA.h / 2, y1: a.y + tA.h / 2};
			if (papel.x0 < txt.x1 && papel.x1 > txt.x0 && papel.y0 < txt.y1 && papel.y1 > txt.y0 && (a.fim ?? Infinity) > c.ini) ERRO(`moldura: o card "${c.texto}" cobre o texto do card "${a.texto}"`);
		}
		const letras = c.texto.replace(/\s/g, '').length;
		const fica = Math.min(b.fim, c.fim ?? b.fim) - (c.ini + (c.entra?.tipo === 'cai' ? 0.9 : 0.3));
		const precisa = letras / 15 + 1.5;
		if (fica < precisa) (vitrine ? notas : avisos).push(`moldura: card "${c.texto}" fica ${f2(fica)} s inteiro (leitura pede ${f2(precisa)} s)`);
	});
	const ev = [b.ini, ...P.palcos[b.moldura.cards].elementos.map((e) => e.ini), b.fim].filter((t) => t >= b.ini && t <= b.fim).sort((a, z) => a - z);
	ev.forEach((t, i) => i && t - ev[i - 1] > 0.7 + 1e-6 && AVISO(`moldura: ${f2(t - ev[i - 1])} s sem evento (${f2(ev[i - 1])}–${f2(t)}; guia: ≤ 0,7)`));
}

// ---------- abertura: texto e cartão fora do rosto e na faixa segura ----------
for (const b of B) if (b.layout === 'abertura' && b.abertura) {
	const R = b.rosto ?? P.rosto, a = b.abertura;
	const zb = Math.max(1, 540 / R.x, 540 / (1080 - R.x)) + 0.004;
	const z = zb * (1 + (a.push ?? 0.07));
	const rosto = {x0: 540 - z * 175, x1: 540 + z * 175, y0: R.queixo - z * (R.queixo - R.topo), y1: R.queixo + 15};
	const tam = a.texto.tamanho ?? 124;
	const larg = Math.max(...a.linhas.map((l) => larguraTexto(l.map((w) => w.w).join(' '), tam, 'serifaReta'))) * 1.1;
	const txt = {x0: a.texto.x, x1: a.texto.x + larg, y0: a.texto.y, y1: a.texto.y + a.linhas.length * tam * 0.98 * 1.1};
	const c = a.cartao, giro = Math.abs(Math.sin(((c.rot ?? -3) * Math.PI) / 180));
	const cart = {x0: c.x - c.w / 2 - giro * c.h / 2, x1: c.x + c.w / 2 + giro * c.h / 2, y0: c.y - c.h / 2 - giro * c.w / 2, y1: c.y + c.h / 2 + giro * c.w / 2};
	const toca = (p, q) => p.x0 < q.x1 && p.x1 > q.x0 && p.y0 < q.y1 && p.y1 > q.y0;
	if (toca(txt, rosto)) ERRO(`abertura: texto digitado sobre o rosto (texto y ${Math.round(txt.y0)}–${Math.round(txt.y1)}, rosto y ${Math.round(rosto.y0)}–${Math.round(rosto.y1)})`);
	if (toca(cart, rosto)) ERRO(`abertura: cartão sobre o rosto (cartão y ${Math.round(cart.y0)}–${Math.round(cart.y1)}, topo da cabeça ${Math.round(rosto.y0)})`);
	if (!dentroDaArea(txt)) ERRO(`abertura: texto fora da faixa segura (x ${Math.round(txt.x0)}–${Math.round(txt.x1)}, y ${Math.round(txt.y0)}–${Math.round(txt.y1)})`);
	if (!dentroDaArea(cart)) ERRO(`abertura: cartão fora da faixa segura (x ${Math.round(cart.x0)}–${Math.round(cart.x1)}, y ${Math.round(cart.y0)}–${Math.round(cart.y1)})`);
	const no1s = a.linhas.flat().filter((w) => w.t - 1 / 24 < b.ini + 1).length + (c.t - 0.23 < b.ini + 1 ? 1 : 0) + (c.t < b.ini + 1 ? 1 : 0);
	const primeiro = Math.min(...a.linhas.flat().map((w) => w.t - 1 / 24));
	if (no1s < 3 || primeiro > b.ini + 0.15 + 1e-6) ERRO(`abertura: ${no1s} eventos no 1º segundo, o 1º em ${f2(primeiro)} s (guia: ≥ 3, o 1º até 0,15 s)`);
}

// ---------- legenda: faixa segura e nunca no rosto ----------
const blocosLeg = [];
{
	// a mesma montagem do montarBlocos (src/legendas.ts), sem destaque: ≤ 3 palavras, ≤ 18 letras, quebra na pontuação
	let atual = [];
	const fechar = () => {
		if (atual.length) blocosLeg.push({ini: atual[0].ini, fim: atual.at(-1).fim, txt: atual.map((p) => p.w.replace(/[.,;:…!?]+$/u, '')).join(' ').toUpperCase()});
		atual = [];
	};
	palavras.forEach((p, i) => {
		atual.push(p);
		const prox = palavras[i + 1];
		const chars = atual.reduce((n, x) => n + x.w.length + 1, 0);
		if (!prox || /[.!?…,;:]$/.test(p.w) || prox.ini - p.fim > 0.35 || atual.length >= 3 || chars + prox.w.length > 18) fechar();
	});
}
for (const bl of blocosLeg) {
	const b = B.find((x) => bl.ini >= x.ini - 1e-6 && bl.ini < x.fim);
	if (!b || b.layout === 'abertura' || b.legenda?.ocultar || (b.card && bl.ini >= b.card.ini)) continue;
	const R = b.rosto ?? P.rosto;
	const y = b.legenda?.y ?? (b.layout === 'split' || b.layout === 'moldura' ? 960 : b.layout === 'ele' || b.layout === 'fecho' ? Math.min(1460, R.queixo + 50) : 1300);
	const tam = Math.min(LEGENDA.tamanho, LEGENDA.largura / Math.max(1, bl.txt.length * POR_LETRA.legenda));
	const w = bl.txt.length * POR_LETRA.legenda * tam;
	const c = {x0: 540 - w / 2, x1: 540 + w / 2, y0: y - LEGENDA.altura / 2, y1: y + LEGENDA.altura / 2};
	if (!dentroDaArea(c)) ERRO(`legenda "${bl.txt}" (${f2(bl.ini)} s) fora da faixa segura (y ${Math.round(c.y0)}–${Math.round(c.y1)})`);
	if ((b.layout === 'ele' || b.layout === 'fecho') && c.y0 < R.queixo + 15) ERRO(`legenda "${bl.txt}" (${f2(bl.ini)} s) no rosto: começa em y ${Math.round(c.y0)}, queixo em ${R.queixo}`);
}

// ---------- SFX: ≥ 1,15 s entre dois, nunca a mesma categoria em seguida ----------
const sfx = [...(P.sfx ?? [])].sort((a, z) => (a.evento?.t ?? a.t) - (z.evento?.t ?? z.t));
sfx.forEach((s, i) => {
	if (!existe(s.som)) ERRO(`SFX não existe: ${s.som}`);
	if (!i) return;
	const a = sfx[i - 1], ta = a.evento?.t ?? a.t, tb = s.evento?.t ?? s.t;
	if (tb - ta < 1.15 - 1e-6) ERRO(`SFX a ${f2(tb - ta)} s um do outro (${f2(ta)} e ${f2(tb)}; mín. 1,15)`);
	const cat = (x) => x.som.split('/').at(-2);
	if (cat(a) === cat(s)) ERRO(`SFX da mesma categoria em seguida (${cat(s)}: ${f2(ta)} e ${f2(tb)})`);
});

// ---------- relatório ----------
const total = Object.values(P.palcos).reduce((s, p) => s + p.elementos.length, 0);
console.log(`[validar-vox] ${path.relative(process.cwd(), arqProps)}: ${f2(P.duracao)} s, ${B.length} blocos, ${total} peças, ${ts.length} trocas (${f2(porS)}/s), plano médio ${f2(medio)} s`);
for (const a of animacoes) {
	const n = pecas(a.pc).filter((t) => t >= a.t0 - 0.06 && t < a.t1).length;
	console.log(`  · ${a.nome}: ${n} peças em ${f2(a.t1 - a.t0)} s (${f2(n / Math.max(0.1, a.t1 - a.t0))}/s)`);
}
for (const n of notas) console.log(`  nota (vitrine): ${n}`);
for (const a of avisos) console.log(`  AVISO: ${a}`);
for (const e of erros) console.log(`  ERRO: ${e}`);
console.log(`[validar-vox] ${erros.length} ERRO, ${avisos.length} AVISO${vitrine ? `, ${notas.length} nota` : ''}`);
process.exit(erros.length ? 1 : 0);
