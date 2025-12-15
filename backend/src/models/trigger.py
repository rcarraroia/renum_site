"""
Trigger Models - Sprint 07A
Pydantic models for automation triggers (WHEN → IF → THEN)
"""

from datetime import datetime
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from uuid import UUID


class TriggerBase(BaseModel):
    """Base model for trigger"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    active: bool = True
    
    # WHEN (Trigger Event)
    trigger_type: Literal['time_based', 'event_based', 'condition_based']
    trigger_config: Dict[str, Any] = Field(default_factory=dict)
    
    # IF (Condition)
    condition_type: Optional[Literal['field_equals', 'field_contains', 'time_elapsed', 'always', 'field_greater_than', 'field_less_than']] = 'always'
    condition_config: Dict[str, Any] = Field(default_factory=dict)
    
    # THEN (Action)
    action_type: Literal['send_message', 'send_email', 'call_tool', 'change_status', 'notify_team']
    action_config: Dict[str, Any] = Field(default_factory=dict)


class TriggerCreate(TriggerBase):
    """Model for creating trigger"""
    client_id: UUID


class TriggerUpdate(BaseModel):
    """Model for updating trigger"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    active: Optional[bool] = None
    trigger_config: Optional[Dict[str, Any]] = None
    condition_config: Optional[Dict[str, Any]] = None
    action_config: Optional[Dict[str, Any]] = None


class Trigger(TriggerBase):
    """Model for trigger response"""
    id: UUID
    client_id: UUID
    last_executed_at: Optional[datetime] = None
    execution_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TriggerExecution(BaseModel):
    """Model for trigger execution log"""
    id: UUID
    trigger_id: UUID
    client_id: UUID
    executed_at: datetime
    condition_met: bool
    action_executed: bool
    result: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TriggerTestResult(BaseModel):
    """Result of trigger simulation/test"""
    success: bool
    simulation: Dict[str, Any]
    message: str


# Helper classes for trigger evaluation
class TriggerCondition(BaseModel):
    """Condition to evaluate"""
    field: str
    operator: Literal['equals', 'not_equals', 'contains', 'not_contains', 'greater_than', 'less_than', 'greater_or_equal', 'less_or_equal']
    value: Any


class TriggerAction(BaseModel):
    """Action to execute"""
    type: Literal['send_message', 'send_email', 'call_tool', 'change_status', 'notify_team']
    config: Dict[str, Any]


class TriggerStatus(BaseModel):
    """Status of trigger execution"""
    trigger_id: UUID
    active: bool
    last_executed_at: Optional[datetime]
    execution_count: int
    last_error: Optional[str] = None
