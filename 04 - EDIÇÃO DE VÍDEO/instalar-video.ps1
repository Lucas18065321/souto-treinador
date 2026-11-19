# Instalador do motor de vídeo (SOUTO TREINADOR) no Windows 10/11.
# Pode rodar quantas vezes quiser: o que já está certo é pulado.
#
# Uso: duplo clique em INSTALAR-VIDEO.bat (nesta pasta), ou no PowerShell:
#   powershell -ExecutionPolicy Bypass -File ".\instalar-video.ps1" [-SemPerguntas] [-SemWhisperGrande] [-SemDeepFilter]
#   -SemPerguntas      não abre o Bloco de Notas nem espera Enter (para o Claude rodar)
#   -SemWhisperGrande  não baixa o modelo grande do Whisper (574 MB; só a transcrição de alta qualidade usa)
#   -SemDeepFilter     não baixa o DeepFilterNet (27 MB; só o estúdio de áudio usa)
param([switch]$SemPerguntas, [switch]$SemWhisperGrande, [switch]$SemDeepFilter)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$RAIZ = Split-Path -Parent $MyInvocation.MyCommand.Path          # ...\04 - EDIÇÃO DE VÍDEO
$REPO = Split-Path -Parent $RAIZ                                  # ...\souto-treinador
$MOTOR = Join-Path $RAIZ 'motor'
$resultado = New-Object System.Collections.ArrayList

function Passo($t) { Write-Host ''; Write-Host "==> $t" -ForegroundColor Cyan }
function Nota($item, $ok, $detalhe) {
	[void]$resultado.Add([pscustomobject]@{Item = $item; Status = $(if ($ok) { 'OK' } else { 'FALTA' }); Detalhe = $detalhe})
	$cor = if ($ok) { 'Green' } else { 'Yellow' }
	Write-Host ("   [{0}] {1} {2}" -f $(if ($ok) { 'ok' } else { '!!' }), $item, $detalhe) -ForegroundColor $cor
}
function AtualizarPath { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }
function Tem($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Sha($arq) { (Get-FileHash $arq -Algorithm SHA256).Hash.ToLower() }

Write-Host "Motor de vídeo: $RAIZ" -ForegroundColor White
if ($RAIZ -match 'OneDrive') {
	Write-Host '   ATENÇÃO: o repositório está dentro do OneDrive. Funciona, mas os ~500 MB do node_modules vão sincronizar.' -ForegroundColor Yellow
	Write-Host '   O ideal é clonar em C:\Users\<você>\souto-treinador (fora do OneDrive). Veja o guia 04-video, passo 2.' -ForegroundColor Yellow
}

# 1. Programas (winget) ------------------------------------------------------------------------------------------
Passo 'Programas (winget)'
$programas = @(
	@{id = 'Git.Git'; cmd = 'git'},
	@{id = 'OpenJS.NodeJS.LTS'; cmd = 'node'},
	@{id = 'Gyan.FFmpeg'; cmd = 'ffmpeg'},
	@{id = 'yt-dlp.yt-dlp'; cmd = 'yt-dlp'}
)
foreach ($p in $programas) {
	if (-not (Tem $p.cmd)) {
		& winget install --id $p.id -e --silent --accept-package-agreements --accept-source-agreements | Out-Host
		AtualizarPath
	}
	if (Tem $p.cmd) {
		$v = if ($p.cmd -eq 'ffmpeg') { (& ffmpeg -hide_banner -version 2>&1 | Select-Object -First 1) -as [string] } else { (& $p.cmd --version 2>&1 | Select-Object -First 1) -as [string] }
		Nota $p.cmd $true $v.Trim()
	} else { Nota $p.cmd $false 'não instalou: feche e abra o PowerShell e rode de novo' }
}
if (Tem 'node') {
	$major = [int]((& node --version) -replace '^v(\d+).*', '$1')
	Nota 'node >= 20' ($major -ge 20) "v$major (testado no 24)"
}

# 2. Pasta dos projetos (fora do repositório e do OneDrive) --------------------------------------------------------
Passo 'Pasta dos projetos (SOUTO_VIDEO_PROJETOS)'
$envArq = Join-Path $REPO '.env'
if (-not (Test-Path $envArq)) {
	$modelo = Join-Path $REPO '.env.example'
	if (Test-Path $modelo) { Copy-Item $modelo $envArq } else { New-Item -ItemType File $envArq | Out-Null }
}
$linha = Get-Content $envArq -Encoding UTF8 | Where-Object { $_ -match '^\s*SOUTO_VIDEO_PROJETOS\s*=\s*\S' } | Select-Object -First 1
$DADOS = if ($linha) { ($linha -split '=', 2)[1].Trim().Trim('"') } else { Join-Path $env:USERPROFILE 'Videos\Souto-Projetos' }
$DADOS = [Environment]::ExpandEnvironmentVariables($DADOS)
foreach ($d in @('', '_biblioteca\broll-reutilizavel', '_biblioteca\musicas', '_sistema\modelos', '_sistema\ferramentas', '_sistema\regressao', '_sistema\render-partes')) {
	New-Item -ItemType Directory -Force -Path (Join-Path $DADOS $d) | Out-Null
}
$cat = Join-Path $DADOS '_biblioteca\catalogo.json'
if (-not (Test-Path $cat)) { Set-Content -Path $cat -Value '[]' -Encoding UTF8 }
$catM = Join-Path $DADOS '_biblioteca\musicas\catalogo.md'
if (-not (Test-Path $catM)) { Set-Content -Path $catM -Value "# Músicas aprovadas`n`n| arquivo | mood | energia | duração | licença | link | usada em |`n|---|---|---|---|---|---|---|" -Encoding UTF8 }
$pil = Join-Path $DADOS '_sistema\regressao\pilotos.exemplo.json'
Copy-Item (Join-Path $MOTOR 'regressao.pilotos.exemplo.json') $pil -Force
Nota 'pasta de projetos' (Test-Path $DADOS) $DADOS

# 3. Pacotes do motor e navegador do Remotion ----------------------------------------------------------------------
Passo 'Pacotes do motor (npm ci) e navegador do Remotion'
Push-Location $MOTOR
if (-not (Test-Path 'node_modules\remotion')) { & npm ci --no-audit --no-fund | Out-Host }
& npx remotion browser ensure | Out-Host
$rv = (& node -e "console.log(require('remotion/package.json').version)") -as [string]
Pop-Location
Nota 'remotion' ($rv -eq '4.0.532') "versão $rv (testado na 4.0.532)"

# 4. Modelos do Whisper e DeepFilterNet (conferidos pelo sha256) ------------------------------------------------------
Passo 'Modelos do Whisper e DeepFilterNet'
$downloads = @(
	@{destino = '_sistema\modelos\ggml-small.bin'; url = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin'; sha = '1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b'; pular = $false},
	@{destino = '_sistema\modelos\ggml-large-v3-turbo-q5_0.bin'; url = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin'; sha = '394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2'; pular = [bool]$SemWhisperGrande},
	@{destino = '_sistema\ferramentas\deepfilternet\deep-filter.exe'; url = 'https://github.com/Rikorose/DeepFilterNet/releases/download/v0.5.6/deep-filter-0.5.6-x86_64-pc-windows-msvc.exe'; sha = '75e11fa16445f560cb6b021521ddb89e89270d13b83089705d98776f58fd7915'; pular = [bool]$SemDeepFilter}
)
foreach ($d in $downloads) {
	$dest = Join-Path $DADOS $d.destino
	if ($d.pular) { Nota (Split-Path $dest -Leaf) $true 'pulado (opção do instalador)'; continue }
	New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
	if (-not (Test-Path $dest) -or (Sha $dest) -ne $d.sha) {
		Write-Host "   baixando $($d.url)"
		Invoke-WebRequest -Uri $d.url -OutFile "$dest.baixando" -UseBasicParsing
		Move-Item -Force "$dest.baixando" $dest
	}
	$ok = (Sha $dest) -eq $d.sha
	Nota (Split-Path $dest -Leaf) $ok $(if ($ok) { 'sha256 confere' } else { 'sha256 DIFERENTE: apague o arquivo e rode de novo' })
}

# 5. SFX de compatibilidade (sons livres com os nomes que as peças esperam) -----------------------------------------
Passo 'Efeitos sonoros (SFX)'
Push-Location $MOTOR
& node scripts/sfx/sfx-substitutos.mjs | Out-Host
Pop-Location
$n = @(Get-ChildItem (Join-Path $RAIZ 'sfx\biblioteca\motionix') -Recurse -Filter *.wav -ErrorAction SilentlyContinue).Count
Nota 'SFX das peças' ($n -ge 77) "$n de 77 (sons CC0 + sintetizados)"
$nl = @(Get-ChildItem (Join-Path $RAIZ 'sfx\lab') -Recurse -Filter *.wav).Count
Nota 'SFX do lab' ($nl -ge 139) "$nl sons (133 Glitch Noises CC0 + 6 de papel; Mixkit/99Sounds você baixa: guia 04-video)"

# 6. Chaves de API (.env) ------------------------------------------------------------------------------------------
Passo 'Chaves de API (.env na raiz do repositório)'
if (-not $SemPerguntas) {
	Write-Host "   Abrindo $envArq no Bloco de Notas: cole PEXELS_API_KEY e PIXABAY_API_KEY, salve e feche." -ForegroundColor Yellow
	Start-Process notepad.exe $envArq -Wait
}
$txt = Get-Content $envArq -Encoding UTF8
foreach ($k in @('PEXELS_API_KEY', 'PIXABAY_API_KEY')) {
	$ok = [bool]($txt | Where-Object { $_ -match "^\s*$k\s*=\s*\S+" })
	Nota $k $ok $(if ($ok) { 'preenchida' } else { 'vazia: o banco de imagens/vídeos fica só com o Openverse' })
}

# 7. Conferência final ----------------------------------------------------------------------------------------------
Passo 'Conferência final'
if (Tem 'ffmpeg') {
	$filtros = (& ffmpeg -hide_banner -filters 2>&1) -join "`n"
	Nota 'ffmpeg: filtro whisper' ($filtros -match ' whisper ') 'transcrição local (precisa do FFmpeg 8 ou mais novo, build full)'
	Nota 'ffprobe' (Tem 'ffprobe') 'vem junto com o FFmpeg'
}
$dfn = Join-Path $DADOS '_sistema\ferramentas\deepfilternet\deep-filter.exe'
if (Test-Path $dfn) { $dv = (& $dfn --version 2>&1 | Select-Object -First 1) -as [string]; Nota 'deep-filter roda' ($dv -match '0\.5') $dv }
Nota 'Arial do sistema' (Test-Path "$env:WINDIR\Fonts\arial.ttf") 'usada nas folhas de quadros'
$chrome = @('C:\Program Files\Google\Chrome\Application\chrome.exe', 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe') | Where-Object { Test-Path $_ } | Select-Object -First 1
Nota 'Chrome ou Edge' ([bool]$chrome) 'usado só para capturar manchetes (capturar-manchete.mjs)'
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
Nota 'memória RAM' ($ram -ge 7) "$ram GB (com menos de 8 GB: um render por vez, sempre pela fila vez.mjs)"

Write-Host ''
$resultado | Format-Table -AutoSize | Out-Host
$falhas = @($resultado | Where-Object { $_.Status -ne 'OK' }).Count
if ($falhas -eq 0) { Write-Host 'TUDO PRONTO: o motor de vídeo está instalado.' -ForegroundColor Green }
else { Write-Host "$falhas item(ns) pendente(s) acima. Veja docs\guias\04-video.md, seção Problemas comuns." -ForegroundColor Yellow }
if (-not $SemPerguntas) { Read-Host 'Enter para fechar' | Out-Null }
exit $falhas
