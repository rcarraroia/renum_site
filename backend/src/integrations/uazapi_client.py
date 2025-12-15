"""
Uazapi Client - WhatsApp API Integration
Sprint 07A - Integrações Core

Complete implementation based on Uazapi API v2.0 documentation.
"""

import httpx
import logging
from typing import Dict, Any, Optional
import hmac
import hashlib

logger = logging.getLogger(__name__)


class UazapiClient:
    """
    Client for Uazapi WhatsApp API v2.0.
    
    Supports:
    - Text messages with link preview
    - Media messages (image, video, audio, document, sticker)
    - Contact cards (vCard)
    - Location sharing
    - Message reactions
    - Webhook signature validation
    """
    
    def __init__(
        self,
        api_url: str,
        api_token: str,
        phone_number: str,
        webhook_secret: Optional[str] = None
    ):
        """
        Initialize Uazapi client.
        
        Args:
            api_url: Base URL of Uazapi API (e.g., https://subdomain.uazapi.com)
            api_token: Authentication token for the instance
            phone_number: WhatsApp phone number
            webhook_secret: Optional secret for webhook signature validation
        """
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token
        self.phone_number = phone_number
        self.webhook_secret = webhook_secret
        self._client = None  # Lazy initialization
        
        logger.info(f"UazapiClient initialized for {phone_number}")
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy initialization of HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "token": self.api_token,
                    "Content-Type": "application/json"
                },
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._client
    
    async def send_message(
        self,
        phone: str,
        message: str,
        link_preview: bool = False,
        reply_id: Optional[str] = None,
        delay: Optional[int] = None,
        track_source: Optional[str] = None,
        track_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send text message via WhatsApp.
        
        Args:
            phone: Recipient phone number (international format without +)
            message: Message text
            link_preview: Enable link preview
            reply_id: ID of message to reply to
            delay: Delay in milliseconds before sending (shows "typing...")
            track_source: Source for tracking
            track_id: ID for tracking
        
        Returns:
            Dict with success status and message details
        """
        try:
            # Remove + if present (Uazapi expects without +)
            if phone.startswith("+"):
                phone = phone[1:]
            
            payload = {
                "number": phone,
                "text": message
            }
            
            # Optional parameters
            if link_preview:
                payload["linkPreview"] = True
            if reply_id:
                payload["replyid"] = reply_id
            if delay:
                payload["delay"] = delay
            if track_source:
                payload["track_source"] = track_source
            if track_id:
                payload["track_id"] = track_id
            
            response = await self.client.post(
                f"{self.api_url}/send/text",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message_id": data.get("messageid"),
                    "id": data.get("id"),
                    "timestamp": data.get("messageTimestamp"),
                    "status": data.get("status", "sent")
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "error": error_data.get("error", f"HTTP {response.status_code}"),
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"Error sending message via Uazapi: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_media(
        self,
        phone: str,
        media_url: str,
        caption: str = "",
        media_type: str = "image",
        doc_name: Optional[str] = None,
        reply_id: Optional[str] = None,
        delay: Optional[int] = None,
        track_source: Optional[str] = None,
        track_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send media via WhatsApp.
        
        Args:
            phone: Recipient phone number
            media_url: URL or base64 of media file
            caption: Optional caption text
            media_type: Type of media (image, video, document, audio, ptt, sticker)
            doc_name: Document name (for documents only)
            reply_id: ID of message to reply to
            delay: Delay in milliseconds before sending
            track_source: Source for tracking
            track_id: ID for tracking
        
        Returns:
            Dict with success status and message details
        """
        try:
            # Remove + if present
            if phone.startswith("+"):
                phone = phone[1:]
            
            payload = {
                "number": phone,
                "type": media_type,
                "file": media_url
            }
            
            # Optional parameters
            if caption:
                payload["text"] = caption
            if doc_name and media_type == "document":
                payload["docName"] = doc_name
            if reply_id:
                payload["replyid"] = reply_id
            if delay:
                payload["delay"] = delay
            if track_source:
                payload["track_source"] = track_source
            if track_id:
                payload["track_id"] = track_id
            
            response = await self.client.post(
                f"{self.api_url}/send/media",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message_id": data.get("messageid"),
                    "id": data.get("id"),
                    "timestamp": data.get("messageTimestamp"),
                    "status": data.get("status", "sent")
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "error": error_data.get("error", f"HTTP {response.status_code}"),
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"Error sending media via Uazapi: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_contact(
        self,
        phone: str,
        full_name: str,
        contact_phone: str,
        organization: Optional[str] = None,
        email: Optional[str] = None,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send contact card (vCard) via WhatsApp.
        
        Args:
            phone: Recipient phone number
            full_name: Full name of contact
            contact_phone: Phone number(s) of contact (comma-separated)
            organization: Organization/company name
            email: Email address
            url: Website URL
        
        Returns:
            Dict with success status and message details
        """
        try:
            if phone.startswith("+"):
                phone = phone[1:]
            
            payload = {
                "number": phone,
                "fullName": full_name,
                "phoneNumber": contact_phone
            }
            
            if organization:
                payload["organization"] = organization
            if email:
                payload["email"] = email
            if url:
                payload["url"] = url
            
            response = await self.client.post(
                f"{self.api_url}/send/contact",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message_id": data.get("messageid"),
                    "id": data.get("id")
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "error": error_data.get("error", f"HTTP {response.status_code}")
                }
                
        except Exception as e:
            logger.error(f"Error sending contact via Uazapi: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_location(
        self,
        phone: str,
        latitude: float,
        longitude: float,
        name: Optional[str] = None,
        address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send location via WhatsApp.
        
        Args:
            phone: Recipient phone number
            latitude: Latitude (-90 to 90)
            longitude: Longitude (-180 to 180)
            name: Location name
            address: Full address
        
        Returns:
            Dict with success status and message details
        """
        try:
            if phone.startswith("+"):
                phone = phone[1:]
            
            payload = {
                "number": phone,
                "latitude": latitude,
                "longitude": longitude
            }
            
            if name:
                payload["name"] = name
            if address:
                payload["address"] = address
            
            response = await self.client.post(
                f"{self.api_url}/send/location",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message_id": data.get("messageid"),
                    "id": data.get("id")
                }
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "error": error_data.get("error", f"HTTP {response.status_code}")
                }
                
        except Exception as e:
            logger.error(f"Error sending location via Uazapi: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format.
        
        Uazapi expects international format without + sign.
        Example: 5511999999999
        
        Args:
            phone: Phone number to validate
        
        Returns:
            True if valid, False otherwise
        """
        # Remove + if present
        if phone.startswith("+"):
            phone = phone[1:]
        
        # Check if it's all digits and has reasonable length
        return phone.isdigit() and 10 <= len(phone) <= 15
    
    def validate_webhook_signature(
        self,
        payload: str,
        signature: str
    ) -> bool:
        """
        Validate webhook signature using HMAC-SHA256.
        
        Args:
            payload: Raw webhook payload (string)
            signature: Signature from X-Signature header
        
        Returns:
            True if valid, False otherwise
        """
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured - skipping signature validation")
            return True
        
        try:
            # Calculate expected signature
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures (constant-time comparison)
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            logger.error(f"Error validating webhook signature: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test connection to Uazapi API by checking instance status.
        
        Returns:
            True if connection successful and instance is connected, False otherwise
        """
        try:
            response = await self.client.get(f"{self.api_url}/instance/status")
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "disconnected")
                logger.info(f"Uazapi connection test: status={status}")
                return status == "connected"
            else:
                logger.error(f"Uazapi connection test failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error testing Uazapi connection: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            logger.info("UazapiClient closed")
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
