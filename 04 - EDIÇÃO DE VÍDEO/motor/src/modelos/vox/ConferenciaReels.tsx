// Quadro de conferência do VOX (guia, "Área morta do Reels", medida em 2026-10-29): o quadro da VoxBroll com uma
// imitação da interface do Reels por cima (abas, coluna de botões com contagens em pt-BR, linha social, @/Seguir/áudio e
// legenda do post) e as linhas da faixa segura (y 240 e 1500; x 90; x 850 abaixo de y 1000; x 990 acima). Só para
// conferir (registrada só no src/lab/RootLab.tsx): nada disto vai para o vídeo. Ícones do lucide-react; texto em HTML.
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Heart, MessageCircle, Music2, Ellipsis, Repeat2, Send} from 'lucide-react';
import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {VoxBroll} from './VoxBroll';
import type {VoxProps} from './tipos';
import {MARCA} from '../../marca';

const inter = loadInterTight('normal', {weights: ['500', '700'], subsets: ['latin', 'latin-ext']}).fontFamily;
const sombra = '0 1px 6px rgba(0,0,0,0.55)';
const txt = (tam: number, peso = 600): React.CSSProperties => ({fontFamily: inter, fontSize: tam, fontWeight: peso, color: '#fff', textShadow: sombra, whiteSpace: 'nowrap'});

const Botao: React.FC<{y: number; icone: React.ReactNode; n?: string}> = ({y, icone, n}) => (
	<div style={{position: 'absolute', left: 913, width: 81, top: y, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
		{icone}
		{n && <div style={txt(30, 600)}>{n}</div>}
	</div>
);

export const InterfaceReels: React.FC<{guias?: boolean}> = ({guias = true}) => {
	const ic = {size: 70, color: '#fff', strokeWidth: 2.1, style: {filter: 'drop-shadow(0 1px 5px rgba(0,0,0,0.5))'}};
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,0.28) 0, rgba(0,0,0,0) 240px, rgba(0,0,0,0) 1450px, rgba(0,0,0,0.45) 1920px)'}} />
			<div style={{position: 'absolute', top: 18, left: 40, ...txt(34, 600)}}>9:41</div>
			<div style={{position: 'absolute', top: 118, width: 1080, display: 'flex', justifyContent: 'center', gap: 46}}>
				<span style={txt(44, 700)}>Reels</span>
				<span style={{...txt(44, 500), opacity: 0.7}}>Amigos</span>
			</div>
			<Botao y={1042} icone={<Heart {...ic} />} n="12,3 mil" />
			<Botao y={1205} icone={<MessageCircle {...ic} />} n="321" />
			<Botao y={1368} icone={<Repeat2 {...ic} />} n="1.204" />
			<Botao y={1531} icone={<Send {...ic} />} n="2.876" />
			<Botao y={1700} icone={<Ellipsis {...ic} />} />
			<div style={{position: 'absolute', left: 921, top: 1802, width: 64, height: 64, borderRadius: 10, border: '3px solid #fff', background: 'linear-gradient(135deg,#2E49CE,#8C9BE4)'}} />
			<div style={{position: 'absolute', left: 36, top: 1555, ...txt(32, 500), opacity: 0.92}}>Curtido por pessoa_x e outras 12,3 mil pessoas</div>
			<div style={{position: 'absolute', left: 36, top: 1624, ...txt(32, 500), opacity: 0.92}}>Ver as 321 respostas</div>
			<div style={{position: 'absolute', left: 36, top: 1715, display: 'flex', alignItems: 'center', gap: 18}}>
				<div style={{width: 84, height: 84, borderRadius: 42, border: '3px solid #fff', background: '#555'}} />
				<span style={txt(36, 700)}>{MARCA.arroba.replace(/^@/, '')}</span>
				<span style={{...txt(32, 700), border: '2px solid rgba(255,255,255,0.85)', borderRadius: 12, padding: '6px 18px'}}>Seguir</span>
			</div>
			<div style={{position: 'absolute', left: 36, top: 1834, display: 'flex', alignItems: 'center', gap: 12, ...txt(32, 500)}}>
				<Music2 size={34} color="#fff" strokeWidth={2.2} /> Áudio original · legenda do post…
			</div>
			{guias && (
				<>
					{/* faixa segura: topo 240, base 1500, laterais 90; x 850 abaixo de y 1000, x 990 acima */}
					<div style={{position: 'absolute', left: 90, top: 240, width: 900, height: 760, border: '3px dashed rgba(255,214,0,0.95)', borderBottom: 'none'}} />
					<div style={{position: 'absolute', left: 90, top: 1000, width: 760, height: 500, border: '3px dashed rgba(255,214,0,0.95)', borderTop: 'none'}} />
					<div style={{position: 'absolute', left: 850, top: 1000, width: 140, height: 0, borderTop: '3px dashed rgba(255,214,0,0.95)'}} />
				</>
			)}
		</AbsoluteFill>
	);
};

export const ConferenciaReels: React.FC<VoxProps> = (p) => (
	<AbsoluteFill>
		<VoxBroll {...p} />
		<InterfaceReels />
	</AbsoluteFill>
);
