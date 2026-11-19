// Cria um projeto novo a partir do modelo e (opcionalmente) copia o bruto para 01_bruto/bruto.<ext>.
// Uso: node scripts/novo-projeto.mjs "<nome do vídeo>" [caminho-do-bruto]
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import * as CAM from './lib/caminhos.mjs';

// Estrutura de cada projeto (criada na hora; os projetos ficam em SOUTO_VIDEO_PROJETOS, fora do repositório)
const PASTAS = ['01_bruto', '02_analise', '03_roteiro', '04_broll/meus', '04_broll/banco', '04_broll/fotos', '04_broll/internet', '04_broll/ia_flow', '04_broll/recortes', '05_audio/musica', '05_audio/sfx', '06_previas', '07_final'];
const modeloProjeto = () => {
	const m = path.join(CAM.PROJETOS, '_MODELO_PROJETO');
	for (const p of PASTAS) fs.mkdirSync(path.join(m, p), {recursive: true});
	return m;
};

const [nome, bruto] = process.argv.slice(2);
if (!nome) {
	console.error('Uso: node scripts/novo-projeto.mjs "<nome do vídeo>" [caminho-do-bruto]');
	process.exit(1);
}
const slug = nome
	.normalize('NFD')
	.replace(/[̀-ͯ]/g, '')
	.toLowerCase()
	.replace(/[^a-z0-9]+/g, '-')
	.replace(/^-|-$/g, '');
const data = new Date().toLocaleDateString('sv-SE'); // AAAA-MM-DD no fuso local (toISOString virava o dia após as 21h)
const dest = path.join(CAM.PROJETOS, `${data}_${slug}`);
if (fs.existsSync(dest)) {
	console.error(`Já existe: ${dest}`);
	process.exit(1);
}
fs.cpSync(modeloProjeto(), dest, {recursive: true});
if (bruto) {
	const ext = path.extname(bruto).toLowerCase() || '.mp4';
	fs.copyFileSync(bruto, path.join(dest, '01_bruto', `bruto${ext}`));
}
console.log(dest);
