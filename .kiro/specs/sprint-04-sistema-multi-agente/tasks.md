# Implementation Plan - Sprint 04: Sistema Multi-Agente

## Overview

Este plano de implementação detalha as tarefas necessárias para construir o sistema multi-agente do RENUM, incluindo RENUS (orquestrador), ISA (assistente admin), Discovery (sub-agente de entrevistas), infraestrutura LangGraph/LangServe, e interfaces de gerenciamento.

---

## 📊 PROGRESSO ATUAL

**Status:** 🟡 Em Andamento (26% completo)

**Tasks Completas:** 18/69 (26%)
- ✅ Phase 2: Database Migration (2/2 tasks)
- ✅ Phase 6: Discovery Agent (3/4 tasks - 75%)
- ✅ Phase 7: Services (2/2 tasks)
- ✅ Phase 9: API Routes (1/7 tasks - 14%)
- ✅ Phase 11: Frontend Interviews (4/4 tasks)

**Tasks Adicionadas:** +17 tasks para integração completa com frontend de configuração RENUS/ISA
- Phase 9B: Backend Models e Services (6 tasks)
- Phase 9C: Frontend Integração (10 tasks)

**Próxima Task:** Task 1 - Configurar ambiente e dependências de IA

**Estimativa Restante:** 40-50 horas (2 semanas)

---

## Tasks

### Phase 1: Infraestrutura Base e Configuração

- [x] 1. Configurar ambiente e dependências de IA


  - Adicionar dependências ao requirements.txt: langserve[all], langsmith, hypothesis
  - Atualizar .env.example com variáveis de IA (OPENAI_API_KEY, ANTHROPIC_API_KEY, LANGSMITH_API_KEY, etc)
  - Atualizar settings.py com configurações de IA e validação de chaves
  - Criar função validate_ai_keys() que falha fast se chaves estiverem faltando
  - _Requirements: 4.4, 11.5_


- [x] 2. Criar estrutura de pastas para agentes

  - Criar backend/src/agents/ com __init__.py
  - Criar backend/src/agents/subagents/ com __init__.py
  - Criar backend/src/tools/ com __init__.py
  - Criar backend/src/providers/ com __init__.py
  - Criar backend/src/providers/whatsapp/ com __init__.py
  - Criar backend/src/langserve/ com __init__.py
  - _Requirements: 4.1_


- [x] 3. Configurar LangSmith para observabilidade


  - Configurar variáveis de ambiente LangSmith em settings.py
  - Criar função de inicialização que configura tracing
  - Adicionar tags padrão (environment, client_id) para todos os traces
  - Testar conexão com LangSmith ao iniciar aplicação
  - _Requirements: 10.1, 10.5_


### Phase 2: Database Migration e Models

- [x] 4. Criar migration para adicionar campos em interviews
  - Criar arquivo migrations/004_add_interview_fields.sql
  - Adicionar colunas: email, country, company, niche_experience, current_rank, operation_size
  - Adicionar comentários SQL para documentação
  - Criar índices em country e company
  - Executar migration no Supabase
  - Verificar que dados existentes não foram afetados
  - _Requirements: 7.1_
  - ✅ **COMPLETO** - Migration executada com sucesso

- [x] 5. Atualizar Pydantic models para interviews
  - Atualizar backend/src/models/interview.py com novos campos
  - Adicionar validação de email com EmailStr
  - Criar InterviewCreate, InterviewUpdate, InterviewResponse
  - Criar InterviewMessageCreate e InterviewMessageResponse
  - Adicionar testes unitários para validação de models
  - _Requirements: 7.1, 7.2_
  - ✅ **COMPLETO** - Models criados e validados

- [x] 6. Criar Pydantic models para sub_agents


  - Criar backend/src/models/sub_agent.py
  - Implementar SubAgentBase, SubAgentCreate, SubAgentUpdate, SubAgentResponse
  - Adicionar validação de channel (whatsapp|web|sms|email)
  - Adicionar validação de model (lista de modelos suportados)
  - Adicionar testes unitários
  - _Requirements: 6.2, 11.4_


- [x] 7. Criar Pydantic models para isa_commands

  - Criar backend/src/models/isa_command.py
  - Implementar IsaCommandCreate e IsaCommandResponse
  - Adicionar validação de admin_id (deve ser UUID válido)
  - Adicionar testes unitários
  - _Requirements: 2.3_

### Phase 3: Tools (Ferramentas para Agentes)


- [x] 8. Implementar Supabase Tool

  - Criar backend/src/tools/supabase_tool.py
  - Implementar SupabaseQueryInput (Pydantic schema)
  - Implementar SupabaseTool com operações: select, insert, update, delete
  - Adicionar suporte a multi-tenant (filtro por client_id)
  - Implementar tratamento de erros que retorna dict com success/error
  - Adicionar testes unitários com mock do Supabase
  - _Requirements: 5.1, 5.4, 5.5_

- [x] 9. Criar abstração WhatsApp Provider



  - Criar backend/src/providers/whatsapp/base.py
  - Implementar WhatsAppMessage (Pydantic model)
  - Implementar WhatsAppProvider (ABC) com métodos abstratos
  - Documentar assinaturas de send_message, send_media, handle_webhook, get_message_status
  - Adicionar type hints completos
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 10. Implementar WhatsApp Tool


  - Criar backend/src/tools/whatsapp_tool.py
  - Implementar WhatsAppMessageInput (Pydantic schema)
  - Implementar WhatsAppTool que usa WhatsAppProvider
  - Adicionar validação de formato de telefone (+5511999999999)
  - Implementar tratamento de erros
  - Adicionar testes unitários com mock do provider
  - _Requirements: 5.2, 5.5, 9.5_

- [x] 11. Implementar Email Tool



  - Criar backend/src/tools/email_tool.py
  - Implementar EmailInput (Pydantic schema com EmailStr)
  - Implementar EmailTool (placeholder para provider futuro)
  - Adicionar suporte a múltiplos destinatários e CC
  - Implementar tratamento de erros
  - Adicionar testes unitários com mock
  - _Requirements: 5.3, 5.5_


### Phase 4: Base Agent e RENUS

- [x] 12. Implementar BaseAgent (classe abstrata)


  - Criar backend/src/agents/base.py
  - Implementar __init__ com model, system_prompt, tools
  - Definir métodos abstratos: _initialize_llm, _build_graph, invoke
  - Adicionar type hints completos
  - Documentar com docstrings
  - _Requirements: 1.1, 4.1_

- [x] 13. Implementar RENUS Agent (orquestrador)


  - Criar backend/src/agents/renus.py
  - Herdar de BaseAgent
  - Implementar _initialize_llm com ChatOpenAI (gpt-4-turbo-preview)
  - Criar system prompt para orquestração
  - Implementar _build_graph com LangGraph (nodes: analyze, route, respond)
  - Implementar lógica de roteamento para sub-agentes
  - Adicionar logging de decisões para LangSmith
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [ ]* 13.1 Escrever testes unitários para RENUS
  - Testar construção do grafo
  - Testar análise de intent com vários tipos de mensagem
  - Testar decisões de roteamento
  - Mockar LLM para testes determinísticos
  - _Requirements: 1.1, 1.2_

- [x] 14. Implementar fallback e error handling no RENUS

  - Adicionar lógica de fallback quando sub-agente falha
  - Implementar retry com backoff exponencial
  - Adicionar opção de escalação para humano
  - Logar todos os erros e fallbacks no LangSmith
  - _Requirements: 1.4, 1.5_

- [ ]* 14.1 Escrever testes de fallback
  - Testar comportamento quando sub-agente retorna erro
  - Testar retry logic
  - Testar escalação para humano
  - _Requirements: 1.4_

### Phase 5: ISA Agent

- [x] 15. Implementar ISA Agent (assistente admin)


  - Criar backend/src/agents/isa.py
  - Herdar de BaseAgent
  - Implementar _initialize_llm com ChatAnthropic (claude-3-5-sonnet)
  - Criar system prompt com comandos administrativos
  - Implementar parsing de comandos
  - Adicionar acesso a Supabase Tool com permissões admin
  - _Requirements: 2.1, 2.2, 2.7_

- [x] 16. Implementar execução de comandos ISA

  - Implementar comando "generate report"
  - Implementar comando "send message to"
  - Implementar comando "query [entity]"
  - Implementar comando "analyze [data]"
  - Implementar comando "list [entity]"
  - Adicionar confirmação para operações destrutivas
  - _Requirements: 2.4, 2.5_

- [x] 17. Implementar auditoria de comandos ISA


  - Criar função para salvar comandos em isa_commands table
  - Registrar user_message, assistant_response, command_executed
  - Adicionar timestamp de execução
  - Verificar role admin antes de executar
  - _Requirements: 2.3, 2.7_

- [ ]* 17.1 Escrever testes para ISA
  - Testar parsing de cada tipo de comando
  - Testar execução com permissões admin
  - Testar rejeição sem permissões admin
  - Testar auditoria em isa_commands
  - _Requirements: 2.1, 2.3, 2.7_


### Phase 6: Discovery Sub-Agent

- [x] 18. Implementar Discovery Agent



  - Criar backend/src/agents/subagents/discovery.py
  - Herdar de BaseAgent
  - Implementar _initialize_llm com ChatOpenAI (gpt-4o-mini)
  - Criar system prompt para entrevistas conversacionais
  - Definir lista de campos obrigatórios
  - Implementar _build_graph com fluxo de entrevista
  - _Requirements: 3.1, 3.2, 3.3_
  - ✅ **COMPLETO** - Agent criado (standalone, precisa refatorar para LangGraph)

- [x] 19. Implementar fluxo de perguntas do Discovery
  - Criar sequência de perguntas para cada campo obrigatório
  - Implementar validação de respostas (email, telefone, etc)
  - Adicionar lógica para re-perguntar se resposta inválida
  - Implementar salvamento de cada mensagem em interview_messages
  - Manter contexto da conversa entre perguntas
  - _Requirements: 3.3, 3.4, 3.7_
  - ✅ **COMPLETO** - Fluxo conversacional funcional

- [x] 20. Implementar geração de AI analysis
  - Criar função para gerar análise ao completar entrevista
  - Extrair insights das respostas coletadas
  - Identificar padrões e oportunidades
  - Gerar recomendações acionáveis
  - Salvar análise em campo ai_analysis (jsonb)
  - _Requirements: 3.6_
  - ✅ **COMPLETO** - AI Analysis gerando insights

- [-] 21. Implementar suporte multi-canal no Discovery

  - Adicionar suporte para WhatsApp (via WhatsApp Tool)
  - Adicionar suporte para formulário web
  - Garantir comportamento consistente entre canais
  - Adaptar formatação de mensagens por canal
  - _Requirements: 3.8_
  - ⚠️ **PARCIAL** - Web form funcional, falta WhatsApp Tool

- [x] 21.2 Registrar Discovery Agent como sub-agente no sistema




  - Criar registro do Discovery Agent na tabela sub_agents
  - Associar com renus_config do cliente
  - Configurar channel como "web" e "whatsapp"
  - Definir topics: ["entrevistas", "pesquisas", "levantamento de requisitos"]
  - Configurar model como "gpt-4o-mini"
  - Copiar system_prompt do Discovery Agent atual
  - Marcar como is_active = true
  - Adicionar ao dropdown de sub-agentes disponíveis no frontend
  - _Requirements: 3.1, 6.2, 12.3_

- [ ]* 21.1 Escrever testes para Discovery
  - Testar fluxo completo de entrevista
  - Testar validação de cada campo
  - Testar geração de AI analysis
  - Testar salvamento em interview_messages
  - Testar multi-canal (mock WhatsApp e web)
  - Testar registro como sub-agente
  - _Requirements: 3.2, 3.4, 3.6, 3.8_

### Phase 7: Services (Lógica de Negócio)

- [x] 22. Criar InterviewService
  - Criar backend/src/services/interview_service.py
  - Implementar create_interview (cria registro com status pending)
  - Implementar get_interview (busca por ID com RLS)
  - Implementar list_interviews (com filtros e paginação)
  - Implementar update_interview (atualiza campos e status)
  - Implementar complete_interview (marca como completed, adiciona ai_analysis)
  - Adicionar validação de transições de status
  - _Requirements: 7.2, 7.3, 7.4_
  - ✅ **COMPLETO** - Service com todas operações CRUD

- [x] 23. Criar InterviewMessageService
  - Adicionar método add_message ao InterviewService
  - Implementar get_messages (com paginação para 50+ mensagens)
  - Validar role (user|assistant|system)
  - Garantir foreign key com interview_id
  - _Requirements: 7.3, 7.6_
  - ✅ **COMPLETO** - Integrado no InterviewService

- [x] 24. Criar SubAgentService


  - Criar backend/src/services/subagent_service.py
  - Implementar create_subagent (validar model e channel)
  - Implementar get_subagent (busca por ID)
  - Implementar list_subagents (filtrar por is_active)
  - Implementar update_subagent (validar campos)
  - Implementar delete_subagent (verificar interviews ativas)
  - Implementar toggle_active (ativar/desativar)
  - _Requirements: 6.2, 6.3, 6.4, 6.6_

- [x] 24.2 Criar RenusConfigService

  - Criar backend/src/services/renus_config_service.py
  - Implementar get_config (busca configuração do cliente)
  - Implementar update_config (atualiza configuração)
  - Implementar get_or_create_config (cria se não existir)
  - Validar estrutura de instructions, guardrails, tools
  - Adicionar suporte a multi-tenant (filtro por client_id)
  - _Requirements: 12.3_

- [x] 24.3 Criar ToolService

  - Criar backend/src/services/tool_service.py
  - Implementar list_tools (listar tools disponíveis)
  - Implementar get_tool (buscar tool por ID)
  - Implementar create_tool (criar nova tool)
  - Implementar update_tool (atualizar tool)
  - Implementar delete_tool (deletar tool)
  - _Requirements: 5.1, 5.4_

- [ ]* 24.1 Escrever testes para services
  - Testar InterviewService com mock Supabase
  - Testar validação de status transitions
  - Testar SubAgentService CRUD completo
  - Testar RenusConfigService get/update
  - Testar ToolService CRUD completo
  - Testar paginação de mensagens
  - _Requirements: 7.2, 7.3, 7.6, 6.2, 12.3_


### Phase 8: LangServe (Exposição de Agentes via API)

- [x] 25. Configurar LangServe app



  - Criar backend/src/langserve/app.py
  - Inicializar FastAPI app separada para LangServe
  - Configurar CORS
  - Adicionar middleware de autenticação
  - Configurar porta separada (8001)
  - _Requirements: 4.2_

- [x] 26. Registrar agentes no LangServe


  - Adicionar rota /agents/renus/invoke
  - Adicionar rota /agents/renus/stream
  - Adicionar rota /agents/isa/invoke
  - Adicionar rota /agents/isa/stream
  - Adicionar rota /agents/discovery/invoke
  - Adicionar rota /agents/discovery/stream
  - Implementar streaming de respostas
  - _Requirements: 4.2_

- [x] 27. Adicionar contexto multi-tenant nas rotas

  - Extrair client_id do token JWT
  - Passar client_id para agentes via context
  - Garantir isolamento de dados por cliente
  - Adicionar client_id aos traces LangSmith
  - _Requirements: 4.4, 12.1, 12.5_

- [ ]* 27.1 Escrever testes de integração LangServe
  - Testar cada endpoint /invoke com payload válido
  - Testar streaming endpoints
  - Testar autenticação (com e sem token)
  - Testar isolamento multi-tenant
  - _Requirements: 4.2, 12.1_

### Phase 9: API Routes (FastAPI Principal)

- [x] 28. Criar rotas de interviews
  - Criar backend/src/api/routes/interviews.py
  - POST /api/interviews - criar entrevista
  - GET /api/interviews - listar entrevistas (com filtros)
  - GET /api/interviews/{id} - buscar entrevista específica
  - PUT /api/interviews/{id} - atualizar entrevista
  - GET /api/interviews/{id}/messages - buscar mensagens (paginado)
  - POST /api/interviews/{id}/messages - adicionar mensagem
  - Adicionar validação de permissões (RLS)
  - _Requirements: 7.4, 7.5, 7.6_
  - ✅ **COMPLETO** - 5 endpoints funcionais (falta PUT e GET messages)


- [x] 29. Criar rotas de sub-agents
  - Criar backend/src/api/routes/subagents.py
  - POST /api/subagents - criar sub-agente
  - GET /api/subagents - listar sub-agentes
  - GET /api/subagents/{id} - buscar sub-agente
  - PUT /api/subagents/{id} - atualizar sub-agente
  - DELETE /api/subagents/{id} - deletar sub-agente
  - PATCH /api/subagents/{id}/toggle - ativar/desativar
  - GET /api/subagents/{id}/stats - estatísticas de uso
  - Restringir acesso a admins
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.7_

- [x] 29.2 Criar rotas de renus-config


  - Criar backend/src/api/routes/renus_config.py
  - GET /api/renus-config - buscar configuração do cliente
  - PUT /api/renus-config - atualizar configuração completa
  - PATCH /api/renus-config/instructions - atualizar apenas instructions
  - PATCH /api/renus-config/guardrails - atualizar apenas guardrails
  - PATCH /api/renus-config/tools - atualizar tools habilitadas
  - GET /api/renus-config/history - histórico de alterações
  - Aplicar RLS por client_id
  - _Requirements: 12.3_


- [x] 29.3 Criar rotas de tools
  - Criar backend/src/api/routes/tools.py
  - GET /api/tools - listar todas as tools disponíveis
  - GET /api/tools/{id} - buscar tool específica
  - POST /api/tools - criar nova tool (admin only)
  - PUT /api/tools/{id} - atualizar tool (admin only)
  - DELETE /api/tools/{id} - deletar tool (admin only)
  - GET /api/tools/enabled - listar tools habilitadas para o cliente
  - _Requirements: 5.1, 5.4_


- [x] 30. Criar rota de chat com ISA
  - Criar backend/src/api/routes/isa.py
  - POST /api/isa/chat - enviar mensagem para ISA
  - GET /api/isa/history - histórico de comandos
  - Restringir acesso a admins
  - Integrar com IsaAgent via LangServe
  - Salvar comandos em isa_commands
  - _Requirements: 2.1, 2.3_


- [x] 31. Integrar rotas no main.py
  - Importar routers de interviews, subagents, renus_config, tools, isa
  - Adicionar routers ao app FastAPI principal
  - Configurar prefixos (/api/interviews, /api/subagents, /api/renus-config, /api/tools, /api/isa)
  - Adicionar tags para documentação Swagger
  - _Requirements: 4.2_

- [ ]* 31.1 Escrever testes de integração das rotas
  - Testar CRUD completo de interviews
  - Testar CRUD completo de sub-agents
  - Testar GET/PUT de renus-config
  - Testar chat com ISA
  - Testar permissões (admin vs client)
  - Testar filtros e paginação
  - _Requirements: 6.1, 7.4, 2.1, 12.1_

### Phase 9B: Backend - Models e Services para Configuração

- [x] 31.2 Criar Pydantic models para renus_config


  - Criar backend/src/models/renus_config.py
  - Implementar RenusConfigBase (system_prompt, model, temperature, max_tokens, guardrails, etc)
  - Implementar RenusConfigUpdate (todos campos opcionais)
  - Implementar RenusConfigResponse
  - Adicionar validação de system_prompt (não vazio)
  - Adicionar validação de model (lista de modelos suportados)
  - Adicionar validação de temperature (0-2), max_tokens (1-4096)
  - _Requirements: 11.4, 12.3_

- [x] 31.3 Criar Pydantic models para tools


  - Criar backend/src/models/tool.py
  - Implementar ToolBase (name, description, function_name, parameters_schema, is_active)
  - Implementar ToolCreate
  - Implementar ToolUpdate
  - Implementar ToolResponse
  - Adicionar validação de parameters_schema (JSON válido)
  - _Requirements: 5.1, 5.4_

- [x] 31.4 Criar RenusConfigService




  - Criar backend/src/services/renus_config_service.py
  - Implementar get_config(client_id) - busca configuração do cliente
  - Implementar update_config(client_id, data) - atualiza configuração
  - Implementar update_instructions(client_id, data) - atualiza apenas system_prompt
  - Implementar update_guardrails(client_id, data) - atualiza apenas guardrails
  - Implementar update_advanced(client_id, data) - atualiza temperature, max_tokens, etc
  - Implementar create_default_config(client_id) - cria config padrão se não existir
  - Adicionar validação de client_id
  - Garantir isolamento multi-tenant
  - _Requirements: 12.1, 12.3_


- [x] 31.5 Criar ToolService




  - Criar backend/src/services/tool_service.py
  - Implementar list_tools() - lista todas as tools disponíveis
  - Implementar get_tool(tool_id) - busca tool específica
  - Implementar create_tool(data) - cria nova tool (admin only)
  - Implementar update_tool(tool_id, data) - atualiza tool (admin only)
  - Implementar delete_tool(tool_id) - deleta tool (admin only)
  - Implementar get_enabled_tools(client_id) - lista tools habilitadas para cliente
  - _Requirements: 5.1, 5.4_

- [x] 31.6 Atualizar rotas de renus_config (task 29.2)


  - Implementar GET /api/renus-config usando RenusConfigService
  - Implementar PUT /api/renus-config
  - Implementar PATCH /api/renus-config/instructions
  - Implementar PATCH /api/renus-config/guardrails
  - Implementar PATCH /api/renus-config/advanced
  - Adicionar middleware de autenticação
  - Aplicar RLS por client_id do token JWT
  - _Requirements: 12.1, 12.2, 12.3_



- [x] 31.7 Atualizar rotas de tools (task 29.3)


  - Implementar GET /api/tools usando ToolService
  - Implementar GET /api/tools/{id}
  - Implementar POST /api/tools (admin only)
  - Implementar PUT /api/tools/{id} (admin only)
  - Implementar DELETE /api/tools/{id} (admin only)
  - Implementar GET /api/tools/enabled (tools do cliente)
  - _Requirements: 5.1, 5.4_

### Phase 9C: Frontend - Integração com Configuração RENUS

- [x] 31.8 Criar service de renus_config no frontend


  - Criar frontend/src/services/renusConfigService.ts
  - Implementar getConfig() - busca configuração do cliente
  - Implementar updateConfig(data) - atualiza configuração completa
  - Implementar updateInstructions(data) - atualiza apenas system_prompt
  - Implementar updateGuardrails(data) - atualiza apenas guardrails
  - Implementar updateAdvanced(data) - atualiza temperature, max_tokens, etc
  - Adicionar tipos TypeScript completos (RenusConfig interface)
  - Adicionar tratamento de erros
  - _Requirements: 11.1, 11.4_


- [x] 31.9 Criar service de tools no frontend


  - Criar frontend/src/services/toolService.ts
  - Implementar getAll() - lista todas as tools
  - Implementar getById(id) - busca tool específica
  - Implementar getEnabled() - lista tools habilitadas para o cliente
  - Implementar create(data) - cria nova tool (admin)
  - Implementar update(id, data) - atualiza tool (admin)
  - Implementar delete(id) - deleta tool (admin)
  - Adicionar tipos TypeScript (Tool interface)
  - _Requirements: 5.1_

- [x] 31.10 Conectar InstructionsTab com backend



  - Atualizar frontend/src/components/renus-config/InstructionsTab.tsx
  - Substituir dados mock por renusConfigService.getConfig()
  - Implementar save usando renusConfigService.updateInstructions()
  - Adicionar loading states (skeleton)
  - Adicionar error handling com toast
  - Mostrar toast de sucesso ao salvar
  - Adicionar debounce no auto-save (opcional)
  - _Requirements: 11.1, 11.2_

- [x] 31.11 Conectar GuardrailsTab com backend

  - Atualizar frontend/src/components/renus-config/GuardrailsTab.tsx
  - Substituir dados mock por renusConfigService.getConfig()
  - Implementar save usando renusConfigService.updateGuardrails()
  - Adicionar toggle para ativar/desativar cada guardrail
  - Implementar configuração de content_filters, rate_limits, etc
  - Adicionar loading states e error handling
  - _Requirements: 11.1_


- [x] 31.12 Conectar AdvancedTab com backend
  - Atualizar frontend/src/components/renus-config/AdvancedTab.tsx
  - Substituir dados mock por renusConfigService.getConfig()
  - Implementar save usando renusConfigService.updateAdvanced()
  - Adicionar sliders para temperature (0-2), max_tokens (1-4096), top_p (0-1)
  - Adicionar validação de ranges
  - Mostrar valores atuais em tempo real
  - Adicionar loading states e error handling
  - _Requirements: 11.4_


- [x] 31.13 Conectar ToolsTab com backend
  - Atualizar frontend/src/components/renus-config/ToolsTab.tsx
  - Substituir dados mock por toolService.getAll()
  - Implementar listagem de tools disponíveis
  - Implementar toggle para ativar/desativar tools
  - Mostrar descrição, parâmetros e status de cada tool
  - Adicionar filtro por categoria (Supabase, WhatsApp, Email, etc)
  - Adicionar loading states e error handling
  - Implementar criação de novas tools com validação
  - Implementar teste de tools
  - Implementar delete de tools customizadas
  - _Requirements: 5.1, 6.5_

- [x] 31.14 Conectar SubAgentsTab com backend real
  - Atualizar frontend/src/components/renus-config/SubAgentsTab.tsx
  - Substituir dados mock por subagentService.getAll()
  - Implementar listagem de sub-agentes do cliente
  - Adicionar botão "Novo Sub-Agente" que abre modal
  - Implementar cards de sub-agentes com status, canal, modelo
  - Adicionar ações: Editar, Deletar, Toggle ativo/inativo

  - Sincronizar com backend via SubAgentService
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [x] 31.15 Implementar modal de criação de sub-agente
  - Criar componente SubAgentModal.tsx (conforme imagem fornecida)
  - Campo "Nome do Sub-Agente" (text input obrigatório)
  - Campo "Descrição" (textarea)
  - Campo "Canal de Atendimento" (radio: WhatsApp / Site)
  - Campo "Modelo de IA" (select: Padrão do Agente Principal / Recomendado / outros)
  - Campo "Prompt Base (System Prompt)" (textarea grande)
  - Campo "Tópicos/Contextos Principais" (tags input com botão Adicionar)
  - Seção "Fine-tuning (Otimização Avançada)" com:
    - Slider "Economia" (-90%)
    - Slider "Streaming" (50)
    - Slider "Samples" (50)
    - Link "Dataset de Treinamento (JSON)"
    - Checkbox "Aguardando definição do fine-tuning"
  - Info box "Como funciona" explicando fine-tuning
  - Toggle "Status Inicial" (ativar imediatamente após criação)
  - Botões "Cancelar" e "Criar Sub-Agente"

  - Validação de campos obrigatórios
  - Integração com subagentService.create()
  - _Requirements: 6.2, 6.3_

- [x] 31.16 Atualizar RenusConfigPage com estado global
  - Atualizar frontend/src/pages/dashboard/RenusConfigPage.tsx
  - Implementar estado global de "unsaved changes"
  - Detectar mudanças em qualquer aba
  - Atualizar badge "Alterações Não Salvas" / "Configuração Publicada"
  - Implementar botão "Salvar e Publicar" que salva todas as abas
  - Adicionar confirmação antes de sair com mudanças não salvas
  - Atualizar painel de status com dados reais do backend
  - _Requirements: 11.1_

- [ ]* 31.17 Escrever testes de integração frontend-backend
  - Testar fluxo completo: carregar config → editar → salvar
  - Testar InstructionsTab: carregar, editar system_prompt, salvar
  - Testar GuardrailsTab: toggle guardrails, salvar
  - Testar AdvancedTab: ajustar sliders, salvar
  - Testar ToolsTab: listar tools, toggle ativo/inativo
  - Testar SubAgentsTab: criar, editar, deletar sub-agente
  - Testar isolamento multi-tenant (cliente A não vê config de B)
  - _Requirements: 11.1, 12.1_
  - Testar CRUD completo de tools
  - Testar chat com ISA
  - Testar permissões (admin vs client)
  - Testar filtros e paginação
  - Testar RLS multi-tenant
  - _Requirements: 6.1, 7.4, 2.1, 12.3_


### Phase 10: Frontend - UI de Gerenciamento de Sub-Agentes

- [x] 32. Criar página de listagem de sub-agentes

  - Criar frontend/src/pages/subagents/SubAgentsPage.tsx
  - Implementar tabela com colunas: name, description, channel, model, status, actions
  - Adicionar filtros por channel e status
  - Adicionar botão "Novo Sub-Agente"
  - Implementar toggle de ativação (switch)
  - Adicionar ações: editar, deletar, ver detalhes
  - _Requirements: 6.1_


- [x] 33. Conectar modal de sub-agente ao backend
  - Atualizar frontend/src/components/subagents/SubAgentModal.tsx (já existe)
  - Remover dados mock, usar API real
  - Conectar campo "Nome do Sub-Agente" ao backend
  - Conectar campo "Descrição" ao backend
  - Conectar seletor "Canal de Atendimento" (WhatsApp/Site)
  - Conectar seletor "Modelo de IA" com modelos disponíveis
  - Conectar textarea "Prompt Base (System Prompt)"
  - Conectar campo "Tópicos/Contextos Principais" (tags)
  - Implementar seção "Fine-tuning (Otimização Avançada)"
  - Conectar toggle "Status Inicial" (ativo/inativo)
  - Implementar validação de todos os campos
  - Adicionar preview do comportamento do agente
  - _Requirements: 6.2, 6.3_


- [x] 34. Criar página de detalhes de sub-agente
  - Criar frontend/src/pages/subagents/SubAgentDetails.tsx
  - Mostrar todas as informações do sub-agente
  - Mostrar estatísticas de uso (total interviews, completion rate)
  - Mostrar últimas entrevistas conduzidas
  - Botões para editar e deletar
  - _Requirements: 6.7_

- [x] 35. Criar service de sub-agentes no frontend
  - Criar frontend/src/services/subagentService.ts
  - Implementar funções: getAll, getById, create, update, delete, toggleActive, getStats
  - Adicionar tratamento de erros
  - Adicionar tipos TypeScript
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [x] 36. Adicionar rotas de sub-agentes no App


  - Atualizar frontend/src/App.tsx
  - Adicionar rota /subagents (listagem)
  - Adicionar rota /subagents/new (criar)
  - Adicionar rota /subagents/:id (detalhes)
  - Adicionar rota /subagents/:id/edit (editar)
  - Adicionar link no menu lateral
  - _Requirements: 6.1_

### Phase 10.5: Frontend - Configuração RENUS e ISA (NOVO)

- [x] 36.2 Conectar InstructionsTab ao backend

  - Atualizar frontend/src/pages/config/InstructionsTab.tsx
  - Remover dados mock, usar API real
  - Implementar GET /api/renus-config para carregar instruções
  - Implementar PATCH /api/renus-config/instructions para salvar
  - Adicionar loading states e error handling
  - Mostrar feedback de sucesso/erro ao salvar
  - _Requirements: 12.3_


- [x] 36.3 Conectar GuardrailsTab ao backend
  - Atualizar frontend/src/pages/config/GuardrailsTab.tsx
  - Remover dados mock, usar API real
  - Implementar GET /api/renus-config para carregar guardrails
  - Implementar PATCH /api/renus-config/guardrails para salvar
  - Adicionar validação de regras antes de salvar
  - Mostrar preview de como guardrails afetam respostas
  - _Requirements: 12.3_


- [x] 36.4 Conectar ToolsTab ao backend
  - Atualizar frontend/src/pages/config/ToolsTab.tsx
  - Remover dados mock, usar API real
  - Implementar GET /api/tools para listar tools disponíveis
  - Implementar GET /api/renus-config para ver tools habilitadas
  - Implementar PATCH /api/renus-config/tools para habilitar/desabilitar
  - Adicionar descrição e exemplos de uso de cada tool

  - _Requirements: 5.1, 12.3_

- [x] 36.5 Conectar StatusTab ao backend
  - Atualizar frontend/src/pages/config/StatusTab.tsx
  - Remover dados mock, usar API real
  - Implementar GET /api/renus-config para status da configuração
  - Mostrar última atualização, versão, status de sincronização
  - Adicionar botão para testar configuração (dry-run)

  - Mostrar métricas de uso do RENUS (chamadas, tokens, custo)
  - _Requirements: 10.1, 12.3_

- [x] 36.6 Conectar IntegrationTab ao backend
  - Atualizar frontend/src/pages/config/IntegrationTab.tsx
  - Remover dados mock, usar API real
  - Implementar configuração de canais (WhatsApp, SMS, Email)
  - Implementar teste de conexão com cada canal

  - Mostrar status de webhooks e APIs externas
  - Adicionar logs de integrações recentes
  - _Requirements: 9.1, 9.5_

- [x] 36.7 Criar service de configuração no frontend
  - Criar frontend/src/services/renusConfigService.ts
  - Implementar getConfig() - buscar configuração completa
  - Implementar updateInstructions() - atualizar instruções
  - Implementar updateGuardrails() - atualizar guardrails
  - Implementar updateTools() - atualizar tools habilitadas

  - Implementar getHistory() - histórico de alterações
  - Implementar testConfig() - testar configuração
  - Adicionar tipos TypeScript completos
  - _Requirements: 12.3_

- [x] 36.8 Criar service de tools no frontend
  - Criar frontend/src/services/toolService.ts
  - Implementar getAll() - listar todas as tools
  - Implementar getById() - buscar tool específica
  - Implementar getEnabled() - tools habilitadas para o cliente
  - Implementar create() - criar nova tool (admin)
  - Implementar update() - atualizar tool (admin)
  - Implementar delete() - deletar tool (admin)
  - Adicionar tipos TypeScript
  - _Requirements: 5.1_

### Phase 11: Frontend - Sistema de Entrevistas

- [x] 37. Criar página de listagem de entrevistas



  - Criar frontend/src/pages/interviews/InterviewsPage.tsx
  - Implementar tabela com: lead name, sub-agent, status, start date, completion date
  - Adicionar filtros por status, date range, sub-agent
  - Adicionar busca por nome ou telefone
  - Adicionar botão "Nova Entrevista"
  - Implementar paginação
  - _Requirements: 8.1, 8.5_
  - ✅ **COMPLETO** - Página admin funcional



- [x] 38. Criar página de detalhes de entrevista


  - Criar frontend/src/pages/interviews/InterviewDetails.tsx
  - Mostrar thread completo de mensagens (chat-like)
  - Mostrar painel com dados estruturados coletados
  - Mostrar AI analysis destacada
  - Adicionar botão de exportar (CSV/JSON)
  - Implementar scroll infinito para mensagens
  - _Requirements: 8.2, 8.3, 8.4_
  - ✅ **COMPLETO** - Visualização completa implementada

- [x] 39. Criar formulário web de entrevista
  - Criar frontend/src/pages/interviews/InterviewForm.tsx
  - Interface de chat para conduzir entrevista
  - Mostrar progresso (campos coletados vs faltantes)
  - Enviar mensagens para Discovery agent via API
  - Receber respostas em tempo real (streaming)
  - Mostrar indicador de "digitando..."
  - _Requirements: 3.8, 8.2_
  - ✅ **COMPLETO** - Chat UI funcional com progresso

- [x] 40. Criar service de entrevistas no frontend
  - Criar frontend/src/services/interviewService.ts
  - Implementar funções: getAll, getById, create, update, getMessages, addMessage, export
  - Adicionar suporte a filtros e paginação
  - Adicionar tipos TypeScript
  - _Requirements: 8.1, 8.5, 8.6_
  - ✅ **COMPLETO** - Service com todas operações


- [x] 41. Adicionar rotas de entrevistas no App
  - Atualizar frontend/src/App.tsx
  - Adicionar rota /interviews (listagem)
  - Adicionar rota /interviews/new (criar/conduzir)
  - Adicionar rota /interviews/:id (detalhes)
  - Adicionar link no menu lateral
  - _Requirements: 8.1_



### Phase 12: Frontend - Interface ISA

- [x] 42. Criar componente de chat com ISA
  - Criar frontend/src/components/isa/IsaChat.tsx
  - Interface de chat similar a ChatGPT
  - Campo de input com sugestões de comandos
  - Histórico de mensagens

  - Indicador de "processando..."
  - Formatação especial para tabelas e listas nas respostas
  - _Requirements: 2.1, 2.6_

- [x] 43. Integrar ISA no dashboard admin
  - Adicionar componente IsaChat no AdminDashboard

  - Posicionar em sidebar ou modal
  - Adicionar atalho de teclado para abrir (Ctrl+K)
  - Persistir histórico na sessão
  - _Requirements: 2.1_

- [x] 44. Criar service de ISA no frontend
  - Criar frontend/src/services/isaService.ts
  - Implementar função sendMessage (com streaming)
  - Implementar função getHistory
  - Adicionar tipos TypeScript
  - _Requirements: 2.1_

### Phase 13: Testes e Validação

- [ ] 45. Checkpoint - Executar todos os testes unitários
  - Executar pytest para todos os testes unitários
  - Verificar cobertura de código (mínimo 70%)
  - Corrigir testes falhando
  - Documentar testes que foram pulados (se houver)
  - _Requirements: All_

- [ ] 46. Executar testes de integração
  - Testar fluxo completo: criar entrevista → conduzir → completar → gerar análise
  - Testar RENUS roteando para Discovery
  - Testar ISA executando comandos
  - Testar isolamento multi-tenant
  - Verificar traces no LangSmith
  - _Requirements: 1.1, 2.1, 3.1, 12.1_

- [ ]* 47. Escrever testes property-based
  - **Property 1: RENUS routing consistency** - Validar que mesma mensagem + contexto = mesma decisão
  - **Property 3: Discovery field completeness** - Validar que entrevistas completed têm todos os campos
  - **Property 6: Multi-tenant isolation** - Validar que client_ids diferentes não veem dados uns dos outros
  - **Property 12: Interview status transitions** - Validar transições válidas de status
  - Configurar hypothesis com 100+ iterações
  - _Requirements: 1.1, 3.2, 12.1, 7.2_

- [ ] 48. Testes manuais end-to-end
  - Criar sub-agente Discovery via UI
  - Iniciar entrevista via formulário web
  - Completar entrevista respondendo todas as perguntas
  - Verificar AI analysis gerada
  - Testar ISA com comando "list interviews"
  - Testar ISA com comando "generate report"
  - Verificar traces no LangSmith dashboard
  - _Requirements: All_

### Phase 14: Documentação e Finalização

- [x] 49. Atualizar documentação da API
  - Atualizar docstrings de todos os endpoints
  - Verificar Swagger UI (/docs) está completo
  - Adicionar exemplos de request/response
  - Documentar códigos de erro
  - _Requirements: 4.2_

- [x] 50. Criar guia de configuração de API keys
  - Documentar como obter OPENAI_API_KEY
  - Documentar como obter ANTHROPIC_API_KEY
  - Documentar como obter LANGSMITH_API_KEY
  - Criar checklist de configuração
  - Adicionar troubleshooting comum
  - _Requirements: 11.5_

- [x] 51. Criar guia de uso dos agentes
  - Documentar como criar sub-agentes
  - Documentar como conduzir entrevistas
  - Documentar comandos disponíveis da ISA
  - Adicionar exemplos práticos
  - Criar FAQ
  - _Requirements: 2.6, 3.1, 6.2_

- [x] 52. Checkpoint Final - Validação completa
  - Verificar que todas as tabelas necessárias existem
  - Verificar que todas as migrations foram aplicadas
  - Verificar que todos os testes passam
  - Verificar que LangSmith está capturando traces
  - Verificar que frontend está funcionando
  - Verificar que documentação está completa
  - Fazer demo completo do sistema
  - _Requirements: All_

---

## Notas de Implementação

### Ordem de Execução
As tasks devem ser executadas sequencialmente dentro de cada phase. Phases podem ter alguma sobreposição, mas recomenda-se completar uma phase antes de iniciar a próxima.

### Tasks Opcionais (marcadas com *)
Tasks marcadas com * são opcionais e focam em testes. Podem ser puladas para MVP mais rápido, mas são recomendadas para qualidade.

### Checkpoints
Tasks 45, 48 e 52 são checkpoints onde todos os testes devem passar antes de prosseguir.

### Dependências Externas
- OpenAI API key (obrigatória)
- Anthropic API key (obrigatória)
- LangSmith API key (obrigatória)
- WhatsApp provider (opcional neste sprint - abstração apenas)

### Estimativa de Tempo
- Phases 1-3: ~8 horas (Infraestrutura + Database + Tools)
- Phases 4-6: ~16 horas (RENUS + ISA + Discovery)
- Phase 7: ~6 horas (Services)
- Phase 8-9: ~10 horas (LangServe + API Routes base)
- **Phase 9B-9C: ~10 horas (Integração RENUS Config + Frontend)** ⭐ NOVO
- Phases 10-12: ~12 horas (Frontend Sub-Agentes + Interviews + ISA)
- Phases 13-14: ~8 horas (Testes + Documentação)
- **Total: ~70 horas** (2 semanas para 1 desenvolvedor)

---

**Implementation Plan Version:** 1.0  
**Last Updated:** 2025-11-29  
**Status:** Ready for Execution
