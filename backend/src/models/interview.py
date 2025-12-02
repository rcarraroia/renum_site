"""
Interview models for Discovery Agent MVP
Sprint 04 - Discovery Agent
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
import re


# ============================================================================
# REQUEST MODELS
# ============================================================================

class InterviewCreate(BaseModel):
    """Request to create new interview"""
    # No fields needed - system creates automatically
    pass


class MessageRequest(BaseModel):
    """Request to send message to interview"""
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=2000,
        description="Message content from user"
    )
    
    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        """Validate content is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty or whitespace only')
        return v.strip()


# ============================================================================
# DATABASE MODELS
# ============================================================================

class InterviewMessage(BaseModel):
    """Interview message (from database)"""
    id: UUID
    interview_id: UUID
    role: str  # 'user', 'assistant', or 'system'
    content: str
    timestamp: datetime
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is one of allowed values"""
        allowed_roles = {'user', 'assistant', 'system'}
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {allowed_roles}')
        return v


class Interview(BaseModel):
    """Interview model (from database)"""
    id: UUID
    lead_id: Optional[UUID] = None
    subagent_id: Optional[UUID] = None
    
    # Collected data fields
    contact_name: Optional[str] = None
    email: Optional[str] = None
    contact_phone: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    experience_level: Optional[str] = None
    operation_size: Optional[str] = None
    
    # Metadata
    status: str  # 'in_progress', 'completed', 'abandoned'
    started_at: datetime
    completed_at: Optional[datetime] = None
    topics_covered: Optional[List[str]] = None
    ai_analysis: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is one of allowed values"""
        allowed_statuses = {'in_progress', 'completed', 'abandoned'}
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate email format if provided"""
        if v is None:
            return v
        
        # Basic email validation (@ and domain)
        email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('contact_phone')
    @classmethod
    def validate_phone_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone format if provided (international format)"""
        if v is None:
            return v
        
        # Phone must start with + and contain only digits after
        phone_pattern = r'^\+\d{10,15}$'
        if not re.match(phone_pattern, v):
            raise ValueError('Phone must be in international format: +[country_code][number]')
        return v


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class InterviewProgress(BaseModel):
    """Progress tracking for interview"""
    collected: int = Field(..., ge=0, le=7, description="Number of fields collected")
    total: int = Field(default=7, description="Total fields to collect")
    missing_fields: List[str] = Field(default_factory=list, description="List of missing field names")
    percentage: int = Field(..., ge=0, le=100, description="Completion percentage")
    
    @field_validator('percentage', mode='before')
    @classmethod
    def calculate_percentage(cls, v, info):
        """Calculate percentage from collected/total"""
        # If percentage is already provided, use it
        if isinstance(v, int):
            return v
        
        # Otherwise calculate from collected and total
        data = info.data
        collected = data.get('collected', 0)
        total = data.get('total', 7)
        
        if total == 0:
            return 0
        
        return int((collected / total) * 100)


class AIAnalysis(BaseModel):
    """AI-generated analysis of completed interview"""
    summary: str = Field(..., description="Summary of the interview")
    lead_quality: str = Field(..., description="Quality assessment: high, medium, or low")
    pain_points: List[str] = Field(default_factory=list, description="Main pain points identified")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for next steps")
    generated_at: datetime = Field(default_factory=datetime.now, description="When analysis was generated")
    
    @field_validator('lead_quality')
    @classmethod
    def validate_lead_quality(cls, v: str) -> str:
        """Validate lead quality is one of allowed values"""
        allowed_qualities = {'high', 'medium', 'low'}
        if v.lower() not in allowed_qualities:
            raise ValueError(f'Lead quality must be one of: {allowed_qualities}')
        return v.lower()


class InterviewDetail(BaseModel):
    """Interview with messages and progress"""
    interview: Interview
    messages: List[InterviewMessage]
    progress: InterviewProgress


class MessageResponse(BaseModel):
    """Response after processing user message"""
    user_message: InterviewMessage
    agent_response: InterviewMessage
    fields_updated: List[str] = Field(default_factory=list, description="Fields that were updated")
    is_complete: bool = Field(default=False, description="Whether interview is complete")
    progress: InterviewProgress


class InterviewListItem(BaseModel):
    """Simplified interview for list view"""
    id: UUID
    contact_name: Optional[str] = None
    email: Optional[str] = None
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    # Computed field
    duration_minutes: Optional[int] = None
    
    model_config = {"from_attributes": True}


class InterviewListResponse(BaseModel):
    """Response for list of interviews"""
    interviews: List[InterviewListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# AGENT RESPONSE MODEL
# ============================================================================

class AgentResponse(BaseModel):
    """Response from Discovery Agent"""
    message: str = Field(..., description="Agent's response message")
    extracted_fields: dict = Field(default_factory=dict, description="Fields extracted from conversation")
    is_complete: bool = Field(default=False, description="Whether all required fields are collected")
    next_question: Optional[str] = Field(None, description="Next question to ask (if not complete)")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_interview_progress(interview: Interview) -> InterviewProgress:
    """
    Calculate progress for an interview
    
    Args:
        interview: Interview object
        
    Returns:
        InterviewProgress with collected count and missing fields
    """
    required_fields = [
        'contact_name',
        'email', 
        'contact_phone',
        'country',
        'company',
        'experience_level',
        'operation_size'
    ]
    
    collected = 0
    missing = []
    
    for field in required_fields:
        value = getattr(interview, field, None)
        if value is not None and value != '':
            collected += 1
        else:
            missing.append(field)
    
    percentage = int((collected / len(required_fields)) * 100)
    
    return InterviewProgress(
        collected=collected,
        total=len(required_fields),
        missing_fields=missing,
        percentage=percentage
    )


def is_interview_complete(interview: Interview) -> bool:
    """
    Check if interview has all required fields
    
    Args:
        interview: Interview object
        
    Returns:
        True if all required fields are filled, False otherwise
    """
    progress = calculate_interview_progress(interview)
    return progress.collected == progress.total
