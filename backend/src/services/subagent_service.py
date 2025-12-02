"""
SubAgent Service - Business logic for managing sub-agents
Sprint 04 - Sistema Multi-Agente

Service for CRUD operations on sub-agents.
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..config.supabase import supabase_admin
from ..models.sub_agent import (
    SubAgentCreate,
    SubAgentUpdate,
    SubAgentResponse
)
from ..utils.logger import logger


class SubAgentService:
    """Service for managing sub-agents"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = supabase_admin
    
    async def create_subagent(self, data: SubAgentCreate) -> SubAgentResponse:
        """
        Create a new sub-agent.
        
        Args:
            data: SubAgentCreate with sub-agent data
        
        Returns:
            SubAgentResponse with created sub-agent
        
        Raises:
            Exception: If creation fails
        """
        try:
            logger.info(f"Creating sub-agent: {data.name}")
            
            # Validate model
            valid_models = ["gpt-4", "gpt-4-turbo-preview", "gpt-4o-mini", "claude-3-5-sonnet-20241022", "claude-3-opus"]
            if data.model not in valid_models:
                raise ValueError(f"Invalid model: {data.model}. Must be one of: {', '.join(valid_models)}")
            
            # Validate channel
            valid_channels = ["whatsapp", "web", "sms", "email"]
            if data.channel not in valid_channels:
                raise ValueError(f"Invalid channel: {data.channel}. Must be one of: {', '.join(valid_channels)}")
            
            # Validate system_prompt
            if not data.system_prompt or len(data.system_prompt.strip()) == 0:
                raise ValueError("system_prompt cannot be empty")
            
            # Prepare data for insertion
            subagent_data = data.model_dump()
            subagent_data['created_at'] = datetime.now().isoformat()
            subagent_data['updated_at'] = datetime.now().isoformat()
            
            # Insert into database
            response = self.supabase.table('sub_agents').insert(subagent_data).execute()
            
            if not response.data:
                raise Exception("Failed to create sub-agent")
            
            subagent = SubAgentResponse(**response.data[0])
            logger.info(f"Sub-agent created: {subagent.id}")
            
            return subagent
            
        except Exception as e:
            logger.error(f"Error creating sub-agent: {e}")
            raise
    
    async def get_subagent(self, subagent_id: UUID) -> Optional[SubAgentResponse]:
        """
        Get sub-agent by ID.
        
        Args:
            subagent_id: UUID of the sub-agent
        
        Returns:
            SubAgentResponse or None if not found
        """
        try:
            response = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('id', str(subagent_id))\
                .execute()
            
            if not response.data:
                return None
            
            return SubAgentResponse(**response.data[0])
            
        except Exception as e:
            logger.error(f"Error getting sub-agent {subagent_id}: {e}")
            raise
    
    async def list_subagents(
        self,
        is_active: Optional[bool] = None,
        channel: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[SubAgentResponse]:
        """
        List sub-agents with optional filtering.
        
        Args:
            is_active: Filter by active status (optional)
            channel: Filter by channel (optional)
            limit: Number of results per page
            offset: Offset for pagination
        
        Returns:
            List of SubAgentResponse objects
        """
        try:
            # Build query
            query = self.supabase.table('sub_agents').select('*')
            
            # Apply filters
            if is_active is not None:
                query = query.eq('is_active', is_active)
            
            if channel:
                query = query.eq('channel', channel)
            
            # Order by created_at DESC
            query = query.order('created_at', desc=True)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1)
            
            # Execute query
            response = query.execute()
            
            return [SubAgentResponse(**agent) for agent in response.data]
            
        except Exception as e:
            logger.error(f"Error listing sub-agents: {e}")
            raise
    
    async def update_subagent(
        self,
        subagent_id: UUID,
        data: SubAgentUpdate
    ) -> SubAgentResponse:
        """
        Update sub-agent.
        
        Args:
            subagent_id: UUID of the sub-agent
            data: SubAgentUpdate with fields to update
        
        Returns:
            SubAgentResponse with updated sub-agent
        
        Raises:
            Exception: If update fails or sub-agent not found
        """
        try:
            logger.info(f"Updating sub-agent: {subagent_id}")
            
            # Check if sub-agent exists
            existing = await self.get_subagent(subagent_id)
            if not existing:
                raise Exception(f"Sub-agent {subagent_id} not found")
            
            # Prepare update data (only include non-None fields)
            update_data = data.model_dump(exclude_unset=True)
            
            # Validate model if provided
            if 'model' in update_data:
                valid_models = ["gpt-4", "gpt-4-turbo-preview", "gpt-4o-mini", "claude-3-5-sonnet-20241022", "claude-3-opus"]
                if update_data['model'] not in valid_models:
                    raise ValueError(f"Invalid model: {update_data['model']}")
            
            # Validate channel if provided
            if 'channel' in update_data:
                valid_channels = ["whatsapp", "web", "sms", "email"]
                if update_data['channel'] not in valid_channels:
                    raise ValueError(f"Invalid channel: {update_data['channel']}")
            
            # Validate system_prompt if provided
            if 'system_prompt' in update_data and not update_data['system_prompt'].strip():
                raise ValueError("system_prompt cannot be empty")
            
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.now().isoformat()
            
            # Update in database
            response = self.supabase.table('sub_agents')\
                .update(update_data)\
                .eq('id', str(subagent_id))\
                .execute()
            
            if not response.data:
                raise Exception("Failed to update sub-agent")
            
            subagent = SubAgentResponse(**response.data[0])
            logger.info(f"Sub-agent updated: {subagent.id}")
            
            return subagent
            
        except Exception as e:
            logger.error(f"Error updating sub-agent {subagent_id}: {e}")
            raise
    
    async def delete_subagent(self, subagent_id: UUID) -> bool:
        """
        Delete sub-agent.
        
        Checks for active interviews before deletion.
        
        Args:
            subagent_id: UUID of the sub-agent
        
        Returns:
            True if deleted successfully
        
        Raises:
            Exception: If deletion fails or sub-agent has active interviews
        """
        try:
            logger.info(f"Deleting sub-agent: {subagent_id}")
            
            # Check if sub-agent exists
            existing = await self.get_subagent(subagent_id)
            if not existing:
                raise Exception(f"Sub-agent {subagent_id} not found")
            
            # Check for active interviews
            interviews_response = self.supabase.table('interviews')\
                .select('id')\
                .eq('subagent_id', str(subagent_id))\
                .eq('status', 'in_progress')\
                .execute()
            
            if interviews_response.data and len(interviews_response.data) > 0:
                raise Exception(
                    f"Cannot delete sub-agent {subagent_id}: "
                    f"{len(interviews_response.data)} active interviews in progress"
                )
            
            # Delete from database
            response = self.supabase.table('sub_agents')\
                .delete()\
                .eq('id', str(subagent_id))\
                .execute()
            
            logger.info(f"Sub-agent deleted: {subagent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting sub-agent {subagent_id}: {e}")
            raise
    
    async def toggle_active(self, subagent_id: UUID) -> SubAgentResponse:
        """
        Toggle is_active status of sub-agent.
        
        Args:
            subagent_id: UUID of the sub-agent
        
        Returns:
            SubAgentResponse with updated sub-agent
        
        Raises:
            Exception: If toggle fails or sub-agent not found
        """
        try:
            logger.info(f"Toggling active status for sub-agent: {subagent_id}")
            
            # Get current status
            existing = await self.get_subagent(subagent_id)
            if not existing:
                raise Exception(f"Sub-agent {subagent_id} not found")
            
            # Toggle status
            new_status = not existing.is_active
            
            # Update in database
            update_data = {
                'is_active': new_status,
                'updated_at': datetime.now().isoformat()
            }
            
            response = self.supabase.table('sub_agents')\
                .update(update_data)\
                .eq('id', str(subagent_id))\
                .execute()
            
            if not response.data:
                raise Exception("Failed to toggle sub-agent status")
            
            subagent = SubAgentResponse(**response.data[0])
            logger.info(f"Sub-agent {subagent_id} is_active set to: {new_status}")
            
            return subagent
            
        except Exception as e:
            logger.error(f"Error toggling sub-agent {subagent_id}: {e}")
            raise
    
    async def get_stats(self, subagent_id: UUID) -> dict:
        """
        Get usage statistics for a sub-agent.
        
        Args:
            subagent_id: UUID of the sub-agent
        
        Returns:
            Dict with statistics (total_interviews, completion_rate, etc)
        """
        try:
            # Get total interviews
            total_response = self.supabase.table('interviews')\
                .select('id', count='exact')\
                .eq('subagent_id', str(subagent_id))\
                .execute()
            
            total_interviews = total_response.count or 0
            
            # Get completed interviews
            completed_response = self.supabase.table('interviews')\
                .select('id', count='exact')\
                .eq('subagent_id', str(subagent_id))\
                .eq('status', 'completed')\
                .execute()
            
            completed_interviews = completed_response.count or 0
            
            # Calculate completion rate
            completion_rate = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
            
            return {
                'total_interviews': total_interviews,
                'completed_interviews': completed_interviews,
                'in_progress_interviews': total_interviews - completed_interviews,
                'completion_rate': round(completion_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting stats for sub-agent {subagent_id}: {e}")
            raise

    
    # ========================================================================
    # Public URL Methods
    # ========================================================================
    
    async def get_by_slug(self, slug: str) -> Optional[dict]:
        """
        Get sub-agent by slug.
        
        Args:
            slug: URL-friendly identifier (ex: pesquisa-mmn)
        
        Returns:
            Dict with sub-agent data or None if not found
        """
        try:
            response = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('slug', slug)\
                .execute()
            
            if not response.data:
                return None
            
            return response.data[0]
            
        except Exception as e:
            logger.error(f"Error getting sub-agent by slug {slug}: {e}")
            raise
    
    async def increment_access_count(self, subagent_id: UUID) -> bool:
        """
        Increment access counter for public URL.
        
        Args:
            subagent_id: UUID of the sub-agent
        
        Returns:
            True if incremented successfully
        """
        try:
            # Get current count
            response = self.supabase.table('sub_agents')\
                .select('access_count')\
                .eq('id', str(subagent_id))\
                .execute()
            
            if not response.data:
                return False
            
            current_count = response.data[0].get('access_count', 0)
            
            # Increment
            self.supabase.table('sub_agents')\
                .update({'access_count': current_count + 1})\
                .eq('id', str(subagent_id))\
                .execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error incrementing access count for {subagent_id}: {e}")
            return False
    
    async def list_public_agents(self) -> List[dict]:
        """
        List all public sub-agents.
        
        Returns:
            List of public sub-agents
        """
        try:
            response = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('is_public', True)\
                .eq('is_active', True)\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error listing public agents: {e}")
            raise
    
    async def generate_public_url(self, subagent_id: UUID, base_url: str) -> str:
        """
        Generate and save public URL for sub-agent.
        
        Args:
            subagent_id: UUID of the sub-agent
            base_url: Base URL of the application (ex: https://app.renum.com)
        
        Returns:
            Complete public URL
        """
        try:
            # Get sub-agent
            subagent = await self.get_subagent(subagent_id)
            if not subagent:
                raise Exception(f"Sub-agent {subagent_id} not found")
            
            # Get or generate slug
            if not subagent.slug:
                # Generate slug from name
                slug = self._generate_slug(subagent.name)
                
                # Update with slug
                self.supabase.table('sub_agents')\
                    .update({'slug': slug})\
                    .eq('id', str(subagent_id))\
                    .execute()
            else:
                slug = subagent.slug
            
            # Generate public URL
            public_url = f"{base_url}/chat/{slug}"
            
            # Save public URL
            self.supabase.table('sub_agents')\
                .update({'public_url': public_url})\
                .eq('id', str(subagent_id))\
                .execute()
            
            return public_url
            
        except Exception as e:
            logger.error(f"Error generating public URL for {subagent_id}: {e}")
            raise
    
    def _generate_slug(self, name: str) -> str:
        """
        Generate URL-friendly slug from name.
        
        Args:
            name: Sub-agent name
        
        Returns:
            URL-friendly slug
        """
        import re
        import unicodedata
        
        # Normalize unicode characters
        slug = unicodedata.normalize('NFKD', name)
        slug = slug.encode('ascii', 'ignore').decode('ascii')
        
        # Convert to lowercase
        slug = slug.lower()
        
        # Replace spaces and special chars with hyphens
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug

    
    def get_by_slug(self, slug: str) -> dict | None:
        """
        Busca sub-agente pelo slug.
        
        Args:
            slug: Slug do sub-agente (ex: "pesquisa-mmn")
        
        Returns:
            Dict com dados do sub-agente ou None se não encontrado
        """
        try:
            response = self.supabase.table('sub_agents')\
                .select('*')\
                .eq('slug', slug)\
                .eq('is_public', True)\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            logger.error(f"Error getting sub-agent by slug {slug}: {e}")
            return None
    
    def increment_access_count(self, subagent_id: str) -> bool:
        """
        Incrementa contador de acessos do sub-agente.
        
        Args:
            subagent_id: UUID do sub-agente
        
        Returns:
            True se incrementou com sucesso
        """
        try:
            # Buscar contador atual
            response = self.supabase.table('sub_agents')\
                .select('access_count')\
                .eq('id', subagent_id)\
                .single()\
                .execute()
            
            current_count = response.data.get('access_count', 0) if response.data else 0
            
            # Incrementar
            self.supabase.table('sub_agents')\
                .update({'access_count': current_count + 1})\
                .eq('id', subagent_id)\
                .execute()
            
            logger.info(f"Access count incremented for sub-agent {subagent_id}: {current_count + 1}")
            return True
            
        except Exception as e:
            logger.error(f"Error incrementing access count for {subagent_id}: {e}")
            return False

    
    def list_sub_agents(self, active_only: bool = False, agent_type: str = None) -> list:
        """
        Lista todos os sub-agentes.
        
        Args:
            active_only: Se True, retorna apenas agentes ativos
            agent_type: Filtrar por tipo de agente
        
        Returns:
            Lista de SubAgentResponse
        """
        try:
            query = self.supabase.table('sub_agents').select('*')
            
            if active_only:
                query = query.eq('is_active', True)
            
            if agent_type:
                query = query.eq('type', agent_type)
            
            response = query.execute()
            
            if not response.data:
                return []
            
            # Converter para SubAgentResponse para garantir todos os campos
            from src.models.sub_agent import SubAgentResponse
            return [SubAgentResponse(**agent) for agent in response.data]
            
        except Exception as e:
            logger.error(f"Error listing sub-agents: {e}")
            return []
