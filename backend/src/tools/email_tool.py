"""
Email Tool - LangChain Tool for Sending Emails
Sprint 04 - Sistema Multi-Agente

Tool that agents can use to send emails.
Placeholder implementation - actual email provider to be configured per project.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, EmailStr
import asyncio


class EmailInput(BaseModel):
    """Input schema for email tool"""
    
    to: List[EmailStr] = Field(
        ...,
        description="List of recipient email addresses"
    )
    subject: str = Field(
        ...,
        description="Email subject line"
    )
    body: str = Field(
        ...,
        description="Email body content (HTML or plain text)"
    )
    cc: Optional[List[EmailStr]] = Field(
        default=None,
        description="Optional list of CC recipients"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "to": ["user@example.com"],
                "subject": "Welcome to RENUM",
                "body": "<h1>Welcome!</h1><p>Thank you for joining us.</p>",
                "cc": ["admin@example.com"]
            }
        }


class EmailTool(BaseTool):
    """
    Tool for sending emails.
    
    This tool allows agents to send emails to one or more recipients.
    Supports both HTML and plain text email bodies.
    
    Note: This is a placeholder implementation. The actual email provider
    (SendGrid, AWS SES, SMTP, etc) should be configured per project.
    
    Example usage in agent:
        tools = [EmailTool()]
        agent = create_agent(llm, tools)
        result = agent.invoke("Send an email to user@example.com")
    """
    
    name: str = "send_email"
    description: str = """Send an email to one or more recipients.
    
    Use this tool when you need to send an email notification or message.
    
    Input should be:
    - to: List of recipient email addresses
    - subject: Email subject line
    - body: Email body content (can be HTML or plain text)
    - cc: Optional list of CC recipients
    
    Returns a dict with success status and message_id."""
    
    args_schema: type[BaseModel] = EmailInput
    
    def _run(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Synchronous version"""
        return asyncio.run(self._arun(to, subject, body, cc))
    
    async def _arun(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send email asynchronously.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (HTML or plain text)
            cc: Optional CC recipients
        
        Returns:
            Dict with success status and message_id or error
        """
        try:
            # Validate recipients
            if not to or len(to) == 0:
                return {
                    "success": False,
                    "error": "At least one recipient is required"
                }
            
            # TODO: Implement actual email sending based on configured provider
            # For now, this is a placeholder that logs the email
            
            from ...config.settings import settings
            
            provider = settings.EMAIL_PROVIDER.lower()
            
            if provider == "none" or not provider:
                # Mock implementation for development
                print(f"📧 [MOCK] Email sent:")
                print(f"   To: {', '.join(to)}")
                if cc:
                    print(f"   CC: {', '.join(cc)}")
                print(f"   Subject: {subject}")
                print(f"   Body: {body[:100]}...")
                
                return {
                    "success": True,
                    "message_id": f"mock_email_{asyncio.get_event_loop().time()}",
                    "recipients": to,
                    "note": "Using mock email provider - no real email sent"
                }
            
            # Future providers can be added here:
            # elif provider == "sendgrid":
            #     return await self._send_via_sendgrid(to, subject, body, cc)
            # elif provider == "ses":
            #     return await self._send_via_ses(to, subject, body, cc)
            # elif provider == "smtp":
            #     return await self._send_via_smtp(to, subject, body, cc)
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown email provider: {provider}. Set EMAIL_PROVIDER in .env"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send email: {str(e)}"
            }
    
    # Placeholder methods for future email providers
    
    async def _send_via_sendgrid(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send email via SendGrid.
        
        TODO: Implement SendGrid integration
        Requires: pip install sendgrid
        """
        raise NotImplementedError("SendGrid integration not yet implemented")
    
    async def _send_via_ses(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send email via AWS SES.
        
        TODO: Implement AWS SES integration
        Requires: pip install boto3
        """
        raise NotImplementedError("AWS SES integration not yet implemented")
    
    async def _send_via_smtp(
        self,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Send email via SMTP.
        
        TODO: Implement SMTP integration
        Requires SMTP server configuration
        """
        raise NotImplementedError("SMTP integration not yet implemented")


def get_email_tool() -> EmailTool:
    """
    Get email tool instance.
    
    Returns:
        EmailTool instance
    
    Example:
        >>> tool = get_email_tool()
        >>> result = await tool._arun(
        ...     to=["user@example.com"],
        ...     subject="Test",
        ...     body="Hello!"
        ... )
    """
    return EmailTool()
