"""
Sub-Agent Models - Pydantic Models for Sub-Agents
Sprint 04 - Sistema Multi-Agente

Models for managing specialized sub-agents that can be dynamically configured.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# Supported models for sub-agents
SUPPORTED_MODELS = [
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-4o-mini",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus"
]

# Supported channels
SUPPORTED_CHANNELS = ["whatsapp", "web", "sms", "email"]


class SubAgentBase(BaseModel):
    """Base sub-agent model with common fields"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Name of the sub-agent")
    description: Optional[str] = Field(None, max_length=500, description="Description of the sub-agent's purpose")
    channel: str = Field(..., description="Communication channel (whatsapp, web, sms, email)")
    system_prompt: str = Field(..., min_length=10, description="System prompt that defines agent behavior")
    topics: Optional[List[str]] = Field(default=None, description="Topics/contexts this agent handles")
    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    is_active: bool = Field(default=True, description="Whether the sub-agent is active")
    fine_tuning_config: Optional[Dict[str, Any]] = Field(default=None, description="Fine-tuning configuration")
    
    @field_validator('channel')
    @classmethod
    def validate_channel(cls, v: str) -> str:
        """Validate channel is one of supported channels"""
        if v not in SUPPORTED_CHANNELS:
            raise ValueError(f"Channel must be one of: {', '.join(SUPPORTED_CHANNELS)}")
        return v
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate model is one of supported models"""
        if v not in SUPPORTED_MODELS:
            raise ValueError(f"Model must be one of: {', '.join(SUPPORTED_MODELS)}")
        return v
    
    @field_validator('system_prompt')
    @classmethod
    def validate_system_prompt(cls, v: str) -> str:
        """Validate system prompt is not empty"""
        if not v or not v.strip():
            raise ValueError("System prompt cannot be empty")
        return v.strip()


class SubAgentCreate(SubAgentBase):
    """Model for creating a new sub-agent"""
    
    config_id: Optional[int] = Field(None, description="Associated renus_config ID")


class SubAgentUpdate(BaseModel):
    """Model for updating a sub-agent (all fields optional)"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    channel: Optional[str] = None
    system_prompt: Optional[str] = Field(None, min_length=10)
    topics: Optional[List[str]] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None
    fine_tuning_config: Optional[Dict[str, Any]] = None
    
    @field_validator('channel')
    @classmethod
    def validate_channel(cls, v: Optional[str]) -> Optional[str]:
        """Validate channel if provided"""
        if v is not None and v not in SUPPORTED_CHANNELS:
            raise ValueError(f"Channel must be one of: {', '.join(SUPPORTED_CHANNELS)}")
        return v
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, v: Optional[str]) -> Optional[str]:
        """Validate model if provided"""
        if v is not None and v not in SUPPORTED_MODELS:
            raise ValueError(f"Model must be one of: {', '.join(SUPPORTED_MODELS)}")
        return v
    
    @field_validator('system_prompt')
    @classmethod
    def validate_system_prompt(cls, v: Optional[str]) -> Optional[str]:
        """Validate system prompt if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError("System prompt cannot be empty")
        return v.strip() if v else None


class SubAgentResponse(SubAgentBase):
    """Model for sub-agent responses (includes database fields)"""
    
    id: UUID = Field(..., description="Unique identifier")
    config_id: Optional[int] = Field(None, description="Associated renus_config ID")
    slug: Optional[str] = Field(None, description="URL-friendly identifier")
    public_url: Optional[str] = Field(None, description="Public URL for this agent")
    access_count: Optional[int] = Field(default=0, description="Number of public accesses")
    is_public: Optional[bool] = Field(default=True, description="Whether agent is publicly accessible")
    knowledge_base: Optional[Dict[str, Any]] = Field(default=None, description="Knowledge base with documents and context")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class SubAgentStats(BaseModel):
    """Model for sub-agent usage statistics"""
    
    sub_agent_id: UUID
    total_interviews: int = Field(default=0, description="Total interviews conducted")
    completed_interviews: int = Field(default=0, description="Successfully completed interviews")
    abandoned_interviews: int = Field(default=0, description="Abandoned interviews")
    completion_rate: float = Field(default=0.0, description="Completion rate (0-100)")
    avg_duration_minutes: Optional[float] = Field(None, description="Average interview duration in minutes")
    last_used_at: Optional[datetime] = Field(None, description="Last time this sub-agent was used")
    
    class Config:
        from_attributes = True


class SubAgentListItem(BaseModel):
    """Model for sub-agent list items (lightweight)"""
    
    id: UUID
    name: str
    description: Optional[str]
    channel: str
    model: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Optional stats (can be joined)
    total_interviews: Optional[int] = None
    completion_rate: Optional[float] = None
    
    class Config:
        from_attributes = True
