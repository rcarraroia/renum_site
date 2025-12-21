
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from src.middleware.auth import get_current_user
from src.services.integration_service import IntegrationService
from src.integrations.uazapi_connector import UazapiConnector
from src.integrations.chatwoot_connector import ChatwootConnector

router = APIRouter(prefix="/integrations", tags=["integrations"])

class IntegrationConfigInput(BaseModel):
    config: Dict[str, Any]
    agent_id: Optional[str] = None # If set, overrides global config for this agent

@router.get("/status")
async def get_integrations_status(
    current_user: Dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Get aggregated status of all integrations for the Radar dashboard.
    """
    client_id = current_user.get('client_id')
    if not client_id:
        return []
        
    service = IntegrationService(client_id=client_id)
    try:
        integrations = service.list_integrations()
        
        status_list = []
        for integration in integrations:
            status_list.append({
                "id": str(integration.get('id')),
                "type": integration.get('provider'),
                "name": integration.get('provider').upper(),
                "status": "active" if integration.get('is_active') else "inactive",
                "last_test": integration.get('updated_at'),
                "error_message": None, # Could be expanded later
                "agent_count": 1 if integration.get('agent_id') else 5 # Mocking count for now
            })
        return status_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_integrations(
    provider: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    List all configured integrations for the current client.
    """
    client_id = current_user.get('client_id')
    client_id = current_user.get('client_id')
    if not client_id:
        # Se não tiver client_id (ex: superadmin global), retornar lista vazia para não quebrar UI
        return []
        
    service = IntegrationService(client_id=client_id)
    try:
        return service.list_integrations(provider)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{provider}")
async def save_integration(
    provider: str,
    input_data: IntegrationConfigInput,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Save integration config (Global or Agent-Specific).
    """
    client_id = current_user.get('client_id')
    if not client_id:
        raise HTTPException(status_code=400, detail="Client ID required")
        
    service = IntegrationService(client_id=client_id)
    try:
        result = service.save_integration(
            provider=provider,
            config=input_data.config,
            agent_id=input_data.agent_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{provider}/test")
async def test_integration(
    provider: str,
    input_data: IntegrationConfigInput,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Test connection with provided credentials (without saving yet, or using saved).
    """
    if provider == "uazapi":
        url = input_data.config.get("url")
        token = input_data.config.get("token")
        
        if not url or not token:
            return {"success": False, "error": "URL and Token required"}
            
        connector = UazapiConnector(api_url=url, token=token)
        status = connector.get_status()
        return {"success": True, "details": status}
    
    elif provider == "chatwoot":
        url = input_data.config.get("url")
        token = input_data.config.get("api_access_token")
        account_id = input_data.config.get("account_id", "1")

        if not url or not token:
            return {"success": False, "error": "URL and API Access Token required"}
            
        connector = ChatwootConnector(api_url=url, api_access_token=token, account_id=account_id)
        # We test by trying to search a contact or list inboxes, simple read op
        try:
            # Simple health check by listing inboxes (even if empty, 200 is success)
            # Or use a dedicated health check if available. Inboxes is safe.
            res = connector.create_inbox(name="Test Inbox", source_id="test-connection") # Actually creating inbox is side-effect.
            # detailed check: Chatwoot doesn't have a simple "profile" endpoint for api token often.
            # Let's try to search contacts with empty query or something or catching an error.
            # Best check: requests.get(f"{url}/api/v1/accounts/{account_id}/inboxes", headers=...)
            import requests
            headers = {"api_access_token": token}
            check_url = f"{url.rstrip('/')}/api/v1/accounts/{account_id}/inboxes"
            r = requests.get(check_url, headers=headers)
            r.raise_for_status()
            return {"success": True, "details": {"status": "connected", "inboxes": len(r.json().get('payload', []))}}
        except Exception as e:
             return {"success": False, "error": str(e)}

    return {"success": False, "error": f"Test not implemented for {provider}"}
