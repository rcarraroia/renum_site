"""
Trigger Tasks - Celery tasks for trigger evaluation and execution
Sprint 07A - Integrações Core

Scheduled task that runs every minute to evaluate and execute triggers.
"""

import logging
from celery import Task

from .celery_app import celery_app
from ..services.trigger_service import TriggerService
from ..services.trigger_evaluator import TriggerEvaluator
from ..services.trigger_executor import TriggerExecutor

logger = logging.getLogger(__name__)


class TriggerTask(Task):
    """Base task for trigger operations with automatic retry"""
    
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 2}
    retry_backoff = True
    retry_backoff_max = 300  # 5 minutes max
    retry_jitter = True


@celery_app.task(base=TriggerTask, bind=True, name="trigger_scheduler")
def trigger_scheduler_task(self):
    """
    Scheduled task that evaluates and executes all active triggers.
    
    This task runs every 60 seconds (configured in celery_app.py beat_schedule).
    
    Process:
    1. Load all active triggers from database
    2. For each trigger:
       a. Evaluate condition
       b. If condition met, execute action
       c. Log execution result
       d. Update execution count and timestamp
    
    Returns:
        Dict with execution summary
    """
    try:
        logger.info("Starting trigger scheduler task")
        
        # Initialize services
        trigger_service = TriggerService()
        evaluator = TriggerEvaluator()
        executor = TriggerExecutor()
        
        # Get all active triggers (across all clients)
        # Note: We need to get all clients first
        from ..config.supabase import supabase_admin
        
        clients_result = supabase_admin.table("clients").select("id").eq("status", "active").execute()
        
        if not clients_result.data:
            logger.info("No active clients found")
            return {
                "success": True,
                "triggers_evaluated": 0,
                "triggers_executed": 0
            }
        
        total_evaluated = 0
        total_executed = 0
        
        # Process triggers for each client
        for client in clients_result.data:
            client_id = client["id"]
            
            # Get active triggers for this client
            import asyncio
            triggers = asyncio.run(trigger_service.get_triggers(client_id, active_only=True))
            
            logger.info(f"Found {len(triggers)} active triggers for client {client_id}")
            
            for trigger in triggers:
                total_evaluated += 1
                
                try:
                    # Evaluate condition
                    condition_met = asyncio.run(evaluator.evaluate(trigger))
                    
                    if condition_met:
                        logger.info(f"Trigger {trigger.id} condition met - executing action")
                        
                        # Execute action
                        context = {
                            "trigger_id": str(trigger.id),
                            "client_id": str(client_id)
                        }
                        
                        result = asyncio.run(executor.execute(trigger, context))
                        
                        action_executed = result.get("success", False)
                        
                        if action_executed:
                            total_executed += 1
                            logger.info(f"Trigger {trigger.id} executed successfully")
                        else:
                            logger.warning(f"Trigger {trigger.id} execution failed: {result.get('error')}")
                        
                        # Log execution
                        asyncio.run(trigger_service.log_execution(
                            trigger_id=trigger.id,
                            client_id=client_id,
                            condition_met=True,
                            action_executed=action_executed,
                            result=result
                        ))
                        
                        # Increment execution count
                        asyncio.run(trigger_service.increment_execution_count(trigger.id))
                    
                    else:
                        logger.debug(f"Trigger {trigger.id} condition not met")
                        
                        # Log that condition was not met
                        asyncio.run(trigger_service.log_execution(
                            trigger_id=trigger.id,
                            client_id=client_id,
                            condition_met=False,
                            action_executed=False,
                            result={"message": "Condition not met"}
                        ))
                
                except Exception as e:
                    logger.error(f"Error processing trigger {trigger.id}: {e}")
                    
                    # Log error
                    asyncio.run(trigger_service.log_execution(
                        trigger_id=trigger.id,
                        client_id=client_id,
                        condition_met=False,
                        action_executed=False,
                        result={"error": str(e)}
                    ))
        
        logger.info(f"Trigger scheduler completed: {total_evaluated} evaluated, {total_executed} executed")
        
        return {
            "success": True,
            "triggers_evaluated": total_evaluated,
            "triggers_executed": total_executed
        }
    
    except Exception as e:
        logger.error(f"Error in trigger scheduler task: {e}")
        raise


# Alias for backward compatibility
trigger_scheduler = trigger_scheduler_task
