@echo off
echo ========================================
echo  RENUM - Iniciando Frontend (Local)
echo ========================================
echo.

echo Verificando se node_modules existe...
if not exist "node_modules" (
    echo Instalando dependências...
    npm install
)

echo.
echo Iniciando servidor de desenvolvimento...
echo URL: http://localhost:5173
echo.

npm run dev

pause