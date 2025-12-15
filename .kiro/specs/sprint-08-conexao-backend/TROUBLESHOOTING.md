# 🔧 Troubleshooting Guide - Sprint 08

## Problemas Comuns e Soluções

### 1. Servidor Backend Não Inicia

**Sintoma:** Erro ao executar `python -m src.main`

**Causas Possíveis:**
- Ambiente virtual errado
- Dependências não instaladas
- Porta 8000 ocupada
- Variáveis de ambiente faltando

**Solução:**
```powershell
# 1. Verificar ambiente virtual correto
cd backend
.\venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar porta
netstat -ano | findstr :8000

# 4. Usar script de inicialização
cd ..
.\START_SERVER_AQUI.ps1
```

---

### 2. UnicodeEncodeError (Emojis)

**Sintoma:** `UnicodeEncodeError: 'charmap' codec can't encode character`

**Causa:** Emojis em código Python no Windows

**Solução:**
- Remover emojis de arquivos `.py`
- Ou configurar encoding UTF-8 no terminal

---

### 3. Testes Falhando (Constraint Violation)

**Sintoma:** `check constraint violation` ao criar dados

**Causa:** Valores não permitidos pelo banco

**Solução:**
```python
# Verificar valores válidos no banco
from src.utils.supabase_client import get_client
supabase = get_client()

# Exemplo: verificar status válidos
result = supabase.table('leads').select('status').limit(5).execute()
valid_statuses = set([d['status'] for d in result.data if d['status']])
print('Valid statuses:', valid_statuses)
```

**Valores Conhecidos:**
- `leads.status`: 'novo'
- `leads.source`: 'pesquisa'
- `projects.type`: 'AI Native'
- `projects.status`: 'Em Andamento'
- `clients.segment`: 'test', 'Teste'
- `interviews.status`: 'in_progress', 'completed'
- `conversations.status`: 'active'

---

### 4. Método Não Encontrado em Service

**Sintoma:** `AttributeError: 'Service' object has no attribute 'method_name'`

**Causa:** Método não implementado no service

**Solução:**
1. Verificar se método existe no arquivo do service
2. Verificar imports corretos
3. Reiniciar servidor após adicionar método

---

### 5. Coluna Não Existe no Banco

**Sintoma:** `Could not find the 'column_name' column in the schema cache`

**Causa:** Schema do banco diferente do esperado

**Solução:**
```python
# Verificar colunas reais da tabela
from src.utils.supabase_client import get_client
supabase = get_client()

result = supabase.table('table_name').select('*').limit(1).execute()
if result.data:
    print('Columns:', list(result.data[0].keys()))
```

---

### 6. Frontend Não Conecta ao Backend

**Sintoma:** Erro CORS ou Network Error

**Causas:**
- Backend não está rodando
- URL incorreta no frontend
- CORS não configurado

**Solução:**
```powershell
# 1. Verificar backend rodando
curl http://localhost:8000/health

# 2. Verificar variável de ambiente no frontend
# Arquivo: .env
VITE_API_URL=http://localhost:8000

# 3. Verificar CORS no backend
# Arquivo: backend/.env
CORS_ORIGINS=http://localhost:5173
```

---

### 7. Testes de Performance Lentos

**Sintoma:** Testes excedendo targets de tempo

**Causas:**
- Conexão lenta com Supabase
- Muitos dados no banco
- Índices faltando

**Solução:**
```sql
-- Verificar índices
SELECT tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename;

-- Criar índices se necessário
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_projects_status ON projects(status);
```

---

### 8. Dados Não Persistem

**Sintoma:** Dados criados desaparecem

**Causas:**
- RLS bloqueando acesso
- Transação não commitada
- Service key não configurada

**Solução:**
```python
# Verificar RLS
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

# Usar service key para bypass RLS (apenas backend)
# Arquivo: backend/.env
SUPABASE_SERVICE_KEY=your_service_key_here
```

---

## Comandos Úteis

### Backend
```powershell
# Ativar ambiente virtual
cd backend
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python -m src.main

# Executar testes unitários
python test_projects_api.py
python test_leads_api.py
python test_clients_api.py

# Executar testes de integração
python test_integration_complete.py

# Executar testes de performance
python test_performance.py
```

### Frontend
```powershell
# Instalar dependências
npm install

# Iniciar dev server
npm run dev

# Build para produção
npm run build

# Verificar erros TypeScript
npm run type-check
```

### Banco de Dados
```sql
-- Verificar dados
SELECT COUNT(*) FROM projects;
SELECT COUNT(*) FROM leads;
SELECT COUNT(*) FROM clients;

-- Limpar dados de teste
DELETE FROM leads WHERE source = 'pesquisa' AND name LIKE 'Test%';
DELETE FROM projects WHERE name LIKE 'Integration Test%';
```

---

## Logs e Debugging

### Backend Logs
```powershell
# Ver logs do servidor
# Os logs aparecem no terminal onde o servidor está rodando

# Adicionar logging em código
import logging
logging.info("Debug message here")
```

### Frontend Logs
```javascript
// Console do navegador (F12)
console.log('Debug:', data);

// Network tab para ver requests
// F12 > Network > XHR
```

---

## Contatos de Suporte

**Documentação:**
- Sprint 08: `.kiro/specs/sprint-08-conexao-backend/`
- Supabase: `docs/SUPABASE_ACCESS.md`
- VPS: `docs/VPS_ACCESS.md`

**Arquivos Importantes:**
- `RESUMO_EXECUTIVO.md` - Overview do sprint
- `RELATORIO_EXECUCAO.md` - Problemas resolvidos
- `GUIA_RAPIDO.md` - Comandos rápidos
- `TROUBLESHOOTING.md` - Este arquivo

---

**Última atualização:** 06/12/2025  
**Versão:** 1.0
