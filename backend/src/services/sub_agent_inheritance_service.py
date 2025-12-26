"""
Task 6: Implement sub-agent inheritance system
Create inheritance calculation logic, configuration merging, routing, and activation
Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
"""

from typing import Dict, Any, List
from uuid import UUID
from src.config.supabase import supabase_admin
from src.utils.logger import logger

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
    
    def get_inherited_integrations(
        self,
        parent_agent_id: UUID,
        sub_agent_config: Dict[str, Any],
        inheritance_config: Dict[str, bool]
    ) -> Dict[str, Any]:
        """
        Calcula integrações efetivas com herança do agente pai
        
        Args:
            parent_agent_id: ID do agente pai
            sub_agent_config: Configuração do sub-agente
            inheritance_config: Regras de herança
            
        Returns:
            Configurações de integração efetivas
        """
        try:
            # Buscar integrações do agente pai
            parent_integrations = self._get_parent_integrations(parent_agent_id)
            
            # Configurações próprias do sub-agente
            sub_integrations = sub_agent_config.get('integrations', {})
            
            # Se herança de integrações está habilitada
            if inheritance_config.get('integrations', True):
                # Herdar todas as integrações do pai
                effective_integrations = self._deep_merge(
                    parent_integrations,
                    sub_integrations
                )
                
                # Aplicar rate limits específicos para sub-agentes
                effective_integrations = self._apply_sub_agent_limits(
                    effective_integrations,
                    sub_agent_config
                )
            else:
                # Usar apenas configurações próprias
                effective_integrations = sub_integrations
            
            return effective_integrations
            
        except Exception as e:
            logger.error(f"Error calculating inherited integrations: {e}")
            return sub_agent_config.get('integrations', {})
    
    def _get_parent_integrations(self, parent_agent_id: UUID) -> Dict[str, Any]:
        """Busca integrações do agente pai"""
        try:
            # Mock de integrações do agente pai
            # Em produção, buscar da tabela de integrações
            return {
                'whatsapp': {
                    'enabled': True,
                    'api_url': 'https://api.whatsapp.com',
                    'credentials': {
                        'token': 'parent_token',
                        'phone_number': '+5511999999999'
                    },
                    'rate_limit': {
                        'max_requests': 1000,
                        'period_seconds': 3600
                    }
                },
                'email': {
                    'enabled': True,
                    'provider': 'smtp',
                    'credentials': {
                        'smtp_host': 'smtp.gmail.com',
                        'smtp_port': 587,
                        'username': 'parent@example.com',
                        'password': 'parent_password'
                    },
                    'rate_limit': {
                        'max_requests': 500,
                        'period_seconds': 3600
                    }
                },
                'calendar': {
                    'enabled': True,
                    'provider': 'google',
                    'credentials': {
                        'api_key': 'parent_api_key',
                        'calendar_id': 'primary'
                    },
                    'rate_limit': {
                        'max_requests': 200,
                        'period_seconds': 3600
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting parent integrations: {e}")
            return {}
    
    def _apply_sub_agent_limits(
        self,
        integrations: Dict[str, Any],
        sub_agent_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aplica limites específicos para sub-agentes"""
        try:
            # Rate limits reduzidos para sub-agentes (50% do pai)
            sub_agent_multiplier = sub_agent_config.get('rate_limit_multiplier', 0.5)
            
            for integration_name, integration_config in integrations.items():
                if 'rate_limit' in integration_config:
                    original_limit = integration_config['rate_limit']['max_requests']
                    new_limit = int(original_limit * sub_agent_multiplier)
                    
                    integration_config['rate_limit']['max_requests'] = max(new_limit, 10)  # Mínimo 10
                    
                    # Adicionar identificação de sub-agente
                    integration_config['sub_agent_mode'] = True
                    integration_config['parent_agent_id'] = sub_agent_config.get('parent_agent_id')
            
            return integrations
            
        except Exception as e:
            logger.error(f"Error applying sub-agent limits: {e}")
            return integrations
    
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
