# Requirements Document - Sprint 06

## Introduction

Este documento define os requisitos para o **Wizard de Criação de Agentes**, uma interface guiada que permite clientes B2B e B2C criarem agentes de IA especializados sem conhecimento técnico. O wizard simplifica o processo de configuração em 5 etapas intuitivas, desde a definição do objetivo até a publicação do agente.

## Glossary

- **Agent**: Agente de IA conversacional especializado criado por um cliente
- **Wizard**: Interface guiada passo-a-passo para criação de agentes
- **Template**: Configuração pré-definida de agente para casos de uso específicos
- **Sandbox**: Ambiente isolado para testar agente antes da publicação
- **Custom Field**: Campo adicional configurável para coleta de informações
- **Client**: Empresa ou distribuidor que usa a plataforma RENUM
- **Lead**: Usuário final que interage com o agente
- **Integration**: Conexão com serviço externo (WhatsApp, Email, Database)
- **System Prompt**: Instrução que define comportamento e personalidade do agente
- **Slug**: Identificador único URL-friendly do agente
- **Embed Code**: Código HTML para incorporar agente em site externo
- **QR Code**: Código QR que redireciona para conversa com agente

## Requirements

### Requirement 1

**User Story:** As a B2B client, I want to create multiple specialized agents for different purposes (customer service, sales, support), so that I can automate different areas of my business.

#### Acceptance Criteria

1. WHEN a B2B client accesses the agent creation page THEN the System SHALL display a wizard with 5 sequential steps
2. WHEN a B2B client completes all wizard steps THEN the System SHALL create a new agent associated with the client's account
3. WHEN a B2B client creates an agent THEN the System SHALL allow selection from predefined templates (Customer Service, Sales, Support, Recruitment, Custom)
4. WHEN a B2B client creates multiple agents THEN the System SHALL maintain independent configurations for each agent
5. WHEN a B2B client saves wizard progress THEN the System SHALL persist the data and allow resuming later

### Requirement 2

**User Story:** As a B2C client (MMN distributor), I want to create a single agent to qualify leads, so that I can automate my recruitment process.

#### Acceptance Criteria

1. WHEN a B2C client accesses the agent creation page THEN the System SHALL display the same wizard interface as B2B clients
2. WHEN a B2C client selects the Recruitment template THEN the System SHALL pre-configure fields for lead qualification (name, phone, experience, interest)
3. WHEN a B2C client creates an agent THEN the System SHALL limit creation to one active agent per B2C account
4. WHEN a B2C client attempts to create a second agent THEN the System SHALL display an upgrade prompt to B2B plan
5. WHEN a B2C client completes agent creation THEN the System SHALL generate a public link and QR code for sharing

### Requirement 3

**User Story:** As a client, I want to choose from predefined templates, so that I can quickly set up an agent without starting from scratch.

#### Acceptance Criteria

1. WHEN a client reaches Step 1 of the wizard THEN the System SHALL display 5 template options (Customer Service, Sales, Support, Recruitment, Custom)
2. WHEN a client selects a template THEN the System SHALL pre-populate personality, tone, and default fields based on the template
3. WHEN a client selects the Custom template THEN the System SHALL allow full customization without pre-populated values
4. WHEN a client selects a non-Custom template THEN the System SHALL allow modification of all pre-populated values in subsequent steps
5. WHEN a client views a template THEN the System SHALL display a description of the template's purpose and typical use cases

### Requirement 4

**User Story:** As a client, I want to define my agent's personality and communication tone, so that it aligns with my brand voice.

#### Acceptance Criteria

1. WHEN a client reaches Step 2 of the wizard THEN the System SHALL display personality options (Professional, Friendly, Technical, Casual)
2. WHEN a client selects a personality THEN the System SHALL adjust the system prompt to reflect the chosen personality
3. WHEN a client adjusts the tone slider (formal vs informal, direct vs descriptive) THEN the System SHALL update the system prompt accordingly
4. WHEN a client views the conversation preview THEN the System SHALL display example responses demonstrating the selected personality and tone
5. WHEN a client changes personality or tone THEN the System SHALL immediately update the preview examples

### Requirement 5

**User Story:** As a client, I want to specify which information my agent should collect, so that I gather relevant data from leads.

#### Acceptance Criteria

1. WHEN a client reaches Step 3 of the wizard THEN the System SHALL display standard fields (Name, Email, Phone, Country, Company) with checkboxes
2. WHEN a client selects standard fields THEN the System SHALL mark them as required or optional
3. WHEN a client adds a custom field THEN the System SHALL allow specification of field type (text, number, date, multiple choice, dropdown)
4. WHEN a client configures a custom field THEN the System SHALL allow setting label, validation rules, placeholder, and order
5. WHEN a client reorders fields THEN the System SHALL update the conversation flow to ask questions in the specified order

### Requirement 6

**User Story:** As a client, I want to connect my agent to external services (WhatsApp, Email, Database), so that it can send messages and access data.

#### Acceptance Criteria

1. WHEN a client reaches Step 4 of the wizard THEN the System SHALL display available integrations (WhatsApp, Email, Database) with status indicators
2. WHEN an integration is already configured THEN the System SHALL display "✅ Configured" and a checkbox to enable it for this agent
3. WHEN an integration is not configured THEN the System SHALL display "⚠️ Not Configured" and a "Configure Now" button
4. WHEN a client clicks "Configure Now" THEN the System SHALL open the integration configuration modal from Sprint 07A
5. WHEN a client completes integration configuration THEN the System SHALL return to the wizard and update the integration status

### Requirement 7

**User Story:** As a client, I want to test my agent in a sandbox environment, so that I can verify it works correctly before publishing.

#### Acceptance Criteria

1. WHEN a client reaches Step 5 of the wizard THEN the System SHALL display a "Test Agent" button and a chat interface
2. WHEN a client clicks "Test Agent" THEN the System SHALL create a temporary sandbox conversation
3. WHEN a client sends messages in the sandbox THEN the System SHALL respond using the configured agent behavior
4. WHEN a client completes the sandbox conversation THEN the System SHALL display collected information and lead qualification result
5. WHEN a client is satisfied with the test THEN the System SHALL enable the "Publish Agent" button

### Requirement 8

**User Story:** As a client, I want to publish my agent and receive sharing links, so that I can deploy it to my audience.

#### Acceptance Criteria

1. WHEN a client clicks "Publish Agent" THEN the System SHALL activate the agent and generate a unique slug
2. WHEN an agent is published THEN the System SHALL generate a public link (https://renum.com.br/chat/{slug})
3. WHEN an agent is published THEN the System SHALL generate HTML embed code for website integration
4. WHEN an agent is published THEN the System SHALL generate a QR code that redirects to the agent conversation
5. WHEN an agent is published THEN the System SHALL display all generated assets (link, embed code, QR code) in a success modal

### Requirement 9

**User Story:** As a client, I want to manage my created agents (view, edit, clone, pause, delete), so that I can maintain and optimize my automation.

#### Acceptance Criteria

1. WHEN a client accesses the agents dashboard THEN the System SHALL display a list of all created agents with status, metrics, and actions
2. WHEN a client clicks "Edit" on an agent THEN the System SHALL open the agent configuration page (not the wizard)
3. WHEN a client clicks "Clone" on an agent THEN the System SHALL create a duplicate with "-copy" suffix and draft status
4. WHEN a client clicks "Pause" on an active agent THEN the System SHALL change status to paused and stop accepting new conversations
5. WHEN a client clicks "Delete" on an agent THEN the System SHALL prompt for confirmation and permanently remove the agent

### Requirement 10

**User Story:** As a client, I want to save my wizard progress at any step, so that I can resume creation later without losing work.

#### Acceptance Criteria

1. WHEN a client completes any wizard step THEN the System SHALL automatically save progress to the database
2. WHEN a client closes the wizard before completion THEN the System SHALL save the agent as draft status
3. WHEN a client returns to the wizard THEN the System SHALL load the saved draft and resume from the last completed step
4. WHEN a client has multiple draft agents THEN the System SHALL display them in the agents dashboard with "Draft" status
5. WHEN a client deletes a draft agent THEN the System SHALL remove all associated wizard progress data

### Requirement 11

**User Story:** As a system administrator, I want to track agent creation metrics, so that I can understand usage patterns and optimize the wizard.

#### Acceptance Criteria

1. WHEN an agent is created THEN the System SHALL log the template used, completion time, and client type (B2B/B2C)
2. WHEN a client abandons the wizard THEN the System SHALL log the step where abandonment occurred
3. WHEN a client tests an agent in sandbox THEN the System SHALL log the number of test messages and duration
4. WHEN a client publishes an agent THEN the System SHALL log the publication timestamp and initial configuration
5. WHEN an administrator views analytics THEN the System SHALL display wizard completion rate, popular templates, and average creation time

### Requirement 12

**User Story:** As a client, I want my agent to validate collected information in real-time, so that I ensure data quality.

#### Acceptance Criteria

1. WHEN a client configures a field with validation rules THEN the System SHALL enforce those rules during conversations
2. WHEN a lead provides invalid input (e.g., malformed email) THEN the Agent SHALL reject the input and request correction
3. WHEN a lead provides valid input THEN the Agent SHALL accept the input and proceed to the next question
4. WHEN a client specifies a phone number field THEN the System SHALL validate international format (+country code)
5. WHEN a client specifies an email field THEN the System SHALL validate email format (contains @ and domain)

### Requirement 13

**User Story:** As a client, I want to preview how my agent will behave, so that I can adjust configuration before publishing.

#### Acceptance Criteria

1. WHEN a client is in Step 2 (Personality) THEN the System SHALL display 3 example conversations demonstrating the selected personality
2. WHEN a client changes personality or tone THEN the System SHALL regenerate example conversations within 2 seconds
3. WHEN a client is in Step 3 (Fields) THEN the System SHALL display the conversation flow showing question order
4. WHEN a client adds or removes fields THEN the System SHALL update the conversation flow preview immediately
5. WHEN a client is in Step 5 (Test) THEN the System SHALL allow full interactive testing with the configured agent

### Requirement 14

**User Story:** As a client, I want to receive notifications when my agent qualifies a lead, so that I can follow up promptly.

#### Acceptance Criteria

1. WHEN an agent completes a conversation and qualifies a lead THEN the System SHALL send a notification to the client
2. WHEN a client has WhatsApp integration enabled THEN the System SHALL send notification via WhatsApp
3. WHEN a client has Email integration enabled THEN the System SHALL send notification via Email
4. WHEN a client has both integrations enabled THEN the System SHALL send notifications via both channels
5. WHEN a notification is sent THEN the System SHALL include lead information, qualification score, and conversation summary

### Requirement 15

**User Story:** As a client, I want my agent to handle multiple languages, so that I can serve international audiences.

#### Acceptance Criteria

1. WHEN a client configures an agent THEN the System SHALL allow selection of primary language (Portuguese, English, Spanish)
2. WHEN a lead starts a conversation THEN the Agent SHALL detect the lead's language from the first message
3. WHEN a lead uses a different language than the agent's primary THEN the Agent SHALL attempt to respond in the lead's language
4. WHEN a lead uses an unsupported language THEN the Agent SHALL respond in the primary language and inform the lead
5. WHEN a client enables multi-language support THEN the System SHALL translate field labels and validation messages

