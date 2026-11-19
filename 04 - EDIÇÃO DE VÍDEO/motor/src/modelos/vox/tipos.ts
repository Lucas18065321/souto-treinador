// Tipos do INSTAGRAM - VOX - B-ROLLs (vox-broll-instagram, composição VoxBroll; guia referencias/modelos/vox-broll-instagram/
// guia-de-estilo.md). Ficam no módulo, não no src/tipos.ts (como os do PAPER VOX).
// Base: os tipos do PAPER VOX (src/modelos/paper-vox/tipos.ts, copiados e adaptados: entradas sem overshoot, palcos em
// retângulo, foco por grupo) + os layouts da espinha do dono do canal. Props = 03_roteiro/vox.json (nunca edicao.json).
// Tempos em segundos da SAÍDA; sem montagem, saída = bruto (a partir de `ini`). Palco = mundo com câmera própria.
import type {Palavra} from '../../tipos';

export type CurvaVox = 'suave' | 'entrada' | 'saida' | 'linear' | 'expo' | 'assento' | 'chicote' | 'cubica' | 's';

// Chave de câmera do palco: no instante t a câmera mira (x, y) do mundo com esse zoom. Sem o `snap` do PAPER VOX
// (passava ~6,6% do alvo): toda curva aqui chega sem overshoot (o validar-vox confere).
export type ChaveCamera = {t: number; x: number; y: number; zoom: number; rot?: number; curva?: CurvaVox; arco?: number};

export type Plano = 'fundo' | 'meio' | 'frente';
export type Lado = 'esq' | 'dir' | 'baixo' | 'cima' | 'ne' | 'no' | 'se' | 'so';

// Entradas (guia, "Especificação de movimento"): voa 0,30 s em arco; monta = voa e trava em S (~0,5 s); borda = sobe
// da borda (0,23–0,33 s); carimbo = 1 passo a 2,2× e depois 1×; cai = cartão que cai 655 px em 1,63 s (−6° → 0°).
export type Entrada = {tipo: 'voa' | 'monta' | 'borda' | 'carimbo' | 'pousa' | 'escala' | 'surge' | 'cai' | 'nenhuma'; dur?: number; de?: Lado; dist?: number};
// Saídas: some = dissolve + desfoque (0,13–0,20 s); desmonta = volta pela borda em ease-in, 2× mais rápido; corte = some seco.
export type Saida = {tipo: 'some' | 'desmonta' | 'corte'; dur?: number};

type Base = {
	id: string;
	x: number; // centro, no mundo do palco
	y: number;
	w: number;
	h?: number;
	rot?: number;
	plano?: Plano;
	ini: number;
	fim?: number;
	entra?: Entrada;
	sai?: Saida;
	passo?: 1 | 2 | 3; // 1 = 24 fps; 2 = 12 fps (colagem, padrão das peças); 3 = 8 fps (traço à mão)
	boia?: number; // deriva depois de entrar (0 = parado; 1 = ±7 px, ±1,1°)
	grupo?: string; // foco por grupo (resquício do mural)
	pendulo?: {amp?: number; periodo?: number; amort?: number; pivo?: [number, number]}; // laço: 22°·sen(2πt/P)·e^(−a·t)
};

export type Elemento =
	| (Base & {tipo: 'cenario'; src: string; srcDesfocado?: string})
	| (Base & {tipo: 'foto'; src: string; srcDesfocado?: string; borda?: number; semente?: number; zoomInterno?: [number, number]})
	| (Base & {tipo: 'recorte'; src: string; srcDesfocado?: string; sombra?: boolean})
	| (Base & {tipo: 'papel'; cor?: string; semente?: number; rasgado?: boolean})
	| (Base & {tipo: 'etiqueta'; texto: string; t?: number; cor?: string; tinta?: string; tamanho?: number; fonte?: 'inter' | 'anton' | 'serifa'; semente?: number})
	| (Base & {tipo: 'texto'; palavras: {t: number; w: string}[]; tamanho: number; fonte?: 'anton' | 'inter' | 'serifa' | 'serifaReta'; cor?: string; degrade?: Degrade; modo?: 'pedaco' | 'digita' | 'carimbo'; alinhar?: 'left' | 'center' | 'right'})
	| (Base & {tipo: 'numero'; valor: number; t: number; dur?: number; prefixo?: string; sufixo?: string; tamanho: number; cor?: string; degrade?: Degrade})
	| (Base & {tipo: 'traco'; d: string; vb: [number, number]; cor?: string; espessura?: number; dur?: number; ponta?: boolean})
	| (Base & {tipo: 'brilho'; cor?: string})
	| (Base & {tipo: 'fita'; semente?: number})
	| (Base & {tipo: 'luz'; cor?: string; forca?: number})
	| (Base & {tipo: 'card'; texto: string; tamanho?: number; prendedores?: boolean; cor?: string; tinta?: string; semente?: number})
	| (Base & {tipo: 'objeto'; nome: string; ev?: Record<string, number>; p?: Record<string, unknown>});

export type Degrade = 'nevoa-eletrico' | 'claro-aco' | 'eletrico-aco';

// Foco por grupo (Resquicio, versão barata do guia): em t o grupo sai de foco em `dur` s: escurece (0,2–0,3) e as fotos
// trocam, por opacidade, para a cópia pré-desfocada (srcDesfocado, feita 1 vez no ffmpeg).
export type FocoVox = {t: number; grupo: string; dur?: number; escurece?: number};
// Véu: o fundo escurece (−50% em 0,4 s) para o número ou rótulo entrar (ref-08 mov §2); fica entre o plano do meio e o da frente.
export type VeuVox = {t: number; fim?: number; v?: number; dur?: number};

export type PalcoVox = {
	camera: ChaveCamera[];
	elementos: Elemento[];
	focos?: FocoVox[];
	veus?: VeuVox[];
	viva?: number; // câmera viva (px de tela)
	fundo?: string; // cor atrás de tudo
	vinheta?: number;
	grao?: number;
	blur?: {ativo: boolean; limiar?: number; maxAmostras?: number; obturador?: number; espaco?: number};
};

export type TrocaPainel = 'chicote' | 'mascara' | 'zoom' | 'blur' | 'corte';

export type AberturaVox = {
	linhas: {w: string; t: number}[][]; // texto digitado: linhas de palavras com o instante falado
	texto: {x: number; y: number; tamanho?: number}; // canto de cima-esquerda do bloco de texto (px da tela)
	cartao: {palavra: string; t: number; x: number; y: number; w: number; h: number; rot?: number};
	sai: number; // texto e cartão saem juntos (dissolve + desfoque de 0,20 s) a partir daqui
	push?: number; // push contínuo do rosto (0,07 = +7%)
};

export type CardFinalVox = {ini: number; texto: string};

export type BlocoVox = {
	layout: 'abertura' | 'invasao' | 'split' | 'ele' | 'mural' | 'moldura' | 'fecho';
	ini: number;
	fim: number;
	palco?: string; // invasao e mural: o palco de tela cheia; moldura: o palco do fundo
	entrada?: 'papel' | 'monta' | 'corte'; // invasao/mural: como a colagem toma a tela
	abertura?: AberturaVox;
	// split: herda = palco da cena anterior (o painel sobe e ela encolhe); animações uma por vez, cada uma no seu palco
	herda?: string;
	animacoes?: {ini: number; palco: string; troca?: TrocaPainel}[];
	punches?: {t: number; z: number}[]; // ele, fecho: punch por corte seco (z = escala sobre a base)
	moldura?: {cards: string; recorte?: {arquivo: string; brutoIni: number; fps: number}; zoomFundo?: number; desfoque?: number; escurece?: number};
	card?: CardFinalVox; // fecho: card final (nome + @)
	legenda?: {y?: number; caixa?: boolean; ocultar?: boolean};
	rosto?: {x: number; olhos: number; queixo: number; topo: number}; // medido no trecho do bloco (ele se mexe ±25 px)
};

// SFX no formato do PAPER VOX (criarSfx do scripts/lib/mural.mjs): t = início do arquivo.
export type SfxVox = {t: number; som: string; vol?: number; evento?: {tipo: string; t: number}; alvo?: 'ataque' | 'pico'};

export type VoxProps = {
	modelo?: string;
	bruto: string; // relativo à pasta pública
	voz?: string;
	ini?: number; // s do bruto em que a composição começa
	duracao: number;
	palavras: string | Palavra[];
	_palavras?: Palavra[];
	rosto: {x: number; olhos: number; queixo: number; topo: number}; // medido no bruto, px de 1080×1920 (zoom 1)
	blocos: BlocoVox[];
	palcos: Record<string, PalcoVox>;
	sfx?: SfxVox[];
	sfxNaMixagem?: boolean;
	preto?: number; // s da saída em que entra o corte para preto
	_desligar?: string[]; // só para perfil de render: blur, grao, sombra, borda, textura, desfoque
};
