// Mural do INSTAGRAM - VOX - B-ROLLs (vox-broll-instagram; nasceu no lab como scripts/lab/vox-mural.mjs, fixo desde
// 2026-10-30): estação em escala k e mergulho com resquício (calibração original, 2026-10-29, pergunta
// 3 = A: "a cena nova nasce dentro de uma parte da anterior e a câmera mergulha nela", com um resquício no canto).
// Ideia copiada do scripts/lib/mural.mjs (o ctx(id, base, k) da l. 229 fica dentro do criarMural e não é exportado; o
// criarMural exige shotlist com estações e grava quadro.json do PAPER VOX, então não serve aqui). Aqui:
//   - estacao(): peças relativas ao centro da estação, × k (posição, tamanho, fonte), no grupo da estação;
//   - mergulho(): câmera que entra no hospedeiro de B e PARA em frac/k (0,8–0,9/k, não 1/k), deslocada para o objeto-chave
//     de A ficar num canto de cima com parte fora da borda; devolve o hospedeiro e a área de tela onde B se compõe;
//   - resquicio(): o texto de A sai antes (dissolve 0,20 s) e o grupo A sai de foco (escurece + cópia pré-desfocada).
// O zoom se acumula a cada mergulho (× 1/k): a câmera do palco interpola o zoom em escala log.
import {r3} from './vox.mjs';

export const estacao = (P, id, base, k = 1) => {
	const c = {id, x: base.x, y: base.y, k};
	c.p = (dx, dy) => [base.x + dx * k, base.y + dy * k];
	// dx, dy = relativo ao centro (× k); sem eles, x e y valem como estão (só o tamanho vai × k)
	c.add = ({dx, dy, ...el}) => {
		const [x, y] = dx == null && el.x != null ? [el.x, el.y] : c.p(dx ?? 0, dy ?? 0);
		const e = {...el, x, y, w: el.w * k, grupo: id};
		if (el.h != null) e.h = el.h * k;
		if (el.tamanho != null) e.tamanho = r3(el.tamanho * k);
		if (el.entra?.dist != null) e.entra = {...el.entra, dist: el.entra.dist * k};
		return P.add(e);
	};
	return c;
};

// chave: caixa do objeto-chave de A no mundo {x, y, w, h}; canto: onde o centro dele fica na tela no fim do mergulho;
// hospTela: canto de cima-esquerda do hospedeiro na tela no fim do mergulho (B se compõe dali até a borda).
export const mergulho = ({chave, k, frac = 0.85, canto = [150, 330], hospTela = [330, 470]}) => {
	const zoom = frac / k;
	const cx = chave.x - (canto[0] - 540) / zoom;
	const cy = chave.y - (canto[1] - 960) / zoom;
	const telaParaMundo = (sx, sy) => [r3(cx + (sx - 540) / zoom), r3(cy + (sy - 960) / zoom)];
	const [hx0, hy0] = telaParaMundo(...hospTela);
	const hosp = {x: r3(hx0 + 540 * k), y: r3(hy0 + 960 * k), w: r3(1080 * k), h: r3(1920 * k)};
	// "ao lado, nunca nele": o hospedeiro não pode cobrir o objeto-chave de A
	const sobrepoe = !(hosp.x - hosp.w / 2 >= chave.x + chave.w / 2 || hosp.y - hosp.h / 2 >= chave.y + chave.h / 2 || hosp.x + hosp.w / 2 <= chave.x - chave.w / 2 || hosp.y + hosp.h / 2 <= chave.y - chave.h / 2);
	if (sobrepoe) throw new Error('[vox-mural] o hospedeiro de B cobre o objeto-chave de A: mude `canto` ou `hospTela`');
	// fração do objeto-chave que fica fora da tela (guia: 15–40%) e a área que ele ocupa (10–25% do quadro)
	const sx0 = 540 + (chave.x - chave.w / 2 - cx) * zoom, sx1 = 540 + (chave.x + chave.w / 2 - cx) * zoom;
	const sy0 = 960 + (chave.y - chave.h / 2 - cy) * zoom, sy1 = 960 + (chave.y + chave.h / 2 - cy) * zoom;
	const area = (sx1 - sx0) * (sy1 - sy0);
	const dentro = Math.max(0, Math.min(1080, sx1) - Math.max(0, sx0)) * Math.max(0, Math.min(1920, sy1) - Math.max(0, sy0));
	return {zoom: r3(zoom), cx: r3(cx), cy: r3(cy), hosp, telaParaMundo, resquicio: {fora: r3(1 - dentro / area), quadro: r3(dentro / (1080 * 1920))}, areaB: {x0: hospTela[0], y0: hospTela[1], x1: 1080, y1: 1500}};
};

// Resquício: o texto de A sai antes (dissolve + desfoque de 0,20 s) e o grupo A sai de foco a partir de t.
export const resquicio = (P, grupo, t, {escurece = 0.26, dur = 0.35} = {}) => {
	for (const e of P.palco.elementos) if (e.grupo === grupo && (e.tipo === 'texto' || e.tipo === 'numero' || e.tipo === 'etiqueta')) {
		if (e.fim == null || e.fim > t) e.fim = r3(t);
		e.sai = {tipo: 'some', dur: 0.2};
	}
	P.palco.focos.push({t: r3(t), grupo, dur, escurece});
};
