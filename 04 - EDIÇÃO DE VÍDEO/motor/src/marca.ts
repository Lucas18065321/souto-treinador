// Identidade visual do Jorge Souto (SOUTO TREINADOR) para todos os formatos de vídeo. UM lugar só:
//   - cores e degradês: ../../../marca/marca-souto.json (o mesmo arquivo das outras frentes: carrossel, documentos…)
//   - nome, cargo, @ e CREF: ../../marca-video.json (campos marcados TROCAR)
//   - logo: ../../../marca/logo/souto-logo-branco.png (PNG transparente)
// Mudou a cor da marca? Edite só o marca-souto.json; o motor inteiro acompanha no próximo render.
import souto from '../../../marca/marca-souto.json';
import video from '../../marca-video.json';
import logoBranco from '../../../marca/logo/souto-logo-branco.png';
import logoAzul from '../../../marca/logo/souto-logo-azul.png';

const C = souto.cores;
const V = souto.video;

// mistura de duas cores hex (0 = a, 1 = b): tons claros/escuros derivados das cores oficiais
export const misturar = (a: string, b: string, t: number): string => {
	const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
	const [x, y] = [p(a), p(b)];
	return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, '0')).join('').toUpperCase();
};
export const rgbaHex = (h: string, a: number): string => `rgba(${[1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)).join(', ')}, ${a})`;

const claro = misturar(V.dominante, C.branco, 0.45); // azul claro (realce sobre fundo escuro)
const clarissimo = misturar(V.dominante, C.branco, 0.7);

export const MARCA = {
	nome: video.nome,
	nomeLinhas: video.nomeLinhas as [string, string],
	marca: video.marca,
	cargo: video.cargo,
	arroba: video.arroba,
	registro: video.registro,
	redes: video.redes,
	logoBranco,
	logoAzul,
	// ---- cores (Paper Vox / VOX usam o par `video` do marca-souto.json) ----
	acento: V.dominante, // azul elétrico: destaque, cartões, objetos de marca
	acentoMedio: C.azul_royal,
	aco: C.azul_aco,
	acentoProfundo: C.azul_noite, // painéis e fundos de tela gráfica
	choque: V.choque, // névoa: 2ª cor de contraste
	creme: V.papel, // texto claro sobre fundo escuro
	papel: V.papel,
	papelEscuro: C.nevoa,
	tinta: V.tinta, // texto escuro / preto da marca
	preto: C.preto,
	grafite: C.grafite,
	claro,
	clarissimo,
	silhueta: C.azul_royal,
	brilhoSilhueta: [misturar(C.branco, V.dominante, 0.08), misturar(C.branco, V.dominante, 0.3)] as [string, string],
	// os 3 degradês das palavras-chave (antes: névoa→azul elétrico, claro→aço, royal→azul claro)
	degrades: {
		'nevoa-eletrico': `linear-gradient(100deg, ${clarissimo} 0%, ${claro} 52%, ${V.dominante} 100%)`,
		'claro-aco': `linear-gradient(100deg, ${C.nevoa} 0%, ${clarissimo} 45%, ${claro} 100%)`,
		'eletrico-aco': `linear-gradient(100deg, ${C.azul_royal} 0%, ${V.dominante} 55%, ${claro} 100%)`,
	},
	degradesVerticais: [
		`linear-gradient(0deg, ${V.dominante} 0%, ${claro} 55%, ${clarissimo} 100%)`,
		`linear-gradient(0deg, ${C.azul_aco} 0%, ${claro} 55%, ${C.nevoa} 100%)`,
	],
};
export type DegradeMarca = keyof typeof MARCA.degrades;
