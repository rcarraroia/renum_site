# Implementation Plan - Sprint 07A: Integrações Core

## Overview

Este documento define as tarefas de implementação para o Sprint 07A, organizadas em fases sequenciais. Cada tarefa é executável e inclui referências aos requisitos que valida.

**Estimativa Total:** 40-50 horas de desenvolvimento

---

## Phase 1: Database Migrations e Setup Inicial

### Task 1.1: Criar migration para tabela `integrations`

Criar migration SQL para tabela de configurações de integrações.

**Subtasks:**
- Criar arquivo `migrations/007_create_integrations_table.sql`
- Definir schema com colunas: id, client_id, type, name, status, config, timestamps
- Adicionar constraints e foreign keys
- Habilitar RLS
- Criar políticas RLS para admins e clients
- Criar índices em client_id, type, status

_Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

### Task 1.2: Criar migration para tabela `triggers`

Criar migration SQL para tabela de gatilhos/automações.

**Subtasks:**
- Criar arquivo `migrations/008_create_triggers_table.sql`
- Definir schema com trigger_type, trigger_config, condition_type, condition_config, action_type, action_config
- Adicionar constraints e foreign keys
- Habilitar RLS
- Criar políticas RLS para admins e clients
- Criar índices em client_id, active, trigger_type

_Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

### Task 1.3: Criar migration para tabela `trigger_executions`

Criar migration SQL para log de execuções de triggers.

**Subtasks:**
- Criar arquivo `migrations/009_create_trigger_executions_table.sql`
- Definir schema com trigger_id, executed_at, condition_met, action_executed, result
- Adicionar constraints e foreign keys
- Habilitar RLS
- Criar políticas RLS (admins full access, clients read-only)
- Criar índices em trigger_id, client_id, executed_at

_Requirements: 4.4, 12.4_

### Task 1.4: Executar migrations no Supabase

Aplicar todas as migrations no banco de dados.

**Subtasks:**
- Conectar ao Supabase via SQL Editor
- Executar migration 007_create_integrations_table.sql
- Executar migration 008_create_triggers_table.sql
- Executar migration 009_create_trigger_executions_table.sql
- Verificar tabelas criadas com `SELECT * FROM information_schema.tables`
- Verificar RLS habilitado com `SELECT tablename, rowsecurity FROM pg_tables`

_Requirements: 7.1, 4.1_


---

## Phase 2: Configuração Celery + Redis

### Task 2.1: Instalar dependências Celery e Redis

Adicionar bibliotecas necessárias ao projeto.

**Subtasks:**
- Adicionar ao `requirements.txt`: celery==5.3.4, redis==5.0.1, aiohttp==3.9.1, httpx==0.25.2
- Executar `pip install -r requirements.txt`
- Verificar instalação com `pip list | grep -E '(celery|redis)'`

_Requirements: 5.1_

### Task 2.2: Criar Celery app configuration

Configurar aplicação Celery com Redis como broker.

**Subtasks:**
- Criar arquivo `backend/src/workers/__init__.py`
- Criar arquivo `backend/src/workers/celery_app.py`
- Configurar Celery app com Redis broker URL
- Configurar result backend
- Configurar task serializer (JSON)
- Configurar timezone (America/Sao_Paulo)
- Configurar beat schedule para trigger_scheduler (every 1 minute)

_Requirements: 5.1, 5.4_

### Task 2.3: Criar Celery tasks para mensagens

Implementar tasks assíncronas para envio de mensagens.

**Subtasks:**
- Criar arquivo `backend/src/workers/message_tasks.py`
- Implementar `send_whatsapp_message_task(client_id, phone, message)`
- Implementar `send_email_task(client_id, to, subject, body, cc)`
- Configurar retry policy (max_retries=3, backoff=exponential)
- Adicionar logging para cada task
- Adicionar error handling

_Requirements: 5.2, 5.3, 5.5_

### Task 2.4: Criar Celery task para trigger scheduler

Implementar task agendada para avaliar triggers.

**Subtasks:**
- Criar arquivo `backend/src/workers/trigger_tasks.py`
- Implementar `trigger_scheduler_task()` que roda a cada 1 minuto
- Carregar todos triggers ativos do banco
- Avaliar condições de cada trigger
- Executar ações para triggers que atendem condições
- Logar execuções em trigger_executions

_Requirements: 4.2, 4.3, 4.4, 5.4_

### Task 2.5: Testar Celery localmente

Validar que Celery está funcionando corretamente.

**Subtasks:**
- Iniciar Redis: `redis-server`
- Iniciar Celery worker: `celery -A src.workers.celery_app worker --loglevel=info`
- Iniciar Celery beat: `celery -A src.workers.celery_app beat --loglevel=info`
- Enfileirar task de teste via Python shell
- Verificar task executada nos logs
- Verificar resultado no Redis

_Requirements: 5.1, 5.2, 5.3, 5.4_


---

## Phase 3: Integração Uazapi (WhatsApp)

### Task 3.1: Criar Uazapi client

Implementar cliente Python para API Uazapi.

**Subtasks:**
- Criar arquivo `backend/src/integrations/__init__.py`
- Criar arquivo `backend/src/integrations/uazapi_client.py`
- Implementar classe `UazapiClient` com métodos:
  - `__init__(api_url, api_token, phone_number)`
  - `async send_message(phone, message) -> dict`
  - `async send_media(phone, media_url, caption, media_type) -> dict`
  - `validate_phone(phone) -> bool`
  - `validate_webhook_signature(payload, signature) -> bool`
- Adicionar error handling e retry logic
- Adicionar logging

_Requirements: 1.3, 1.4_

**Note:** Aguardando documentação da API Uazapi em `docs/API_UAZAPI.md`

### Task 3.2: Criar Integration Service

Implementar serviço para gerenciar configurações de integrações.

**Subtasks:**
- Criar arquivo `backend/src/services/integration_service.py`
- Implementar classe `IntegrationService` com métodos:
  - `create_integration(client_id, type, config) -> Integration`
  - `get_integration(client_id, type) -> Integration`
  - `update_integration(integration_id, config) -> Integration`
  - `delete_integration(integration_id) -> bool`
  - `test_connection(integration_id) -> TestResult`
  - `encrypt_credentials(credentials) -> dict`
  - `decrypt_credentials(encrypted) -> dict`
- Usar biblioteca `cryptography` para AES-256-GCM
- Adicionar validação de RLS

_Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

### Task 3.3: Criar endpoints de API para WhatsApp

Implementar rotas FastAPI para configuração WhatsApp.

**Subtasks:**
- Criar arquivo `backend/src/api/routes/integrations.py`
- Implementar `POST /api/integrations/whatsapp/configure`
- Implementar `GET /api/integrations/whatsapp/status`
- Implementar `POST /api/integrations/whatsapp/send`
- Implementar `POST /api/integrations/whatsapp/test`
- Adicionar validação de input com Pydantic models
- Adicionar autenticação JWT
- Adicionar rate limiting

_Requirements: 1.1, 1.2, 1.3, 9.1, 9.2_

### Task 3.4: Criar webhook handler para Uazapi

Implementar endpoint para receber mensagens do WhatsApp.

**Subtasks:**
- Criar arquivo `backend/src/api/routes/webhooks.py`
- Implementar `POST /webhooks/uazapi`
- Validar signature do webhook
- Extrair dados da mensagem (from, message, timestamp)
- Rotear para Discovery Agent para processamento
- Retornar HTTP 200 em sucesso, 500 em erro
- Adicionar logging detalhado

_Requirements: 1.4, 8.1, 8.2, 8.3, 8.4, 8.5_


### Task 3.5: Atualizar WhatsAppTool para usar Uazapi

Modificar LangChain Tool existente para usar UazapiClient.

**Subtasks:**
- Abrir arquivo `backend/src/tools/whatsapp_tool.py`
- Modificar `WhatsAppTool` para usar `UazapiClient` em vez de provider abstrato
- Atualizar método `_arun` para carregar config do banco
- Adicionar integração com Celery (enfileirar send_whatsapp_message_task)
- Manter interface LangChain Tool inalterada
- Adicionar testes unitários

_Requirements: 1.3, 6.1, 6.2_

---

## Phase 4: Integração Email (SMTP + SendGrid)

### Task 4.1: Criar SMTP client

Implementar cliente SMTP nativo Python.

**Subtasks:**
- Criar arquivo `backend/src/integrations/smtp_client.py`
- Implementar classe `SMTPClient` com métodos:
  - `__init__(host, port, username, password, use_tls, from_email)`
  - `async send_email(to, subject, body, cc) -> dict`
  - `async test_connection() -> bool`
- Usar biblioteca `aiosmtplib` para async SMTP
- Adicionar suporte para HTML e plain text
- Adicionar error handling

_Requirements: 2.1, 2.3, 2.4_

### Task 4.2: Criar SendGrid client

Implementar cliente SendGrid como alternativa.

**Subtasks:**
- Criar arquivo `backend/src/integrations/sendgrid_client.py`
- Implementar classe `SendGridClient` com métodos:
  - `__init__(api_key, from_email, from_name)`
  - `async send_email(to, subject, body, cc) -> dict`
  - `async test_connection() -> bool`
- Usar biblioteca `sendgrid` oficial
- Adicionar suporte para templates
- Adicionar error handling

_Requirements: 2.2, 2.3, 2.4_

### Task 4.3: Criar endpoints de API para Email

Implementar rotas FastAPI para configuração Email.

**Subtasks:**
- Adicionar ao arquivo `backend/src/api/routes/integrations.py`
- Implementar `POST /api/integrations/email/configure`
- Implementar `GET /api/integrations/email/status`
- Implementar `POST /api/integrations/email/send`
- Implementar `POST /api/integrations/email/test`
- Suportar ambos providers (SMTP e SendGrid)
- Adicionar validação de email addresses

_Requirements: 2.1, 2.2, 2.3, 2.4, 9.3_

### Task 4.4: Atualizar EmailTool para usar SMTP/SendGrid

Modificar LangChain Tool existente para usar clientes reais.

**Subtasks:**
- Abrir arquivo `backend/src/tools/email_tool.py`
- Remover implementação MOCK
- Adicionar lógica para detectar provider (SMTP vs SendGrid)
- Carregar config do banco baseado em client_id
- Integrar com Celery (enfileirar send_email_task)
- Adicionar testes unitários

_Requirements: 2.4, 6.1, 6.3_


---

## Phase 5: Integração Database do Cliente

### Task 5.1: Criar Supabase client para banco do cliente

Implementar cliente para conectar ao Supabase do cliente.

**Subtasks:**
- Criar arquivo `backend/src/integrations/client_supabase.py`
- Implementar classe `ClientSupabaseClient` com métodos:
  - `__init__(supabase_url, supabase_key, read_only, allowed_tables)`
  - `async execute_query(table, operation, filters, data) -> dict`
  - `async test_connection() -> bool`
  - `validate_query_safety(query) -> bool` (prevent SQL injection)
- Adicionar whitelist de tabelas permitidas
- Enforçar read_only mode por padrão

_Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

### Task 5.2: Criar endpoints de API para Database

Implementar rotas FastAPI para configuração Database.

**Subtasks:**
- Adicionar ao arquivo `backend/src/api/routes/integrations.py`
- Implementar `POST /api/integrations/database/configure`
- Implementar `GET /api/integrations/database/status`
- Implementar `POST /api/integrations/database/test`
- Validar credenciais Supabase
- Testar conexão com SELECT 1

_Requirements: 3.1, 3.2, 9.4_

### Task 5.3: Atualizar SupabaseQueryTool para usar banco do cliente

Modificar LangChain Tool existente para consultar banco do cliente.

**Subtasks:**
- Abrir arquivo `backend/src/tools/supabase_tool.py`
- Adicionar lógica para carregar config do cliente
- Criar instância de `ClientSupabaseClient` com credenciais do cliente
- Manter interface LangChain Tool inalterada
- Adicionar validação de segurança (SQL injection prevention)
- Adicionar testes unitários

_Requirements: 3.3, 3.4, 3.5, 6.1, 6.4_

---

## Phase 6: Sistema de Triggers

### Task 6.1: Criar Trigger Service

Implementar serviço para gerenciar triggers.

**Subtasks:**
- Criar arquivo `backend/src/services/trigger_service.py`
- Implementar classe `TriggerService` com métodos:
  - `create_trigger(client_id, trigger_data) -> Trigger`
  - `get_triggers(client_id, active_only) -> List[Trigger]`
  - `get_trigger(trigger_id) -> Trigger`
  - `update_trigger(trigger_id, trigger_data) -> Trigger`
  - `toggle_trigger(trigger_id, active) -> Trigger`
  - `delete_trigger(trigger_id) -> bool`
- Adicionar validação de configuração
- Adicionar RLS enforcement

_Requirements: 4.1, 4.5_

### Task 6.2: Criar Trigger Evaluator

Implementar lógica para avaliar condições de triggers.

**Subtasks:**
- Criar arquivo `backend/src/services/trigger_evaluator.py`
- Implementar classe `TriggerEvaluator` com métodos:
  - `evaluate_time_based(trigger) -> bool`
  - `evaluate_event_based(trigger, event) -> bool`
  - `evaluate_condition(trigger, context) -> bool`
- Suportar operadores: equals, contains, greater_than, less_than
- Suportar campos: conversation.status, conversation.last_message_at, lead.score
- Adicionar logging de avaliações

_Requirements: 4.2, 4.3_


### Task 6.3: Criar Trigger Executor

Implementar lógica para executar ações de triggers.

**Subtasks:**
- Criar arquivo `backend/src/services/trigger_executor.py`
- Implementar classe `TriggerExecutor` com métodos:
  - `execute_send_message(trigger, context) -> dict`
  - `execute_send_email(trigger, context) -> dict`
  - `execute_call_tool(trigger, context) -> dict`
  - `execute_change_status(trigger, context) -> dict`
- Integrar com WhatsAppTool e EmailTool
- Logar execuções em trigger_executions table
- Adicionar error handling

_Requirements: 4.3, 4.4_

### Task 6.4: Implementar trigger_scheduler_task

Completar implementação da task Celery Beat.

**Subtasks:**
- Abrir arquivo `backend/src/workers/trigger_tasks.py`
- Implementar lógica completa de `trigger_scheduler_task()`:
  - Carregar todos triggers ativos
  - Para cada trigger, avaliar condição
  - Se condição atendida, executar ação
  - Logar resultado em trigger_executions
  - Atualizar last_executed_at e execution_count
- Adicionar tratamento de erros
- Adicionar métricas de performance

_Requirements: 4.2, 4.3, 4.4, 5.4_

### Task 6.5: Criar endpoints de API para Triggers

Implementar rotas FastAPI para gerenciamento de triggers.

**Subtasks:**
- Criar arquivo `backend/src/api/routes/triggers.py`
- Implementar `POST /api/triggers`
- Implementar `GET /api/triggers`
- Implementar `GET /api/triggers/{id}`
- Implementar `PUT /api/triggers/{id}`
- Implementar `DELETE /api/triggers/{id}`
- Implementar `PATCH /api/triggers/{id}/toggle`
- Implementar `POST /api/triggers/{id}/test` (simulate execution)
- Adicionar validação de input
- Adicionar autenticação JWT

_Requirements: 4.1, 4.5, 11.2, 11.3, 11.4, 11.5_

---

## Phase 7: Conectar Frontend ao Backend

### Task 7.1: Criar service de integrações no frontend

Implementar chamadas de API para integrações.

**Subtasks:**
- Criar arquivo `frontend/src/services/integrationService.ts`
- Implementar funções:
  - `configureWhatsApp(config) -> Promise<Integration>`
  - `getWhatsAppStatus() -> Promise<Status>`
  - `testWhatsApp() -> Promise<TestResult>`
  - `configureEmail(config) -> Promise<Integration>`
  - `getEmailStatus() -> Promise<Status>`
  - `testEmail() -> Promise<TestResult>`
  - `configureDatabase(config) -> Promise<Integration>`
  - `getDatabaseStatus() -> Promise<Status>`
  - `testDatabase() -> Promise<TestResult>`
- Usar axios para HTTP requests
- Adicionar error handling

_Requirements: 10.1, 10.2, 10.3, 10.4_

### Task 7.2: Conectar IntegrationsTab ao backend

Substituir dados MOCK por chamadas reais de API.

**Subtasks:**
- Abrir arquivo `frontend/src/components/settings/IntegrationsTab.tsx`
- Remover MOCK_INTEGRATIONS
- Usar `integrationService` para carregar status real
- Implementar `handleTestConnection` com chamada real de API
- Implementar `handleSave` com POST /api/integrations/*/configure
- Adicionar loading states
- Adicionar error handling com toast notifications

_Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_


### Task 7.3: Criar service de triggers no frontend

Implementar chamadas de API para triggers.

**Subtasks:**
- Criar arquivo `frontend/src/services/triggerService.ts`
- Implementar funções:
  - `getTriggers(activeOnly) -> Promise<Trigger[]>`
  - `getTrigger(id) -> Promise<Trigger>`
  - `createTrigger(data) -> Promise<Trigger>`
  - `updateTrigger(id, data) -> Promise<Trigger>`
  - `deleteTrigger(id) -> Promise<void>`
  - `toggleTrigger(id, active) -> Promise<Trigger>`
  - `testTrigger(id) -> Promise<TestResult>`
- Usar axios para HTTP requests
- Adicionar error handling

_Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

### Task 7.4: Conectar TriggersTab ao backend

Substituir dados MOCK por chamadas reais de API.

**Subtasks:**
- Abrir arquivo `frontend/src/components/agents/config/TriggersTab.tsx`
- Remover MOCK_TRIGGERS
- Usar `triggerService` para carregar triggers reais
- Implementar `handleToggle` com PATCH /api/triggers/{id}/toggle
- Implementar `handleTestTrigger` com POST /api/triggers/{id}/test
- Implementar formulário de criação com POST /api/triggers
- Adicionar loading states
- Adicionar error handling

_Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

### Task 7.5: Criar types TypeScript para integrações e triggers

Definir interfaces TypeScript para type safety.

**Subtasks:**
- Criar arquivo `frontend/src/types/integration.ts`
- Definir interfaces:
  - `Integration { id, client_id, type, name, status, config, ... }`
  - `IntegrationConfig { ... }` (union type para WhatsApp/Email/Database)
  - `IntegrationStatus { status, last_tested_at, ... }`
- Criar arquivo `frontend/src/types/trigger.ts`
- Definir interfaces:
  - `Trigger { id, name, active, trigger_type, trigger_config, ... }`
  - `TriggerConfig { ... }`
  - `TriggerExecution { ... }`

_Requirements: 10.1, 11.1_

---

## Phase 8: Testes e Validação

### Task 8.1: Criar testes unitários para Integration Service

Testar lógica de gerenciamento de integrações.

**Subtasks:**
- Criar arquivo `backend/tests/unit/test_integration_service.py`
- Testar `create_integration` com dados válidos/inválidos
- Testar `encrypt_credentials` e `decrypt_credentials`
- Testar `test_connection` para cada tipo de integração
- Testar RLS enforcement
- Usar pytest e pytest-mock

_Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

### Task 8.2: Criar testes unitários para Uazapi Client

Testar comunicação com API Uazapi.

**Subtasks:**
- Criar arquivo `backend/tests/unit/test_uazapi_client.py`
- Testar `send_message` com sucesso e falha
- Testar `validate_phone` com números válidos/inválidos
- Testar `validate_webhook_signature` com assinaturas válidas/inválidas
- Mockar respostas da API Uazapi
- Usar pytest-asyncio para testes async

_Requirements: 1.3, 1.4, 8.1_

### Task 8.3: Criar testes unitários para Email Clients

Testar envio de emails via SMTP e SendGrid.

**Subtasks:**
- Criar arquivo `backend/tests/unit/test_smtp_client.py`
- Criar arquivo `backend/tests/unit/test_sendgrid_client.py`
- Testar `send_email` com sucesso e falha
- Testar `test_connection` para ambos providers
- Mockar conexões SMTP e API SendGrid
- Testar retry logic

_Requirements: 2.3, 2.4, 2.5_


### Task 8.4: Criar testes unitários para Trigger Service

Testar lógica de triggers.

**Subtasks:**
- Criar arquivo `backend/tests/unit/test_trigger_service.py`
- Testar CRUD operations para triggers
- Testar `TriggerEvaluator.evaluate_condition` com diferentes operadores
- Testar `TriggerExecutor.execute_action` para cada tipo de ação
- Mockar dependências (database, WhatsAppTool, EmailTool)
- Testar edge cases (trigger inativo, condição não atendida, erro na execução)

_Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

### Task 8.5: Criar testes de integração end-to-end

Testar fluxos completos do sistema.

**Subtasks:**
- Criar arquivo `backend/tests/integration/test_whatsapp_flow.py`
- Testar fluxo: Configure WhatsApp → Send message → Receive webhook → Process response
- Criar arquivo `backend/tests/integration/test_email_flow.py`
- Testar fluxo: Configure Email → Send email → Verify delivery
- Criar arquivo `backend/tests/integration/test_trigger_flow.py`
- Testar fluxo: Create trigger → Wait for condition → Execute action → Verify execution log
- Usar banco de dados de teste (não produção)
- Mockar APIs externas (Uazapi, SMTP)

_Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.3, 2.4, 4.1, 4.2, 4.3, 4.4_

### Task 8.6: Validação manual completa

Executar checklist de validação manual.

**Subtasks:**
- **WhatsApp:**
  - [ ] Configurar credenciais Uazapi no frontend
  - [ ] Testar conexão (botão "Testar e Salvar")
  - [ ] Enviar mensagem de teste via API
  - [ ] Simular webhook do Uazapi (POST /webhooks/uazapi)
  - [ ] Verificar mensagem processada pelo Discovery Agent
  - [ ] Verificar resposta enviada de volta

- **Email:**
  - [ ] Configurar credenciais SMTP no frontend
  - [ ] Testar conexão
  - [ ] Enviar email de teste via API
  - [ ] Verificar email recebido na caixa de entrada
  - [ ] Testar com SendGrid (se disponível)

- **Database:**
  - [ ] Configurar credenciais Supabase do cliente
  - [ ] Testar conexão
  - [ ] Executar query de teste via SupabaseQueryTool
  - [ ] Verificar resultados retornados
  - [ ] Testar read-only enforcement

- **Triggers:**
  - [ ] Criar trigger time-based no frontend
  - [ ] Aguardar 1 minuto (Celery beat cycle)
  - [ ] Verificar trigger avaliado (logs)
  - [ ] Verificar ação executada (mensagem enviada)
  - [ ] Verificar log em trigger_executions
  - [ ] Testar toggle on/off
  - [ ] Testar simulação de trigger

- **Celery:**
  - [ ] Verificar Celery worker rodando
  - [ ] Verificar Celery beat rodando
  - [ ] Verificar Redis conectado
  - [ ] Enfileirar task manualmente
  - [ ] Verificar task executada
  - [ ] Verificar retry em caso de falha

_Requirements: All requirements_

---

## Phase 9: Documentação e Deploy

### Task 9.1: Atualizar documentação de API

Documentar todos os novos endpoints.

**Subtasks:**
- Atualizar `docs/API_DOCUMENTATION.md`
- Documentar endpoints de integrações (WhatsApp, Email, Database)
- Documentar endpoints de triggers
- Documentar webhook Uazapi
- Incluir exemplos de request/response
- Incluir códigos de erro

_Requirements: All requirements_

### Task 9.2: Criar guia de configuração para clientes

Documentar como configurar integrações.

**Subtasks:**
- Criar arquivo `docs/INTEGRATION_SETUP_GUIDE.md`
- Documentar passo a passo para configurar WhatsApp (Uazapi)
- Documentar passo a passo para configurar Email (SMTP/SendGrid)
- Documentar passo a passo para configurar Database
- Documentar como criar triggers
- Incluir screenshots do frontend
- Incluir troubleshooting comum

_Requirements: 10.1, 10.2, 10.3, 11.1, 11.2_

### Task 9.3: Configurar serviços na VPS

Preparar ambiente de produção.

**Subtasks:**
- Conectar via SSH: `ssh root@72.60.151.78`
- Instalar Redis: `sudo apt install redis-server`
- Configurar Redis para iniciar no boot: `sudo systemctl enable redis`
- Criar arquivo systemd para Celery worker: `/etc/systemd/system/renum-celery.service`
- Criar arquivo systemd para Celery beat: `/etc/systemd/system/renum-celery-beat.service`
- Atualizar .env com variáveis necessárias (REDIS_URL, ENCRYPTION_KEY, etc)
- Reiniciar backend: `sudo systemctl restart renum-api`
- Iniciar Celery worker: `sudo systemctl start renum-celery`
- Iniciar Celery beat: `sudo systemctl start renum-celery-beat`
- Verificar todos serviços rodando: `sudo systemctl status renum-*`

_Requirements: 5.1_

### Task 9.4: Checkpoint Final - Validação Completa

Garantir que tudo está funcionando em produção.

**Subtasks:**
- Executar todos testes automatizados
- Executar checklist de validação manual
- Verificar logs de erro (não deve haver erros críticos)
- Verificar métricas de performance (latência < 500ms)
- Verificar Celery processando tasks
- Verificar triggers executando a cada minuto
- Obter aprovação do usuário antes de considerar sprint completo

_Requirements: All requirements_

---

## Summary

**Total Tasks:** 45 tasks across 9 phases

**Estimated Time:**
- Phase 1 (Migrations): 4 hours
- Phase 2 (Celery): 6 hours
- Phase 3 (WhatsApp): 8 hours
- Phase 4 (Email): 6 hours
- Phase 5 (Database): 4 hours
- Phase 6 (Triggers): 8 hours
- Phase 7 (Frontend): 6 hours
- Phase 8 (Tests): 6 hours
- Phase 9 (Deploy): 4 hours

**Total:** ~52 hours

**Dependencies:**
- Documentação API Uazapi (aguardando)
- Credenciais Uazapi de teste (aguardando)
- Acesso SSH à VPS (disponível)
- Credenciais Supabase (disponível)

---

**Document Version:** 1.0  
**Created:** 2025-12-04  
**Status:** Draft - Awaiting Approval  
**Next Steps:** Aguardar aprovação do usuário e documentação API Uazapi
