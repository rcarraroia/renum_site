"""
Modelos Pydantic para Lead
Baseado na estrutura REAL do banco de dados
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal, List
from datetime import datetime
from src.utils.validators import validate_phone


class LeadBase(BaseModel):
    """Schema base de Lead"""
    name: str = Field(..., min_length=2, max_length=200)
    phone: str = Field(..., min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    source: Literal["pesquisa", "home", "campanha", "indicacao"] = Field(..., description="Origem do lead")
    notes: Optional[str] = None
    score: Optional[int] = Field(None, ge=0, le=100, description="Score de qualificação (0-100)")
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        """Valida formato de telefone"""
        if not validate_phone(v):
            raise ValueError('Invalid phone format')
        return v


class LeadCreate(LeadBase):
    """Schema para criar Lead"""
    status: Literal["novo", "qualificado", "em_negociacao", "perdido"] = "novo"
    subagent_id: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schema para atualizar Lead"""
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    source: Optional[Literal["pesquisa", "home", "campanha", "indicacao"]] = None
    status: Optional[Literal["novo", "qualificado", "em_negociacao", "perdido"]] = None
    subagent_id: Optional[str] = None
    notes: Optional[str] = None
    score: Optional[int] = Field(None, ge=0, le=100)
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        """Valida formato de telefone"""
        if v and not validate_phone(v):
            raise ValueError('Invalid phone format')
        return v


class LeadResponse(LeadBase):
    """Schema de resposta de Lead"""
    id: str
    status: Literal["novo", "qualificado", "em_negociacao", "perdido"]
    subagent_id: Optional[str] = None
    first_contact_at: Optional[datetime] = None
    last_interaction_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LeadList(BaseModel):
    """Schema de lista paginada de Leads"""
    items: List[LeadResponse]
    total: int
    page: int
    limit: int
    has_next: bool


class LeadConvertRequest(BaseModel):
    """Schema para converter Lead em Cliente"""
    company_name: str = Field(..., min_length=2, max_length=200)
    cnpj: str = Field(..., min_length=14, max_length=18)
    segment: str = Field(..., min_length=2, max_length=100)
    plan: Literal["basic", "pro", "enterprise"] = "basic"
