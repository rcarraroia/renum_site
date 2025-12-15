# Requirements Document - Sprint 07A: Integrações Core

## Introduction

Este documento define os requisitos para o Sprint 07A do sistema RENUM, focado na implementação das integrações core que permitirão aos agentes de IA se comunicarem com leads através de múltiplos canais (WhatsApp, Email) e acessarem dados externos (banco de dados do cliente). Adicionalmente, implementa um sistema de triggers/gatilhos para automações baseadas em eventos.

O objetivo principal é criar a infraestrutura de integrações que permitirá aos agentes RENUS, ISA e Discovery executarem ações no mundo real, transformando o sistema de um chatbot isolado em uma plataforma de automação completa.

## Glossary

- **RENUM System**: Sistema completo de agentes de IA para automação de negócios
- **Agent**: Agente de IA (RENUS, ISA, Discovery) que processa conversas e executa ações
- **Integration**: Conexão configurada com serviço externo (WhatsApp, Email, Database)
- **Client**: Empresa que contrata o sistema RENUM
- **Lead**: Usuário final que interage com os agentes via WhatsApp/Email
- **Trigger**: Gatilho automático baseado em eventos (QUANDO → SE → ENTÃO)
- **Uazapi**: Provedor de API WhatsApp Business escolhido para este projeto
- **LangChain Tool**: Ferramenta que agentes podem usar para executar ações
- **Celery**: Sistema de filas assíncronas para processamento em background
- **Redis**: Message broker usado pelo Celery
- **RLS**: Row Level Security - segurança em nível de linha no Supabase
- **Webhook**: Endpoint HTTP que recebe notificações de serviços externos
- **Rate Limiting**: Limitação de taxa de requisições para evitar sobrecarga

## Requirements

### Requirement 1: Integração WhatsApp via Uazapi

**User Story:** As a client, I want to configure WhatsApp integration once, so that all my agents can send and receive messages via WhatsApp without additional setup.

#### Acceptance Criteria

1. WHEN a client provides Uazapi credentials (API URL, API Token, Phone Number), THE RENUM System SHALL store them securely in the integrations table with encryption
2. WHEN a client tests the WhatsApp connection, THE RENUM System SHALL validate credentials by making a test API call to Uazapi and return success or error status
3. WHEN an agent needs to send a WhatsApp message, THE RENUM System SHALL use the stored Uazapi credentials to send the message via the Uazapi API
4. WHEN Uazapi receives a message from a lead, THE RENUM System SHALL receive the webhook notification and route it to the appropriate agent for processing
5. WHEN the Uazapi API returns a rate limit error, THE RENUM System SHALL queue the message for retry with exponential backoff

### Requirement 2: Integração Email (SMTP + SendGrid)

**User Story:** As a client, I want to configure email integration, so that my agents can send email notifications and reports to leads and team members.

#### Acceptance Criteria

1. WHEN a client provides SMTP credentials (host, port, username, password), THE RENUM System SHALL store them securely in the integrations table
2. WHERE a client has SendGrid API key, THE RENUM System SHALL support SendGrid as an alternative email provider
3. WHEN a client tests the email connection, THE RENUM System SHALL send a test email and return success or error status
4. WHEN an agent needs to send an email, THE RENUM System SHALL use the configured provider (SMTP or SendGrid) to deliver the message
5. WHEN email sending fails, THE RENUM System SHALL retry up to 3 times with exponential backoff before marking as failed

### Requirement 3: Integração Database do Cliente (Supabase/Postgres)

**User Story:** As a client, I want to connect my own Supabase database, so that agents can query my business data to provide personalized responses.

#### Acceptance Criteria

1. WHEN a client provides Supabase credentials (URL, Service Key), THE RENUM System SHALL store them securely in the integrations table
2. WHEN a client tests the database connection, THE RENUM System SHALL execute a simple query (SELECT 1) and return success or error status
3. WHEN an agent needs to query client data, THE RENUM System SHALL use the stored credentials to execute read-only queries by default
4. WHERE a client explicitly enables write permissions, THE RENUM System SHALL allow agents to execute INSERT, UPDATE, DELETE operations
5. WHEN executing queries on client database, THE RENUM System SHALL sanitize all inputs to prevent SQL injection attacks

### Requirement 4: Sistema de Triggers/Gatilhos

**User Story:** As a client, I want to create automated triggers, so that the system can execute actions automatically based on events and conditions without manual intervention.

#### Acceptance Criteria

1. WHEN a client creates a trigger with WHEN (event), IF (condition), THEN (action) structure, THE RENUM System SHALL store it in the triggers table with active status
2. WHILE a trigger is active, THE RENUM System SHALL evaluate its conditions every minute via Celery scheduled task
3. WHEN a trigger condition is met, THE RENUM System SHALL execute the configured action (send message, notify team, call tool, change status)
4. WHEN a trigger executes, THE RENUM System SHALL log the execution in trigger_executions table with timestamp, trigger_id, and result
5. WHEN a client toggles a trigger status, THE RENUM System SHALL immediately activate or deactivate the trigger evaluation

### Requirement 5: Sistema de Filas Assíncronas (Celery + Redis)

**User Story:** As a system administrator, I want asynchronous task processing, so that long-running operations don't block the API and the system remains responsive.

#### Acceptance Criteria

1. WHEN the RENUM System starts, THE Celery worker SHALL connect to Redis broker and be ready to process tasks
2. WHEN a WhatsApp message needs to be sent, THE RENUM System SHALL enqueue it as a Celery task for background processing
3. WHEN an email needs to be sent, THE RENUM System SHALL enqueue it as a Celery task for background processing
4. WHEN a trigger evaluation is scheduled, THE RENUM System SHALL execute it via Celery beat scheduler every minute
5. WHEN a Celery task fails, THE RENUM System SHALL retry up to 3 times with exponential backoff (1s, 5s, 25s) before marking as failed

### Requirement 6: LangChain Tools para Agentes

**User Story:** As an agent (RENUS, ISA, Discovery), I want to use integrations as tools, so that I can execute actions in the real world based on conversation context.

#### Acceptance Criteria

1. WHEN an agent is initialized, THE RENUM System SHALL provide WhatsAppTool, EmailTool, and SupabaseQueryTool as available tools
2. WHEN an agent decides to send a WhatsApp message, THE WhatsAppTool SHALL validate phone format and send via configured Uazapi integration
3. WHEN an agent decides to send an email, THE EmailTool SHALL validate email addresses and send via configured SMTP/SendGrid integration
4. WHEN an agent decides to query client data, THE SupabaseQueryTool SHALL execute the query on the client's configured database
5. WHEN a tool execution fails, THE RENUM System SHALL return a descriptive error message to the agent for context-aware error handling

### Requirement 7: Armazenamento de Configurações de Integração

**User Story:** As a system, I want to store integration configurations securely, so that credentials are protected and accessible only to authorized clients.

#### Acceptance Criteria

1. WHEN integration credentials are stored, THE RENUM System SHALL encrypt sensitive fields (tokens, passwords, API keys) before saving to database
2. WHEN retrieving integration credentials, THE RENUM System SHALL decrypt them only in memory and never expose them in API responses
3. WHILE RLS is enabled on integrations table, THE RENUM System SHALL ensure clients can only access their own integration configurations
4. WHEN an admin views integrations, THE RENUM System SHALL show all integrations across all clients for monitoring purposes
5. WHEN integration credentials are updated, THE RENUM System SHALL invalidate any cached credentials and reload from database

### Requirement 8: Webhooks para Recebimento de Mensagens

**User Story:** As a system, I want to receive webhook notifications from external services, so that I can process incoming messages and events in real-time.

#### Acceptance Criteria

1. WHEN Uazapi sends a webhook notification, THE RENUM System SHALL validate the request signature to ensure authenticity
2. WHEN a valid webhook is received, THE RENUM System SHALL extract the message content, sender phone, and timestamp
3. WHEN a webhook message is processed, THE RENUM System SHALL route it to the Discovery Agent for intent detection and response generation
4. WHEN webhook processing fails, THE RENUM System SHALL return HTTP 500 to trigger Uazapi retry mechanism
5. WHEN webhook processing succeeds, THE RENUM System SHALL return HTTP 200 to acknowledge receipt

### Requirement 9: Rate Limiting e Controle de Quota

**User Story:** As a system administrator, I want rate limiting on integrations, so that we don't exceed API quotas and incur additional costs.

#### Acceptance Criteria

1. WHEN sending WhatsApp messages, THE RENUM System SHALL enforce a rate limit of 100 messages per minute per client
2. WHEN rate limit is exceeded, THE RENUM System SHALL queue additional messages for delayed sending
3. WHEN sending emails, THE RENUM System SHALL enforce a rate limit of 50 emails per minute per client
4. WHEN querying client databases, THE RENUM System SHALL enforce a rate limit of 100 queries per minute per client
5. WHEN rate limit is reached, THE RENUM System SHALL return a clear error message indicating retry-after time

### Requirement 10: Frontend de Configuração de Integrações

**User Story:** As a client, I want a user-friendly interface to configure integrations, so that I can set up WhatsApp, Email, and Database connections without technical knowledge.

#### Acceptance Criteria

1. WHEN a client accesses the Integrations tab, THE RENUM System SHALL display cards for WhatsApp, Email, and Database with current status (connected/disconnected)
2. WHEN a client clicks "Configure" on an integration card, THE RENUM System SHALL open a modal with input fields for credentials
3. WHEN a client fills credentials and clicks "Test and Save", THE RENUM System SHALL validate the connection and show success or error feedback
4. WHEN an integration is successfully configured, THE RENUM System SHALL update the card status to "connected" with a green indicator
5. WHEN a client views configured integrations, THE RENUM System SHALL mask sensitive fields (show only last 4 characters of tokens)

### Requirement 11: Frontend de Gerenciamento de Triggers

**User Story:** As a client, I want a user-friendly interface to create and manage triggers, so that I can automate workflows without writing code.

#### Acceptance Criteria

1. WHEN a client accesses the Triggers tab, THE RENUM System SHALL display a list of existing triggers with WHEN → IF → THEN structure
2. WHEN a client clicks "New Trigger", THE RENUM System SHALL open a form with dropdowns for event selection, condition input, and action selection
3. WHEN a client saves a new trigger, THE RENUM System SHALL validate the configuration and create it in active status
4. WHEN a client toggles a trigger switch, THE RENUM System SHALL immediately activate or deactivate the trigger
5. WHEN a client clicks "Test" on a trigger, THE RENUM System SHALL simulate the trigger execution and show the result

### Requirement 12: Logs e Auditoria de Integrações

**User Story:** As a system administrator, I want detailed logs of integration usage, so that I can monitor performance, debug issues, and track costs.

#### Acceptance Criteria

1. WHEN a WhatsApp message is sent, THE RENUM System SHALL log the timestamp, client_id, phone number, message length, and result (success/failure)
2. WHEN an email is sent, THE RENUM System SHALL log the timestamp, client_id, recipient, subject, and result
3. WHEN a database query is executed, THE RENUM System SHALL log the timestamp, client_id, table name, operation type, and execution time
4. WHEN a trigger executes, THE RENUM System SHALL log the timestamp, trigger_id, condition evaluation result, and action result
5. WHEN viewing logs, THE RENUM System SHALL allow filtering by client, integration type, date range, and status (success/failure)

---

## Non-Functional Requirements

### Performance

1. THE RENUM System SHALL process webhook notifications within 500ms average response time
2. THE RENUM System SHALL send WhatsApp messages within 2 seconds of agent decision
3. THE RENUM System SHALL evaluate all active triggers within 60 seconds of scheduled execution

### Security

1. THE RENUM System SHALL encrypt all integration credentials at rest using AES-256
2. THE RENUM System SHALL use HTTPS for all external API communications
3. THE RENUM System SHALL validate webhook signatures to prevent unauthorized access
4. THE RENUM System SHALL enforce RLS on all integration-related tables

### Scalability

1. THE RENUM System SHALL support up to 1000 concurrent webhook requests
2. THE RENUM System SHALL support up to 100 active triggers per client
3. THE RENUM System SHALL support up to 10,000 messages per day per client

### Reliability

1. THE RENUM System SHALL retry failed message sends up to 3 times
2. THE RENUM System SHALL maintain 99.5% uptime for webhook endpoints
3. THE RENUM System SHALL gracefully handle external API downtime with queuing

---

**Document Version:** 1.0  
**Created:** 2025-12-04  
**Status:** Draft - Awaiting Approval
