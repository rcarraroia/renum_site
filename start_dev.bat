@echo off
echo ========================================
echo  RENUM - Ambiente de Desenvolvimento
echo ========================================
echo.
echo Iniciando Backend e Frontend...
echo.

echo [1/2] Iniciando Backend...
start "RENUM Backend" cmd /k "cd /d %~dp0 && start_backend.bat"

timeout /t 3 /nobreak > nul

echo [2/2] Iniciando Frontend...
start "RENUM Frontend" cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo ✅ Ambiente iniciado!
echo.
echo URLs:
echo - Backend: http://127.0.0.1:8000
echo - Frontend: http://localhost:5173
echo - API Docs: http://127.0.0.1:8000/docs
echo.
echo Pressione qualquer tecla para fechar...
pause > nul