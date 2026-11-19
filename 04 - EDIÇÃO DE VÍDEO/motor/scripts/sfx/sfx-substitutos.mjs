// Monta a pasta de compatibilidade sfx/biblioteca/motionix/ com sons LIVRES (CC0 do Glitch Noises + sintetizados
// pelo próprio motor), com os MESMOS nomes que as peças do motor esperam (lista em sfx/biblioteca/motionix-nomes.tsv).
//
// Por quê: o motor original foi calibrado com o pacote "Motionix" (77 SFX). Esse pacote NÃO tem licença de
// redistribuição registrada, então não vai no repositório público. Sem esses arquivos, as peças (cards, gráficos,
// transições…) não teriam som e o validador acusaria "arquivo não existe". Este script preenche cada nome com o som
// livre mais parecido da mesma família (whoosh → whoosh, clique → clique…), cortado na duração do original e em
// 48 kHz estéreo 16 bits.
//
// Uso (de dentro de motor/):  node scripts/sfx/sfx-substitutos.mjs [--forcar]
//   sem --forcar, não sobrescreve arquivos que já existem (se você tiver o pacote original licenciado e colocar os
//   arquivos dele na pasta, eles ficam).
// A pasta sfx/biblioteca/motionix/ está no .gitignore (é gerada na instalação).
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import * as CAM from '../lib/caminhos.mjs';

const forcar = process.argv.includes('--forcar');
const LISTA = path.join(CAM.SFX_BIB, 'motionix-nomes.tsv');
const DEST = path.join(CAM.SFX_BIB, 'motionix');
const lab = (cat, filtro = () => true) => {
	const d = path.join(CAM.SFX_LAB, cat);
	return fs.existsSync(d) ? fs.readdirSync(d).filter((f) => f.endsWith('.wav') && filtro(f)).sort().map((f) => path.join(d, f)) : [];
};
const bib = (...nomes) => nomes.map((n) => path.join(CAM.SFX_BIB, `${n}.wav`)).filter((f) => fs.existsSync(f));

// família do Motionix → sons livres parecidos (em rodízio)
const FONTES = {
	whooshes: [...bib('whoosh_soft', 'whoosh_fast', 'swish_air'), ...lab('whoosh'), ...lab('glitch', (f) => f.includes('transicao'))],
	clicks: [...bib('click_soft', 'tick_micro'), ...lab('clique')],
	pop: [...bib('pop_soft'), ...lab('clique', (f) => f.includes('selecionar')), ...lab('ding')],
	'ui-sound-effects': [...lab('scroll-ui'), ...lab('futurista', (f) => /bip-(mini|clique)/.test(f)), ...lab('ding'), ...bib('shimmer')],
	'data-collect': [...lab('futurista', (f) => /processado|telemetria/.test(f)), ...lab('glitch', (f) => f.includes('data-riser'))],
	'camera-shutters': [...lab('clique'), ...lab('glitch', (f) => f.includes('estalo'))],
	gear: [...lab('futurista', (f) => /bip-clique|bip-0/.test(f)), ...lab('clique')],
	money: [...lab('ding'), ...bib('shimmer')],
	risers: [...bib('riser_short', 'reverse_swell'), ...lab('glitch', (f) => f.includes('data-riser')), ...lab('whoosh')],
};

if (!fs.existsSync(LISTA)) {
	console.error(`[substitutos] falta ${LISTA}`);
	process.exit(1);
}
const linhas = fs.readFileSync(LISTA, 'utf8').split(/\r?\n/).filter(Boolean).map((l) => l.split('\t'));
const giro = {};
let feitos = 0, mantidos = 0;
const registro = [];
for (const [nome, durTxt] of linhas) {
	const [familia] = nome.split('/');
	const fontes = FONTES[familia] ?? [];
	if (!fontes.length) {
		console.error(`[substitutos] sem fonte livre para a família ${familia} (confira sfx/lab e sfx/biblioteca)`);
		process.exit(1);
	}
	const saida = path.join(DEST, `${nome}.wav`);
	if (fs.existsSync(saida) && !forcar) {
		mantidos++;
		continue;
	}
	fs.mkdirSync(path.dirname(saida), {recursive: true});
	const i = (giro[familia] = (giro[familia] ?? -1) + 1);
	const fonte = fontes[i % fontes.length];
	// mesma duração do original (mín. 0,15 s, máx. 2,4 s: o Tela Dividida corta SFX em 2,5 s), com fade de 40 ms no fim
	const dur = Math.min(2.4, Math.max(0.15, Number(durTxt) || 1));
	const fadeIni = Math.max(0, dur - 0.04).toFixed(3);
	const r = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', fonte, '-t', String(dur), '-af', `aresample=48000,afade=t=out:st=${fadeIni}:d=0.04`, '-ac', '2', '-c:a', 'pcm_s16le', '-map_metadata', '-1', saida], {encoding: 'utf8'});
	if (r.status !== 0) {
		console.error(`[substitutos] ffmpeg falhou em ${nome}: ${r.stderr || r.error}`);
		process.exit(1);
	}
	registro.push(`${nome}\t${path.relative(CAM.RAIZ, fonte).replace(/\\/g, '/')}`);
	feitos++;
}
if (registro.length) fs.writeFileSync(path.join(DEST, 'ORIGEM.tsv'), 'nome\tfonte livre usada (CC0 ou sintetizado)\n' + registro.join('\n') + '\n');
console.log(`[substitutos] ${feitos} criados, ${mantidos} já existiam → ${DEST}`);
