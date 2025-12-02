# Design Document - Sprint 02: CRUD Core

## Overview

Este sprint implementa a camada de API REST para gerenciamento de Clientes, Leads e Projetos no sistema RENUM. A arquitetura segue o padrão de três camadas: Routes (endpoints) → Services (lógica de negócio) → Supabase (persistência).

A estrutura do banco de dados já existe e é mais completa que o planejamento inicial, incluindo campos JSONB para flexibilidade e campos adicionais para rastreamento e métricas.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  - ClientsPage, LeadsPage, ProjectsPage                 │
│  - Formulários de criação/edição                        │
│  - Listagens com filtros e paginação                    │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS + JWT Bearer Token
                     │
┌────────────────────▼────────────────────────────────────┐
│                 BACKEND (FastAPI)                        │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Routes Layer (API Endpoints)                    │   │
│  │ - /api/clients (GET, POST, PUT, DELETE)         │   │
│  │ - /api/leads (GET, POST, PUT, DELETE)           │   │
│  │ - /api/projects (GET, POST, PUT, DELETE)        │   │
│  │ - Auth Middleware (valida JWT)                  │   │
│  └────────────────────┬────────────────────────────┘   │
│                       │                                  │
│  ┌────────────────────▼────────────────────────────┐   │
│  │ Services Layer (Business Logic)                 │   │
│  │ - ClientService (validações + CRUD)             │   │
│  │ - LeadService (validações + CRUD)               │   │
│  │ - ProjectService (validações + CRUD)            │   │
│  └────────────────────┬────────────────────────────┘   │
│                       │                                  │
│  ┌────────────────────▼────────────────────────────┐   │
│  │ Models Layer (Pydantic Schemas)                 │   │
│  │ - ClientCreate, ClientUpdate, ClientResponse    │   │
│  │ - LeadCreate, LeadUpdate, LeadResponse          │   │
│  │ - ProjectCreate, ProjectUpdate, ProjectResponse │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              SUPABASE (PostgreSQL)                       │
│                                                          │
│  clients                                                 │
│  - id, company_name, document, website, segment         │
│  - status, contact (JSONB), address (JSONB)             │
│  - tags, notes, last_interaction                        │
│  - created_at, updated_at                               │
│  - RLS: Admins full access                              │
│                                                          │
│  leads                                                   │
│  - id, name, phone, email, source, status               │
│  - subagent_id, score, notes                            │
│  - first_contact_at, last_interaction_at                │
│  - created_at, updated_at                               │
│  - RLS: Admins full access                              │
│                                                          │
│  projects                                                │
│  - id, name, type, description, scope                   │
│  - client_id, responsible_id, status                    │
│  - start_date, due_date, progress, budget               │
│  - created_at, updated_at                               │
│  - RLS: Admins full access                              │
└─────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Models (Pydantic Schemas)

#### Client Models
```python
# ContactInfo - Nested model para JSONB
- phone: Optional[str]
- email: Optional[str]
- whatsapp: Optional[str]
- telegram: Optional[str]

# AddressInfo - Nested model para JSONB
- street, number, complement, neighborhood
- city, state, zipcode, country

# ClientBase
- company_name: str (3-200 chars)
- document: Optional[str] (CPF/CNPJ validado)
- website: Optional[str]
- segment: str
- contact: Optional[ContactInfo]
- address: Optional[AddressInfo]
- tags: Optional[List[str]]
- notes: Optional[str]

# ClientCreate (herda ClientBase)
- status: Literal["active", "inactive", "suspended"] = "active"

# ClientUpdate
- Todos campos opcionais
- Permite atualização parcial

# ClientResponse (herda ClientBase)
- id: str
- status: str
- last_interaction: Optional[datetime]
- created_at: datetime
- updated_at: Optional[datetime]

# ClientList
- items: List[ClientResponse]
- total: int
- page: int
- limit: int
- has_next: bool
```

#### Lead Models
```python
# LeadBase
- name: str (2-200 chars)
- phone: str (validado)
- email: Optional[EmailStr]
- source: str
- notes: Optional[str]
- score: Optional[int] (0-100)

# LeadCreate (herda LeadBase)
- status: Literal["new", "contacted", "qualified", "converted", "lost"] = "new"
- subagent_id: Optional[str]

# LeadUpdate
- Todos campos opcionais

# LeadResponse (herda LeadBase)
- id: str
- status: str
- subagent_id: Optional[str]
- first_contact_at: Optional[datetime]
- last_interaction_at: Optional[datetime]
- created_at: datetime
- updated_at: Optional[datetime]

# LeadList
- items: List[LeadResponse]
- total: int
- page: int
- limit: int
- has_next: bool
```

#### Project Models
```python
# ProjectBase
- name: str (3-200 chars)
- type: str
- description: Optional[str] (max 2000)
- scope: Optional[str] (max 5000)
- start_date: Optional[date]
- due_date: Optional[date]
- budget: Optional[Decimal] (>= 0)

# ProjectCreate (herda ProjectBase)
- client_id: Optional[str]
- responsible_id: Optional[str]
- status: Literal["planning", "active", "paused", "completed", "cancelled"] = "planning"
- progress: int = 0 (0-100)

# ProjectUpdate
- Todos campos opcionais

# ProjectResponse (herda ProjectBase)
- id: str
- client_id: Optional[str]
- responsible_id: Optional[str]
- status: str
- progress: int
- created_at: datetime
- updated_at: Optional[datetime]

# ProjectList
- items: List[ProjectResponse]
- total: int
- page: int
- limit: int
- has_next: bool
```

### 2. Services (Business Logic)

#### ClientService
```python
async def get_all(page, limit, search, status) -> ClientList
    - Query Supabase com filtros
    - Aplicar paginação (offset/limit)
    - Ordenar por created_at desc
    - Retornar lista paginada

async def get_by_id(client_id) -> ClientResponse
    - Buscar por ID
    - Raise NotFoundError se não existir
    - Retornar dados completos

async def create(data: ClientCreate) -> ClientResponse
    - Validar dados (Pydantic)
    - Inserir no Supabase
    - Retornar cliente criado

async def update(client_id, data: ClientUpdate) -> ClientResponse
    - Verificar se existe
    - Validar dados
    - Atualizar apenas campos fornecidos (exclude_unset)
    - Retornar cliente atualizado

async def delete(client_id) -> bool
    - Verificar se existe
    - Deletar do Supabase
    - Retornar True
```

#### LeadService
```python
async def get_all(page, limit, search, status, source) -> LeadList
    - Query com filtros múltiplos
    - Busca em name, email, phone
    - Paginação e ordenação

async def get_by_id(lead_id) -> LeadResponse
    - Buscar por ID
    - Raise NotFoundError se não existir

async def create(data: LeadCreate) -> LeadResponse
    - Validar telefone
    - Inserir com status "new"
    - Retornar lead criado

async def update(lead_id, data: LeadUpdate) -> LeadResponse
    - Atualização parcial
    - Validar dados modificados

async def delete(lead_id) -> bool
    - Remover do banco
```

#### ProjectService
```python
async def get_all(page, limit, search, status, type, client_id) -> ProjectList
    - Filtros múltiplos
    - Busca em name, description
    - Paginação

async def get_by_id(project_id) -> ProjectResponse
    - Buscar por ID

async def create(data: ProjectCreate) -> ProjectResponse
    - Validar progresso (0-100)
    - Validar budget (>= 0)
    - Status inicial "planning"

async def update(project_id, data: ProjectUpdate) -> ProjectResponse
    - Atualização parcial

async def delete(project_id) -> bool
    - Remover do banco
```

### 3. Routes (API Endpoints)

#### Client Routes
```
GET    /api/clients              - Lista clientes (paginado)
GET    /api/clients/{id}         - Busca cliente por ID
POST   /api/clients              - Cria novo cliente
PUT    /api/clients/{id}         - Atualiza cliente
DELETE /api/clients/{id}         - Deleta cliente

Query params (GET /api/clients):
- page: int (default 1, min 1)
- limit: int (default 10, min 1, max 100)
- search: str (busca em company_name)
- status: str (active, inactive, suspended)
```

#### Lead Routes
```
GET    /api/leads                - Lista leads (paginado)
GET    /api/leads/{id}           - Busca lead por ID
POST   /api/leads                - Cria novo lead
PUT    /api/leads/{id}           - Atualiza lead
DELETE /api/leads/{id}           - Deleta lead

Query params (GET /api/leads):
- page: int
- limit: int
- search: str (busca em name, email, phone)
- status: str (new, contacted, qualified, converted, lost)
- source: str
```

#### Project Routes
```
GET    /api/projects             - Lista projetos (paginado)
GET    /api/projects/{id}        - Busca projeto por ID
POST   /api/projects             - Cria novo projeto
PUT    /api/projects/{id}        - Atualiza projeto
DELETE /api/projects/{id}        - Deleta projeto

Query params (GET /api/projects):
- page: int
- limit: int
- search: str (busca em name, description)
- status: str (planning, active, paused, completed, cancelled)
- type: str
- client_id: str
```

## Data Models

### Database Schema (Existing)

```sql
-- clients
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL,
    document TEXT,
    website TEXT,
    segment TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    contact JSONB,
    address JSONB,
    last_interaction TIMESTAMPTZ,
    tags TEXT[],
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- leads
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    source TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    subagent_id UUID,
    first_contact_at TIMESTAMPTZ,
    last_interaction_at TIMESTAMPTZ,
    notes TEXT,
    score INTEGER CHECK (score >= 0 AND score <= 100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    client_id UUID,
    status TEXT NOT NULL DEFAULT 'planning',
    type TEXT NOT NULL,
    start_date DATE,
    due_date DATE,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    responsible_id UUID,
    budget NUMERIC(15,2),
    description TEXT,
    scope TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Criação de cliente retorna dados completos
*Para qualquer* ClientCreate válido, criar um cliente deve retornar ClientResponse com id gerado, timestamps preenchidos e status "active"
**Validates: Requirements 1.1**

### Property 2: Listagem paginada respeita limites
*Para qualquer* requisição de listagem com limit=N, o sistema deve retornar no máximo N items
**Validates: Requirements 5.2, 5.3**

### Property 3: Busca por ID inexistente retorna 404
*Para qualquer* ID que não existe no banco, buscar por ID deve retornar NotFoundError (404)
**Validates: Requirements 7.2**

### Property 4: Atualização parcial preserva campos não fornecidos
*Para qualquer* cliente existente, atualizar apenas um campo deve preservar todos os outros campos inalterados
**Validates: Requirements 1.4**

### Property 5: Validação de telefone rejeita formatos inválidos
*Para qualquer* string que não seja telefone válido (10-11 dígitos), a validação deve retornar False
**Validates: Requirements 2.6, 4.1**

### Property 6: Validação de documento rejeita CPF/CNPJ inválidos
*Para qualquer* string que não tenha 11 ou 14 dígitos, a validação de documento deve retornar False
**Validates: Requirements 1.8, 4.2, 4.3**

### Property 7: Paginação calcula has_next corretamente
*Para qualquer* listagem, has_next deve ser True se total > (page * limit), False caso contrário
**Validates: Requirements 5.1**

### Property 8: Filtro por status retorna apenas registros com aquele status
*Para qualquer* status fornecido, todos os items retornados devem ter exatamente aquele status
**Validates: Requirements 1.2, 2.2, 3.2**

### Property 9: Score de lead deve estar entre 0 e 100
*Para qualquer* lead com score, o valor deve ser >= 0 e <= 100
**Validates: Requirements 2.8**

### Property 10: Progresso de projeto deve estar entre 0 e 100
*Para qualquer* projeto, o progresso deve ser >= 0 e <= 100
**Validates: Requirements 3.6**

### Property 11: Orçamento de projeto deve ser positivo
*Para qualquer* projeto com budget, o valor deve ser >= 0
**Validates: Requirements 3.7**

### Property 12: Busca case-insensitive funciona
*Para qualquer* termo de busca, deve encontrar registros independente de maiúsculas/minúsculas
**Validates: Requirements 5.4**

## Error Handling

### Exception Classes
```python
class NotFoundError(Exception)
    - Raised quando recurso não é encontrado
    - HTTP 404

class ValidationError(Exception)
    - Raised quando validação Pydantic falha
    - HTTP 400

class AuthenticationError(Exception)
    - Raised quando token é inválido
    - HTTP 401

class AuthorizationError(Exception)
    - Raised quando usuário não tem permissão
    - HTTP 403
```

### Error Response Format
```json
{
    "detail": "Error message",
    "timestamp": "2025-11-25T10:30:00Z",
    "path": "/api/clients/123",
    "request_id": "uuid"
}
```

## Testing Strategy

### Unit Tests
- Testar validators isoladamente (validate_phone, validate_document, etc)
- Testar Pydantic models com dados válidos e inválidos
- Testar lógica de paginação (cálculo de offset, has_next)
- Testar formatação de dados (format_phone, format_cpf, format_cnpj)

### Integration Tests
- Testar endpoints completos (create → read → update → delete)
- Testar filtros e paginação com dados reais
- Testar autenticação (com e sem token)
- Testar RLS (admin vê tudo)

### Property-Based Tests
Framework: **Hypothesis** (Python)

Configuração: Mínimo 100 iterações por teste

**Test 1: Property 1 - Criação retorna dados completos**
```python
@given(client_data=st.builds(ClientCreate))
def test_create_client_returns_complete_data(client_data):
    result = await client_service.create(client_data)
    assert result.id is not None
    assert result.created_at is not None
    assert result.status == "active"
```
**Feature: sprint-02-crud-core, Property 1: Criação de cliente retorna dados completos**

**Test 2: Property 2 - Listagem respeita limites**
```python
@given(limit=st.integers(min_value=1, max_value=100))
def test_list_respects_limit(limit):
    result = await client_service.get_all(page=1, limit=limit)
    assert len(result.items) <= limit
```
**Feature: sprint-02-crud-core, Property 2: Listagem paginada respeita limites**

**Test 3: Property 5 - Validação de telefone**
```python
@given(phone=st.text())
def test_phone_validation(phone):
    is_valid = validate_phone(phone)
    if is_valid:
        clean = re.sub(r'\D', '', phone)
        assert len(clean) in [10, 11, 13]
```
**Feature: sprint-02-crud-core, Property 5: Validação de telefone rejeita formatos inválidos**

**Test 4: Property 7 - has_next correto**
```python
@given(total=st.integers(min_value=0, max_value=1000),
       page=st.integers(min_value=1, max_value=10),
       limit=st.integers(min_value=1, max_value=100))
def test_has_next_calculation(total, page, limit):
    has_next = total > (page * limit)
    # Verificar que cálculo está correto
```
**Feature: sprint-02-crud-core, Property 7: Paginação calcula has_next corretamente**

**Test 5: Property 9 - Score válido**
```python
@given(score=st.integers())
def test_lead_score_validation(score):
    if 0 <= score <= 100:
        # Deve aceitar
        lead = LeadCreate(name="Test", phone="11999999999", source="test", score=score)
        assert lead.score == score
    else:
        # Deve rejeitar
        with pytest.raises(ValidationError):
            LeadCreate(name="Test", phone="11999999999", source="test", score=score)
```
**Feature: sprint-02-crud-core, Property 9: Score de lead deve estar entre 0 e 100**

## Security Considerations

- Todos endpoints protegidos por JWT (middleware)
- RLS habilitado em todas as tabelas
- Service key usado apenas no backend (nunca expor)
- Validação de entrada em todas as operações
- Logs de todas as operações (audit trail)

## Performance Considerations

- Índices em colunas de busca frequente
- Paginação obrigatória (máximo 100 items)
- Query otimizada com select específico
- JSONB para dados flexíveis sem joins
- Ordenação por created_at (índice existente)

## Deployment Notes

- Verificar que tabelas existem antes de deploy
- Verificar que RLS está habilitado
- Verificar que políticas estão criadas
- Testar endpoints com Swagger antes de integrar frontend
- Monitorar logs para erros de validação
