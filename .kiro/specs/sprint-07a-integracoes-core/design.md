# Design Document - Sprint 07A: Integrações Core

## Overview

Este documento descreve a arquitetura técnica e decisões de design para o Sprint 07A do sistema RENUM. O objetivo é implementar um sistema robusto de integrações que permita aos agentes de IA se comunicarem com o mundo externo através de múltiplos canais (WhatsApp, Email) e acessarem dados de clientes (Supabase/Postgres).

### Objetivos Principais

1. **Integração WhatsApp (Uazapi)**: Envio e recebimento de mensagens via API Uazapi
2. **Integração Email (SMTP + SendGrid)**: Envio de emails via SMTP nativo ou SendGrid
3. **Integração Database**: Consulta a bancos de dados Supabase dos clientes
4. **Sistema de Triggers**: Automações baseadas em eventos (QUANDO → SE → ENTÃO)
5. **Processamento Assíncrono**: Celery + Redis para filas de mensagens
6. **LangChain Tools**: Ferramentas que agentes podem usar para executar ações

### Princípios de Design

- **Configuração Única**: Cliente configura integração 1 vez, todos os agentes herdam
- **Segurança First**: Credenciais criptografadas, RLS habilitado, validação de webhooks
- **Resiliência**: Retry automático, filas assíncronas, graceful degradation
- **Extensibilidade**: Fácil adicionar novos provedores (Evolution API, Twilio, etc)
- **Observabilidade**: Logs detalhados, auditoria completa, métricas de uso

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ IntegrationsTab  │  │   TriggersTab    │  │  Dashboard Stats │ │
│  │ (Config UI)      │  │ (Automation UI)  │  │  (Monitoring)    │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘ │
└───────────┼────────────────────┼────────────────────┼─────────────┘
            │                    │                    │
            │ HTTP + JWT         │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    API Routes                                 │  │
│  │  /api/integrations/*  /api/triggers/*  /webhooks/uazapi     │  │
│  └────────┬──────────────────┬──────────────────┬───────────────┘  │
│           │                  │                  │                   │
│  ┌────────▼─────────┐ ┌─────▼──────────┐ ┌────▼──────────────┐   │
│  │ Integration      │ │ Trigger        │ │ Webhook           │   │
│  │ Service          │ │ Service        │ │ Handler           │   │
│  └────────┬─────────┘ └─────┬──────────┘ └────┬──────────────┘   │
│           │                  │                  │                   │
│  ┌────────▼──────────────────▼──────────────────▼───────────────┐ │
│  │                    Celery Tasks                               │ │
│  │  send_whatsapp_task  send_email_task  trigger_scheduler     │ │
│  └────────┬──────────────────┬──────────────────┬───────────────┘ │
└───────────┼──────────────────┼──────────────────┼─────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         REDIS (Message Broker)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Message Queue│  │ Email Queue  │  │ Trigger Queue│             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Uazapi     │  │ SMTP/SendGrid│  │ Client       │             │
│  │   (WhatsApp) │  │   (Email)    │  │ Supabase DB  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPABASE (Database)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ integrations │  │   triggers   │  │trigger_exec  │             │
│  │ (configs)    │  │ (automations)│  │ (audit log)  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flows

#### Flow 1: Lead Sends WhatsApp Message

```
Lead (WhatsApp)
    │
    │ 1. Sends message
    ▼
Uazapi API
    │
    │ 2. POST /webhooks/uazapi
    ▼
FastAPI (Webhook Handler)
    │
    │ 3. Validate signature
    │ 4. Extract message data
    ▼
Discovery Agent
    │
    │ 5. Process message
    │ 6. Generate response
    ▼
WhatsAppTool (LangChain)
    │
    │ 7. Enqueue send_whatsapp_task
    ▼
Celery Worker
    │
    │ 8. POST /messages/send (Uazapi)
    ▼
Uazapi API
    │
    │ 9. Delivers message
    ▼
Lead (WhatsApp) - Receives response
```

#### Flow 2: ISA Sends Email Report

```
ISA Agent
    │
    │ 1. Decides to send email
    ▼
EmailTool (LangChain)
    │
    │ 2. Enqueue send_email_task
    ▼
Celery Worker
    │
    │ 3. Load SMTP/SendGrid config
    │ 4. Send email
    ▼
SMTP Server / SendGrid API
    │
    │ 5. Delivers email
    ▼
Recipient - Receives email
```

#### Flow 3: Agent Queries Client Database

```
Agent (RENUS/ISA/Discovery)
    │
    │ 1. Needs client data
    ▼
SupabaseQueryTool (LangChain)
    │
    │ 2. Load client DB credentials
    │ 3. Sanitize query
    ▼
Client Supabase Database
    │
    │ 4. Execute query
    │ 5. Return results
    ▼
Agent - Uses data in response
```

#### Flow 4: Trigger Executes Automation

```
Celery Beat Scheduler
    │
    │ 1. Every 1 minute
    ▼
trigger_scheduler_task
    │
    │ 2. Load active triggers
    │ 3. Evaluate conditions
    ▼
Trigger Evaluator
    │
    │ 4. Check: 3 days since last message?
    │ 5. Check: conversation status = open?
    ▼
Trigger Executor
    │
    │ 6. Execute action: send_message
    ▼
WhatsAppTool
    │
    │ 7. Send follow-up message
    ▼
Lead - Receives automated follow-up
```

## Components and Interfaces

### 1. Integration Service

**Responsibility:** Manage integration configurations (CRUD operations)

**Key Methods:**
```python
class IntegrationService:
    def create_integration(client_id: str, type: str, config: dict) -> Integration
    def get_integration(client_id: str, type: str) -> Integration
    def update_integration(integration_id: str, config: dict) -> Integration
    def delete_integration(integration_id: str) -> bool
    def test_connection(integration_id: str) -> TestResult
    def encrypt_credentials(credentials: dict) -> dict
    def decrypt_credentials(encrypted: dict) -> dict
```

**Dependencies:**
- Supabase client (database access)
- Encryption library (cryptography)
- Integration clients (Uazapi, SMTP, SendGrid)

### 2. Uazapi Client

**Responsibility:** Communicate with Uazapi WhatsApp API

**Key Methods:**
```python
class UazapiClient:
    def __init__(api_url: str, api_token: str, phone_number: str)
    async def send_message(phone: str, message: str) -> SendResult
    async def send_media(phone: str, media_url: str, caption: str) -> SendResult
    def validate_phone(phone: str) -> bool
    def validate_webhook_signature(payload: dict, signature: str) -> bool
```

**Configuration:**
- API URL: From integration config
- API Token: From integration config (encrypted)
- Phone Number ID: From integration config

### 3. Email Clients (SMTP + SendGrid)

**SMTP Client:**
```python
class SMTPClient:
    def __init__(host: str, port: int, username: str, password: str, use_tls: bool)
    async def send_email(to: List[str], subject: str, body: str, cc: List[str]) -> SendResult
    async def test_connection() -> bool
```

**SendGrid Client:**
```python
class SendGridClient:
    def __init__(api_key: str, from_email: str)
    async def send_email(to: List[str], subject: str, body: str, cc: List[str]) -> SendResult
    async def test_connection() -> bool
```

### 4. Trigger Service

**Responsibility:** Manage triggers and execute automations

**Key Methods:**
```python
class TriggerService:
    def create_trigger(client_id: str, trigger_data: dict) -> Trigger
    def get_triggers(client_id: str, active_only: bool) -> List[Trigger]
    def update_trigger(trigger_id: str, trigger_data: dict) -> Trigger
    def toggle_trigger(trigger_id: str, active: bool) -> Trigger
    def delete_trigger(trigger_id: str) -> bool
    async def evaluate_trigger(trigger: Trigger) -> bool
    async def execute_trigger_action(trigger: Trigger) -> ExecutionResult
```

### 5. Celery Tasks

**Message Tasks:**
```python
@celery_app.task(bind=True, max_retries=3)
def send_whatsapp_message(self, client_id: str, phone: str, message: str):
    # Load integration config
    # Send via Uazapi
    # Log result
    pass

@celery_app.task(bind=True, max_retries=3)
def send_email(self, client_id: str, to: List[str], subject: str, body: str):
    # Load integration config
    # Send via SMTP/SendGrid
    # Log result
    pass
```

**Trigger Tasks:**
```python
@celery_app.task
def trigger_scheduler():
    # Load all active triggers
    # Evaluate each trigger
    # Execute actions for matched triggers
    pass
```


## Data Models

### Database Schema

#### Table: integrations

Stores integration configurations for WhatsApp, Email, and Database connections.

```sql
CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'whatsapp', 'email_smtp', 'email_sendgrid', 'database'
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'disconnected', -- 'connected', 'disconnected', 'error'
    config JSONB NOT NULL, -- Encrypted credentials and settings
    last_tested_at TIMESTAMP WITH TIME ZONE,
    last_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    UNIQUE(client_id, type)
);

-- RLS Policies
ALTER TABLE integrations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins have full access to integrations"
    ON integrations FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Clients can manage own integrations"
    ON integrations FOR ALL
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE profile_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX idx_integrations_client_id ON integrations(client_id);
CREATE INDEX idx_integrations_type ON integrations(type);
CREATE INDEX idx_integrations_status ON integrations(status);
```

**Config Structure Examples:**

WhatsApp (Uazapi):
```json
{
  "api_url": "https://api.uazapi.com/v1",
  "api_token": "encrypted_token_here",
  "phone_number": "+5511999999999",
  "webhook_secret": "encrypted_secret_here"
}
```

Email SMTP:
```json
{
  "host": "smtp.gmail.com",
  "port": 587,
  "username": "user@example.com",
  "password": "encrypted_password_here",
  "use_tls": true,
  "from_email": "noreply@renum.com.br"
}
```


Email SendGrid:
```json
{
  "api_key": "encrypted_key_here",
  "from_email": "noreply@renum.com.br",
  "from_name": "RENUM"
}
```

Database (Client Supabase):
```json
{
  "supabase_url": "https://client-project.supabase.co",
  "supabase_key": "encrypted_service_key_here",
  "read_only": true,
  "allowed_tables": ["distribuidores", "vendas", "produtos"]
}
```

#### Table: triggers

Stores automation triggers with WHEN → IF → THEN structure.

```sql
CREATE TABLE triggers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT true,
    
    -- WHEN (Trigger Event)
    trigger_type VARCHAR(50) NOT NULL, -- 'time_based', 'event_based', 'condition_based'
    trigger_config JSONB NOT NULL,
    
    -- IF (Condition)
    condition_type VARCHAR(50), -- 'field_equals', 'field_contains', 'time_elapsed', 'always'
    condition_config JSONB,
    
    -- THEN (Action)
    action_type VARCHAR(50) NOT NULL, -- 'send_message', 'send_email', 'call_tool', 'change_status'
    action_config JSONB NOT NULL,
    
    last_executed_at TIMESTAMP WITH TIME ZONE,
    execution_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- RLS Policies
ALTER TABLE triggers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins have full access to triggers"
    ON triggers FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Clients can manage own triggers"
    ON triggers FOR ALL
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE profile_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX idx_triggers_client_id ON triggers(client_id);
CREATE INDEX idx_triggers_active ON triggers(active);
CREATE INDEX idx_triggers_type ON triggers(trigger_type);
```


**Trigger Config Examples:**

Time-based trigger (3 days after last message):
```json
{
  "trigger_type": "time_based",
  "trigger_config": {
    "delay_days": 3,
    "reference_field": "conversations.last_message_at"
  },
  "condition_type": "field_equals",
  "condition_config": {
    "field": "conversations.status",
    "operator": "equals",
    "value": "open"
  },
  "action_type": "send_message",
  "action_config": {
    "channel": "whatsapp",
    "template_id": "follow_up_1",
    "message": "Olá! Notamos que faz 3 dias desde nossa última conversa. Posso ajudar em algo?"
  }
}
```

Event-based trigger (intent detected):
```json
{
  "trigger_type": "event_based",
  "trigger_config": {
    "event": "intent_detected",
    "intent_values": ["cancelamento", "reclamacao"]
  },
  "condition_type": "always",
  "condition_config": {},
  "action_type": "send_email",
  "action_config": {
    "to": ["sucesso@renum.com.br"],
    "subject": "Alerta: Cliente com intenção de cancelamento",
    "template_id": "alert_critical_intent"
  }
}
```

#### Table: trigger_executions

Audit log of trigger executions for monitoring and debugging.

```sql
CREATE TABLE trigger_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trigger_id UUID NOT NULL REFERENCES triggers(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    condition_met BOOLEAN NOT NULL,
    action_executed BOOLEAN NOT NULL,
    
    result JSONB, -- Success/failure details
    error_message TEXT,
    execution_time_ms INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- RLS Policies
ALTER TABLE trigger_executions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins have full access to trigger executions"
    ON trigger_executions FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Clients can view own trigger executions"
    ON trigger_executions FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE profile_id = auth.uid()
        )
    );

-- Indexes
CREATE INDEX idx_trigger_executions_trigger_id ON trigger_executions(trigger_id);
CREATE INDEX idx_trigger_executions_client_id ON trigger_executions(client_id);
CREATE INDEX idx_trigger_executions_executed_at ON trigger_executions(executed_at DESC);
```


## API Contracts

### Integration Endpoints

#### POST /api/integrations/whatsapp/configure

Configure WhatsApp integration via Uazapi.

**Request:**
```json
{
  "api_url": "https://api.uazapi.com/v1",
  "api_token": "uazapi_token_here",
  "phone_number": "+5511999999999"
}
```

**Response (Success):**
```json
{
  "success": true,
  "integration": {
    "id": "uuid",
    "type": "whatsapp",
    "status": "connected",
    "created_at": "2025-12-04T10:30:00Z"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid API token",
  "error_code": "INVALID_CREDENTIALS"
}
```

#### GET /api/integrations/whatsapp/status

Get current WhatsApp integration status.

**Response:**
```json
{
  "success": true,
  "status": "connected",
  "last_tested_at": "2025-12-04T10:30:00Z",
  "phone_number": "+5511999999999",
  "messages_sent_today": 45,
  "rate_limit_remaining": 55
}
```

#### POST /api/integrations/whatsapp/send

Send WhatsApp message (used by agents via LangChain Tool).

**Request:**
```json
{
  "phone": "+5511999999999",
  "message": "Olá! Como posso ajudar?"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "msg_abc123",
  "sent_at": "2025-12-04T10:30:00Z"
}
```

#### POST /api/integrations/whatsapp/test

Test WhatsApp connection.

**Response:**
```json
{
  "success": true,
  "message": "Connection successful",
  "latency_ms": 245
}
```


#### POST /webhooks/uazapi

Receive incoming WhatsApp messages from Uazapi.

**Request (from Uazapi):**
```json
{
  "from": "+5511999999999",
  "message": "Olá, preciso de ajuda",
  "timestamp": "2025-12-04T10:30:00Z",
  "message_id": "msg_xyz789",
  "signature": "webhook_signature_here"
}
```

**Response:**
```json
{
  "success": true,
  "processed_at": "2025-12-04T10:30:01Z"
}
```

### Email Endpoints

#### POST /api/integrations/email/configure

Configure email integration (SMTP or SendGrid).

**Request (SMTP):**
```json
{
  "provider": "smtp",
  "host": "smtp.gmail.com",
  "port": 587,
  "username": "user@example.com",
  "password": "app_password_here",
  "use_tls": true,
  "from_email": "noreply@renum.com.br"
}
```

**Request (SendGrid):**
```json
{
  "provider": "sendgrid",
  "api_key": "SG.xxxxx",
  "from_email": "noreply@renum.com.br",
  "from_name": "RENUM"
}
```

**Response:**
```json
{
  "success": true,
  "integration": {
    "id": "uuid",
    "type": "email_smtp",
    "status": "connected"
  }
}
```

#### POST /api/integrations/email/send

Send email (used by agents via LangChain Tool).

**Request:**
```json
{
  "to": ["user@example.com"],
  "subject": "Relatório de Leads",
  "body": "<h1>Relatório</h1><p>Conteúdo aqui...</p>",
  "cc": ["admin@renum.com.br"]
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "email_abc123",
  "sent_at": "2025-12-04T10:30:00Z"
}
```


### Database Endpoints

#### POST /api/integrations/database/configure

Configure client's Supabase database connection.

**Request:**
```json
{
  "supabase_url": "https://client-project.supabase.co",
  "supabase_key": "service_role_key_here",
  "read_only": true,
  "allowed_tables": ["distribuidores", "vendas"]
}
```

**Response:**
```json
{
  "success": true,
  "integration": {
    "id": "uuid",
    "type": "database",
    "status": "connected",
    "read_only": true
  }
}
```

#### POST /api/integrations/database/test

Test database connection.

**Response:**
```json
{
  "success": true,
  "message": "Connection successful",
  "tables_found": ["distribuidores", "vendas", "produtos"],
  "latency_ms": 120
}
```

### Trigger Endpoints

#### POST /api/triggers

Create new trigger.

**Request:**
```json
{
  "name": "Follow-up de Inatividade",
  "description": "Envia mensagem após 3 dias sem resposta",
  "trigger_type": "time_based",
  "trigger_config": {
    "delay_days": 3,
    "reference_field": "conversations.last_message_at"
  },
  "condition_type": "field_equals",
  "condition_config": {
    "field": "conversations.status",
    "value": "open"
  },
  "action_type": "send_message",
  "action_config": {
    "channel": "whatsapp",
    "message": "Olá! Posso ajudar em algo?"
  }
}
```

**Response:**
```json
{
  "success": true,
  "trigger": {
    "id": "uuid",
    "name": "Follow-up de Inatividade",
    "active": true,
    "created_at": "2025-12-04T10:30:00Z"
  }
}
```

#### GET /api/triggers

List all triggers for client.

**Query Parameters:**
- `active`: boolean (optional) - Filter by active status

**Response:**
```json
{
  "success": true,
  "triggers": [
    {
      "id": "uuid",
      "name": "Follow-up de Inatividade",
      "active": true,
      "execution_count": 45,
      "last_executed_at": "2025-12-04T09:00:00Z"
    }
  ],
  "total": 1
}
```


#### GET /api/triggers/{id}

Get specific trigger details.

**Response:**
```json
{
  "success": true,
  "trigger": {
    "id": "uuid",
    "name": "Follow-up de Inatividade",
    "description": "Envia mensagem após 3 dias sem resposta",
    "active": true,
    "trigger_type": "time_based",
    "trigger_config": {...},
    "condition_type": "field_equals",
    "condition_config": {...},
    "action_type": "send_message",
    "action_config": {...},
    "execution_count": 45,
    "last_executed_at": "2025-12-04T09:00:00Z",
    "created_at": "2025-12-03T10:00:00Z"
  }
}
```

#### PUT /api/triggers/{id}

Update trigger configuration.

**Request:**
```json
{
  "name": "Follow-up de Inatividade (Atualizado)",
  "active": true,
  "action_config": {
    "channel": "whatsapp",
    "message": "Nova mensagem de follow-up"
  }
}
```

**Response:**
```json
{
  "success": true,
  "trigger": {
    "id": "uuid",
    "name": "Follow-up de Inatividade (Atualizado)",
    "updated_at": "2025-12-04T10:30:00Z"
  }
}
```

#### PATCH /api/triggers/{id}/toggle

Toggle trigger active status.

**Request:**
```json
{
  "active": false
}
```

**Response:**
```json
{
  "success": true,
  "trigger": {
    "id": "uuid",
    "active": false
  }
}
```

#### DELETE /api/triggers/{id}

Delete trigger.

**Response:**
```json
{
  "success": true,
  "message": "Trigger deleted successfully"
}
```

#### POST /api/triggers/{id}/test

Test trigger execution (simulate).

**Response:**
```json
{
  "success": true,
  "simulation": {
    "condition_met": true,
    "action_would_execute": true,
    "affected_conversations": 3,
    "estimated_messages": 3
  }
}
```


## Error Handling

### Error Response Format

All API errors follow this structure:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "details": {
    "field": "Additional context"
  },
  "timestamp": "2025-12-04T10:30:00Z"
}
```

### Error Codes

**Integration Errors:**
- `INVALID_CREDENTIALS`: API token/password is invalid
- `CONNECTION_FAILED`: Cannot connect to external service
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTEGRATION_NOT_FOUND`: Integration doesn't exist
- `INTEGRATION_DISABLED`: Integration is disabled

**Trigger Errors:**
- `TRIGGER_NOT_FOUND`: Trigger doesn't exist
- `INVALID_TRIGGER_CONFIG`: Trigger configuration is invalid
- `TRIGGER_EXECUTION_FAILED`: Trigger execution failed
- `CONDITION_EVALUATION_ERROR`: Error evaluating trigger condition

**Webhook Errors:**
- `INVALID_SIGNATURE`: Webhook signature validation failed
- `INVALID_PAYLOAD`: Webhook payload is malformed
- `PROCESSING_FAILED`: Error processing webhook

### Retry Strategy

**Celery Tasks:**
- Max retries: 3
- Backoff: Exponential (1s, 5s, 25s)
- Retry on: Connection errors, timeout errors, 5xx errors
- Don't retry on: 4xx errors (except 429 rate limit)

**External API Calls:**
- Timeout: 30 seconds
- Retry on: Connection timeout, 502, 503, 504
- Circuit breaker: After 5 consecutive failures, wait 60 seconds

### Logging

All operations are logged with:
- Timestamp
- Client ID
- Operation type
- Result (success/failure)
- Execution time
- Error details (if failed)

**Log Levels:**
- INFO: Successful operations
- WARNING: Retries, rate limits
- ERROR: Failed operations after all retries
- CRITICAL: System-level failures (Redis down, database unavailable)


## Testing Strategy

### Unit Tests

**Integration Service:**
- Test CRUD operations for integrations
- Test credential encryption/decryption
- Test connection validation logic
- Test RLS policy enforcement

**Uazapi Client:**
- Test message sending with valid/invalid phones
- Test webhook signature validation
- Test rate limiting logic
- Test error handling

**Email Clients:**
- Test SMTP connection and sending
- Test SendGrid API integration
- Test email validation
- Test retry logic

**Trigger Service:**
- Test trigger CRUD operations
- Test condition evaluation logic
- Test action execution
- Test trigger scheduling

### Integration Tests

**End-to-End Flows:**
1. Configure WhatsApp → Send message → Receive webhook → Process response
2. Configure Email → Send email → Verify delivery
3. Configure Database → Query data → Return results
4. Create Trigger → Wait for condition → Execute action

**API Tests:**
- Test all endpoints with valid/invalid inputs
- Test authentication and authorization
- Test rate limiting
- Test error responses

### Property-Based Tests

Not applicable for this sprint (integration-focused, not algorithm-focused).

### Manual Testing Checklist

**WhatsApp Integration:**
- [ ] Configure Uazapi credentials
- [ ] Test connection
- [ ] Send test message
- [ ] Receive webhook from Uazapi
- [ ] Verify message appears in conversation

**Email Integration:**
- [ ] Configure SMTP credentials
- [ ] Test connection
- [ ] Send test email
- [ ] Verify email received
- [ ] Test with SendGrid (if available)

**Database Integration:**
- [ ] Configure client Supabase credentials
- [ ] Test connection
- [ ] Query test data
- [ ] Verify results returned
- [ ] Test read-only enforcement

**Triggers:**
- [ ] Create time-based trigger
- [ ] Wait for condition to be met
- [ ] Verify action executed
- [ ] Check trigger_executions log
- [ ] Toggle trigger off/on

**Celery:**
- [ ] Start Celery worker
- [ ] Enqueue test task
- [ ] Verify task executed
- [ ] Check Redis queue
- [ ] Test retry on failure


## Security Considerations

### Credential Storage

**Encryption:**
- All sensitive fields (tokens, passwords, API keys) encrypted at rest
- Encryption algorithm: AES-256-GCM
- Encryption key stored in environment variable (not in database)
- Decryption only in memory, never exposed in API responses

**Access Control:**
- RLS enabled on all integration tables
- Clients can only access their own integrations
- Admins have full access for support purposes
- Service role key used for backend operations (bypasses RLS)

### Webhook Security

**Signature Validation:**
- All webhooks must include signature header
- Signature validated using shared secret
- Invalid signatures rejected with 401 Unauthorized
- Replay attacks prevented with timestamp validation

**Rate Limiting:**
- Webhooks limited to 1000 requests/minute per client
- Excessive requests return 429 Too Many Requests
- IP-based rate limiting for additional protection

### API Security

**Authentication:**
- All endpoints require JWT token
- Token includes client_id claim
- Token expiration: 30 minutes
- Refresh token mechanism for long sessions

**Authorization:**
- Client can only access own integrations/triggers
- Admin role required for cross-client operations
- Service endpoints (webhooks) use API key authentication

### Data Privacy

**PII Handling:**
- Phone numbers and emails stored encrypted
- Message content not stored (only metadata)
- Logs sanitized to remove PII
- LGPD compliance enforced

## Performance Considerations

### Caching

**Integration Configs:**
- Cached in Redis for 5 minutes
- Invalidated on update
- Reduces database load

**Trigger Evaluation:**
- Active triggers cached in memory
- Refreshed every minute
- Reduces query overhead

### Database Optimization

**Indexes:**
- All foreign keys indexed
- Status fields indexed for filtering
- Timestamp fields indexed for sorting
- Composite indexes for common queries

**Query Optimization:**
- Use SELECT specific columns (not *)
- Limit result sets with pagination
- Use EXPLAIN ANALYZE for slow queries
- Monitor query performance with pg_stat_statements

### Async Processing

**Celery Benefits:**
- Non-blocking API responses
- Horizontal scaling (add more workers)
- Automatic retry on failure
- Task prioritization (high/normal/low queues)

**Redis Performance:**
- In-memory broker (fast)
- Persistence enabled for durability
- Connection pooling
- Pub/sub for real-time updates


## Deployment Considerations

### Environment Variables

**Required:**
```bash
# Supabase
SUPABASE_URL=https://vhixvzaxswphwoymdhgg.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Encryption
ENCRYPTION_KEY=base64_encoded_32_byte_key_here

# API
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Uazapi (default, can be overridden per client)
UAZAPI_API_URL=https://api.uazapi.com/v1
UAZAPI_WEBHOOK_SECRET=shared_secret_here

# SMTP (default, can be overridden per client)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true

# SendGrid (optional)
SENDGRID_API_KEY=SG.xxxxx
```

### Service Dependencies

**Required Services:**
1. PostgreSQL (via Supabase) - Database
2. Redis - Message broker and cache
3. Celery Worker - Background task processing
4. Celery Beat - Scheduled task execution
5. FastAPI - Web server

**Service Start Order:**
1. Redis
2. PostgreSQL (Supabase)
3. FastAPI
4. Celery Worker
5. Celery Beat

### Systemd Services

**FastAPI:**
```ini
[Unit]
Description=RENUM FastAPI Server
After=network.target

[Service]
Type=simple
User=renum
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
ExecStart=/home/renum/backend/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Celery Worker:**
```ini
[Unit]
Description=RENUM Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=renum
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
ExecStart=/home/renum/backend/venv/bin/celery -A src.workers.celery_app worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

**Celery Beat:**
```ini
[Unit]
Description=RENUM Celery Beat Scheduler
After=network.target redis.service

[Service]
Type=simple
User=renum
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
ExecStart=/home/renum/backend/venv/bin/celery -A src.workers.celery_app beat --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```


## Monitoring and Observability

### Metrics to Track

**Integration Health:**
- Connection status (connected/disconnected/error)
- Last successful test timestamp
- Error rate (failures / total attempts)
- Average response time

**Message Delivery:**
- Messages sent per hour/day
- Delivery success rate
- Average delivery time
- Queue depth (pending messages)

**Trigger Performance:**
- Active triggers count
- Executions per hour
- Success rate
- Average execution time

**System Health:**
- Celery worker status
- Redis connection status
- Queue sizes
- Task processing rate

### Logging Strategy

**Structured Logging:**
```python
logger.info(
    "whatsapp_message_sent",
    extra={
        "client_id": client_id,
        "phone": phone,
        "message_id": message_id,
        "latency_ms": latency,
        "success": True
    }
)
```

**Log Aggregation:**
- Centralized logging (future: ELK stack or CloudWatch)
- Log retention: 30 days
- Error alerts via email/Slack

### Health Check Endpoints

**GET /health**
```json
{
  "status": "healthy",
  "services": {
    "database": "up",
    "redis": "up",
    "celery": "up"
  },
  "timestamp": "2025-12-04T10:30:00Z"
}
```

**GET /health/integrations**
```json
{
  "whatsapp": {
    "configured_clients": 5,
    "connected": 4,
    "errors": 1
  },
  "email": {
    "configured_clients": 3,
    "connected": 3,
    "errors": 0
  }
}
```

## Future Enhancements

### Phase 2 (Future Sprints)

1. **Additional Integrations:**
   - Slack notifications
   - Telegram bot
   - SMS via Twilio
   - Voice calls

2. **Advanced Triggers:**
   - Multi-condition triggers (AND/OR logic)
   - Trigger chains (one trigger activates another)
   - A/B testing for trigger messages
   - Machine learning-based trigger optimization

3. **Enhanced Monitoring:**
   - Real-time dashboard
   - Predictive alerts
   - Cost tracking per integration
   - Performance analytics

4. **Scalability:**
   - Multi-region deployment
   - Load balancing
   - Auto-scaling Celery workers
   - Database sharding

---

**Document Version:** 1.0  
**Created:** 2025-12-04  
**Status:** Draft - Awaiting Approval  
**Next Steps:** Create tasks.md with implementation plan
