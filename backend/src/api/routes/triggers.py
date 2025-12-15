"""
Triggers API Routes
Sprint 07A - Integrações Core

API endpoints for managing automation triggers.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID

from ...models.trigger import (
    Trigger,
    TriggerCreate,
    TriggerUpdate,
    TriggerTestResult
)
from ...services.trigger_service import TriggerService
from ...services.trigger_evaluator import TriggerEvaluator
from ...services.trigger_executor import TriggerExecutor
from ...middleware.auth import get_current_user, get_current_client_id

router = APIRouter(prefix="/triggers", tags=["triggers"])


@router.post("/", response_model=Trigger, status_code=status.HTTP_201_CREATED)
async def create_trigger(
    trigger_data: TriggerCreate,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """
    Create a new automation trigger.
    
    Triggers can be time-based or event-based.
    """
    try:
        trigger = await service.create_trigger(client_id, trigger_data)
        return trigger
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create trigger: {str(e)}"
        )


@router.get("/", response_model=List[Trigger])
async def get_triggers(
    active_only: bool = False,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """
    Get all triggers for the current client.
    
    Query params:
    - active_only: If true, only return active triggers
    """
    triggers = await service.get_triggers(client_id, active_only=active_only)
    return triggers


@router.get("/{trigger_id}", response_model=Trigger)
async def get_trigger(
    trigger_id: UUID,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """Get a specific trigger by ID"""
    trigger = await service.get_trigger(trigger_id)
    
    if not trigger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trigger not found"
        )
    
    # Verify ownership
    if str(trigger.client_id) != str(client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return trigger


@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(
    trigger_id: UUID,
    trigger_data: TriggerUpdate,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """Update a trigger configuration"""
    # Verify ownership
    existing = await service.get_trigger(trigger_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trigger not found"
        )
    
    if str(existing.client_id) != str(client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        trigger = await service.update_trigger(trigger_id, trigger_data)
        return trigger
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update trigger: {str(e)}"
        )


@router.delete("/{trigger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trigger(
    trigger_id: UUID,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """Delete a trigger"""
    # Verify ownership
    existing = await service.get_trigger(trigger_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trigger not found"
        )
    
    if str(existing.client_id) != str(client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        await service.delete_trigger(trigger_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete trigger: {str(e)}"
        )


@router.patch("/{trigger_id}/toggle", response_model=Trigger)
async def toggle_trigger(
    trigger_id: UUID,
    active: bool,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends()
):
    """
    Toggle trigger active status.
    
    Body:
    - active: true to activate, false to deactivate
    """
    # Verify ownership
    existing = await service.get_trigger(trigger_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trigger not found"
        )
    
    if str(existing.client_id) != str(client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        trigger = await service.toggle_trigger(trigger_id, active)
        return trigger
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to toggle trigger: {str(e)}"
        )


@router.post("/{trigger_id}/test", response_model=TriggerTestResult)
async def test_trigger(
    trigger_id: UUID,
    client_id: UUID = Depends(get_current_client_id),
    service: TriggerService = Depends(),
    evaluator: TriggerEvaluator = Depends(),
    executor: TriggerExecutor = Depends()
):
    """
    Test a trigger (simulate execution).
    
    Evaluates condition and executes action without waiting for scheduled time.
    Does not increment execution count or update last_executed_at.
    """
    # Verify ownership
    trigger = await service.get_trigger(trigger_id)
    if not trigger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trigger not found"
        )
    
    if str(trigger.client_id) != str(client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        # Evaluate condition
        condition_met = await evaluator.evaluate(trigger)
        
        result = {
            "success": True,
            "condition_met": condition_met,
            "action_executed": False,
            "action_result": None
        }
        
        if condition_met:
            # Execute action
            context = {
                "trigger_id": str(trigger_id),
                "client_id": str(client_id),
                "test_mode": True
            }
            
            action_result = await executor.execute(trigger, context)
            
            result["action_executed"] = action_result.get("success", False)
            result["action_result"] = action_result
        
        return TriggerTestResult(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test trigger: {str(e)}"
        )
