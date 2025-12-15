"""
WhatsApp Tool - LangChain Tool for Sending WhatsApp Messages
Sprint 07A - Integrações Core (Updated)

Tool that agents can use to send WhatsApp messages.
Uses UazapiClient and Celery for async message sending.
"""

from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import asyncio
from uuid import UUID

from ..integrations.uazapi_client import UazapiClient
from ..services.integration_service import IntegrationService


class WhatsAppMessageInput(BaseModel):
    """Input schema for WhatsApp message tool"""
    
    phone: str = Field(
        ...,
        description="Phone number in international format with country code (e.g., +5511999999999)"
    )
    message: str = Field(
        ...,
        description="Message content to send"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+5511999999999",
                "message": "Hello! This is a message from RENUM."
            }
        }


class WhatsAppMediaInput(BaseModel):
    """Input schema for WhatsApp media tool"""
    
    phone: str = Field(
        ...,
        description="Phone number in international format"
    )
    media_url: str = Field(
        ...,
        description="URL of the media file to send"
    )
    caption: str = Field(
        default="",
        description="Optional caption for the media"
    )
    media_type: str = Field(
        default="image",
        description="Type of media: image, video, document, audio"
    )


class WhatsAppTool(BaseTool):
    """
    Tool for sending WhatsApp text messages.
    
    This tool allows agents to send WhatsApp messages to phone numbers.
    Uses UazapiClient and Celery for async message sending.
    
    Example usage in agent:
        tools = [WhatsAppTool(client_id="uuid")]
        agent = create_agent(llm, tools)
        result = agent.invoke("Send a WhatsApp to +5511999999999 saying hello")
    """
    
    name: str = "send_whatsapp"
    description: str = """Send a WhatsApp text message to a phone number.
    
    Use this tool when you need to send a WhatsApp message to a user.
    
    Input should be:
    - phone: Phone number in international format (e.g., +5511999999999)
    - message: The text message to send
    
    Returns a dict with success status and task_id."""
    
    args_schema: type[BaseModel] = WhatsAppMessageInput
    
    client_id: Optional[UUID] = None
    
    def __init__(self, client_id: Optional[UUID] = None, **kwargs):
        """
        Initialize WhatsApp tool.
        
        Args:
            client_id: Client ID for loading integration config
            **kwargs: Additional BaseTool arguments
        """
        super().__init__(**kwargs)
        self.client_id = client_id
    
    def _run(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Synchronous version (not recommended, use _arun instead).
        
        Args:
            phone: Phone number in international format
            message: Message content
        
        Returns:
            Dict with success status and task_id or error
        """
        return asyncio.run(self._arun(phone, message))
    
    async def _arun(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send WhatsApp message asynchronously via Celery.
        
        Args:
            phone: Phone number in international format
            message: Message content
        
        Returns:
            Dict with success status and task_id or error
        """
        try:
            # Validate phone format (basic check)
            if not phone.startswith("+"):
                return {
                    "success": False,
                    "error": f"Invalid phone format: {phone}. Must start with + and country code"
                }
            
            # Load integration config
            if not self.client_id:
                return {
                    "success": False,
                    "error": "client_id is required to send WhatsApp messages"
                }
            
            integration_service = IntegrationService()
            integration = await integration_service.get_integration(self.client_id, "whatsapp")
            
            if not integration:
                return {
                    "success": False,
                    "error": "WhatsApp integration not configured for this client"
                }
            
            if integration.status != "active":
                return {
                    "success": False,
                    "error": f"WhatsApp integration is {integration.status}, not active"
                }
            
            # Enqueue Celery task for async sending
            from ..workers.message_tasks import send_whatsapp_message_task
            
            task = send_whatsapp_message_task.delay(
                client_id=str(self.client_id),
                phone=phone,
                message=message
            )
            
            return {
                "success": True,
                "task_id": task.id,
                "phone": phone,
                "status": "queued"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send WhatsApp message: {str(e)}"
            }


class WhatsAppMediaTool(BaseTool):
    """
    Tool for sending WhatsApp media (images, videos, documents).
    
    This tool allows agents to send media files via WhatsApp.
    Uses UazapiClient for media sending.
    
    Example usage in agent:
        tools = [WhatsAppMediaTool(client_id="uuid")]
        agent = create_agent(llm, tools)
        result = agent.invoke("Send an image to +5511999999999")
    """
    
    name: str = "send_whatsapp_media"
    description: str = """Send media (image, video, document) via WhatsApp.
    
    Use this tool when you need to send a media file to a user via WhatsApp.
    
    Input should be:
    - phone: Phone number in international format
    - media_url: URL of the media file
    - caption: Optional caption for the media
    - media_type: Type of media (image, video, document, audio)
    
    Returns a dict with success status and message_id."""
    
    args_schema: type[BaseModel] = WhatsAppMediaInput
    
    client_id: Optional[UUID] = None
    
    def __init__(self, client_id: Optional[UUID] = None, **kwargs):
        """
        Initialize WhatsApp media tool.
        
        Args:
            client_id: Client ID for loading integration config
            **kwargs: Additional BaseTool arguments
        """
        super().__init__(**kwargs)
        self.client_id = client_id
    
    def _run(
        self,
        phone: str,
        media_url: str,
        caption: str = "",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """Synchronous version"""
        return asyncio.run(self._arun(phone, media_url, caption, media_type))
    
    async def _arun(
        self,
        phone: str,
        media_url: str,
        caption: str = "",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Send WhatsApp media asynchronously.
        
        Args:
            phone: Phone number in international format
            media_url: URL of the media file
            caption: Optional caption
            media_type: Type of media
        
        Returns:
            Dict with success status and message_id or error
        """
        try:
            # Validate phone format
            if not phone.startswith("+"):
                return {
                    "success": False,
                    "error": f"Invalid phone format: {phone}"
                }
            
            # Validate media type
            valid_types = ["image", "video", "document", "audio"]
            if media_type not in valid_types:
                return {
                    "success": False,
                    "error": f"Invalid media_type: {media_type}. Must be one of: {', '.join(valid_types)}"
                }
            
            # Load integration config
            if not self.client_id:
                return {
                    "success": False,
                    "error": "client_id is required to send WhatsApp media"
                }
            
            integration_service = IntegrationService()
            integration = await integration_service.get_integration(self.client_id, "whatsapp")
            
            if not integration:
                return {
                    "success": False,
                    "error": "WhatsApp integration not configured for this client"
                }
            
            # Get decrypted config
            config = await integration_service.decrypt_credentials(integration.config)
            
            # Create UazapiClient with context manager (auto-closes connection)
            async with UazapiClient(
                api_url=config.get("api_url"),
                api_token=config.get("api_token"),
                phone_number=config.get("phone_number")
            ) as client:
                # Send media
                result = await client.send_media(
                    phone=phone,
                    media_url=media_url,
                    caption=caption,
                    media_type=media_type
                )
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send WhatsApp media: {str(e)}"
            }


# Convenience function to get both tools
def get_whatsapp_tools(client_id: Optional[UUID] = None) -> list[BaseTool]:
    """
    Get all WhatsApp tools.
    
    Args:
        client_id: Client ID for loading integration config
    
    Returns:
        List of WhatsApp tools (message and media)
    
    Example:
        >>> tools = get_whatsapp_tools(client_id="uuid")
        >>> agent = create_agent(llm, tools)
    """
    return [
        WhatsAppTool(client_id=client_id),
        WhatsAppMediaTool(client_id=client_id)
    ]
