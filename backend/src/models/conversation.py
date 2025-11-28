"""Conversation models with strict validation"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from uuid import UUID


class ConversationBase(BaseModel):
    """Base conversation model with required fields"""
    client_id: UUID
    status: Literal['active', 'closed', 'pending']
    channel: Literal['whatsapp', 'email', 'web']
    assigned_agent_id: Optional[UUID] = None
    priority: Literal['Low', 'Medium', 'High'] = 'Low'
    summary: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation"""
    pass


class ConversationUpdate(BaseModel):
    """Model for updating an existing conversation"""
    status: Optional[Literal['active', 'closed', 'pending']] = None
    assigned_agent_id: Optional[UUID] = None
    priority: Optional[Literal['Low', 'Medium', 'High']] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None


class ConversationResponse(ConversationBase):
    """Model for conversation responses"""
    id: UUID
    unread_count: int
    start_date: datetime
    last_update: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
