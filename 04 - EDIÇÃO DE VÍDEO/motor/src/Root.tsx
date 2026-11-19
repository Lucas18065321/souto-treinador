import React from 'react';
import {Composition, Still} from 'remotion';
import {FontPreview} from './FontPreview';
import {EdicaoComp, calcularEdicao, type EdicaoProps} from './Edicao';
import {MotorCamadas, calcularCamadas, type CamadasProps} from './modelos/MotorCamadas';
import {PaperVox, calcularPaperVox} from './modelos/paper-vox/PaperVox';
import type {QuadroProps} from './modelos/paper-vox/tipos';
import {TelaDividida2, calcularTD2, type TelaDividida2Props} from './modelos/tela-dividida-2/TelaDividida2';
import {VoxBroll, calcularVox} from './modelos/vox/VoxBroll';
import type {VoxProps} from './modelos/vox/tipos';
import MODELOS from './modelos.json';
import {TesteKit} from './testes/TesteKit';

const exemplo: EdicaoProps = {
	duracao: 5,
	fonte: 'A',
	bruto: '01_bruto/bruto.mp4',
	palavras: '02_analise/palavras.json',
	destaques: [],
	cenas: [{ini: 0, fim: 5, layout: 'fala'}],
};

const exemploCamadas = (modelo: CamadasProps['modelo']): CamadasProps => ({
	modelo,
	duracao: 5,
	bruto: '01_bruto/bruto.mp4',
	palavras: '02_analise/palavras.json',
	cenas: [{ini: 0, fim: 5, layout: 'fala'}],
});

const exemploPaperVox: QuadroProps = {voz: '', duracao: 5, camera: [{t: 0, x: 0, y: 0, zoom: 1}], elementos: []};

const exemploTD2: TelaDividida2Props = {bruto: '01_bruto/bruto.mp4', palavras: '02_analise/palavras.json', duracao: 5, destaques: [], cenas: [{ini: 0, fim: 5, layout: 'fala'}]};

const exemploVox: VoxProps = {bruto: '', duracao: 1, palavras: [], rosto: {x: 540, olhos: 840, queixo: 1000, topo: 610}, blocos: [{layout: 'ele', ini: 0, fim: 1}], palcos: {}};

const {['cut-dinamico-instagram']: cut, ['mix-edit-youtube']: mix, ['paper-vox-instagram']: pv, ['tela-dividida-2-instagram']: td2, ['vox-broll-instagram']: vox} = MODELOS.modelos;

export const RemotionRoot: React.FC = () => {
	return (
		<>
			{/* INSTAGRAM - TELA DIVIDIDA: congelado (única mudança: 24 fps, regra do Instagram) */}
			<Composition id="Edicao" component={EdicaoComp} width={1080} height={1920} fps={MODELOS.modelos["tela-dividida-instagram"].fps} durationInFrames={150} defaultProps={exemplo} calculateMetadata={calcularEdicao} />
			{/* INSTAGRAM - TELA DIVIDIDA (o atual): substitui o clássico no /editar desde 2026-10-27 (props = edicao.json, tipo EdicaoTD2; render sem gl) */}
			<Composition id={td2.composicao} component={TelaDividida2} width={td2.largura} height={td2.altura} fps={td2.fps} durationInFrames={120} defaultProps={exemploTD2} calculateMetadata={calcularTD2} />
			{/* Formatos novos: motor de camadas, tamanho por src/modelos.json */}
			<Composition id={cut.composicao} component={MotorCamadas} width={cut.largura} height={cut.altura} fps={cut.fps} durationInFrames={150} defaultProps={exemploCamadas('cut-dinamico-instagram')} calculateMetadata={calcularCamadas} />
			<Composition id={mix.composicao} component={MotorCamadas} width={mix.largura} height={mix.altura} fps={mix.fps} durationInFrames={150} defaultProps={exemploCamadas('mix-edit-youtube')} calculateMetadata={calcularCamadas} />
			{/* INSTAGRAM - PAPER VOX ANIMATION: só a voz; mural contínuo por código (props = 03_roteiro/quadro.json, render por scripts/render-paper-vox.mjs) */}
			<Composition id={pv.composicao} component={PaperVox} width={pv.largura} height={pv.altura} fps={pv.fps} durationInFrames={120} defaultProps={exemploPaperVox} calculateMetadata={calcularPaperVox} />
			{/* INSTAGRAM - VOX - B-ROLLs: rosto + colagens animadas na espinha do dono do canal (props = 03_roteiro/vox.json, render por scripts/render-vox.mjs, sem gl) */}
			<Composition id={vox.composicao} component={VoxBroll} width={vox.largura} height={vox.altura} fps={vox.fps} durationInFrames={24} defaultProps={exemploVox} calculateMetadata={calcularVox} />
			<Still id="FontPreview" component={FontPreview} width={1080} height={1920} defaultProps={{pair: 0}} />
			<Composition id="TesteKit" component={TesteKit} width={1920} height={1080} fps={30} durationInFrames={60} />
		</>
	);
};
