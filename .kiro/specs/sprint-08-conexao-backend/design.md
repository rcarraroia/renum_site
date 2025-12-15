# SPRINT 08 - CONEXÃO BACKEND - DESIGN

## Overview

Este sprint implementa a camada de integração entre frontend React e backend FastAPI, substituindo dados mock por comunicação real com o Supabase. A arquitetura segue o padrão Service Layer no frontend, com tratamento robusto de erros, estados de loading e sincronização de dados.

## Architecture

### Fluxo Geral de Comunicação

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/TypeScript)               │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Pages      │─────▶│   Services   │─────▶│  Hooks   │  │
│  │ (UI Layer)   │◀─────│ (API Layer)  │◀─────│ (State)  │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                      │                    │        │
└─────────┼──────────────────────┼────────────────────┼────────┘
          │                      │                    │
          │ HTTP/REST            │ WebSocket          │
          ▼                      ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Routes     │─────▶│   Services   │─────▶│  Models  │  │
│  │ (Endpoints)  │◀─────│  (Business)  │◀─────│ (Pydantic)│ │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│         │                      │                    │        │
└─────────┼──────────────────────┼────────────────────┼────────┘
          │                      │                    │
          │ SQL Queries          │ RLS Policies       │
          ▼                      ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE (PostgreSQL)                     │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ projects │  │  leads   │  │ clients  │  │messages  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐                                │
│  │interviews│  │ reports  │                                │
│  └──────────┘  └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Frontend Service Layer

Cada funcionalidade terá um service dedicado seguindo este padrão:

**Estrutura de Service:**
```
src/services/
├── api/
│   ├── client.ts          # Axios instance configurado
│   ├── projectService.ts  # CRUD de projetos
│   ├── leadService.ts     # CRUD de leads + conversão
│   ├── clientService.ts   # CRUD de clientes
│   ├── conversationService.ts  # Mensagens + histórico
│   ├── interviewService.ts     # Entrevistas + resultados
│   └── reportService.ts        # Analytics + exportação
├── websocket/
│   ├── websocketClient.ts      # Cliente WebSocket
│   └── useWebSocket.ts         # Hook React para WS
└── types/
    ├── project.types.ts
    ├── lead.types.ts
    ├── client.types.ts
    ├── conversation.types.ts
    ├── interview.types.ts
    └── report.types.ts
```

**Responsabilidades do Service Layer:**
- Fazer requisições HTTP ao backend
- Transformar dados entre formato API e formato UI
- Tratar erros de rede e API
- Gerenciar tokens de autenticação
- Implementar retry logic quando apropriado
- Cachear dados quando necessário

### Backend API Layer

Cada funcionalidade terá endpoints RESTful seguindo este padrão:

**Estrutura de Routes:**
```
src/api/routes/
├── projects.py      # CRUD de projetos
├── leads.py         # CRUD de leads + conversão
├── clients.py       # CRUD de clientes
├── conversations.py # WebSocket + mensagens
├── interviews.py    # Entrevistas + Discovery Agent
└── reports.py       # Analytics + exportação
```

**Estrutura de Services:**
```
src/services/
├── project_service.py
├── lead_service.py
├── client_service.py
├── conversation_service.py
├── interview_service.py
└── report_service.py
```

**Estrutura de Models:**
```
src/models/
├── project.py
├── lead.py
├── client.py
├── conversation.py
├── interview.py
└── report.py
```

## Data Models

### 1. PROJETOS

**Backend Model (Pydantic):**
```
ProjectBase:
  - name: str
  - description: str | None
  - type: ProjectType (enum)
  - status: ProjectStatus (enum)
  - config: dict[str, Any]

ProjectCreate(ProjectBase):
  - client_id: UUID

ProjectUpdate(ProjectBase):
  - (todos campos opcionais)

ProjectResponse(ProjectBase):
  - id: UUID
  - client_id: UUID
  - created_at: datetime
  - updated_at: datetime
```

**Frontend Type (TypeScript):**
```
interface Project {
  id: string
  clientId: string
  name: string
  description?: string
  type: ProjectType
  status: ProjectStatus
  config: Record<string, any>
  createdAt: string
  updatedAt: string
}

type ProjectType = 'survey' | 'campaign' | 'support'
type ProjectStatus = 'draft' | 'active' | 'paused' | 'completed'
```

**Endpoints:**
- GET /api/projects - Lista projetos (com paginação e filtros)
- POST /api/projects - Cria projeto
- GET /api/projects/{id} - Busca projeto específico
- PUT /api/projects/{id} - Atualiza projeto
- DELETE /api/projects/{id} - Deleta projeto

### 2. LEADS

**Backend Model (Pydantic):**
```
LeadBase:
  - phone: str
  - name: str
  - email: str | None
  - metadata: dict[str, Any]
  - status: LeadStatus (enum)
  - stage: LeadStage (enum)

LeadCreate(LeadBase):
  - client_id: UUID

LeadUpdate(LeadBase):
  - (todos campos opcionais)

LeadResponse(LeadBase):
  - id: UUID
  - client_id: UUID
  - created_at: datetime
  - updated_at: datetime

LeadConvertRequest:
  - company_name: str
  - cnpj: str
  - plan: ClientPlan (enum)
```

**Frontend Type (TypeScript):**
```
interface Lead {
  id: string
  clientId: string
  phone: string
  name: string
  email?: string
  metadata: Record<string, any>
  status: LeadStatus
  stage: LeadStage
  createdAt: string
  updatedAt: string
}

type LeadStatus = 'active' | 'inactive' | 'blocked'
type LeadStage = 'new' | 'contacted' | 'qualified' | 'proposal' | 'negotiation' | 'won' | 'lost'
```

**Endpoints:**
- GET /api/leads - Lista leads (com paginação e filtros)
- POST /api/leads - Cria lead
- GET /api/leads/{id} - Busca lead específico
- PUT /api/leads/{id} - Atualiza lead
- DELETE /api/leads/{id} - Deleta lead
- POST /api/leads/{id}/convert - Converte lead em cliente

### 3. CLIENTES

**Backend Model (Pydantic):**
```
ClientBase:
  - company_name: str
  - cnpj: str
  - plan: ClientPlan (enum)
  - status: ClientStatus (enum)

ClientCreate(ClientBase):
  - profile_id: UUID

ClientUpdate(ClientBase):
  - (todos campos opcionais)

ClientResponse(ClientBase):
  - id: UUID
  - profile_id: UUID
  - created_at: datetime
  - updated_at: datetime
```

**Frontend Type (TypeScript):**
```
interface Client {
  id: string
  profileId: string
  companyName: string
  cnpj: string
  plan: ClientPlan
  status: ClientStatus
  createdAt: string
  updatedAt: string
}

type ClientPlan = 'basic' | 'pro' | 'enterprise'
type ClientStatus = 'active' | 'inactive' | 'suspended'
```

**Endpoints:**
- GET /api/clients - Lista clientes (com paginação e filtros)
- POST /api/clients - Cria cliente
- GET /api/clients/{id} - Busca cliente específico
- PUT /api/clients/{id} - Atualiza cliente
- DELETE /api/clients/{id} - Deleta cliente

### 4. CONVERSAS

**Backend Model (Pydantic):**
```
ConversationBase:
  - lead_id: UUID
  - client_id: UUID
  - status: ConversationStatus (enum)

ConversationResponse(ConversationBase):
  - id: UUID
  - last_message_at: datetime | None
  - created_at: datetime
  - updated_at: datetime

MessageBase:
  - conversation_id: UUID
  - role: MessageRole (enum)
  - content: str
  - channel: MessageChannel (enum)
  - metadata: dict[str, Any]

MessageResponse(MessageBase):
  - id: UUID
  - timestamp: datetime
  - created_at: datetime

WebSocketMessage:
  - type: str (message, typing, presence)
  - data: dict[str, Any]
```

**Frontend Type (TypeScript):**
```
interface Conversation {
  id: string
  leadId: string
  clientId: string
  status: ConversationStatus
  lastMessageAt?: string
  createdAt: string
  updatedAt: string
}

interface Message {
  id: string
  conversationId: string
  role: MessageRole
  content: string
  channel: MessageChannel
  metadata: Record<string, any>
  timestamp: string
  createdAt: string
}

type ConversationStatus = 'open' | 'closed'
type MessageRole = 'user' | 'assistant' | 'system'
type MessageChannel = 'whatsapp' | 'sms' | 'email' | 'web'

interface WebSocketMessage {
  type: 'message' | 'typing' | 'presence'
  data: any
}
```

**Endpoints:**
- GET /api/conversations - Lista conversas
- POST /api/conversations - Cria conversa
- GET /api/conversations/{id} - Busca conversa específica
- GET /api/conversations/{id}/messages - Lista mensagens da conversa
- POST /api/conversations/{id}/messages - Envia mensagem
- WS /ws/conversations/{id} - WebSocket para tempo real

### 5. ENTREVISTAS

**Backend Model (Pydantic):**
```
InterviewBase:
  - lead_id: UUID
  - project_id: UUID
  - status: InterviewStatus (enum)
  - metadata: dict[str, Any]

InterviewResponse(InterviewBase):
  - id: UUID
  - started_at: datetime | None
  - completed_at: datetime | None
  - created_at: datetime
  - updated_at: datetime

InterviewDetailResponse(InterviewResponse):
  - messages: list[InterviewMessage]
  - lead: LeadResponse
  - project: ProjectResponse

InterviewResultsResponse:
  - interview: InterviewResponse
  - analysis: dict[str, Any]  # Gerado pelo Discovery Agent
  - summary: str
  - insights: list[str]
```

**Frontend Type (TypeScript):**
```
interface Interview {
  id: string
  leadId: string
  projectId: string
  status: InterviewStatus
  metadata: Record<string, any>
  startedAt?: string
  completedAt?: string
  createdAt: string
  updatedAt: string
}

interface InterviewDetail extends Interview {
  messages: InterviewMessage[]
  lead: Lead
  project: Project
}

interface InterviewResults {
  interview: Interview
  analysis: Record<string, any>
  summary: string
  insights: string[]
}

type InterviewStatus = 'pending' | 'in_progress' | 'completed' | 'cancelled'
```

**Endpoints:**
- GET /api/interviews - Lista entrevistas
- GET /api/interviews/{id} - Busca detalhes da entrevista
- GET /api/interviews/{id}/results - Busca resultados + análise AI

### 6. RELATÓRIOS

**Backend Model (Pydantic):**
```
ReportOverviewResponse:
  - total_leads: int
  - total_clients: int
  - total_conversations: int
  - total_interviews: int
  - active_projects: int
  - conversion_rate: float

AgentPerformanceResponse:
  - agent_id: str
  - agent_name: str
  - total_conversations: int
  - avg_response_time: float
  - satisfaction_score: float

ConversionFunnelResponse:
  - stage: str
  - count: int
  - conversion_rate: float

ReportFilters:
  - start_date: date | None
  - end_date: date | None
  - client_id: UUID | None
  - project_id: UUID | None
  - agent_type: str | None
```

**Frontend Type (TypeScript):**
```
interface ReportOverview {
  totalLeads: number
  totalClients: number
  totalConversations: number
  totalInterviews: number
  activeProjects: number
  conversionRate: number
}

interface AgentPerformance {
  agentId: string
  agentName: string
  totalConversations: number
  avgResponseTime: number
  satisfactionScore: number
}

interface ConversionFunnel {
  stage: string
  count: number
  conversionRate: number
}

interface ReportFilters {
  startDate?: string
  endDate?: string
  clientId?: string
  projectId?: string
  agentType?: string
}
```

**Endpoints:**
- GET /api/reports/overview - Métricas gerais
- GET /api/reports/agents - Performance de agentes
- GET /api/reports/conversions - Funil de conversão
- GET /api/reports/export - Exportar dados (CSV/Excel)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: CRUD Consistency

*For any* entity (project, lead, client), when a CREATE operation succeeds, a subsequent READ operation should return the created entity with all fields matching the input data.

**Validates: Requirements 1.1, 2.1, 3.1**

### Property 2: Update Idempotence

*For any* entity, when an UPDATE operation is performed twice with the same data, the second operation should succeed and the entity state should remain unchanged from the first update.

**Validates: Requirements 1.3, 2.3, 3.3**

### Property 3: Delete Cascade Safety

*For any* entity deletion, when a DELETE operation succeeds, subsequent READ operations should return 404 Not Found, and related entities should handle the deletion gracefully without breaking referential integrity.

**Validates: Requirements 1.4, 2.4, 3.4**

### Property 4: Lead Conversion Atomicity

*For any* lead conversion, when a lead is converted to a client, either both the client creation and lead status update succeed, or both fail, ensuring no partial state.

**Validates: Requirements 2.5**

### Property 5: WebSocket Message Delivery

*For any* message sent via WebSocket, when the connection is active, the message should be delivered to all connected participants and persisted in the database within 1 second.

**Validates: Requirements 4.2, 4.3**

### Property 6: WebSocket Reconnection

*For any* WebSocket disconnection, when the connection is lost, the client should attempt automatic reconnection with exponential backoff, and upon reconnection, should sync any missed messages.

**Validates: Requirements 4.6**

### Property 7: Historical Data Integrity

*For any* conversation, when messages are loaded from history, they should appear in chronological order and match exactly what was sent, with no duplicates or missing messages.

**Validates: Requirements 4.1**

### Property 8: Interview Data Completeness

*For any* interview detail view, when loaded, it should include all associated messages, lead information, and project information without requiring additional requests.

**Validates: Requirements 5.2**

### Property 9: Analytics Calculation Accuracy

*For any* report metric, when calculated by the backend, it should match the result of manually counting the same data in the database, ensuring no discrepancies.

**Validates: Requirements 6.1, 6.3, 6.4**

### Property 10: Filter Application Consistency

*For any* report filter applied, when the same filter is applied multiple times, it should return identical results, demonstrating deterministic behavior.

**Validates: Requirements 6.2**

### Property 11: Error Message Clarity

*For any* API error response, when an operation fails, the error message should clearly indicate the cause and be actionable by the user.

**Validates: Requirements 7.2, 7.3, 7.4, 7.5**

### Property 12: Loading State Visibility

*For any* asynchronous operation, when initiated, a loading indicator should be displayed immediately and remain visible until the operation completes or fails.

**Validates: Requirements 7.1**

### Property 13: State Synchronization After Mutation

*For any* data mutation (create, update, delete), when the operation succeeds, the local state should be updated to reflect the change without requiring a full page reload.

**Validates: Requirements 8.3, 8.4**

### Property 14: Optimistic Update Rollback

*For any* optimistic update, when the backend operation fails, the local state should be rolled back to its previous value and an error should be displayed.

**Validates: Requirements 8.1**

### Property 15: Export Data Completeness

*For any* data export operation, when filters are applied, the exported file should contain exactly the same data visible in the UI with those filters, with no missing or extra records.

**Validates: Requirements 6.5**

## Error Handling

### Frontend Error Handling Strategy

**Network Errors:**
- Display user-friendly message: "Erro de conexão. Verifique sua internet."
- Implement retry button
- Log technical details to console

**Authentication Errors (401):**
- Clear local auth tokens
- Redirect to login page
- Display message: "Sessão expirada. Faça login novamente."

**Authorization Errors (403):**
- Display message: "Você não tem permissão para esta ação."
- Log attempt for security audit

**Validation Errors (400):**
- Parse error response from backend
- Display field-specific error messages
- Highlight invalid fields in form

**Server Errors (500):**
- Display generic message: "Erro no servidor. Tente novamente em alguns instantes."
- Log full error details to console
- Optionally send error report to monitoring service

**WebSocket Errors:**
- Detect disconnection
- Show connection status indicator
- Attempt automatic reconnection with exponential backoff
- Queue messages during disconnection
- Resend queued messages upon reconnection

### Backend Error Handling Strategy

**Validation Errors:**
- Return 400 with detailed field errors
- Use Pydantic validation messages

**Not Found Errors:**
- Return 404 with clear message
- Include resource type and ID in message

**Database Errors:**
- Catch and log full exception
- Return 500 with generic message to client
- Never expose database details to client

**RLS Policy Violations:**
- Return 403 with message about permissions
- Log security event

**WebSocket Errors:**
- Send error message through WebSocket
- Close connection if unrecoverable
- Log error details server-side

## Testing Strategy

### Unit Testing

**Frontend:**
- Test each service function independently
- Mock axios responses
- Test error handling paths
- Test data transformation logic
- Test WebSocket hook behavior

**Backend:**
- Test each service function independently
- Mock Supabase client
- Test validation logic
- Test error handling
- Test RLS policy application

### Integration Testing

**API Integration:**
- Test full request/response cycle
- Test authentication flow
- Test CRUD operations end-to-end
- Test WebSocket connection and messaging
- Test error scenarios

**Database Integration:**
- Test data persistence
- Test RLS policies
- Test cascade deletes
- Test transaction rollbacks

### Property-Based Testing

**Framework:** Hypothesis (Python) for backend, fast-check (TypeScript) for frontend

**Test Configuration:**
- Minimum 100 iterations per property
- Generate random valid inputs
- Test edge cases (empty strings, max lengths, special characters)
- Test boundary conditions

**Property Test Tagging:**
Each property-based test must include a comment with this format:
```
# Feature: sprint-08-conexao-backend, Property X: [property description]
```

### Manual Testing Checklist

**For each functionality:**
- Create operation works and persists
- Read operation loads correct data
- Update operation modifies data correctly
- Delete operation removes data
- Error states display correctly
- Loading states display correctly
- WebSocket connects and sends messages (for conversations)
- Filters work correctly (for reports)
- Export generates correct file (for reports)

## Performance Considerations

**Frontend:**
- Implement pagination for large lists (20 items per page)
- Debounce search inputs (300ms)
- Cache API responses when appropriate
- Use React.memo for expensive components
- Lazy load routes and components

**Backend:**
- Add database indexes on frequently queried columns
- Implement query result caching with Redis
- Use connection pooling for database
- Limit query results with pagination
- Optimize N+1 queries with joins

**WebSocket:**
- Implement heartbeat to detect dead connections
- Limit message size to prevent abuse
- Rate limit messages per user
- Use message compression for large payloads

## Security Considerations

**Authentication:**
- Include JWT token in all API requests
- Refresh token before expiration
- Clear tokens on logout
- Validate token on backend for every request

**Authorization:**
- Apply RLS policies on all database queries
- Verify user permissions before operations
- Never trust client-side validation alone

**Data Validation:**
- Validate all inputs on backend
- Sanitize user inputs to prevent injection
- Use Pydantic models for type safety
- Validate file uploads (type, size)

**WebSocket Security:**
- Authenticate WebSocket connections with JWT
- Validate message format and content
- Rate limit messages per connection
- Close connections on suspicious activity
