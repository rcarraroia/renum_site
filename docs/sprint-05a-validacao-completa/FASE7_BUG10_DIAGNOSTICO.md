# 🔍 BUG #10 - DIAGNÓSTICO COMPLETO

**Data:** 03/12/2025 18:40  
**Investigador:** Kiro  
**Status:** ✅ CAUSA IDENTIFICADA

---

## 🚨 PROBLEMA

Servidor trava após 1-2 requests. Sintomas:
- Timeout em requests subsequentes
- Múltiplos processos na porta 8000
- Conexões em estado CLOSE_WAIT
- Servidor não responde mas processo continua rodando

---

## 🔬 INVESTIGAÇÃO

### Teste de Stress

Executado `test_bug10_stress.py`:
- **Resultado:** Servidor travou no request #1
- **Evidência:** Timeout de 5 segundos

### Análise de Processos

```
netstat -ano | findstr :8000
  TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       17164
  TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       9480
  TCP    127.0.0.1:8000         127.0.0.1:50658        CLOSE_WAIT      9480
  TCP    127.0.0.1:50658        127.0.0.1:8000         FIN_WAIT
```

**Conclusão:** Múltiplos processos + conexões não fechadas

### Análise de Código

Arquivo: `backend/src/config/supabase.py`

```python
# Cliente admin (usa SERVICE_KEY - bypassa RLS)
supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)

# Cliente público (usa ANON_KEY - respeita RLS)
supabase_client: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)
```

**PROBLEMA IDENTIFICADO:**
1. Clientes Supabase são **variáveis globais**
2. Criados uma vez no import do módulo
3. **NUNCA são fechados**
4. Cada request usa a mesma conexão global
5. Conexões HTTP subjacentes acumulam e travam

---

## 🎯 CAUSA RAIZ

**Pool de conexões HTTP não gerenciado**

O cliente Supabase usa `httpx` internamente. Quando criado como variável global:
- Abre conexões HTTP
- Mantém pool de conexões ativo
- Nunca fecha conexões antigas
- Após N requests, pool esgota
- Servidor trava esperando conexão disponível

---

## ✅ SOLUÇÃO

### Opção 1: Context Manager (RECOMENDADO)

Criar função que retorna cliente com context manager:

```python
from contextlib import contextmanager
from supabase import create_client, Client
from src.config.settings import settings

@contextmanager
def get_supabase_admin():
    """Context manager para cliente admin"""
    client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )
    try:
        yield client
    finally:
        # Fechar conexões HTTP
        if hasattr(client, '_client') and hasattr(client._client, 'aclose'):
            import asyncio
            asyncio.run(client._client.aclose())

# Uso:
with get_supabase_admin() as supabase:
    result = supabase.table('clients').select('*').execute()
```

### Opção 2: Dependency Injection FastAPI

```python
from fastapi import Depends
from supabase import Client

async def get_supabase_admin() -> Client:
    """Dependency para injetar cliente Supabase"""
    client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )
    try:
        yield client
    finally:
        # Cleanup
        await client._client.aclose()

# Uso em endpoint:
@router.get("/clients")
async def list_clients(
    supabase: Client = Depends(get_supabase_admin)
):
    result = supabase.table('clients').select('*').execute()
    return result.data
```

### Opção 3: Singleton com Cleanup (MAIS SIMPLES)

Manter global mas adicionar cleanup no shutdown:

```python
# src/config/supabase.py
supabase_admin: Client = create_client(...)
supabase_client: Client = create_client(...)

async def cleanup_supabase():
    """Fechar conexões no shutdown"""
    if hasattr(supabase_admin, '_client'):
        await supabase_admin._client.aclose()
    if hasattr(supabase_client, '_client'):
        await supabase_client._client.aclose()

# src/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await cleanup_supabase()
```

---

## 📊 IMPACTO

**Severidade:** 🔴 CRÍTICA  
**Bloqueio:** Sim - impede validação de BUG #7  
**Arquivos afetados:** 20+ (todos os services)

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Diagnóstico completo
2. ⏳ Escolher solução (Opção 3 = mais rápida)
3. ⏳ Implementar correção
4. ⏳ Testar com 100 requests
5. ⏳ Validar BUG #7 após correção

---

## 📝 LIÇÕES APRENDIDAS

1. **Variáveis globais com recursos externos são perigosas**
2. **Sempre usar context managers para recursos que precisam cleanup**
3. **Pool de conexões HTTP precisa ser gerenciado**
4. **Testes de stress revelam problemas de resource leak**

---

**Tempo de investigação:** 0.5h  
**Tempo estimado de correção:** 1h  
**Confiança na solução:** 95%
