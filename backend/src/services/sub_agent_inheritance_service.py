"""
Task 6: Implement sub-agent inheritance system
Create inheritance calculation logic, configuration merging, routing, and activation
Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
"""

from typing import Dict, Any, List
from uuid import UUID
from src.config.supabase import supabase_admin

class SubAgentInheritanceService:
    """Service for managing sub-agent inheritance and configuration merging"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    def calculate_effective_config(
        self,
        parent_config: Dict[str, Any],
        sub_agent_config: Dict[str, Any],
        inheritance_config: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calculate effective configuration by merging parent and sub-agent configs
        based on inheritance rules
        
        Args:
            parent_config: Parent agent's configuration
            sub_agent_config: Sub-agent's own configuration
            inheritance_config: Rules for which categories to inherit
            
        Returns:
            Effective configuration with proper inheritance applied
        """
        effective_config = {}
        
        categories = [
            'instructions', 'intelligence', 'tools', 'integrations',
            'knowledge', 'triggers', 'guardrails'
        ]
        
        for category in categories:
            if inheritance_config.get(category, False):
                # Inherit from parent
                effective_config[category] = self._deep_merge(
                    parent_config.get(category, {}),
                    sub_agent_config.get(category, {})
                )
            else:
                # Use own config
                effective_config[category] = sub_agent_config.get(category, {})
        
        # sub_agents and advanced are never inherited
        effective_config['sub_agents'] = sub_agent_config.get('sub_agents', {})
        effective_config['advanced'] = sub_agent_config.get('advanced', {})
        
        return effective_config
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries, with override taking precedence"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def evaluate_routing_conditions(
        self,
        routing_config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate if sub-agent should be activated based on routing conditions
        
        Args:
            routing_config: Routing rules for the sub-agent
            context: Current conversation context (message, user_profile, etc)
            
        Returns:
            True if sub-agent should be activated
        """
        if not routing_config:
            return False
        
        # Keyword-based activation
        if 'keywords' in routing_config:
            keywords = routing_config['keywords']
            message = context.get('message', '').lower()
            
            if any(keyword.lower() in message for keyword in keywords):
                return True
        
        # User profile-based activation
        if 'user_profile' in routing_config:
            required_profile = routing_config['user_profile']
            user_profile = context.get('user_profile', {})
            
            if all(
                user_profile.get(key) == value
                for key, value in required_profile.items()
            ):
                return True
        
        # Context-based activation
        if 'context_conditions' in routing_config:
            conditions = routing_config['context_conditions']
            
            for condition in conditions:
                field = condition.get('field')
                operator = condition.get('operator')
                value = condition.get('value')
                
                if self._evaluate_condition(
                    context.get(field),
                    operator,
                    value
                ):
                    return True
        
        return False
    
    def _evaluate_condition(
        self,
        actual_value: Any,
        operator: str,
        expected_value: Any
    ) -> bool:
        """Evaluate a single routing condition"""
        if operator == 'equals':
            return actual_value == expected_value
        elif operator == 'contains':
            return expected_value in str(actual_value)
        elif operator == 'greater_than':
            return actual_value > expected_value
        elif operator == 'less_than':
            return actual_value < expected_value
        elif operator == 'in':
            return actual_value in expected_value
        
        return False
    
    def get_active_sub_agents(
        self,
        parent_id: UUID,
        context: Dict[str, Any]
    ) -> List[Dict]:
        """
        Get list of sub-agents that should be activated for current context
        
        Args:
            parent_id: Parent agent ID
            context: Current conversation context
            
        Returns:
            List of active sub-agents with effective configs
        """
        # Get all sub-agents for parent
        result = self.supabase.table('sub_agents')\
            .select('*')\
            .eq('parent_agent_id', str(parent_id))\
            .eq('is_active', True)\
            .execute()
        
        active_sub_agents = []
        
        for sub_agent in result.data:
            # Check if routing conditions are met
            if self.evaluate_routing_conditions(
                sub_agent['routing_config'],
                context
            ):
                # Get parent config
                parent_result = self.supabase.table('agents')\
                    .select('config')\
                    .eq('id', str(parent_id))\
                    .single()\
                    .execute()
                
                parent_config = parent_result.data['config']
                
                # Calculate effective config
                effective_config = self.calculate_effective_config(
                    parent_config,
                    sub_agent['config'],
                    sub_agent['inheritance_config']
                )
                
                active_sub_agents.append({
                    **sub_agent,
                    'effective_config': effective_config
                })
        
        return active_sub_agents

# Singleton
_inheritance_service = None

def get_inheritance_service() -> SubAgentInheritanceService:
    global _inheritance_service
    if _inheritance_service is None:
        _inheritance_service = SubAgentInheritanceService()
    return _inheritance_service
