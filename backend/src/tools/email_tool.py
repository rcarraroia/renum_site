"""
Email Tool - LangChain Tool for Sending Emails
Sprint 07A - Integrações Core (Updated)

Tool that agents can use to send emails.
Uses SMTP or SendGrid clients and Celery for async sending.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field, EmailStr
import asyncio
from uuid import UUID

from ..services.integration_service import IntegrationService


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
    Uses SMTP or SendGrid clients and Celery for async sending.
    
    Example usage in agent:
        tools = [EmailTool(client_id="uuid")]
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
    
    Returns a dict with success status and task_id."""
    
    args_schema: type[BaseModel] = EmailInput
    
    client_id: Optional[UUID] = None
    
    def __init__(self, client_id: Optional[UUID] = None, **kwargs):
        """
        Initialize Email tool.
        
        Args:
            client_id: Client ID for loading integration config
            **kwargs: Additional BaseTool arguments
        """
        super().__init__(**kwargs)
        self.client_id = client_id
    
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
        Send email asynchronously via Celery.
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body (HTML or plain text)
            cc: Optional CC recipients
        
        Returns:
            Dict with success status and task_id or error
        """
        try:
            # Validate recipients
            if not to or len(to) == 0:
                return {
                    "success": False,
                    "error": "At least one recipient is required"
                }
            
            # Load integration config
            if not self.client_id:
                return {
                    "success": False,
                    "error": "client_id is required to send emails"
                }
            
            integration_service = IntegrationService()
            
            # Try SMTP first
            integration = await integration_service.get_integration(self.client_id, "email_smtp")
            
            # If no SMTP, try SendGrid
            if not integration:
                integration = await integration_service.get_integration(self.client_id, "email_sendgrid")
            
            if not integration:
                return {
                    "success": False,
                    "error": "Email integration not configured for this client"
                }
            
            if integration.status != "active":
                return {
                    "success": False,
                    "error": f"Email integration is {integration.status}, not active"
                }
            
            # Enqueue Celery task for async sending
            from ..workers.message_tasks import send_email_task
            
            task = send_email_task.delay(
                client_id=str(self.client_id),
                to=to,
                subject=subject,
                body=body,
                cc=cc
            )
            
            return {
                "success": True,
                "task_id": task.id,
                "recipients": to,
                "status": "queued"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send email: {str(e)}"
            }


def get_email_tool(client_id: Optional[UUID] = None) -> EmailTool:
    """
    Get email tool instance.
    
    Args:
        client_id: Client ID for loading integration config
    
    Returns:
        EmailTool instance
    
    Example:
        >>> tool = get_email_tool(client_id="uuid")
        >>> result = await tool._arun(
        ...     to=["user@example.com"],
        ...     subject="Test",
        ...     body="Hello!"
        ... )
    """
    return EmailTool(client_id=client_id)
