"""
ISA Command Models - Pydantic Models for ISA Administrative Commands
Sprint 04 - Sistema Multi-Agente

Models for tracking ISA (Intelligent System Assistant) command executions
for audit and compliance purposes.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class IsaCommandBase(BaseModel):
    """Base ISA command model"""
    
    admin_id: UUID = Field(..., description="UUID of the admin who executed the command")
    user_message: str = Field(..., min_length=1, description="Original message from admin")
    assistant_response: str = Field(..., min_length=1, description="ISA's response")
    command_executed: bool = Field(default=False, description="Whether a command was actually executed")
    command_type: Optional[str] = Field(None, description="Type of command (query, report, bulk_action, etc)")
    target_entity: Optional[str] = Field(None, description="Entity affected (leads, clients, interviews, etc)")
    affected_records: Optional[int] = Field(None, ge=0, description="Number of records affected")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional command metadata")
    
    @field_validator('user_message', 'assistant_response')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Validate message is not empty"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class IsaCommandCreate(IsaCommandBase):
    """Model for creating ISA command records"""
    pass


class IsaCommandResponse(IsaCommandBase):
    """Model for ISA command responses (includes database fields)"""
    
    id: UUID = Field(..., description="Unique identifier")
    executed_at: datetime = Field(..., description="Timestamp when command was executed")
    created_at: datetime = Field(..., description="Record creation timestamp")
    
    class Config:
        from_attributes = True


class IsaCommandListItem(BaseModel):
    """Model for ISA command list items (lightweight)"""
    
    id: UUID
    admin_id: UUID
    user_message: str
    command_executed: bool
    command_type: Optional[str]
    target_entity: Optional[str]
    affected_records: Optional[int]
    executed_at: datetime
    
    class Config:
        from_attributes = True


class IsaCommandStats(BaseModel):
    """Model for ISA command statistics"""
    
    total_commands: int = Field(default=0, description="Total commands executed")
    successful_commands: int = Field(default=0, description="Commands that executed successfully")
    failed_commands: int = Field(default=0, description="Commands that failed")
    queries: int = Field(default=0, description="Query commands")
    reports: int = Field(default=0, description="Report generation commands")
    bulk_actions: int = Field(default=0, description="Bulk action commands")
    most_active_admin: Optional[UUID] = Field(None, description="Admin with most commands")
    last_command_at: Optional[datetime] = Field(None, description="Timestamp of last command")
    
    class Config:
        from_attributes = True


class IsaChatMessage(BaseModel):
    """Model for ISA chat messages (frontend)"""
    
    role: str = Field(..., pattern="^(user|assistant)$", description="Message role")
    content: str = Field(..., min_length=1, description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    command_executed: Optional[bool] = Field(None, description="Whether command was executed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate content is not empty"""
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class IsaChatRequest(BaseModel):
    """Model for ISA chat requests"""
    
    message: str = Field(..., min_length=1, max_length=2000, description="User message to ISA")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the command")
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate message is not empty"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class IsaChatResponse(BaseModel):
    """Model for ISA chat responses"""
    
    message: str = Field(..., description="ISA's response message")
    command_executed: bool = Field(default=False, description="Whether a command was executed")
    command_type: Optional[str] = Field(None, description="Type of command executed")
    result: Optional[Dict[str, Any]] = Field(None, description="Command execution result")
    suggestions: Optional[List[str]] = Field(None, description="Suggested follow-up commands")
    
    class Config:
        from_attributes = True
