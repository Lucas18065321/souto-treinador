// Prova que o INSTAGRAM - VOX - B-ROLLs aprovado continua igual: renderiza trechos fixos do piloto ("creatina sem
// treino", %SOUTO_VIDEO_PROJETOS%/2026-10-28_creatina-sem-treino, aprovado em 2026-10-30) pelo render-vox.mjs, em resolução cheia e
// sem trilha, e compara quadro a quadro com a referência em %SOUTO_VIDEO_PROJETOS%/_sistema/regressao/vox_base[_k].mp4: trechos do FINAL
// aprovado (07_final/), cortados por número de quadro com --gravar. Script próprio: o render e o áudio do VOX não passam
// pelo render.mjs dos outros. Trechos: 0–3 s (abertura: texto digitado, cartão azul da marca, papel que invade e a 1ª montagem),
// 10,4–12,4 s (invasão → split: o painel sobe com a emenda esfumada e o 1º chicote no painel) e 29,9–31,9 s (último
// mergulho do mural → moldura: cabeça recortada vazando, fundo desfocado e o card que cai).
// Compara só o vídeo, por PSNR na miniatura 135×240 (EQUIVALENTE ≥ 45 dB): a referência é um corte reencodado do final,
// então o md5 de quadro nunca bate (o IDÊNTICO do regressao-paper-vox.mjs não existe aqui).
// Calibração: ver LIMIAR, abaixo.
// Uso (de dentro do motor, pela fila): node scripts/vez.mjs node scripts/regressao-vox.mjs [--gravar | --gravar-render]
//   [--props <arquivo>] [--trechos 1,2,3]
//   --gravar → corta a referência do final aprovado (só com ok do dono do canal). --gravar-render → grava a referência a partir de
//   um render do código atual: só quando o dono do canal aprovar uma mudança visual no formato (o final do piloto não muda mais).
//   --props → renderiza com outro props (calibração com mudança proposital); --trechos → só os trechos indicados.
// Rode junto com as outras 5 depois de qualquer mudança em src/modelos/vox/, src/kit/, src/legendas.ts, Root.tsx,
// scripts/render-vox.mjs ou pacotes (o áudio não entra na conta: só o vídeo se compara).
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import * as CAM from './lib/caminhos.mjs';

const MOTOR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RAIZ = CAM.DADOS;
const CFG = CAM.piloto('vox', {proj: null, base: 'vox_base', trechos: [['0', '3']], nome: 'O VOX - B-ROLLs aprovado', escala: '135:240', fps: 24});
// LIMIAR (calibrado em 2026-10-30, trecho 10,4–12,4 s): render novo × final aprovado = só ruído de render e de 2 encodes,
// PSNR mín. 49,7–50,3 dB nos 3 trechos. Mudança pequena de propósito: foto de 260 px deslocada 2 px = 36,9 dB; texto de
// uma etiqueta (~440×50 px) de tinta para azul da marca = 40,7 dB, que o limiar 40 do PAPER VOX deixaria passar. Limiar: 45.
const LIMIAR = 45;
const PROJ = path.join(CAM.PROJETOS, CFG.proj);
const FINAL = path.join(PROJ, '07_final', `${CFG.proj}_final.mp4`);
const args = process.argv.slice(2);
const gravar = args.includes('--gravar'), gravarRender = args.includes('--gravar-render');
const props = args.includes('--props') ? path.resolve(args[args.indexOf('--props') + 1]) : null;
const so = args.includes('--trechos') ? args[args.indexOf('--trechos') + 1].split(',').map(Number) : null;

// referência: o trecho do final pelo número do quadro (o mesmo arredondamento do frameRange do render-vox.mjs), em 540×960
const cortar = (a, b, saida) => {
	const q0 = Math.round(Number(a) * CFG.fps), q1 = Math.round(Number(b) * CFG.fps) - 1;
	const r = spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', FINAL, '-map', '0:v:0', '-an', '-vf', `select='between(n,${q0},${q1})',setpts=N/FRAME_RATE/TB,scale=540:960:flags=area`, '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', String(CFG.fps), saida], {encoding: 'utf8'});
	if (r.status !== 0) throw new Error(`[regressão] ffmpeg não cortou o final: ${r.stderr}`);
};
const nQuadros = (f) => parseInt(spawnSync('ffprobe', ['-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', f], {encoding: 'utf8'}).stdout, 10);

let falhou = false;
CFG.trechos.forEach((trecho, k) => {
	if (so && !so.includes(k + 1)) return;
	const BASE = path.join(CAM.REGRESSAO, `${CFG.base}${k ? `_${k + 1}` : ''}.mp4`);
	const rotulo = ` (trecho ${trecho[0]}–${trecho[1]} s)`;
	if (gravar) {
		cortar(trecho[0], trecho[1], BASE);
		console.log(`[regressão] referência gravada do final aprovado: ${CAM.mostrar(BASE)} (${nQuadros(BASE)} quadros)`);
		return;
	}
	const saida = gravarRender ? BASE : path.join(os.tmpdir(), `regressao_vox_${process.pid}_${k}.mp4`);
	const r = spawnSync(process.execPath, ['scripts/render-vox.mjs', PROJ, '--trecho', ...trecho, '--sem-trilha', '--saida', saida, ...(props ? ['--props', props] : [])], {cwd: MOTOR, stdio: ['inherit', 'ignore', 'inherit']});
	if (r.status !== 0) process.exit(r.status ?? 1);
	if (gravarRender) {
		console.log(`[regressão] referência gravada do render atual: ${CAM.mostrar(BASE)}`);
		return;
	}
	if (!fs.existsSync(BASE)) {
		console.log(`[regressão] sem referência ${CAM.mostrar(BASE)}: grave com --gravar (com ok do dono do canal)`);
		falhou = true;
		return;
	}
	const na = nQuadros(BASE), nb = nQuadros(saida);
	const stats = path.join(os.tmpdir(), `psnr_vox_${process.pid}_${k}.txt`);
	spawnSync('ffmpeg', ['-v', 'error', '-i', saida, '-i', BASE, '-lavfi', `[0:v]scale=${CFG.escala}:flags=area[a];[1:v]scale=${CFG.escala}:flags=area[b];[a][b]psnr=stats_file=${path.basename(stats)}`, '-f', 'null', '-'], {cwd: os.tmpdir()});
	const v = fs.readFileSync(stats, 'utf8').trim().split('\n').map((l) => l.match(/psnr_avg:(\S+)/)?.[1]).map((x) => (x === 'inf' ? 99 : Number(x)));
	fs.rmSync(stats, {force: true});
	const min = Math.min(...v), media = v.reduce((s, x) => s + x, 0) / v.length;
	if (min >= LIMIAR && na === nb) {
		console.log(`[regressão] EQUIVALENTE${rotulo}: ${na} quadros, só ruído (PSNR mín. ${min.toFixed(1)} dB, média ${media.toFixed(1)}, ≥ ${LIMIAR} a 135×240). ${CFG.nome} não mudou.`);
		fs.rmSync(saida, {force: true});
	} else {
		console.log(`[regressão] ATENÇÃO${rotulo}: mudança visual (PSNR mín. ${min.toFixed(1)} dB no quadro ${v.indexOf(min) + 1}, média ${media.toFixed(1)}; ${na} × ${nb} quadros). Render novo: ${saida}`);
		falhou = true;
	}
});
if (falhou) process.exit(1);
