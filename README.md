<p align="center"><img src="marca/logo/souto-logo-azul.png" width="260" alt="Souto Treinador"></p>

# Sistema Souto Treinador

Ecossistema de trabalho do **Jorge Souto, educador físico**, comandado pelo Claude Code: um cérebro científico de treino de força que alimenta a prescrição de treino, os roteiros, os carrosséis, os vídeos e o acompanhamento dos alunos no **Painel ST**.

> **Comece pelo guia em PDF:** [`docs/Guia Souto Treinador.pdf`](docs/Guia%20Souto%20Treinador.pdf) (instalação, uso, ferramentas, boas práticas e FAQ de cada motor, com prints).

## Os motores

| # | Pasta | O que faz | Guia |
|---|---|---|---|
| 01 | `01 - BASE CIENTÍFICA` | Cérebro científico: coleção de artigos de treino de força (Schoenfeld, Prestes, de Salles, Trindade, Paes e as principais revisões de volume, carga, RIR, periodização, autorregulação e deload), catalogados com teto de certeza; Fichas e Protocolos | [01](docs/guias/01-base-cientifica.md) |
| 05 | `05 - TREINO` | Prescrição de treino e controle de volume × desempenho: 1RM estimado, cargas por %1RM e RIR, volume load semanal, decisão PROGREDIR / MANTER / REDUZIR / DELOAD, mesociclos e ficha de treino em PDF | [06](docs/guias/06-treino.md) |
| 02 | `02 - ROTEIROS` | Roteiros de Reels e YouTube calibrados pela evidência, com validador (ética do CONFEF) | [02](docs/guias/02-roteiros.md) |
| 03 | `03 - CARROSSÉIS E ARTE` | Carrosséis em 5 formatos na identidade azul, editor visual, artes pelo Gemini/Flow ou Higgsfield (MCP) e banco de imagens | [03](docs/guias/03-carrossel.md) |
| 04 | `04 - EDIÇÃO DE VÍDEO` | Motor de edição (Remotion): 5 formatos, legendas, SFX, B-roll, ilha de edição ao vivo | [04](docs/guias/04-video.md) |
| 06 | `06 - GESTÃO DA CONSULTORIA` | Painel ST (Supabase), formulários Tally e plano alimentar do aluno com o nutricionista Responsável Técnico | [05](docs/guias/05-dieta-e-painel-st.md) |

Instalação: [Guia 00 · Instalação geral](docs/guias/00-instalacao-geral.md).

## Instalação rápida (resumo do guia 00)

```powershell
cd $env:USERPROFILE\Documents
git clone https://github.com/Lucas18065321/souto-treinador.git
cd souto-treinador
Copy-Item .env.example .env
```

Depois, abra a pasta no app Claude (aba **Code**) e escreva: `Leia o CLAUDE.md e me diga se está tudo instalado.`

## Regras que o sistema segue

- **Evidência primeiro:** nada é afirmado sem artigo processado na base; o verbo segue a certeza do estudo.
- **Ética do CONFEF** (Res. 307/2015) em todo conteúdo: sem promessa de resultado, antes/depois, depoimento ou preço.
- **Dieta é ato do nutricionista** (Lei 8.234/1991): o plano alimentar do aluno é prescrito e aprovado pelo Responsável Técnico, **Lucas Melo, nutricionista, CRN6 - 50479-P**. Nenhuma dieta sai sem a aprovação do RT no Painel ST.
- **Segredos e dados de alunos nunca entram no repositório:** chaves no `.env` e em `%USERPROFILE%\SoutoTreinador\privado\`, alunos em `%USERPROFILE%\SoutoTreinador\Alunos\`, assinatura do RT só por pen drive.
- **Direito autoral:** PDFs de artigos, músicas, B-roll e SFX com licença restrita não vêm no repositório; cada instalação baixa os seus (os guias explicam).

## Licenças de terceiros incluídas
- SFX "Glitch Noises" (Vladislav Zharkov): CC0 1.0 (`04 - EDIÇÃO DE VÍDEO/sfx/lab/licencas/`).
- Fontes Google Fonts: SIL Open Font License (`OFL.txt` em cada pasta de fontes).
- Tabela TACO (NEPA/Unicamp) e TBCA (USP/FoRC): tabelas públicas de composição de alimentos.
- Remotion: grátis para pessoa física e empresas de até 3 pessoas (confira em remotion.dev).
