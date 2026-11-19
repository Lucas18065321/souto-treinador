// Palco do VOX: o mundo da animação com câmera, 3 planos de parallax e motion blur, num retângulo (tela cheia
// 1080×1920, painel do split 1080×960, fundo da moldura). Cópia adaptada do Mundo/BlurMovimento/Acabamento do PaperVox.tsx
// (src/modelos/paper-vox/, que não muda): W e H vêm por prop (centro da câmera), o acabamento (vinheta e grão) fica só
// dentro do retângulo, e as camadas valem entre planos: TODO texto fica por cima de toda imagem, inclusive do 1º plano
// que cruza (Decisões 2026-10-20), e o traço à mão por cima do texto. Rosto e recorte da pessoa ficam fora daqui.
import React from 'react';
import {AbsoluteFill, Freeze, useCurrentFrame, useVideoConfig} from 'remotion';
import {Grao} from '../../kit/Grao';
import {PARALLAX, cameraViva, transformPlano, velocidadeTela, type EstadoCamera} from './camera';
import {COR, DESLIGADO, ElementoView, nasce} from './elementos';
import type {Elemento, PalcoVox, Plano} from './tipos';

const PLANOS: Plano[] = ['fundo', 'meio', 'frente'];
const MARGEM = 260;
const cl = (v: number) => Math.min(1, Math.max(0, v));

const visivel = (e: Elemento, t: number, c: EstadoCamera, k: number, W: number, H: number, alto: number) => {
	if (t < nasce(e) - 0.001 || (e.fim != null && t > e.fim + 0.3)) return false;
	const z = Math.pow(c.zoom, k);
	const raio = (Math.hypot(e.w, e.h ?? e.w * 1.3) / 2) * z * 1.4;
	const sx = W / 2 + (e.x - c.x * k) * z, sy = H / 2 + (e.y - c.y * k) * z;
	return sx + raio > -MARGEM && sx - raio < W + MARGEM && sy + raio > -MARGEM && sy - raio < alto + MARGEM;
};

// 0 = imagem/papel, 1 = texto e número, 2 = traço à mão e brilho (o risco que corta a palavra continua cortando)
const camada = (e: Elemento) => (e.tipo === 'traco' || e.tipo === 'brilho' ? 2 : e.tipo === 'texto' || e.tipo === 'numero' ? 1 : 0);

export type PalcoProps = {
	p: PalcoVox;
	W?: number;
	H?: number; // altura de referência do centro da câmera (painel: 960)
	alto?: number; // altura visível (painel com a emenda: 1150)
	zoom?: number; // multiplicador do zoom (cena herdada no split: 0,8; fundo da moldura: 1,4)
	passoCamera?: 1 | 2; // 2 = a cena inteira a 12 fps (fundo da moldura)
};

const Mundo: React.FC<PalcoProps & {W: number; H: number; alto: number}> = ({p, W, H, alto, zoom = 1, passoCamera = 1}) => {
	const f0 = useCurrentFrame();
	const {fps} = useVideoConfig();
	// quadro fracionário dentro do BlurMovimento (amostras sub-quadro): só o fundo a 12 fps é arredondado
	const frame = passoCamera > 1 ? Math.floor(f0 / passoCamera) * passoCamera : f0;
	const t = f0 / fps;
	const c0 = cameraViva(p.camera, frame / fps, p.viva ?? 5);
	const c = {...c0, zoom: c0.zoom * zoom};
	const focoDe = (e: Elemento) => {
		let d = 0, esc = 0.25;
		for (const f of p.focos ?? []) if ((f.grupo === '*' || f.grupo === e.grupo) && t >= f.t) {
			const v = cl((t - f.t) / (f.dur ?? 0.3));
			if (v > d) [d, esc] = [v, f.escurece ?? 0.25];
		}
		return [d, esc] as const;
	};
	const grupoPlano = (k: number, pl: Plano) => {
		const lista = p.elementos.filter((e) => camada(e) === k && (e.plano ?? 'meio') === pl && visivel(e, t, c, PARALLAX[pl], W, H, alto));
		if (!lista.length) return null;
		return (
			<div key={`${k}${pl}`} style={{position: 'absolute', left: 0, top: 0, width: 0, height: 0, transformOrigin: '0 0', transform: transformPlano(c, PARALLAX[pl], W, H)}}>
				{lista.map((e) => {
					const [d, esc] = focoDe(e);
					return <ElementoView key={e.id} e={e} frame={frame} fps={fps} d={d} esc={esc} />;
				})}
			</div>
		);
	};
	// véu: o fundo escurece para o número ou rótulo entrar (fica entre o meio e o 1º plano)
	let veu = 0;
	for (const v of p.veus ?? []) if (t >= v.t && (v.fim == null || t < v.fim + 0.2)) {
		const dentro = cl((t - v.t) / (v.dur ?? 0.4)) * (v.fim == null ? 1 : cl((v.fim + 0.2 - t) / 0.2));
		veu = Math.max(veu, (v.v ?? 0.5) * dentro);
	}
	return (
		<AbsoluteFill style={{overflow: 'hidden', backgroundColor: p.fundo ?? COR.fundo}}>
			{grupoPlano(0, 'fundo')}
			{grupoPlano(0, 'meio')}
			{veu > 0 && <AbsoluteFill style={{background: '#000', opacity: veu}} />}
			{grupoPlano(0, 'frente')}
			{PLANOS.map((pl) => grupoPlano(1, pl))}
			{PLANOS.map((pl) => grupoPlano(2, pl))}
		</AbsoluteFill>
	);
};

// Motion blur de câmera (cópia do PAPER VOX): n cópias do mundo em instantes sub-quadro, somadas; 1 blur leve no conjunto
// quando as amostras ficam espaçadas.
const BlurMovimento: React.FC<{amostras: number; obturador: number; suavizar: number; children: React.ReactNode}> = ({amostras, obturador, suavizar, children}) => {
	const frame = useCurrentFrame();
	const n = Math.max(1, Math.round(amostras));
	return (
		<AbsoluteFill style={{isolation: 'isolate', filter: n > 1 && suavizar > 0.5 ? `blur(${suavizar.toFixed(1)}px)` : undefined}}>
			{Array.from({length: n}, (_, i) => {
				const off = n === 1 ? 0 : obturador * (i / (n - 1) - 0.5);
				return (
					<AbsoluteFill key={i} style={n > 1 ? {mixBlendMode: 'plus-lighter', opacity: 1 / n} : undefined}>
						<Freeze frame={Math.max(0, frame + off)}>{children}</Freeze>
					</AbsoluteFill>
				);
			})}
		</AbsoluteFill>
	);
};

export const Palco: React.FC<PalcoProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const W = props.W ?? 1080, H = props.H ?? 1920, alto = props.alto ?? H;
	const p = props.p;
	const b = p.blur ?? {ativo: true};
	const obt = b.obturador ?? 0.5;
	let n = 1, suavizar = 0;
	if (b.ativo && !DESLIGADO.has('blur') && (props.passoCamera ?? 1) === 1) {
		const v = velocidadeTela(p.camera, frame / fps, 1 / fps, W, H) * (props.zoom ?? 1);
		if (v > (b.limiar ?? 18)) {
			const rastro = v * obt;
			n = Math.min(b.maxAmostras ?? 8, Math.max(3, Math.ceil(rastro / (b.espaco ?? 14)) + 1));
			const espaco = rastro / (n - 1);
			suavizar = espaco > 5 ? espaco * 0.5 : 0;
		}
	}
	return (
		<div style={{position: 'absolute', left: 0, top: 0, width: W, height: alto, overflow: 'hidden'}}>
			<BlurMovimento amostras={n} obturador={obt} suavizar={suavizar}>
				<Mundo {...props} W={W} H={H} alto={alto} />
			</BlurMovimento>
			{/* acabamento só no palco: vinheta e grão (nunca no rosto; Decisões 2026-10-09) */}
			<AbsoluteFill style={{background: `radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,${p.vinheta ?? 0.5}) 100%)`, pointerEvents: 'none'}} />
			{!DESLIGADO.has('grao') && (p.grao ?? 0.07) > 0 && <Grao forca={p.grao ?? 0.07} />}
		</div>
	);
};
