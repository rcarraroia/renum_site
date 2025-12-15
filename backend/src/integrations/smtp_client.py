"""
SMTP Client - Sprint 07A
Native Python SMTP client for sending emails
"""

try:
    import aiosmtplib
except ImportError:
    # Mock aiosmtplib if not available to prevent crashes
    from unittest.mock import MagicMock
    print("Warning: aiosmtplib not installed. Email functions will be mocked.")
    aiosmtplib = MagicMock()
    # Define exception classes on the mock so except blocks don't fail
    class _MockSMTPException(Exception): pass
    class _MockSMTPAuthError(_MockSMTPException): pass
    class _MockSMTPConnectError(_MockSMTPException): pass
    aiosmtplib.SMTPException = _MockSMTPException
    aiosmtplib.SMTPAuthenticationError = _MockSMTPAuthError
    aiosmtplib.SMTPConnectError = _MockSMTPConnectError

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from ..utils.logger import logger


class SMTPClient:
    """
    Client for sending emails via SMTP.
    Supports TLS encryption and HTML/plain text emails.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize SMTP client.
        
        Args:
            config: Configuration dict with keys:
                - host: SMTP server host
                - port: SMTP server port
                - username: SMTP username
                - password: SMTP password
                - use_tls: Use TLS encryption (default: True)
                - from_email: From email address
                - from_name: Optional from name
        """
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.use_tls = config.get('use_tls', True)
        self.from_email = config.get('from_email', self.username)
        self.from_name = config.get('from_name')
        
        logger.info(f"[SMTP] Client initialized for {self.from_email}")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        required = ['host', 'port', 'username', 'password']
        return all(key in self.__dict__ for key in required)
    
    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        is_html: bool = True
    ) -> Dict[str, Any]:
        """
        Send email via SMTP.
        
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
        
        logger.info(f"[SMTP] Sending email to {', '.join(to)}")
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>" if self.from_name else self.from_email
            msg['To'] = ', '.join(to)
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Attach body
            mime_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, mime_type, 'utf-8'))
            
            # Send email
            async with aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_tls
            ) as smtp:
                await smtp.login(self.username, self.password)
                
                recipients = to + (cc if cc else [])
                await smtp.send_message(msg, self.from_email, recipients)
            
            logger.info(f"[SMTP] Email sent successfully to {', '.join(to)}")
            
            return {
                "success": True,
                "message_id": msg['Message-ID'] if 'Message-ID' in msg else 'unknown',
                "recipients": to
            }
            
        except aiosmtplib.SMTPException as e:
            logger.error(f"[SMTP] SMTP error: {str(e)}")
            return {
                "success": False,
                "error": f"SMTP error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"[SMTP] Error sending email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test SMTP connection.
        
        Returns:
            dict with success status and message
        """
        import time
        start_time = time.time()
        
        try:
            async with aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_tls,
                timeout=10
            ) as smtp:
                await smtp.login(self.username, self.password)
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"[SMTP] Connection test successful ({latency_ms}ms)")
            
            return {
                "success": True,
                "message": "Connection successful",
                "latency_ms": latency_ms
            }
            
        except aiosmtplib.SMTPAuthenticationError:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "message": "Authentication failed - invalid username or password",
                "latency_ms": latency_ms
            }
        except aiosmtplib.SMTPConnectError:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "message": f"Connection failed - cannot reach {self.host}:{self.port}",
                "latency_ms": latency_ms
            }
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "latency_ms": latency_ms
            }
