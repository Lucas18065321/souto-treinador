// Peças dos palcos do VOX - B-ROLLs. Cópia adaptada do elementos.tsx do PAPER VOX (src/modelos/paper-vox/, que não muda):
//   - look C (foto-colagem com luz real, ref-09): cenário fotográfico, foto com borda de papel claro, recorte P&B com a
//     borda de papel já gravada no PNG (ffmpeg, 1 vez), etiqueta rasgada com texto digitado, card de contexto;
//   - entradas VOX sem overshoot: voa 0,30 s em arco, monta (S de ~0,5 s), borda (sobe da borda), carimbo (2,2× → 1×),
//     cai (cartão de 1,63 s); saídas some / desmonta (ease-in, 2× mais rápido) / corte;
//   - colagem a 12 fps (passo 2) e traço a 8 fps (passo 3) por padrão; texto, número e cenário a 24 fps;
//   - laço (pêndulo amortecido), boia e foco por grupo (resquício: escurece e troca para a cópia pré-desfocada).
// Texto sempre em HTML (nunca <text> em SVG: saiu 2,4× maior no render longo do PAPER VOX).
import React from 'react';
import {Img, staticFile} from 'remotion';
import {noise2D} from '@remotion/noise';
import {evolvePath, getLength, getPointAtLength, getTangentAtLength} from '@remotion/paths';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {CURVAS} from '../../kit/tempo';
import {FONTES} from '../../kit/fontes';
import {bordaRasgada, prng, texturaPapel} from './texturas';
import {CURVAS_VOX} from './camera';
import type {Degrade, Elemento, Lado} from './tipos';
import {MARCA} from '../../marca';

const anton = loadAnton('normal', {weights: ['400'], subsets: ['latin', 'latin-ext']}).fontFamily;

// Paleta do look C (guia, "Visual"): papel #DCE1ED–#E7E8DA, tinta #1C1A19, texto #EFECE2; acento azul da marca da marca.
export const COR = {preto: '#0E0C10', fundo: '#2B2A2C', papel: MARCA.papel, papelEscuro: MARCA.papelEscuro, tinta: MARCA.tinta, texto: MARCA.papel, acento: MARCA.acento, borda: MARCA.papelEscuro, creme: MARCA.creme};
export const DESLIGADO = new Set<string>();

const cl = (v: number) => Math.min(1, Math.max(0, v));
export const tempoPasso = (frame: number, fps: number, passo = 1) => (Math.floor(frame / passo) * passo) / fps;

// Passo padrão por tipo (guia: colagem a 12 fps, traço à mão a 8 fps; rosto, legenda e pós a 24 fps).
const PASSO: Partial<Record<Elemento['tipo'], 1 | 2 | 3>> = {recorte: 2, foto: 2, papel: 2, etiqueta: 2, fita: 2, card: 2, brilho: 2, objeto: 2, traco: 3};
export const passoDe = (e: Elemento) => e.passo ?? PASSO[e.tipo] ?? 1;

const DUR_PADRAO = {voa: 0.3, monta: 0.5, borda: 0.28, carimbo: 2 / 24, pousa: 0.3, escala: 0.15, surge: 0.12, cai: 1.63, nenhuma: 0};
const VOO: Record<Lado, [number, number]> = {esq: [-1, 0], dir: [1, 0], baixo: [0, 1], cima: [0, -1], ne: [0.8, -0.8], no: [-0.8, -0.8], se: [0.8, 0.8], so: [-0.8, 0.8]};
const BOIA_PADRAO: Partial<Record<Elemento['tipo'], number>> = {recorte: 1, foto: 0.7, objeto: 0.8, card: 0.6, etiqueta: 0.5, texto: 0.25, numero: 0.25, brilho: 0.4};

export const boiar = (e: Elemento, t: number, entrou: number) => {
	const A = (e.boia ?? BOIA_PADRAO[e.tipo] ?? 0) * cl((t - entrou) / 0.5);
	if (A <= 0) return {tx: 0, ty: 0, r: 0, s: 1};
	return {tx: noise2D(`${e.id}x`, t * 0.33, 0) * 7 * A, ty: noise2D(`${e.id}y`, 0, t * 0.29) * 9 * A, r: noise2D(`${e.id}r`, t * 0.25, 1) * 1.1 * A, s: 1 + noise2D(`${e.id}s`, t * 0.2, 2) * 0.01 * A};
};

export type Anim = {opacity: number; tx: number; ty: number; s: number; r: number; blur: number};

export const durEntrada = (e: Elemento) => e.entra?.dur ?? DUR_PADRAO[e.entra?.tipo ?? 'surge'];

// Entrada + boia + laço + saída. t já vem no passo da peça.
export const animar = (e: Elemento, t: number): Anim => {
	// texto, número, traço e brilho animam a própria entrada; o cenário entra por corte seco
	const tipo = e.entra?.tipo ?? (e.tipo === 'texto' || e.tipo === 'numero' || e.tipo === 'traco' || e.tipo === 'brilho' || e.tipo === 'cenario' ? 'nenhuma' : 'surge');
	const dur = e.entra?.dur ?? DUR_PADRAO[tipo];
	const lt = t - e.ini;
	const a: Anim = {opacity: 1, tx: 0, ty: 0, s: 1, r: 0, blur: 0};
	const [dx, dy] = VOO[e.entra?.de ?? 'baixo'];
	const d = e.entra?.dist ?? (tipo === 'borda' ? 700 : tipo === 'monta' ? 1200 : 1400);
	if (tipo === 'voa') {
		// expo-out em arco, giro 24° → 0°, blur 18 → 0 (PAPER VOX; Decisões 2026-10-20), sem passar do ponto
		const p = CURVAS.entrada(cl(lt / dur));
		const arco = Math.sin(Math.PI * (1 - p)) * d * 0.24 * (dx >= 0 ? 1 : -1);
		Object.assign(a, {opacity: cl(lt / 0.04), tx: dx * d * (1 - p) - dy * arco, ty: dy * d * (1 - p) + dx * arco, r: (dx >= 0 ? 1 : -1) * 24 * (1 - p), s: 1.1 - 0.1 * p, blur: 18 * Math.pow(1 - p, 1.5)});
	} else if (tipo === 'monta') {
		// voa das bordas e TRAVA em S (50% em ~0,2 s, 90% em ~0,4 s; Pisa, ref-08 mov §4): sem giro, sem fade
		const p = CURVAS_VOX.s(cl(lt / dur));
		Object.assign(a, {opacity: lt >= 0 ? 1 : 0, tx: dx * d * (1 - p), ty: dy * d * (1 - p), blur: 10 * (1 - p)});
	} else if (tipo === 'borda') {
		const p = CURVAS.entrada(cl(lt / dur));
		Object.assign(a, {opacity: lt >= 0 ? 1 : 0, tx: dx * d * (1 - p), ty: dy * d * (1 - p), blur: 6 * (1 - p)});
	} else if (tipo === 'carimbo') {
		// 1 passo a 2,2× e depois 1× (ref-08: "?" a 2,2× por 2 q); impacto sem overshoot de posição
		Object.assign(a, {opacity: lt >= 0 ? 1 : 0, s: lt < dur ? 2.2 : 1});
	} else if (tipo === 'pousa') {
		const p = CURVAS.entrada(cl(lt / dur));
		Object.assign(a, {opacity: cl(lt / 0.06), s: 1 + 0.16 * (1 - p), r: 6 * (1 - p), ty: -40 * (1 - p)});
	} else if (tipo === 'escala') {
		const p = CURVAS.entrada(cl(lt / dur));
		Object.assign(a, {opacity: p, s: 0.72 + 0.28 * p, blur: 6 * (1 - p)}); // "passa para menos": 72% → 100% (ref-09)
	} else if (tipo === 'cai') {
		// cartão que cai 655 px em 1,63 s, easeOutCubic, −6° → 0° (ref-08 mov §3.3)
		const p = CURVAS_VOX.cubica(cl(lt / dur));
		Object.assign(a, {opacity: cl(lt / 0.05), ty: -(e.entra?.dist ?? 655) * (1 - p), r: -6 * (1 - p)});
	} else if (tipo === 'surge') {
		a.opacity = cl(lt / Math.max(0.01, dur));
	}
	const b = boiar(e, t, e.ini + dur);
	a.tx += b.tx;
	a.ty += b.ty;
	a.r += b.r;
	a.s *= b.s;
	if (e.pendulo) {
		const {amp = 22, periodo = 2, amort = 0.25} = e.pendulo;
		const u = Math.max(0, t - e.ini - dur * 0.6);
		a.r += amp * Math.sin((2 * Math.PI * u) / periodo) * Math.exp(-amort * u) * cl(u / 0.15);
	}
	if (e.fim != null) {
		const sai = e.sai?.tipo ?? 'some';
		const ds = e.sai?.dur ?? (sai === 'desmonta' ? Math.max(0.12, dur / 2) : 0.18);
		const q = cl((e.fim - t) / ds); // 1 → 0 na saída
		if (sai === 'some') {
			a.opacity *= q;
			a.blur += 8 * (1 - q);
		} else if (sai === 'desmonta') {
			const p = CURVAS.saida(1 - q);
			a.tx += dx * d * p;
			a.ty += dy * d * p;
			a.blur += 8 * p;
		} else if (t >= e.fim) a.opacity = 0;
	}
	return a;
};

const estiloBase = (e: Elemento, a: Anim, h?: number, origem?: string): React.CSSProperties => ({
	position: 'absolute',
	left: e.x,
	top: e.y,
	width: e.w,
	height: h,
	transformOrigin: origem,
	transform: `translate(-50%, -50%) translate(${a.tx}px, ${a.ty}px) rotate(${(e.rot ?? 0) + a.r}deg) scale(${a.s})`,
	opacity: a.opacity,
	filter: a.blur > 0.3 ? `blur(${a.blur.toFixed(1)}px)` : undefined,
});

// Foto/recorte com a cópia pré-desfocada (resquício): d = 0 nítida, 1 desfocada; troca por opacidade.
const ImgFoco: React.FC<{src: string; srcD?: string; d: number; style: React.CSSProperties}> = ({src, srcD, d, style}) => {
	if (!srcD || d <= 0 || DESLIGADO.has('desfoque')) return <Img src={staticFile(src)} style={style} />;
	if (d >= 1) return <Img src={staticFile(srcD)} style={style} />;
	return (
		<>
			<Img src={staticFile(src)} style={style} />
			<Img src={staticFile(srcD)} style={{...style, position: 'absolute', left: 0, top: 0, opacity: d}} />
		</>
	);
};

const Cenario: React.FC<{e: Extract<Elemento, {tipo: 'cenario'}>; a: Anim; d: number}> = ({e, a, d}) => (
	<div style={{...estiloBase(e, a, e.h ?? e.w * (16 / 9)), overflow: 'hidden'}}>
		<ImgFoco src={e.src} srcD={e.srcDesfocado} d={d} style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}} />
	</div>
);

const Foto: React.FC<{e: Extract<Elemento, {tipo: 'foto'}>; a: Anim; t: number; d: number}> = ({e, a, t, d}) => {
	const h = e.h ?? e.w * 1.25;
	const borda = e.borda ?? 12;
	const [z0, z1] = e.zoomInterno ?? [1, 1.05];
	const vida = e.fim != null ? e.fim - e.ini : 6;
	const z = z0 + (z1 - z0) * CURVAS.suave(cl((t - e.ini) / vida));
	return (
		<div style={estiloBase(e, a, h)}>
			<div style={{position: 'absolute', inset: 0, background: COR.borda, clipPath: DESLIGADO.has('borda') ? undefined : bordaRasgada(e.semente ?? 3, 0.4, 28), padding: borda, boxSizing: 'border-box'}}>
				<div style={{position: 'relative', width: '100%', height: '100%', overflow: 'hidden', background: '#222'}}>
					<ImgFoco src={e.src} srcD={e.srcDesfocado} d={d} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`, display: 'block'}} />
				</div>
			</div>
		</div>
	);
};

const Recorte: React.FC<{e: Extract<Elemento, {tipo: 'recorte'}>; a: Anim; d: number}> = ({e, a, d}) => (
	<div style={{...estiloBase(e, a, e.h), filter: [a.blur > 0.3 ? `blur(${a.blur.toFixed(1)}px)` : '', e.sombra && !DESLIGADO.has('sombra') ? 'drop-shadow(0 18px 26px rgba(0,0,0,0.45))' : ''].join(' ').trim() || undefined}}>
		<ImgFoco src={e.src} srcD={e.srcDesfocado} d={d} style={{width: '100%', height: e.h ? '100%' : 'auto', objectFit: 'contain', display: 'block'}} />
	</div>
);

const Papel: React.FC<{e: Extract<Elemento, {tipo: 'papel'}>; a: Anim}> = ({e, a}) => {
	const h = e.h ?? e.w * 1.3;
	const cor = e.cor ?? COR.papel;
	return (
		<div style={estiloBase(e, a, h)}>
			<div style={{position: 'absolute', inset: 0, backgroundColor: cor, backgroundImage: DESLIGADO.has('textura') ? undefined : `url(${texturaPapel(e.w, h, e.semente ?? 1, cor)})`, backgroundSize: '100% 100%', clipPath: e.rasgado === false || DESLIGADO.has('borda') ? undefined : bordaRasgada(e.semente ?? 1, 0.9)}} />
		</div>
	);
};

const fonteDe = (f?: string): React.CSSProperties =>
	f === 'anton' ? {fontFamily: anton, fontWeight: 400, letterSpacing: '0.01em'} :
	f === 'serifa' ? {fontFamily: FONTES.serifa.family, fontStyle: 'italic', fontWeight: 400} :
	f === 'serifaReta' ? {fontFamily: FONTES.serifaReta.family, fontWeight: 400} :
	{fontFamily: FONTES.impacto.family, fontWeight: 900, letterSpacing: '-0.02em'};

// Digitação: 3 letras por passo de 2 quadros (36 letras/s; ref-09: 15–43 letras/s, 2–3 por passo).
export const letrasDigitadas = (t: number, t0: number, total: number, fps = 24) => {
	if (t < t0) return 0;
	const passos = Math.floor(((t - t0) * fps) / 2) + 1;
	return Math.min(total, passos * 3);
};

const Etiqueta: React.FC<{e: Extract<Elemento, {tipo: 'etiqueta'}>; a: Anim; tTexto: number}> = ({e, a, tTexto}) => {
	const tam = e.tamanho ?? 48;
	const h = e.h ?? tam * 1.9;
	const cor = e.cor ?? COR.papel;
	const n = letrasDigitadas(tTexto, e.t ?? e.ini + 0.05, e.texto.length);
	return (
		<div style={{...estiloBase(e, a, h), display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
			<div style={{position: 'absolute', inset: 0, backgroundColor: cor, backgroundImage: DESLIGADO.has('textura') ? undefined : `url(${texturaPapel(e.w, h, e.semente ?? 5, cor)})`, backgroundSize: '100% 100%', clipPath: DESLIGADO.has('borda') ? undefined : bordaRasgada(e.semente ?? 5, 2.2, 24)}} />
			<div style={{position: 'relative', ...fonteDe(e.fonte), fontSize: tam, lineHeight: 1, color: e.tinta ?? COR.tinta, textTransform: 'uppercase', whiteSpace: 'nowrap', paddingTop: tam * 0.08}}>
				{e.texto.slice(0, n)}
				<span style={{opacity: 0}}>{e.texto.slice(n)}</span>
			</div>
		</div>
	);
};

const DEGRADES: Record<Degrade, string> = {
	'nevoa-eletrico': MARCA.degrades['nevoa-eletrico'],
	'claro-aco': MARCA.degrades['claro-aco'],
	'eletrico-aco': MARCA.degrades['eletrico-aco'],
};
// degradê no PRÓPRIO nó do texto (background-clip não pega filho com transform), com folga em cima para o acento
const pintura = (cor?: string, degrade?: Degrade): React.CSSProperties =>
	cor === 'marca' ? {backgroundImage: DEGRADES[degrade ?? 'nevoa-eletrico'], WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', padding: '0.1em 0.05em 0 0.02em'} : {color: cor ?? COR.texto};

const Texto: React.FC<{e: Extract<Elemento, {tipo: 'texto'}>; frame: number; fps: number; a: Anim}> = ({e, frame, fps, a}) => {
	const t = frame / fps;
	const modo = e.modo ?? 'pedaco';
	const marca = e.cor === 'marca';
	return (
		<div
			style={{
				position: 'absolute',
				left: e.x,
				top: e.y,
				width: e.w,
				transform: `translate(-50%, -50%) translate(${a.tx}px, ${a.ty}px) rotate(${(e.rot ?? 0) + a.r}deg) scale(${a.s})`,
				...fonteDe(e.fonte),
				fontSize: e.tamanho,
				lineHeight: 0.98,
				textTransform: 'uppercase',
				textAlign: e.alinhar ?? 'center',
				opacity: a.opacity,
				filter: [a.blur > 0.3 ? `blur(${a.blur.toFixed(1)}px)` : '', 'drop-shadow(0 6px 16px rgba(0,0,0,0.6))'].join(' ').trim(),
			}}
		>
			{e.palavras.map((p, i) => {
				const lt = t - p.t;
				let estilo: React.CSSProperties = {opacity: 0};
				let txt: React.ReactNode = p.w;
				if (lt >= 0) {
					if (modo === 'digita') {
						const n = letrasDigitadas(t, p.t, p.w.length, fps);
						txt = (
							<>
								{p.w.slice(0, n)}
								<span style={{opacity: 0}}>{p.w.slice(n)}</span>
							</>
						);
						estilo = {};
					} else if (modo === 'carimbo') {
						estilo = {transform: `scale(${lt < 2 / 24 ? 2.2 : 1})`};
					} else {
						// pedaço: 1,3 → 1 em 0,13 s, sem passar de 1; opacidade cheia em 0,04 s (lemo, sem quique)
						const q = CURVAS.entrada(cl(lt / 0.13));
						estilo = {opacity: cl(lt / 0.04), transform: `scale(${1.3 - 0.3 * q})`};
					}
				}
				return (
					<span key={i} style={{display: 'inline-block', marginRight: i < e.palavras.length - 1 ? '0.22em' : 0, ...(marca ? pintura('marca', e.degrade) : pintura(e.cor)), ...estilo}}>
						{txt}
					</span>
				);
			})}
		</div>
	);
};

const Numero: React.FC<{e: Extract<Elemento, {tipo: 'numero'}>; t: number; a: Anim}> = ({e, t, a}) => {
	const p = CURVAS.entrada(cl((t - e.t) / (e.dur ?? 0.6)));
	const v = Math.round(e.valor * p);
	return (
		<div style={{position: 'absolute', left: e.x, top: e.y, width: e.w, transform: `translate(-50%, -50%) translate(${a.tx}px, ${a.ty}px) rotate(${(e.rot ?? 0) + a.r}deg) scale(${a.s})`, textAlign: 'center', fontFamily: anton, fontSize: e.tamanho, lineHeight: 1, opacity: t < e.t ? 0 : a.opacity, filter: 'drop-shadow(0 6px 16px rgba(0,0,0,0.6))', fontVariantNumeric: 'tabular-nums'}}>
			<span style={{display: 'inline-block', ...pintura(e.cor ?? 'marca', e.degrade)}}>
				{e.prefixo ?? ''}
				{v}
				{e.sufixo ?? ''}
			</span>
		</div>
	);
};

const Traco: React.FC<{e: Extract<Elemento, {tipo: 'traco'}>; frame: number; fps: number; a: Anim}> = ({e, frame, fps, a}) => {
	const passo = passoDe(e);
	const t = tempoPasso(frame, fps, passo);
	const p = CURVAS.risco(cl((t - e.ini) / (e.dur ?? 0.33)));
	if (p <= 0) return null;
	const ev = evolvePath(p, e.d);
	const r = prng(Math.floor(frame / passo) + 5);
	const h = e.h ?? (e.w * e.vb[1]) / e.vb[0];
	const esp = e.espessura ?? 7;
	let ponta: string | null = null;
	if (e.ponta && p > 0.9) {
		// ponta da seta só nos últimos 10% do traço (ref-09; lemo)
		const L = getLength(e.d);
		const fim = getPointAtLength(e.d, L * p);
		const tg = getTangentAtLength(e.d, L * p);
		if (fim && tg) {
			const ang = Math.atan2(tg.y, tg.x);
			const k = esp * 4.2 * cl((p - 0.9) / 0.1);
			const ab = (s: number) => `${fim.x - k * Math.cos(ang + s * 0.55)},${fim.y - k * Math.sin(ang + s * 0.55)}`;
			ponta = `M${ab(1)} L${fim.x},${fim.y} L${ab(-1)}`;
		}
	}
	return (
		<svg viewBox={`0 0 ${e.vb[0]} ${e.vb[1]}`} style={{position: 'absolute', left: e.x, top: e.y, width: e.w, height: h, overflow: 'visible', opacity: a.opacity, transform: `translate(-50%, -50%) translate(${(r() - 0.5) * 3 + a.tx}px, ${(r() - 0.5) * 3 + a.ty}px) rotate(${(e.rot ?? 0) + a.r}deg)`}}>
			<path d={e.d} fill="none" stroke={e.cor ?? COR.creme} strokeWidth={esp} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
			{ponta && <path d={ponta} fill="none" stroke={e.cor ?? COR.creme} strokeWidth={esp} strokeLinecap="round" strokeLinejoin="round" />}
		</svg>
	);
};

// Brilho ✦ (ref-09): estrela de 4 pontas que abre em 0,15 s e cintila.
const Brilho: React.FC<{e: Extract<Elemento, {tipo: 'brilho'}>; t: number; a: Anim}> = ({e, t, a}) => {
	const lt = t - e.ini;
	const abre = CURVAS.entrada(cl(lt / 0.15));
	const cint = 0.85 + 0.15 * Math.sin(lt * 9 + e.x);
	return (
		<div style={{...estiloBase(e, {...a, s: a.s * abre * cint, r: a.r + lt * 40}, e.w), background: e.cor ?? COR.creme, clipPath: 'polygon(50% 0, 58% 42%, 100% 50%, 58% 58%, 50% 100%, 42% 58%, 0 50%, 42% 42%)', filter: 'drop-shadow(0 0 10px rgba(255,240,220,0.9))'}} />
	);
};

const Fita: React.FC<{e: Extract<Elemento, {tipo: 'fita'}>; a: Anim}> = ({e, a}) => (
	<div style={estiloBase(e, a, e.h ?? 50)}>
		<div style={{width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(196,192,184,0.82), rgba(170,166,158,0.75))', clipPath: 'polygon(0 6%, 4% 0, 96% 3%, 100% 10%, 97% 50%, 100% 92%, 95% 100%, 3% 96%, 0 88%, 3% 50%)', boxShadow: 'inset 0 0 10px rgba(0,0,0,0.18)'}} />
	</div>
);

const Luz: React.FC<{e: Extract<Elemento, {tipo: 'luz'}>; a: Anim}> = ({e, a}) => (
	<div style={{...estiloBase(e, a, e.h ?? e.w), filter: undefined, background: `radial-gradient(closest-side, ${e.cor ?? `rgba(255,214,170,${e.forca ?? 0.22})`}, rgba(255,214,170,0))`, mixBlendMode: 'screen'}} />
);

// Card de contexto da moldura (CardsContexto) e cartão que cai (R14): papel claro, texto em tinta, 2 prendedores.
const Card: React.FC<{e: Extract<Elemento, {tipo: 'card'}>; a: Anim}> = ({e, a}) => {
	const h = e.h ?? 260;
	const cor = e.cor ?? COR.papel;
	return (
		<div style={{...estiloBase(e, a, h), filter: [a.blur > 0.3 ? `blur(${a.blur.toFixed(1)}px)` : '', DESLIGADO.has('sombra') ? '' : 'drop-shadow(0 16px 22px rgba(0,0,0,0.42))'].join(' ').trim() || undefined}}>
			<div style={{position: 'absolute', inset: 0, backgroundColor: cor, backgroundImage: DESLIGADO.has('textura') ? undefined : `url(${texturaPapel(e.w, h, e.semente ?? 9, cor)})`, backgroundSize: '100% 100%', clipPath: DESLIGADO.has('borda') ? undefined : bordaRasgada(e.semente ?? 9, 0.6, 30)}} />
			<div style={{position: 'absolute', inset: '14% 7%', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: FONTES.pesada.family, fontWeight: 800, fontSize: e.tamanho ?? 50, lineHeight: 1.08, letterSpacing: '-0.01em', color: e.tinta ?? COR.tinta, textTransform: 'uppercase', whiteSpace: 'pre-line'}}>{e.texto}</div>
			{e.prendedores !== false &&
				[0.22, 0.78].map((fx, i) => (
					<div key={i} style={{position: 'absolute', left: `${fx * 100}%`, top: -34, width: 30, height: 86, transform: `translateX(-50%) rotate(${i ? 4 : -3}deg)`, background: 'linear-gradient(90deg, #B89C6E, #D8C29A 45%, #A98D60)', borderRadius: 5, boxShadow: '0 4px 6px rgba(0,0,0,0.35)'}}>
						<div style={{position: 'absolute', left: '50%', top: 10, width: 3, height: 66, marginLeft: -1.5, background: 'rgba(60,45,25,0.55)'}} />
					</div>
				))}
		</div>
	);
};

// Silhuetas (cópia do objeto do PAPER VOX, com a tinta do look C): cabeças sem rosto em cascata de 2 q.
const CABECA = 'M50 8 C73 8 87 25 87 46 C87 57 83 63 86 70 L93 81 L86 85 C86 93 81 99 72 99 L64 99 L64 109 C85 113 99 121 100 132 L0 132 C1 121 16 113 36 109 L36 99 C21 94 13 79 13 60 C13 30 28 8 50 8 Z';
const Silhuetas: React.FC<{e: Extract<Elemento, {tipo: 'objeto'}>; t: number}> = ({e, t}) => {
	const n = (e.p?.n as number) ?? 7;
	const cor = (e.p?.cor as string) ?? COR.tinta;
	const ev = e.ev ?? {};
	const h = (e.w / n) * 1.32;
	return (
		<svg style={{position: 'absolute', left: e.x, top: e.y, width: e.w, height: h, transform: `translate(-50%, -50%) rotate(${e.rot ?? 0}deg)`}} viewBox={`0 0 ${n * 100} 132`} overflow="visible">
			{Array.from({length: n}, (_, i) => {
				const lt = t - ((ev.entra ?? e.ini) + (i * 2) / 24);
				if (lt < 0) return null;
				const s = 0.8 + 0.2 * CURVAS.entrada(cl(lt / 0.15));
				return (
					<g key={i} transform={`translate(${i * 100 + 50} 132) scale(${s}) translate(-50 -132)`} opacity={cl(lt / 0.08)}>
						<path d={CABECA} fill={cor} />
					</g>
				);
			})}
		</svg>
	);
};
const OBJETOS: Record<string, React.FC<{e: Extract<Elemento, {tipo: 'objeto'}>; t: number}>> = {silhuetas: Silhuetas};

// Peça por peça; `d` = quanto o grupo dela está fora de foco (0–1), `esc` = quanto escurece no foco perdido.
export const ElementoView: React.FC<{e: Elemento; frame: number; fps: number; d: number; esc: number}> = ({e, frame, fps, d, esc}) => {
	const t = tempoPasso(frame, fps, passoDe(e));
	const a = animar(e, t);
	if (a.opacity <= 0.002) return null;
	let corpo: React.ReactNode = null;
	if (e.tipo === 'texto') corpo = <Texto e={e} frame={frame} fps={fps} a={a} />;
	else if (e.tipo === 'numero') corpo = <Numero e={e} t={frame / fps} a={a} />;
	else if (e.tipo === 'traco') corpo = <Traco e={e} frame={frame} fps={fps} a={a} />;
	else if (e.tipo === 'brilho') corpo = <Brilho e={e} t={t} a={a} />;
	else if (e.tipo === 'cenario') corpo = <Cenario e={e} a={a} d={d} />;
	else if (e.tipo === 'foto') corpo = <Foto e={e} a={a} t={t} d={d} />;
	else if (e.tipo === 'recorte') corpo = <Recorte e={e} a={a} d={d} />;
	else if (e.tipo === 'papel') corpo = <Papel e={e} a={a} />;
	else if (e.tipo === 'etiqueta') corpo = <Etiqueta e={e} a={a} tTexto={tempoPasso(frame, fps, 1)} />;
	else if (e.tipo === 'fita') corpo = <Fita e={e} a={a} />;
	else if (e.tipo === 'luz') corpo = <Luz e={e} a={a} />;
	else if (e.tipo === 'card') corpo = <Card e={e} a={a} />;
	else if (e.tipo === 'objeto') {
		const C = OBJETOS[e.nome];
		corpo = C ? (
			<div style={{position: 'absolute', left: 0, top: 0, transformOrigin: `${e.x}px ${e.y}px`, transform: `translate(${a.tx}px, ${a.ty}px) rotate(${a.r}deg) scale(${a.s})`, opacity: a.opacity}}>
				<C e={e} t={t} />
			</div>
		) : null;
	}
	if (d <= 0) return <>{corpo}</>;
	// fora de foco: escurece (20–30%); quem não tem cópia pré-desfocada ganha um desfoque leve (peças pequenas)
	const temCopia = (e.tipo === 'foto' || e.tipo === 'recorte' || e.tipo === 'cenario') && !!e.srcDesfocado;
	const filtro = [`brightness(${(1 - esc * d).toFixed(3)})`, !temCopia ? `blur(${(6 * d).toFixed(1)}px)` : ''].join(' ').trim();
	return <div style={{position: 'absolute', left: 0, top: 0, filter: filtro}}>{corpo}</div>;
};

// 1º instante em que a peça aparece (texto: a 1ª palavra).
export const nasce = (e: Elemento) => (e.tipo === 'texto' ? Math.min(e.ini, ...e.palavras.map((p) => p.t)) : e.tipo === 'numero' ? Math.min(e.ini, e.t) : e.ini);
