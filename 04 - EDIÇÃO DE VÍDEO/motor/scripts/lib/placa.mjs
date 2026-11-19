// Leitura de vídeo pela placa de vídeo Intel (Quick Sync, QSV), usada só quando sai idêntica à da CPU.
// Medido em 27/10/2026 (i5-1235U, Intel UHD, FFmpeg 9.0.2) em 3 brutos: câmera HEVC 4K 10 bits 4:2:2 deitado, celular
// H.264 1440×2560 e HEVC 10 bits 1080×1920. Com a volta ao formato de pixel da CPU e o giro explícito, os quadros saem
// com o mesmo md5 da leitura na CPU, e o preparar.mjs inteiro (com o x264) caiu de 34,6 s para 25,3 s em 4 s de 4K.
// O giro gravado pelo celular/câmera sai do automático do FFmpeg (que converteria o formato da placa por outro caminho
// e daria quadros diferentes) e vira filtro: -display_rotation 0 zera a marcação, que senão iria para a saída já girada.
import {spawnSync} from 'node:child_process';

const DECODIFICADOR = {h264: 'h264_qsv', hevc: 'hevc_qsv', av1: 'av1_qsv', vp9: 'vp9_qsv'};
const GIRO = {0: '', 90: 'transpose=clock', 180: 'hflip,vflip', 270: 'transpose=cclock'}; // mesmo do autorotate

// → {dec, entrada, filtro} para pôr antes do -i e no começo da cadeia de vídeo, ou null (lê na CPU).
// vf = a cadeia de vídeo do script; a conferência compara os primeiros quadros já filtrados nas duas leituras.
export const leituraPlaca = (src, vf = 'null', quadros = 12) => {
	const s = JSON.parse(spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,pix_fmt:stream_side_data=rotation', '-of', 'json', src], {encoding: 'utf8'}).stdout || '{}').streams?.[0];
	const dec = DECODIFICADOR[s?.codec_name];
	if (!dec || !s.pix_fmt) return null;
	const theta = Math.round(((-Number(s.side_data_list?.find((d) => d.rotation != null)?.rotation ?? 0) % 360) + 360) % 360);
	if (GIRO[theta] == null) return null;
	const entrada = ['-display_rotation', '0', '-c:v', dec, '-gpu_copy', 'on'];
	const filtro = [`format=${s.pix_fmt}`, GIRO[theta]].filter(Boolean).join(',');
	const md5 = (pre, cadeia) => (spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', ...pre, '-i', src, '-an', '-vf', cadeia, '-frames:v', String(quadros), '-f', 'framemd5', '-'], {encoding: 'utf8', maxBuffer: 1 << 24}).stdout ?? '')
		.split(/\r?\n/).filter((l) => l && !l.startsWith('#')).map((l) => l.split(',').pop().trim());
	const cpu = md5([], vf), placa = md5(entrada, `${filtro},${vf}`);
	return cpu.length && cpu.join() === placa.join() ? {dec, entrada, filtro} : null;
};
