"""
Webhooks API Routes
Sprint 07A - Integrações Core

Webhook endpoints for receiving external events (WhatsApp, etc).
"""

from fastapi import APIRouter, Request, HTTPException, status, Header
from typing import Optional
import logging

from ...integrations.uazapi_client import UazapiClient
from ...services.integration_service import IntegrationService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


@router.post("/uazapi")
async def uazapi_webhook(
    request: Request,
    x_signature: Optional[str] = Header(None)
):
    """
    Webhook endpoint for Uazapi (WhatsApp) messages.
    
    Receives incoming WhatsApp messages and routes them to the Discovery Agent.
    
    Expected payload format (will be defined in API_UAZAPI.md):
    {
        "from": "+5511999999999",
        "message": "Hello!",
        "timestamp": "2025-12-04T10:00:00Z",
        "message_id": "msg_123",
        "media_url": null,  // optional
        "media_type": null  // optional
    }
    
    Headers:
    - X-Signature: Webhook signature for validation (if configured)
    """
    try:
        # Get raw body
        body = await request.body()
        
        # Parse JSON
        payload = await request.json()
        
        logger.info(f"Received Uazapi webhook: {payload}")
        
        # TODO: Validate webhook signature
        # This requires the webhook_secret from integration config
        # For now, we'll skip validation (to be implemented when API docs are available)
        
        # Extract message data
        from_phone = payload.get("from")
        message = payload.get("message")
        timestamp = payload.get("timestamp")
        message_id = payload.get("message_id")
        media_url = payload.get("media_url")
        media_type = payload.get("media_type")
        
        if not from_phone or not message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: from, message"
            )
        
        # TODO: Route to Discovery Agent for processing
        # This would involve:
        # 1. Identify which client this message belongs to (based on phone number or instance)
        # 2. Load the appropriate agent configuration
        # 3. Process the message through LangGraph
        # 4. Generate response
        # 5. Send response back via WhatsApp
        
        # For now, log the message
        logger.info(f"WhatsApp message from {from_phone}: {message}")
        
        # Return success response
        return {
            "success": True,
            "message_id": message_id,
            "status": "received"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Uazapi webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )


@router.get("/uazapi/health")
async def uazapi_webhook_health():
    """
    Health check endpoint for Uazapi webhook.
    
    Some webhook providers require a GET endpoint to verify the webhook URL.
    """
    return {
        "status": "ok",
        "webhook": "uazapi",
        "version": "1.0"
    }
