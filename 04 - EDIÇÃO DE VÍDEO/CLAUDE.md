# Frente 04: Edição de vídeo (SOUTO TREINADOR)

Motor de edição local (Remotion + scripts Node + FFmpeg) operado pelo Claude Code, na identidade azul do Jorge Souto. Responda em português, curto e direto. Guia de uso para o Jorge (instalação, passo a passo, problemas): `docs/guias/04-video.md`.

## Onde fica cada coisa
| O quê | Onde |
|---|---|
| Motor (Remotion + scripts) | `04 - EDIÇÃO DE VÍDEO/motor` (rode `node scripts/...` de dentro dele) |
| Mapa de pastas (fonte única) | `motor/scripts/lib/caminhos.mjs` |
| Guias de estilo dos 5 formatos | `referencias/modelos/<id>/guia-de-estilo.md` · registro `referencias/modelos/MODELOS.md` |
| Histórico completo de calibração (tempos medidos, erros já vividos, dicas do Flow) | `referencias/MANUAL-COMPLETO-DO-MOTOR.md` |
| Decisões de estilo (herdadas; o Jorge pode mudar) | `Decisões de edição.md` |
| Catálogo de peças de motion | `kit/KIT.md` |
| SFX sintetizados + pasta de compatibilidade `motionix/` (gerada) | `sfx/biblioteca/` |
| SFX catalogados (Glitch Noises CC0 + Mixkit/99Sounds que o Jorge baixar) | `sfx/lab/<categoria>/` + `sfx/lab/catalogo.tsv` |
| Identidade: cores e logo | `../marca/marca-souto.json` (par `video`) e `../marca/logo/` → lidos por `motor/src/marca.ts` |
| Identidade: nome, cargo, @, CREF (campos TROCAR) | `marca-video.json` |
| Dicionário pt-BR e glossário de treino | `ferramentas/` |
| **Projetos, brutos, prévias, finais** | **`%SOUTO_VIDEO_PROJETOS%/<AAAA-MM-DD>_<nome>/01_bruto … 07_final`** (fora do repositório e do OneDrive; padrão `%USERPROFILE%\Videos\Souto-Projetos`, definido no `.env` da raiz) |
| Biblioteca de B-roll e músicas | `%SOUTO_VIDEO_PROJETOS%/_biblioteca/{broll-reutilizavel,musicas,catalogo.json}` |
| Modelos do Whisper, DeepFilterNet, regressão, fila de render | `%SOUTO_VIDEO_PROJETOS%/_sistema/` |

Nada de vídeo, foto, voz ou rosto do Jorge entra no repositório (é público). O `.gitignore` desta pasta barra; mesmo assim, nunca salve mídia dentro de `04 - EDIÇÃO DE VÍDEO/`.

## Os 5 formatos (todos FIXOS: estilo e guia só mudam a pedido do Jorge)
| Formato (id) | Saída | Para quê |
|---|---|---|
| INSTAGRAM - TELA DIVIDIDA (`tela-dividida-2-instagram`, composição `TelaDividida2`) | 1080×1920, 24 fps | Reels explicativo: B-roll em cima, rosto embaixo, objetos voando, gráficos em vidro |
| INSTAGRAM - EDIÇÃO CUT DINÂMICO (`cut-dinamico-instagram`, `CutDinamico`) | 1080×1920, 24 fps | Reels de ritmo alto: legenda cinética, texto atrás da pessoa, 3D, cards |
| YOUTUBE - MIX EDIT (`mix-edit-youtube`, `MixEdit`) | 1920×1080, 30 fps | Vídeo longo do YouTube: intro cinematográfica, Apple edit + 3D flash, capítulos |
| INSTAGRAM - PAPER VOX ANIMATION (`paper-vox-instagram`, `PaperVox`) | 1080×1920, 24 fps | Só a partir de um ÁUDIO: mural de papel animado, 100% dark, o Jorge não aparece |
| INSTAGRAM - VOX - B-ROLLs (`vox-broll-instagram`, `VoxBroll`) | 1080×1920, 24 fps | O Jorge falando + colagens animadas estilo Vox (abertura, invasão, mural, moldura) |

O clássico `tela-dividida-instagram` (composição `Edicao`) está congelado e arquivado: só para referência.
**Regra do Instagram:** 1080×1920 a 24 fps (`motor/src/modelos.json`); não subir.

## Fluxo
O comando é **`/editar <bruto ou áudio>`** (`.claude/skills/editar/SKILL.md`), com pontos de aprovação ⏸. Formato novo: **`/novo-modelo`**. Agentes em `.claude/agents/04-video/`: `montador`, `decupador`, `revisor-de-video`, `analista-de-referencias`, `diretor-paper-vox`, `diretor-vox`.
Resumo: novo projeto → (preparar/decupar/cor/áudio só se o Jorge marcar) → assistir/transcrever → plano ⏸ → material (biblioteca → banco `stock.mjs` → Flow) ⏸ → montagem (`montador` + `validar-edicao.mjs` até 0 ERRO) → **ilha de edição** (prévia ao vivo, ajustes por tempo) ⏸ → pergunta do tratamento de voz ⏸ → render final → biblioteca.
- **Ilha:** `node scripts/ilha.mjs [<proj>]` abre o Remotion Studio em `http://127.0.0.1:3123/<composição>` e recarrega a cada mudança do `edicao.json`. O projeto ativo fica em `%SOUTO_VIDEO_PROJETOS%/.projeto-ativo`. Não vale para PAPER VOX e VOX (prévia renderizada).
- **Validador:** `node scripts/validar-edicao.mjs <proj>` (ERRO = código 1). Com o hook configurado no `.claude/settings.json` da raiz, roda sozinho a cada gravação de `03_roteiro/edicao.json`. Nunca edite o validador, os guias ou o `tipos.ts` para "passar".
- **Render:** `node scripts/vez.mjs node scripts/render.mjs <proj> [--previa] [--trecho a b]` (TELA DIVIDIDA, CUT, MIX); `render-paper-vox.mjs` e `render-vox.mjs` nos outros dois, sempre pela fila.

## Identidade visual (azul)
Acento azul elétrico `#2E49CE`, profundo `#141A3D`, texto claro `#F2F4F8`, tinta `#0B0B0E`, degradês `nevoa-eletrico`, `claro-aco`, `eletrico-aco` (antes eram salmão/laranja). Tudo sai de `motor/src/marca.ts`, que lê `../marca/marca-souto.json`. A logo branca entra no card de apresentação (`apresentacao-redes`, parâmetro `logo`) e no card final (`encerramento-insta`). Nome/@/CREF de `marca-video.json`: **antes do primeiro vídeo publicado, confirme com o Jorge o @ e o CREF (campos TROCAR)**.
Fontes: Google Fonts (OFL) baixadas no render pelo `@remotion/google-fonts` (precisa de internet); Instrument Serif + Inter Tight são o par padrão dos formatos.

## SFX
- As peças pedem nomes `motionix/<categoria>/<arquivo>` (o motor foi calibrado com esse pacote, que não pode ser redistribuído). O instalador gera essa pasta com sons livres parecidos: `node scripts/sfx/sfx-substitutos.mjs` (`--forcar` refaz).
- Biblioteca do lab: 133 Glitch Noises (CC0, prova em `sfx/lab/licencas/`) + 6 de papel sintetizados. Mixkit (lista `sfx/lab/lista-mixkit.html` → `node scripts/sfx/sfx-importar-mixkit.mjs`) e 99Sounds (lote + `sfx-catalogar.mjs`) o Jorge baixa à mão: a licença proíbe redistribuir e baixar por robô. Nunca suba esses arquivos.
- `sfx-variado.mjs` (só no Tela Dividida clássico), `refinar-sfx.mjs` (PAPER VOX e VOX) e `synth-sfx.mjs` (gera os sintetizados) estão em `motor/scripts`.

## Regressão (depois de QUALQUER mudança no motor)
Cada formato tem um piloto = um vídeo do Jorge já aprovado, configurado em `%SOUTO_VIDEO_PROJETOS%/_sistema/regressao/pilotos.json` (modelo: `motor/regressao.pilotos.exemplo.json`). Sem piloto, o script avisa e sai com código 2. Uma por vez, pela fila:
`node scripts/vez.mjs node scripts/regressao.mjs --td2` · `--cut` · `--mix` · `node scripts/vez.mjs node scripts/regressao-paper-vox.mjs` · `node scripts/vez.mjs node scripts/regressao-vox.mjs`. Referência nova (`--gravar`) só com o ok do Jorge.

## Regras da máquina
- **Um render/recorte/conversão pesada por vez** (`vez.mjs`). Com ~8 GB de RAM: no máximo 2–3 agentes em paralelo, prévias em meia resolução, `--concurrency=2` (VOX: 1). Feche o Chrome pesado durante render longo.
- Avise o tempo antes de render longo (medidos numa máquina de 7,7 GB: prévia ≈ 3 s de render por segundo de vídeo; final 9:16 ≈ 6–10 s/s; MIX ≈ 5 s/s; PAPER VOX final ≈ 12 s/s; VOX final ≈ 5,6 s/s).
- 3D e efeitos WebGL usam `--gl=angle` (já no `modelos.json`). Placa Intel (Quick Sync) é usada quando existe; sem ela tudo cai na CPU sozinho.
- Caminhos dentro de filtros do FFmpeg: relativos (sem `C:`); `SOUTO_VIDEO_PROJETOS` no mesmo disco do Windows (C:).
- O render copia a pasta inteira do projeto: versões antigas do final fora de `07_final/`.
- **Custo zero:** só ferramentas grátis ou já pagas. API paga (Gemini via `gen.mjs`) só em emergência e com o ok do Jorge.
- Vídeo aprovado é intocável: ajuste pedido depois muda só aquilo.
- Áudio: sempre perguntar antes de tratar a voz; cor: não mexer se o bruto já vem ajustado.
- Música: no máximo 1/4 da voz (−12 dB), medida (`ebur128`), nunca cobrindo a voz.
- Sem repetição visual: o mesmo B-roll nunca duas vezes no mesmo vídeo.
- Nunca use imagem/pessoa real gerada por IA como se fosse real; manchetes reais só por `capturar-manchete.mjs`, sem "melhorar".

## Ligação com as outras frentes
- Roteiro: `../02 - ROTEIROS/` (se existir). Fontes citadas na tela vêm da seção **Fontes** do roteiro.
- Carrossel: `../03 - CARROSSÉIS E ARTE` usa `motor/scripts/stock.mjs` para buscar imagens (não mude a interface desse script).
- Publicação: `../05 - PUBLICAÇÃO E CRESCIMENTO/Publicados.md`, se existir.
