"""
Agent Loader - Sprint 09
Loads agents and sub-agents from database dynamically
"""

from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime

from src.config.supabase import supabase_admin
from src.utils.logger import logger


class AgentRegistry:
    """
    Registry for dynamically loaded agents and sub-agents
    
    Replaces static registry with database-driven approach
    """
    
    def __init__(self):
        """Initialize empty registry"""
        self.agents: Dict[str, dict] = {}  # agent_id -> agent_data
        self.sub_agents: Dict[str, List[dict]] = {}  # agent_id -> [sub_agents]
        self.last_sync: Optional[datetime] = None
        self.supabase = supabase_admin
    
    def load_agents_from_db(self) -> int:
        """
        Load all active agents from database
        
        Returns:
            Number of agents loaded
        """
        try:
            logger.info("Loading agents from database...")
            
            # Query active agents (Orchestrators or Supervisors usually top-level)
            # Unified Agent Model: Agents with parent_id IS NULL are top level?
            # Or filtering by role?
            # Existing logic loads ALL active agents into self.agents?
            # Let's filter by is_active=True.
            agents_response = self.supabase.table('agents')\
                .select('*')\
                .eq('is_active', True)\
                .execute()
            
            if not agents_response.data:
                logger.warning("No active agents found in database")
                self.agents = {}
                self.sub_agents = {}
                self.last_sync = datetime.utcnow()
                return 0
            
            # Clear current registry
            self.agents = {}
            self.sub_agents = {}
            
            # Load each agent
            for agent_data in agents_response.data:
                agent_id = agent_data['id']
                self.agents[agent_id] = agent_data
                
                # Load sub-agents for this agent
                sub_agents = self._load_subagents_for_agent(agent_id)
                self.sub_agents[agent_id] = sub_agents
                
                logger.info(
                    f"Loaded agent {agent_id}: {agent_data['name']} "
                    f"with {len(sub_agents)} sub-agents"
                )
            
            self.last_sync = datetime.utcnow()
            logger.info(f"Successfully loaded {len(self.agents)} agents from database")
            
            return len(self.agents)
            
        except Exception as e:
            logger.error(f"Error loading agents from database: {e}")
            raise
    
    def _load_subagents_for_agent(self, agent_id: str) -> List[dict]:
        """
        Load sub-agents for a specific agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of sub-agent data
        """
        try:
            # Unified Schema: Sub-agents are agents with parent_id = agent_id
            response = self.supabase.table('agents')\
                .select('*')\
                .eq('parent_id', agent_id)\
                .eq('is_active', True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            logger.error(f"Error loading sub-agents for agent {agent_id}: {e}")
            return []
    
    def sync(self) -> Dict[str, int]:
        """
        Sync registry with database
        
        Detects new agents, removed agents, and updated sub-agents
        
        Returns:
            Dict with sync statistics
        """
        try:
            logger.info("Syncing agent registry with database...")
            
            old_agent_ids = set(self.agents.keys())
            
            # Reload from database
            count = self.load_agents_from_db()
            
            new_agent_ids = set(self.agents.keys())
            
            # Calculate changes
            added = new_agent_ids - old_agent_ids
            removed = old_agent_ids - new_agent_ids
            kept = old_agent_ids & new_agent_ids
            
            stats = {
                'total': count,
                'added': len(added),
                'removed': len(removed),
                'kept': len(kept)
            }
            
            if added:
                logger.info(f"Added {len(added)} new agents: {added}")
            if removed:
                logger.info(f"Removed {len(removed)} agents: {removed}")
            
            logger.info(f"Sync complete: {stats}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Error syncing agent registry: {e}")
            raise
    
    def get_agent(self, agent_id: str) -> Optional[dict]:
        """
        Get agent by ID
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent data or None
        """
        return self.agents.get(agent_id)
    
    def get_subagents(self, agent_id: str) -> List[dict]:
        """
        Get sub-agents for an agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of sub-agent data
        """
        return self.sub_agents.get(agent_id, [])
    
    def find_agent_by_slug(self, slug: str) -> Optional[dict]:
        """
        Find agent by slug
        
        Args:
            slug: Agent slug
            
        Returns:
            Agent data or None
        """
        for agent in self.agents.values():
            if agent.get('slug') == slug:
                return agent
        return None
    
    def find_agent_by_client(self, client_id: str) -> List[dict]:
        """
        Find agents by client ID
        
        Args:
            client_id: Client ID
            
        Returns:
            List of agent data
        """
        return [
            agent for agent in self.agents.values()
            if agent.get('client_id') == client_id
        ]
    
    def list_all_agents(self) -> List[dict]:
        """
        List all agents in registry
        
        Returns:
            List of all agent data
        """
        return list(self.agents.values())
    
    def get_stats(self) -> dict:
        """
        Get registry statistics
        
        Returns:
            Dict with statistics
        """
        total_subagents = sum(len(subs) for subs in self.sub_agents.values())
        
        return {
            'total_agents': len(self.agents),
            'total_subagents': total_subagents,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'agents_with_subagents': len([
                agent_id for agent_id, subs in self.sub_agents.items()
                if len(subs) > 0
            ])
        }


# Singleton instance
_agent_registry = None

def get_agent_registry() -> AgentRegistry:
    """Get singleton instance of AgentRegistry"""
    global _agent_registry
    if _agent_registry is None:
        _agent_registry = AgentRegistry()
    return _agent_registry
