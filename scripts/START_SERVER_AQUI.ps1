# ============================================================
# SCRIPT PARA INICIAR O SERVIDOR BACKEND
# Execute este arquivo clicando com botão direito > "Executar com PowerShell"
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INICIANDO SERVIDOR BACKEND - RENUM" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Caminho do projeto
$ProjectRoot = $PSScriptRoot
$BackendPath = Join-Path $ProjectRoot "backend"
$VenvPython = Join-Path $BackendPath "venv\Scripts\python.exe"

# Verificar se ambiente virtual existe
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "   Esperado em: $VenvPython" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Mudar para diretório backend
Set-Location $BackendPath

Write-Host "Diretorio: $BackendPath" -ForegroundColor Green
Write-Host "Python: $VenvPython" -ForegroundColor Green
Write-Host "Porta: 8000" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  SERVIDOR INICIANDO..." -ForegroundColor Cyan
Write-Host "  Pressione CTRL+C para parar" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar servidor
& $VenvPython -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Se chegou aqui, servidor foi parado
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  SERVIDOR PARADO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
