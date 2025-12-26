
from typing import List, Optional, Type
from langchain.tools import BaseTool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from src.services.integration_service import IntegrationService
from src.integrations.chatwoot_connector import ChatwootConnector

class HandoffInput(BaseModel):
    message: str = Field(..., description="Message to send to the user before handoff (e.g., 'Transferring you now...')")
    reason: str = Field(..., description="Internal note explaining why handoff is needed")

def get_chatwoot_tools(client_id: str, agent_id: Optional[str] = None) -> List[BaseTool]:
    """
    Factory for Chatwoot Tools.
    """
    svc = IntegrationService(client_id=client_id)
    config_entry = svc.get_integration(provider='chatwoot', agent_id=agent_id)
    
    if not config_entry or not config_entry.get('config'):
        return []

    connector = ChatwootConnector(config_entry['config'])

    def handoff_func(message: str, reason: str, conversation_id: Optional[str] = None) -> str:
        """
        Transfers the conversation to a human agent.
        NOTE: Ideally, conversation_id comes from context. 
        If the tool is called within an Agent handling a request, the Agent usually knows the conversation ID.
        However, standard tools are stateless.
        
        If conversation_id is NOT passed, we might fail or need to infer from some global context (bad practice).
        For now, let's assume the Agent (Brain) will pass the 'id' if available in memory.
        """
        # In a real "Handoff", we:
        # 1. Send the 'message' to the user.
        # 2. Toggle Conversation Status to 'open' (if it was 'snoozed' or 'bot').
        # 3. Add a private note with 'reason'.
        
        # NOTE: Connector needs to support 'toggle_status' and 'create_note'. 
        # Current connector mostly does sync_message. 
        # For MVP, we will try to just 'send message' marking it as imminent handover.
        
        # If conversation_id is missing (which is common if tool is just a string definition), 
        # this logic is tricky without the Context Injection of LangChain.
        
        return f"Handoff simulated: User told '{message}'. Internal Reason: {reason}. (Real API call pending full implementation)"

    # To make this real, we need the conversation_id. 
    # Usually, we inject this via `functools.partial` when initializing the tool for a specific request context.
    # But `get_chatwoot_tools` is called at Agent Initialization time (Registry).
    
    return [
        StructuredTool.from_function(
            func=handoff_func,
            name="handoff_to_human",
            description="Transfer the conversation to a human support agent. Use this when you cannot answer the user's question.",
            args_schema=HandoffInput
        )
    ]
