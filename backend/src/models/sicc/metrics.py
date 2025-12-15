"""
Metrics Models - Agent Performance Metrics
Sprint 10 - SICC Implementation

Models for tracking agent performance and quality metrics.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class MetricType(str, Enum):
    """Types of performance metrics"""
    RESPONSE_QUALITY = "response_quality"
    CONVERSATION_SUCCESS = "conversation_success"
    USER_SATISFACTION = "user_satisfaction"
    CONVERSION_RATE = "conversion_rate"
    RESPONSE_TIME = "response_time"
    ACCURACY = "accuracy"
    ENGAGEMENT = "engagement"
    RETENTION = "retention"


class PerformanceMetricBase(BaseModel):
    """Base performance metric model"""
    
    metric_type: MetricType = Field(..., description="Type of metric")
    metric_value: float = Field(..., description="Metric value")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Context for this metric")
    period_start: datetime = Field(..., description="Start of measurement period")
    period_end: datetime = Field(..., description="End of measurement period")
    sample_size: int = Field(default=1, ge=1, description="Number of samples in this metric")
    
    @field_validator('metric_value')
    @classmethod
    def validate_metric_value(cls, v: float) -> float:
        """Validate metric value is not negative for most metrics"""
        if v < 0:
            raise ValueError("Metric value cannot be negative")
        return v
    
    @field_validator('period_end')
    @classmethod
    def validate_period_end(cls, v: datetime, info) -> datetime:
        """Validate period end is after period start"""
        period_start = info.data.get('period_start')
        if period_start and v < period_start:
            raise ValueError("Period end must be after period start")
        return v


class PerformanceMetricCreate(PerformanceMetricBase):
    """Model for creating a new performance metric"""
    
    agent_id: UUID = Field(..., description="Agent ID for this metric")
    source_id: Optional[UUID] = Field(None, description="ID of source entity (conversation, etc)")


class PerformanceMetricResponse(PerformanceMetricBase):
    """Model for performance metric responses"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID for this metric")
    source_id: Optional[UUID] = Field(None, description="ID of source entity")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True


class MetricAggregation(BaseModel):
    """Model for aggregated metrics"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    metric_type: MetricType = Field(..., description="Type of metric")
    period_start: datetime = Field(..., description="Start of aggregation period")
    period_end: datetime = Field(..., description="End of aggregation period")
    avg_value: float = Field(..., description="Average metric value")
    min_value: float = Field(..., description="Minimum metric value")
    max_value: float = Field(..., description="Maximum metric value")
    total_samples: int = Field(..., description="Total number of samples")
    std_deviation: Optional[float] = Field(None, description="Standard deviation")
    trend: str = Field(default="stable", description="Trend (improving, declining, stable)")
    
    class Config:
        from_attributes = True


class AgentPerformanceSummary(BaseModel):
    """Model for comprehensive agent performance summary"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    period_start: datetime = Field(..., description="Start of summary period")
    period_end: datetime = Field(..., description="End of summary period")
    
    # Quality metrics
    avg_response_quality: float = Field(default=0.0, ge=0.0, le=1.0, description="Average response quality")
    avg_user_satisfaction: float = Field(default=0.0, ge=0.0, le=1.0, description="Average user satisfaction")
    avg_accuracy: float = Field(default=0.0, ge=0.0, le=1.0, description="Average accuracy")
    
    # Performance metrics
    total_conversations: int = Field(default=0, description="Total conversations")
    successful_conversations: int = Field(default=0, description="Successful conversations")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate")
    avg_response_time_ms: float = Field(default=0.0, description="Average response time in ms")
    
    # Engagement metrics
    avg_engagement_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Average engagement")
    retention_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="User retention rate")
    
    # Learning metrics
    total_learnings: int = Field(default=0, description="Total learning events")
    applied_learnings: int = Field(default=0, description="Applied learning events")
    
    # Trends
    quality_trend: str = Field(default="stable", description="Quality trend")
    performance_trend: str = Field(default="stable", description="Performance trend")
    engagement_trend: str = Field(default="stable", description="Engagement trend")
    
    # Overall score
    overall_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall performance score")
    
    class Config:
        from_attributes = True


class MetricQuery(BaseModel):
    """Model for querying metrics"""
    
    agent_id: UUID = Field(..., description="Agent ID to query metrics for")
    metric_types: Optional[list[MetricType]] = Field(None, description="Filter by metric types")
    period_start: Optional[datetime] = Field(None, description="Start of query period")
    period_end: Optional[datetime] = Field(None, description="End of query period")
    aggregation: str = Field(default="none", description="Aggregation type (none, hourly, daily, weekly, monthly)")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")
    
    @field_validator('aggregation')
    @classmethod
    def validate_aggregation(cls, v: str) -> str:
        """Validate aggregation type"""
        valid_aggregations = ["none", "hourly", "daily", "weekly", "monthly"]
        if v not in valid_aggregations:
            raise ValueError(f"Aggregation must be one of: {', '.join(valid_aggregations)}")
        return v



class MetricsPeriod(str, Enum):
    """Metrics period enumeration"""
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"


class MetricsCreate(BaseModel):
    """Model for creating metrics (simplified for SICC)"""
    
    agent_id: UUID = Field(..., description="Agent ID")
    client_id: UUID = Field(..., description="Client ID")
    metric_date: str = Field(..., description="Date for metrics")


class MetricsUpdate(BaseModel):
    """Model for updating metrics"""
    
    total_interactions: Optional[int] = Field(None, description="Total interactions")
    successful_interactions: Optional[int] = Field(None, description="Successful interactions")
    avg_response_time_ms: Optional[int] = Field(None, description="Average response time")
    user_satisfaction_score: Optional[float] = Field(None, description="User satisfaction score")


class MetricsResponse(BaseModel):
    """Model for metrics responses (matches database schema)"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID")
    client_id: UUID = Field(..., description="Client ID")
    metric_date: str = Field(..., description="Date for metrics")
    total_interactions: int = Field(default=0, description="Total interactions")
    successful_interactions: int = Field(default=0, description="Successful interactions")
    avg_response_time_ms: Optional[int] = Field(None, description="Average response time in ms")
    user_satisfaction_score: Optional[float] = Field(None, description="User satisfaction score (0.0-5.0)")
    conversion_rate: Optional[float] = Field(None, description="Conversion rate")
    memory_chunks_used: int = Field(default=0, description="Memory chunks used")
    patterns_applied: int = Field(default=0, description="Patterns applied")
    new_learnings: int = Field(default=0, description="New learnings")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
