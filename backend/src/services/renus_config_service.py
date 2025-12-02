"""
Renus Config Service - Business logic for RENUS configuration
Sprint 04 - Sistema Multi-Agente

Service for managing RENUS agent configuration per client.
"""

from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ..config.supabase import supabase_admin
from ..models.renus_config import (
    RenusConfigCreate,
    RenusConfigUpdate,
    RenusConfigResponse,
    InstructionsUpdate,
    GuardrailsUpdate,
    AdvancedUpdate,
    ToolsUpdate
)
from ..utils.logger import logger


class RenusConfigService:
    """Service for managing RENUS configuration"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = supabase_admin
    
    async def get_config(self, client_id: UUID) -> Optional[RenusConfigResponse]:
        """
        Get RENUS configuration for a client.
        
        Args:
            client_id: UUID of the client
        
        Returns:
            RenusConfigResponse or None if not found
        """
        try:
            response = self.supabase.table('renus_config')\
                .select('*')\
                .eq('client_id', str(client_id))\
                .execute()
            
            if not response.data:
                return None
            
            return RenusConfigResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Error getting config for client {client_id}: {e}")
            raise
    
    async def create_default_config(self, client_id: UUID) -> RenusConfigResponse:
        """
        Create default RENUS configuration for a client.
        
        Args:
            client_id: UUID of the client
        
        Returns:
            RenusConfigResponse with created configuration
        
        Raises:
            Exception: If creation fails
        """
        try:
            logger.info(f"Creating default config for client {client_id}")
            
            # Default configuration
            default_config = {
                'client_id': str(client_id),
                'system_prompt': """You are RENUS, an intelligent assistant for the RENUM system.

Your role is to help users by:
1. Answering questions about the system
2. Routing conversations to specialized sub-agents when needed
3. Providing helpful and accurate information
4. Maintaining a professional and friendly tone

Always be helpful, clear, and concise in your responses.""",
                'instructions': 'Be helpful and professional',
                'model': 'gpt-4-turbo-preview',
                'temperature': 0.7,
                'max_tokens': 2048,
                'top_p': 1.0,
                'guardrails': {
                    'content_filter': True,
                    'rate_limit': 100,
                    'max_message_length': 4000
                },
                'enabled_tools': [],
                'topics': [],
                'streaming': True,
                'memory_enabled': True,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Insert into database
            response = self.supabase.table('renus_config').insert(default_config).execute()
            
            if not response.data:
                raise Exception("Failed to create default config")
            
            config = RenusConfigResponse(**response.data[0])
            logger.info(f"Default config created for client {client_id}")
            
            return config
            
        except Exception as e:
            logger.error(f"Error creating default config for client {client_id}: {e}")
            raise
    
    async def get_or_create_config(self, client_id: UUID) -> RenusConfigResponse:
        """
        Get configuration for client, creating default if doesn't exist.
        
        Args:
            client_id: UUID of the client
        
        Returns:
            RenusConfigResponse
        """
        config = await self.get_config(client_id)
        
        if not config:
            config = await self.create_default_config(client_id)
        
        return config
    
    async def update_config(
        self,
        client_id: UUID,
        data: RenusConfigUpdate
    ) -> RenusConfigResponse:
        """
        Update RENUS configuration for a client.
        
        Args:
            client_id: UUID of the client
            data: RenusConfigUpdate with fields to update
        
        Returns:
            RenusConfigResponse with updated configuration
        
        Raises:
            Exception: If update fails or config not found
        """
        try:
            logger.info(f"Updating config for client {client_id}")
            
            # Check if config exists
            existing = await self.get_config(client_id)
            if not existing:
                raise Exception(f"Config not found for client {client_id}")
            
            # Prepare update data (only include non-None fields)
            update_data = data.model_dump(exclude_unset=True)
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.now().isoformat()
            
            # Update in database
            response = self.supabase.table('renus_config')\
                .update(update_data)\
                .eq('client_id', str(client_id))\
                .execute()
            
            if not response.data:
                raise Exception("Failed to update config")
            
            config = RenusConfigResponse(**response.data[0])
            logger.info(f"Config updated for client {client_id}")
            
            return config
            
        except Exception as e:
            logger.error(f"Error updating config for client {client_id}: {e}")
            raise
    
    async def update_instructions(
        self,
        client_id: UUID,
        data: InstructionsUpdate
    ) -> RenusConfigResponse:
        """
        Update only instructions section.
        
        Args:
            client_id: UUID of the client
            data: InstructionsUpdate with system_prompt and instructions
        
        Returns:
            RenusConfigResponse with updated configuration
        """
        update_data = RenusConfigUpdate(
            system_prompt=data.system_prompt,
            instructions=data.instructions
        )
        return await self.update_config(client_id, update_data)
    
    async def update_guardrails(
        self,
        client_id: UUID,
        data: GuardrailsUpdate
    ) -> RenusConfigResponse:
        """
        Update only guardrails section.
        
        Args:
            client_id: UUID of the client
            data: GuardrailsUpdate with guardrails configuration
        
        Returns:
            RenusConfigResponse with updated configuration
        """
        update_data = RenusConfigUpdate(guardrails=data.guardrails)
        return await self.update_config(client_id, update_data)
    
    async def update_advanced(
        self,
        client_id: UUID,
        data: AdvancedUpdate
    ) -> RenusConfigResponse:
        """
        Update only advanced settings section.
        
        Args:
            client_id: UUID of the client
            data: AdvancedUpdate with advanced settings
        
        Returns:
            RenusConfigResponse with updated configuration
        """
        update_data = RenusConfigUpdate(**data.model_dump(exclude_unset=True))
        return await self.update_config(client_id, update_data)
    
    async def update_tools(
        self,
        client_id: UUID,
        data: ToolsUpdate
    ) -> RenusConfigResponse:
        """
        Update enabled tools.
        
        Args:
            client_id: UUID of the client
            data: ToolsUpdate with list of enabled tool IDs
        
        Returns:
            RenusConfigResponse with updated configuration
        """
        update_data = RenusConfigUpdate(enabled_tools=data.enabled_tools)
        return await self.update_config(client_id, update_data)
