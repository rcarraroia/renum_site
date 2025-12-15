
import os
import logging
from typing import Dict, Any, List, Optional
from src.config.supabase import supabase_admin
from uuid import UUID

logger = logging.getLogger(__name__)

class IntegrationService:
    """
    Service to manage external integrations (Uazapi, Chatwoot, etc.)
    Handles encryption, storage, and retrieval with Client/Agent hierarchy.
    """
    
    def __init__(self, client_id: Optional[str] = None):
        """
        :param client_id: Context client_id (optional, used for listing)
        """
        self.client_id = client_id

    def list_integrations(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List integrations for the current client, optionally filtered by provider.
        Returns both Global (agent_id=NULL) and Agent-Specific (agent_id=NOT NULL).
        """
        if not self.client_id:
            raise ValueError("Client ID is required to list integrations")

        try:
            query = supabase_admin.table('agent_integrations').select('*').eq('client_id', self.client_id)
            
            if provider:
                query = query.eq('provider', provider)
                
            response = query.execute()
            
            # Simple post-processing (e.g. masking secrets) could happen here
            return response.data
        except Exception as e:
            logger.error(f"Error listing integrations: {e}")
            raise

    def get_integration(self, provider: str, agent_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the BEST integration config for a given agent/provider.
        Logic:
        1. If agent_id provided, check for Agent-Specific Override.
        2. If not found or no agent_id, check for Client Global config.
        3. Validates 'is_active'.
        """
        if not self.client_id:
            logger.warning("No client_id in context, attempting to infer from agent or fallback.")
            # In a real scenario we'd fetch client_id from agent_id if missing. 
            # For now assume client_id is passed or we query differently.
            pass

        try:
            # 1. Try Agent Specific
            if agent_id:
                agent_res = supabase_admin.table('agent_integrations')\
                    .select('*')\
                    .eq('provider', provider)\
                    .eq('agent_id', agent_id)\
                    .eq('is_active', True)\
                    .execute()
                
                if agent_res.data and len(agent_res.data) > 0:
                    logger.info(f"Using Agent-Specific integration for {provider} (Agent: {agent_id})")
                    return agent_res.data[0]
            
            # 2. Fallback to Client Global
            # If we don't know client_id but have agent_id, fetch it?
            # ideally self.client_id should be set.
            if self.client_id:
                client_res = supabase_admin.table('agent_integrations')\
                    .select('*')\
                    .eq('provider', provider)\
                    .eq('client_id', self.client_id)\
                    .is_('agent_id', 'null')\
                    .eq('is_active', True)\
                    .execute()
                    
                if client_res.data and len(client_res.data) > 0:
                    logger.info(f"Using Client-Global integration for {provider} (Client: {self.client_id})")
                    return client_res.data[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error resolving integration hierarchy: {e}")
            return None

    def save_integration(self, 
                        provider: str, 
                        config: Dict[str, Any], 
                        agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create or Update an integration.
        If agent_id is None => Global Client Config.
        """
        if not self.client_id:
            raise ValueError("Client ID required to save integration")
            
        # TODO: Encrypt sensitive fields in 'config' here
        # For MVP we store raw (RLS protects access)
        
        data = {
            "client_id": self.client_id,
            "provider": provider,
            "config": config,
            "is_active": True
        }
        
        if agent_id:
            data['agent_id'] = agent_id
        else:
            data['agent_id'] = None # Global
            
        # Upsert Logic
        # We need a conflict constraint. We created UNIQUE indexes in migration.
        # However, supabase upsert needs the constraint name or columns.
        
        try:
            # Try to find existing id to update, or insert new
            existing = self.get_exact_integration(provider, agent_id)
            
            if existing:
                # Update
                res = supabase_admin.table('agent_integrations')\
                    .update(data)\
                    .eq('id', existing['id'])\
                    .execute()
                return res.data[0] if res.data else {}
            else:
                # Insert
                res = supabase_admin.table('agent_integrations')\
                    .insert(data)\
                    .execute()
                return res.data[0] if res.data else {}
                
        except Exception as e:
            logger.error(f"Error saving integration: {e}")
            raise

    def get_exact_integration(self, provider: str, agent_id: Optional[str] = None):
        """Helper to find specific row without hierarchy fallback"""
        query = supabase_admin.table('agent_integrations')\
            .select('*')\
            .eq('client_id', self.client_id)\
            .eq('provider', provider)
            
        if agent_id:
            query = query.eq('agent_id', agent_id)
        else:
            query = query.is_('agent_id', 'null')
            
        res = query.execute()
        return res.data[0] if res.data else None
