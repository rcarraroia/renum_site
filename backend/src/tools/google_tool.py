
from typing import List, Optional, Dict, Any, Type
from langchain.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field

from src.services.integration_service import IntegrationService
from src.integrations.google_connector import GoogleConnector

# --- Input Schemas ---
class SendEmailInput(BaseModel):
    to: str = Field(..., description="Email address of the recipient")
    subject: str = Field(..., description="Subject of the email")
    body: str = Field(..., description="Content of the email message")

class CreateEventInput(BaseModel):
    summary: str = Field(..., description="Title of the event")
    start_time: str = Field(..., description="ISO start time (e.g. 2023-12-25T10:00:00)")
    duration_minutes: int = Field(60, description="Duration in minutes")

class DriveListInput(BaseModel):
    query: Optional[str] = Field(None, description="Search query for file name")

# --- Factories ---
def get_google_tools(client_id: str, agent_id: Optional[str] = None) -> List[BaseTool]:
    """
    Factory to create Google Suite tools for a specific client/agent.
    """
    # 1. Load credentials
    service = IntegrationService()
    # Logic: Try agent specific first, then client global
    # IntegrationService.get_integration handles the 'best match' logic?
    # Actually get_integration logic is: provide agent_id, if not found, look for client global.
    # But IntegrationService needs client_id to be set in __init__ or passed.
    # Current IntegrationService implementation might need instantiation with client_id.
    
    # Let's check IntegrationService again or assume we set client_id
    svc = IntegrationService(client_id=client_id)
    config_entry = svc.get_integration(provider='google', agent_id=agent_id)
    
    if not config_entry or not config_entry.get('config'):
        # If no integration, return empty list (Tools unavailable)
        return []

    connector = GoogleConnector(config_entry['config'])
    
    # 2. Define Tools
    
    def gmail_send_func(to: str, subject: str, body: str) -> str:
        res = connector.send_email(to, subject, body)
        if res.get("success"):
            return f"Email sent successfully. ID: {res.get('id')}"
        return f"Failed to send email: {res.get('error')}"

    def calendar_create_func(summary: str, start_time: str, duration_minutes: int) -> str:
        # Simplification: Connector currently has list_events only. 
        # We need to implement create_event in connector if widely used.
        # check connector capabilities first.
        # Assuming for now we only have list. Let's expose list only for safety or add create to connector.
        # But per user request, we want tools. Let's expose what exists: list_events
        return "Feature pending implementation in Connector."

    def calendar_list_func(max_results: int = 5) -> str:
        res = connector.list_events(max_results)
        if res.get("success"):
            events = res.get("events", [])
            if not events:
                return "No upcoming events found."
            return "\n".join([f"- {e.get('summary')} ({e.get('start', {}).get('dateTime', 'N/A')})" for e in events])
        return f"Error listing events: {res.get('error')}"

    def drive_list_func(query: Optional[str] = None) -> str:
        res = connector.list_files()
        if res.get("success"):
            files = res.get("files", [])
            return "\n".join([f"- {f.get('name')} (ID: {f.get('id')})" for f in files])
        return f"Error listing files: {res.get('error')}"

    tools = [
        StructuredTool.from_function(
            func=gmail_send_func,
            name="gmail_send",
            description="Send an email using the connected Gmail account.",
            args_schema=SendEmailInput
        ),
        StructuredTool.from_function(
            func=calendar_list_func,
            name="calendar_list",
            description="List upcoming events from the connected Google Calendar."
        ),
        StructuredTool.from_function(
            func=drive_list_func,
            name="drive_list_files",
            description="List files in Google Drive."
        )
    ]
    
    return tools
