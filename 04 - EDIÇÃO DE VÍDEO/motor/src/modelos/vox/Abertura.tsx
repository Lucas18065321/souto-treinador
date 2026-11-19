// Abertura do VOX (calibração original, 2026-10-29, pergunta 2 = B; ref-09 §5.1 "LOOK AT THIS" + "Vox"): rosto em tela cheia,
// TextoDigitado (Instrument Serif reta em caixa alta, creme, 2–3 letras por passo, cada pedaço 0–2 q antes da palavra)
// e CartaoAba (azul da marca, abre como aba girando na própria borda em 0,17 s; a palavra acende em 0,20 s NA palavra falada).
// Os dois crescem devagar (~10% o texto, ~2% o cartão) e saem juntos em 0,20 s (dissolve + desfoque) antes de a
// invasão chegar neles. Nunca sobre o rosto: o gerador mede a cabeça e o validar-vox confere.
import React from 'react';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {CURVAS} from '../../kit/tempo';
import {FONTES} from '../../kit/fontes';
import {letrasDigitadas} from './elementos';
import type {AberturaVox} from './tipos';
import {MARCA} from '../../marca';

const anton = loadAnton('normal', {weights: ['400'], subsets: ['latin', 'latin-ext']}).fontFamily;
const cl = (v: number) => Math.min(1, Math.max(0, v));
export const ACENTO = MARCA.acento;

export const TextoDigitado: React.FC<{a: AberturaVox; t: number; cresce: number}> = ({a, t, cresce}) => {
	const tam = a.texto.tamanho ?? 124;
	return (
		<div style={{position: 'absolute', left: a.texto.x, top: a.texto.y, transformOrigin: '0 0', transform: `scale(${cresce})`, fontFamily: FONTES.serifaReta.family, fontSize: tam, lineHeight: 0.98, color: '#F2F4F8', textTransform: 'uppercase', whiteSpace: 'nowrap', filter: 'drop-shadow(0 4px 14px rgba(0,0,0,0.55)) drop-shadow(0 0 2px rgba(0,0,0,0.35))'}}>
			{a.linhas.map((linha, i) => (
				<div key={i}>
					{linha.map((p, j) => {
						const n = letrasDigitadas(t, p.t - 1 / 24, p.w.length);
						return (
							<span key={j} style={{marginRight: j < linha.length - 1 ? '0.24em' : 0}}>
								{p.w.slice(0, n)}
								<span style={{opacity: 0}}>{p.w.slice(n)}</span>
							</span>
						);
					})}
				</div>
			))}
		</div>
	);
};

export const CartaoAba: React.FC<{a: AberturaVox; t: number; cresce: number}> = ({a, t, cresce}) => {
	const c = a.cartao;
	const abre0 = c.t - 0.23; // a aba termina de abrir ~0,06 s antes da palavra
	if (t < abre0) return null;
	const pa = CURVAS.entrada(cl((t - abre0) / 0.17));
	const pw = CURVAS.entrada(cl((t - (c.t - 1 / 24)) / 0.2));
	const brilho = cl((t - c.t - 0.05) / 0.32); // risco de brilho que corre no canto, 1×
	const tam = Math.min(c.h * 0.62, (c.w * 0.86) / Math.max(1, c.palavra.length * 0.5));
	return (
		<div style={{position: 'absolute', left: c.x - c.w / 2, top: c.y - c.h / 2, width: c.w, height: c.h, perspective: 900, transform: `rotate(${c.rot ?? -3}deg) scale(${cresce})`}}>
			<div style={{position: 'absolute', inset: 0, transformOrigin: '50% 0', transform: `rotateX(${-92 * (1 - pa)}deg)`, background: `linear-gradient(160deg, #445DB4 0%, ${ACENTO} 55%, #1F33A3 100%)`, borderRadius: 6, overflow: 'hidden', boxShadow: '0 18px 40px rgba(0,0,0,0.45)'}}>
				{brilho > 0 && brilho < 1 && (
					<div style={{position: 'absolute', top: -c.h, left: c.w * (0.45 + 0.7 * brilho), width: 70, height: c.h * 3, transform: 'rotate(28deg)', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent)', filter: 'blur(4px)'}} />
				)}
				<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: anton, fontSize: tam, lineHeight: 1, color: '#FFFFFF', textTransform: 'uppercase', letterSpacing: '0.02em', paddingTop: tam * 0.06, opacity: pw, transform: `scale(${1.06 - 0.06 * pw})`, textShadow: `0 0 ${18 * pw}px rgba(255,235,225,${0.35 * pw})`}}>
					{c.palavra}
				</div>
			</div>
		</div>
	);
};

export const Abertura: React.FC<{a: AberturaVox; t: number; ini: number}> = ({a, t, ini}) => {
	const q = cl((t - a.sai) / 0.2);
	if (q >= 1) return null;
	const vida = Math.max(0.1, a.sai - ini);
	const u = cl((t - ini) / vida);
	return (
		<div style={{position: 'absolute', inset: 0, opacity: 1 - q, filter: q > 0 ? `blur(${(10 * q).toFixed(1)}px)` : undefined}}>
			<TextoDigitado a={a} t={t} cresce={1 + 0.1 * u} />
			<CartaoAba a={a} t={t} cresce={1 + 0.02 * u} />
		</div>
	);
};
