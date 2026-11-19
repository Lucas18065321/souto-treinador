// PapelInvade (ref-08 mov §1.1; entrada 1 da `invasao`): manchas de papel amassado nascem nas bordas e comem a tela em
// 0,10 s (25% → 70% → 100%), estouram para o claro em mais 0,10 s e o claro se abre sobre a cena já montada. Nada nasce
// do preto (TD2). Formas em <polygon> de um clipPath SVG (sem texto no SVG).
import React from 'react';
import {prng, papelAmassado} from './texturas';

const W = 1080, H = 1920;
const cl = (v: number) => Math.min(1, Math.max(0, v));
// centros nas bordas e nos cantos (+ o meio, que fecha o último buraco) e o atraso de cada mancha (fração dos 0,10 s)
const MANCHAS: [number, number, number, number][] = [
	[-40, -60, 760, 0], [560, -140, 700, 0.15], [1120, -40, 760, 0.05], [1180, 700, 720, 0.2], [1140, 1460, 760, 0.1],
	[1100, 2000, 800, 0.0], [520, 2060, 740, 0.25], [-60, 1960, 800, 0.08], [-140, 1180, 720, 0.18], [-120, 520, 700, 0.3], [540, 960, 640, 0.55],
];

const forma = (cx: number, cy: number, raio: number, sem: number) => {
	const r = prng(sem);
	const n = 22;
	return Array.from({length: n}, (_, i) => {
		const a = (i / n) * Math.PI * 2;
		const k = raio * (0.82 + r() * 0.3);
		return `${(cx + Math.cos(a) * k).toFixed(1)},${(cy + Math.sin(a) * k).toFixed(1)}`;
	}).join(' ');
};

export const DUR_PAPEL = {cobre: 0.1, estoura: 0.1, abre: 0.14};

export const PapelInvade: React.FC<{t: number; t0: number; id?: string}> = ({t, t0, id = 'pi'}) => {
	const lt = t - t0;
	const {cobre, estoura, abre} = DUR_PAPEL;
	if (lt < 0 || lt > cobre + estoura + abre) return null;
	const pc = cl(lt / cobre);
	const claro = cl((lt - cobre) / estoura); // estouro para o claro
	const some = cl((lt - cobre - estoura) / abre); // o claro se abre sobre a cena
	return (
		<div style={{position: 'absolute', inset: 0, opacity: 1 - some, pointerEvents: 'none'}}>
			<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0}}>
				<defs>
					<clipPath id={`papel-${id}`}>
						{MANCHAS.map(([x, y, R, atraso], i) => {
							const p = cl((pc - atraso * 0.5) / (1 - atraso * 0.5));
							return p > 0 ? <polygon key={i} points={forma(x, y, R * (0.25 + 0.95 * Math.pow(p, 0.8)), i + 3)} /> : null;
						})}
					</clipPath>
				</defs>
				<image href={papelAmassado(W, H)} x={0} y={0} width={W} height={H} preserveAspectRatio="none" clipPath={`url(#papel-${id})`} />
			</svg>
			{claro > 0 && <div style={{position: 'absolute', inset: 0, background: '#FBF8F2', opacity: claro}} />}
		</div>
	);
};
