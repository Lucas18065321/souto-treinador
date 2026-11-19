// INSTAGRAM - VOX - B-ROLLs (vox-broll-instagram, composição VoxBroll; guia referencias/modelos/vox-broll-instagram/
// guia-de-estilo.md). Fixo desde 2026-10-30; nasceu no lab como o formato 5.
// A espinha do dono do canal (2026-10-28/29) em blocos: abertura (rosto + texto digitado + cartão azul da marca), invasao (colagem toma
// a tela), split (uma animação por vez em cima, ele embaixo, emenda esfumada do TD2), ele, mural (câmera contínua com
// mergulho e resquício), moldura (ele meio cortado, cabeça vazando, cards de contexto) e fecho (card final + preto).
// Molde: TelaDividida2.tsx (um <Video> só para o rosto, com o enquadramento do layout do quadro; trocas sem opacidade;
// arredondamento q() das cenas) + palcos do PAPER VOX (Palco.tsx). Copiado, nunca importado de lá para editar.
// Sem música (a trilha entra no mixar-audio.mjs) e sem o sfxAuto do TD2. Render pelo scripts/render-vox.mjs, com
// concurrency 1 e sem angle (<Video> + Sequence estoura o tempo no TD2).
import React, {useMemo} from 'react';
import type {CalculateMetadataFunction} from 'remotion';
import {AbsoluteFill, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';
import {loadFont as loadInterTight} from '@remotion/google-fonts/InterTight';
import {loadFont as loadAnton} from '@remotion/google-fonts/Anton';
import {CURVAS} from '../../kit/tempo';
import type {Palavra} from '../../tipos';
import {Abertura} from './Abertura';
import {CURVAS_VOX} from './camera';
import {DESLIGADO} from './elementos';
import {LegendaVox} from './LegendaVox';
import {MOLDURA, RecorteCabeca, insetLocal, transformDe, type Enquadre} from './Moldura';
import {Palco} from './Palco';
import {DUR_PAPEL, PapelInvade} from './PapelInvade';
import type {BlocoVox, PalcoVox, TrocaPainel, VoxProps} from './tipos';
import {MARCA} from '../../marca';

const W = 1080;
const H = 1920;
const ESFUMA = 190; // emenda esfumada do TD2 (Decisões 2026-10-27: "fica estiloso")
const ESFUMA_CIMA = 230;
const QUEIXO_SPLIT = 1470; // queixo no painel de baixo: acima da linha social do Reels (1531)
const SOBE = 0.8; // split que sobe: assenta em 0,8 s (ref-09 8,00 s)
const cl = (v: number) => Math.max(0, Math.min(1, v));
const opts = {subsets: ['latin', 'latin-ext'] as ('latin' | 'latin-ext')[]};
const inter = loadInterTight('normal', {weights: ['700', '800'], ...opts}).fontFamily;
const anton = loadAnton('normal', {weights: ['400'], ...opts}).fontFamily;

export const calcularVox: CalculateMetadataFunction<VoxProps> = async ({props}) => {
	const _palavras: Palavra[] = Array.isArray(props.palavras) ? props.palavras : await fetch(staticFile(props.palavras)).then((r) => r.json());
	return {durationInFrames: Math.max(1, Math.ceil(props.duracao * 24 - 1e-6)), fps: 24, width: W, height: H, props: {...props, _palavras}};
};

// ---------- trocas dentro do painel (cópia do TD2: só a metade de cima troca) ----------
const DUR_TROCA: Record<TrocaPainel, number> = {corte: 0, chicote: 0.32, mascara: 0.4, zoom: 0.36, blur: 0.32};
const inOut = CURVAS.expo;
const entra = (tipo: TrocaPainel, p: number): React.CSSProperties => {
	const e = inOut(cl(p));
	if (p >= 1) return {};
	if (tipo === 'zoom') return {transform: `scale(${1.35 - 0.35 * e})`, filter: `blur(${14 * (1 - e)}px)`, opacity: cl(p * 2.2)};
	if (tipo === 'chicote') return {transform: `translateX(${W * (1 - e)}px) scaleX(${1 + 0.18 * Math.sin(Math.PI * e)})`, filter: `blur(${16 * Math.sin(Math.PI * Math.min(1, e + 0.15))}px)`};
	if (tipo === 'mascara') {
		const x = -0.45 * W + e * 1.9 * W;
		return {clipPath: `polygon(0 0, ${x + 0.3 * W}px 0, ${x}px 100%, 0 100%)`};
	}
	if (tipo === 'blur') return {filter: `blur(${16 * (1 - e)}px)`, opacity: e};
	return {};
};
// a cena velha anda menos que a nova no chicote: 2–3 q dela sobram na borda (ref-09 10,73 s)
const sai = (tipo: TrocaPainel, q: number): React.CSSProperties => {
	const e = inOut(cl(q));
	if (q <= 0) return {};
	if (tipo === 'zoom') return {transform: `scale(${1 + 0.7 * e})`, filter: `blur(${18 * e}px)`, opacity: 1 - e};
	if (tipo === 'chicote') return {transform: `translateX(${-0.35 * W * e}px)`, filter: `blur(${12 * Math.sin(Math.PI * e)}px)`};
	if (tipo === 'mascara') return {filter: `brightness(${1 - 0.35 * e})`};
	return {};
};
const FioMascara: React.FC<{p: number; alto: number}> = ({p, alto}) => {
	if (p <= 0 || p >= 1) return null;
	const e = inOut(cl(p));
	const x = -0.45 * W + e * 1.9 * W;
	const ang = (Math.atan2(alto, 0.3 * W) * 180) / Math.PI;
	return <div style={{position: 'absolute', left: x + 0.15 * W - 60, top: alto / 2 - alto * 0.7, width: 120, height: alto * 1.4, transform: `rotate(${90 - ang}deg)`, background: 'linear-gradient(90deg, transparent 0%, rgba(255,236,214,0.55) 45%, rgba(255,255,255,0.9) 50%, rgba(255,236,214,0.55) 55%, transparent 100%)', filter: 'blur(6px)', mixBlendMode: 'screen'}} />;
};
// emenda esfumada; desl = quanto o painel dele ainda está abaixo do lugar (split que sobe): a emenda desce junto e a cena
// de cima continua cobrindo a tela inteira, sem faixa preta
const mascaraEmenda = (desl: number) => {
	const y0 = H / 2 - ESFUMA_CIMA + desl;
	const y1 = H / 2 + ESFUMA + desl;
	const n = 24;
	const p = Array.from({length: n + 1}, (_, i) => {
		const x = i / n;
		const s = x * x * x * (x * (6 * x - 15) + 10);
		return `rgba(0,0,0,${(1 - s).toFixed(4)}) ${(y0 + x * (y1 - y0)).toFixed(1)}px`;
	}).join(', ');
	return `linear-gradient(to bottom, #000 0, ${p})`;
};

// ---------- painel de cima do split: uma animação por vez ----------
const Painel: React.FC<{b: BlocoVox; t: number; palcos: Record<string, PalcoVox>; sobe: number}> = ({b, t, palcos, sobe}) => {
	const alto = Math.min(H, H / 2 + ESFUMA + sobe);
	const anims = b.animacoes ?? [];
	const iAtual = anims.reduce((k, a, i) => (t >= a.ini ? i : k), -1);
	const lt = t - b.ini;
	const camadas: React.ReactNode[] = [];
	// cena herdada (vinda da invasão): encolhe ~20% e é recortada em 9:8 enquanto o painel dele sobe
	const herdada = (estilo: React.CSSProperties) => {
		const e = CURVAS_VOX.cubica(cl(lt / SOBE));
		return (
			<div key="herdada" style={{position: 'absolute', inset: 0, overflow: 'hidden', ...estilo}}>
				<Palco p={palcos[b.herda!]} W={W} H={H - (H / 2) * e} alto={alto} zoom={1 - 0.2 * e} />
			</div>
		);
	};
	const anim = (i: number, estilo: React.CSSProperties) => (
		<div key={`a${i}`} style={{position: 'absolute', inset: 0, overflow: 'hidden', ...estilo}}>
			<Palco p={palcos[anims[i].palco]} W={W} H={H / 2} alto={alto} />
		</div>
	);
	let fio: React.ReactNode = null;
	if (iAtual < 0) {
		if (b.herda) camadas.push(herdada({}));
	} else {
		const a = anims[iAtual];
		const tipo = a.troca ?? 'corte';
		const D = DUR_TROCA[tipo];
		const p = D ? (t - a.ini) / D : 1;
		if (p < 1) {
			if (iAtual > 0) camadas.push(anim(iAtual - 1, sai(tipo, p)));
			else if (b.herda) camadas.push(herdada(sai(tipo, p)));
		}
		camadas.push(anim(iAtual, entra(tipo, p)));
		if (tipo === 'mascara') fio = <FioMascara p={p} alto={alto} />;
	}
	return (
		<div style={{position: 'absolute', top: 0, width: W, height: alto, overflow: 'hidden', WebkitMaskImage: mascaraEmenda(sobe), maskImage: mascaraEmenda(sobe)}}>
			{camadas}
			{fio}
		</div>
	);
};

// ---------- card final (cópia do CardTexto do TD2: o @ só aqui; Decisões 2026-10-08) ----------
const CardFinal: React.FC<{texto: string; lt: number}> = ({texto, lt}) => {
	const partes = texto.split(/(\*[^*]+\*)/).filter(Boolean);
	let k = 0;
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 42%, #1d1a20 0%, #0E0C10 70%)', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 60}}>
			<div style={{transform: `scale(${1 + 0.03 * cl(lt / 1.5)})`}}>
				{partes.map((parte, i) => {
					const chave = parte.startsWith('*');
					const palavras = parte.replace(/\*/g, '').trim().split(/\s+/);
					return (
						<div key={i} style={{display: 'block'}}>
							{palavras.map((w, j) => {
								const t0 = 0.08 + k++ * 0.08;
								const e = interpolate(lt, [t0, t0 + 0.3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: CURVAS.entrada});
								return chave ? (
									<span key={j} style={{display: 'inline-block', marginRight: '0.18em', opacity: e, transform: `scale(${0.8 + 0.2 * e}) translateY(${(1 - e) * 26}px)`, filter: `blur(${(1 - e) * 10}px)`}}>
										<span style={{fontFamily: anton, fontSize: 168, lineHeight: 1.05, textTransform: 'uppercase', backgroundImage: MARCA.degrades['claro-aco'], WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', padding: '0.08em 0.06em 0'}}>{w}</span>
									</span>
								) : (
									<span key={j} style={{display: 'inline-block', marginRight: '0.3em', fontFamily: inter, fontWeight: 800, fontSize: 54, letterSpacing: '0.03em', textTransform: w.startsWith('@') ? 'none' : 'uppercase', color: MARCA.creme, opacity: e, transform: `translateY(${(1 - e) * 16}px)`, filter: `blur(${(1 - e) * 8}px)`}}>
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

// Escala mínima que centraliza o rosto em x sem abrir faixa preta nas laterais.
const zBaseDe = (x: number) => Math.max(1, 540 / x, 540 / (W - x)) + 0.004;

export const VoxBroll: React.FC<VoxProps> = (p) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	DESLIGADO.clear();
	for (const d of p._desligar ?? []) DESLIGADO.add(d);
	const ini = p.ini ?? 0;
	const palavras = p._palavras ?? (Array.isArray(p.palavras) ? p.palavras : []);
	const t = ini + frame / fps;
	// bloco do quadro pelo MESMO arredondamento em quadros (TD2: por tempo, a fronteira escapava 1 quadro)
	const q = (s: number) => Math.round((s - ini) * fps);
	let idx = p.blocos.findIndex((b) => frame >= q(b.ini) && frame < q(b.fim));
	if (idx < 0) idx = frame < q(p.blocos[0].ini) ? 0 : p.blocos.length - 1;
	const b = p.blocos[idx];
	const ant = p.blocos[idx - 1];
	const lt = t - b.ini;
	const dur = b.fim - b.ini;
	const R = b.rosto ?? p.rosto;
	const zb = zBaseDe(R.x);

	// ---- rosto: um <Video> só; enquadramento pelo layout do quadro ----
	const punchEm = (bl: BlocoVox, tt: number) => (bl.punches ?? []).reduce((z, k) => (tt >= k.t - 1e-6 ? k.z : z), 1);
	const pushAbertura = (bl: BlocoVox, tt: number) => 1 + (bl.abertura?.push ?? 0.07) * CURVAS.entrada(cl((tt - bl.ini) / Math.max(0.1, bl.fim - bl.ini)));
	const tela = (z: number): Enquadre => ({z, tx: 540 - z * R.x, ty: R.queixo - z * R.queixo}); // queixo parado no punch
	let rosto: Enquadre | null = null;
	let clip: string | undefined;
	let sobe = 0;
	if (b.layout === 'ele' || b.layout === 'fecho') rosto = tela(zb * punchEm(b, t));
	else if (b.layout === 'abertura') rosto = tela(zb * pushAbertura(b, t));
	else if (b.layout === 'invasao' && b.entrada === 'papel' && lt < DUR_PAPEL.cobre && ant?.layout === 'abertura') {
		const Ra = ant.rosto ?? p.rosto, za = zBaseDe(Ra.x) * pushAbertura(ant, ant.fim);
		rosto = {z: za, tx: 540 - za * Ra.x, ty: Ra.queixo - za * Ra.queixo}; // o papel come o rosto da abertura
	}
	else if (b.layout === 'split') {
		const z = zb * (1 + 0.03 * cl(lt / dur));
		sobe = b.herda ? (H - (H / 2 - ESFUMA_CIMA)) * (1 - CURVAS_VOX.cubica(cl(lt / SOBE))) : 0;
		rosto = {z, tx: 540 - z * R.x, ty: QUEIXO_SPLIT - z * R.queixo + sobe};
		clip = insetLocal({...rosto, ty: rosto.ty - sobe}, 0, H / 2 - ESFUMA_CIMA, W, H);
	} else if (b.layout === 'moldura') {
		// olhos na borda de cima da moldura e topo da cabeça em ~1095 (ref-08 mov §3.1)
		const z = (MOLDURA.y0 - MOLDURA.topoCabeca) / Math.max(40, R.olhos - R.topo);
		rosto = {z, tx: 540 - z * R.x, ty: MOLDURA.y0 - z * R.olhos};
		clip = insetLocal(rosto, MOLDURA.x0, MOLDURA.y0, MOLDURA.x1, MOLDURA.y1 + 200, MOLDURA.raio, 0);
	}

	// ---- legenda: posição pelo layout do quadro (muda no mesmo quadro da troca) ----
	const cardFinal = b.layout === 'fecho' && b.card && t >= b.card.ini;
	const legendaY = b.legenda?.y ?? (b.layout === 'split' || b.layout === 'moldura' ? 960 : b.layout === 'ele' || b.layout === 'fecho' ? Math.min(1460, R.queixo + 50) : 1300);
	// sem legenda enquanto o papel cobre a tela (branca sobre o papel claro, ela some)
	const papelNaTela = b.layout === 'invasao' && b.entrada === 'papel' && lt < DUR_PAPEL.cobre + DUR_PAPEL.estoura + DUR_PAPEL.abre;
	const mostraLegenda = b.layout !== 'abertura' && !b.legenda?.ocultar && !cardFinal && !papelNaTela && !(p.preto != null && t >= p.preto);

	const sons = useMemo(() => p.sfxNaMixagem ? [] : (p.sfx ?? []), [p.sfx, p.sfxNaMixagem]);
	const preto = p.preto != null ? cl((t - p.preto) / 0.2) : 0;

	return (
		<AbsoluteFill style={{background: '#000'}}>
			{/* atrás do rosto: fundo da moldura, cards e a cabeça recortada */}
			{b.layout === 'moldura' && b.palco && (
				<>
					<Palco p={{...p.palcos[b.palco], focos: [{t: -1e9, grupo: '*', escurece: b.moldura?.escurece ?? 0.18}], blur: {ativo: false}}} zoom={b.moldura?.zoomFundo ?? 1.4} passoCamera={2} />
					{b.moldura?.cards && <Palco p={p.palcos[b.moldura.cards]} />}
					{b.moldura?.recorte && rosto && <RecorteCabeca {...b.moldura.recorte} tBruto={t} q={rosto} />}
				</>
			)}
			<Video src={staticFile(p.bruto)} trimBefore={Math.round(ini * fps)} muted style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: rosto ? transformDe(rosto) : undefined, clipPath: clip, opacity: rosto ? 1 : 0}} />
			{/* na frente do rosto: palcos de tela cheia e o painel do split */}
			{(b.layout === 'invasao' || b.layout === 'mural') && b.palco && (b.entrada !== 'papel' || lt >= DUR_PAPEL.cobre) && <Palco p={p.palcos[b.palco]} />}
			{b.layout === 'split' && <Painel b={b} t={t} palcos={p.palcos} sobe={sobe} />}
			{b.layout === 'abertura' && b.abertura && <Abertura a={b.abertura} t={t} ini={b.ini} />}
			{b.layout === 'invasao' && b.entrada === 'papel' && <PapelInvade t={t} t0={b.ini} id={`pi${idx}`} />}
			{mostraLegenda && <LegendaVox t={t} palavras={palavras} y={legendaY} caixa={b.legenda?.caixa} />}
			{cardFinal && <CardFinal texto={b.card!.texto} lt={t - b.card!.ini} />}
			{preto > 0 && <AbsoluteFill style={{background: '#000', opacity: preto}} />}
			<Audio src={staticFile(p.voz ?? p.bruto)} trimBefore={Math.round(ini * fps)} />
			{sons.map((s, i) => {
				const de = Math.round((s.t - ini) * fps);
				if (de < 0 || de > p.duracao * fps) return null;
				return (
					<Sequence key={`s${i}`} from={de} durationInFrames={Math.round(3 * fps)}>
						<Audio src={staticFile(s.som)} volume={s.vol ?? 0.3} />
					</Sequence>
				);
			})}
		</AbsoluteFill>
	);
};
