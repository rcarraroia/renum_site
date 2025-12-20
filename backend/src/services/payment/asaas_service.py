"""
Asaas Payment Service
Integração com gateway Asaas (Brasil)
"""
import httpx
from typing import Dict, Any, Optional
from uuid import UUID

from src.config.settings import settings


class AsaasService:
    """Serviço de integração com Asaas"""
    
    def __init__(self):
        self.api_key = settings.ASAAS_API_KEY
        self.base_url = settings.ASAAS_BASE_URL or "https://www.asaas.com/api/v3"
        self.headers = {
            "access_token": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def create_customer(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria cliente no Asaas
        
        Args:
            client_data: Dados do cliente (company_name, email, document)
        
        Returns:
            Dados do cliente criado no Asaas
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/customers",
                headers=self.headers,
                json={
                    "name": client_data.get("company_name"),
                    "email": client_data.get("email"),
                    "cpfCnpj": client_data.get("document"),
                    "phone": client_data.get("phone"),
                    "mobilePhone": client_data.get("mobile_phone"),
                    "address": client_data.get("address", ""),
                    "addressNumber": client_data.get("address_number", ""),
                    "complement": client_data.get("complement"),
                    "province": client_data.get("province", ""),
                    "postalCode": client_data.get("postal_code")
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def create_subscription(
        self, 
        customer_id: str, 
        plan_value: float,
        billing_type: str = "CREDIT_CARD",
        cycle: str = "MONTHLY"
    ) -> Dict[str, Any]:
        """
        Cria assinatura recorrente no Asaas
        
        Args:
            customer_id: ID do cliente no Asaas
            plan_value: Valor do plano
            billing_type: Tipo de cobrança (CREDIT_CARD, BOLETO, PIX)
            cycle: Ciclo de cobrança (MONTHLY, YEARLY)
        
        Returns:
            Dados da assinatura criada
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/subscriptions",
                headers=self.headers,
                json={
                    "customer": customer_id,
                    "billingType": billing_type,
                    "value": plan_value,
                    "cycle": cycle,
                    "description": "Assinatura RENUM - Template de Agente"
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Cancela assinatura no Asaas
        
        Args:
            subscription_id: ID da assinatura
        
        Returns:
            Dados da assinatura cancelada
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/subscriptions/{subscription_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Busca dados de uma assinatura
        
        Args:
            subscription_id: ID da assinatura
        
        Returns:
            Dados da assinatura
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/subscriptions/{subscription_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_payment_link(
        self,
        customer_id: str,
        value: float,
        description: str
    ) -> Dict[str, Any]:
        """
        Cria link de pagamento único
        
        Args:
            customer_id: ID do cliente
            value: Valor
            description: Descrição
        
        Returns:
            Link de pagamento
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/payments",
                headers=self.headers,
                json={
                    "customer": customer_id,
                    "billingType": "UNDEFINED",  # Cliente escolhe
                    "value": value,
                    "dueDate": None,  # Pagamento imediato
                    "description": description
                }
            )
            response.raise_for_status()
            return response.json()
