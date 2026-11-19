# Prévia: cada página do PDF vira PNG, pela API de PDF do próprio Windows (sem baixar nada). Rode com "powershell -MTA".
# Página que o leitor do Windows não consegue desenhar em 40 s é pulada e avisada (o PDF em si não muda).
param([string]$Pdf, [string]$OutDir, [int]$Largura = 1240, [string]$Paginas = "")
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$metodos = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asTaskOp = $metodos | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$asTaskAc = $metodos | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' } | Select-Object -First 1
function Esperar($op, [Type]$t) { $task = $asTaskOp.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait() | Out-Null; $task.Result }
function EsperarAcao($op, [int]$ms) { $task = $asTaskAc.Invoke($null, @($op)); return $task.Wait($ms) }
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFolder, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime] | Out-Null
$arq = Esperar ([Windows.Storage.StorageFile]::GetFileFromPathAsync((Resolve-Path -LiteralPath $Pdf).Path)) ([Windows.Storage.StorageFile])
$doc = Esperar ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($arq)) ([Windows.Data.Pdf.PdfDocument])
New-Item -ItemType Directory -Force $OutDir | Out-Null
$pasta = Esperar ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync((Resolve-Path -LiteralPath $OutDir).Path)) ([Windows.Storage.StorageFolder])
$lista = if ($Paginas) { $Paginas.Split(',') | ForEach-Object { [int]$_ - 1 } } else { 0..($doc.PageCount - 1) }
foreach ($i in $lista) {
  $pag = $doc.GetPage($i)
  $nome = 'pagina-{0:D2}.png' -f ($i + 1)
  $saida = Esperar ($pasta.CreateFileAsync($nome, [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) ([Windows.Storage.StorageFile])
  $fluxo = Esperar ($saida.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite)) ([Windows.Storage.Streams.IRandomAccessStream])
  $op = New-Object Windows.Data.Pdf.PdfPageRenderOptions
  $op.DestinationWidth = $Largura
  if (-not (EsperarAcao ($pag.RenderToStreamAsync($fluxo, $op)) 40000)) { Write-Output "AVISO: $nome não foi desenhada em 40 s (pulada)" }
  $fluxo.Dispose(); $pag.Dispose()
}
Write-Output "$($doc.PageCount) paginas"
