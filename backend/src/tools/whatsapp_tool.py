"""
WhatsApp Tool - LangChain Tool for Sending WhatsApp Messages
Sprint 04 - Sistema Multi-Agente

Tool that agents can use to send WhatsApp messages.
Uses the abstract WhatsAppProvider interface for flexibility.
"""

from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import asyncio

from ..providers.whatsapp.base import WhatsAppProvider, get_whatsapp_provider


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
    It uses the configured WhatsApp provider (Evolution, Twilio, etc).
    
    Example usage in agent:
        tools = [WhatsAppTool()]
        agent = create_agent(llm, tools)
        result = agent.invoke("Send a WhatsApp to +5511999999999 saying hello")
    """
    
    name: str = "send_whatsapp"
    description: str = """Send a WhatsApp text message to a phone number.
    
    Use this tool when you need to send a WhatsApp message to a user.
    
    Input should be:
    - phone: Phone number in international format (e.g., +5511999999999)
    - message: The text message to send
    
    Returns a dict with success status and message_id."""
    
    args_schema: type[BaseModel] = WhatsAppMessageInput
    
    provider: Optional[WhatsAppProvider] = None
    
    def __init__(self, provider: Optional[WhatsAppProvider] = None, **kwargs):
        """
        Initialize WhatsApp tool.
        
        Args:
            provider: WhatsApp provider instance (defaults to configured provider)
            **kwargs: Additional BaseTool arguments
        """
        super().__init__(**kwargs)
        self.provider = provider or get_whatsapp_provider()
    
    def _run(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Synchronous version (not recommended, use _arun instead).
        
        Args:
            phone: Phone number in international format
            message: Message content
        
        Returns:
            Dict with success status and message_id or error
        """
        return asyncio.run(self._arun(phone, message))
    
    async def _arun(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send WhatsApp message asynchronously.
        
        Args:
            phone: Phone number in international format
            message: Message content
        
        Returns:
            Dict with success status and message_id or error
        """
        try:
            # Validate phone format
            if not self.provider.validate_phone(phone):
                return {
                    "success": False,
                    "error": f"Invalid phone format: {phone}. Must be in international format (e.g., +5511999999999)"
                }
            
            # Send message via provider
            result = await self.provider.send_message(phone, message)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send WhatsApp message: {str(e)}"
            }


class WhatsAppMediaTool(BaseTool):
    """
    Tool for sending WhatsApp media (images, videos, documents).
    
    This tool allows agents to send media files via WhatsApp.
    
    Example usage in agent:
        tools = [WhatsAppMediaTool()]
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
    
    provider: Optional[WhatsAppProvider] = None
    
    def __init__(self, provider: Optional[WhatsAppProvider] = None, **kwargs):
        """
        Initialize WhatsApp media tool.
        
        Args:
            provider: WhatsApp provider instance (defaults to configured provider)
            **kwargs: Additional BaseTool arguments
        """
        super().__init__(**kwargs)
        self.provider = provider or get_whatsapp_provider()
    
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
            if not self.provider.validate_phone(phone):
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
            
            # Send media via provider
            result = await self.provider.send_media(
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
def get_whatsapp_tools(provider: Optional[WhatsAppProvider] = None) -> list[BaseTool]:
    """
    Get all WhatsApp tools.
    
    Args:
        provider: WhatsApp provider instance (optional)
    
    Returns:
        List of WhatsApp tools (message and media)
    
    Example:
        >>> tools = get_whatsapp_tools()
        >>> agent = create_agent(llm, tools)
    """
    return [
        WhatsAppTool(provider=provider),
        WhatsAppMediaTool(provider=provider)
    ]
