// Legenda pequena do VOX (calibração original, 2026-10-29: "pequena e discreta em tudo", escolha B, como a ref-09 §12): 1–3 palavras
// (blocos do montarBlocos, sem destaque: a palavra grande fica no texto da cena), Inter Tight 700 em caixa alta, branca,
// ~45 px, sombra suave; caixa cinza #81817A só sobre fundo claro. Até 620 px de tinta centrada em x 540 (x 230–850):
// bloco maior encolhe a fonte até caber, nunca vaza. A posição vem do layout do quadro (e muda no mesmo quadro da troca).
import React, {useMemo} from 'react';
import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {montarBlocos} from '../../legendas';
import type {Palavra} from '../../tipos';

const inter = loadInterTight('normal', {weights: ['700'], subsets: ['latin', 'latin-ext']}).fontFamily;
export const LEGENDA = {tamanho: 45, largura: 620, porLetra: 0.64, cinza: '#81817A'};

// estimativa conservadora da largura da tinta (a mesma conta do validar-vox): letras × 0,64 × tamanho
export const tamanhoLegenda = (txt: string) => Math.min(LEGENDA.tamanho, LEGENDA.largura / Math.max(1, txt.length * LEGENDA.porLetra));

export const LegendaVox: React.FC<{t: number; palavras: Palavra[]; y: number; caixa?: boolean}> = ({t, palavras, y, caixa}) => {
	const blocos = useMemo(() => montarBlocos(palavras, []), [palavras]);
	const b = blocos.find((x) => t >= x.ini - 1 / 24 && t < x.fim);
	if (!b) return null;
	const txt = b.palavras.map((p) => p.w.replace(/[.,;:…!?]+$/u, '')).join(' ').toLocaleUpperCase('pt-BR');
	const tam = tamanhoLegenda(txt);
	const lt = t - (b.ini - 1 / 24);
	const e = Math.min(1, lt / (2 / 24)); // entra em 2 quadros, sem pulo
	return (
		<div style={{position: 'absolute', left: 0, width: 1080, top: y, display: 'flex', justifyContent: 'center', transform: `translateY(-50%) translateY(${(1 - e) * 6}px)`, opacity: e, pointerEvents: 'none'}}>
			<div
				style={{
					fontFamily: inter,
					fontWeight: 700,
					fontSize: tam,
					lineHeight: 1.1,
					letterSpacing: '0.01em',
					color: '#FFFFFF',
					whiteSpace: 'nowrap',
					padding: caixa ? '7px 18px 6px' : 0,
					borderRadius: 12,
					background: caixa ? LEGENDA.cinza : undefined,
					textShadow: caixa ? 'none' : '0 2px 10px rgba(0,0,0,0.6), 0 0 3px rgba(0,0,0,0.5)',
				}}
			>
				{txt}
			</div>
		</div>
	);
};
