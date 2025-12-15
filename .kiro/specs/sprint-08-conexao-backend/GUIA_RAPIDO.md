# ⚡ GUIA RÁPIDO - SPRINT 08

**Referência rápida para desenvolvedores**

---

## 🚀 INICIAR SERVIDOR

### Opção 1: Script Automático (Recomendado)
```powershell
.\START_SERVER_AQUI.ps1
```

### Opção 2: Manual
```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Verificar Status
```powershell
# Health check
curl http://localhost:8000/health

# Docs
# Abrir: http://localhost:8000/docs
```

---

## 🧪 EXECUTAR TESTES

### Todos os Testes
```powershell
cd backend

# Projects
.\venv\Scripts\python.exe test_projects_api.py

# Leads
.\venv\Scripts\python.exe test_leads_api.py

# Clients
.\venv\Scripts\python.exe test_clients_api.py

# Conversations
.\venv\Scripts\python.exe test_conversations_api.py

# Interviews
.\venv\Scripts\python.exe test_interviews_api.py

# Reports
.\venv\Scripts\python.exe test_reports_service.py
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### Backend
```
backend/
├── src/
│   ├── api/routes/          # Endpoints REST
│   │   ├── projects.py
│   │   ├── leads.py
│   │   ├── clients.py
│   │   ├── conversations.py
│   │   ├── interviews.py
│   │   └── reports.py
│   │
│   ├── services/            # Lógica de negócio
│   │   ├── project_service.py
│   │   ├── lead_service.py
│   │   ├── client_service.py
│   │   ├── conversation_service.py
│   │   ├── interview_service.py
│   │   └── report_service.py
│   │
│   └── main.py              # Entry point
│
└── test_*.py                # Scripts de validação
```

### Frontend
```
src/
├── services/                # API calls
│   ├── projectService.ts
│   ├── leadService.ts
│   ├── clientService.ts
│   ├── conversationService.ts
│   ├── interviewService.ts
│   └── reportService.ts
│
├── types/                   # TypeScript types
│   ├── project.ts
│   ├── lead.ts
│   ├── client.ts
│   ├── conversation.ts
│   ├── interview.ts
│   └── report.ts
│
└── pages/                   # Páginas React
    └── dashboard/
        ├── AdminProjectsPage.tsx
        ├── AdminLeadsPageNew.tsx
        └── ...
```

---

## 🔗 ENDPOINTS PRINCIPAIS

### Projects
```
GET    /api/projects          # Listar
POST   /api/projects          # Criar
GET    /api/projects/{id}     # Detalhes
PUT    /api/projects/{id}     # Atualizar
DELETE /api/projects/{id}     # Deletar
```

### Leads
```
GET    /api/leads             # Listar
POST   /api/leads             # Criar
GET    /api/leads/{id}        # Detalhes
PUT    /api/leads/{id}        # Atualizar
DELETE /api/leads/{id}        # Deletar
POST   /api/leads/{id}/convert # Converter para cliente
```

### Clients
```
GET    /api/clients           # Listar
POST   /api/clients           # Criar
GET    /api/clients/{id}      # Detalhes
PUT    /api/clients/{id}      # Atualizar
DELETE /api/clients/{id}      # Deletar
```

### Conversations
```
GET    /api/conversations     # Listar
POST   /api/conversations     # Criar
GET    /api/conversations/{id} # Detalhes
POST   /api/conversations/{id}/messages # Enviar mensagem
GET    /api/conversations/{id}/messages # Listar mensagens
```

### Interviews
```
GET    /api/interviews        # Listar
POST   /api/interviews        # Criar
GET    /api/interviews/{id}   # Detalhes
PUT    /api/interviews/{id}   # Atualizar
POST   /api/interviews/{id}/messages # Enviar mensagem
GET    /api/interviews/{id}/messages # Listar mensagens
```

### Reports
```
GET    /api/reports/overview      # Métricas gerais
GET    /api/reports/agents        # Performance de agentes
GET    /api/reports/conversions   # Funil de conversão
GET    /api/reports/export        # Exportar dados
```

---

## 🐛 TROUBLESHOOTING

### Servidor não inicia

**Problema:** Porta 8000 ocupada
```powershell
# Verificar processo
netstat -ano | findstr :8000

# Matar processo
taskkill /PID <PID> /F
```

**Problema:** Dependências faltando
```powershell
cd backend
.\venv\Scripts\pip.exe install -r requirements.txt
```

**Problema:** Ambiente virtual errado
```powershell
# Usar sempre: backend/venv
cd backend
.\venv\Scripts\python.exe -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Testes falhando

**Problema:** Token expirado
```powershell
# Gerar novo token
cd backend
.\venv\Scripts\python.exe generate_test_token.py
```

**Problema:** Supabase desconectado
```powershell
# Verificar credenciais em:
# docs/SUPABASE_CREDENTIALS.md
```

### Erro de encoding

**Problema:** `UnicodeEncodeError`
```
Solução: Remover emojis do código Python
```

---

## 📊 DADOS DE TESTE

### Criar Projeto
```json
POST /api/projects
{
  "name": "Projeto Teste",
  "description": "Descrição do projeto",
  "type": "survey",
  "status": "active",
  "client_id": "uuid-do-cliente"
}
```

### Criar Lead
```json
POST /api/leads
{
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "+5511999999999",
  "status": "new",
  "stage": "contact",
  "client_id": "uuid-do-cliente"
}
```

### Criar Cliente
```json
POST /api/clients
{
  "company_name": "Empresa Teste",
  "cnpj": "12345678000190",
  "plan": "pro",
  "status": "active",
  "contact_info": {
    "name": "João Silva",
    "email": "contato@empresa.com",
    "phone": "+5511999999999"
  }
}
```

---

## 🔍 VERIFICAÇÕES RÁPIDAS

### Backend Funcionando?
```powershell
curl http://localhost:8000/health
# Esperado: {"status":"healthy",...}
```

### Supabase Conectado?
```powershell
cd backend
.\venv\Scripts\python.exe -c "from src.config.supabase import supabase_admin; print('OK' if supabase_admin else 'ERRO')"
```

### Tabelas Existem?
```powershell
cd backend
.\venv\Scripts\python.exe -c "from src.config.supabase import supabase_admin; result = supabase_admin.table('projects').select('*').limit(1).execute(); print('OK' if result.data is not None else 'ERRO')"
```

---

## 📝 COMANDOS ÚTEIS

### Listar Jobs PowerShell
```powershell
Get-Job
```

### Ver Output de Job
```powershell
Receive-Job -Id <ID> -Keep
```

### Parar Job
```powershell
Stop-Job -Id <ID>
Remove-Job -Id <ID>
```

### Verificar Porta
```powershell
netstat -ano | findstr :8000
```

### Logs do Servidor
```powershell
# Ver últimas 50 linhas
Receive-Job -Id <ID> -Keep | Select-Object -Last 50
```

---

## 🎯 CHECKLIST DE VALIDAÇÃO

### Antes de Marcar Task como Completa

- [ ] Código implementado
- [ ] Testes criados
- [ ] Testes passando (100%)
- [ ] Dados persistindo no Supabase
- [ ] Error handling implementado
- [ ] Loading states implementados
- [ ] TypeScript sem erros
- [ ] Documentação atualizada

### Antes de Fazer Deploy

- [ ] Todos os testes passando
- [ ] Servidor iniciando sem erros
- [ ] Supabase conectado
- [ ] RLS habilitado
- [ ] Variáveis de ambiente configuradas
- [ ] Logs sem erros críticos
- [ ] Performance aceitável (<500ms)

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **Relatório Completo:** `RELATORIO_EXECUCAO.md`
- **Resumo Executivo:** `RESUMO_EXECUTIVO.md`
- **Estatísticas:** `ESTATISTICAS.md`
- **Tasks:** `tasks.md`

---

## 🆘 SUPORTE

### Problemas Comuns

1. **Servidor não inicia**
   - Verificar porta 8000
   - Verificar ambiente virtual
   - Verificar dependências

2. **Testes falhando**
   - Verificar token
   - Verificar Supabase
   - Verificar dados de teste

3. **Erro de encoding**
   - Remover emojis
   - Usar ASCII apenas

### Contatos

- **Documentação:** `.kiro/specs/sprint-08-conexao-backend/`
- **Logs:** `backend/logs/`
- **Supabase:** `docs/SUPABASE_CREDENTIALS.md`

---

**Atualizado em:** 06/12/2025  
**Versão:** 1.0
