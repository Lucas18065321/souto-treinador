---
tipo: template
atualizada: 2026-11-19
status: modelo pronto (portado e adaptado à marca Souto Treinador); fórmula do sono conferida (ver Fundamentação)
---
# Receituário de suplementação

A receita de manipulação que vai para a farmácia, em uma página A4, com a marca Souto Treinador e com todos os campos que a Res. CFN 656/2020 e a RDC Anvisa 67/2007 exigem. Sai de um JSON, por script, no Chrome do PC, sem token e sem internet. Usa as fontes, o logo e a impressão do template do plano (`../template`).

> **Quem prescreve e assina é o nutricionista RT** (Responsável Técnico pela dieta). O educador físico não prescreve suplemento manipulado. Por isso a Entrega do tipo "receituario" também passa pela **APROVAÇÃO DO RT** no Painel ST antes de ir ao aluno.

## Como gerar
```
python montar_receita.py receita-sono.json --saida "%USERPROFILE%\SoutoTreinador\Alunos\<nome do aluno>"
```
- Sai `Receituário - {primeiro nome} - AAAA-MM-DD` em .pdf e .html. Com o paciente em branco, sai `Receituário - em branco`, com as linhas para preencher à mão.
- **Para um aluno:** copie `receita-sono.json` para a pasta do aluno (fora do repositório), preencha `paciente` (`nome`, `nascimento`, `endereco`), `data` e `local`, e gere. (Na receita, a palavra é "paciente": é o termo da norma do CFN.)

## Arquivos
| Arquivo | O que é |
|---|---|
| `montar_receita.py` | monta e imprime a receita |
| `receita.css` | visual (claro, sóbrio, degradê azul só na faixa do topo, no selo e nos marcadores) |
| `prescritor.json` | modelo com o nome e o CRN do RT, **sem contato**. O contato profissional (WhatsApp, e-mail, endereço) vai numa cópia em `%USERPROFILE%\SoutoTreinador\privado\prescritor.json`, fora do repositório; o script usa a de lá primeiro |
| `receita-sono.json` | a fórmula do sono pronta (glicina, bisglicinato de magnésio e L-teanina, em sachê) |
| `Fundamentação - suplementação para o sono.md` | regras, doses, evidência, o que ficou de fora (valeriana, melatonina…) e fontes |

## Campos do JSON
- **`paciente`:** {`nome`, `nascimento`, `endereco`}. O que ficar em branco sai como linha para preencher à mão.
- **`data` e `local`:** saem em "Local e data", junto da assinatura.
- **`formulas[]`:** `uso`, `publico` e `forma` (a forma farmacêutica é o título: a RDC 67 proíbe nome de fórmula ou nome fantasia); `componentes[]` {`ativo` pela DCB, `detalhe`, `dose`} e `excipiente` {`nome`, `quantidade`}; `quantidade` (por extenso), `posologia` e `duracao`; `obs_farmacia`, `contraindicacoes` e `advertencias`.
- **`orientacoes[]`:** frases curtas, para o aluno.
- **`assinatura_digital`:** liga o espaço para a assinatura eletrônica do RT (ICP-Brasil ou gov.br).
- **`base_legal` e `fontes`:** as linhas do rodapé.

## Regras que o modelo já cumpre
- **Prescritor:** nome, CRN e contato profissional do RT (o contato vem da pasta privada).
- **Paciente:** nome e endereço.
- **Composição:** via e uso; ativos pela DCB, com a dose por unidade; forma farmacêutica; quantidade por extenso.
- **Uso:** posologia e duração.
- **Fechamento:** local e data, e assinatura e carimbo do RT (nome e CRN impressos embaixo da linha).
- **Sem:** nome de fórmula e logotipo de farmácia.
- **Envio:** a receita pode ir digitalizada ou com assinatura digital certificada, com confirmação de recebimento (Res. 656, parágrafo único-A).
- **No prontuário, fora da receita:** a justificativa de uso, o diagnóstico nutricional e a sintomatologia (Res. 656, art. 3º, XII).
- **Fitoterápico (quando o RT tiver a habilitação):** vai numa receita **separada**, nunca junto de aminoácido ou mineral (Res. 680/2021, art. 9º, II).
