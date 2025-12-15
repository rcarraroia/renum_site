
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from src.utils.logger import logger
from src.config.supabase import supabase_admin
from src.services.integration_service import IntegrationService
from src.integrations.uazapi_connector import UazapiConnector
from src.integrations.google_connector import GoogleConnector

class TriggerService:
    """Service to evaluate and execute automation triggers"""

    async def evaluate_triggers(self, agent: Any, context: Dict[str, Any], event_type: str = "on_message_received"):
        """
        Evaluate configured triggers against current context.
        """
        # Ensure config is dict
        agent_config = agent.config if isinstance(agent.config, dict) else {}
        
        if 'triggers' not in agent_config:
            return

        triggers = agent_config['triggers']
        if not isinstance(triggers, list):
            return

        for trigger in triggers:
            # 1. Check Event Type
            if trigger.get('event') != event_type:
                continue

            # 2. Check Conditions
            if self._check_conditions(trigger.get('conditions', []), context):
                # 3. Execute Actions
                await self._execute_actions(trigger.get('actions', []), agent, context)

    def _check_conditions(self, conditions: List[Dict], context: Dict) -> bool:
        """Check if all conditions are met"""
        for condition in conditions:
            field = condition.get('field')
            operator = condition.get('operator')
            value = condition.get('value')
            
            # Resolve field value from context
            context_value = self._get_context_value(context, field)

            if not self._evaluate_condition(context_value, operator, value):
                return False
        
        return True

    def _get_context_value(self, context: Dict, path: str) -> Any:
        """Helper to get deep value from dict"""
        if not path:
            return None
        parts = path.split('.')
        current = context
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def _evaluate_condition(self, actual: Any, operator: str, expected: Any) -> bool:
        """Evaluate single condition"""
        if operator == 'equals':
            return str(actual).lower() == str(expected).lower()
        elif operator == 'contains':
            return str(expected).lower() in str(actual).lower()
        elif operator == 'not_contains':
            return str(expected).lower() not in str(actual).lower()
        return False

    async def _execute_actions(self, actions: List[Dict], agent: Any, context: Dict):
        """Execute defined actions"""
        client_id = str(agent.client_id) if hasattr(agent, 'client_id') and agent.client_id else None
        
        for action in actions:
            action_type = action.get('type')
            params = action.get('params', {})
            
            logger.info(f"Executing trigger action: {action_type} for agent {agent.id}")

            try:
                if action_type == 'send_message':
                    await self._action_send_message(agent, context, params, client_id)
                elif action_type == 'add_tag':
                    await self._action_add_tag(context, params)
                elif action_type == 'google_action':
                    await self._action_google_execute(agent, params, client_id)
                elif action_type == 'chatwoot_handoff':
                     # Potential explicit action for handoff via trigger
                     # For now, maybe just log or create specific method later
                     pass
            except Exception as e:
                logger.error(f"Error executing trigger action {action_type}: {e}")

    async def _action_send_message(self, agent: Any, context: Dict, params: Dict, client_id: Optional[str]):
        """Action: Send a message to the conversation AND External Channel"""
        interview_id = context.get('interview_id')
        message = params.get('message')
        # Try to get phone number from context if available
        remote_jid = context.get('remote_jid') # e.g., '5511999999999@s.whatsapp.net'
        
        if interview_id and message:
            # 1. Store in Database (History)
            msg_data = {
                'interview_id': interview_id,
                'role': 'assistant',
                'content': message,
                'timestamp': datetime.now().isoformat(),
                'metadata': {'source': 'automation_trigger'}
            }
            supabase_admin.table('interview_messages').insert(msg_data).execute()

            # 2. Send to Uazapi (Real World) if configured
            if client_id and remote_jid:
                svc = IntegrationService(client_id=client_id)
                integration = svc.get_integration('uazapi', str(agent.id))
                
                if integration and integration.get('config'):
                     try:
                         conn = UazapiConnector(integration['config'])
                         # Extract plain phone from remote_jid if needed by connector
                         # remote_jid usually format: 554799998888@s.whatsapp.net
                         # conn.send_message expects '554799998888' usually or full JID depending on impl.
                         # let's assume connector handles JID or we strip
                         identifier = remote_jid.split('@')[0]
                         logger.info(f"Trigger dispatching Uazapi message to {identifier}")
                         conn.send_message(identifier, message)
                     except Exception as ex:
                         logger.error(f"Failed to dispatch Uazapi message in trigger: {ex}")

    async def _action_add_tag(self, context: Dict, params: Dict):
        """Action: Add a tag to the interview"""
        tag = params.get('tag')
        interview_id = context.get('interview_id')
        if interview_id and tag:
            logger.info(f"Tagging interview {interview_id} with {tag}")
            # Implementation would update a tags column or table
            # supabase_admin.table('interviews').update({'tags': ...})...
            pass

    async def _action_google_execute(self, agent: Any, params: Dict, client_id: Optional[str]):
        """Action: Execute a Google Action (Send Email, etc.)"""
        action_subtype = params.get('subtype') # e.g. 'send_email'
        
        if not client_id:
            logger.warning("Google Action skipped: No Client ID context")
            return

        svc = IntegrationService(client_id=client_id)
        integration = svc.get_integration('google', str(agent.id))
        
        if not integration or not integration.get('config'):
             logger.warning(f"Google Action skipped: Agent {agent.id} has no Google integration")
             return

        conn = GoogleConnector(integration['config'])

        if action_subtype == 'send_email':
            to = params.get('to')
            subject = params.get('subject')
            body = params.get('body')
            if to and subject and body:
                 conn.send_email(to, subject, body)
                 logger.info(f"Trigger sent email to {to}")

trigger_service = TriggerService()
