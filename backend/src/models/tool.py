"""
Tool Models - Pydantic models for agent tools
Sprint 04 - Sistema Multi-Agente

Models for managing tools that agents can invoke.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
import json


class ToolBase(BaseModel):
    """Base model for tools"""
    
    name: str = Field(
        ...,
        description="Tool name (unique identifier)",
        min_length=3,
        max_length=100
    )
    description: str = Field(
        ...,
        description="Description of what the tool does",
        min_length=10
    )
    function_name: str = Field(
        ...,
        description="Python function name to invoke",
        pattern=r'^[a-z_][a-z0-9_]*$'
    )
    parameters_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema for tool parameters"
    )
    category: Optional[str] = Field(
        default="general",
        description="Tool category: database, messaging, email, analytics, etc"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the tool is active and available"
    )
    
    @field_validator('parameters_schema')
    @classmethod
    def validate_parameters_schema(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that parameters_schema is valid JSON schema"""
        if not v:
            raise ValueError("parameters_schema cannot be empty")
        
        # Check for required JSON schema fields
        if 'type' not in v:
            raise ValueError("parameters_schema must have 'type' field")
        
        # Try to serialize to ensure it's valid JSON
        try:
            json.dumps(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"parameters_schema must be valid JSON: {e}")
        
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate tool name format"""
        # Name should be lowercase with underscores
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Tool name must contain only letters, numbers, underscores, and hyphens")
        return v.lower()


class ToolCreate(ToolBase):
    """Model for creating tools"""
    pass


class ToolUpdate(BaseModel):
    """Model for updating tools (all fields optional)"""
    
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    function_name: Optional[str] = Field(None, pattern=r'^[a-z_][a-z0-9_]*$')
    parameters_schema: Optional[Dict[str, Any]] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    
    @field_validator('parameters_schema')
    @classmethod
    def validate_parameters_schema(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate parameters_schema if provided"""
        if v is None:
            return v
        
        if 'type' not in v:
            raise ValueError("parameters_schema must have 'type' field")
        
        try:
            json.dumps(v)
        except (TypeError, ValueError) as e:
            raise ValueError(f"parameters_schema must be valid JSON: {e}")
        
        return v


class ToolResponse(ToolBase):
    """Model for tool responses"""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ToolListItem(BaseModel):
    """Simplified model for tool list items"""
    
    id: UUID
    name: str
    description: str
    category: str
    is_active: bool
    
    class Config:
        from_attributes = True


class ToolEnableRequest(BaseModel):
    """Model for enabling/disabling a tool"""
    
    is_active: bool = Field(
        ...,
        description="Whether to enable or disable the tool"
    )
