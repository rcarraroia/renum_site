"""
Payment Service
Serviço unificado de pagamento (Asaas + Stripe)
Detecta automaticamente o gateway baseado no país do cliente
"""
from typing import Dict, Any, Optional, Literal
from uuid import UUID

from src.services.payment.asaas_service import AsaasService
from src.services.payment.stripe_service import StripeService
from src.config.supabase import supabase_admin


# Planos disponíveis
PLANS = {
    # B2C
    "b2c_basic": {
        "name": "B2C Básico",
        "price_brl": 49.90,
        "price_usd": 9.99,
        "stripe_price_id": "price_b2c_basic",  # Criar no Stripe Dashboard
        "features": ["1 agente", "1000 mensagens/mês", "Ferramentas básicas"],
        "category": "b2c"
    },
    "b2c_pro": {
        "name": "B2C Pro",
        "price_brl": 99.90,
        "price_usd": 19.99,
        "stripe_price_id": "price_b2c_pro",
        "features": ["1 agente", "5000 mensagens/mês", "Todas ferramentas"],
        "category": "b2c"
    },
    
    # B2B
    "b2b_starter": {
        "name": "B2B Starter",
        "price_brl": 299.90,
        "price_usd": 59.99,
        "stripe_price_id": "price_b2b_starter",
        "features": ["3 agentes", "10 usuários", "10000 mensagens/mês"],
        "category": "b2b"
    },
    "b2b_business": {
        "name": "B2B Business",
        "price_brl": 599.90,
        "price_usd": 119.99,
        "stripe_price_id": "price_b2b_business",
        "features": ["10 agentes", "50 usuários", "50000 mensagens/mês"],
        "category": "b2b"
    },
    "b2b_enterprise": {
        "name": "B2B Enterprise",
        "price_brl": None,  # Sob consulta
        "price_usd": None,
        "stripe_price_id": None,
        "features": ["Ilimitado", "Ilimitado", "Ilimitado"],
        "category": "b2b"
    }
}


class PaymentService:
    """Serviço unificado de pagamento"""
    
    def __init__(self):
        self.asaas = AsaasService()
        self.stripe = StripeService()
    
    def get_gateway(self, country: str) -> Literal["asaas", "stripe"]:
        """
        Detecta gateway baseado no país
        
        Args:
            country: País do cliente
        
        Returns:
            Nome do gateway (asaas ou stripe)
        """
        brazil_variations = ["brasil", "brazil", "br", "bra"]
        return "asaas" if country.lower() in brazil_variations else "stripe"
    
    async def get_client(self, client_id: UUID) -> Dict[str, Any]:
        """Busca dados do cliente no Supabase"""
        result = supabase_admin.table('clients')\
            .select('*')\
            .eq('id', str(client_id))\
            .single()\
            .execute()
        
        if not result.data:
            raise ValueError(f"Client {client_id} not found")
        
        return result.data
    
    async def create_subscription(
        self,
        client_id: UUID,
        plan_key: str,
        template_id: UUID
    ) -> Dict[str, Any]:
        """
        Cria assinatura no gateway apropriado
        
        Args:
            client_id: ID do cliente
            plan_key: Chave do plano (ex: b2c_pro)
            template_id: ID do template sendo assinado
        
        Returns:
            Dados da assinatura criada
        """
        # Buscar cliente
        client = await self.get_client(client_id)
        
        # Buscar plano
        plan = PLANS.get(plan_key)
        if not plan:
            raise ValueError(f"Plan {plan_key} not found")
        
        # Detectar gateway
        country = client.get("address", {}).get("country", "Brasil")
        gateway = self.get_gateway(country)
        
        # Criar assinatura no gateway apropriado
        if gateway == "asaas":
            return await self._create_asaas_subscription(client, plan, template_id)
        else:
            return await self._create_stripe_subscription(client, plan, template_id)
    
    async def _create_asaas_subscription(
        self,
        client: Dict[str, Any],
        plan: Dict[str, Any],
        template_id: UUID
    ) -> Dict[str, Any]:
        """Cria assinatura no Asaas"""
        # Criar ou buscar cliente no Asaas
        asaas_customer = await self.asaas.create_customer({
            "company_name": client.get("company_name"),
            "email": client.get("contact", {}).get("email"),
            "document": client.get("document"),
            "phone": client.get("contact", {}).get("phone")
        })
        
        # Criar assinatura
        subscription = await self.asaas.create_subscription(
            customer_id=asaas_customer["id"],
            plan_value=plan["price_brl"]
        )
        
        # Salvar referência no banco
        await self._save_subscription(
            client_id=client["id"],
            template_id=template_id,
            gateway="asaas",
            external_id=subscription["id"],
            plan_key=plan["name"],
            status=subscription.get("status", "active")
        )
        
        return {
            "gateway": "asaas",
            "subscription_id": subscription["id"],
            "status": subscription.get("status"),
            "payment_url": subscription.get("invoiceUrl")
        }
    
    async def _create_stripe_subscription(
        self,
        client: Dict[str, Any],
        plan: Dict[str, Any],
        template_id: UUID
    ) -> Dict[str, Any]:
        """Cria assinatura no Stripe"""
        # Criar ou buscar cliente no Stripe
        stripe_customer = await self.stripe.create_customer({
            "company_name": client.get("company_name"),
            "email": client.get("contact", {}).get("email"),
            "id": client.get("id")
        })
        
        # Criar assinatura
        subscription = await self.stripe.create_subscription(
            customer_id=stripe_customer.id,
            price_id=plan["stripe_price_id"]
        )
        
        # Salvar referência no banco
        await self._save_subscription(
            client_id=client["id"],
            template_id=template_id,
            gateway="stripe",
            external_id=subscription.id,
            plan_key=plan["name"],
            status=subscription.status
        )
        
        return {
            "gateway": "stripe",
            "subscription_id": subscription.id,
            "status": subscription.status,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret
        }
    
    async def _save_subscription(
        self,
        client_id: str,
        template_id: UUID,
        gateway: str,
        external_id: str,
        plan_key: str,
        status: str
    ):
        """Salva referência da assinatura no banco"""
        from datetime import datetime
        
        subscription_data = {
            "client_id": client_id,
            "template_id": str(template_id),
            "gateway": gateway,
            "external_subscription_id": external_id,
            "plan": plan_key,
            "status": status,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Criar tabela subscriptions se não existir (migration futura)
        # Por enquanto, salvar em metadata do cliente
        supabase_admin.table('clients')\
            .update({"subscription": subscription_data})\
            .eq('id', client_id)\
            .execute()
    
    async def cancel_subscription(self, client_id: UUID) -> Dict[str, Any]:
        """Cancela assinatura do cliente"""
        client = await self.get_client(client_id)
        subscription_data = client.get("subscription")
        
        if not subscription_data:
            raise ValueError("No active subscription found")
        
        gateway = subscription_data.get("gateway")
        external_id = subscription_data.get("external_subscription_id")
        
        if gateway == "asaas":
            result = await self.asaas.cancel_subscription(external_id)
        else:
            result = await self.stripe.cancel_subscription(external_id)
        
        # Atualizar status no banco
        subscription_data["status"] = "cancelled"
        supabase_admin.table('clients')\
            .update({"subscription": subscription_data})\
            .eq('id', str(client_id))\
            .execute()
        
        return {"status": "cancelled", "gateway": gateway}
    
    def get_plans(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Retorna planos disponíveis
        
        Args:
            category: Filtrar por categoria (b2c/b2b)
        
        Returns:
            Dicionário de planos
        """
        if category:
            return {k: v for k, v in PLANS.items() if v["category"] == category}
        return PLANS
