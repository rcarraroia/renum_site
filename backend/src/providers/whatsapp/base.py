"""
WhatsApp Provider - Abstract Base Class
Sprint 04 - Sistema Multi-Agente

Abstract interface for WhatsApp API providers.
Allows easy switching between different WhatsApp APIs (Evolution, Twilio, etc)
without changing agent code.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class WhatsAppMessage(BaseModel):
    """Standardized WhatsApp message model"""
    
    phone: str = Field(..., description="Phone number in international format (+5511999999999)")
    content: str = Field(..., description="Message content")
    message_id: Optional[str] = Field(None, description="Provider's message ID")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")
    status: Optional[str] = Field(None, description="Message status: sent, delivered, read, failed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+5511999999999",
                "content": "Hello! This is a test message.",
                "message_id": "msg_123456",
                "timestamp": "2025-11-29T10:30:00Z",
                "status": "sent"
            }
        }


class WhatsAppProvider(ABC):
    """
    Abstract base class for WhatsApp providers.
    
    All WhatsApp provider implementations must inherit from this class
    and implement all abstract methods.
    
    This allows the system to easily switch between different WhatsApp APIs
    (Evolution, Twilio, WhatsApp Business API, etc) by only changing
    environment variables, without modifying agent code.
    """
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize WhatsApp provider.
        
        Args:
            api_url: API endpoint URL
            api_key: API authentication key
        """
        self.api_url = api_url
        self.api_key = api_key
        self._validate_config()
    
    def _validate_config(self) -> None:
        """
        Validate provider configuration.
        
        Raises:
            ValueError: If required configuration is missing
        """
        if not self.api_url:
            raise ValueError(
                f"{self.__class__.__name__} requires api_url to be configured.\n"
                f"Set WHATSAPP_API_URL in your .env file."
            )
        
        if not self.api_key:
            raise ValueError(
                f"{self.__class__.__name__} requires api_key to be configured.\n"
                f"Set WHATSAPP_API_KEY in your .env file."
            )
    
    @abstractmethod
    async def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Send a text message via WhatsApp.
        
        Args:
            phone: Phone number in international format (+5511999999999)
            message: Message content to send
        
        Returns:
            Dict with:
                - success (bool): Whether message was sent successfully
                - message_id (str): Provider's message ID
                - error (str, optional): Error message if failed
        
        Example:
            >>> result = await provider.send_message("+5511999999999", "Hello!")
            >>> print(result)
            {"success": True, "message_id": "msg_123456"}
        """
        pass
    
    @abstractmethod
    async def send_media(
        self,
        phone: str,
        media_url: str,
        caption: str = "",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """
        Send media (image, video, document) via WhatsApp.
        
        Args:
            phone: Phone number in international format
            media_url: URL of the media file to send
            caption: Optional caption for the media
            media_type: Type of media: image, video, document, audio
        
        Returns:
            Dict with:
                - success (bool): Whether media was sent successfully
                - message_id (str): Provider's message ID
                - error (str, optional): Error message if failed
        
        Example:
            >>> result = await provider.send_media(
            ...     "+5511999999999",
            ...     "https://example.com/image.jpg",
            ...     caption="Check this out!",
            ...     media_type="image"
            ... )
            >>> print(result)
            {"success": True, "message_id": "msg_123457"}
        """
        pass
    
    @abstractmethod
    async def handle_webhook(self, payload: Dict[str, Any]) -> WhatsAppMessage:
        """
        Parse webhook payload from provider and return standardized message.
        
        Each provider has a different webhook payload format.
        This method normalizes the payload into a standard WhatsAppMessage.
        
        Args:
            payload: Raw webhook payload from the provider
        
        Returns:
            WhatsAppMessage: Standardized message object
        
        Raises:
            ValueError: If payload is invalid or cannot be parsed
        
        Example:
            >>> payload = {"from": "+5511999999999", "body": "Hello", ...}
            >>> message = await provider.handle_webhook(payload)
            >>> print(message.phone, message.content)
            +5511999999999 Hello
        """
        pass
    
    @abstractmethod
    async def get_message_status(self, message_id: str) -> str:
        """
        Get delivery status of a sent message.
        
        Args:
            message_id: Provider's message ID
        
        Returns:
            Status string: 'sent', 'delivered', 'read', 'failed'
        
        Example:
            >>> status = await provider.get_message_status("msg_123456")
            >>> print(status)
            delivered
        """
        pass
    
    def validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
        
        Returns:
            True if valid, False otherwise
        
        Example:
            >>> provider.validate_phone("+5511999999999")
            True
            >>> provider.validate_phone("11999999999")
            False
        """
        import re
        # Phone must start with + and contain 10-15 digits
        pattern = r'^\+\d{10,15}$'
        return bool(re.match(pattern, phone.strip()))


class NoneWhatsAppProvider(WhatsAppProvider):
    """
    Dummy WhatsApp provider for when no provider is configured.
    
    This provider does nothing and always returns success.
    Useful for development/testing without a real WhatsApp API.
    """
    
    def __init__(self):
        """Initialize without requiring API credentials"""
        self.api_url = "none"
        self.api_key = "none"
        # Skip validation
    
    def _validate_config(self) -> None:
        """Skip validation for dummy provider"""
        pass
    
    async def send_message(self, phone: str, message: str) -> Dict[str, Any]:
        """Simulate sending message"""
        print(f"📱 [MOCK] WhatsApp to {phone}: {message}")
        return {
            "success": True,
            "message_id": f"mock_{datetime.now().timestamp()}",
            "note": "Using NoneWhatsAppProvider - no real message sent"
        }
    
    async def send_media(
        self,
        phone: str,
        media_url: str,
        caption: str = "",
        media_type: str = "image"
    ) -> Dict[str, Any]:
        """Simulate sending media"""
        print(f"📱 [MOCK] WhatsApp media to {phone}: {media_type} - {media_url}")
        if caption:
            print(f"   Caption: {caption}")
        return {
            "success": True,
            "message_id": f"mock_{datetime.now().timestamp()}",
            "note": "Using NoneWhatsAppProvider - no real media sent"
        }
    
    async def handle_webhook(self, payload: Dict[str, Any]) -> WhatsAppMessage:
        """Parse mock webhook"""
        return WhatsAppMessage(
            phone=payload.get("phone", "+5511999999999"),
            content=payload.get("message", ""),
            message_id=f"mock_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            status="received"
        )
    
    async def get_message_status(self, message_id: str) -> str:
        """Return mock status"""
        return "delivered"


def get_whatsapp_provider() -> WhatsAppProvider:
    """
    Factory function to get the configured WhatsApp provider.
    
    Returns:
        WhatsAppProvider: Configured provider instance
    
    Example:
        >>> provider = get_whatsapp_provider()
        >>> await provider.send_message("+5511999999999", "Hello!")
    """
    from ...config.settings import settings
    
    provider_name = settings.WHATSAPP_PROVIDER.lower()
    
    if provider_name == "none" or not provider_name:
        return NoneWhatsAppProvider()
    
    # Future providers can be added here:
    # elif provider_name == "evolution":
    #     from .evolution import EvolutionWhatsAppProvider
    #     return EvolutionWhatsAppProvider(settings.WHATSAPP_API_URL, settings.WHATSAPP_API_KEY)
    # elif provider_name == "twilio":
    #     from .twilio import TwilioWhatsAppProvider
    #     return TwilioWhatsAppProvider(settings.WHATSAPP_API_URL, settings.WHATSAPP_API_KEY)
    
    else:
        raise ValueError(
            f"Unknown WhatsApp provider: {provider_name}\n"
            f"Supported providers: none, evolution, twilio\n"
            f"Set WHATSAPP_PROVIDER in your .env file."
        )
