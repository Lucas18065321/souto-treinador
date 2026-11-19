# Cria o atalho "Painel ST" na área de trabalho (ícone ST azul). Rode com o botão direito → "Executar com o PowerShell",
# ou no PowerShell:  powershell -ExecutionPolicy Bypass -File ".\criar_atalho.ps1"
# Com -Demo, cria também "Painel ST (demonstração)", que abre com os dados fictícios, sem Supabase.
param([switch]$Demo)

$ErrorActionPreference = "Stop"
$pasta = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $pasta "painel_st.py"
$icone = Join-Path $pasta "icone.ico"

# pythonw.exe: abre o painel sem a janela preta do console
$pythonw = $null
$cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if ($cmd) { $pythonw = $cmd.Source }
if (-not $pythonw) {
  $py = Get-Command py.exe -ErrorAction SilentlyContinue
  if ($py) {
    $exe = & $py.Source -3 -c "import sys; print(sys.executable)"
    $candidato = Join-Path (Split-Path -Parent $exe) "pythonw.exe"
    if (Test-Path $candidato) { $pythonw = $candidato }
  }
}
if (-not $pythonw) {
  Write-Host "Nao achei o Python (pythonw.exe). Instale o Python 3.12 em https://www.python.org/downloads/ marcando 'Add python.exe to PATH' e rode de novo." -ForegroundColor Red
  exit 1
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shell = New-Object -ComObject WScript.Shell

function Novo-Atalho([string]$nome, [string]$argumentos) {
  $lnk = $shell.CreateShortcut((Join-Path $desktop "$nome.lnk"))
  $lnk.TargetPath = $pythonw
  $lnk.Arguments = $argumentos
  $lnk.WorkingDirectory = $pasta
  $lnk.IconLocation = "$icone,0"
  $lnk.Description = "Painel da consultoria Souto Treinador"
  $lnk.Save()
  Write-Host "Atalho criado: $nome" -ForegroundColor Green
}

Novo-Atalho "Painel ST" "`"$script`" --app"
if ($Demo) { Novo-Atalho "Painel ST (demonstracao)" "`"$script`" --app --demo --porta 8788" }
Write-Host "Pronto. Use o atalho da area de trabalho. Para fixar na barra de tarefas: abra o painel, clique com o botao direito no icone da barra e escolha 'Fixar'."
