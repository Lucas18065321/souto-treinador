// Lógica comum dos geradores do INSTAGRAM - VOX - B-ROLLs (vox-broll-instagram; guia
// referencias/modelos/vox-broll-instagram/guia-de-estilo.md). Nasceu no lab como scripts/lab/vox-lib.mjs (fixo desde 2026-10-30).
// O gerador de cada vídeo (03_roteiro/montar_<slug>.mjs) só escreve o criativo: blocos da espinha, palcos e peças. Aqui ficam:
//   - âncoras nas palavras (T, PAL, fim) e a sincronia de 0–2 q antes da palavra;
//   - área segura do Reels (medida em 2026-10-29), largura estimada de texto por fonte e posição da legenda por layout;
//   - palco com id automático, peças de colagem (voa/monta/borda/carimbo) e traços à mão (seta, sublinhado, círculo);
//   - imagens: cópia para o projeto em P&B, borda de papel de ~7 px por fora da máscara do recorte e a cópia pré-desfocada
//     (resquício e fundo da moldura), tudo no ffmpeg, 1 vez;
//   - SFX pelo criarSfx do scripts/lib/mural.mjs (importado, só exports puros), com a escolha reaproveitada do vox.json
//     anterior (planejarSfx), e a gravação do 03_roteiro/vox.json (gravar, com --saida para conferir sem sobrescrever).
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {RAIZ, criarSfx} from './mural.mjs';
import * as CAM from './caminhos.mjs';

export {RAIZ, criarSfx};
export const ID = 'vox-broll-instagram';
export const FPS = 24;
export const Q = 1 / FPS;
export const r3 = (v) => Math.round(v * 1000) / 1000;

// ---------- câmera (as mesmas curvas do src/kit/tempo.ts e do src/modelos/vox/camera.ts), para o gerador e o validador ----------
const bez = (x1, y1, x2, y2) => {
	const bx = (u) => 3 * x1 * u * (1 - u) ** 2 + 3 * x2 * u * u * (1 - u) + u ** 3;
	const by = (u) => 3 * y1 * u * (1 - u) ** 2 + 3 * y2 * u * u * (1 - u) + u ** 3;
	return (x) => { let a = 0, b = 1; for (let i = 0; i < 40; i++) { const m = (a + b) / 2; if (bx(m) < x) a = m; else b = m; } return by((a + b) / 2); };
};
export const CURVAS_VOX = {
	suave: bez(0.65, 0, 0.35, 1), entrada: bez(0.16, 1, 0.3, 1), saida: bez(0.7, 0, 0.84, 0), linear: (t) => t, expo: bez(0.87, 0, 0.13, 1),
	assento: bez(0.22, 1, 0.36, 1), chicote: bez(0.9, 0, 0.1, 1), cubica: (t) => 1 - (1 - t) ** 3, s: bez(0.33, 0, 0.2, 1), risco: bez(0.37, 0, 0.63, 1),
};
export const cameraEm = (chaves, t) => {
	if (!chaves?.length) return {x: 540, y: 960, zoom: 1};
	if (t <= chaves[0].t) return {...chaves[0]};
	for (let i = 1; i < chaves.length; i++) {
		const a = chaves[i - 1], b = chaves[i];
		if (t <= b.t) {
			const p = (CURVAS_VOX[b.curva ?? 'suave'] ?? CURVAS_VOX.suave)(Math.min(1, Math.max(0, (t - a.t) / Math.max(1e-6, b.t - a.t))));
			const lz = Math.log(a.zoom) + (Math.log(b.zoom) - Math.log(a.zoom)) * p;
			const recuo = b.arco ? 1 - b.arco * Math.sin(Math.PI * p) : 1;
			return {x: a.x + (b.x - a.x) * p, y: a.y + (b.y - a.y) * p, zoom: Math.exp(lz) * recuo};
		}
	}
	return {...chaves.at(-1)};
};
// mundo → tela e tela → mundo (plano do meio; W×H do palco)
export const telaDe = (cam, x, y, W = 1080, H = 1920) => [W / 2 + (x - cam.x) * cam.zoom, H / 2 + (y - cam.y) * cam.zoom];
export const mundoDe = (cam, sx, sy, W = 1080, H = 1920) => [r3(cam.x + (sx - W / 2) / cam.zoom), r3(cam.y + (sy - H / 2) / cam.zoom)];

// ---------- área segura (guia, "Área morta do Reels"; medida em 2026-10-29) ----------
export const AREA = {topo: 240, base: 1500, xMin: 90, xMax: 990, xMaxBaixo: 850, linha: 1000};
// a caixa inteira dentro da faixa segura? (x 90–850 quando alguma parte fica em y ≥ 1000)
export const dentroDaArea = (c) => c.y0 >= AREA.topo && c.y1 <= AREA.base && c.x0 >= AREA.xMin && c.x1 <= (c.y1 >= AREA.linha ? AREA.xMaxBaixo : AREA.xMax);

// Largura média por letra (em fração do tamanho da fonte), caixa alta; estimativa conservadora sem métrica de fonte
// (opentype/fontkit pediriam instalação): medir 1 vez numa still e ajustar aqui.
export const POR_LETRA = {anton: 0.5, inter: 0.7, serifa: 0.56, serifaReta: 0.62, legenda: 0.64, card: 0.66};
export const larguraTexto = (txt, tamanho, fonte = 'inter') => String(txt).length * (POR_LETRA[fonte] ?? 0.66) * tamanho;
// Etiqueta de papel: o texto + folga de 1,4 × a letra (mínimo 4 letras). A folga era de 70 px de mundo: no mural, com o
// zoom de 11× da 4ª estação, virava 800 px de tela (creatina, 2026-10-30). Proporcional à letra, ela acompanha a estação.
export const larguraEtiqueta = (texto, tamanho) => r3(Math.max(4 * tamanho, String(texto).length * POR_LETRA.card * tamanho + 1.4 * tamanho));

// ---------- legenda pequena (calibração original, 2026-10-29) ----------
export const LEGENDA = {tamanho: 45, largura: 620, altura: 59};
export const legendaY = (layout, queixoTela = 1000) =>
	layout === 'split' || layout === 'moldura' ? 960 : layout === 'ele' || layout === 'fecho' ? Math.min(1460, queixoTela + 50) : layout === 'abertura' ? null : 1300;

// ---------- âncoras ----------
const norm = (s) => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%]/g, '');
export const criarAncoras = (palavras) => {
	const ws = palavras.map((p) => ({...p, n: norm(p.w)}));
	// a n-ésima ocorrência da sequência de palavras (frase com espaços) a partir de `desde` s
	const achar = (frase, n = 1, desde = 0) => {
		const alvo = String(frase).split(/\s+/).map(norm).filter(Boolean);
		let achados = 0;
		for (let i = 0; i + alvo.length <= ws.length; i++) {
			if (ws[i].ini < desde - 1e-6) continue;
			if (alvo.every((a, k) => ws[i + k].n === a) && ++achados === n) return ws.slice(i, i + alvo.length);
		}
		throw new Error(`[vox] não achei "${frase}" (ocorrência ${n}, desde ${desde} s) nas palavras`);
	};
	return {
		// início da palavra (ou da frase), em s; a peça entra 0–2 q antes: use T(...) - Q
		T: (frase, n = 1, desde = 0) => achar(frase, n, desde)[0].ini,
		fim: (frase, n = 1, desde = 0) => achar(frase, n, desde).at(-1).fim,
		// palavras da frase com o instante de cada uma, para o texto da cena (pedaço/digitação)
		PAL: (frase, n = 1, desde = 0) => achar(frase, n, desde).map((p) => ({t: r3(p.ini - Q), w: p.w.replace(/[.,;:…!?]+$/u, '')})),
	};
};

// ---------- palco ----------
export const criarPalco = (nome, base = {}) => {
	const palco = {camera: [], elementos: [], focos: [], veus: [], ...base};
	let n = 0;
	const add = (el) => {
		const e = {id: `${nome}-${String(++n).padStart(2, '0')}`, ...el};
		for (const k of ['x', 'y', 'w', 'h', 'ini', 'fim', 'rot']) if (e[k] != null) e[k] = r3(e[k]);
		palco.elementos.push(e);
		return e;
	};
	const chave = (t, x, y, zoom, curva = 'suave', extra = {}) => palco.camera.push({t: r3(t), x: r3(x), y: r3(y), zoom: r3(zoom), curva, ...extra});
	return {nome, palco, add, chave};
};

// ---------- traços à mão (seta, sublinhado, círculo): elemento `traco` centrado na caixa do desenho ----------
const tracoDe = (pts, extra) => {
	const xs = pts.flat().filter((_, i) => i % 2 === 0), ys = pts.flat().filter((_, i) => i % 2 === 1);
	const x0 = Math.min(...xs) - 20, y0 = Math.min(...ys) - 20, x1 = Math.max(...xs) + 20, y1 = Math.max(...ys) + 20;
	const loc = (x, y) => `${r3(x - x0)},${r3(y - y0)}`;
	const [a, ...resto] = pts;
	let d = `M${loc(...a)}`;
	if (resto.length === 2) d += ` Q${loc(...resto[0])} ${loc(...resto[1])}`;
	else if (resto.length === 3) d += ` C${loc(...resto[0])} ${loc(...resto[1])} ${loc(...resto[2])}`;
	else d += resto.map((p) => ` L${loc(...p)}`).join('');
	return {tipo: 'traco', x: (x0 + x1) / 2, y: (y0 + y1) / 2, w: x1 - x0, h: y1 - y0, vb: [r3(x1 - x0), r3(y1 - y0)], d, ...extra};
};
// seta curva de (x0,y0) a (x1,y1); curva = desvio lateral do meio em fração do comprimento
export const seta = (x0, y0, x1, y1, curva = 0.22, extra = {}) => {
	const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, dx = x1 - x0, dy = y1 - y0;
	return tracoDe([[x0, y0], [mx - dy * curva, my + dx * curva], [x1, y1]], {ponta: true, dur: 0.33, ...extra});
};
export const sublinhado = (x0, x1, y, extra = {}) => tracoDe([[x0, y + 6], [(x0 + x1) / 2, y - 8], [x1 + 14, y + 2]], {dur: 0.27, ...extra});
// círculo à caneta: elipse que passa um pouco do começo (como na mão)
export const circulo = (cx, cy, rx, ry, extra = {}) => {
	const pts = [];
	for (let i = 0; i <= 26; i++) {
		const a = -Math.PI * 0.6 + (i / 24) * Math.PI * 2;
		const k = 1 + 0.05 * Math.sin(i * 1.7);
		pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
	}
	return tracoDe(pts, {dur: 0.4, ...extra});
};

// ---------- imagens (ffmpeg, 1 vez por arquivo; nada se refaz se já existe) ----------
const ff = (args) => {
	const r = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], {encoding: 'utf8'});
	if (r.status !== 0) throw new Error(`[vox] ffmpeg falhou: ${r.stderr}`);
};
const tamanho = (arq) => {
	const o = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', arq], {encoding: 'utf8'}).stdout.trim();
	const [w, h] = o.split(',').map(Number);
	return {w, h};
};
// caminho de imagem: absoluto; "@biblioteca/..." (B-roll da biblioteca); relativo à pasta de projetos
// (SOUTO_VIDEO_PROJETOS, ex.: "<proj>/04_broll/ia_flow/f01.png"); ou relativo à raiz do motor de vídeo.
export const caminhoFonte = (rel) => {
	if (path.isAbsolute(rel)) return rel;
	const bib = CAM.resolverBiblioteca(rel);
	if (bib) return bib;
	const dados = path.join(CAM.DADOS, rel);
	return fs.existsSync(dados) ? dados : path.join(RAIZ, rel);
};

// Foto ou cenário: P&B (ou não), escurecida de leve, no tamanho em que aparece (largura em px), + cópia desfocada.
// recorte = PNG com alfa: P&B, borda de papel de `borda` px por fora da máscara (esconde o erro do chroma; lemo, ref-02).
export const prepararImagem = (proj, origem, nome, o = {}) => {
	const {pb = true, largura = 1080, recorte = false, borda = 7, escurece = 0, desfocada = false, contraste = 1.06, recorteQuadrado = false} = o;
	const pasta = path.join(proj, '04_broll', 'vox');
	fs.mkdirSync(pasta, {recursive: true});
	const ext = recorte ? 'png' : 'jpg';
	const rel = `04_broll/vox/${nome}.${ext}`;
	const relD = `04_broll/vox/${nome}_desf.${ext}`;
	const abs = path.join(proj, rel);
	const src = caminhoFonte(origem);
	if (!fs.existsSync(src)) throw new Error(`[vox] imagem não existe: ${origem}`);
	if (!fs.existsSync(abs)) {
		const cor = pb ? 'hue=s=0,' : '';
		const eq = `eq=contrast=${contraste}:brightness=${(-escurece).toFixed(3)},`;
		if (recorte) {
			// P&B no próprio RGBA (o alfa não passa por YUV) + borda: alfa dilatado `borda` px pintado de papel, por baixo
			const dil = Array.from({length: borda}, () => 'dilation').join(',');
			const pbRgba = pb ? 'colorchannelmixer=.3:.59:.11:0:.3:.59:.11:0:.3:.59:.11:0,' : '';
			ff(['-i', src, '-filter_complex',
				`[0]scale=${largura}:-2:flags=lanczos,format=rgba,${pbRgba}pad=iw+${borda * 2 + 8}:ih+${borda * 2 + 8}:${borda + 4}:${borda + 4}:color=0x00000000,split=3[o][m][k];` +
				`[m]alphaextract,${dil}[al];[k]drawbox=x=0:y=0:w=iw:h=ih:color=0xF2F4F8@1:t=fill[c];[c][al]alphamerge[b];[b][o]overlay=format=auto,format=rgba`,
				'-frames:v', '1', abs]);
		} else {
			const corte = recorteQuadrado ? 'crop=min(iw\\,ih):min(iw\\,ih),' : '';
			ff(['-i', src, '-vf', `${corte}scale=${largura}:-2:flags=lanczos,${cor}${eq}format=yuv420p`, '-q:v', '3', '-frames:v', '1', abs]);
		}
	}
	if (desfocada && !fs.existsSync(path.join(proj, relD))) {
		// a cópia pré-desfocada do guia: gblur sigma 5 + escurecida a 0,75 (o escurecer do foco soma no código)
		ff(['-i', abs, '-vf', recorte ? 'format=rgba,gblur=sigma=5:planes=15' : 'gblur=sigma=5,format=yuv420p', ...(recorte ? [] : ['-q:v', '4']), '-frames:v', '1', path.join(proj, relD)]);
	}
	const {w, h} = tamanho(abs);
	return {src: rel, srcDesfocado: desfocada ? relD : undefined, w, h, ar: h / w};
};

// ---------- SFX: plano curado do gerador + travas + escolha reaproveitada (2026-10-30) ----------
// plano = [[t do evento visual, categoria, alvo ('ataque' | 'pico'), nota, {ajuste: ms}?], …] em ordem. Para com erro se
// dois ficam a < 1,15 s ou se a categoria se repete em seguida. Se o vox.json anterior tem o mesmo evento (categoria, alvo
// e t a ± 0,02 s) e o arquivo existe, a escolha (arquivo, volume, ponto medido) volta de lá: o criarSfx lista e mede o
// banco inteiro a cada escolha (na creatina, com pouca RAM, a 1ª rodada passou de 1 h; reaproveitando, ~3 min).
// ajuste = o que o dono do canal pede no carretel do refinar-sfx.mjs ("o 7 entra 2 quadros antes" → {ajuste: -83}), como no
// plano do PAPER VOX: o som se desloca e o refino desconta o ajuste do desvio.
export const planejarSfx = (proj, plano, {vozI, anterior = '03_roteiro/vox.json'} = {}) => {
	plano.forEach(([t, cat], i) => {
		if (!i) return;
		const [ta, ca] = plano[i - 1];
		if (t - ta < 1.15 - 1e-6) throw new Error(`[vox] SFX a ${(t - ta).toFixed(2)} s um do outro (${ta} e ${t})`);
		if (ca === cat) throw new Error(`[vox] SFX da mesma categoria em seguida (${cat}: ${ta} e ${t})`);
	});
	const arq = path.join(proj, anterior);
	const antes = fs.existsSync(arq) ? JSON.parse(fs.readFileSync(arq, 'utf8')).sfx ?? [] : [];
	let sel = null;
	const sfx = plano.map(([ev, cat, alvo, , o = {}]) => {
		const aj = o.ajuste ?? 0;
		// ponto = onde o ataque/pico cai dentro do arquivo (s): do vox.json anterior (sem o ajuste antigo) ou medido agora
		let som, vol, ponto;
		const a = antes.find((s) => s.evento?.tipo === cat && s.alvo === alvo && Math.abs(s.evento.t - ev) < 0.02 && fs.existsSync(path.join(proj, s.som)));
		if (a) [som, vol, ponto] = [a.som, a.vol, a.evento.t - a.t + (a.ajuste ?? 0) / 1000];
		else {
			sel ??= criarSfx(proj, {vozI, pontos: true});
			const s = sel.escolher(cat);
			[som, vol, ponto] = [s.som, s.vol, s._pontos[alvo]];
		}
		return {t: r3(Math.max(0, ev - ponto + aj / 1000)), som, vol, evento: {tipo: cat, t: r3(ev)}, alvo, ...(aj ? {ajuste: aj} : {})};
	});
	sel?.salvar();
	return sfx;
};

// ---------- gravação ----------
// Grava o modelo de produção no props. Com `--saida <arquivo>` na linha de comando do gerador, grava lá e não no
// 03_roteiro/vox.json (conferir o gerador do piloto sem sobrescrever a referência, como o --saida do lib/mural.mjs).
export const gravar = (proj, props, nome = '03_roteiro/vox.json') => {
	const i = process.argv.indexOf('--saida');
	const arq = i > -1 && process.argv[i + 1] ? path.resolve(process.argv[i + 1]) : path.join(proj, nome);
	props = {...props, modelo: ID};
	fs.mkdirSync(path.dirname(arq), {recursive: true});
	fs.writeFileSync(arq, JSON.stringify(props, null, 1));
	const kb = fs.statSync(arq).size / 1024;
	const n = Object.values(props.palcos).reduce((s, p) => s + p.elementos.length, 0);
	console.log(`[vox] ${CAM.mostrar(arq)}: ${props.blocos.length} blocos, ${Object.keys(props.palcos).length} palcos, ${n} peças, ${(props.sfx ?? []).length} SFX, ${kb.toFixed(0)} KB`);
	return arq;
};
