"""
Integration Models - Sprint 07A
Pydantic models for integration configurations (WhatsApp, Email, Database)
"""

from datetime import datetime
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
from uuid import UUID


class IntegrationBase(BaseModel):
    """Base model for integration"""
    type: Literal['whatsapp', 'email_smtp', 'email_sendgrid', 'database']
    name: str = Field(..., min_length=1, max_length=255)
    config: Dict[str, Any] = Field(default_factory=dict)


class IntegrationCreate(IntegrationBase):
    """Model for creating integration"""
    client_id: UUID


class IntegrationUpdate(BaseModel):
    """Model for updating integration"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    config: Optional[Dict[str, Any]] = None
    status: Optional[Literal['connected', 'disconnected', 'error']] = None


class Integration(IntegrationBase):
    """Model for integration response"""
    id: UUID
    client_id: UUID
    status: Literal['connected', 'disconnected', 'error'] = 'disconnected'
    last_tested_at: Optional[datetime] = None
    last_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Specific config models for each integration type

class WhatsAppConfig(BaseModel):
    """WhatsApp (Uazapi) configuration"""
    api_url: str = Field(..., description="Uazapi API base URL")
    api_token: str = Field(..., description="Uazapi API token (will be encrypted)")
    phone_number: str = Field(..., description="WhatsApp phone number in international format")
    webhook_secret: Optional[str] = Field(None, description="Webhook validation secret")

    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            raise ValueError('Phone number must start with + and country code')
        if not v[1:].isdigit():
            raise ValueError('Phone number must contain only digits after +')
        return v


class EmailSMTPConfig(BaseModel):
    """Email SMTP configuration"""
    host: str = Field(..., description="SMTP server host")
    port: int = Field(..., ge=1, le=65535, description="SMTP server port")
    username: str = Field(..., description="SMTP username")
    password: str = Field(..., description="SMTP password (will be encrypted)")
    use_tls: bool = Field(True, description="Use TLS encryption")
    from_email: str = Field(..., description="From email address")
    from_name: Optional[str] = Field(None, description="From name")


class EmailSendGridConfig(BaseModel):
    """Email SendGrid configuration"""
    api_key: str = Field(..., description="SendGrid API key (will be encrypted)")
    from_email: str = Field(..., description="From email address")
    from_name: Optional[str] = Field("RENUM", description="From name")


class DatabaseConfig(BaseModel):
    """Client database (Supabase) configuration"""
    supabase_url: str = Field(..., description="Client's Supabase project URL")
    supabase_key: str = Field(..., description="Client's Supabase service key (will be encrypted)")
    read_only: bool = Field(True, description="Restrict to read-only queries")
    allowed_tables: list[str] = Field(default_factory=list, description="Whitelist of allowed tables")


class IntegrationTestResult(BaseModel):
    """Result of integration connection test"""
    success: bool
    message: str
    latency_ms: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


# Type alias for integration types
IntegrationType = Literal['whatsapp', 'email_smtp', 'email_sendgrid', 'database']
