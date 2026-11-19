# Prompts do Google Flow: INSTAGRAM - PAPER VOX ANIMATION (apoio do guia de estilo)

> **Nota da adaptação (SOUTO TREINADOR):** este texto veio da calibração original do motor, feita em outro canal antes da entrega ao Jorge Souto. Nomes de pilotos e projetos citados (ex.: "sono x imunidade", "sociedade que adoece", "creatina sem treino") são desses vídeos de calibração e **não estão no repositório**; para o Jorge, "o piloto" de um formato é o 1º vídeo dele aprovado naquele formato. Cores já convertidas para a identidade azul (`marca/marca-souto.json`). Caminhos: projetos em `%SOUTO_VIDEO_PROJETOS%`, motor em `04 - EDIÇÃO DE VÍDEO/motor` (mapa em `motor/scripts/lib/caminhos.mjs`).


Versão aprovada no piloto "sociedade que adoece" (prompts e 47 imagens aprovados pelo Jorge em 2026-10-19; 0 crédito). Substitui o rascunho do lab (`05_LAB/formatos/4-paper-vox-animation/prompts-nano-banana.md`). Etapa P3 do guia (`guia-de-estilo.md`): o agente `diretor-paper-vox` (modo "prompts") escreve `03_roteiro/prompts_flow.md` (leitura do Jorge) e `prompts_flow.json` (operação) a partir da shot list aprovada. ⏸ Jorge antes de gerar.

## O que vem do Flow e o que é código
- **Do Flow (Nano Banana 2.1, 0 crédito):** só stills.
  - fotos de estação (`Fnn`, bloco FOTO);
  - objetos e estátuas para recorte (`Fnn`, bloco RECORTE);
  - planos de montagem (`Mnn`, bloco MONT).
- **Em código:** jornal, papel, mesa, interface, texto, silhuetas, cabeças, objetos de papel (bateria, balança, engrenagens…), traço, luz. Nada disso vai para o Flow.
- **Sem vídeo gerado** (Omni/Veo só como exceção, com ⏸ e custo).
- **Ids:** `F01…` na ordem das estações; `M01…` numerados em sequência pelas montagens (o `montar_shotlist.mjs` numera sozinho). O id é o nome do arquivo em todo o resto do fluxo.

## Blocos de estilo (vão no começo de cada prompt, sem mudar)
- **FOTO** (foto de estação ou do jornal; proporção 3:4 ou 4:3):
  `Black and white halftone press photograph, high contrast, crushed blacks, heavy film grain, full frame, no borders. No recognizable faces. No text, no letters, no numbers, no logo, no brand, no watermark.`
- **RECORTE** (objeto ou estátua que vira PNG com alfa; 1:1):
  `Studio product photo, centered, the whole object visible with margin, isolated on a solid flat pure blue background (#0000FF), even flat lighting, no shadow, no reflection, sharp edges. No text, no letters, no logo, no brand, no watermark.`
- **MONT** (plano de montagem; 9:16):
  `Cinematic black and white photograph, vertical 9:16, low-key lighting, one hard light source, deep blacks, shallow depth of field, subtle film grain, realistic, dramatic. No recognizable faces. No text, no letters, no numbers, no logos, no brand, no watermark.`
- **Prompt final = bloco + espaço + assunto** (em inglês, uma ou duas frases concretas).
- Luz de recorte, sombra, borda, halftone extra e P&B final são feitos em código: não pedir no RECORTE (luz de borda sobre o azul deixa halo).

## Como escrever o assunto (o que o piloto mostrou que funciona)
- Concreto e fotografável: lugar, objeto, luz, enquadramento. Ex.: `A plain black office swivel chair, three-quarter view.`
- **Recorte:** um objeto só, inteiro, sem marca. `plain`, `no markings`, `no brand`. Estátua: `A classical white marble bust of an anonymous ancient … man, head and shoulders only, weathered stone texture.`
- **Montagem:** ação com mãos, objeto ou gente de costas, sempre de noite ou pouca luz. Telas e papéis com `screen not readable` / `nothing readable`; relógio com `plain dial without numbers`; sacola, crachá e tênis com `no brand` ou `blank`.
- **Rimas entre montagens** (escolha de propósito, nunca repetição): o mesmo objeto em dois estados (tênis na caixa → mãos amarrando o cadarço; bicicleta empoeirada → bicicleta saindo para a luz).
- **Ética:**
  - nunca rosto reconhecível, pessoa real, "no estilo de [artista]", marca ou logo;
  - nenhum corpo no tema emagrecimento (estátua só com cabeça e ombros; montagem só com mãos, objetos e gente de costas);
  - texto nunca dentro da imagem.
- **Filtro do Flow:** no piloto, a F06 com "Roman woman… eyes looking down" foi barrada (sem cobrança); "anonymous ancient Roman figure, head bowed slightly forward" passou. Se barrar, trocar o sujeito por uma figura anônima neutra.

## Quantidade e orçamento
- **Variações:** x2 por imagem; x4 nas de destaque (no piloto: F01, F02, F04, F06). Piloto: 47 imagens, 102 variações.
- **Teto:** 25 imagens por minuto de vídeo (ERRO no `validar-shotlist.mjs`); ≥ 35% das estações sem imagem (AVISO).
- **Proporções do piloto:** FOTO 3:4 (vertical) ou 4:3 (horizontal), conforme o papel da estação; RECORTE 1:1; MONT 9:16.
- Foto da biblioteca (`%SOUTO_VIDEO_PROJETOS%/_biblioteca/broll-reutilizavel`) não vai para o Flow: entra como `biblioteca:<caminho>` na shot list e vira P&B no gerador.

## `prompts_flow.md` (leitura do Jorge)
Cabeçalho com o total (imagens, variações, créditos = 0, "Omni = 0"), as regras acima em 3–4 linhas e a tabela:

| id | onde entra | estilo | proporção | x | assunto (inglês, vai depois do bloco) |
|---|---|---|---|---|---|
| F03 | E07 sentado | RECORTE | 1:1 | 2 | A plain black office swivel chair, three-quarter view. |
| M01 | M1 · ônibus lotado à noite, gente de pé de costas segurando a barra | MONT | 9:16 | 2 | A crowded city bus at night, standing passengers seen from behind holding the overhead bar, blurred city lights through the windows. |

Depois da geração, acrescentar a linha "Gerado em AAAA-MM-DD no projeto do Flow "<nome>": N de N, 0 crédito; brutos em `04_broll/ia_flow/_brutos/<id>/`".

## `prompts_flow.json` (operação)
```json
{
  "modelo": "Nano Banana 2.1",
  "creditos_por_imagem": 0,
  "creditos_total": 0,
  "estilos": {"FOTO": "…", "RECORTE": "…", "MONT": "…"},
  "itens": [
    {"id": "F04", "uso": "E14 polêmica", "estilo": "RECORTE", "aspecto": "1:1", "x": 4,
     "assunto": "A classical white marble bust of an anonymous ancient Greek man in strict side profile, head and shoulders only, weathered stone texture.",
     "prompt": "<bloco RECORTE> A classical white marble bust …"}
  ]
}
```
- `prompt` = o texto exato que vai no campo do Flow (bloco + assunto).

## Operação no Flow (Chrome do Jorge, ferramentas Claude in Chrome)
1. **Antes:** nenhum render rodando (com a máquina sem RAM, o Chrome dá timeout no mouse e o texto colado por JS não chega ao editor). A janela do Chrome precisa estar visível.
2. `flow.google.com` → Novo projeto com o nome do vídeo (piloto: "lab formato4 - sociedade que adoece").
3. No chip do modelo: **Nano Banana 2.1**, Imagem, a proporção do item e o x. **Conferir a linha "A geração vai usar 0 créditos"** antes de enviar; se passar de 0, parar e pedir ⏸ ao Jorge.
4. Prompt no campo "O que você quer criar?" → "Iniciar geração". Uma linha por prompt, na ordem da tabela. **Não clicar "às cegas" em sequência:** no piloto saíram 7 lotes repetidos assim.
5. **Baixar para escolher:** "Baixar lote" de cada linha (zip em 1K, com nomes descritivos que casam com o prompt). Por JS: `button[aria-label="Baixar lote"].click()`, rolando o `.cdk-virtual-scrollable`. Os downloads das artes do Flow já estão liberados pelo Jorge.
   - Salvar as variações em `04_broll/ia_flow/_brutos/<id>/<id>_vN.jpg`.
6. **Escolher:** agente `diretor-de-arte` (modo qualidade) dá nota a cada variação e grava `04_broll/ia_flow/escolhas.json` (`{"F10": {"v": 1, "nota": "…"}}`, com alertas de halo ou artefato).
7. **Baixar a escolhida em 2K:** abrir a imagem no Flow → Baixar → **2K Aprimorada**. O 1K do lote (896×1200; 768×1376 no 9:16) fica pequeno: no final, os planos de montagem são ampliados 1,6–1,8×.
   - Salvar como `04_broll/ia_flow/<id>.jpg`.
8. **Recortes** (bloco RECORTE), de dentro do motor, com os caminhos completos (o script não recebe `<proj>`: lê a entrada direto e resolve a saída a partir da pasta atual):
   `node scripts/recorte-chroma.mjs <proj>/04_broll/ia_flow/<id>.jpg <proj>/04_broll/ia_flow/recortes/<id>.png --pb --aparar [--choke 1|2] [--conferir <proj>/06_previas/<id>_conferir.png]`
   - A cor-chave é medida nos 4 cantos (o "azul" veio ~`#0035FF`, não `#0000FF`). O script também aceita fundo verde `#00FF00`.
   - Halo > 3% (> 6% com `--pb`) = refazer com `--sim` maior ou gerar de novo. Objeto fino (tubo, fio) pede `--choke 1-2` (F10, o estetoscópio).
   - Guarde a variante escolhida em `_brutos/` até a prévia ser aprovada: é a única fonte para recortar de novo.
9. **Folha de contato:** `06_previas/imagens-escolhidas_<n>.jpg` → ⏸ Jorge.
10. **Área clara:** plano que passe de ~15% de área clara (no piloto, M27: porta aberta ao sol) leva `escurecer` no gerador do mural.
11. Se o Flow falhar, entregar os prompts para o Jorge gerar e soltar os arquivos na pasta com os nomes dos ids.

## Do rascunho do lab, o que mudou
- **Saíram** (não usados no piloto; a cena é montada em código):
  - STYLE-CENA, P3 diorama e P6 mesa: fundo, mesa e jornal são papel em código;
  - P4 camadas e P5 poses;
  - P7 silhueta: virou o objeto `silhuetas`;
  - P8 ícone pixel-art: só recorte realista.
- **Viraram os 3 blocos aprovados:**
  - P1 foto do jornal → **FOTO**;
  - P2 recorte → **RECORTE**, que agora é "studio product photo" em azul, luz chapada, sem sombra;
  - plano de montagem 9:16 P&B → **MONT** (novo).
- O fallback `remove-background` não foi preciso: o `recorte-chroma.mjs` com despill e `--choke` resolveu os 8 recortes.
