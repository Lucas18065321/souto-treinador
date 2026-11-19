// TELA DIVIDIDA (nasceu no lab, 2026-10-27): B-roll composto no split. Em vez de uma foto parada, a metade de cima vira uma
// cena em camadas: fundo (imagem ou vídeo, com Ken Burns) + objetos recortados que VOAM de fora da tela em arco (giro,
// blur de movimento, expo-out, a entrada `voa` do PAPER VOX) na palavra exata e depois ficam BOIANDO (deriva sutil).
// Quando o 1º objeto pousa, o fundo ganha profundidade de campo (desfoca e escurece de leve) para os objetos saltarem.
// Emenda esfumaçada igual à do Tela Dividida de produção e legenda na fonte B aprovada.
import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';
import {noise2D} from '@remotion/noise';
import {CURVAS} from '../../kit/tempo';
import {LegendaB} from './VidroTD2';
import type {Palavra} from '../../tipos';

const W = 1080;
const H = 1920;
const ESFUMA = 190;
const ESFUMA_CIMA = 230;
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const cl = (v: number) => Math.max(0, Math.min(1, v));
const isVideo = (s: string) => /\.(mp4|webm|mov)$/i.test(s);

export type RecorteTD2 = {
	src: string;
	t: number; // s do bruto: instante em que o objeto chega (a palavra)
	x: number; // centro, fração da largura
	y: number; // centro, fração da metade de cima (0 = topo, 1 = emenda)
	tamanho: number; // px de largura
	de: 'esq' | 'dir' | 'baixo' | 'cima';
	rot?: number; // inclinação final (graus)
};
export type CenaCompostaTD2 = {ini: number; fim: number; fundo: string; fundoIni?: number; recortes: RecorteTD2[]};
export type SplitCompostoTD2Props = {bruto: string; ini: number; duracao: number; rostoY?: number; cenas: CenaCompostaTD2[]; palavras: Palavra[]; destaques: string[]};

const VOO: Record<RecorteTD2['de'], [number, number]> = {esq: [-1, 0.25], dir: [1, 0.2], baixo: [0.2, 1], cima: [-0.15, -1]};
const DUR_VOO = 0.42;
const SAIDA = 0.22;

export const Recorte: React.FC<{r: RecorteTD2; t: number; fimCena: number; id: string}> = ({r, t, fimCena, id}) => {
	const lt = t - r.t + DUR_VOO * 0.35; // o objeto já está quase pousado quando a palavra soa
	if (lt < 0) return null;
	const [dx, dy] = VOO[r.de];
	const p = CURVAS.entrada(cl(lt / DUR_VOO));
	const d = 1400;
	const lado = dx >= 0 ? 1 : -1;
	const arco = Math.sin(Math.PI * (1 - p)) * d * 0.24 * lado;
	// boia: deriva sutil depois de pousar (±7 px, ±9 px, ±1,1°), com rampa de 0,5 s
	const A = cl((lt - DUR_VOO) / 0.5);
	const bx = noise2D(`${id}x`, t * 0.33, 0) * 7 * A;
	const by = noise2D(`${id}y`, 0, t * 0.29) * 9 * A;
	const br = noise2D(`${id}r`, t * 0.25, 1) * 1.1 * A;
	const q = cl((fimCena - t) / SAIDA); // saída: blur + fade + leve encolhida
	const tx = dx * d * (1 - p) - dy * arco + bx;
	const ty = dy * d * (1 - p) + dx * arco + by;
	const giro = lado * 24 * (1 - p) + br + (r.rot ?? 0);
	const s = (1.12 - 0.12 * p) * (0.9 + 0.1 * q);
	const blur = 18 * Math.pow(1 - p, 1.5) + 10 * (1 - q);
	return (
		<Img
			src={staticFile(r.src)}
			style={{
				position: 'absolute',
				left: r.x * W,
				top: r.y * (H / 2),
				width: r.tamanho,
				transform: `translate(-50%, -50%) translate(${tx}px, ${ty}px) rotate(${giro}deg) scale(${s})`,
				opacity: cl(lt / 0.04) * q,
				filter: `drop-shadow(0 26px 34px rgba(0,0,0,0.5)) drop-shadow(0 6px 10px rgba(0,0,0,0.35))${blur > 0.3 ? ` blur(${blur.toFixed(1)}px)` : ''}`,
			}}
		/>
	);
};

const Fundo: React.FC<{c: CenaCompostaTD2; t: number; fps: number; foco: number}> = ({c, t, fps, foco}) => {
	const lt = t - c.ini;
	const dur = c.fim - c.ini;
	const kb = 1.06 + 0.08 * cl(lt / dur); // Ken Burns
	const entra = interpolate(lt, [0, 0.28], [0, 1], {...clamp, easing: CURVAS.entrada});
	const estilo: React.CSSProperties = {
		position: 'absolute',
		inset: 0,
		width: '100%',
		height: '100%',
		objectFit: 'cover',
		transform: `scale(${kb + (1 - entra) * 0.12})`,
		filter: `blur(${(foco * 11 + (1 - entra) * 14).toFixed(1)}px) brightness(${1 - foco * 0.32}) saturate(${1 - foco * 0.15})`,
		opacity: entra,
	};
	return isVideo(c.fundo) ? (
		<Video src={staticFile(c.fundo)} trimBefore={Math.round((c.fundoIni ?? 0) * fps)} muted objectFit="cover" style={estilo} />
	) : (
		<Img src={staticFile(c.fundo)} style={estilo} />
	);
};

export const SplitCompostoTD2: React.FC<SplitCompostoTD2Props> = (p) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = p.ini + frame / fps;
	const altoBroll = H / 2 + ESFUMA;
	const topoFaixa = H / 2 - ESFUMA_CIMA;
	const rostoY = p.rostoY ?? 0.5;
	const n = 24;
	const paradas = Array.from({length: n + 1}, (_, i) => {
		const x = i / n;
		const s = x * x * x * (x * (6 * x - 15) + 10);
		return `rgba(0,0,0,${(1 - s).toFixed(4)}) ${(topoFaixa + x * (altoBroll - topoFaixa)).toFixed(1)}px`;
	}).join(', ');
	const degrade = `linear-gradient(to bottom, #000 0, ${paradas})`;
	const cena = p.cenas.find((c) => t >= c.ini && t < c.fim) ?? p.cenas[p.cenas.length - 1];
	const primeiro = Math.min(...cena.recortes.map((r) => r.t));
	const foco = interpolate(t, [primeiro - 0.1, primeiro + 0.35], [0, 1], {...clamp, easing: CURVAS.suave});
	// rosto: mesmo enquadramento do split de produção (metade de baixo = faixa central do bruto) + zoom leve contínuo
	const topoVideo = H / 2 - (H - H / 2) * rostoY - topoFaixa;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<div style={{position: 'absolute', top: topoFaixa, width: W, height: H / 2 + ESFUMA_CIMA, overflow: 'hidden'}}>
				<Video src={staticFile(p.bruto)} trimBefore={Math.round(p.ini * fps)} muted style={{position: 'absolute', top: topoVideo, width: W, height: H, transform: `scale(${1 + 0.04 * cl((t - p.ini) / p.duracao)})`, transformOrigin: '50% 50%'}} />
			</div>
			<div style={{position: 'absolute', top: 0, width: W, height: altoBroll, overflow: 'hidden', WebkitMaskImage: degrade, maskImage: degrade}}>
				<Fundo key={cena.ini} c={cena} t={t} fps={fps} foco={foco} />
				{/* luz suave atrás dos objetos */}
				<AbsoluteFill style={{background: `radial-gradient(ellipse 60% 45% at 50% 42%, rgba(255,226,190,${0.16 * foco}) 0%, transparent 70%)`}} />
			</div>
			{cena.recortes.map((r, i) => (
				<Recorte key={`${cena.ini}-${i}`} r={r} t={t} fimCena={cena.fim} id={`${cena.ini}-${i}`} />
			))}
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)', pointerEvents: 'none'}} />
			<LegendaB t={t} palavras={p.palavras} destaques={p.destaques} y={H / 2} />
			<Audio src={staticFile(p.bruto)} trimBefore={Math.round(p.ini * fps)} />
		</AbsoluteFill>
	);
};
