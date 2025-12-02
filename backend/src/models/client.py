"""
Modelos Pydantic para Cliente
Baseado na estrutura REAL do banco de dados
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, Dict, Any, List
from datetime import datetime
from src.utils.validators import validate_document


class ContactInfo(BaseModel):
    """Informações de contato (JSONB)"""
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None


class AddressInfo(BaseModel):
    """Informações de endereço (JSONB)"""
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = "Brasil"


class ClientBase(BaseModel):
    """Schema base de Cliente"""
    company_name: str = Field(..., min_length=3, max_length=200)
    document: Optional[str] = Field(None, description="CPF ou CNPJ")
    website: Optional[str] = None
    segment: str = Field(..., description="Segmento de atuação")
    contact: Optional[ContactInfo] = None
    address: Optional[AddressInfo] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    
    @field_validator('document')
    @classmethod
    def validate_document_format(cls, v):
        """Valida formato de CPF/CNPJ"""
        if v and not validate_document(v):
            raise ValueError('Invalid document format (CPF/CNPJ)')
        return v


class ClientCreate(ClientBase):
    """Schema para criar Cliente"""
    status: Literal["active", "inactive", "suspended"] = "active"


class ClientUpdate(BaseModel):
    """Schema para atualizar Cliente"""
    company_name: Optional[str] = Field(None, min_length=3, max_length=200)
    document: Optional[str] = None
    website: Optional[str] = None
    segment: Optional[str] = None
    status: Optional[Literal["active", "inactive", "suspended"]] = None
    contact: Optional[ContactInfo] = None
    address: Optional[AddressInfo] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    
    @field_validator('document')
    @classmethod
    def validate_document_format(cls, v):
        """Valida formato de CPF/CNPJ"""
        if v and not validate_document(v):
            raise ValueError('Invalid document format (CPF/CNPJ)')
        return v


class ClientResponse(ClientBase):
    """Schema de resposta de Cliente"""
    id: str
    status: Literal["active", "inactive", "suspended"]
    last_interaction: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ClientList(BaseModel):
    """Schema de lista paginada de Clientes"""
    items: List[ClientResponse]
    total: int
    page: int
    limit: int
    has_next: bool
