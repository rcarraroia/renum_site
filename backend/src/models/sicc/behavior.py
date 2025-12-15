"""
Behavior Models - Agent Behavior Patterns
Sprint 10 - SICC Implementation

Models for tracking and evolving agent behavioral patterns.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class PatternType(str, Enum):
    """Types of behavior patterns - matches DB constraint"""
    RESPONSE_STRATEGY = "response_strategy"
    TONE_ADJUSTMENT = "tone_adjustment"
    FLOW_OPTIMIZATION = "flow_optimization"
    OBJECTION_HANDLING = "objection_handling"


class BehaviorPatternBase(BaseModel):
    """Base behavior pattern model"""
    
    pattern_type: PatternType = Field(..., description="Type of behavior pattern")
    trigger_context: Dict[str, Any] = Field(..., description="Conditions that trigger this pattern")
    action_config: Dict[str, Any] = Field(..., description="Actions to take when pattern is triggered")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate (0-1)")
    total_applications: int = Field(default=0, ge=0, description="Number of times pattern was used")
    is_active: bool = Field(default=True, description="Whether pattern is currently active")
    
    @field_validator('trigger_context')
    @classmethod
    def validate_trigger_context(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trigger conditions is not empty"""
        if not v:
            raise ValueError("Trigger conditions cannot be empty")
        return v
    
    @field_validator('action_config')
    @classmethod
    def validate_action_config(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate action_config is not empty"""
        if not v:
            raise ValueError("Actions cannot be empty")
        return v


class BehaviorPatternCreate(BehaviorPatternBase):
    """Model for creating a new behavior pattern"""
    
    agent_id: UUID = Field(..., description="Agent ID that owns this pattern")
    client_id: UUID = Field(..., description="Client ID that owns this pattern")


class BehaviorPatternUpdate(BaseModel):
    """Model for updating a behavior pattern"""
    
    trigger_context: Optional[Dict[str, Any]] = None
    action_config: Optional[Dict[str, Any]] = None
    success_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    total_applications: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    
    @field_validator('trigger_context')
    @classmethod
    def validate_trigger_context(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate trigger conditions if provided"""
        if v is not None and not v:
            raise ValueError("Trigger conditions cannot be empty")
        return v
    
    @field_validator('action_config')
    @classmethod
    def validate_action_config(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate action_config if provided"""
        if v is not None and not v:
            raise ValueError("Actions cannot be empty")
        return v


class BehaviorPatternResponse(BehaviorPatternBase):
    """Model for behavior pattern responses"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID that owns this pattern")
    last_used_at: Optional[datetime] = Field(None, description="Last time pattern was used")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class BehaviorPatternStats(BaseModel):
    """Model for behavior pattern statistics"""
    
    pattern_id: UUID = Field(..., description="Pattern ID")
    total_uses: int = Field(default=0, description="Total number of uses")
    successful_applications: int = Field(default=0, description="Number of successful uses")
    failed_uses: int = Field(default=0, description="Number of failed uses")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate")
    avg_last_7_days_uses: int = Field(default=0, description="Uses in last 7 days")
    trend: str = Field(default="stable", description="Usage trend (increasing, decreasing, stable)")
    
    class Config:
        from_attributes = True
