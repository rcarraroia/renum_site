@echo off
echo ========================================
echo TESTE COMPLETO DO ORQUESTRADOR
echo ========================================
echo.

echo 1. Verificando se backend esta rodando...
python scripts\quick_validate.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Validacao rapida passou!
    echo.
    echo 2. Executando validacao completa...
    python scripts\validate_orchestrator.py
) else (
    echo.
    echo ❌ Validacao rapida falhou!
    echo.
    echo Verifique se:
    echo - Backend esta rodando: cd backend ^&^& python -m src.main
    echo - Dependencias instaladas: pip install -r requirements.txt
    echo - Variaveis de ambiente configuradas (.env)
)

echo.
echo ========================================
echo TESTE CONCLUIDO
echo ========================================
pause