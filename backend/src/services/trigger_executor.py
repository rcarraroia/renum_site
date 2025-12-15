"""
Trigger Executor - Execute trigger actions
Sprint 07A - Integrações Core

Executes actions when trigger conditions are met.
"""

from typing import Dict, Any
from uuid import UUID
import logging

from ..models.trigger import Trigger
from ..config.supabase import supabase_admin

logger = logging.getLogger(__name__)


class TriggerExecutor:
    """Executes trigger actions"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    async def execute(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute trigger action.
        
        Args:
            trigger: Trigger to execute
            context: Execution context
        
        Returns:
            Execution result dict
        """
        try:
            action_type = trigger.action_type
            
            if action_type == "send_message":
                return await self.execute_send_message(trigger, context)
            elif action_type == "send_email":
                return await self.execute_send_email(trigger, context)
            elif action_type == "call_tool":
                return await self.execute_call_tool(trigger, context)
            elif action_type == "change_status":
                return await self.execute_change_status(trigger, context)
            else:
                logger.warning(f"Unknown action type: {action_type}")
                return {
                    "success": False,
                    "error": f"Unknown action type: {action_type}"
                }
                
        except Exception as e:
            logger.error(f"Error executing trigger {trigger.id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_send_message(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute send_message action (WhatsApp).
        
        Args:
            trigger: Trigger
            context: Context with phone and message template
        
        Returns:
            Execution result
        """
        try:
            from ..workers.message_tasks import send_whatsapp_message_task
            
            action_config = trigger.action_config
            
            # Get phone from context or config
            phone = context.get("phone") or action_config.get("phone")
            
            if not phone:
                return {
                    "success": False,
                    "error": "No phone number provided"
                }
            
            # Get message template and replace variables
            message_template = action_config.get("message", "")
            message = self._replace_variables(message_template, context)
            
            # Enqueue Celery task
            task = send_whatsapp_message_task.delay(
                client_id=str(trigger.client_id),
                phone=phone,
                message=message
            )
            
            logger.info(f"Enqueued WhatsApp message task {task.id} for trigger {trigger.id}")
            
            return {
                "success": True,
                "task_id": task.id,
                "phone": phone,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error executing send_message for trigger {trigger.id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_send_email(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute send_email action.
        
        Args:
            trigger: Trigger
            context: Context with email and subject/body templates
        
        Returns:
            Execution result
        """
        try:
            from ..workers.message_tasks import send_email_task
            
            action_config = trigger.action_config
            
            # Get email from context or config
            to_email = context.get("email") or action_config.get("to")
            
            if not to_email:
                return {
                    "success": False,
                    "error": "No email address provided"
                }
            
            # Get subject and body templates
            subject_template = action_config.get("subject", "")
            body_template = action_config.get("body", "")
            
            # Replace variables
            subject = self._replace_variables(subject_template, context)
            body = self._replace_variables(body_template, context)
            
            # Get CC if provided
            cc = action_config.get("cc", [])
            
            # Enqueue Celery task
            task = send_email_task.delay(
                client_id=str(trigger.client_id),
                to=[to_email],
                subject=subject,
                body=body,
                cc=cc if cc else None
            )
            
            logger.info(f"Enqueued email task {task.id} for trigger {trigger.id}")
            
            return {
                "success": True,
                "task_id": task.id,
                "to": to_email,
                "subject": subject
            }
            
        except Exception as e:
            logger.error(f"Error executing send_email for trigger {trigger.id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_call_tool(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute call_tool action (invoke LangChain tool).
        
        Args:
            trigger: Trigger
            context: Context with tool parameters
        
        Returns:
            Execution result
        """
        try:
            action_config = trigger.action_config
            
            tool_name = action_config.get("tool_name")
            tool_params = action_config.get("tool_params", {})
            
            if not tool_name:
                return {
                    "success": False,
                    "error": "No tool_name provided"
                }
            
            # Replace variables in tool params
            resolved_params = {}
            for key, value in tool_params.items():
                if isinstance(value, str):
                    resolved_params[key] = self._replace_variables(value, context)
                else:
                    resolved_params[key] = value
            
            # TODO: Implement tool invocation
            # This would require loading the tool registry and invoking the tool
            # For now, log the action
            
            logger.info(f"Would call tool {tool_name} with params {resolved_params} for trigger {trigger.id}")
            
            return {
                "success": True,
                "tool_name": tool_name,
                "tool_params": resolved_params,
                "note": "Tool invocation not yet implemented"
            }
            
        except Exception as e:
            logger.error(f"Error executing call_tool for trigger {trigger.id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_change_status(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute change_status action (update database record).
        
        Args:
            trigger: Trigger
            context: Context with record ID and new status
        
        Returns:
            Execution result
        """
        try:
            action_config = trigger.action_config
            
            table = action_config.get("table")
            record_id = context.get("record_id") or action_config.get("record_id")
            new_status = action_config.get("status")
            
            if not all([table, record_id, new_status]):
                return {
                    "success": False,
                    "error": "Missing required fields: table, record_id, status"
                }
            
            # Update record in database
            result = self.supabase.table(table).update({
                "status": new_status
            }).eq("id", record_id).execute()
            
            if not result.data:
                return {
                    "success": False,
                    "error": f"Record {record_id} not found in table {table}"
                }
            
            logger.info(f"Changed status of {table}.{record_id} to {new_status} for trigger {trigger.id}")
            
            return {
                "success": True,
                "table": table,
                "record_id": record_id,
                "new_status": new_status
            }
            
        except Exception as e:
            logger.error(f"Error executing change_status for trigger {trigger.id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _replace_variables(self, template: str, context: Dict[str, Any]) -> str:
        """
        Replace variables in template string.
        
        Variables are in format: {{variable_name}} or {{nested.field}}
        
        Args:
            template: Template string with variables
            context: Context dict with variable values
        
        Returns:
            String with variables replaced
        """
        import re
        
        def replace_match(match):
            var_name = match.group(1)
            value = self._get_nested_value(context, var_name)
            return str(value) if value is not None else match.group(0)
        
        return re.sub(r'\{\{([^}]+)\}\}', replace_match, template)
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """
        Get nested value from dict using dot notation.
        
        Args:
            data: Data dict
            path: Path with dots (e.g., "lead.name")
        
        Returns:
            Value or None if not found
        """
        try:
            parts = path.split(".")
            value = data
            
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            
            return value
            
        except Exception:
            return None
