"""
Learning Models - Agent Learning Logs
Sprint 10 - SICC Implementation

Models for tracking agent learning events and approval workflow.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class LearningSource(str, Enum):
    """Sources of learning events"""
    CONVERSATION = "conversation"
    DOCUMENT = "document"
    FEEDBACK = "feedback"
    PATTERN_DETECTION = "pattern_detection"
    ISA_ANALYSIS = "isa_analysis"
    MANUAL_INPUT = "manual_input"
    CONSOLIDATION = "consolidation"


class LearningStatus(str, Enum):
    """Status of learning events"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO_APPROVED = "auto_approved"
    NEEDS_REVIEW = "needs_review"


class LearningLogBase(BaseModel):
    """Base learning log model"""
    
    source: LearningSource = Field(..., description="Source of the learning event")
    learning_type: str = Field(..., min_length=1, max_length=100, description="Type of learning")
    content: Dict[str, Any] = Field(..., description="Learning content and context")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    impact_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Expected impact score")
    status: LearningStatus = Field(default=LearningStatus.PENDING, description="Approval status")
    
    @field_validator('learning_type')
    @classmethod
    def validate_learning_type(cls, v: str) -> str:
        """Validate learning type is not empty"""
        if not v or not v.strip():
            raise ValueError("Learning type cannot be empty")
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content is not empty"""
        if not v:
            raise ValueError("Content cannot be empty")
        return v


class LearningLogCreate(LearningLogBase):
    """Model for creating a new learning log"""
    
    agent_id: UUID = Field(..., description="Agent ID that learned this")
    source_id: Optional[UUID] = Field(None, description="ID of source entity (conversation, document, etc)")


class LearningLogResponse(BaseModel):
    """Model for learning log responses - matches database schema"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID that learned this")
    client_id: UUID = Field(..., description="Client ID")
    learning_type: str = Field(..., description="Type of learning")
    source_data: Dict[str, Any] = Field(..., description="Source data")
    analysis: Dict[str, Any] = Field(..., description="Analysis data")
    action_taken: str = Field(..., description="Action taken")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    status: str = Field(..., description="Status")
    reviewed_by: Optional[UUID] = Field(None, description="User/ISA that reviewed this")
    reviewed_at: Optional[datetime] = Field(None, description="Review timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True


class LearningApproval(BaseModel):
    """Model for approving/rejecting learning"""
    
    status: LearningStatus = Field(..., description="New status (approved/rejected)")
    approved_by: UUID = Field(..., description="User/ISA ID approving this")
    rejection_reason: Optional[str] = Field(None, max_length=1000, description="Reason if rejecting")
    
    @field_validator('rejection_reason')
    @classmethod
    def validate_rejection_reason(cls, v: Optional[str], info) -> Optional[str]:
        """Validate rejection reason is provided when rejecting"""
        status = info.data.get('status')
        if status == LearningStatus.REJECTED and not v:
            raise ValueError("Rejection reason is required when rejecting learning")
        return v


class LearningStats(BaseModel):
    """Model for learning statistics"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    total_learnings: int = Field(default=0, description="Total learning events")
    pending_count: int = Field(default=0, description="Pending approval count")
    approved_count: int = Field(default=0, description="Approved count")
    rejected_count: int = Field(default=0, description="Rejected count")
    auto_approved_count: int = Field(default=0, description="Auto-approved count")
    applied_count: int = Field(default=0, description="Applied to agent count")
    avg_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Average confidence")
    last_learning_at: Optional[datetime] = Field(None, description="Last learning event timestamp")
    
    class Config:
        from_attributes = True


class LearningBatch(BaseModel):
    """Model for batch learning operations"""
    
    learning_ids: list[UUID] = Field(..., min_length=1, description="List of learning IDs to process")
    action: LearningStatus = Field(..., description="Action to apply (approved/rejected)")
    approved_by: UUID = Field(..., description="User/ISA ID performing batch action")
    rejection_reason: Optional[str] = Field(None, max_length=1000, description="Reason if batch rejecting")
    
    @field_validator('learning_ids')
    @classmethod
    def validate_learning_ids(cls, v: list[UUID]) -> list[UUID]:
        """Validate learning IDs list is not empty"""
        if not v:
            raise ValueError("Learning IDs list cannot be empty")
        return v
    
    @field_validator('rejection_reason')
    @classmethod
    def validate_rejection_reason(cls, v: Optional[str], info) -> Optional[str]:
        """Validate rejection reason when batch rejecting"""
        action = info.data.get('action')
        if action == LearningStatus.REJECTED and not v:
            raise ValueError("Rejection reason is required when batch rejecting")
        return v
