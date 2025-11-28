"""Message models with strict validation"""
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID


class MessageBase(BaseModel):
    """Base message model with required fields"""
    conversation_id: UUID
    sender: Literal['admin', 'client', 'system']
    type: Literal['text', 'image', 'file']
    content: str
    metadata: Optional[dict] = None


class MessageCreate(MessageBase):
    """Model for creating a new message"""
    pass


class MessageResponse(MessageBase):
    """Model for message responses"""
    id: UUID
    timestamp: datetime
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
