// Prova que os formatos aprovados continuam iguais: renderiza trechos fixos de vídeos entregues e compara quadro a
// quadro com a referência gravada.
// Uso: node scripts/regressao.mjs            → INSTAGRAM - TELA DIVIDIDA clássico (arquivado, congelado): md5 de cada quadro decodificado
//      --cut                                 → INSTAGRAM - EDIÇÃO CUT DINÂMICO aprovado (SONO X IMUNIDADE, 0–5 s:
//                                              abertura com silhueta, recorte, cards e legenda cinética)
//      --mix                                 → YOUTUBE - MIX EDIT aprovado (SONO X EMAGRECIMENTO: 0–4 s = zoom com
//                                              chaves e "TÓXICA" atrás da pessoa; 727–731 s = gráfico em escala log com
//                                              o rodapé de fonte de 26 px)
//      --td2                                 → INSTAGRAM - TELA DIVIDIDA atual (piloto de 24/10, 03_roteiro/edicao_td2.json: 20–26 s =
//                                              trocas, flashes P&B e mesa girando; 79,5–83 s = vidro; 95,5–98,5 s = recortes voando)
//      --gravar                              → grava uma referência nova (só se a mudança for aprovada pelo usuário)
// Rode as três depois de qualquer mudança no motor (render.mjs, Root.tsx, MotorCamadas, peças, pacotes, fontes...).
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import * as CAM from './lib/caminhos.mjs';

const MOTOR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RAIZ = CAM.DADOS;
const cut = process.argv.includes('--cut');
const mix = process.argv.includes('--mix');
const td2 = process.argv.includes('--td2');
// ruido: o motor de camadas decodifica o vídeo da pessoa no navegador (GPU), então dois renders do MESMO código já
// diferem por ruído; a comparação é por PSNR em miniatura (escala), não por md5.
// Pilotos = vídeos SEUS já aprovados (configurados em %SOUTO_VIDEO_PROJETOS%/_sistema/regressao/pilotos.json).
const CFG = td2
	? CAM.piloto('td2', {proj: null, base: 'tela-dividida-2_base', trechos: [['0', '5']], nome: 'O TELA DIVIDIDA', escala: '135:240', limiar: 40})
	: mix
	? CAM.piloto('mix', {proj: null, base: 'mix-edit_base', trechos: [['0', '4']], nome: 'O YOUTUBE - MIX EDIT aprovado', escala: '240:135'})
	: cut
		? CAM.piloto('cut', {proj: null, base: 'cut-dinamico_base', trechos: [['0', '5']], nome: 'O CUT DINÂMICO aprovado', escala: '135:240'})
		: CAM.piloto('tela-dividida-classico', {proj: null, base: 'tela-dividida_base', trechos: [['0', '5']], nome: 'O Tela Dividida clássico', escala: null});
const PROJETOS = CAM.PROJETOS;
const PROJ = [path.join(PROJETOS, CFG.proj), ...fs.readdirSync(PROJETOS, {withFileTypes: true}).filter((d) => d.isDirectory()).map((d) => path.join(PROJETOS, d.name, CFG.proj))].find((p) => fs.existsSync(path.join(p, '03_roteiro', 'edicao.json')));
if (!PROJ) {
	console.error(`[regressão] não achei o piloto ${CFG.proj} em ${PROJETOS} nem nas subpastas`);
	process.exit(1);
}
const gravar = process.argv.includes('--gravar');

const quadros = (f) =>
	spawnSync('ffmpeg', ['-v', 'error', '-i', f, '-map', '0:v', '-f', 'framemd5', '-'], {encoding: 'utf8', maxBuffer: 64 * 1024 * 1024})
		.stdout.split('\n')
		.filter((l) => l && !l.startsWith('#'))
		.map((l) => l.split(',').pop().trim());

let falhou = false;
CFG.trechos.forEach((trecho, k) => {
	const BASE = path.join(CAM.REGRESSAO, `${CFG.base}${k ? `_${k + 1}` : ''}.mp4`);
	const rotulo = CFG.trechos.length > 1 ? ` (trecho ${trecho[0]}–${trecho[1]} s)` : '';
	const saida = gravar ? BASE : path.join(os.tmpdir(), `regressao_${process.pid}_${k}.mp4`);
	const r = spawnSync(process.execPath, ['scripts/render.mjs', PROJ, '--previa', '--trecho', ...trecho, '--saida', saida, ...(CFG.edicao ? ['--edicao', CFG.edicao] : [])], {cwd: MOTOR, stdio: 'inherit'});
	if (r.status !== 0) process.exit(r.status ?? 1);
	if (gravar) {
		console.log(`[regressão] referência gravada: ${CAM.mostrar(BASE)}`);
		return;
	}
	const a = quadros(BASE);
	const b = quadros(saida);
	const dif = a.filter((h, i) => h !== b[i]).length + Math.abs(a.length - b.length);
	if (dif === 0) {
		console.log(`[regressão] IDÊNTICO${rotulo}: ${a.length} quadros iguais à referência. ${CFG.nome} não mudou.`);
		fs.rmSync(saida, {force: true});
	} else if (CFG.escala) {
		// CUT: em resolução cheia o ruído dá PSNR mín. 38–41 dB; a 135×240 (área) ele some (≥ 45 dB) e o que é estrutural
		// fica: medido: contraste +1% → 42,5 dB; deslocamento de 4 px → 26 dB; card/texto/cor diferente → bem menos.
		// Limiar: 42 dB. O MIX usa a mesma conta na miniatura 16:9 (240×135).
		const stats = path.join(os.tmpdir(), `psnr_${process.pid}_${k}.txt`);
		spawnSync('ffmpeg', ['-v', 'error', '-i', saida, '-i', BASE, '-lavfi', `[0:v]scale=${CFG.escala}:flags=area[a];[1:v]scale=${CFG.escala}:flags=area[b];[a][b]psnr=stats_file=${path.basename(stats)}`, '-f', 'null', '-'], {cwd: os.tmpdir()});
		const v = fs.readFileSync(stats, 'utf8').trim().split('\n').map((l) => l.match(/psnr_avg:(\S+)/)?.[1]).map((x) => (x === 'inf' ? 99 : Number(x)));
		fs.rmSync(stats, {force: true});
		const min = Math.min(...v);
		const pior = v.indexOf(min) + 1;
		// TELA DIVIDIDA atual: 40 dB, como o PAPER VOX. Na conferência da referência (2026-10-27, mesmo código) o último
		// quadro do trecho 95,5–98,5 s deu 40,9 dB e os outros 71 ficaram ≥ 45 dB: ruído do vídeo decodificado no navegador.
		const limiar = CFG.limiar ?? 42;
		if (min >= limiar && a.length === b.length) {
			console.log(`[regressão] EQUIVALENTE${rotulo}: ${a.length} quadros, ${a.length - dif} idênticos e o resto só com ruído de decodificação (PSNR mín. ${min.toFixed(1)} dB ≥ ${limiar} a ${CFG.escala.replace(':', '×')}). ${CFG.nome} não mudou.`);
			fs.rmSync(saida, {force: true});
		} else {
			console.log(`[regressão] ATENÇÃO${rotulo}: mudança visual (PSNR mín. ${min.toFixed(1)} dB no quadro ${pior}). Render novo: ${saida}`);
			falhou = true;
		}
	} else {
		const psnr = spawnSync('ffmpeg', ['-v', 'info', '-i', saida, '-i', BASE, '-lavfi', 'psnr', '-f', 'null', '-'], {encoding: 'utf8'}).stderr.match(/average:(\S+)/)?.[1];
		console.log(`[regressão] ATENÇÃO: ${dif} de ${a.length} quadros diferentes (PSNR médio ${psnr} dB). Render novo: ${saida}`);
		falhou = true;
	}
});
if (falhou) process.exit(1);
