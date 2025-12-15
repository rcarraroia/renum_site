# Design Document - Sprint 06

## Overview

O **Wizard de Criação de Agentes** é uma interface guiada que permite clientes B2B e B2C criarem agentes de IA especializados em 5 etapas sequenciais. O sistema utiliza templates pré-configurados, permite customização completa, oferece sandbox para testes e gera assets de publicação (link público, embed code, QR code).

**Principais Funcionalidades:**
- Wizard de 5 etapas com validação progressiva
- 5 templates pré-configurados (Customer Service, Sales, Support, Recruitment, Custom)
- Sistema de campos customizados com validação
- Integração com serviços externos (WhatsApp, Email, Database)
- Sandbox para teste antes da publicação
- Geração automática de link público, embed code e QR code
- Dashboard de gestão de agentes criados

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + TypeScript)               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              AgentWizard (Main Component)                   │ │
│  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │ │
│  │  │  Step 1  │  Step 2  │  Step 3  │  Step 4  │  Step 5  │  │ │
│  │  │ Objetivo │Personali │  Campos  │Integraçõe│  Teste   │  │ │
│  │  │          │   dade   │          │    s     │Publicação│  │ │
│  │  └──────────┴──────────┴──────────┴──────────┴──────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              AgentsDashboard (Management)                   │ │
│  │  - List agents (with filters)                              │ │
│  │  - View metrics (conversations, leads, conversion rate)    │ │
│  │  - Actions (Edit, Clone, Pause, Delete)                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              SandboxChat (Testing)                          │ │
│  │  - Interactive chat interface                              │ │
│  │  - Real-time agent responses                               │ │
│  │  - Display collected information                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP + JWT
                              │
┌─────────────────────────────▼─────────────────────────────────────┐
│                      BACKEND (FastAPI + Python)                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Wizard API Endpoints                       │ │
│  │  POST   /api/agents/wizard/start                             │ │
│  │  PUT    /api/agents/wizard/{wizard_id}/step/{step_number}    │ │
│  │  GET    /api/agents/wizard/{wizard_id}                       │ │
│  │  POST   /api/agents/wizard/{wizard_id}/test                  │ │
│  │  POST   /api/agents/wizard/{wizard_id}/publish               │ │
│  │  DELETE /api/agents/wizard/{wizard_id}                       │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Templates Service                          │ │
│  │  - Load predefined templates (in-memory)                     │ │
│  │  - Generate system prompts based on template + customization │ │
│  │  - Validate template compatibility                           │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Sandbox Service                            │ │
│  │  - Create temporary conversation                             │ │
│  │  - Process messages with configured agent                    │ │
│  │  - Collect and validate information                          │ │
│  │  - Clean up after test completion                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Publication Service                        │ │
│  │  - Generate unique slug                                      │ │
│  │  - Create public URL                                         │ │
│  │  - Generate embed code (HTML/JS)                             │ │
│  │  - Generate QR code (PNG)                                    │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────▼─────────────────────────────────────┐
│                      SUPABASE (PostgreSQL)                         │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  sub_agents (MODIFIED)                                        │ │
│  │  + client_id (UUID, FK → clients) [NEW]                      │ │
│  │  + template_type (enum) [NEW]                                │ │
│  │  + status (enum: draft, active, paused, inactive) [NEW]      │ │
│  │  + config (JSONB) - stores custom fields, personality, etc   │ │
│  │  + slug, public_url, access_count, is_public                 │ │
│  │  + knowledge_base (JSONB)                                    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  integrations (FROM SPRINT 07A)                               │ │
│  │  - id, client_id, type, name, status, config                 │ │
│  │  - Used in Step 4 to check available integrations            │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  conversations (EXISTING)                                     │ │
│  │  - Used for sandbox testing (with is_test flag)              │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Frontend Components

#### 1. AgentWizard (Main Container)
```typescript
interface WizardFormData {
  // Step 1: Objetivo
  template_type: 'customer_service' | 'sales' | 'support' | 'recruitment' | 'custom';
  name: string;
  description: string;
  niche: 'mmn' | 'clinicas' | 'vereadores' | 'ecommerce' | 'generico';
  
  // Step 2: Personalidade
  personality: 'professional' | 'friendly' | 'technical' | 'casual';
  tone_formal: number; // 0-100 slider
  tone_direct: number; // 0-100 slider
  
  // Step 3: Campos
  standard_fields: {
    name: { enabled: boolean; required: boolean };
    email: { enabled: boolean; required: boolean };
    phone: { enabled: boolean; required: boolean };
    country: { enabled: boolean; required: boolean };
    company: { enabled: boolean; required: boolean };
  };
  custom_fields: CustomField[];
  
  // Step 4: Integrações
  integrations: {
    whatsapp: boolean;
    email: boolean;
    database: boolean;
  };
  
  // Step 5: Teste (runtime only, not saved)
  sandbox_conversation_id?: string;
}

interface CustomField {
  id: string;
  label: string;
  type: 'text' | 'textarea' | 'number' | 'date' | 'time' | 'radio' | 'checkbox' | 'dropdown';
  required: boolean;
  validation?: {
    format?: 'email' | 'phone' | 'url';
    min?: number;
    max?: number;
    pattern?: string;
  };
  placeholder?: string;
  options?: string[]; // For radio, checkbox, dropdown
  order: number;
}
```

#### 2. Step Components

**Step1Objective.tsx**
- Template selection (5 cards with icons and descriptions)
- Agent name input (with real-time slug generation)
- Description textarea
- Niche dropdown

**Step2Personality.tsx**
- Personality selector (4 options with visual cards)
- Tone sliders (formal vs informal, direct vs descriptive)
- Conversation preview (3 example exchanges)
- Real-time preview updates

**Step3Fields.tsx**
- Standard fields checklist (with required toggle)
- Custom fields builder:
  - Add field button
  - Field configuration form (type, label, validation, order)
  - Drag-and-drop reordering
- Conversation flow preview

**Step4Integrations.tsx**
- Integration cards (WhatsApp, Email, Database)
- Status indicators (✅ Configured / ⚠️ Not Configured)
- Enable checkboxes (only for configured integrations)
- "Configure Now" buttons (opens Sprint 07A modals)

**Step5TestPublish.tsx**
- Sandbox chat interface
- "Start Test" button
- Message input and display
- Collected information summary
- "Publish Agent" button (enabled after successful test)
- Publication success modal (with link, embed code, QR code)

#### 3. AgentsDashboard
```typescript
interface AgentListItem {
  id: string;
  name: string;
  template_type: string;
  status: 'draft' | 'active' | 'paused' | 'inactive';
  created_at: string;
  metrics: {
    conversations_total: number;
    conversations_today: number;
    leads_qualified: number;
    conversion_rate: number;
  };
}
```

### Backend Services

#### 1. WizardService
```python
class WizardService:
    """Manages wizard sessions and progress"""
    
    def start_wizard(self, client_id: UUID) -> WizardSession:
        """Create new wizard session"""
        
    def save_step(
        self, 
        wizard_id: UUID, 
        step_number: int, 
        data: dict
    ) -> WizardSession:
        """Save progress for a specific step"""
        
    def get_wizard(self, wizard_id: UUID) -> WizardSession:
        """Retrieve wizard session"""
        
    def delete_wizard(self, wizard_id: UUID) -> bool:
        """Delete wizard session (abandon)"""
```

#### 2. TemplateService
```python
class TemplateService:
    """Manages agent templates"""
    
    TEMPLATES = {
        'customer_service': {
            'name': 'Customer Service',
            'description': 'Friendly agent for customer support',
            'personality': 'friendly',
            'tone_formal': 60,
            'tone_direct': 50,
            'system_prompt_base': '...',
            'default_fields': ['name', 'email', 'phone', 'issue'],
        },
        'sales': {
            'name': 'Sales',
            'description': 'Persuasive agent for lead qualification',
            'personality': 'professional',
            'tone_formal': 70,
            'tone_direct': 80,
            'system_prompt_base': '...',
            'default_fields': ['name', 'phone', 'interest', 'budget'],
        },
        # ... other templates
    }
    
    def get_template(self, template_type: str) -> dict:
        """Get template configuration"""
        
    def generate_system_prompt(
        self, 
        template_type: str,
        personality: str,
        tone_formal: int,
        tone_direct: int,
        custom_instructions: str = None
    ) -> str:
        """Generate system prompt based on template and customization"""
```

#### 3. SandboxService
```python
class SandboxService:
    """Manages sandbox testing"""
    
    def create_sandbox(
        self, 
        agent_config: dict
    ) -> SandboxSession:
        """Create temporary sandbox conversation"""
        
    async def process_message(
        self, 
        sandbox_id: UUID, 
        message: str
    ) -> dict:
        """Process message in sandbox"""
        
    def get_sandbox_history(
        self, 
        sandbox_id: UUID
    ) -> list[dict]:
        """Get conversation history"""
        
    def get_collected_data(
        self, 
        sandbox_id: UUID
    ) -> dict:
        """Get information collected during sandbox"""
        
    def cleanup_sandbox(
        self, 
        sandbox_id: UUID
    ) -> bool:
        """Delete sandbox data"""
```

#### 4. PublicationService
```python
class PublicationService:
    """Manages agent publication"""
    
    def generate_slug(self, name: str, client_id: UUID) -> str:
        """Generate unique URL-friendly slug"""
        
    def generate_public_url(self, slug: str) -> str:
        """Generate public URL"""
        
    def generate_embed_code(
        self, 
        agent_id: UUID, 
        slug: str
    ) -> str:
        """Generate HTML embed code"""
        
    def generate_qr_code(self, public_url: str) -> bytes:
        """Generate QR code PNG"""
        
    def publish_agent(
        self, 
        wizard_id: UUID
    ) -> PublicationResult:
        """Publish agent and generate all assets"""
```

## Data Models

### Database Schema Changes

#### Modified: sub_agents table
```sql
ALTER TABLE sub_agents
ADD COLUMN client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
ADD COLUMN template_type VARCHAR(50) CHECK (template_type IN (
    'customer_service', 
    'sales', 
    'support', 
    'recruitment', 
    'custom'
)),
ADD COLUMN status VARCHAR(20) DEFAULT 'draft' CHECK (status IN (
    'draft', 
    'active', 
    'paused', 
    'inactive'
));

-- Index for performance
CREATE INDEX idx_sub_agents_client_id ON sub_agents(client_id);
CREATE INDEX idx_sub_agents_status ON sub_agents(status);
CREATE INDEX idx_sub_agents_template_type ON sub_agents(template_type);

-- Update RLS policies
CREATE POLICY "Clients can view own agents"
    ON sub_agents
    FOR SELECT
    TO authenticated
    USING (client_id IN (
        SELECT id FROM clients WHERE profile_id = auth.uid()
    ));

CREATE POLICY "Clients can create own agents"
    ON sub_agents
    FOR INSERT
    TO authenticated
    WITH CHECK (client_id IN (
        SELECT id FROM clients WHERE profile_id = auth.uid()
    ));

CREATE POLICY "Clients can update own agents"
    ON sub_agents
    FOR UPDATE
    TO authenticated
    USING (client_id IN (
        SELECT id FROM clients WHERE profile_id = auth.uid()
    ));

CREATE POLICY "Clients can delete own agents"
    ON sub_agents
    FOR DELETE
    TO authenticated
    USING (client_id IN (
        SELECT id FROM clients WHERE profile_id = auth.uid()
    ));
```

#### sub_agents.config JSONB Structure
```json
{
  "wizard_data": {
    "template_type": "sales",
    "personality": "professional",
    "tone_formal": 70,
    "tone_direct": 80,
    "niche": "mmn"
  },
  "fields": {
    "standard": {
      "name": { "enabled": true, "required": true },
      "email": { "enabled": true, "required": false },
      "phone": { "enabled": true, "required": true },
      "country": { "enabled": false, "required": false },
      "company": { "enabled": false, "required": false }
    },
    "custom": [
      {
        "id": "field_1",
        "label": "Experience Level",
        "type": "dropdown",
        "required": true,
        "options": ["Beginner", "Intermediate", "Advanced"],
        "order": 1
      }
    ]
  },
  "integrations": {
    "whatsapp": true,
    "email": true,
    "database": false
  },
  "conversation_flow": {
    "greeting": "Hello! I'm here to help you...",
    "questions_order": ["name", "phone", "field_1", "email"]
  }
}
```

### Pydantic Models

```python
# backend/src/models/wizard.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID
from datetime import datetime

class CustomFieldConfig(BaseModel):
    """Configuration for a custom field"""
    id: str
    label: str
    type: Literal['text', 'textarea', 'number', 'date', 'time', 'radio', 'checkbox', 'dropdown']
    required: bool = False
    validation: Optional[Dict[str, Any]] = None
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None
    order: int

class StandardFieldConfig(BaseModel):
    """Configuration for standard fields"""
    enabled: bool
    required: bool

class WizardStep1Data(BaseModel):
    """Step 1: Objetivo"""
    template_type: Literal['customer_service', 'sales', 'support', 'recruitment', 'custom']
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    niche: Literal['mmn', 'clinicas', 'vereadores', 'ecommerce', 'generico']

class WizardStep2Data(BaseModel):
    """Step 2: Personalidade"""
    personality: Literal['professional', 'friendly', 'technical', 'casual']
    tone_formal: int = Field(..., ge=0, le=100)
    tone_direct: int = Field(..., ge=0, le=100)

class WizardStep3Data(BaseModel):
    """Step 3: Campos"""
    standard_fields: Dict[str, StandardFieldConfig]
    custom_fields: List[CustomFieldConfig]

class WizardStep4Data(BaseModel):
    """Step 4: Integrações"""
    integrations: Dict[str, bool]

class WizardSessionCreate(BaseModel):
    """Create wizard session"""
    client_id: UUID

class WizardSessionUpdate(BaseModel):
    """Update wizard step"""
    step_number: int = Field(..., ge=1, le=5)
    data: Dict[str, Any]

class WizardSession(BaseModel):
    """Wizard session response"""
    id: UUID
    client_id: UUID
    current_step: int
    step_1_data: Optional[WizardStep1Data] = None
    step_2_data: Optional[WizardStep2Data] = None
    step_3_data: Optional[WizardStep3Data] = None
    step_4_data: Optional[WizardStep4Data] = None
    created_at: datetime
    updated_at: datetime

class SandboxMessageRequest(BaseModel):
    """Send message in sandbox"""
    message: str

class SandboxMessageResponse(BaseModel):
    """Sandbox message response"""
    role: Literal['user', 'assistant']
    content: str
    timestamp: datetime
    collected_data: Optional[Dict[str, Any]] = None

class PublicationResult(BaseModel):
    """Agent publication result"""
    agent_id: UUID
    slug: str
    public_url: str
    embed_code: str
    qr_code_url: str
    status: str
```

## Error Handling

### Validation Errors

**Wizard Step Validation:**
- Step 1: Name required (min 3 chars), template_type required
- Step 2: Personality required, tone values 0-100
- Step 3: At least one field must be enabled
- Step 4: No validation (integrations are optional)
- Step 5: Sandbox test must complete successfully before publish

**Custom Field Validation:**
- Label required (min 1 char)
- Type must be valid enum value
- Options required for radio/checkbox/dropdown types
- Validation rules must match field type

**Slug Generation:**
- Must be unique per client
- Auto-append number if collision (agent-name, agent-name-2, etc)
- Only lowercase letters, numbers, hyphens

### Error Responses

```python
# 400 Bad Request - Validation Error
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "name",
            "message": "Name must be at least 3 characters"
        }
    ]
}

# 404 Not Found - Wizard Session Not Found
{
    "detail": "Wizard session not found"
}

# 409 Conflict - Slug Already Exists
{
    "detail": "Agent slug already exists",
    "suggestion": "agent-name-2"
}

# 403 Forbidden - B2C Limit Reached
{
    "detail": "B2C clients can only create 1 agent",
    "upgrade_url": "/pricing"
}

# 500 Internal Server Error
{
    "detail": "Failed to generate QR code",
    "error_code": "QR_GENERATION_FAILED"
}
```

## Testing Strategy

### Unit Tests

**Backend:**
- `test_wizard_service.py`: Test wizard CRUD operations
- `test_template_service.py`: Test template loading and system prompt generation
- `test_sandbox_service.py`: Test sandbox creation and message processing
- `test_publication_service.py`: Test slug generation, URL creation, embed code, QR code

**Frontend:**
- `AgentWizard.test.tsx`: Test wizard navigation and state management
- `Step1Objective.test.tsx`: Test template selection and name validation
- `Step2Personality.test.tsx`: Test personality selection and preview updates
- `Step3Fields.test.tsx`: Test field configuration and reordering
- `Step4Integrations.test.tsx`: Test integration status display
- `Step5TestPublish.test.tsx`: Test sandbox interaction and publication

### Integration Tests

**Wizard Flow:**
1. Create wizard session
2. Complete all 5 steps
3. Test in sandbox
4. Publish agent
5. Verify agent is active and accessible

**Template Application:**
1. Select template
2. Verify pre-populated values
3. Modify values
4. Verify system prompt reflects changes

**Sandbox Testing:**
1. Start sandbox
2. Send messages
3. Verify agent responses
4. Verify data collection
5. Clean up sandbox

**Publication:**
1. Publish agent
2. Verify slug uniqueness
3. Verify public URL accessibility
4. Verify embed code validity
5. Verify QR code generation

### Property-Based Tests

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

**Property 1: Wizard progress persistence**
*For any* wizard session and any step data, saving progress then retrieving the session should return the same data
**Validates: Requirements 10.1, 10.2**

**Property 2: Slug uniqueness**
*For any* agent name and client, generating a slug should produce a unique identifier that doesn't conflict with existing agents for that client
**Validates: Requirements 8.1**

**Property 3: Template application idempotence**
*For any* template type, applying the template multiple times should produce the same initial configuration
**Validates: Requirements 3.2, 3.3**

**Property 4: Custom field validation**
*For any* custom field configuration, the agent should enforce the specified validation rules during conversations
**Validates: Requirements 12.1, 12.2, 12.3**

**Property 5: Sandbox isolation**
*For any* sandbox session, data collected should not persist to production conversations
**Validates: Requirements 7.2, 7.3**

**Property 6: Integration status consistency**
*For any* client, the integration status displayed in Step 4 should match the actual integration configuration in the database
**Validates: Requirements 6.2, 6.3**

**Property 7: Publication atomicity**
*For any* agent publication, either all assets (slug, URL, embed code, QR code) are generated successfully or none are
**Validates: Requirements 8.1, 8.2, 8.3, 8.4**

**Property 8: B2C agent limit enforcement**
*For any* B2C client, attempting to create a second active agent should be rejected
**Validates: Requirements 2.3, 2.4**

**Property 9: Field order preservation**
*For any* set of custom fields with specified order, the conversation flow should ask questions in the exact order specified
**Validates: Requirements 5.5**

**Property 10: Multi-language consistency**
*For any* agent with multi-language support, field labels and validation messages should be translated consistently across all supported languages
**Validates: Requirements 15.5**

## Performance Considerations

**Wizard Session Storage:**
- Store wizard sessions in database (not Redis) for persistence
- Clean up abandoned sessions after 30 days
- Index on client_id for fast retrieval

**Template Loading:**
- Templates stored in-memory (Python constants)
- No database queries for template retrieval
- Fast system prompt generation (<100ms)

**Sandbox Performance:**
- Limit sandbox conversations to 50 messages
- Auto-cleanup after 1 hour of inactivity
- Use same LangGraph infrastructure as production agents

**QR Code Generation:**
- Generate on-demand (not pre-generated)
- Cache QR codes in CDN for 24 hours
- Use lightweight library (qrcode or segno)

**Slug Generation:**
- Check uniqueness with database query
- Use index on (client_id, slug) for fast lookup
- Retry with incremented suffix if collision

## Security Considerations

**Wizard Sessions:**
- Associate with authenticated client only
- Validate client_id matches auth.uid()
- Prevent cross-client access

**Sandbox Isolation:**
- Mark sandbox conversations with is_test flag
- Never send real notifications from sandbox
- Clean up sandbox data after test

**Public URLs:**
- Generate unpredictable slugs (include random component if needed)
- Rate limit public agent access (100 requests/minute per IP)
- Monitor for abuse

**Embed Code:**
- Include CSP headers in embed code
- Sanitize all user inputs in embedded chat
- Prevent XSS attacks

**Integration Access:**
- Verify client owns integration before enabling
- Encrypt integration credentials in database
- Audit integration usage

