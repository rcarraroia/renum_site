# 📚 Documentação da API - RENUM

## Visão Geral

A API do RENUM é construída com FastAPI e fornece endpoints RESTful para gerenciar agentes, entrevistas, sub-agentes e configurações.

**Base URL:** `http://localhost:8000/api`

**Documentação Interativa:** `http://localhost:8000/docs` (Swagger UI)

---

## 🔐 Autenticação

Todos os endpoints (exceto públicos) requerem autenticação via JWT.

### Headers Obrigatórios

```http
Authorization: Bearer <token>
Content-Type: application/json
```

### Obter Token

```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@renum.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "admin@renum.com",
    "role": "admin"
  }
}
```

---

## 📋 Endpoints

### Sub-Agents

#### Listar Sub-Agentes
```http
GET /api/sub-agents
```

**Query Parameters:**
- `active_only` (boolean): Filtrar apenas ativos
- `agent_type` (string): Filtrar por tipo

**Response 200:**
```json
[
  {
    "id": "uuid",
    "name": "Discovery MMN",
    "description": "Agente de pesquisa para MMN",
    "type": "discovery",
    "channel": "whatsapp",
    "system_prompt": "Você é um pesquisador...",
    "model": "openai/gpt-4o-mini",
    "topics": ["Prospecção", "Atendimento"],
    "is_active": true,
    "slug": "discovery-mmn",
    "public_url": "http://localhost:5173/chat/discovery-mmn",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Criar Sub-Agente
```http
POST /api/sub-agents
Content-Type: application/json

{
  "name": "Novo Agente",
  "description": "Descrição do agente",
  "type": "custom",
  "channel": "whatsapp",
  "system_prompt": "Você é um assistente...",
  "model": "openai/gpt-4o-mini",
  "topics": ["Vendas", "Suporte"],
  "is_active": true
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "name": "Novo Agente",
  "slug": "novo-agente",
  "public_url": "http://localhost:5173/chat/novo-agente",
  ...
}
```

#### Atualizar Sub-Agente
```http
PUT /api/sub-agents/{id}
Content-Type: application/json

{
  "name": "Nome Atualizado",
  "is_active": false
}
```

**Response 200:** Objeto do sub-agente atualizado

#### Deletar Sub-Agente
```http
DELETE /api/sub-agents/{id}
```

**Response 204:** No Content

#### Toggle Status
```http
PATCH /api/sub-agents/{id}/toggle
```

**Response 200:** Objeto do sub-agente com status atualizado

#### Estatísticas
```http
GET /api/sub-agents/{id}/stats
```

**Response 200:**
```json
{
  "total_conversations": 150,
  "active_conversations": 12,
  "total_messages": 3420,
  "avg_response_time": 1.2,
  "satisfaction_rate": 0.87,
  "last_activity": "2024-01-01T12:00:00Z"
}
```

---

### Interviews

#### Listar Entrevistas
```http
GET /api/interviews
```

**Query Parameters:**
- `status` (string): pending, in_progress, completed, cancelled
- `limit` (int): Número de resultados (padrão: 50)
- `offset` (int): Paginação

**Response 200:**
```json
[
  {
    "id": "uuid",
    "lead_id": "uuid",
    "project_id": "uuid",
    "status": "completed",
    "started_at": "2024-01-01T10:00:00Z",
    "completed_at": "2024-01-01T10:15:00Z",
    "metadata": {
      "total_questions": 10,
      "completion_rate": 1.0
    }
  }
]
```

#### Criar Entrevista
```http
POST /api/interviews
Content-Type: application/json

{
  "lead_id": "uuid",
  "project_id": "uuid",
  "metadata": {}
}
```

**Response 201:** Objeto da entrevista criada

#### Obter Mensagens da Entrevista
```http
GET /api/interviews/{id}/messages
```

**Response 200:**
```json
[
  {
    "id": "uuid",
    "interview_id": "uuid",
    "role": "assistant",
    "content": "Olá! Vamos começar a entrevista...",
    "timestamp": "2024-01-01T10:00:00Z"
  },
  {
    "id": "uuid",
    "interview_id": "uuid",
    "role": "user",
    "content": "Sim, estou pronto!",
    "timestamp": "2024-01-01T10:00:30Z"
  }
]
```

#### Enviar Mensagem
```http
POST /api/interviews/{id}/messages
Content-Type: application/json

{
  "content": "Minha resposta aqui"
}
```

**Response 200:**
```json
{
  "user_message": {
    "id": "uuid",
    "content": "Minha resposta aqui",
    "timestamp": "2024-01-01T10:01:00Z"
  },
  "assistant_message": {
    "id": "uuid",
    "content": "Entendi. Próxima pergunta...",
    "timestamp": "2024-01-01T10:01:02Z"
  },
  "interview_status": "in_progress"
}
```

---

### RENUS Config

#### Obter Configuração
```http
GET /api/renus-config
```

**Response 200:**
```json
{
  "id": "uuid",
  "client_id": "uuid",
  "system_prompt": "Você é o RENUS...",
  "model": "openai/gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 4000,
  "guardrails": {
    "enabled": true,
    "blocked_words": ["palavra1", "palavra2"]
  },
  "tools_enabled": ["tool1", "tool2"]
}
```

#### Atualizar Configuração
```http
PUT /api/renus-config
Content-Type: application/json

{
  "system_prompt": "Novo prompt...",
  "temperature": 0.8
}
```

**Response 200:** Configuração atualizada

#### Atualizar Instruções
```http
PATCH /api/renus-config/instructions
Content-Type: application/json

{
  "system_prompt": "Novo prompt..."
}
```

**Response 200:** Configuração atualizada

---

### Tools

#### Listar Tools
```http
GET /api/tools
```

**Response 200:**
```json
[
  {
    "id": "uuid",
    "name": "Supabase Query",
    "description": "Execute queries on Supabase",
    "function_name": "supabase_query",
    "category": "database",
    "is_active": true,
    "parameters_schema": {
      "type": "object",
      "properties": {
        "table": {"type": "string"},
        "operation": {"type": "string"}
      }
    }
  }
]
```

#### Criar Tool (Admin)
```http
POST /api/tools
Content-Type: application/json

{
  "name": "Nova Tool",
  "description": "Descrição",
  "function_name": "nova_tool",
  "category": "custom",
  "parameters_schema": {}
}
```

**Response 201:** Tool criada

---

### ISA (Admin Only)

#### Chat com ISA
```http
POST /api/isa/chat
Content-Type: application/json

{
  "message": "Liste todos os clientes ativos"
}
```

**Response 200:**
```json
{
  "message": "Encontrei 15 clientes ativos...",
  "command_executed": true,
  "result": {
    "count": 15,
    "clients": [...]
  }
}
```

#### Histórico de Comandos
```http
GET /api/isa/history?limit=50
```

**Response 200:**
```json
[
  {
    "id": "uuid",
    "admin_id": "uuid",
    "command": "list clients",
    "target_type": "client",
    "result": {},
    "executed_at": "2024-01-01T10:00:00Z"
  }
]
```

---

### Public Chat

#### Chat Público (Sem Auth)
```http
POST /api/public-chat/{agent_slug}
Content-Type: application/json

{
  "message": "Olá!",
  "session_id": "optional-session-id"
}
```

**Response 200:**
```json
{
  "response": "Olá! Como posso ajudar?",
  "session_id": "uuid",
  "agent_name": "Discovery MMN"
}
```

---

## ❌ Códigos de Erro

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📊 Rate Limiting

- **Endpoints públicos:** 100 requests/minuto por IP
- **Endpoints autenticados:** 1000 requests/minuto por usuário
- **ISA chat:** 20 requests/minuto por admin

---

## 🔗 Links Úteis

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

**Última atualização:** 2024-01-01  
**Versão da API:** 1.0.0
