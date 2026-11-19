// Moldura do VOX (ref-08 mov §3.1; dono do canal, 2026-10-29: entre o mural e o split 2, com cards de contexto): ele "meio
// cortado no cenário", numa moldura embaixo (x 58–1021, y 1354–1920, raio 102 nos cantos de cima, sem borda nem sombra),
// com a cabeça vazando por cima da animação a partir da linha dos olhos (topo da cabeça em ~y 1095).
// Matte da cabeça = sequência WebP do scripts/recortar.mjs (q0001.webp…), lida com <Img> quadro a quadro como o
// `Recortado` do src/modelos/MotorCamadas.tsx (copiado: nunca OffthreadVideo, que falha com "No frame found").
import React from 'react';
import {Img, staticFile} from 'remotion';

export const MOLDURA = {x0: 58, x1: 1021, y0: 1354, y1: 1920, raio: 102, topoCabeca: 1095};

export type Enquadre = {tx: number; ty: number; z: number};
// bruto (px) → tela: tela = t + z·bruto (transform-origin 0 0)
export const transformDe = (q: Enquadre) => `translate(${q.tx.toFixed(2)}px, ${q.ty.toFixed(2)}px) scale(${q.z.toFixed(5)})`;

// Retângulo da TELA → inset() no espaço local do vídeo (1080×1920), para o clip-path acompanhar o transform.
export const insetLocal = (q: Enquadre, x0: number, y0: number, x1: number, y1: number, raio = 0, raioBaixo = 0) => {
	const L = (x0 - q.tx) / q.z, T = (y0 - q.ty) / q.z, R = (x1 - q.tx) / q.z, B = (y1 - q.ty) / q.z;
	const top = Math.max(0, T), left = Math.max(0, L), right = Math.max(0, 1080 - R), bottom = Math.max(0, 1920 - B);
	const r = raio / q.z, rb = raioBaixo / q.z;
	return `inset(${top.toFixed(1)}px ${right.toFixed(1)}px ${bottom.toFixed(1)}px ${left.toFixed(1)}px${raio || raioBaixo ? ` round ${r.toFixed(1)}px ${r.toFixed(1)}px ${rb.toFixed(1)}px ${rb.toFixed(1)}px` : ''})`;
};

// Cabeça recortada: o mesmo enquadre do rosto da moldura, cortada para mostrar só o que fica ACIMA da moldura.
export const RecorteCabeca: React.FC<{arquivo: string; brutoIni: number; fps: number; tBruto: number; q: Enquadre; nMax?: number}> = ({arquivo, brutoIni, fps, tBruto, q, nMax}) => {
	// quadro MAIS PRÓXIMO, não floor: o brutoIni vem arredondado (14,4167 × 14,41666…) e o floor dava 28,999 → 1 quadro
	// atrasado; nas emendas do bruto, a cabeça ficava de antes do corte e o rosto de depois (vitrine, 15,6 s)
	const n0 = Math.round((tBruto - brutoIni) * fps) + 1;
	if (n0 < 1) return null;
	const n = nMax ? Math.min(n0, nMax) : n0;
	return (
		<Img
			src={staticFile(`${arquivo}q${String(n).padStart(4, '0')}.webp`)}
			style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, transformOrigin: '0 0', transform: transformDe(q), clipPath: insetLocal(q, 0, 0, 1080, MOLDURA.y0 + 2)}}
		/>
	);
};
