// Mapa de pastas do motor (um lugar só). Tudo o que é LEVE (código, guias, SFX livres, kit) fica no repositório;
// tudo o que é PESADO ou PESSOAL (projetos, brutos, renders, B-roll, músicas, modelos do Whisper, referências da
// regressão) fica FORA do repositório e do OneDrive, na pasta da variável SOUTO_VIDEO_PROJETOS
// (padrão: %USERPROFILE%\Videos\Souto-Projetos).
//
//   <repo>/04 - EDIÇÃO DE VÍDEO/                    = RAIZ
//     motor/                                         = MOTOR (Remotion + scripts)
//     referencias/modelos/<id>/guia-de-estilo.md     = guias dos 5 formatos
//     sfx/biblioteca/                                = SFX sintetizados (+ motionix/ gerado na instalação)
//     sfx/lab/<categoria>/                           = SFX catalogados (Glitch Noises CC0 + os que você baixar)
//     kit/KIT.md                                     = catálogo das peças de motion
//     ferramentas/                                   = dicionário pt-BR + glossário
//   %SOUTO_VIDEO_PROJETOS%/                          = DADOS
//     <AAAA-MM-DD>_<nome>/01_bruto … 07_final        = um projeto por vídeo
//     _MODELO_PROJETO/                               = criado sozinho
//     _biblioteca/{broll-reutilizavel,musicas,catalogo.json}
//     _sistema/{modelos,ferramentas,regressao,render-partes,.fila-render}
//
// Carrega também as chaves do .env (na raiz do repositório, em 04 - EDIÇÃO DE VÍDEO/ ou em motor/), sem sobrescrever
// o que já estiver no ambiente.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export const MOTOR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
export const RAIZ = path.resolve(MOTOR, '..');
export const REPO = path.resolve(RAIZ, '..');

// ---------- .env ----------
export function lerEnv(arquivo) {
	if (!fs.existsSync(arquivo)) return {};
	return Object.fromEntries(
		fs
			.readFileSync(arquivo, 'utf8')
			.split(/\r?\n/)
			.filter((l) => /^\s*[A-Z0-9_]+\s*=/.test(l))
			.map((l) => [l.split('=')[0].trim(), l.slice(l.indexOf('=') + 1).trim().replace(/^["']|["']$/g, '')])
			.filter(([, v]) => v !== ''),
	);
}
for (const f of [path.join(MOTOR, '.env'), path.join(RAIZ, '.env'), path.join(REPO, '.env')]) {
	for (const [k, v] of Object.entries(lerEnv(f))) if (process.env[k] === undefined || process.env[k] === '') process.env[k] = v;
}
export const env = process.env;

// ---------- pastas ----------
const expandir = (p) => p.replace(/%([^%]+)%/g, (_, n) => process.env[n] ?? `%${n}%`).replace(/^~(?=$|[\\/])/, os.homedir());
export const DADOS = path.resolve(expandir(process.env.SOUTO_VIDEO_PROJETOS || path.join(os.homedir(), 'Videos', 'Souto-Projetos')));
export const PROJETOS = DADOS;
export const SISTEMA = path.join(DADOS, '_sistema');
export const MODELOS_WHISPER = path.join(SISTEMA, 'modelos');
export const FERRAMENTAS_BAIXADAS = path.join(SISTEMA, 'ferramentas');
export const REGRESSAO = path.join(SISTEMA, 'regressao');
export const RENDER_PARTES = path.join(SISTEMA, 'render-partes');
export const FILA = path.join(SISTEMA, '.fila-render');
export const BIBLIOTECA = path.join(DADOS, '_biblioteca');
export const BROLL = path.join(BIBLIOTECA, 'broll-reutilizavel');
export const CATALOGO = path.join(BIBLIOTECA, 'catalogo.json');
export const MUSICAS = path.join(BIBLIOTECA, 'musicas');
export const SFX_BIB = path.join(RAIZ, 'sfx', 'biblioteca');
export const SFX_LAB = path.join(RAIZ, 'sfx', 'lab');
export const REFERENCIAS = path.join(RAIZ, 'referencias', 'modelos');
export const KIT = path.join(RAIZ, 'kit');
export const FERRAMENTAS = path.join(RAIZ, 'ferramentas');
export const GLOSSARIO = path.join(FERRAMENTAS, 'glossario.txt');
export const MARCA = path.join(MOTOR, 'src', 'marca.json');

// Modelos do Whisper (baixados pelo instalar.ps1; ficam fora do repositório)
export const WHISPER_SMALL = path.join(MODELOS_WHISPER, 'ggml-small.bin');
export const WHISPER_TURBO = path.join(MODELOS_WHISPER, 'ggml-large-v3-turbo-q5_0.bin');

// "@biblioteca/musicas/x.mp3" (gravado nos props do PAPER VOX/VOX) → caminho real
export const resolverBiblioteca = (src) => (src.startsWith('@biblioteca/') ? path.join(BIBLIOTECA, src.slice(12)) : null);

// ---------- pilotos da regressão ----------
// Cada pessoa tem os SEUS pilotos (os vídeos aprovados que viram referência). Ficam em
// %SOUTO_VIDEO_PROJETOS%/_sistema/regressao/pilotos.json (modelo: motor/regressao.pilotos.exemplo.json).
export function piloto(chave, padrao) {
	const arq = path.join(REGRESSAO, 'pilotos.json');
	const cfg = fs.existsSync(arq) ? JSON.parse(fs.readFileSync(arq, 'utf8')) : {};
	const c = {...padrao, ...(cfg[chave] ?? {})};
	if (!c.proj) {
		console.error(
			`[regressão] piloto "${chave}" não configurado.\n` +
				`  1) Escolha um vídeo SEU já aprovado neste formato (pasta em ${PROJETOS}).\n` +
				`  2) Copie motor/regressao.pilotos.exemplo.json para ${arq} e preencha "proj" e "trechos".\n` +
				`  3) Grave a referência uma vez com --gravar. Passo a passo: docs/guias/04-video.md, seção "Regressão".`,
		);
		process.exit(2);
	}
	fs.mkdirSync(REGRESSAO, {recursive: true});
	return c;
}

// caminho curto para mensagens: relativo à pasta de projetos ou ao motor de vídeo, senão o completo
export const mostrar = (p) => {
	for (const base of [DADOS, RAIZ]) {
		const r = path.relative(base, p);
		if (r && !r.startsWith('..') && !path.isAbsolute(r)) return r;
	}
	return p;
};
export const garantirPasta = (p) => (fs.mkdirSync(p, {recursive: true}), p);
