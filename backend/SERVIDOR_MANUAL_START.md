# 🚀 Como Iniciar o Servidor Backend Manualmente

## ✅ Problema Resolvido

Todos os problemas de dependências foram corrigidos:
- ✅ `langchain_openai` instalado
- ✅ `aiosmtplib` instalado  
- ✅ `langgraph` instalado
- ✅ `langchain` instalado
- ✅ Conflitos de versão do `httpx` resolvidos

## 📋 Instruções para Iniciar o Servidor

### Opção 1: Usando PowerShell (Recomendado)

Abra um novo terminal PowerShell e execute:

```powershell
cd "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
.\venv\Scripts\python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Opção 2: Usando o Script Fixo

```powershell
cd "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
.\start_server_fixed.ps1
```

## ✅ Como Saber que Funcionou

Você verá mensagens como:

```
✅ LangSmith configured:
   Project: renum-backend
   Environment: development
   Tracing: true
==================================================
🚀 RENUM Backend Starting...
📍 Environment: Development
🌐 API Host: 0.0.0.0:8000
🔒 CORS Origins: [...]
==================================================
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🧪 Testar se Está Funcionando

Em outro terminal PowerShell, execute:

```powershell
cd "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
python test_interviews_api.py
```

Ou teste manualmente:

```powershell
curl http://localhost:8000/health
```

Deve retornar:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-06T...",
  "version": "1.0.0"
}
```

## ⚠️ Troubleshooting

### Erro: "porta 8000 já em uso"

```powershell
# Encontrar processo usando porta 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Matar processo (substitua PID pelo número retornado)
Stop-Process -Id PID -Force
```

### Erro: "ModuleNotFoundError"

Se aparecer erro de módulo faltando, instale:

```powershell
cd "E:\PROJETOS SITE\Projeto Renum\Projeto Site Renum\renum_site\backend"
.\venv\Scripts\pip.exe install [nome-do-modulo]
```

## 📊 Próximos Passos

Após o servidor iniciar com sucesso:

1. Execute os testes de validação:
   ```powershell
   python test_interviews_api.py
   ```

2. Kiro continuará com a validação do Sprint 08

---

**Criado em:** 06/12/2025  
**Status:** Pronto para uso  
**Dependências:** Todas instaladas ✅
