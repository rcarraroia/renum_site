"""
Wizard Models - Sprint 06
Pydantic models for agent creation wizard
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID
from datetime import datetime


class CustomFieldConfig(BaseModel):
    """Configuration for a custom field"""
    id: str = Field(..., description="Unique identifier for the field")
    label: str = Field(..., min_length=1, max_length=100, description="Field label")
    type: Literal['text', 'textarea', 'number', 'date', 'time', 'radio', 'checkbox', 'dropdown']
    required: bool = Field(default=False, description="Whether field is required")
    validation: Optional[Dict[str, Any]] = Field(default=None, description="Validation rules")
    placeholder: Optional[str] = Field(default=None, max_length=200, description="Placeholder text")
    options: Optional[List[str]] = Field(default=None, description="Options for radio/checkbox/dropdown")
    order: int = Field(..., ge=0, description="Display order")
    
    @field_validator('options')
    @classmethod
    def validate_options(cls, v, info):
        """Validate options are provided for choice fields"""
        field_type = info.data.get('type')
        if field_type in ['radio', 'checkbox', 'dropdown']:
            if not v or len(v) == 0:
                raise ValueError(f"Options required for {field_type} fields")
        return v


class StandardFieldConfig(BaseModel):
    """Configuration for standard fields"""
    enabled: bool = Field(default=False, description="Whether field is enabled")
    required: bool = Field(default=False, description="Whether field is required")


class WizardStep1Data(BaseModel):
    """Step 1: Objetivo do Agente"""
    template_type: Literal['customer_service', 'sales', 'support', 'recruitment', 'custom']
    name: str = Field(..., min_length=3, max_length=100, description="Agent name")
    description: Optional[str] = Field(None, max_length=500, description="Agent description")
    niche: Literal['mmn', 'clinicas', 'vereadores', 'ecommerce', 'generico']
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate name doesn't contain special characters"""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class WizardStep2Data(BaseModel):
    """Step 2: Personalidade e Tom"""
    personality: Literal['professional', 'friendly', 'technical', 'casual']
    tone_formal: int = Field(..., ge=0, le=100, description="Formality level (0-100)")
    tone_direct: int = Field(..., ge=0, le=100, description="Directness level (0-100)")
    custom_instructions: Optional[str] = Field(None, max_length=1000, description="Additional custom instructions")


class WizardStep3Data(BaseModel):
    """Step 3: Informações a Coletar"""
    standard_fields: Dict[str, StandardFieldConfig] = Field(
        default_factory=dict,
        description="Standard fields configuration"
    )
    custom_fields: List[CustomFieldConfig] = Field(
        default_factory=list,
        description="Custom fields configuration"
    )
    
    @field_validator('standard_fields')
    @classmethod
    def validate_at_least_one_field(cls, v, info):
        """Validate at least one field is enabled"""
        custom_fields = info.data.get('custom_fields', [])
        enabled_standard = sum(1 for field in v.values() if field.enabled)
        
        if enabled_standard == 0 and len(custom_fields) == 0:
            raise ValueError("At least one field must be enabled")
        
        return v


class WizardStep4Data(BaseModel):
    """Step 4: Integrações"""
    integrations: Dict[str, bool] = Field(
        default_factory=dict,
        description="Enabled integrations (whatsapp, email, database)"
    )


class WizardSessionCreate(BaseModel):
    """Create wizard session"""
    client_id: UUID = Field(..., description="Client ID creating the agent")


class WizardSessionUpdate(BaseModel):
    """Update wizard step"""
    step_number: int = Field(..., ge=1, le=5, description="Step number (1-5)")
    data: Dict[str, Any] = Field(..., description="Step data")


class WizardStepData(BaseModel):
    """Step data only (for PUT endpoint)"""
    data: Dict[str, Any] = Field(..., description="Step data")


class WizardSession(BaseModel):
    """Wizard session response"""
    id: UUID = Field(..., description="Wizard session ID")
    client_id: UUID = Field(..., description="Client ID")
    current_step: int = Field(default=1, ge=1, le=5, description="Current step")
    step_1_data: Optional[WizardStep1Data] = None
    step_2_data: Optional[WizardStep2Data] = None
    step_3_data: Optional[WizardStep3Data] = None
    step_4_data: Optional[WizardStep4Data] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SandboxMessageRequest(BaseModel):
    """Send message in sandbox"""
    message: str = Field(..., min_length=1, max_length=2000, description="Message content")


class SandboxMessageResponse(BaseModel):
    """Sandbox message response"""
    role: Literal['user', 'assistant', 'system']
    content: str
    timestamp: datetime
    collected_data: Optional[Dict[str, Any]] = Field(default=None, description="Data collected so far")


class SandboxSession(BaseModel):
    """Sandbox session"""
    id: UUID
    wizard_id: UUID
    conversation_id: UUID
    created_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True


class PublicationResult(BaseModel):
    """Agent publication result"""
    agent_id: UUID = Field(..., description="Created agent ID")
    slug: str = Field(..., description="URL-friendly slug")
    public_url: str = Field(..., description="Public chat URL")
    embed_code: str = Field(..., description="HTML embed code")
    qr_code_url: str = Field(..., description="QR code image URL")
    status: str = Field(default="active", description="Agent status")


class TemplateInfo(BaseModel):
    """Template information"""
    type: str = Field(..., description="Template type identifier")
    name: str = Field(..., description="Template display name")
    description: str = Field(..., description="Template description")
    default_personality: str = Field(..., description="Default personality")
    default_fields: List[str] = Field(default_factory=list, description="Default fields")
    recommended_integrations: List[str] = Field(default_factory=list, description="Recommended integrations")


class AgentCreateFromWizard(BaseModel):
    """Create agent from wizard session"""
    wizard_id: UUID = Field(..., description="Wizard session ID")
    
    class Config:
        from_attributes = True


class AgentCloneRequest(BaseModel):
    """Clone existing agent"""
    source_agent_id: UUID = Field(..., description="Agent to clone")
    new_name: Optional[str] = Field(None, description="New agent name (defaults to 'Copy of {original}')")


class AgentStatusUpdate(BaseModel):
    """Update agent status"""
    status: Literal['draft', 'active', 'paused', 'inactive']


class AgentListFilter(BaseModel):
    """Filters for agent list"""
    client_id: Optional[UUID] = None
    status: Optional[Literal['draft', 'active', 'paused', 'inactive']] = None
    template_type: Optional[Literal['customer_service', 'sales', 'support', 'recruitment', 'custom']] = None
    search: Optional[str] = Field(None, max_length=100, description="Search in name/description")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class AgentMetrics(BaseModel):
    """Agent usage metrics"""
    agent_id: UUID
    conversations_total: int = Field(default=0, description="Total conversations")
    conversations_today: int = Field(default=0, description="Conversations today")
    leads_qualified: int = Field(default=0, description="Leads qualified")
    conversion_rate: float = Field(default=0.0, ge=0, le=100, description="Conversion rate (%)")
    avg_conversation_duration: Optional[float] = Field(None, description="Average duration in minutes")
    last_conversation_at: Optional[datetime] = None


class AgentListItem(BaseModel):
    """Agent list item (lightweight)"""
    id: UUID
    name: str
    description: Optional[str]
    template_type: str
    status: str
    slug: Optional[str]
    public_url: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    metrics: Optional[AgentMetrics] = None
    
    class Config:
        from_attributes = True
