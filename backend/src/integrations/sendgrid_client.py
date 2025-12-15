"""
SendGrid Client - Sprint 07A
Client for SendGrid email API (alternative to SMTP)
"""

import httpx
from typing import List, Optional, Dict, Any
from ..utils.logger import logger


class SendGridClient:
    """
    Client for sending emails via SendGrid API.
    Alternative to SMTP for better deliverability and features.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize SendGrid client.
        
        Args:
            config: Configuration dict with keys:
                - api_key: SendGrid API key
                - from_email: From email address
                - from_name: From name (default: RENUM)
        """
        self.api_key = config['api_key']
        self.from_email = config['from_email']
        self.from_name = config.get('from_name', 'RENUM')
        self.api_url = "https://api.sendgrid.com/v3/mail/send"
        self.timeout = 30.0
        
        logger.info(f"[SendGrid] Client initialized for {self.from_email}")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        return bool(self.api_key and self.from_email)
    
    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        is_html: bool = True
    ) -> Dict[str, Any]:
        """
        Send email via SendGrid API.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (HTML or plain text)
            cc: Optional CC recipients
            is_html: Whether body is HTML (default: True)
        
        Returns:
            dict with success status and message_id
        """
        if not to or len(to) == 0:
            return {
                "success": False,
                "error": "At least one recipient is required"
            }
        
        logger.info(f"[SendGrid] Sending email to {', '.join(to)}")
        
        try:
            # Build personalizations
            personalizations = [{
                "to": [{"email": email} for email in to]
            }]
            
            if cc:
                personalizations[0]["cc"] = [{"email": email} for email in cc]
            
            # Build request payload
            payload = {
                "personalizations": personalizations,
                "from": {
                    "email": self.from_email,
                    "name": self.from_name
                },
                "subject": subject,
                "content": [{
                    "type": "text/html" if is_html else "text/plain",
                    "value": body
                }]
            }
            
            # Send request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                response.raise_for_status()
                
                # SendGrid returns 202 Accepted on success
                message_id = response.headers.get('X-Message-Id', 'unknown')
                
                logger.info(f"[SendGrid] Email sent successfully: {message_id}")
                
                return {
                    "success": True,
                    "message_id": message_id,
                    "recipients": to
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"[SendGrid] HTTP error: {e.response.status_code} - {e.response.text}")
            
            error_msg = "Unknown error"
            try:
                error_data = e.response.json()
                if 'errors' in error_data:
                    error_msg = '; '.join([err.get('message', '') for err in error_data['errors']])
            except:
                error_msg = e.response.text
            
            return {
                "success": False,
                "error": f"SendGrid API error: {error_msg}"
            }
        except Exception as e:
            logger.error(f"[SendGrid] Error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test SendGrid API connection.
        
        Returns:
            dict with success status and message
        """
        import time
        start_time = time.time()
        
        try:
            # SendGrid doesn't have a dedicated test endpoint
            # We'll validate the API key by checking if it's properly formatted
            if not self.api_key.startswith('SG.'):
                return {
                    "success": False,
                    "message": "Invalid API key format - should start with 'SG.'",
                    "latency_ms": 0
                }
            
            # Try to get account details (validates API key)
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    "https://api.sendgrid.com/v3/user/profile",
                    headers={
                        "Authorization": f"Bearer {self.api_key}"
                    }
                )
                
                response.raise_for_status()
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"[SendGrid] Connection test successful ({latency_ms}ms)")
            
            return {
                "success": True,
                "message": "Connection successful",
                "latency_ms": latency_ms
            }
            
        except httpx.HTTPStatusError as e:
            latency_ms = int((time.time() - start_time) * 1000)
            
            if e.response.status_code == 401:
                return {
                    "success": False,
                    "message": "Authentication failed - invalid API key",
                    "latency_ms": latency_ms
                }
            else:
                return {
                    "success": False,
                    "message": f"API error: {e.response.status_code}",
                    "latency_ms": latency_ms
                }
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "latency_ms": latency_ms
            }
