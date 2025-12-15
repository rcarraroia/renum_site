# Script para iniciar o servidor backend com ambiente virtual correto

# Caminho absoluto do projeto
$BackendPath = "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
$VenvPython = "$BackendPath\venv\Scripts\python.exe"

# Verificar se o ambiente virtual existe
if (-not (Test-Path $VenvPython)) {
    Write-Host "❌ Ambiente virtual não encontrado em: $VenvPython" -ForegroundColor Red
    Write-Host "Execute: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Mudar para o diretório do backend
Set-Location $BackendPath

# Iniciar servidor usando o Python do ambiente virtual
Write-Host "🚀 Iniciando servidor backend..." -ForegroundColor Green
Write-Host "📍 Usando Python: $VenvPython" -ForegroundColor Cyan
Write-Host "📂 Diretório: $BackendPath" -ForegroundColor Cyan
Write-Host ""

& $VenvPython -m uvicorn src.main:app --host 0.0.0.0 --port 8000
