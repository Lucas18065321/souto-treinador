// Imagens importadas direto no código (logo da marca): o bundler do Remotion devolve a URL do arquivo.
declare module '*.png' {
	const url: string;
	export default url;
}
declare module '*.jpg' {
	const url: string;
	export default url;
}
