// Prova que o INSTAGRAM - PAPER VOX ANIMATION aprovado continua igual: renderiza trechos fixos do piloto ("sociedade
// que adoece", %SOUTO_VIDEO_PROJETOS%/2026-10-19_sociedade-que-adoece, aprovado em 2026-10-20) e compara quadro a quadro com a
// referência em %SOUTO_VIDEO_PROJETOS%/_sistema/regressao/paper-vox_base[_k].mp4. Script próprio: o render e o áudio do Paper Vox não passam pelo render.mjs
// dos outros 3. Trechos: 0–4 s (abertura: foto que voa, papéis, texto, "vergonha" com slam e marca azul da marca), 15–16,6 s
// (montagem M1: mergulho, planos de 0,2 s, emergência) e 48,6–50 s (chicote com motion blur + a mão que voa e boia).
// Compara só o vídeo: md5 de cada quadro (IDÊNTICO) e, se mudar, PSNR na miniatura 135×240 (EQUIVALENTE ≥ 40 dB).
// Calibração (2026-10-20): dois renders do MESMO código nunca saem com md5 igual (composição da GPU e da trama do
// halftone); esse ruído dá PSNR mín. ≥ 42 dB (medido 42,2–47,8) depois que as texturas passaram a segurar o quadro até decodificar (antes,
// 41). Mudança real pequena: palavra 30×15 px trocada de cor = 38,6 dB; deslocar 2 px = 25 dB. Limiar: 40 dB.
// Uso (de dentro do motor, pela fila): node scripts/vez.mjs node scripts/regressao-paper-vox.mjs [--gravar]
//   --gravar → grava a referência nova (só se a mudança for aprovada pelo dono do canal).
// Rode junto com as 3 do regressao.mjs depois de qualquer mudança em src/modelos/paper-vox/, src/kit/, Root.tsx,
// scripts/render-paper-vox.mjs, scripts/lib/mural.mjs ou pacotes.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import * as CAM from './lib/caminhos.mjs';

const MOTOR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RAIZ = CAM.DADOS;
const CFG = CAM.piloto('paper-vox', {proj: null, base: 'paper-vox_base', trechos: [['0', '4']], nome: 'O PAPER VOX ANIMATION aprovado', escala: '135:240'});
const PROJ = path.join(CAM.PROJETOS, CFG.proj);
const gravar = process.argv.includes('--gravar');

const quadros = (f) =>
	spawnSync('ffmpeg', ['-v', 'error', '-i', f, '-map', '0:v', '-f', 'framemd5', '-'], {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024})
		.stdout.split('\n')
		.filter((l) => l && !l.startsWith('#'))
		.map((l) => l.split(',').pop().trim());

let falhou = false;
CFG.trechos.forEach((trecho, k) => {
	const BASE = path.join(CAM.REGRESSAO, `${CFG.base}${k ? `_${k + 1}` : ''}.mp4`);
	const rotulo = ` (trecho ${trecho[0]}–${trecho[1]} s)`;
	const saida = gravar ? BASE : path.join(os.tmpdir(), `regressao_pv_${process.pid}_${k}.mp4`);
	const r = spawnSync(process.execPath, ['scripts/render-paper-vox.mjs', PROJ, '--previa', '--trecho', ...trecho, '--sem-trilha', '--saida', saida], {cwd: MOTOR, stdio: ['inherit', 'ignore', 'inherit']});
	if (r.status !== 0) process.exit(r.status ?? 1);
	if (gravar) {
		console.log(`[regressão] referência gravada: ${CAM.mostrar(BASE)}`);
		return;
	}
	if (!fs.existsSync(BASE)) {
		console.log(`[regressão] sem referência ${CAM.mostrar(BASE)}: grave com --gravar (com ok do dono do canal)`);
		falhou = true;
		return;
	}
	const a = quadros(BASE);
	const b = quadros(saida);
	const dif = a.filter((h, i) => h !== b[i]).length + Math.abs(a.length - b.length);
	if (dif === 0) {
		console.log(`[regressão] IDÊNTICO${rotulo}: ${a.length} quadros iguais à referência. ${CFG.nome} não mudou.`);
		fs.rmSync(saida, {force: true});
		return;
	}
	const stats = path.join(os.tmpdir(), `psnr_pv_${process.pid}_${k}.txt`);
	spawnSync('ffmpeg', ['-v', 'error', '-i', saida, '-i', BASE, '-lavfi', `[0:v]scale=${CFG.escala}:flags=area[a];[1:v]scale=${CFG.escala}:flags=area[b];[a][b]psnr=stats_file=${path.basename(stats)}`, '-f', 'null', '-'], {cwd: os.tmpdir()});
	const v = fs.readFileSync(stats, 'utf8').trim().split('\n').map((l) => l.match(/psnr_avg:(\S+)/)?.[1]).map((x) => (x === 'inf' ? 99 : Number(x)));
	fs.rmSync(stats, {force: true});
	const min = Math.min(...v);
	if (min >= 40 && a.length === b.length) {
		console.log(`[regressão] EQUIVALENTE${rotulo}: ${a.length} quadros, ${a.length - dif} idênticos e o resto só com ruído (PSNR mín. ${min.toFixed(1)} dB ≥ 40 a 135×240). ${CFG.nome} não mudou.`);
		fs.rmSync(saida, {force: true});
	} else {
		console.log(`[regressão] ATENÇÃO${rotulo}: mudança visual (PSNR mín. ${min.toFixed(1)} dB no quadro ${v.indexOf(min) + 1}; ${a.length} × ${b.length} quadros). Render novo: ${saida}`);
		falhou = true;
	}
});
if (falhou) process.exit(1);
