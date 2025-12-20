from typing import Optional, Dict, Any, List
import stripe
from fastapi import HTTPException
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class StripeService:
    @staticmethod
    async def create_checkout_session(
        price_id: str,
        customer_email: Optional[str] = None,
        client_reference_id: Optional[str] = None,
        success_url: str = None,
        cancel_url: str = None,
        mode: str = 'subscription'
    ) -> Dict[str, Any]:
        try:
            session_params = {
                "payment_method_types": ["card"],
                "line_items": [{
                    "price": price_id,
                    "quantity": 1,
                }],
                "mode": mode,
                "success_url": success_url,
                "cancel_url": cancel_url,
            }

            if customer_email:
                session_params["customer_email"] = customer_email
            
            if client_reference_id:
                session_params["client_reference_id"] = client_reference_id

            session = stripe.checkout.Session.create(**session_params)
            return {"url": session.url, "id": session.id}

        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @staticmethod
    async def get_subscription(subscription_id: str) -> Dict[str, Any]:
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_customer_portal_url(customer_id: str, return_url: str) -> str:
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            return session.url
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def list_prices(limit: int = 10) -> List[Dict[str, Any]]:
        try:
            prices = stripe.Price.list(limit=limit, active=True, expand=['data.product'])
            return prices.data
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))
