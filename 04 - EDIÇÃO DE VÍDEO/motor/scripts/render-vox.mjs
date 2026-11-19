// Render do INSTAGRAM - VOX - B-ROLLs (modelo fixo vox-broll-instagram, desde 2026-10-30). Separado do render.mjs de
// propósito, como o render-paper-vox.mjs: os outros modelos não mudam, e este tem áudio próprio (a composição toca só a
// voz do bruto; os SFX, com sfxNaMixagem, e a trilha entram depois pelo mixar-audio.mjs, com loudnorm de 2 passadas).
// Render pela API do Remotion com os padrões do vídeo aprovado (creatina): concurrency 1 e sem angle (<Video> dentro de
// Sequence estoura o tempo com angle, TD2). Com concurrency 1 os quadros saem em ordem e o tempo entre dois avisos de
// progresso é o tempo daquele quadro: o fim imprime os s de render por s de vídeo de cada bloco (nasceu no lab como
// scripts/lab/render-medido.mjs).
// Uso (de dentro do motor, SEMPRE pela fila):
//   node scripts/vez.mjs node scripts/render-vox.mjs <proj> [--previa] [--trecho a b] [--trilhas A,B | --sem-trilha]
//     [--props 03_roteiro/vox.json] [--saida f.mp4] [--manter-base] [--concurrency 1] [--gl nenhum|angle]
//   --previa → metade da resolução, CRF 26, em 06_previas/previa_<data>_vox[_trecho][_trilha-<X>].mp4; padrão: todas as
//              trilhas de props.musicas (para comparar). Final → 1080×1920, CRF 17, AAC 320k, em 07_final/<proj>_final.mp4,
//              com a trilha escolhida (props.musica).
//   --manter-base → guarda o vídeo sem trilha (<saída>.base.mp4) para remisturar com o mixar-audio.mjs (refino dos SFX).
// Tempo medido no piloto (creatina, 112,3 s, resolução cheia, ~1,3 GB livres): 626 s de render (5,6 s/s; pior bloco, a
// moldura, 14,2 s/s) + ~75 s do mixar-audio --final. Avise o dono do canal antes de rodar.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import {binariosRemotion} from './lib/binarios.mjs';
import MODELOS from '../src/modelos.json' with {type: 'json'};
import * as CAM from './lib/caminhos.mjs';

const MOTOR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RAIZ = CAM.RAIZ;
const ID = 'vox-broll-instagram';
const args = process.argv.slice(2);
const opcao = (nome, padrao = null) => (args.includes(nome) ? args[args.indexOf(nome) + 1] : padrao);
const proj = path.resolve(args[0] ?? '');
if (!args[0] || !fs.existsSync(proj)) {
	console.error('Uso: node scripts/vez.mjs node scripts/render-vox.mjs <proj> [--previa] [--trecho a b] [--trilhas A,B | --sem-trilha] [--props 03_roteiro/vox.json] [--saida f] [--manter-base] [--concurrency 1]');
	process.exit(1);
}
const propsPath = path.resolve(proj, opcao('--props', '03_roteiro/vox.json'));
if (!fs.existsSync(propsPath)) {
	console.error(`[vox] não achei ${CAM.mostrar(propsPath)}: rode antes o gerador (node 03_roteiro/montar_<slug>.mjs)`);
	process.exit(1);
}
const props = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
if (props.modelo !== ID) {
	console.error(`[vox] o props é do modelo "${props.modelo}", não do ${ID}`);
	process.exit(1);
}
const mod = MODELOS.modelos[ID];
const previa = args.includes('--previa');
const ti = args.indexOf('--trecho');
const trecho = ti === -1 ? null : [Number(args[ti + 1]), Number(args[ti + 2])];
const gl = opcao('--gl', mod.gl ?? 'nenhum');
const conc = Number(opcao('--concurrency', '1'));
const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '');
const faixa = trecho ? `_${trecho[0]}-${trecho[1]}s` : '';
const saidaFinal = opcao('--saida') ? path.resolve(opcao('--saida')) : path.join(proj, previa ? '06_previas' : '07_final', previa ? `previa_${stamp}_vox${faixa}.mp4` : `${path.basename(proj)}_final${faixa}.mp4`);
fs.mkdirSync(path.dirname(saidaFinal), {recursive: true});
const base = saidaFinal.replace(/\.mp4$/, '.base.mp4');

// trilhas: --sem-trilha | --trilhas A,B | prévia = todas as opções | final = a escolhida
const opcoes = Object.keys(props.musicas ?? {});
const semTrilha = args.includes('--sem-trilha');
const trilhas = semTrilha ? [] : opcao('--trilhas') ? opcao('--trilhas').split(',') : previa && opcoes.length > 1 ? opcoes : props.musica || props.sfxNaMixagem ? [null] : [];
for (const t of trilhas) if (t && !props.musicas?.[t]) {
	console.error(`[vox] trilha ${t} não está em props.musicas (${opcoes.join(', ') || 'nenhuma'})`);
	process.exit(1);
}

// 1. render da composição (voz do bruto) sem loudnorm, pela API: bundle 1 vez, tempo de cada quadro
const bin = binariosRemotion(MOTOR).find((a) => a.startsWith('--binaries-directory='))?.split('=')[1];
const chromiumOptions = gl !== 'nenhum' ? {gl} : {};
const t0 = Date.now();
const serveUrl = await bundle({entryPoint: path.join(MOTOR, 'src', 'index.ts'), publicDir: proj});
const tBundle = (Date.now() - t0) / 1000;
const composition = await selectComposition({serveUrl, id: mod.composicao, inputProps: props, binariesDirectory: bin, logLevel: 'error', chromiumOptions});
const fps = composition.fps;
const frameRange = trecho ? [Math.round(trecho[0] * fps), Math.round(trecho[1] * fps) - 1] : null;
const f0 = frameRange ? frameRange[0] : 0;
const nQ = frameRange ? frameRange[1] - frameRange[0] + 1 : composition.durationInFrames;
const dur = nQ / fps;
console.log(`[vox] ${mod.nome} · ${previa ? 'prévia' : 'final'} · ${dur.toFixed(1)} s · concurrency ${conc} · gl ${gl} → ${CAM.mostrar(saidaFinal)}${trilhas.filter(Boolean).length > 1 ? ` (+ ${trilhas.length} trilhas)` : ''} (bundle ${tBundle.toFixed(0)} s)`);
let ms = [];
const tRender0 = Date.now();
for (let tentativa = 1; tentativa <= 2; tentativa++) {
	ms = [];
	let ultimo = 0, tUlt = Date.now(), pct = -1;
	try {
		await renderMedia({
			composition, serveUrl, codec: 'h264', audioCodec: 'aac', outputLocation: base, inputProps: props, concurrency: conc, frameRange,
			crf: previa ? 26 : 17, scale: previa ? 0.5 : 1, ...(previa ? {} : {audioBitrate: '320k'}), binariesDirectory: bin, logLevel: 'error', chromiumOptions,
			onProgress: ({renderedFrames}) => {
				if (renderedFrames <= ultimo) return;
				const agora = Date.now();
				const d = (agora - tUlt) / Math.max(1, renderedFrames - ultimo);
				for (let k = ultimo; k < renderedFrames; k++) ms.push(Math.round(d));
				ultimo = renderedFrames;
				tUlt = agora;
				const p = Math.floor((renderedFrames / nQ) * 10);
				if (p > pct) {
					pct = p;
					console.log(`  ${renderedFrames}/${nQ} quadros · ${((agora - tRender0) / 1000).toFixed(0)} s`);
				}
			},
		});
		break;
	} catch (e) {
		const log = path.join(proj, '06_previas', `render_erro_${stamp}_${tentativa}.log`);
		fs.mkdirSync(path.dirname(log), {recursive: true});
		fs.writeFileSync(log, `${args.join(' ')}\n\n${e?.stack ?? e}`);
		console.error(`[vox] falhou (tentativa ${tentativa}); erro em ${CAM.mostrar(log)}${tentativa === 1 ? '. Tentando de novo…' : ''}`);
		if (tentativa === 2) process.exit(1);
	}
}
const tRender = (Date.now() - tRender0) / 1000;

// 2. áudio: trilha(s) e SFX na amostra exata (mixar-audio) ou, sem nada a misturar, só o loudnorm de 2 passadas
const saidas = [];
const mixar = (trilha, saida) => {
	const a = [path.join(MOTOR, 'scripts', 'mixar-audio.mjs'), proj, '--video', base, '--props', propsPath, '--saida', saida, ...(semTrilha || (!trilha && !props.musica) ? ['--trilha', 'nenhuma'] : trilha ? ['--trilha', trilha] : []), ...(trecho ? ['--desde', String(trecho[0])] : []), ...(previa ? [] : ['--final'])];
	const m = spawnSync(process.execPath, a, {cwd: MOTOR, stdio: 'inherit'});
	if (m.status !== 0) process.exit(m.status ?? 1);
	saidas.push(saida);
};
if (trilhas.length === 0) mixar(null, saidaFinal);
else for (const t of trilhas) mixar(t, trilhas.length > 1 ? saidaFinal.replace(/\.mp4$/, `_trilha-${t}.mp4`) : saidaFinal);
if (!args.includes('--manter-base')) fs.rmSync(base, {force: true});

// 3. relatório: total e, com concurrency 1, o custo de cada bloco (para achar o pior trecho)
const mb = saidas.map((s) => (fs.statSync(s).size / 1e6).toFixed(1)).join(' + ');
console.log(`[vox] ok: render ${tRender.toFixed(0)} s para ${dur.toFixed(1)} s = ${(tRender / dur).toFixed(1)} s por s de vídeo (+ bundle ${tBundle.toFixed(0)} s), total ${((Date.now() - t0) / 1000).toFixed(0)} s, ${mb} MB${args.includes('--manter-base') ? ` · base: ${CAM.mostrar(base)}` : ''}`);
if (conc === 1 && Array.isArray(props.blocos) && ms.length === nQ) {
	const ini = props.ini ?? 0;
	const linhas = [];
	for (const b of props.blocos) {
		const a = Math.max(f0, Math.round((b.ini - ini) * fps)), z = Math.min(f0 + nQ, Math.round((b.fim - ini) * fps));
		if (z <= a) continue;
		const fatia = ms.slice(a - f0, z - f0);
		const sps = fatia.reduce((x, y) => x + y, 0) / 1000 / (fatia.length / fps);
		linhas.push({layout: b.layout, sps});
		console.log(`  ${b.layout.padEnd(9)} ${b.ini.toFixed(2)}–${b.fim.toFixed(2)} s: ${sps.toFixed(1)} s/s (pior quadro ${(Math.max(...fatia) / 1000).toFixed(2)} s)`);
	}
	const pior = linhas.sort((x, y) => y.sps - x.sps)[0];
	if (pior) console.log(`[vox] pior bloco: ${pior.layout} (${pior.sps.toFixed(1)} s/s)`);
}
