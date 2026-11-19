// Caça de repetição escondida (calibração original, 2026-10-28, vídeo do lipedema). O Whisper, numa janela longa, "limpa"
// a fala: quando o dono do canal começa uma frase, para numa pausa curta e recomeça igual ("Não acredite em qualquer…
// Não acredite em qualquer coisa"; "E para você? E para você não cair…"), ele escreve uma vez só e as palavras somem
// do palavras.json, então nem o decupador nem as pistas enxergam a repetição.
// Como acha: em cada silêncio medido no meio de uma frase (≥ 80 ms abaixo do limiar, palavra anterior sem ponto
// final), retranscreve só o trecho que COMEÇA no silêncio (até ~4 s). Se esse trecho começa com palavras que o
// palavras.json não tem ali, e elas repetem as palavras logo antes do silêncio, é a 1ª tentativa escondida.
// Custo: todas as janelas num Whisper só (uma janela por fila de 5 s, quadros de 0,1 s para a fila fechar exatamente
// na borda; várias janelas na mesma fila embaralhavam os tempos): ~6 s por janela + ~15 s de modelo, na placa de vídeo.
// Tempos: o fim do corte (início da tentativa boa) é o silêncio medido, exato. O início sai por fatias (passo 5): o
// tempo de palavra do Whisper erra até 0,6 s ali, e reler a emenda não serve de prova, porque ele "limpa" a sobra
// ("charlatão não. Não acredite" sai igual a "charlatão. Não acredite"). Testado em 2026-10-28 no lipedema: as 2
// repetições achadas, 0 falso alarme em 25 pausas.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const SIN = {para: 'pra', esta: 'ta', estou: 'to', estao: 'tao'};
export const chaveRep = (s) => {
	const k = String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
	return SIN[k] ?? k;
};
// "acredite"/"acredito" contam como a mesma palavra (o Whisper troca a terminação entre janelas)
const igual = (x, y) => !!x && !!y && (x === y || (Math.min(x.length, y.length) >= 5 && x.slice(0, 5) === y.slice(0, 5)));

// Retranscreve várias janelas num Whisper só. janelas: [[a, b]] ou [[[a1, b1], [a2, b2]]] (pedaços emendados, para
// conferir uma junção); cada janela ≤ slot − 0,6 s. Devolve as palavras de cada janela no tempo do áudio (pedaço único)
// ou no tempo da janela emendada (vários pedaços).
export const whisperLote = ({audio16k, tmp, modelo, janelas, slot = 5, gpu = true}) => {
	if (!janelas.length) return [];
	fs.mkdirSync(tmp, {recursive: true});
	const pecas = janelas.map((j) => (Array.isArray(j[0]) ? j : [j]));
	const fc = pecas
		.map((ps, k) => {
			const cortes = ps.map(([a, b], q) => `[0]atrim=${a.toFixed(3)}:${b.toFixed(3)},asetpts=N/SR/TB[p${k}_${q}]`).join(';');
			return `${cortes};${ps.map((_, q) => `[p${k}_${q}]`).join('')}concat=n=${ps.length}:v=0:a=1,apad=whole_dur=${slot}[p${k}]`;
		})
		.join(';');
	const ffc = path.join(tmp, 'lote_filtro.txt');
	fs.writeFileSync(ffc, `${fc};${pecas.map((_, k) => `[p${k}]`).join('')}concat=n=${pecas.length}:v=0:a=1[o]`);
	const cat = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', audio16k, '-/filter_complex', ffc, '-map', '[o]', '-ar', '16000', '-ac', '1', path.join(tmp, 'lote.wav')], {encoding: 'utf8'});
	// falha calada viraria "0 repetições" (falsa segurança): para com o erro
	if (cat.status !== 0) throw new Error(`[repetição escondida] o FFmpeg não montou o lote: ${String(cat.stderr).slice(-400)}`);
	const rel = path.relative(tmp, modelo).replace(/\\/g, '/');
	const roda = (g) => {
		fs.rmSync(path.join(tmp, 'lote.json'), {force: true});
		return spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', 'lote.wav', '-af', `asetnsamples=n=1600:p=1,whisper=model=${rel}:language=pt:use_gpu=${g}:queue=${slot}:max_len=1:destination=lote.json:format=json`, '-f', 'null', '-'], {cwd: tmp, encoding: 'utf8'});
	};
	let w = roda(gpu);
	if (w.status !== 0 && gpu) w = roda(false);
	const f = path.join(tmp, 'lote.json');
	if (w.status !== 0 || !fs.existsSync(f)) throw new Error(`[repetição escondida] o Whisper falhou (${w.status}): ${String(w.stderr).slice(-400)}`);
	const linhas = !fs.existsSync(f) ? [] : fs.readFileSync(f, 'utf8').split(/\r?\n/).filter((l) => l.trim()).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
	const out = pecas.map(() => []);
	for (const x of linhas) {
		const t = x.start / 1000;
		const k = Math.floor((t + 1e-3) / slot);
		if (k < 0 || k >= pecas.length) continue;
		const total = pecas[k].reduce((s, [a, b]) => s + b - a, 0);
		const r0 = t - k * slot, r1 = Math.min(x.end / 1000 - k * slot, total);
		const w = String(x.text || '').trim();
		if (!w || /^\[.*\]$|^\(.*\)$/.test(w) || !chaveRep(w) || r0 > total + 0.15) continue;
		const base = pecas[k].length === 1 ? pecas[k][0][0] : 0;
		out[k].push({w, ini: +(base + r0).toFixed(3), fim: +(base + Math.max(r0, r1)).toFixed(3)});
	}
	return out;
};

// Começos de sílaba: vale do nível (mínimo local) seguido de subida ≥ 8 dB em até 80 ms.
const comecos = (nivel, JAN, ini, fim) => {
	const out = [];
	for (let t = ini; t <= fim; t += JAN) {
		const v = nivel(t);
		if (v <= nivel(t - JAN) && v <= nivel(t + JAN) && Math.max(nivel(t + 0.04), nivel(t + 0.06), nivel(t + 0.08)) - v >= 8) out.push(+t.toFixed(3));
	}
	return out;
};

// niveis: dB por janela de JAN s (o mesmo cálculo do decupar-inteligente); palavras: o palavras.json (com .i)
export const cacarRepeticoes = ({palavras, niveis, JAN, limiar, audio16k, tmp, modelo, log = () => {}}) => {
	const dur = niveis.length * JAN;
	const nivel = (t) => niveis[Math.max(0, Math.min(niveis.length - 1, Math.round(t / JAN)))] ?? -120;
	// 1. silêncios medidos
	const runs = [];
	let r0 = null;
	niveis.forEach((v, k) => {
		if (v < limiar) { if (r0 == null) r0 = k; }
		else { if (r0 != null && k - r0 >= 4) runs.push([r0 * JAN, k * JAN]); r0 = null; }
	});
	// 2. candidatos: silêncio de 0,2 a 2 s no meio de uma frase, com fala logo depois (o recomeço vem depois de um
	// respiro: 0,26 e 0,32 s nos dois casos do lipedema; pausa menor que 0,2 s é consoante ou emenda de palavra)
	const cand = [];
	for (const [a, b] of runs) {
		if (b - a > 2 || b - a < 0.2) continue;
		const m = (a + b) / 2;
		let ia = -1;
		for (let i = 0; i < palavras.length && (palavras[i].ini + palavras[i].fim) / 2 < m; i++) ia = i;
		if (ia < 0 || ia + 1 >= palavras.length || /[.!?…]$/.test(palavras[ia].w) || palavras[ia + 1].ini - b > 1.5) continue;
		let fim = Math.min(dur, b + 4.2);
		const prox = runs.find(([c, d]) => c >= b + 1.2 && c <= b + 4.2 && d - c >= 0.15);
		if (prox) fim = prox[0] + 0.05;
		cand.push({a, b, ia, janela: [Math.max(0, b - 0.03), fim]});
	}
	if (!cand.length) return {candidatos: 0, achados: []};
	const t0 = Date.now();
	const depois = whisperLote({audio16k, tmp, modelo, janelas: cand.map((c) => c.janela)});
	// 3. palavras a mais no começo da janela que repetem as de logo antes do silêncio
	const achados = [];
	cand.forEach((c, x) => {
		const T = depois[x];
		const Tn = T.map((w) => chaveRep(w.w));
		const A = palavras.filter((w) => (w.ini + w.fim) / 2 >= c.janela[0] - 0.12 && (w.ini + w.fim) / 2 <= c.janela[1]);
		const An = A.map((w) => chaveRep(w.w));
		if (!An.length || Tn.length < 2) return;
		let k = -1;
		for (let q = 1; q <= 5 && q < Tn.length; q++) if (igual(Tn[q], An[0]) && (An.length < 2 || q + 1 >= Tn.length || igual(Tn[q + 1], An[1]))) { k = q; break; }
		if (k < 1) return;
		const extra = Tn.slice(0, k);
		if (k === 1 && extra[0].length < 4) return;
		const cauda = palavras.slice(Math.max(0, c.ia - 5), c.ia + 1).map((w) => chaveRep(w.w));
		const repete = cauda.some((_, j) => extra.every((e, q) => igual(cauda[j + q], e)));
		if (!repete) return;
		let casadas = 0;
		while (k + casadas < Tn.length && casadas < An.length && igual(Tn[k + casadas], An[casadas])) casadas++;
		achados.push({...c, T, k, casadas, A});
	});
	// 4. começo da 1ª tentativa: retranscreve de um silêncio de ≥ 0,2 s (até 4,2 s antes) até a pausa
	const antes = whisperLote({
		audio16k, tmp, modelo,
		janelas: achados.map((h) => {
			const s = [...runs].reverse().find(([c, d]) => d <= h.a - 0.6 && d >= h.a - 4.2 && d - c >= 0.2);
			return [s ? s[1] - 0.05 : Math.max(0, h.a - 4.2), h.a + 0.02];
		}),
	});
	// conta a sequência repetida na retranscrição curta (antes + depois) e no palavras.json no mesmo trecho: só é
	// repetição escondida se a curta ouviu MAIS vezes (no "Envia" do lipedema a palavra só estava do lado errado da pausa)
	const conta = (ws, ext) => ws.reduce((s, _, q) => s + (ext.every((e, r) => igual(chaveRep(ws[q + r]?.w ?? ''), e)) ? 1 : 0), 0);
	const res = achados.map((h, n) => ({h, Tb: antes[n]})).filter(({h, Tb}) => {
		const ext = h.T.slice(0, h.k).map((w) => chaveRep(w.w));
		const ini = Tb.length ? Tb[0].ini - 0.1 : h.a - 4.2, fim = h.T[h.T.length - 1].fim + 0.1;
		const longas = palavras.filter((w) => (w.ini + w.fim) / 2 >= ini && (w.ini + w.fim) / 2 <= fim);
		return conta([...Tb, ...h.T], ext) > conta(longas, ext);
	});
	// 5. começo da 1ª tentativa, por fatias: retranscreve de cada começo de sílaba (até 3 s antes da pausa) até a pausa;
	// o corte começa no ÚLTIMO começo cuja fatia abre com a 1ª palavra repetida ("não…", "E…") com tempo de palavra de
	// verdade: ela começa até 0,2 s depois do corte e dura pelo menos 0,03 s + 0,03 s por letra ("E": 0,07 s medido; "não":
	// 0,17 s). Quando a fatia começa
	// no meio da tentativa ("acredite em…"), o Whisper INVENTA o "Não" pelo sentido, mas espremido contra a palavra
	// seguinte (0,08 s no lipedema, contra 0,17 s do "não" de verdade); quando começa em cima da palavra, ele a ouve
	// atrasada (0,58 s). Conferido só em 2 casos: é sugestão, e o decupador confere pelas fatias.
	const fatias = res.map(({h, Tb}) => comecos(nivel, JAN, Math.max(Tb.length ? Tb[0].ini - 0.3 : 0, h.a - 3), h.a - 0.2).slice(-10));
	const ouvidas = whisperLote({audio16k, tmp, modelo, janelas: res.flatMap(({h}, n) => fatias[n].map((c) => [c, h.a + 0.02]))});
	let q0 = 0;
	const fim = res.map(({h, Tb}, n) => {
		const ext = h.T.slice(0, h.k).map((w) => chaveRep(w.w));
		const ok = fatias[n].map((c, q) => ({c, ws: ouvidas[q0 + q] ?? []})).filter(({c, ws}) =>
			ws.length && igual(chaveRep(ws[0].w), ext[0]) && ws[0].ini - c <= 0.2 &&
			(ws.length < 2 || ws[1].ini - ws[0].ini >= 0.03 + 0.03 * chaveRep(ws[0].w).length - 0.005) &&
			(ext.length < 2 || ws.slice(1, 3).some((w) => igual(chaveRep(w.w), ext[1]))));
		q0 += fatias[n].length;
		const tDe = ok.length ? ok[ok.length - 1].c : null;
		const tAte = Math.max(h.a, h.b - 0.04);
		const usadas = h.T.slice(0, h.k + h.casadas);
		return {
			n: n + 1,
			iAntes: h.ia, // última palavra do palavras.json antes do silêncio
			pausa: [+h.a.toFixed(3), +h.b.toFixed(3)],
			// sem fatia que abra com a palavra repetida: o decupador marca o corte por índice ou confere no áudio
			t_de: tDe,
			t_ate: +tAte.toFixed(3),
			fatias: fatias[n].map((c, q) => `${c}: ${(ouvidas[q0 - fatias[n].length + q] ?? []).map((w) => `${w.w}@${w.ini}`).join(' ')}`),
			repete: h.T.slice(0, h.k).map((w) => w.w).join(' '),
			ouviuAntes: Tb.map((w) => w.w).join(' '),
			antesPalavras: Tb,
			ouviuDepois: h.T.map((w) => w.w).join(' '),
			// palavras da tentativa boa, nos tempos da retranscrição curta: entram na legenda no lugar das do palavras.json
			trocar: usadas.length ? {de: +(usadas[0].ini - 0.12).toFixed(3), ate: usadas[usadas.length - 1].fim, palavras: usadas} : null,
		};
	});
	log(`${cand.length} pausas no meio de frase retranscritas, ${fim.length} repetição(ões) escondida(s), ${((Date.now() - t0) / 1000).toFixed(0)} s`);
	return {candidatos: cand.length, achados: fim};
};

// Tira intervalos de tempo da montagem (cada trecho pode virar dois).
export const subtrairTempo = (montagem, cortes) => {
	let segs = montagem.map((m) => ({...m}));
	for (const {t_de: x, t_ate: y} of cortes) {
		segs = segs.flatMap((m) => {
			if (y <= m.ini || x >= m.fim) return [m];
			const out = [];
			if (x - m.ini > 0.04) out.push({ini: m.ini, fim: +x.toFixed(3)});
			if (m.fim - y > 0.04) out.push({ini: +y.toFixed(3), fim: m.fim});
			return out;
		});
	}
	return segs;
};
