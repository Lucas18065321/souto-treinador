# Guia 00 · Instalação geral do Sistema Souto Treinador

> Este é o primeiro guia. Siga na ordem, sem pular etapa. Cada motor tem o seu guia próprio (01 a 05), que começa onde este termina.
> Tempo estimado da instalação completa: **2 a 3 horas** (a maior parte é download).

---

## 1. O que você vai ter no final

| Motor | Pasta | Para que serve | Guia |
|---|---|---|---|
| Cérebro científico | `01 - BASE CIENTÍFICA` | Base de artigos de treino e nutrição, com Fichas e Protocolos. Tudo sai daqui: treino, roteiro, carrossel e vídeo | `01-base-cientifica.md` |
| Prescrição de treino | `05 - TREINO` | Ficha de treino, cargas por %1RM e RIR, volume load semanal e decisão de progressão | `06-treino.md` |
| Roteiros | `02 - ROTEIROS` | Roteiros de Reels e YouTube calibrados pela evidência | `02-roteiros.md` |
| Carrosséis | `03 - CARROSSÉIS E ARTE` | Carrosséis 1080×1350 na sua identidade azul, com editor visual | `03-carrossel.md` |
| Edição de vídeo | `04 - EDIÇÃO DE VÍDEO` | Motor de edição (Remotion) com 5 formatos, SFX e B-roll | `04-video.md` |
| Dieta e Painel ST | `06 - GESTÃO DA CONSULTORIA` | Prescrição de dieta (com o nutricionista RT), documento do aluno e o Painel ST no Supabase | `05-dieta-e-painel-st.md` |

Tudo é comandado pelo **Claude Code** (app Claude no computador). Você conversa em português e ele roda os motores.

---

## 2. Contas que você precisa criar (você mesmo, com e-mail e senha seus)

> Ninguém deve criar conta ou digitar senha por você. Guarde cada senha num gerenciador de senhas.

| Conta | Para quê | Onde criar | Custo |
|---|---|---|---|
| Claude (plano Pro ou Max) | Rodar o Claude Code | https://claude.ai | pago (Max recomendado para vídeo) |
| GitHub | Baixar e atualizar o sistema | https://github.com/signup | grátis |
| Supabase | Banco de dados do Painel ST | https://supabase.com/dashboard | grátis (plano Free) |
| Tally | Formulários de anamnese e check-in | https://tally.so | grátis |
| Pexels | Banco de fotos e vídeos grátis (API) | https://www.pexels.com/api/ | grátis |
| Pixabay | Banco de fotos, vídeos e sons (API) | https://pixabay.com/api/docs/ | grátis |
| Edison Scientific | Busca de artigos científicos com IA | https://platform.edisonscientific.com | grátis com limite mensal |
| Google (Gemini/Flow) **ou** Higgsfield | Geração de imagens | https://labs.google/flow · https://higgsfield.ai | varia |

---

## 3. Programas para instalar (na ordem)

Abra o **PowerShell** (tecla Windows → digite "PowerShell" → Enter). Cole um comando por vez e espere terminar.

### 3.1 Git
```powershell
winget install --id Git.Git -e
```
Feche e abra o PowerShell de novo. Confira:
```powershell
git --version
```

### 3.2 Python 3.12
```powershell
winget install --id Python.Python.3.12 -e
```
Confira (feche e abra o PowerShell antes):
```powershell
python --version
```
Se aparecer a Microsoft Store em vez da versão: Configurações → Aplicativos → Configurações avançadas de aplicativos → Aliases de execução → desligue "python.exe" e "python3.exe".

### 3.3 Node.js 24 (LTS)
```powershell
winget install --id OpenJS.NodeJS.LTS -e
```
```powershell
node --version
```

### 3.4 Google Chrome
Os carrosséis, os PDFs da dieta e o motor de vídeo usam o Chrome para desenhar as páginas.
```powershell
winget install --id Google.Chrome -e
```

### 3.5 FFmpeg (vídeo e áudio)
```powershell
winget install --id Gyan.FFmpeg -e
```
```powershell
ffmpeg -version
```

### 3.6 Poppler (ler PDFs dos artigos)
```powershell
winget install --id oschwartz10612.Poppler -e
```
```powershell
pdftotext -v
```

### 3.7 Claude (app do computador)
Baixe em https://claude.ai/download, instale e entre com a sua conta. Abra a aba **Code**.

---

## 4. Baixar o sistema (clonar o repositório)

```powershell
cd $env:USERPROFILE\Documents
```
```powershell
git clone https://github.com/Lucas18065321/souto-treinador.git
```
```powershell
cd souto-treinador
```

> **Não coloque a pasta dentro do OneDrive.** O motor de vídeo gera arquivos grandes e a sincronização trava os renders.

Para atualizar no futuro (quando sair versão nova):
```powershell
git pull
```

---

## 5. Pasta privada (fora do repositório)

Tudo o que é segredo ou dado de aluno fica em `%USERPROFILE%\SoutoTreinador\`, **nunca** dentro da pasta do repositório.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\SoutoTreinador\privado"
```
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\SoutoTreinador\Alunos"
```

| Arquivo | O que é | Quem fornece |
|---|---|---|
| `privado\assinatura-rt.png` | Assinatura do nutricionista Responsável Técnico (Lucas Melo) | o Lucas entrega por pen drive, nunca por e-mail ou chat |
| `privado\supabase.env` | Endereço e chave do Supabase | você copia do painel do Supabase (guia 05) |
| `%USERPROFILE%\.edison-key` | Chave da Edison Scientific | você copia do site da Edison (guia 01) |

---

## 6. Chaves de API (`.env`)

1. Na pasta do repositório, copie o modelo:
```powershell
Copy-Item .env.example .env
```
2. Abra o `.env` no Bloco de Notas:
```powershell
notepad .env
```
3. Cole cada chave depois do `=` (sem espaço e sem aspas). Como conseguir cada chave está no guia de cada motor.

> **Nunca** mande uma chave pelo chat do Claude, WhatsApp ou e-mail. Ela fica só no `.env`, e o `.env` nunca sobe para o GitHub (já está no `.gitignore`).

---

## 7. Conectores do Claude (o que ligar e por quê)

No app Claude: **Configurações → Conectores** (Settings → Connectors). Ligue só o que for usar.

| Conector | Obrigatório? | Para que o sistema usa | Como ligar |
|---|---|---|---|
| **Claude in Chrome** (extensão) | Recomendado | Gerar imagens no Gemini/Flow pelo navegador, conferir publicações, abrir o Painel ST | Instale a extensão "Claude" na Chrome Web Store, entre com a sua conta e autorize. Guia oficial: https://support.claude.com |
| **Google Drive** | Recomendado | Ler e salvar materiais (PDFs de alunos exportados, artes), compartilhar documentos | Conectores → Google Drive → Conectar → escolha a sua conta Google. Guia oficial: https://support.claude.com/en/articles/10166901-use-google-workspace-connectors |
| **Supabase (MCP)** | Recomendado | O Claude consulta o banco do Painel ST (ex.: "quais alunos não mandaram check-in?") | No PowerShell, dentro da pasta do repositório: `claude mcp add --transport http supabase "https://mcp.supabase.com/mcp?project_ref=SEU_PROJECT_REF&read_only=true"` e depois `/mcp` no Claude Code → Supabase → Authenticate. Guia oficial: https://supabase.com/docs/guides/getting-started/mcp |
| **Higgsfield (MCP)** | Opcional | Gerar imagens e vídeos curtos para carrossel e vídeo, direto pelo Claude | Veja o passo a passo no guia 03 (carrossel) |
| **Gmail / Google Calendar** | Opcional | Lembretes e agenda de consultas | Conectores → Gmail / Google Calendar |
| **GitHub** | Opcional | Já funciona pelo `git` instalado no item 3.1 | — |

> Dica de segurança: deixe o Supabase MCP em **somente leitura** (`read_only=true`). As gravações no banco são feitas pelo Painel ST, que tem confirmação em dois toques.

---

## 8. Primeira abertura no Claude Code

1. Abra o app Claude → aba **Code** → **Abrir pasta** → escolha `Documents\souto-treinador`.
2. Escreva: `Leia o CLAUDE.md e me diga se está tudo instalado.` O Claude confere os programas e as chaves e aponta o que falta.
3. Carregue o cérebro científico (uma vez só, cerca de 15 minutos):
```powershell
python "01 - BASE CIENTÍFICA/_MÁQUINA/scripts/baixar_colecao.py" --baixar
```
4. Instale o motor de vídeo: dois cliques em `04 - EDIÇÃO DE VÍDEO\INSTALAR-VIDEO.bat` (detalhes no guia 04).
5. Siga para o **guia 01 (Base científica)** e depois os outros, na ordem do sumário.

---

## 9. Problemas comuns na instalação

| Problema | Solução |
|---|---|
| `winget` não é reconhecido | Atualize o "Instalador de Aplicativo" na Microsoft Store |
| `python` abre a Microsoft Store | Desligue os aliases (item 3.2) |
| Comando funciona numa janela e não na outra | Feche **todas** as janelas do PowerShell e abra de novo (o PATH só atualiza assim) |
| `git clone` pede senha | O repositório é público: confira o endereço. Se ele tiver virado privado, peça acesso ao Lucas |
| Antivírus bloqueou o FFmpeg | Libere a pasta do FFmpeg no Windows Defender |
| Pasta dentro do OneDrive com ícone de nuvem | Mova o repositório para `Documents` fora do OneDrive (item 4) |
| "Permission denied" ao renomear pasta | Feche o Explorer e o Claude Code apontados para aquela pasta e tente de novo |

---

## 10. Suporte

- Primeiro: pergunte ao próprio Claude Code, dentro da pasta do sistema ("o painel não abre, o que faço?"). Ele lê os guias.
- Depois: o guia em PDF (`docs/Guia Souto Treinador.pdf`) tem o FAQ completo de cada motor.
- Ainda com dúvida: fale com o Lucas.
