# Frente 03: Carrosséis e arte

Carrosséis do Instagram do Jorge Souto (SOUTO TREINADOR, educador físico), 1080×1350 exportados em 2160×2700, escritos pelo método de texto nativo de carrossel (inspirado na BrandsDecoded) em **5 formatos** visuais, na identidade azul da marca, com artes em foto realista (Gemini/Google Flow no navegador ou Higgsfield pelo MCP) e renderização local com verificação automática de diagramação. Guia passo a passo para humanos: `../docs/guias/03-carrossel.md`.

## Comando
`/carrossel` (`../.claude/skills/carrossel/SKILL.md`). Fluxo, com ⏸ aprovação do Jorge:
entrada (conteúdo existente ou tema da base) + Ficha → triagem recomenda o **TIPO** ⏸ → Jorge escolhe o **FORMATO** e o nº de slides ⏸ → 10 headlines ⏸ → (espinha, só se pedir) → texto por slide (validador até 0 ERRO) → revisão editorial (7 parâmetros ≥ 8) → aprovação do texto ⏸ → artes ⏸ créditos → render com 0 ALERTA + folha de contato → editor visual (opcional) → fontes por script, legenda, entrega.

- **Tipo ≠ formato.** Tipo = linha narrativa (Tendência · Tese, com a variação Mito × evidência · Case · Previsão). Formato = design (M1 Mangá Dark · M2 Editorial Clean · M3 Dossiê · M4 Cinema · M5 BrandsDecoded). Qualquer tipo sai em qualquer formato.
- Padrão de **9 slides** (5, 7 ou 12 também valem).
- **CTA pelo conteúdo:** `consultoria` (padrão) = treino individualizado com Jorge Souto, treinador, CREF, link na bio; `ebook` só se o Jorge tiver um material próprio. Um só, diretivo, sem preço.

## Agentes (`../.claude/agents/03-carrosseis/`, salvo o legendista)
| Agente | Etapa |
|---|---|
| `chefe-de-pauta` | triagem, eixo, funil, TIPO, CTA; 10 headlines + versão de capa |
| `redator-de-carrossel` | espinha; texto no `carrossel.json` até 0 ERRO |
| `editor-de-texto` | revisão editorial (7 parâmetros ≥ 8, 5 testes), tabela QA |
| `diretor-de-arte` | prompts por espaço de arte, com a rota (banco, Gemini/Flow ou Higgsfield) e controle de qualidade |
| `revisor-de-diagramacao` | diagnóstico do render e da folha quando houver dúvida |
| `legendista` (`../.claude/agents/05-publicacao/`) | legenda: gancho ≤ 125 caracteres, contexto, análise, Fontes do script, CTA, 5–12 hashtags |

## Marca (um lugar só)
`Gerador/marca.json`: logo branca transparente (`Gerador/logo.png`, cópia de `../marca/logo/souto-logo-branco.png`), paleta azul (aço `#445DB4`, elétrico `#2E49CE`, royal `#1F33A3`, noite `#141A3D`), fundos `#0B0B0E` e `#F2F4F8`, degradês (`gradiente`, `gradiente_escuro` para texto sobre fundo escuro, `gradiente_titulo`), assinatura "JORGE SOUTO · TREINADOR", par de cores do vídeo (`video`) e os dois campos **provisórios, marcados TROCAR**: `nome` (o @, hoje `@soutotreinador`) e `registro` (o CREF, hoje `CREF 000000-G/UF`). O render imprime um LEMBRETE enquanto não forem trocados. Cores-fonte: `../marca/marca-souto.json`.

## Validação do texto (antes de gastar arte e render)
- No `carrossel.json`: no topo `"ficha": "<Tema> - Ficha"`, `"tipo_carrossel"`, `"eixo"`, `"funil"`, `"headline"`, `"cta"`; em cada slide `"funcao"` e `"afirmacoes": [n, "N1", "M2", "H1"]` em todo slide com fato científico ou número. **Nunca [#n] no texto do slide.**
- `Gerador/validar_carrossel.py <carrossel.json>`: limites de caracteres, ids na Ficha, verbo × certeza, números na linha citada, palavras proibidas (módulo de evidência compartilhado: `../02 - ROTEIROS/_SISTEMA/validar_roteiro.py`) + `Gerador/editorial.py` (regras editoriais e de ética).
- **Ética = ERRO:** antes/depois, depoimento ou resultado de aluno, preço/promoção, promessa de quilos/centímetros com prazo ou garantia (CONFEF + marca); **prescrição de dieta, cardápio, calorias ou suplemento com dose** (atividade do nutricionista, Lei 8.234/1991); ordem sobre remédio ou hormônio (médico).
- **AVISO:** ordem de comida/suplemento sem dose; slide de nutrição sem id da Ficha (nutrição só como educação geral, com a fonte); "exercício que seca a barriga"; ordem de treino com número para o leitor; 2ª pessoa fora de aplicação/CTA; jargão; coach; sigla/termo técnico; consultoria sem CREF no CTA (M1–M4); forma do M5.
- `--montar-fontes` escreve `## Fontes` e `## Nível de certeza` no `carrossel.md`. Fonte nunca à mão.
- Hook opcional: `../.claude/hooks/validar_peca.py` (da frente de roteiros) roda o validador a cada gravação de `Carrosséis/**/carrossel.json`, se estiver registrado no `.claude/settings.json` (guia, seção "Hook").

## Editor visual (tudo é HTML antes do PNG)
- Cada slide vira `html/slide-NN.html`; todos os elementos dos 5 modelos são editáveis: dois cliques em `Abrir editor de carrossel.bat` → http://localhost:8765/editor (só escuta no próprio computador).
- Slide salvo no editor ganha `data-editado` e o render **não** o sobrescreve (só com `--refazer`). Mudança de conteúdo vai no JSON, para passar pelo validador.

## Artes
- **Foto realista conceitual, sóbria e clean**, sem anime/3D/ilustração, sem texto ou marca, sem pessoa real reconhecível, sem corpo de antes/depois; treino plausível e seguro. A paleta azul vale para os elementos gráficos; a foto pode ter outras cores.
- **Rotas:** (A) Gemini / Google Flow no Chrome do Jorge, 1 ou 2 gerações por disparo, com pausa; (B) Higgsfield pelo conector MCP no Claude (gasta créditos da conta Higgsfield a cada geração); (C) banco de imagens pelo `../04 - EDIÇÃO DE VÍDEO/motor/scripts/stock.mjs` (Pixabay/Pexels com `PIXABAY_API_KEY` e `PEXELS_API_KEY` no `.env` da raiz; Openverse/Wikimedia sem chave), para cena, fundo e textura.
- **Recorte:** gerar em FUNDO BRANCO puro, sujeito opaco e de tom médio/escuro; preto puro só para objeto luminoso. M1 e M4 escolhem o modo pelo fundo (`comum.modo_pelo_fundo`); M2 e M3 usam "borda".
- Nome das artes: `artes/slide-NN.png` (2ª arte `slide-NN-2.png`; blend `slide-NN-fundo.png`). Arquivo que não existe = marcador cinza + ALERTA. Nenhuma foto se repete no carrossel.

## Arquivos
| Pasta / arquivo | O que tem |
|---|---|
| `Referências/Método BrandsDecoded/Método de texto - carrossel.md` | o método de texto (resumo próprio, adaptado a treino). O material original do curso **não** fica no repositório |
| `Gerador/` | `render_carrossel.py` (M1 + render/verificação de todos), `modelo_editorial.py` (M2), `modelo_dossie.py` (M3), `modelo_cinema.py` (M4), `modelo_brandsdecoded.py` (M5), `comum.py` (recorte, posicionamento), `editor.py` + `editor.html`, `folha.py`, `conferir_recortes.py`, `validar_carrossel.py`, `editorial.py`, `marca.json`, `logo.png`, `_marcadores/` (marcadores cinza: cache, o render refaz quando falta). O formato do JSON de cada modelo está na docstring do topo de cada script |
| `requirements.txt` | dependências Python (Pillow, numpy, scipy) |
| `Abrir editor de carrossel.bat` | abre o editor visual |
| `Carrosséis/AAAA-MM-DD - tema/` | um carrossel por pasta: `carrossel.json`, `artes/`, `html/`, PNGs, `folha.jpg`, `prompts_arte.md`, `carrossel.md` |
| `Carrosséis/_testes/` | testes dos 5 modelos com texto fictício e marcadores cinza (`_teste-modeloN.json`; folhas `folha.jpg` e `_folha-modelos-1-3-4.jpg`). Não publicar |

## Regras
- Tipo antes do formato; texto aprovado **antes** das artes; créditos de geração com ⏸ do Jorge.
- Voz mista (reportagem no corpo; 2ª pessoa só em aplicação e CTA); fonte simples no slide; linguagem leiga; verbo pela certeza.
- Paleta sempre em degradê nos elementos gráficos; destaque do M5 em degradê.
- Recortes conferidos antes do render (`conferir_recortes.py`); correção renderiza só os slides alterados (`--slides=4,6`).
- Só entregar com 0 ALERTA e depois de olhar a folha de contato inteira.
- Requisitos: Python 3.12+, `pip install -r requirements.txt`, Google Chrome (a variável `CHROME` aponta outro caminho; o Edge não funcionou no teste). Os scripts acham `marca.json`, `logo.png` e `_marcadores/` pela própria pasta: se mover o `Gerador/`, mova tudo junto.
