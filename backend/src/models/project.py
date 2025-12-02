"""
Modelos Pydantic para Projeto
Baseado na estrutura REAL do banco de dados
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime, date
from decimal import Decimal


class ProjectBase(BaseModel):
    """Schema base de Projeto"""
    name: str = Field(..., min_length=3, max_length=200)
    type: Literal["AI Native", "Workflow", "Agente Solo"] = Field(..., description="Tipo do projeto")
    description: Optional[str] = Field(None, max_length=2000)
    scope: Optional[str] = Field(None, max_length=5000, description="Escopo detalhado do projeto")
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    budget: Optional[Decimal] = Field(None, ge=0, description="Orçamento do projeto")


class ProjectCreate(ProjectBase):
    """Schema para criar Projeto"""
    client_id: Optional[str] = Field(None, description="ID do cliente (opcional)")
    responsible_id: Optional[str] = Field(None, description="ID do responsável")
    status: Literal["Em Andamento", "Concluído", "Pausado", "Atrasado", "Em Revisão"] = "Em Andamento"
    progress: int = Field(0, ge=0, le=100, description="Progresso em % (0-100)")


class ProjectUpdate(BaseModel):
    """Schema para atualizar Projeto"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    type: Optional[Literal["AI Native", "Workflow", "Agente Solo"]] = None
    description: Optional[str] = Field(None, max_length=2000)
    scope: Optional[str] = Field(None, max_length=5000)
    status: Optional[Literal["Em Andamento", "Concluído", "Pausado", "Atrasado", "Em Revisão"]] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    client_id: Optional[str] = None
    responsible_id: Optional[str] = None
    budget: Optional[Decimal] = Field(None, ge=0)


class ProjectResponse(ProjectBase):
    """Schema de resposta de Projeto"""
    id: str
    client_id: Optional[str] = None
    responsible_id: Optional[str] = None
    status: Literal["Em Andamento", "Concluído", "Pausado", "Atrasado", "Em Revisão"]
    progress: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    """Schema de lista paginada de Projetos"""
    items: List[ProjectResponse]
    total: int
    page: int
    limit: int
    has_next: bool
