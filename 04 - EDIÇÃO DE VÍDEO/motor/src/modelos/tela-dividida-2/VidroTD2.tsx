// TELA DIVIDIDA (nasceu no lab, 2026-10-27): cena "vidro". A tela inteira desfoca e escurece com o dono do canal falando ao fundo, e um
// card de vidro (liquid glass) sobe com o gráfico: título claro, barras no degradê da marca crescendo com mola, números
// contando COM decimais (o Edicao.tsx congelado arredondava 46,5 → 47), selo "≈" no tempo da fala e rodapé de fonte.
// Legenda na fonte B aprovada (Inter Tight 700 caixa alta + Anton no degradê, chave 15% menor que o teste).
// Prévia de um trecho do piloto (vídeo de 24/10): rosto → vidro → rosto, com a voz original.
import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';
import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {montarBlocos, limparPalavra} from '../../legendas';
import type {Palavra} from '../../tipos';
import {MARCA} from '../../marca';

const W = 1080;
const H = 1920;
const opts = {subsets: ['latin', 'latin-ext'] as ('latin' | 'latin-ext')[]};
const inter = loadInterTight('normal', {weights: ['500', '600', '700', '800'], ...opts}).fontFamily;
const anton = loadAnton('normal', {weights: ['400'], ...opts}).fontFamily;
const CREME = MARCA.creme;
const DEGRADES = [
	MARCA.degrades['nevoa-eletrico'],
	MARCA.degrades['claro-aco'],
	MARCA.degrades['eletrico-aco'],
];
const DEGRADES_V = [
	MARCA.degradesVerticais[0],
	MARCA.degradesVerticais[1],
];
const expoOut = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export type BarraTD2 = {rotulo: string; valor: number};
export type VidroTD2Props = {
	bruto: string;
	ini: number; // s do bruto onde o trecho começa
	duracao: number;
	vidroIni: number; // s do bruto
	vidroFim: number;
	titulo: string;
	subtitulo?: string;
	barras: BarraTD2[];
	sufixo?: string;
	casas?: number;
	destaqueEm?: number; // s do bruto
	selo?: string;
	fonte: string;
	palavras: Palavra[];
	destaques: string[];
};

const fmt = (v: number, casas: number) => v.toLocaleString('pt-BR', {minimumFractionDigits: casas, maximumFractionDigits: casas});

// ---------- legenda fonte B ----------
export const LegendaB: React.FC<{t: number; palavras: Palavra[]; destaques: string[]; y: number}> = ({t, palavras, destaques, y}) => {
	const blocos = useMemo(() => montarBlocos(palavras, destaques), [palavras, destaques]);
	const i = blocos.findIndex((b) => t >= b.ini && t < b.fim);
	if (i === -1) return null;
	const b = blocos[i];
	const normais = b.palavras.filter((w) => !w.destaque);
	const chave = b.palavras.find((w) => w.destaque);
	const entra = (w: Palavra) => interpolate(t, [w.ini - 0.04, w.ini + 0.16], [0, 1], {...clamp, easing: expoOut});
	const saida = interpolate(t, [b.fim - 0.13, b.fim], [1, 0], clamp);
	return (
		<div style={{position: 'absolute', top: y, left: 50, right: 50, transform: 'translateY(-50%)', textAlign: 'center', opacity: saida}}>
			{normais.length > 0 && (
				<div style={{fontFamily: inter, fontWeight: 700, fontSize: 48, letterSpacing: '0.02em', textTransform: 'uppercase', color: CREME, textShadow: '0 3px 18px rgba(0,0,0,0.65), 0 1px 3px rgba(0,0,0,0.6)'}}>
					{normais.map((w, k) => {
						const e = entra(w);
						return (
							<span key={k} style={{display: 'inline-block', marginRight: '0.3em', opacity: e, filter: `blur(${(1 - e) * 8}px)`, transform: `translateY(${(1 - e) * 14}px)`}}>
								{limparPalavra(w.w)}
							</span>
						);
					})}
				</div>
			)}
			{chave && (() => {
				const e = entra(chave);
				const m = spring({frame: Math.max(0, (t - chave.ini) * 30), fps: 30, config: {damping: 11, stiffness: 170, mass: 0.9}});
				// O degradê só pinta dentro da caixa do span; com lineHeight 0,95 o acento das maiúsculas (Ã, Â, Á) ficava fora
				// e sumia ("DESNUTRIÇAO", 2026-10-27). A folga de cima estende a pintura e a margem negativa a desconta: a
				// palavra fica no mesmo lugar.
				return (
					<div style={{filter: 'drop-shadow(0 0 18px rgba(0,0,0,0.75)) drop-shadow(0 3px 6px rgba(0,0,0,0.6))', opacity: e, transform: `scale(${0.6 + 0.4 * m}) rotate(${(1 - m) * -4}deg)`}}>
						<span style={{display: 'inline-block', fontFamily: anton, fontSize: 167, lineHeight: 0.95, textTransform: 'uppercase', letterSpacing: '0.005em', backgroundImage: DEGRADES[i % 3], WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', padding: '0.25em 0.08em 0', marginTop: '-0.25em'}}>
							{limparPalavra(chave.w)}
						</span>
					</div>
				);
			})()}
		</div>
	);
};

// ---------- card de vidro com o gráfico ----------
export const CardGrafico: React.FC<{p: VidroTD2Props; tl: number; durVidro: number}> = ({p, tl, durVidro}) => {
	// tl = s desde o início do vidro
	const entrada = spring({frame: Math.max(0, (tl - 0.04) * 30), fps: 30, config: {damping: 20, stiffness: 120, mass: 1}});
	const saida = interpolate(tl, [durVidro - 0.32, durVidro], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
	const vis = entrada * (1 - saida);
	const cardW = 940;
	const cardH = 1200;
	const cardTop = 300;
	const baseY = 900; // linha de base das barras, dentro do card
	const alturaMax = 420;
	const max = Math.max(...p.barras.map((b) => b.valor)) / 0.92;
	const casas = p.casas ?? 1;
	const larguraBarra = 230;
	const passo = 360;
	const x0 = cardW / 2 - ((p.barras.length - 1) * passo) / 2;
	const reflexo = interpolate(tl, [0.55, 1.25], [-0.4, 1.4], clamp);
	const deriva = interpolate(tl, [0, durVidro], [1, 1.025], clamp);
	const filho = (t0: number) => {
		const e = interpolate(tl, [t0, t0 + 0.4], [0, 1], {...clamp, easing: expoOut});
		return {opacity: e * (1 - saida), filter: `blur(${(1 - e) * 8}px)`, transform: `translateY(${(1 - e) * 18}px)`};
	};
	const dTopo = (p.destaqueEm ?? Infinity) - p.vidroIni;
	const sel = spring({frame: Math.max(0, (tl - dTopo) * 30), fps: 30, config: {damping: 13, stiffness: 140}});
	const desenhoColchete = interpolate(tl, [dTopo, dTopo + 0.35], [0, 1], {...clamp, easing: expoOut});
	return (
		<div
			style={{
				position: 'absolute',
				left: (W - cardW) / 2,
				top: cardTop,
				width: cardW,
				height: cardH,
				borderRadius: 56,
				opacity: vis,
				transform: `translateY(${(1 - entrada) * 90 - saida * 30}px) scale(${(0.93 + 0.07 * entrada) * deriva - saida * 0.04})`,
				filter: `blur(${(1 - entrada) * 14 + saida * 12}px)`,
				background: 'linear-gradient(160deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.06) 45%, rgba(255,255,255,0.10) 100%)',
				backdropFilter: 'blur(28px) saturate(160%)',
				border: '1.5px solid rgba(255,255,255,0.26)',
				boxShadow: '0 40px 120px rgba(0,0,0,0.45), inset 0 1.5px 0 rgba(255,255,255,0.35), inset 0 -1px 0 rgba(255,255,255,0.08)',
				overflow: 'hidden',
			}}
		>
			{/* reflexo diagonal atravessa o vidro uma vez */}
			<div style={{position: 'absolute', inset: 0, background: `linear-gradient(115deg, transparent ${reflexo * 100 - 18}%, rgba(255,255,255,0.16) ${reflexo * 100}%, transparent ${reflexo * 100 + 18}%)`}} />
			<div style={{position: 'absolute', top: 70, left: 0, right: 0, textAlign: 'center', ...filho(0.35)}}>
				<div style={{fontFamily: inter, fontWeight: 800, fontSize: 50, letterSpacing: '0.03em', textTransform: 'uppercase', color: CREME}}>{p.titulo}</div>
				{p.subtitulo && <div style={{fontFamily: inter, fontWeight: 600, fontSize: 36, color: 'rgba(242,239,234,0.72)', marginTop: 12}}>{p.subtitulo}</div>}
			</div>
			{/* linha de base */}
			<div style={{position: 'absolute', top: baseY, left: 90, width: (cardW - 180) * interpolate(tl, [0.45, 0.85], [0, 1], {...clamp, easing: expoOut}), height: 3, borderRadius: 2, background: 'rgba(242,239,234,0.45)', opacity: 1 - saida}} />
			{p.barras.map((b, i) => {
				const tb = 0.7 + i * 0.33;
				const m = spring({frame: Math.max(0, (tl - tb) * 30), fps: 30, config: {damping: 26, stiffness: 158, overshootClamping: true}});
				const conta = interpolate(tl, [tb, tb + 0.9], [0, b.valor], {...clamp, easing: expoOut});
				const brilho = interpolate(tl, [tb + 0.85, tb + 1.0, tb + 1.4], [0, 1, 0], clamp);
				const h = (b.valor / max) * alturaMax * m;
				const cx = x0 + i * passo;
				return (
					<React.Fragment key={i}>
						<div
							style={{
								position: 'absolute',
								left: cx - larguraBarra / 2,
								top: baseY - h,
								width: larguraBarra,
								height: h,
								borderRadius: '30px 30px 6px 6px',
								backgroundImage: DEGRADES_V[i % 2],
								boxShadow: `inset 0 2px 0 rgba(255,255,255,0.45), 0 0 ${30 + brilho * 50}px rgba(140, 155, 228,${0.25 + brilho * 0.35})`,
								opacity: 1 - saida,
							}}
						/>
						<div style={{position: 'absolute', left: cx - 200, width: 400, top: baseY - h - 150, textAlign: 'center', opacity: m * (1 - saida)}}>
							<span style={{fontFamily: anton, fontSize: 124, color: CREME, textShadow: `0 0 ${brilho * 30}px rgba(255,255,255,0.7)`}}>
								{fmt(conta, casas)}
								<span style={{fontSize: 74, marginLeft: 4}}>{p.sufixo ?? ''}</span>
							</span>
						</div>
						<div style={{position: 'absolute', left: cx - 200, width: 400, top: baseY + 28, textAlign: 'center', whiteSpace: 'pre-line', fontFamily: inter, fontWeight: 700, fontSize: 38, lineHeight: 1.1, letterSpacing: '0.02em', textTransform: 'uppercase', color: CREME, ...filho(tb + 0.15)}}>
							{b.rotulo}
						</div>
					</React.Fragment>
				);
			})}
			{/* colchete + selo "≈" no tempo da fala */}
			{p.barras.length >= 2 && tl >= dTopo && (() => {
				const a = x0;
				const b = x0 + (p.barras.length - 1) * passo;
				const topo = baseY - alturaMax * 0.92 - 150 - 60;
				const meio = (a + b) / 2;
				const meiaLarg = ((b - a) / 2) * desenhoColchete;
				return (
					<>
						<div style={{position: 'absolute', left: meio - meiaLarg, top: topo, width: meiaLarg * 2, height: 3, background: CREME, opacity: 0.85 * (1 - saida)}} />
						<div style={{position: 'absolute', left: meio - meiaLarg, top: topo, width: 3, height: 26 * desenhoColchete, background: CREME, opacity: 0.85 * (1 - saida)}} />
						<div style={{position: 'absolute', left: meio + meiaLarg - 3, top: topo, width: 3, height: 26 * desenhoColchete, background: CREME, opacity: 0.85 * (1 - saida)}} />
						<div
							style={{
								position: 'absolute',
								left: meio - 46,
								top: topo - 46,
								width: 92,
								height: 92,
								borderRadius: 46,
								backgroundImage: DEGRADES[0],
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
								fontFamily: inter,
								fontWeight: 800,
								fontSize: 58,
								color: CREME,
								transform: `scale(${sel})`,
								opacity: 1 - saida,
								boxShadow: '0 10px 30px rgba(46, 73, 206,0.45)',
							}}
						>
							{p.selo ?? '≈'}
						</div>
					</>
				);
			})()}
			<div style={{position: 'absolute', bottom: 60, left: 0, right: 0, textAlign: 'center', fontFamily: inter, fontWeight: 500, fontSize: 26, color: 'rgba(242,239,234,0.7)', ...filho(1.6)}}>{p.fonte}</div>
		</div>
	);
};

export const VidroTD2: React.FC<VidroTD2Props> = (p) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = p.ini + frame / fps; // s do bruto
	const tl = t - p.vidroIni;
	const durVidro = p.vidroFim - p.vidroIni;
	// rampa do desfoque do fundo: entra em 0,35 s, sai em 0,3 s
	const fundo = Math.min(interpolate(tl, [0, 0.35], [0, 1], {...clamp, easing: expoOut}), interpolate(tl, [durVidro - 0.3, durVidro], [1, 0], clamp));
	const noVidro = tl >= 0 && tl < durVidro;
	return (
		<AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
			<Video
				src={staticFile(p.bruto)}
				trimBefore={Math.round(p.ini * fps)}
				muted
				style={{width: W, height: H, objectFit: 'cover', transform: `scale(${1.08 + fundo * 0.06})`, transformOrigin: '50% 30%', filter: `blur(${fundo * 30}px) brightness(${1 - fundo * 0.42}) saturate(${1 + fundo * 0.15})`}}
			/>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
			{noVidro && <CardGrafico p={p} tl={tl} durVidro={durVidro} />}
			<LegendaB t={t} palavras={p.palavras} destaques={p.destaques} y={noVidro ? 1640 : 1330} />
			<Audio src={staticFile(p.bruto)} trimBefore={Math.round(p.ini * fps)} />
		</AbsoluteFill>
	);
};
