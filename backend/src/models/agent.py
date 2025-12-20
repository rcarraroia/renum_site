"""
Modelos de Agente - Pydantic Models
Fase 2 - Modelo de Agente Unificado
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field, field_validator

# Modelos LLM suportados
MODELOS_SUPORTADOS = [
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-4o",
    "gpt-4o-mini",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus"
]

# Canais suportados
CANAIS_SUPORTADOS = ["whatsapp", "web", "sms", "email"]

# Tipos de template
TEMPLATES_SUPORTADOS = ["custom", "mmn", "vereador", "clinica", "pesquisa"]

# Status suportados (mantido para compatibilidade, mas mapeado para is_active)
STATUS_SUPORTADOS = ["draft", "active", "paused", "archived"]

class AgentRole(str, Enum):
    SYSTEM_ORCHESTRATOR = "system_orchestrator"
    SYSTEM_SUPERVISOR = "system_supervisor"
    CLIENT_AGENT = "client_agent"

class AgentBase(BaseModel):
    """Modelo base de agente com campos comuns"""
    
    role: AgentRole = Field(default=AgentRole.CLIENT_AGENT, description="Papel do agente no sistema")
    name: str = Field(..., min_length=1, max_length=100, description="Nome do agente")
    description: Optional[str] = Field(None, max_length=500, description="Descrição do propósito do agente")
    client_id: Optional[UUID] = Field(None, description="ID do Cliente dono deste agente (opcional para sistema)")
    parent_id: Optional[UUID] = Field(None, description="ID do agente pai (ex: Renus)")
    
    # Config é o container principal para model, prompt, provider, tools
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuração principal (model, prompt, tools)")
    
    sicc_enabled: bool = Field(default=True, description="Se o SICC está ativado")
    fine_tuning_config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Configuração de Fine-tuning")
    
    slug: Optional[str] = Field(None, max_length=100, description="Identificador amigável para URL")
    is_active: bool = Field(default=True, description="Se o agente está ativo")
    is_public: bool = Field(default=False, description="Se é acessível publicamente")
    public_url: Optional[str] = Field(None, description="URL pública do agente")
    
    # Campos de Template (Marketplace)
    is_template: bool = Field(default=False, description="Se é template do marketplace")
    category: Optional[str] = Field(None, description="Categoria: b2b ou b2c")
    niche: Optional[str] = Field(None, max_length=100, description="Nicho de atuação")
    marketplace_visible: bool = Field(default=False, description="Visível no marketplace")
    available_tools: Dict[str, Any] = Field(default_factory=dict, description="Ferramentas configuráveis pelo cliente")
    available_integrations: Dict[str, Any] = Field(default_factory=dict, description="Integrações configuráveis pelo cliente")

    # Propriedades auxiliares para acessar campos dentro de Config de forma fácil
    @property
    def model(self) -> str:
        return self.config.get('model', 'gpt-4o-mini')

    @property
    def system_prompt(self) -> str:
        return self.config.get('system_prompt', '')
        
    @property
    def channel(self) -> Optional[str]:
        return self.config.get('channel')


class AgentCreate(AgentBase):
    """Modelo para criação de novo agente"""
    pass 


class AgentUpdate(BaseModel):
    """Modelo para atualização de agente"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    config: Optional[Dict[str, Any]] = None
    sicc_enabled: Optional[bool] = None
    fine_tuning_config: Optional[Dict[str, Any]] = None
    
    # Campos de status legados, mapear logicamente no service se necessário
    status: Optional[str] = None 
    
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    public_url: Optional[str] = None
    
    role: Optional[AgentRole] = None
    client_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None


class AgentResponse(AgentBase):
    """Modelo de resposta (inclui campos de banco de dados)"""
    
    id: UUID = Field(..., description="Identificador Único")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")
    
    class Config:
        from_attributes = True


class AgentListItem(BaseModel):
    """Modelo para listagem leve de agentes"""
    
    id: UUID
    role: AgentRole
    client_id: Optional[UUID]
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentStats(BaseModel):
    """Estatísticas de uso do agente"""
    
    agent_id: UUID
    sub_agents_count: int = Field(default=0, description="Quantidade de sub-agentes")
    total_conversations: int = Field(default=0, description="Total de conversas")
    active_conversations: int = Field(default=0, description="Conversas ativas")
    total_messages: int = Field(default=0, description="Total de mensagens")
    access_count: int = Field(default=0, description="Acessos à URL pública")
    last_used_at: Optional[datetime] = Field(None, description="Último uso")
    
    class Config:
        from_attributes = True
