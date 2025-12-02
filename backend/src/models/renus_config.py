"""
Renus Config Models - Pydantic models for RENUS configuration
Sprint 04 - Sistema Multi-Agente

Models for managing RENUS agent configuration per client.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class RenusConfigBase(BaseModel):
    """Base model for RENUS configuration"""
    
    # System Prompt and Instructions
    system_prompt: str = Field(
        ...,
        description="Main system prompt for RENUS agent",
        min_length=10
    )
    instructions: Optional[str] = Field(
        None,
        description="Additional instructions for the agent"
    )
    
    # Model Configuration
    model: str = Field(
        default="gpt-4-turbo-preview",
        description="LLM model to use"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for generation (0-2)"
    )
    max_tokens: int = Field(
        default=2048,
        ge=1,
        le=4096,
        description="Maximum tokens for response (1-4096)"
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Top P for nucleus sampling (0-1)"
    )
    
    # Guardrails
    guardrails: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Guardrails configuration (content filters, rate limits, etc)"
    )
    
    # Tools Configuration
    enabled_tools: Optional[List[str]] = Field(
        default_factory=list,
        description="List of enabled tool IDs"
    )
    
    # Topics and Context
    topics: Optional[List[str]] = Field(
        default_factory=list,
        description="Main topics the agent should handle"
    )
    
    # Advanced Settings
    streaming: bool = Field(
        default=True,
        description="Enable streaming responses"
    )
    memory_enabled: bool = Field(
        default=True,
        description="Enable conversation memory"
    )
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate model is supported"""
        valid_models = [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4o-mini",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus"
        ]
        if v not in valid_models:
            raise ValueError(f"Model must be one of: {', '.join(valid_models)}")
        return v
    
    @field_validator('system_prompt')
    @classmethod
    def validate_system_prompt(cls, v: str) -> str:
        """Validate system prompt is not empty"""
        if not v or len(v.strip()) < 10:
            raise ValueError("System prompt must be at least 10 characters")
        return v.strip()


class RenusConfigCreate(RenusConfigBase):
    """Model for creating RENUS configuration"""
    client_id: Optional[UUID] = Field(
        None,
        description="Client ID (will be set from auth context)"
    )


class RenusConfigUpdate(BaseModel):
    """Model for updating RENUS configuration (all fields optional)"""
    
    system_prompt: Optional[str] = Field(None, min_length=10)
    instructions: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    guardrails: Optional[Dict[str, Any]] = None
    enabled_tools: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    streaming: Optional[bool] = None
    memory_enabled: Optional[bool] = None
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, v: Optional[str]) -> Optional[str]:
        """Validate model if provided"""
        if v is None:
            return v
        valid_models = [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4o-mini",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus"
        ]
        if v not in valid_models:
            raise ValueError(f"Model must be one of: {', '.join(valid_models)}")
        return v
    
    @field_validator('system_prompt')
    @classmethod
    def validate_system_prompt(cls, v: Optional[str]) -> Optional[str]:
        """Validate system prompt if provided"""
        if v is None:
            return v
        if len(v.strip()) < 10:
            raise ValueError("System prompt must be at least 10 characters")
        return v.strip()


class RenusConfigResponse(RenusConfigBase):
    """Model for RENUS configuration responses"""
    
    id: int
    client_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Partial update models for specific sections

class InstructionsUpdate(BaseModel):
    """Model for updating only instructions"""
    system_prompt: str = Field(..., min_length=10)
    instructions: Optional[str] = None


class GuardrailsUpdate(BaseModel):
    """Model for updating only guardrails"""
    guardrails: Dict[str, Any] = Field(
        ...,
        description="Guardrails configuration"
    )


class AdvancedUpdate(BaseModel):
    """Model for updating only advanced settings"""
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    streaming: Optional[bool] = None
    memory_enabled: Optional[bool] = None


class ToolsUpdate(BaseModel):
    """Model for updating enabled tools"""
    enabled_tools: List[str] = Field(
        ...,
        description="List of enabled tool IDs"
    )
