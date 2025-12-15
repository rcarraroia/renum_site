
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ChatwootConnector:
    """
    Connector for Chatwoot API.
    Used for syncing conversations and Human Handoff.
    """
    
    def __init__(self, api_url: str, api_access_token: str, account_id: str = "1"):
        """
        :param api_url: Base URL (e.g., https://app.chatwoot.com)
        :param api_access_token: User API Token (Admin)
        :param account_id: Account ID (default 1)
        """
        self.api_url = api_url.rstrip('/')
        self.headers = {
            "api_access_token": api_access_token,
            "Content-Type": "application/json"
        }
        self.account_id = account_id

    def create_inbox(self, name: str, source_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an API Inbox for an Agent.
        :param name: Inbox Name (e.g. "Agent Vendas")
        :param source_id: Useful for mapping back to Renus Agent ID
        """
        url = f"{self.api_url}/api/v1/accounts/{self.account_id}/inboxes"
        payload = {
            "name": name,
            "channel": {
                "type": "api",
                "webhook_url": "" # We could set a webhook to receive replies back to Renus
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating Chatwoot inbox: {e}")
            return {"error": str(e)}

    def create_contact(self, inbox_id: int, name: str, identifier: str) -> Dict[str, Any]:
        """
        Create or Get Contact.
        :param identifier: Unique ID (e.g. Phone Number or Email)
        """
        # Chatwoot usually searches by identifier first
        search_url = f"{self.api_url}/api/v1/accounts/{self.account_id}/contacts/search"
        try:
            search_res = requests.get(search_url, params={"q": identifier}, headers=self.headers)
            if search_res.ok and search_res.json()['payload']:
                return search_res.json()['payload'][0]
                
            # Create
            create_url = f"{self.api_url}/api/v1/accounts/{self.account_id}/contacts"
            payload = {
                "inbox_id": inbox_id,
                "name": name,
                "identifier": identifier,
                "phone_number": identifier if identifier.startswith('+') else None
            }
            res = requests.post(create_url, json=payload, headers=self.headers)
            res.raise_for_status()
            return res.json()['payload']['contact']
        except Exception as e:
             logger.error(f"Error managing Chatwoot contact: {e}")
             return {}

    def sync_message(self, 
                    inbox_id: int, 
                    source_id: str, 
                    content: str, 
                    message_type: str = "incoming",
                    contact_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Push a message to Chatwoot.
        :param message_type: 'incoming' (User->New) or 'outgoing' (Agent->User)
        """
        # First we need a conversation
        try:
            # Create/Find conversation
            conv_url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations"
            conv_payload = {
                "source_id": source_id,
                "inbox_id": inbox_id
            }
            if contact_id:
                conv_payload["contact_id"] = contact_id
                
            # Chatwoot API behaves differently for finding existing by source_id depending on version
            # Usually we use source_id to map. 
            # For API channels, creating a conversation with same source_id returns the existing one usually.
            
            conv_res = requests.post(conv_url, json=conv_payload, headers=self.headers)
            # If 200/201, we have conversation
            conversation_id = conv_res.json().get('id')
            
            # Send Message
            msg_url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
            msg_payload = {
                "content": content,
                "message_type": message_type,
                "private": False
            }
            
            msg_res = requests.post(msg_url, json=msg_payload, headers=self.headers)
            msg_res.raise_for_status()
            return msg_res.json()
            
        except Exception as e:
            logger.error(f"Error syncing message to Chatwoot: {e}")
            return {"error": str(e)}
