# 🗂️ RENUM - Arquitetura e Estrutura

## Stack Técnica

### Backend
- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Validação:** Pydantic
- **ORM:** Supabase Client (PostgreSQL)
- **Filas:** Celery + Redis
- **IA:** LangChain + LangGraph
- **WhatsApp:** API a ser definida por projeto

### Banco de Dados
- **SGBD:** PostgreSQL (via Supabase)
- **Versão:** 15+
- **Features:** RLS, Triggers, Functions, Policies

### Infraestrutura
- **Hospedagem:** VPS
- **Proxy:** Nginx
- **Process Manager:** Systemd / Supervisor
- **Monitoramento:** Logs + Sentry (futuro)

---

## 📂 Estrutura de Pastas

```
renum-backend/
├── .kiro/
│   └── steering/              # Documentação de contexto para IA
│       ├── product.md
│       ├── structure.md
│       ├── tech.md
│       ├── integration-standard.md
│       └── policy-artifacts.md
│
├── docs/
│   ├── SUPABASE_ACCESS.md     # Guia de acesso ao banco
│   ├── SUPABASE_CREDENTIALS.md # Credenciais (NÃO COMMITAR)
│   └── VPS_ACCESS.md          # Guia de acesso à VPS
│
├── src/
│   ├── api/                   # Endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── clients.py
│   │   │   ├── leads.py
│   │   │   ├── interviews.py
│   │   │   ├── conversations.py
│   │   │   ├── projects.py
│   │   │   └── webhooks.py
│   │   └── dependencies.py
│   │
│   ├── services/              # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── agent_service.py   # Orquestração LangGraph
│   │   ├── interview_service.py
│   │   ├── notification_service.py
│   │   ├── whatsapp_service.py
│   │   └── analytics_service.py
│   │
│   ├── models/                # Modelos Pydantic
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   ├── interview.py
│   │   ├── conversation.py
│   │   └── renus_config.py
│   │
│   ├── workers/               # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── message_tasks.py
│   │   ├── interview_tasks.py
│   │   └── notification_tasks.py
│   │
│   ├── utils/                 # Utilitários
│   │   ├── __init__.py
│   │   ├── supabase_client.py
│   │   ├── redis_client.py
│   │   ├── logger.py
│   │   └── validators.py
│   │
│   ├── config.py              # Configurações
│   └── main.py                # Entry point FastAPI
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── migrations/                # Migrations SQL (Supabase)
│   └── *.sql
│
├── .env                       # Variáveis de ambiente (NÃO COMMITAR)
├── .env.example               # Template de variáveis
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🗄️ Arquitetura do Banco de Dados

### Tabelas Principais (12 tabelas)

#### 1. `profiles`
Usuários do sistema (admins, clientes)
```sql
- id (uuid, PK)
- email (text, unique)
- full_name (text)
- role (enum: admin, client)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 2. `clients`
Empresas que compram agentes
```sql
- id (uuid, PK)
- profile_id (uuid, FK → profiles)
- company_name (text)
- cnpj (text)
- plan (enum: basic, pro, enterprise)
- status (enum: active, inactive, suspended)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 3. `leads`
Contatos dos clientes (usuários finais)
```sql
- id (uuid, PK)
- client_id (uuid, FK → clients)
- phone (text)
- name (text)
- email (text, nullable)
- metadata (jsonb)
- status (enum: active, inactive, blocked)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 4. `interviews`
Metadados de pesquisas/entrevistas
```sql
- id (uuid, PK)
- lead_id (uuid, FK → leads)
- project_id (uuid, FK → projects)
- status (enum: pending, in_progress, completed, cancelled)
- started_at (timestamp)
- completed_at (timestamp, nullable)
- metadata (jsonb)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 5. `interview_messages` ⚠️ CRÍTICO
Mensagens individuais das entrevistas (1:N com interviews)
```sql
- id (uuid, PK)
- interview_id (uuid, FK → interviews)
- role (enum: user, assistant, system)
- content (text)
- metadata (jsonb)
- timestamp (timestamp)
- created_at (timestamp)
```

**MOTIVO DA SEPARAÇÃO:**
- Performance: 1000+ entrevistas ativas = 100.000+ mensagens
- Queries otimizadas: buscar metadados sem carregar mensagens
- Escalabilidade: particionamento futuro por data

#### 6. `projects`
Projetos/campanhas dos clientes
```sql
- id (uuid, PK)
- client_id (uuid, FK → clients)
- name (text)
- description (text)
- type (enum: survey, campaign, support)
- status (enum: draft, active, paused, completed)
- config (jsonb)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 7. `conversations`
Conversas gerais (não-entrevistas)
```sql
- id (uuid, PK)
- lead_id (uuid, FK → leads)
- client_id (uuid, FK → clients)
- status (enum: open, closed)
- last_message_at (timestamp)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 8. `messages`
Mensagens de conversas gerais
```sql
- id (uuid, PK)
- conversation_id (uuid, FK → conversations)
- role (enum: user, assistant, system)
- content (text)
- channel (enum: whatsapp, sms, email)
- metadata (jsonb)
- timestamp (timestamp)
- created_at (timestamp)
```

#### 9. `renus_config`
Configurações dos agentes por cliente
```sql
- id (uuid, PK)
- client_id (uuid, FK → clients)
- agent_type (enum: renus_base, mmn, vereador, clinica)
- config (jsonb)
- prompts (jsonb)
- active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 10. `tools`
Ferramentas disponíveis para agentes
```sql
- id (uuid, PK)
- name (text)
- description (text)
- function_name (text)
- parameters_schema (jsonb)
- active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 11. `sub_agents`
Sub-agentes especializados
```sql
- id (uuid, PK)
- name (text)
- type (enum: mmn, vereador, clinica, custom)
- description (text)
- config (jsonb)
- tools (jsonb) # IDs das tools disponíveis
- active (boolean)
- created_at (timestamp)
- updated_at (timestamp)
```

#### 12. `isa_commands`
Comandos administrativos executados
```sql
- id (uuid, PK)
- admin_id (uuid, FK → profiles)
- command (text)
- target_type (enum: client, lead, interview, conversation)
- target_id (uuid)
- result (jsonb)
- executed_at (timestamp)
- created_at (timestamp)
```

---

## 🔄 Fluxos Críticos

### 1. Fluxo de Pesquisa/Entrevista

```
Cliente cria projeto
    ↓
Sistema cria interviews para leads
    ↓
Celery task envia convites (WhatsApp)
    ↓
Lead responde → webhook WhatsApp
    ↓
FastAPI recebe mensagem
    ↓
LangGraph processa resposta
    ↓
Salva em interview_messages
    ↓
Verifica se entrevista completa
    ↓
Se completo: gera relatório + notifica cliente
```

### 2. Conversão Lead → Cliente

```
Lead conversa com agente
    ↓
Agente identifica interesse comercial
    ↓
Qualifica lead (perguntas específicas)
    ↓
Lead qualificado → cria registro em clients
    ↓
Cria projeto específico
    ↓
Agente muda contexto (relacionamento personalizado)
```

### 3. Sistema de Filas (Celery)

**Filas principais:**
- `high_priority`: Mensagens críticas (respostas de leads)
- `default`: Operações normais
- `low_priority`: Relatórios, analytics

**Workers:**
- `message_worker`: Processa envio de mensagens
- `interview_worker`: Processa lógica de entrevistas
- `notification_worker`: Envia notificações multi-canal

**Retry Policy:**
- Tentativas: 3x
- Backoff: exponencial (1s, 5s, 25s)
- Dead Letter Queue: mensagens falhadas vão para `failed_tasks`

### 4. Notificações Multi-canal

```
Evento dispara notificação
    ↓
Tenta WhatsApp
    ↓ (se falhar)
Tenta SMS
    ↓ (se falhar)
Envia Email
    ↓
Log completo em messages
```

---

## 🔒 Segurança (RLS - Row Level Security)

### Políticas por Tabela

**clients:**
- Admins: acesso total
- Clients: apenas seus próprios dados

**leads:**
- Admins: acesso total
- Clients: apenas leads do seu client_id

**interviews / interview_messages:**
- Admins: acesso total
- Clients: apenas entrevistas de seus leads

**conversations / messages:**
- Admins: acesso total
- Clients: apenas conversas de seus leads

**renus_config:**
- Admins: acesso total
- Clients: apenas suas configurações

---

## 📊 Índices Críticos

```sql
-- Performance em queries frequentes
CREATE INDEX idx_leads_client_id ON leads(client_id);
CREATE INDEX idx_leads_phone ON leads(phone);
CREATE INDEX idx_interviews_lead_id ON interviews(lead_id);
CREATE INDEX idx_interviews_status ON interviews(status);
CREATE INDEX idx_interview_messages_interview_id ON interview_messages(interview_id);
CREATE INDEX idx_interview_messages_timestamp ON interview_messages(timestamp);
CREATE INDEX idx_conversations_lead_id ON conversations(lead_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

---

## 🚀 Escalabilidade

### Estratégias Implementadas
1. **Tabela separada para mensagens:** `interview_messages`
2. **Índices otimizados:** queries rápidas mesmo com milhões de registros
3. **Filas assíncronas:** Celery processa operações pesadas
4. **Cache:** Redis para dados frequentes
5. **Paginação:** todas listagens com limit/offset

### Estratégias Futuras
1. **Particionamento:** `interview_messages` por data
2. **Read replicas:** queries de leitura em réplicas
3. **CDN:** assets estáticos
4. **Sharding:** separar clientes grandes em bancos dedicados

---

## 🧪 Testes

### Estrutura
```
tests/
├── unit/                    # Testes unitários
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Testes de integração
│   ├── test_api.py
│   ├── test_celery.py
│   └── test_supabase.py
└── conftest.py             # Fixtures compartilhadas
```

### Cobertura Mínima
- Unit tests: 80%
- Integration tests: 60%
- Total: 70%

---

**Última atualização:** 2025-11-25  
**Versão:** 1.0  
**Responsável:** Equipe RENUM
