"""
Payment API Routes
Endpoints para pagamentos e assinaturas
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from src.models.payment import Plan, SubscriptionCreate, SubscriptionResponse
from src.models.user import UserProfile
from src.services.payment_service import PaymentService, PLANS
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/payment", tags=["payment"])


@router.get("/plans", response_model=List[Plan])
async def list_plans(
    category: Optional[str] = None,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Lista planos disponíveis
    
    Opcionalmente filtra por categoria (b2c/b2b)
    """
    payment_service = PaymentService()
    plans_dict = payment_service.get_plans(category=category)
    
    # Converter dict para lista de Plans
    plans = []
    for key, plan_data in plans_dict.items():
        plans.append(Plan(
            key=key,
            **plan_data
        ))
    
    return plans


@router.post("/subscribe", response_model=SubscriptionResponse)
async def create_subscription(
    data: SubscriptionCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Cria assinatura para um template
    
    Detecta automaticamente o gateway (Asaas/Stripe) baseado no país do cliente
    """
    payment_service = PaymentService()
    
    try:
        result = await payment_service.create_subscription(
            client_id=current_user.client_id,
            plan_key=data.plan_key,
            template_id=data.template_id
        )
        
        return SubscriptionResponse(**result)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create subscription: {str(e)}"
        )


@router.post("/cancel")
async def cancel_subscription(
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Cancela assinatura ativa do cliente
    """
    payment_service = PaymentService()
    
    try:
        result = await payment_service.cancel_subscription(
            client_id=current_user.client_id
        )
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}"
        )


@router.get("/subscription")
async def get_subscription_status(
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Retorna status da assinatura atual do cliente
    """
    payment_service = PaymentService()
    
    try:
        client = await payment_service.get_client(current_user.client_id)
        subscription = client.get("subscription")
        
        if not subscription:
            return {"status": "none", "message": "No active subscription"}
        
        return subscription
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscription status: {str(e)}"
        )


@router.post("/webhook/asaas")
async def asaas_webhook(payload: dict):
    """
    Webhook do Asaas para notificações de pagamento
    
    TODO: Implementar validação de assinatura
    """
    # Processar evento do Asaas
    event_type = payload.get("event")
    
    if event_type == "PAYMENT_CONFIRMED":
        # Ativar template/agente
        pass
    elif event_type == "PAYMENT_OVERDUE":
        # Suspender agente
        pass
    
    return {"status": "received"}


@router.post("/webhook/stripe")
async def stripe_webhook(payload: dict):
    """
    Webhook do Stripe para notificações de pagamento
    
    TODO: Implementar validação de assinatura
    """
    import stripe
    from src.config.settings import settings
    
    # Verificar assinatura do webhook
    # sig_header = request.headers.get('stripe-signature')
    # event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    
    event_type = payload.get("type")
    
    if event_type == "invoice.payment_succeeded":
        # Ativar template/agente
        pass
    elif event_type == "invoice.payment_failed":
        # Suspender agente
        pass
    
    return {"status": "received"}
