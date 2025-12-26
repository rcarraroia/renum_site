@echo off
echo ========================================
echo  RENUM - Iniciando Backend (Local)
echo ========================================
echo.

cd backend
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo Iniciando servidor FastAPI (Desenvolvimento Local)...
echo URL: http://127.0.0.1:8000
echo Docs: http://127.0.0.1:8000/docs
echo Health: http://127.0.0.1:8000/health
echo.

python -m src.main_local

pause