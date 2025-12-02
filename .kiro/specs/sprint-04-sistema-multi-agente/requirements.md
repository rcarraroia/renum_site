# Requirements Document - Sprint 04: Sistema Multi-Agente

## Introduction

Este documento especifica os requisitos para implementação do sistema multi-agente do RENUM, incluindo o agente principal RENUS (orquestrador), a assistente administrativa ISA, e o primeiro sub-agente especializado Discovery para condução de entrevistas estruturadas. O sistema utilizará LangChain/LangGraph para orquestração, LangServe para exposição de APIs, e LangSmith para observabilidade completa.

## Glossary

- **RENUS**: Agente principal orquestrador que roteia conversas para sub-agentes especializados
- **ISA**: Intelligent System Assistant - assistente administrativa separada do RENUS para comandos internos
- **Discovery Agent**: Sub-agente especializado em conduzir entrevistas estruturadas de levantamento de requisitos
- **LangGraph**: Framework para construção de fluxos de agentes com estados e transições
- **LangChain**: Framework para desenvolvimento de aplicações com LLMs
- **LangServe**: Biblioteca para expor agentes LangChain como APIs REST
- **LangSmith**: Plataforma de observabilidade para rastreamento de interações com LLMs
- **WhatsApp Provider**: Interface abstrata para integração com APIs de WhatsApp
- **Tool**: Ferramenta que um agente pode invocar para executar ações específicas
- **System Prompt**: Instruções base que definem o comportamento de um agente
- **Multi-tenant**: Arquitetura que permite isolamento de dados entre diferentes clientes
- **Interview**: Sessão de entrevista estruturada conduzida por um sub-agente
- **Interview Message**: Mensagem individual dentro de uma entrevista (pergunta ou resposta)

## Requirements

### Requirement 1: RENUS - Agente Principal Orquestrador

**User Story:** As a system, I want an orchestrator agent that routes conversations to specialized sub-agents, so that each interaction is handled by the most appropriate agent.

#### Acceptance Criteria

1. WHEN a user message is received, THE RENUS SHALL analyze the message content and determine the appropriate sub-agent to handle it
2. WHEN no specialized sub-agent is suitable, THE RENUS SHALL handle the conversation directly using general-purpose responses
3. WHEN a sub-agent completes its task, THE RENUS SHALL receive control back and decide the next action
4. WHEN a sub-agent encounters an error or cannot proceed, THE RENUS SHALL implement fallback logic to either retry, switch agents, or escalate to human
5. WHEN routing decisions are made, THE RENUS SHALL log all decisions with reasoning to LangSmith for observability
6. WHEN managing conversation context, THE RENUS SHALL maintain state across multiple turns and sub-agent delegations

### Requirement 2: ISA - Assistente Administrativa Interna

**User Story:** As an administrator, I want a conversational assistant in the admin dashboard that can execute administrative commands, so that I can manage the system efficiently through natural language.

#### Acceptance Criteria

1. WHEN an admin sends a message to ISA, THE System SHALL process the message as a potential administrative command
2. WHEN ISA identifies a valid command, THE System SHALL execute the command with appropriate database access using service role permissions
3. WHEN ISA executes a command, THE System SHALL record the command, response, and execution status in the isa_commands table for audit purposes
4. WHEN ISA generates reports, THE System SHALL query relevant data from Supabase and format results in a readable format
5. WHEN ISA sends bulk messages, THE System SHALL queue messages appropriately and provide progress feedback
6. WHEN ISA cannot understand a command, THE System SHALL provide helpful suggestions and examples of valid commands
7. WHEN ISA accesses sensitive data, THE System SHALL verify admin role and log all access attempts

### Requirement 3: Discovery Sub-Agent - Entrevistas Estruturadas

**User Story:** As a client, I want a sub-agent that conducts structured interviews with my leads, so that I can gather consistent and comprehensive information about their needs and background.

#### Acceptance Criteria

1. WHEN an interview is initiated, THE Discovery Agent SHALL create an interview record with status 'pending' in the interviews table
2. WHEN conducting an interview, THE Discovery Agent SHALL collect mandatory fields: contact_name, contact_phone, email, country, company, niche_experience, current_rank, operation_size
3. WHEN asking questions, THE Discovery Agent SHALL follow a structured flow while maintaining conversational flexibility
4. WHEN a lead provides an answer, THE Discovery Agent SHALL save each message in the interview_messages table with appropriate role (user/assistant)
5. WHEN an interview is completed, THE Discovery Agent SHALL update the interview status to 'completed' and generate an AI analysis summary in the ai_analysis field
6. WHEN generating analysis, THE Discovery Agent SHALL extract key insights, identify patterns, and provide actionable recommendations
7. WHEN an interview is interrupted, THE Discovery Agent SHALL save progress and allow resumption from the last question
8. WHEN operating multi-channel, THE Discovery Agent SHALL support both WhatsApp and web form interfaces with consistent behavior

### Requirement 4: Infraestrutura LangGraph e LangServe

**User Story:** As a developer, I want a robust infrastructure for agent orchestration and API exposure, so that agents can be easily integrated and monitored.

#### Acceptance Criteria

1. WHEN the system starts, THE System SHALL initialize LangGraph with proper state management and checkpointing capabilities
2. WHEN agents are exposed via LangServe, THE System SHALL provide REST endpoints with streaming support for real-time responses
3. WHEN LangSmith is configured, THE System SHALL trace all LLM calls, agent decisions, and tool invocations automatically
4. WHEN multiple tenants use the system, THE System SHALL isolate data and context appropriately using client_id filtering
5. WHEN agents invoke tools, THE System SHALL provide standardized tool interfaces for Supabase queries, WhatsApp messaging, and email notifications
6. WHEN errors occur in agent execution, THE System SHALL capture detailed error context and provide meaningful error messages

### Requirement 5: Tools Customizadas

**User Story:** As an agent, I want access to specialized tools for database queries, messaging, and notifications, so that I can perform actions beyond text generation.

#### Acceptance Criteria

1. WHEN an agent needs to query data, THE Supabase Tool SHALL execute SQL queries with proper RLS enforcement based on the user context
2. WHEN an agent needs to send a WhatsApp message, THE WhatsApp Tool SHALL use the configured provider through an abstract interface
3. WHEN an agent needs to send an email, THE Email Tool SHALL compose and send emails using the configured email service
4. WHEN tools are invoked, THE System SHALL validate input parameters against defined schemas before execution
5. WHEN tools fail, THE System SHALL return structured error information that agents can interpret and handle
6. WHEN tools access external services, THE System SHALL implement retry logic with exponential backoff for transient failures

### Requirement 6: UI de Gerenciamento de Sub-Agentes

**User Story:** As an administrator, I want a dashboard interface to manage sub-agents, so that I can create, configure, and monitor specialized agents without code changes.

#### Acceptance Criteria

1. WHEN viewing the sub-agents page, THE System SHALL display a list of all sub-agents with their name, description, channel, status, and last updated date
2. WHEN creating a sub-agent, THE System SHALL provide a form to input name, description, channel, model, system_prompt, topics, and initial status
3. WHEN editing a sub-agent, THE System SHALL load current configuration and allow modification of all fields except id
4. WHEN activating or deactivating a sub-agent, THE System SHALL update the is_active field and immediately affect routing decisions
5. WHEN configuring a sub-agent, THE System SHALL validate that the selected model is available and the system_prompt is not empty
6. WHEN deleting a sub-agent, THE System SHALL check for active interviews and prevent deletion if interviews are in progress
7. WHEN viewing sub-agent details, THE System SHALL show usage statistics including total interviews conducted and completion rate

### Requirement 7: Sistema de Entrevistas - Backend

**User Story:** As a system, I want a complete interview management system, so that structured data collection is reliable and scalable.

#### Acceptance Criteria

1. WHEN the interviews table is accessed, THE System SHALL have columns: id, lead_id, subagent_id, contact_name, contact_phone, email, country, company, niche_experience, current_rank, operation_size, status, started_at, completed_at, topics_covered, ai_analysis, created_at, updated_at
2. WHEN creating an interview, THE System SHALL validate that lead_id exists and subagent_id references an active sub-agent
3. WHEN saving interview messages, THE System SHALL enforce foreign key relationship with interviews table and validate role is one of: user, assistant, system
4. WHEN querying interviews, THE System SHALL support filtering by status, date range, sub-agent, and lead
5. WHEN generating reports, THE System SHALL aggregate interview data with proper joins to leads, sub_agents, and interview_messages tables
6. WHEN an interview reaches 50+ messages, THE System SHALL implement pagination for message retrieval to maintain performance

### Requirement 8: Sistema de Entrevistas - Frontend

**User Story:** As an administrator, I want a web interface to view and analyze interviews, so that I can monitor data collection and extract insights.

#### Acceptance Criteria

1. WHEN viewing the interviews dashboard, THE System SHALL display a list of interviews with lead name, sub-agent, status, start date, and completion date
2. WHEN clicking on an interview, THE System SHALL show the complete conversation thread with all messages in chronological order
3. WHEN viewing interview details, THE System SHALL display all collected structured data fields in a formatted panel
4. WHEN an interview has AI analysis, THE System SHALL render the analysis prominently with key insights highlighted
5. WHEN filtering interviews, THE System SHALL support filters by status, date range, sub-agent, and search by lead name or phone
6. WHEN exporting interview data, THE System SHALL generate CSV or JSON files with all interview details and messages

### Requirement 9: Abstração WhatsApp Provider

**User Story:** As a developer, I want an abstract WhatsApp provider interface, so that the system can easily switch between different WhatsApp API providers without code changes in agents.

#### Acceptance Criteria

1. WHEN defining the WhatsApp provider interface, THE System SHALL specify abstract methods: send_message, send_media, handle_webhook, get_message_status
2. WHEN implementing a provider, THE System SHALL ensure all abstract methods are implemented with consistent return types
3. WHEN sending messages, THE System SHALL accept phone number in international format and message content as parameters
4. WHEN receiving webhooks, THE System SHALL parse the provider-specific payload and return a standardized Message object
5. WHEN the provider is not configured, THE System SHALL raise a clear configuration error with instructions
6. WHEN switching providers, THE System SHALL require only environment variable changes without code modifications

### Requirement 10: Observabilidade com LangSmith

**User Story:** As a developer, I want complete observability of all agent interactions, so that I can debug issues, optimize performance, and understand agent behavior.

#### Acceptance Criteria

1. WHEN any agent makes an LLM call, THE System SHALL automatically trace the call to LangSmith with input, output, and metadata
2. WHEN agents make routing decisions, THE System SHALL log the decision reasoning and selected sub-agent to LangSmith
3. WHEN tools are invoked, THE System SHALL trace tool name, input parameters, and execution results to LangSmith
4. WHEN errors occur, THE System SHALL capture full error context including stack traces in LangSmith traces
5. WHEN viewing traces in LangSmith, THE System SHALL organize traces by conversation_id for easy debugging of multi-turn interactions
6. WHEN analyzing performance, THE System SHALL tag traces with environment (development/production) and agent type for filtering

### Requirement 11: Configuração de Modelos de IA

**User Story:** As an administrator, I want flexible model configuration per agent, so that I can optimize cost and performance for different use cases.

#### Acceptance Criteria

1. WHEN RENUS is initialized, THE System SHALL use GPT-4-turbo-preview as the default model for orchestration decisions
2. WHEN ISA is initialized, THE System SHALL use Claude-3-5-sonnet as the default model for administrative commands
3. WHEN Discovery agent is initialized, THE System SHALL use GPT-4o-mini as the default model for cost-effective interviews
4. WHEN a sub-agent is created, THE System SHALL allow selection of model from available options: GPT-4, GPT-4-turbo, GPT-4o-mini, Claude-3-5-sonnet, Claude-3-opus
5. WHEN API keys are missing, THE System SHALL fail fast at startup with clear error messages indicating which keys are required
6. WHEN switching models, THE System SHALL validate that the selected model is compatible with the agent's system prompt and tools

### Requirement 12: Multi-tenant e Isolamento de Dados

**User Story:** As a client, I want complete data isolation from other clients, so that my conversations and interviews remain private and secure.

#### Acceptance Criteria

1. WHEN querying interviews, THE System SHALL automatically filter by client_id derived from the authenticated user
2. WHEN agents access data through tools, THE System SHALL enforce RLS policies that restrict access to the client's data only
3. WHEN creating sub-agents, THE System SHALL associate them with the client's renus_config for proper isolation
4. WHEN ISA executes admin commands, THE System SHALL bypass RLS only for users with admin role in the profiles table
5. WHEN logging to LangSmith, THE System SHALL include client_id in metadata for filtering and analysis without exposing sensitive data
6. WHEN errors occur, THE System SHALL ensure error messages do not leak information about other clients' data
