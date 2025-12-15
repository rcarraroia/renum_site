"""
Trigger Evaluator - Evaluate trigger conditions
Sprint 07A - Integrações Core

Evaluates whether trigger conditions are met.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from ..models.trigger import Trigger
from ..config.supabase import supabase_admin

logger = logging.getLogger(__name__)


class TriggerEvaluator:
    """Evaluates trigger conditions"""
    
    def __init__(self):
        self.supabase = supabase_admin
    
    async def evaluate(
        self,
        trigger: Trigger,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Evaluate if trigger condition is met.
        
        Args:
            trigger: Trigger to evaluate
            context: Optional context data (for event-based triggers)
        
        Returns:
            True if condition is met, False otherwise
        """
        try:
            # Check trigger type
            if trigger.trigger_type == "time_based":
                return await self.evaluate_time_based(trigger)
            elif trigger.trigger_type == "event_based":
                return await self.evaluate_event_based(trigger, context)
            else:
                logger.warning(f"Unknown trigger type: {trigger.trigger_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error evaluating trigger {trigger.id}: {e}")
            return False
    
    async def evaluate_time_based(self, trigger: Trigger) -> bool:
        """
        Evaluate time-based trigger.
        
        Time-based triggers check if enough time has passed since last execution.
        
        Args:
            trigger: Trigger to evaluate
        
        Returns:
            True if time condition is met
        """
        try:
            config = trigger.trigger_config
            interval_minutes = config.get("interval_minutes", 60)
            
            # If never executed, condition is met
            if not trigger.last_executed_at:
                logger.info(f"Time-based trigger {trigger.id} never executed - condition met")
                return True
            
            # Check if enough time has passed
            last_executed = datetime.fromisoformat(trigger.last_executed_at.replace('Z', '+00:00'))
            now = datetime.utcnow()
            elapsed = (now - last_executed).total_seconds() / 60  # minutes
            
            condition_met = elapsed >= interval_minutes
            
            if condition_met:
                logger.info(f"Time-based trigger {trigger.id} condition met ({elapsed:.1f} >= {interval_minutes} minutes)")
            
            return condition_met
            
        except Exception as e:
            logger.error(f"Error evaluating time-based trigger {trigger.id}: {e}")
            return False
    
    async def evaluate_event_based(
        self,
        trigger: Trigger,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Evaluate event-based trigger.
        
        Event-based triggers check database state or context data.
        
        Args:
            trigger: Trigger to evaluate
            context: Event context data
        
        Returns:
            True if event condition is met
        """
        try:
            config = trigger.trigger_config
            event_type = config.get("event_type")
            
            if event_type == "conversation_status_change":
                return await self._evaluate_conversation_status(trigger, context)
            elif event_type == "lead_score_threshold":
                return await self._evaluate_lead_score(trigger, context)
            elif event_type == "interview_completed":
                return await self._evaluate_interview_completed(trigger, context)
            else:
                logger.warning(f"Unknown event type: {event_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error evaluating event-based trigger {trigger.id}: {e}")
            return False
    
    async def evaluate_condition(
        self,
        trigger: Trigger,
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate trigger condition against context data.
        
        Supports operators: equals, contains, greater_than, less_than
        
        Args:
            trigger: Trigger to evaluate
            context: Context data to evaluate against
        
        Returns:
            True if condition is met
        """
        try:
            condition_type = trigger.condition_type
            condition_config = trigger.condition_config
            
            if condition_type == "always":
                return True
            
            if condition_type == "field_comparison":
                field = condition_config.get("field")
                operator = condition_config.get("operator")
                value = condition_config.get("value")
                
                # Get field value from context
                field_value = self._get_nested_field(context, field)
                
                if field_value is None:
                    return False
                
                # Evaluate operator
                if operator == "equals":
                    return field_value == value
                elif operator == "not_equals":
                    return field_value != value
                elif operator == "contains":
                    return value in str(field_value)
                elif operator == "greater_than":
                    return float(field_value) > float(value)
                elif operator == "less_than":
                    return float(field_value) < float(value)
                elif operator == "greater_or_equal":
                    return float(field_value) >= float(value)
                elif operator == "less_or_equal":
                    return float(field_value) <= float(value)
                else:
                    logger.warning(f"Unknown operator: {operator}")
                    return False
            
            logger.warning(f"Unknown condition type: {condition_type}")
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating condition for trigger {trigger.id}: {e}")
            return False
    
    def _get_nested_field(self, data: Dict[str, Any], field_path: str) -> Any:
        """
        Get nested field value from dict using dot notation.
        
        Example: "conversation.status" -> data["conversation"]["status"]
        
        Args:
            data: Data dict
            field_path: Field path with dots
        
        Returns:
            Field value or None if not found
        """
        try:
            parts = field_path.split(".")
            value = data
            
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None
            
            return value
            
        except Exception:
            return None
    
    async def _evaluate_conversation_status(
        self,
        trigger: Trigger,
        context: Optional[Dict[str, Any]]
    ) -> bool:
        """Evaluate conversation status change event"""
        if not context or "conversation_id" not in context:
            return False
        
        conversation_id = context["conversation_id"]
        
        # Fetch conversation from database
        result = self.supabase.table("conversations").select("*").eq("id", conversation_id).execute()
        
        if not result.data:
            return False
        
        conversation = result.data[0]
        
        # Evaluate condition against conversation data
        return await self.evaluate_condition(trigger, {"conversation": conversation})
    
    async def _evaluate_lead_score(
        self,
        trigger: Trigger,
        context: Optional[Dict[str, Any]]
    ) -> bool:
        """Evaluate lead score threshold event"""
        if not context or "lead_id" not in context:
            return False
        
        lead_id = context["lead_id"]
        
        # Fetch lead from database
        result = self.supabase.table("leads").select("*").eq("id", lead_id).execute()
        
        if not result.data:
            return False
        
        lead = result.data[0]
        
        # Evaluate condition against lead data
        return await self.evaluate_condition(trigger, {"lead": lead})
    
    async def _evaluate_interview_completed(
        self,
        trigger: Trigger,
        context: Optional[Dict[str, Any]]
    ) -> bool:
        """Evaluate interview completed event"""
        if not context or "interview_id" not in context:
            return False
        
        interview_id = context["interview_id"]
        
        # Fetch interview from database
        result = self.supabase.table("interviews").select("*").eq("id", interview_id).execute()
        
        if not result.data:
            return False
        
        interview = result.data[0]
        
        # Check if interview is completed
        if interview.get("status") != "completed":
            return False
        
        # Evaluate additional conditions if any
        return await self.evaluate_condition(trigger, {"interview": interview})
