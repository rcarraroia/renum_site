"""
Task 3: Implement unified agent management service
AgentService class with CRUD operations and type-specific logic
Requirements: 5.1, 5.4
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from src.config.supabase import supabase_admin
from src.models.agent import AgentResponse, AgentCreate, AgentUpdate, AgentStats

class AgentService:
    """Unified service for managing all agent types"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    async def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """
        Create agent with type-specific logic
        
        Args:
            agent_data: Agent creation data with type information
            
        Returns:
            Created agent
        """
        # Determine agent type and apply specific logic
        if agent_data.is_template:
            return self._create_template_agent(agent_data)
        elif agent_data.is_system:
            return self._create_system_agent(agent_data)
        else:
            return self._create_client_agent(agent_data)
    
    def _create_template_agent(self, data: AgentCreate) -> AgentResponse:
        """Create marketplace template agent"""
        agent_dict = {
            **data.dict(exclude={'is_template', 'is_system'}),
            'is_template': True,
            'marketplace_visible': data.marketplace_visible or False,
            'client_id': None,  # Templates have no client
            'category': data.category or 'b2b',
            'niche': data.niche,
            'config': self._init_config_structure(data.config or {})
        }
        
        result = self.supabase.table('agents').insert(agent_dict).execute()
        return AgentResponse(**result.data[0])
    
    def _create_client_agent(self, data: AgentCreate) -> AgentResponse:
        """Create client-specific agent"""
        if not data.client_id:
            raise ValueError("client_id required for client agents")
        
        agent_dict = {
            **data.dict(exclude={'is_template', 'is_system'}),
            'is_template': False,
            'is_system': False,
            'marketplace_visible': False,
            'config': self._init_config_structure(data.config or {})
        }
        
        result = self.supabase.table('agents').insert(agent_dict).execute()
        return AgentResponse(**result.data[0])
    
    def _create_system_agent(self, data: AgentCreate) -> AgentResponse:
        """Create system agent (RENUS, ISA, etc)"""
        agent_dict = {
            **data.dict(exclude={'is_template', 'is_system'}),
            'is_template': False,
            'is_system': True,
            'client_id': None,
            'config': self._init_config_structure(data.config or {})
        }
        
        result = self.supabase.table('agents').insert(agent_dict).execute()
        return AgentResponse(**result.data[0])
    
    def _init_config_structure(self, base_config: Dict) -> Dict:
        """Initialize config with 9-category structure"""
        return {
            "instructions": base_config.get("instructions", {}),
            "intelligence": base_config.get("intelligence", {}),
            "tools": base_config.get("tools", {}),
            "integrations": base_config.get("integrations", {}),
            "knowledge": base_config.get("knowledge", {}),
            "triggers": base_config.get("triggers", {}),
            "guardrails": base_config.get("guardrails", {}),
            "sub_agents": base_config.get("sub_agents", {}),
            "advanced": base_config.get("advanced", {})
        }
    
    async def get_agent(self, agent_id: UUID) -> Optional[AgentResponse]:
        """Get agent by ID"""
        result = self.supabase.table('agents')\
            .select('*')\
            .eq('id', str(agent_id))\
            .single()\
            .execute()
        
        return AgentResponse(**result.data) if result.data else None
    
    async def update_agent(self, agent_id: UUID, update_data: AgentUpdate) -> AgentResponse:
        """Update agent"""
        update_dict = {
            k: v for k, v in update_data.dict(exclude_unset=True).items()
            if v is not None
        }
        update_dict['updated_at'] = datetime.utcnow().isoformat()
        
        result = self.supabase.table('agents')\
            .update(update_dict)\
            .eq('id', str(agent_id))\
            .execute()
        
        return AgentResponse(**result.data[0])
    
    async def delete_agent(self, agent_id: UUID) -> bool:
        """Delete agent"""
        result = self.supabase.table('agents')\
            .delete()\
            .eq('id', str(agent_id))\
            .execute()
        
        return len(result.data) > 0
    
    async def list_agents(
        self,
        client_id: Optional[UUID] = None,
        role: Optional[str] = None,
        is_template: Optional[bool] = None,
        is_system: Optional[bool] = None,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AgentResponse]:
        """List agents with filtering"""
        query = self.supabase.table('agents').select('*')
        
        if client_id:
            query = query.eq('client_id', str(client_id))
        if role:
            query = query.eq('role', role)
        if is_template is not None:
            query = query.eq('is_template', is_template)
        if is_system is not None:
            query = query.eq('is_system', is_system)
        if is_active is not None:
            query = query.eq('is_active', is_active)
        
        query = query.order('created_at', desc=True)
        query = query.range(offset, offset + limit - 1)
        
        result = query.execute()
        return [AgentResponse(**agent) for agent in result.data]
    
    async def get_by_slug(self, slug: str) -> Optional[AgentResponse]:
        """Get agent by slug"""
        result = self.supabase.table('agents')\
            .select('*')\
            .eq('slug', slug)\
            .execute()
        
        return AgentResponse(**result.data[0]) if result.data else None

    async def toggle_status(self, agent_id: UUID, new_status: str) -> AgentResponse:
        """Update agent status (is_active) based on status string"""
        is_active = new_status == "active"
        
        result = self.supabase.table('agents')\
            .update({'is_active': is_active, 'updated_at': datetime.utcnow().isoformat()})\
            .eq('id', str(agent_id))\
            .execute()
        
        if not result.data:
            raise ValueError(f"Agent {agent_id} not found")
            
        return AgentResponse(**result.data[0])

    async def get_stats(self, agent_id: UUID) -> AgentStats:
        """Get agent statistics"""
        # Count sub-agents
        sub_agents_result = self.supabase.table('sub_agents')\
            .select('id', count='exact')\
            .eq('parent_agent_id', str(agent_id))\
            .execute()
        
        sub_agents_count = sub_agents_result.count or 0
        
        # Real statistics would come from message/conversation tables
        # For now, return counts from DB if available or default to 0
        return AgentStats(
            agent_id=agent_id,
            sub_agents_count=sub_agents_count,
            total_conversations=0,
            active_conversations=0,
            total_messages=0,
            access_count=0
        )

    # Sub-agent management
    def create_sub_agent(
        self,
        parent_id: UUID,
        name: str,
        specialization: str,
        inheritance_config: Dict,
        config: Dict = None
    ) -> Dict:
        """Create sub-agent with inheritance"""
        sub_agent_data = {
            'parent_agent_id': str(parent_id),
            'name': name,
            'specialization': specialization,
            'inheritance_config': inheritance_config,
            'config': config or {},
            'routing_config': {}
        }
        
        result = self.supabase.table('sub_agents').insert(sub_agent_data).execute()
        return result.data[0]
    
    def get_effective_config(self, sub_agent_id: UUID) -> Dict:
        """Get effective configuration with inheritance applied"""
        # Get sub-agent
        sub_agent = self.supabase.table('sub_agents')\
            .select('*')\
            .eq('id', str(sub_agent_id))\
            .single()\
            .execute().data
        
        # Get parent agent
        parent = self.get_agent(UUID(sub_agent['parent_agent_id']))
        
        # Merge configs based on inheritance_config
        effective_config = {}
        inheritance = sub_agent['inheritance_config']
        
        for category in ['instructions', 'intelligence', 'tools', 'integrations',
                        'knowledge', 'triggers', 'guardrails']:
            if inheritance.get(category, False):
                # Inherit from parent
                effective_config[category] = parent.config.get(category, {})
            else:
                # Use own config
                effective_config[category] = sub_agent['config'].get(category, {})
        
        return effective_config

# Singleton
_agent_service = None

def get_agent_service() -> AgentService:
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
