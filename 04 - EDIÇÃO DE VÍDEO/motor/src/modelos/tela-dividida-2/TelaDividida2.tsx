// INSTAGRAM - TELA DIVIDIDA (`tela-dividida-2-instagram`, composição `TelaDividida2`; nasceu no lab em 2026-10-27,
// promovido a formato fixo no mesmo dia e SUBSTITUI o Tela Dividida clássico no /editar). Junta as peças aprovadas:
//   - layouts: split (emenda esfumaçada; B-roll simples, stop-motion ou COMPOSTO com recortes que voam e boiam),
//     fala (punch), vidro (rosto desfocado + card liquid glass com gráfico), tela (B-roll em tela cheia, a quebra de
//     padrão; `giro` vira a imagem de cabeça para baixo na fala) e texto (card escuro na fonte B);
//   - trocas dentro do split (só a metade de cima troca, o rosto segue): mascara (cortina diagonal com fio de luz),
//     zoom (a imagem velha atravessa a câmera e a nova chega de longe), chicote (pan rápido com rastro), flash, blur;
//     troca de layout: o quadro inteiro entra com o mesmo efeito;
//   - flashes P&B de ~0,15 s no começo de uma cena (montagem rápida nos respiros);
//   - legenda na fonte B aprovada, que acompanha o layout do quadro; voz, trilha e SFX nas trocas.
// Props = 03_roteiro/edicao.json (tipo EdicaoTD2 de src/tipos.ts); tempos em s do bruto, que já vem decupado (saída =
// bruto). `ini` só existe no lab (trecho). Render pelo render.mjs de sempre, SEM --gl=angle (com ele, os <Video> do
// @remotion/media dentro de Sequence estouram o tempo).
import React, {useMemo} from 'react';
import type {CalculateMetadataFunction} from 'remotion';
import {AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';
import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {CURVAS} from '../../kit/tempo';
import {CardGrafico, LegendaB, type BarraTD2} from './VidroTD2';
import {Recorte, type RecorteTD2} from './SplitCompostoTD2';
import type {Palavra} from '../../tipos';
import {MARCA} from '../../marca';

const W = 1080;
const H = 1920;
const ESFUMA = 190;
const ESFUMA_CIMA = 230;
const CREME = MARCA.creme;
const opts = {subsets: ['latin', 'latin-ext'] as ('latin' | 'latin-ext')[]};
const inter = loadInterTight('normal', {weights: ['700', '800'], ...opts}).fontFamily;
const anton = loadAnton('normal', {weights: ['400'], ...opts}).fontFamily;
const DEGRADES = [
	MARCA.degrades['nevoa-eletrico'],
	MARCA.degrades['claro-aco'],
	MARCA.degrades['eletrico-aco'],
];
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const cl = (v: number) => Math.max(0, Math.min(1, v));
const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);
const inOut = CURVAS.expo;

export type TrocaTD2 = 'corte' | 'mascara' | 'zoom' | 'chicote' | 'flash' | 'blur';
const DUR_TROCA: Record<TrocaTD2, number> = {corte: 0, mascara: 0.4, zoom: 0.36, chicote: 0.3, flash: 0.3, blur: 0.32};
// SFX automáticos: rodízio por tipo (nunca o mesmo som em seguida; o dono do canal reclamou de "efeitos repetitivos" em
// 2026-10-19), baixos sob a voz. `sfxAuto: false` desliga; a lista `sfx` do edicao.json soma sons manuais.
const W_ = 'motionix/whooshes/whooshes_';
const SONS_TROCA: Partial<Record<TrocaTD2, [string[], number]>> = {
	mascara: [[W_ + '16_smooth-and-fast-whoosh', W_ + '17_smooth-like-a-butter-whoosh', W_ + '13_simple-whoosh-2'], 0.2],
	zoom: [[W_ + '19_whoosh-deep-short', W_ + '18_whoosh-deep-light-2', W_ + '05_cinematic-low-whoosh'], 0.22],
	chicote: [[W_ + '08_fast-whoosh', W_ + '09_fast-whoosh', W_ + '10_high-and-fast-whoosh'], 0.2],
	flash: [['shimmer'], 0.2],
	blur: [[W_ + '15_slow-and-smooth-whoosh', W_ + '14_simple-whoosh', W_ + '06_cinematic-mediam-whoosh'], 0.16],
};
const SONS_POUSO: [string[], number] = [['motionix/pop/pop_05_smooth-pop', 'motionix/pop/pop_03_premium-and-smooth-pop', 'motionix/pop/pop_04_slow-and-smooth-pop', 'motionix/pop/pop_02_normal-pop'], 0.2];
const SONS_FLASH: [string[], number] = [['motionix/camera-shutters/camera-shutters_03_smooth-cammera-shutter', 'motionix/camera-shutters/camera-shutters_01_camera-shutter'], 0.15];
const DUR_FLASH = 0.15;

export type GraficoTD2 = {titulo: string; subtitulo?: string; barras: BarraTD2[]; sufixo?: string; casas?: number; destaqueEm?: number; selo?: string; fonte: string}; // destaqueEm: s desde o início da cena
export type CenaTD2 = {
	ini: number;
	fim: number;
	layout: 'split' | 'fala' | 'vidro' | 'tela' | 'texto';
	broll?: string;
	brollIni?: number;
	sequencia?: string[];
	quadroDur?: number;
	recortes?: RecorteTD2[];
	flashes?: string[];
	punch?: number;
	grafico?: GraficoTD2;
	texto?: string; // layout texto: *destaque*
	giro?: [number, number]; // layout tela: s do bruto em que a imagem gira 180°
	transicao?: TrocaTD2;
};
export type MusicaTD2 = {arquivo: string; ini?: number; vol?: number; volSemFala?: number};
export type TelaDividida2Props = {
	modelo?: string;
	bruto: string;
	voz?: string;
	ini?: number; // só no lab (trecho): s do bruto onde a composição começa
	duracao: number;
	rostoY?: number;
	aspectoBruto?: number;
	cenas: CenaTD2[];
	palavras: string | Palavra[]; // caminho do palavras.json (produção) ou a lista (lab)
	_palavras?: Palavra[];
	destaques: string[];
	musica?: MusicaTD2;
	sfx?: {t: number; som: string; vol?: number}[];
	sfxAuto?: boolean;
};

export const calcularTD2: CalculateMetadataFunction<TelaDividida2Props> = async ({props}) => {
	const _palavras: Palavra[] = Array.isArray(props.palavras) ? props.palavras : await fetch(staticFile(props.palavras)).then((r) => r.json());
	return {durationInFrames: Math.max(1, Math.ceil(props.duracao * 24 - 1e-6)), fps: 24, width: W, height: H, props: {...props, _palavras}};
};

// ---------- trocas: estilo da camada que ENTRA (p 0→1) e da que SAI (q 0→1) ----------
const entra = (tipo: TrocaTD2, p: number): React.CSSProperties => {
	const e = inOut(cl(p));
	if (p >= 1) return {};
	if (tipo === 'zoom') return {transform: `scale(${1.35 - 0.35 * e})`, filter: `blur(${14 * (1 - e)}px)`, opacity: cl(p * 2.2)};
	if (tipo === 'chicote') return {transform: `translateX(${W * (1 - e)}px) scaleX(${1 + 0.18 * Math.sin(Math.PI * e)})`, filter: `blur(${16 * Math.sin(Math.PI * Math.min(1, e + 0.15))}px)`};
	if (tipo === 'mascara') {
		// cortina diagonal: a borda corre da esquerda para a direita, inclinada
		const x = -0.45 * W + e * 1.9 * W;
		return {clipPath: `polygon(0 0, ${x + 0.3 * W}px 0, ${x}px 100%, 0 100%)`};
	}
	if (tipo === 'blur') return {filter: `blur(${16 * (1 - e)}px)`, opacity: e};
	if (tipo === 'flash') return {};
	return {};
};
// troca de LAYOUT (o quadro inteiro): sem opacidade, senão o quadro nasce do preto (calibração original, 2026-10-27: "fica a tela
// preta, ou muito escura" aos 0:22, 1:03 e 1:20). O desfoque e o zoom escondem a troca de enquadramento do rosto.
const entraQuadro = (tipo: TrocaTD2, p: number): React.CSSProperties => {
	const e = inOut(cl(p));
	if (p >= 1 || tipo === 'corte' || tipo === 'flash') return {};
	if (tipo === 'chicote') return {transform: `translateX(${160 * (1 - e)}px)`, filter: `blur(${14 * (1 - e)}px)`};
	if (tipo === 'blur') return {filter: `blur(${16 * (1 - e)}px)`, transform: `scale(${1.04 - 0.04 * e})`};
	return {transform: `scale(${1.12 - 0.12 * e})`, filter: `blur(${12 * (1 - e)}px)`}; // zoom e mascara
};
const sai = (tipo: TrocaTD2, q: number): React.CSSProperties => {
	const e = inOut(cl(q));
	if (q <= 0) return {};
	if (tipo === 'zoom') return {transform: `scale(${1 + 0.7 * e})`, filter: `blur(${18 * e}px)`, opacity: 1 - e};
	if (tipo === 'chicote') return {transform: `translateX(${-W * e}px) scaleX(${1 + 0.18 * Math.sin(Math.PI * e)})`, filter: `blur(${16 * Math.sin(Math.PI * e)}px)`};
	if (tipo === 'mascara') return {filter: `brightness(${1 - 0.35 * e})`};
	return {};
};
// fio de luz na borda da cortina
const FioMascara: React.FC<{p: number; alto: number}> = ({p, alto}) => {
	if (p <= 0 || p >= 1) return null;
	const e = inOut(cl(p));
	const x = -0.45 * W + e * 1.9 * W;
	const ang = (Math.atan2(alto, 0.3 * W) * 180) / Math.PI;
	return (
		<div
			style={{
				position: 'absolute',
				left: x + 0.15 * W - 60,
				top: alto / 2 - alto * 0.7,
				width: 120,
				height: alto * 1.4,
				transform: `rotate(${90 - ang}deg)`,
				background: 'linear-gradient(90deg, transparent 0%, rgba(255,236,214,0.55) 45%, rgba(255,255,255,0.9) 50%, rgba(255,236,214,0.55) 55%, transparent 100%)',
				filter: 'blur(6px)',
				mixBlendMode: 'screen',
			}}
		/>
	);
};

// ---------- mídia de B-roll (Ken Burns; stop-motion; flashes P&B no começo) ----------
const Midia: React.FC<{c: CenaTD2; lt: number; fps: number; foco: number}> = ({c, lt, fps, foco}) => {
	const dur = c.fim - c.ini;
	const nFlash = c.flashes?.length ?? 0;
	if (nFlash && lt < nFlash * DUR_FLASH) {
		const img = c.flashes![Math.min(nFlash - 1, Math.floor(lt / DUR_FLASH))];
		return <Img src={staticFile(img)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(1) contrast(1.45) brightness(0.92)', transform: `scale(${1.12 - 0.06 * ((lt % DUR_FLASH) / DUR_FLASH)})`}} />;
	}
	const video = !!c.broll && isVideo(c.broll);
	const kb = video ? 1.03 + 0.04 * cl(lt / dur) : 1.06 + 0.09 * cl(lt / dur);
	const estilo: React.CSSProperties = {position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${kb})`, filter: foco > 0 ? `blur(${(foco * 11).toFixed(1)}px) brightness(${1 - foco * 0.32}) saturate(${1 - foco * 0.15})` : undefined};
	if (c.sequencia?.length) {
		const passo = c.quadroDur ?? dur / c.sequencia.length;
		return <Img src={staticFile(c.sequencia[Math.min(c.sequencia.length - 1, Math.floor(lt / passo))])} style={estilo} />;
	}
	if (!c.broll) return null;
	return video ? <Video src={staticFile(c.broll)} trimBefore={Math.round((c.brollIni ?? 0) * fps)} muted objectFit="cover" style={estilo} /> : <Img src={staticFile(c.broll)} style={estilo} />;
};

const mascaraEmenda = (() => {
	const y0 = H / 2 - ESFUMA_CIMA;
	const y1 = H / 2 + ESFUMA;
	const n = 24;
	const p = Array.from({length: n + 1}, (_, i) => {
		const x = i / n;
		const s = x * x * x * (x * (6 * x - 15) + 10);
		return `rgba(0,0,0,${(1 - s).toFixed(4)}) ${(y0 + x * (y1 - y0)).toFixed(1)}px`;
	}).join(', ');
	return `linear-gradient(to bottom, #000 0, ${p})`;
})();

const CardTexto: React.FC<{texto: string; lt: number; dur: number}> = ({texto, lt, dur}) => {
	const partes = texto.split(/(\*[^*]+\*)/).filter(Boolean);
	let k = 0;
	const saida = interpolate(lt, [dur - 0.3, dur], [1, 0], clamp);
	// Movimento contínuo e orgânico (zoom in dinâmico + leve flutuação vertical)
	const escala = interpolate(lt, [0, dur], [0.98, 1.07], clamp);
	const flutuaY = Math.sin(lt * 2.2) * 8;
	const pulsoAura = 0.85 + 0.15 * Math.sin(lt * 3.2);

	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 46%, #1e1922 0%, #0c0a0e 75%)', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 60, overflow: 'hidden'}}>
			{/* Aura de luz dinâmica e quente no fundo */}
			<div
				style={{
					position: 'absolute',
					width: 800,
					height: 800,
					borderRadius: '50%',
					background: 'radial-gradient(circle, rgba(140, 155, 228, 0.24) 0%, rgba(46, 73, 206, 0.10) 42%, transparent 70%)',
					filter: 'blur(55px)',
					transform: `scale(${pulsoAura}) translate(${Math.sin(lt * 1.6) * 30}px, ${Math.cos(lt * 1.8) * 20}px)`,
					pointerEvents: 'none',
				}}
			/>
			{/* Faixa sutil de brilho / sweep na entrada */}
			{lt > 0.1 && lt < 1.0 && (
				<div
					style={{
						position: 'absolute',
						top: -200,
						left: interpolate(lt, [0.1, 0.85], [-W * 0.3, W * 1.3], clamp),
						width: 160,
						height: H + 400,
						transform: 'rotate(24deg)',
						background: 'linear-gradient(90deg, transparent 0%, rgba(255,240,230,0.07) 50%, transparent 100%)',
						filter: 'blur(12px)',
						pointerEvents: 'none',
					}}
				/>
			)}
			<div
				style={{
					opacity: saida,
					filter: saida < 1 ? `blur(${(1 - saida) * 10}px)` : undefined,
					transform: `scale(${escala}) translateY(${flutuaY}px)`,
				}}
			>
				{partes.map((parte, i) => {
					const chave = parte.startsWith('*');
					const palavras = parte.replace(/\*/g, '').trim().split(/\s+/);
					return (
						<div key={i} style={{display: 'block'}}>
							{palavras.map((w, j) => {
								const t0 = 0.12 + k++ * 0.09;
								const e = interpolate(lt, [t0, t0 + 0.35], [0, 1], {...clamp, easing: CURVAS.entrada});
								return chave ? (
									<span
										key={j}
										style={{
											display: 'inline-block',
											opacity: e,
											transform: `scale(${0.7 + 0.3 * e}) translateY(${(1 - e) * 30}px)`,
											filter: `blur(${(1 - e) * 10}px) drop-shadow(0 0 ${16 + 8 * Math.sin(lt * 3.5)}px rgba(140, 155, 228,0.55)) drop-shadow(0 0 45px rgba(46, 73, 206,0.3))`,
										}}
									>
										<span style={{fontFamily: anton, fontSize: 200, lineHeight: 1, textTransform: 'uppercase', backgroundImage: DEGRADES[1], WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', padding: '0 0.06em'}}>{w}</span>
									</span>
								) : (
									<span
										key={j}
										style={{
											display: 'inline-block',
											marginRight: '0.3em',
											fontFamily: inter,
											fontWeight: 800,
											fontSize: 58,
											letterSpacing: '0.03em',
											textTransform: w.startsWith('@') ? 'none' : 'uppercase',
											color: CREME,
											opacity: e,
											transform: `translateY(${(1 - e) * 18}px)`,
											filter: `blur(${(1 - e) * 8}px) drop-shadow(0 2px 8px rgba(0,0,0,0.5))`,
										}}
									>
										{w}
									</span>
								);
							})}
						</div>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

// ---------- uma cena (dentro da própria Sequence: o frame é relativo ao início dela) ----------
const Cena: React.FC<{c: CenaTD2; ant?: CenaTD2; prox?: CenaTD2; p: TelaDividida2Props}> = ({c, ant, prox, p}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const lt = frame / fps;
	const t = c.ini + lt;
	const dur = c.fim - c.ini;
	const trocaIn = ant?.layout === c.layout ? c.transicao ?? 'corte' : 'corte'; // troca de layout: quem anima é o quadro inteiro
	const pIn = DUR_TROCA[trocaIn] ? lt / DUR_TROCA[trocaIn] : 1;
	const mesmoLayout = prox && prox.layout === c.layout && c.layout === 'split';
	const trocaOut = mesmoLayout ? prox!.transicao ?? 'corte' : 'corte';
	const qOut = mesmoLayout && DUR_TROCA[trocaOut] ? (t - c.fim) / DUR_TROCA[trocaOut] : 0;
	if (c.layout === 'split') {
		const primeiro = c.recortes?.length ? Math.min(...c.recortes.map((r) => r.t)) : Infinity;
		const foco = Number.isFinite(primeiro) ? interpolate(t, [primeiro - 0.1, primeiro + 0.35], [0, 1], {...clamp, easing: CURVAS.suave}) : 0;
		return (
			<>
				<div style={{position: 'absolute', top: 0, width: W, height: H / 2 + ESFUMA, overflow: 'hidden', WebkitMaskImage: mascaraEmenda, maskImage: mascaraEmenda}}>
					<div style={{position: 'absolute', inset: 0, overflow: 'hidden', ...entra(trocaIn, pIn), ...sai(trocaOut, qOut)}}>
						<Midia c={c} lt={lt} fps={fps} foco={foco} />
						{foco > 0 && <AbsoluteFill style={{background: `radial-gradient(ellipse 60% 45% at 50% 42%, rgba(255,226,190,${0.16 * foco}) 0%, transparent 70%)`}} />}
					</div>
					{trocaIn === 'mascara' && <FioMascara p={pIn} alto={H / 2 + ESFUMA} />}
				</div>
				{(c.recortes ?? []).map((r, i) => (
					<Recorte key={i} r={r} t={t} fimCena={c.fim} id={`${c.ini}-${i}`} />
				))}
			</>
		);
	}
	if (c.layout === 'tela') {
		const giro = c.giro ? interpolate(t, c.giro, [0, 180], {...clamp, easing: inOut}) : 0;
		const meio = Math.sin((giro / 180) * Math.PI);
		return (
			<AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
				<div style={{position: 'absolute', inset: 0, transform: `rotate(${giro}deg) scale(${1 + 0.55 * meio})`, filter: meio > 0.02 ? `blur(${(meio * 6).toFixed(1)}px)` : undefined}}>
					<Midia c={c} lt={lt} fps={fps} foco={0} />
				</div>
			</AbsoluteFill>
		);
	}
	if (c.layout === 'texto') return <CardTexto texto={c.texto ?? ''} lt={lt} dur={dur} />;
	if (c.layout === 'vidro' && c.grafico) {
		const g = c.grafico;
		return <CardGrafico p={{bruto: p.bruto, ini: p.ini ?? 0, duracao: p.duracao, vidroIni: c.ini, vidroFim: c.fim, palavras: [], destaques: [], ...g, destaqueEm: g.destaqueEm != null ? c.ini + g.destaqueEm : undefined}} tl={lt} durVidro={dur} />;
	}
	return null; // fala: só o rosto (camada global)
};

export const TelaDividida2: React.FC<TelaDividida2Props> = (p) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const ini = p.ini ?? 0;
	const palavras = p._palavras ?? (Array.isArray(p.palavras) ? p.palavras : []);
	const t = ini + frame / fps;
	// a cena do quadro pelo MESMO arredondamento das Sequences (por tempo, a fronteira escapava 1 quadro: rosto no
	// enquadramento do split sem o B-roll em cima = metade preta aos 22,67 s)
	const q = (s: number) => Math.round((s - ini) * fps);
	const idx = Math.max(0, p.cenas.findIndex((c) => frame >= q(c.ini) && frame < q(c.fim)));
	const c = p.cenas[idx];
	const ant = p.cenas[idx - 1];
	const lt = t - c.ini;
	const rostoY = p.rostoY ?? 0.5;

	// rosto: um <Video> só para o vídeo inteiro; o enquadramento muda com o layout do quadro
	let rosto: React.CSSProperties = {opacity: 0};
	if (c.layout === 'split') {
		const topo = H / 2 - (H / 2) * rostoY;
		rosto = {transform: `translateY(${topo}px) scale(${1 + 0.03 * cl(lt / (c.fim - c.ini))})`, clipPath: `inset(${H / 2 - ESFUMA_CIMA - topo}px 0 0 0)`};
	} else if (c.layout === 'fala' || c.layout === 'vidro') {
		const punch = c.punch ?? 1;
		const z = c.layout === 'vidro' ? Math.min(interpolate(lt, [0, 0.35], [0, 1], {...clamp, easing: CURVAS.entrada}), interpolate(lt, [c.fim - c.ini - 0.3, c.fim - c.ini], [1, 0], clamp)) : 0;
		rosto = {transform: `scale(${punch * (1 + 0.025 * cl(lt / (c.fim - c.ini))) + z * 0.06})`, transformOrigin: '50% 30%', filter: z > 0 ? `blur(${z * 30}px) brightness(${1 - z * 0.3}) saturate(${1 + z * 0.15})` : undefined};
	}

	// troca de layout: o quadro inteiro entra com o efeito da cena
	const trocaLayout = !!ant && ant.layout !== c.layout;
	const troca = c.transicao ?? 'corte';
	const pIn = trocaLayout && DUR_TROCA[troca] ? cl(lt / DUR_TROCA[troca]) : 1;
	const quadro: React.CSSProperties = pIn < 1 ? entraQuadro(troca, pIn) : {};
	const flash = troca === 'flash' ? interpolate(lt, [0, 0.06, 0.3], [0.9, 0.7, 0], clamp) : 0;

	const yLegenda = c.layout === 'split' ? H / 2 : c.layout === 'vidro' ? 1640 : 1330;
	const sons = useMemo(() => {
		const out: [number, string, number][] = (p.sfx ?? []).map((s) => [s.t, s.som, s.vol ?? 0.3]);
		if (p.sfxAuto === false) return out;
		const giro: Record<string, number> = {};
		const prox = (tipo: string, lista: string[]) => lista[(giro[tipo] = ((giro[tipo] ?? -1) + 1) % lista.length)];
		p.cenas.forEach((x, i) => {
			const s = i > 0 && x.transicao ? SONS_TROCA[x.transicao] : undefined;
			if (s) out.push([Math.max(ini, x.ini - (x.transicao === 'flash' ? 0.02 : 0.12)), prox(x.transicao!, s[0]), s[1]]);
			(x.recortes ?? []).forEach((r) => out.push([r.t - 0.12, prox('pouso', SONS_POUSO[0]), SONS_POUSO[1]]));
			(x.flashes ?? []).forEach((_, k) => out.push([x.ini + k * DUR_FLASH, prox('flash-pb', SONS_FLASH[0]), SONS_FLASH[1]]));
		});
		return out;
	}, [p.cenas, p.sfx, p.sfxAuto, ini]);
	// ducking da trilha: `vol` com fala e `volSemFala` sem fala (média móvel de ~0,37 s, como no Tela Dividida clássico)
	const falando = useMemo(() => {
		const arr = new Float32Array(Math.ceil(p.duracao * fps) + 1);
		palavras.forEach((w) => {
			for (let f = Math.floor((w.ini - 0.15 - ini) * fps); f <= Math.ceil((w.fim + 0.3 - ini) * fps); f++) if (f >= 0 && f < arr.length) arr[f] = 1;
		});
		return arr;
	}, [palavras, p.duracao, fps, ini]);

	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{overflow: 'hidden', ...quadro}}>
				<Video src={staticFile(p.bruto)} trimBefore={Math.round(ini * fps)} muted style={{position: 'absolute', top: 0, left: 0, width: W, height: H, ...rosto}} />
				{p.cenas.map((x, i) => {
					const prox = p.cenas[i + 1];
					const cauda = prox && prox.layout === 'split' && x.layout === 'split' ? DUR_TROCA[prox.transicao ?? 'corte'] : 0;
					const de = Math.round((x.ini - ini) * fps);
					const dur = Math.round((x.fim - x.ini + cauda) * fps);
					if (de + dur < 0 || de > p.duracao * fps) return null;
					return (
						<Sequence key={i} from={de} durationInFrames={Math.max(1, dur)} premountFor={fps}>
							<Cena c={x} ant={p.cenas[i - 1]} prox={prox} p={p} />
						</Sequence>
					);
				})}
				<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.42) 100%)', pointerEvents: 'none'}} />
			</AbsoluteFill>
			{flash > 0 && <AbsoluteFill style={{background: '#fff', opacity: flash}} />}
			{c.layout !== 'texto' && <LegendaB t={t} palavras={palavras} destaques={p.destaques} y={yLegenda} />}
			<Audio src={staticFile(p.voz ?? p.bruto)} trimBefore={Math.round(ini * fps)} />
			{p.musica && (
				<Audio
					src={staticFile(p.musica.arquivo)}
					trimBefore={Math.round((p.musica.ini ?? 0) * fps)}
					volume={(f) => {
						const base = p.musica!.vol ?? 0.1;
						const livre = p.musica!.volSemFala ?? base;
						const raio = Math.round(0.18 * fps);
						let s = 0;
						for (let k = -raio; k <= raio; k++) s += falando[Math.min(falando.length - 1, Math.max(0, f + k))] ?? 0;
						const fade = interpolate(f, [0, fps * 0.8, p.duracao * fps - fps * 1.2, p.duracao * fps], [0, 1, 1, 0], clamp);
						return (livre + (base - livre) * (s / (2 * raio + 1))) * fade;
					}}
				/>
			)}
			{sons.map(([ts, som, vol], i) => {
				const de = Math.round((ts - ini) * fps);
				if (de < 0 || de > p.duracao * fps) return null;
				return (
					<Sequence key={`s${i}`} from={de} durationInFrames={Math.round(2.5 * fps)}>
						<Audio src={staticFile(`05_audio/sfx/${som}.wav`)} volume={vol} />
					</Sequence>
				);
			})}
		</AbsoluteFill>
	);
};

