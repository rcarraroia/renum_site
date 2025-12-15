"""
Message Tasks - Sprint 07A
Celery tasks for sending WhatsApp and Email messages
"""

from celery import Task
from typing import List, Optional
import time
from uuid import UUID

from .celery_app import celery_app
from ..utils.logger import logger


class CallbackTask(Task):
    """
    Base task with automatic retry on failure.
    Implements exponential backoff: 1s, 5s, 25s
    """
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes max
    retry_jitter = True


@celery_app.task(base=CallbackTask, bind=True, name='src.workers.message_tasks.send_whatsapp_message_task')
async def send_whatsapp_message_task(self, client_id: str, phone: str, message: str) -> dict:
    """
    Send WhatsApp message via Uazapi.
    
    Args:
        client_id: Client UUID
        phone: Phone number in international format
        message: Message content
    
    Returns:
        dict with success status and message_id
    """
    start_time = time.time()
    
    try:
        logger.info(
            f"[Celery] Sending WhatsApp message",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "phone": phone,
                "message_length": len(message)
            }
        )
        
        # Import here to avoid circular imports
        from ..services.integration_service import IntegrationService
        from ..integrations.uazapi_client import UazapiClient
        
        # Load integration config
        integration_service = IntegrationService()
        integration = integration_service.get_integration(client_id, 'whatsapp')
        
        if not integration:
            raise ValueError(f"WhatsApp integration not configured for client {client_id}")
        
        if integration['status'] != 'connected':
            raise ValueError(f"WhatsApp integration is {integration['status']}, not connected")
        
        # Decrypt config
        config = integration_service.decrypt_credentials(integration['config'])
        
        # Create Uazapi client with context manager (auto-closes connection)
        async with UazapiClient(
            api_url=config['api_url'],
            api_token=config['api_token'],
            phone_number=config['phone_number']
        ) as uazapi:
            # Send message
            result = await uazapi.send_message(phone, message)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"[Celery] WhatsApp message sent successfully",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "phone": phone,
                "message_id": result.get('message_id'),
                "execution_time_ms": execution_time
            }
        )
        
        return {
            "success": True,
            "message_id": result.get('message_id'),
            "execution_time_ms": execution_time
        }
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        
        logger.error(
            f"[Celery] Failed to send WhatsApp message: {str(e)}",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "phone": phone,
                "error": str(e),
                "execution_time_ms": execution_time
            }
        )
        
        # Re-raise to trigger retry
        raise


@celery_app.task(base=CallbackTask, bind=True, name='src.workers.message_tasks.send_email_task')
async def send_email_task(
    self,
    client_id: str,
    to: List[str],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None
) -> dict:
    """
    Send email via SMTP or SendGrid.
    
    Args:
        client_id: Client UUID
        to: List of recipient email addresses
        subject: Email subject
        body: Email body (HTML or plain text)
        cc: Optional CC recipients
    
    Returns:
        dict with success status and message_id
    """
    start_time = time.time()
    
    try:
        logger.info(
            f"[Celery] Sending email",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "to": to,
                "subject": subject
            }
        )
        
        # Import here to avoid circular imports
        from ..services.integration_service import IntegrationService
        from ..integrations.smtp_client import SMTPClient
        from ..integrations.sendgrid_client import SendGridClient
        
        # Load integration config
        integration_service = IntegrationService()
        
        # Try SMTP first, then SendGrid
        integration = integration_service.get_integration(client_id, 'email_smtp')
        if not integration:
            integration = integration_service.get_integration(client_id, 'email_sendgrid')
        
        if not integration:
            raise ValueError(f"Email integration not configured for client {client_id}")
        
        if integration['status'] != 'connected':
            raise ValueError(f"Email integration is {integration['status']}, not connected")
        
        # Decrypt config
        config = integration_service.decrypt_credentials(integration['config'])
        
        # Send email based on provider
        if integration['type'] == 'email_smtp':
            client = SMTPClient(
                host=config['host'],
                port=config['port'],
                username=config['username'],
                password=config['password'],
                use_tls=config.get('use_tls', True),
                from_email=config['from_email']
            )
        else:  # email_sendgrid
            client = SendGridClient(
                api_key=config['api_key'],
                from_email=config['from_email'],
                from_name=config.get('from_name', 'RENUM')
            )
        
        result = client.send_email(to, subject, body, cc)
        
        execution_time = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"[Celery] Email sent successfully",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "to": to,
                "message_id": result.get('message_id'),
                "execution_time_ms": execution_time
            }
        )
        
        return {
            "success": True,
            "message_id": result.get('message_id'),
            "execution_time_ms": execution_time
        }
        
    except Exception as e:
        execution_time = int((time.time() - start_time) * 1000)
        
        logger.error(
            f"[Celery] Failed to send email: {str(e)}",
            extra={
                "task_id": self.request.id,
                "client_id": client_id,
                "to": to,
                "error": str(e),
                "execution_time_ms": execution_time
            }
        )
        
        # Re-raise to trigger retry
        raise


# Aliases for backward compatibility
send_whatsapp_message = send_whatsapp_message_task
send_email = send_email_task
