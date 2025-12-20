"""
Payment Models
Modelos para pagamentos, planos e assinaturas
"""
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class Plan(BaseModel):
    """Plano de assinatura"""
    key: str = Field(..., description="Chave única do plano")
    name: str = Field(..., description="Nome do plano")
    category: Literal['b2c', 'b2b'] = Field(..., description="Categoria do plano")
    price_brl: Optional[float] = Field(None, description="Preço em BRL")
    price_usd: Optional[float] = Field(None, description="Preço em USD")
    stripe_price_id: Optional[str] = Field(None, description="ID do preço no Stripe")
    features: List[str] = Field(default_factory=list, description="Lista de funcionalidades")
    
    class Config:
        json_schema_extra = {
            "example": {
                "key": "b2c_pro",
                "name": "B2C Pro",
                "category": "b2c",
                "price_brl": 99.90,
                "price_usd": 19.99,
                "stripe_price_id": "price_b2c_pro",
                "features": ["1 agente", "5000 mensagens/mês", "Todas ferramentas"]
            }
        }


class SubscriptionCreate(BaseModel):
    """Dados para criar assinatura"""
    plan_key: str = Field(..., description="Chave do plano")
    template_id: UUID = Field(..., description="ID do template sendo assinado")
    payment_method: Optional[Literal['credit_card', 'boleto', 'pix']] = Field(
        'credit_card',
        description="Método de pagamento (apenas Asaas)"
    )


class SubscriptionResponse(BaseModel):
    """Resposta de assinatura criada"""
    gateway: Literal['asaas', 'stripe'] = Field(..., description="Gateway utilizado")
    subscription_id: str = Field(..., description="ID da assinatura no gateway")
    status: str = Field(..., description="Status da assinatura")
    payment_url: Optional[str] = Field(None, description="URL de pagamento (Asaas)")
    client_secret: Optional[str] = Field(None, description="Client secret (Stripe)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gateway": "asaas",
                "subscription_id": "sub_abc123",
                "status": "active",
                "payment_url": "https://www.asaas.com/pay/abc123"
            }
        }


class PaymentMethod(BaseModel):
    """Método de pagamento salvo"""
    id: str
    type: Literal['credit_card', 'boleto', 'pix']
    last_digits: Optional[str] = None
    brand: Optional[str] = None
    is_default: bool = False


class Subscription(BaseModel):
    """Assinatura ativa"""
    id: UUID
    client_id: UUID
    template_id: UUID
    gateway: Literal['asaas', 'stripe']
    external_subscription_id: str
    plan: str
    status: Literal['active', 'cancelled', 'past_due', 'unpaid']
    created_at: datetime
    cancelled_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "123e4567-e89b-12d3-a456-426614174001",
                "template_id": "123e4567-e89b-12d3-a456-426614174002",
                "gateway": "asaas",
                "external_subscription_id": "sub_abc123",
                "plan": "B2C Pro",
                "status": "active",
                "created_at": "2025-12-18T18:00:00Z"
            }
        }
