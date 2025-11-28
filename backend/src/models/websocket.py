"""WebSocket message types and models"""
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from enum import Enum


class WSMessageType(str, Enum):
    """WebSocket message types"""
    # Client → Server
    SEND_MESSAGE = "send_message"
    TYPING_START = "typing_start"
    TYPING_STOP = "typing_stop"
    MARK_READ = "mark_read"
    
    # Server → Client
    NEW_MESSAGE = "new_message"
    USER_TYPING = "user_typing"
    USER_STOPPED_TYPING = "user_stopped_typing"
    PRESENCE_UPDATE = "presence_update"
    ERROR = "error"
    CONNECTED = "connected"


class WSMessage(BaseModel):
    """WebSocket message wrapper"""
    type: WSMessageType
    payload: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
