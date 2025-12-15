"""
Settings Models - Agent Learning Settings
Sprint 10 - SICC Implementation

Models for configuring agent learning behavior and thresholds.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class LearningSettingsBase(BaseModel):
    """Base learning settings model"""
    
    # Auto-approval thresholds
    auto_approve_threshold: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for auto-approval (0-1)"
    )
    
    manual_review_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Confidence threshold requiring manual review (0-1)"
    )
    
    # Consolidation settings
    consolidation_frequency_hours: int = Field(
        default=24,
        ge=1,
        le=168,
        description="Hours between consolidation cycles (1-168)"
    )
    
    min_learnings_for_consolidation: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Minimum learnings before consolidation"
    )
    
    # Memory settings
    max_memory_chunks: int = Field(
        default=10000,
        ge=100,
        le=100000,
        description="Maximum memory chunks per agent"
    )
    
    memory_importance_threshold: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Minimum importance to keep memory (0-1)"
    )
    
    memory_retention_days: int = Field(
        default=365,
        ge=7,
        le=3650,
        description="Days to retain low-importance memories"
    )
    
    # Pattern settings
    max_behavior_patterns: int = Field(
        default=1000,
        ge=10,
        le=10000,
        description="Maximum behavior patterns per agent"
    )
    
    pattern_min_usage_count: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Minimum uses before pattern is considered valid"
    )
    
    pattern_success_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Minimum success rate to keep pattern (0-1)"
    )
    
    # Snapshot settings
    auto_snapshot_enabled: bool = Field(
        default=True,
        description="Whether to create automatic snapshots"
    )
    
    snapshot_frequency_days: int = Field(
        default=7,
        ge=1,
        le=90,
        description="Days between automatic snapshots"
    )
    
    max_snapshots: int = Field(
        default=52,
        ge=5,
        le=365,
        description="Maximum snapshots to retain"
    )
    
    # Learning sources
    learn_from_conversations: bool = Field(
        default=True,
        description="Learn from conversation interactions"
    )
    
    learn_from_documents: bool = Field(
        default=True,
        description="Learn from uploaded documents"
    )
    
    learn_from_feedback: bool = Field(
        default=True,
        description="Learn from user feedback"
    )
    
    learn_from_patterns: bool = Field(
        default=True,
        description="Learn from detected patterns"
    )
    
    # Advanced settings
    embedding_model: str = Field(
        default="gte-small",
        description="Embedding model to use (gte-small, minilm-l6-v2)"
    )
    
    similarity_algorithm: str = Field(
        default="cosine",
        description="Similarity algorithm (cosine, euclidean, dot_product)"
    )
    
    custom_config: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Custom configuration options"
    )
    
    @field_validator('manual_review_threshold')
    @classmethod
    def validate_manual_review_threshold(cls, v: float, info) -> float:
        """Validate manual review threshold is less than auto-approve threshold"""
        auto_approve = info.data.get('auto_approve_threshold')
        if auto_approve and v >= auto_approve:
            raise ValueError("Manual review threshold must be less than auto-approve threshold")
        return v
    
    @field_validator('embedding_model')
    @classmethod
    def validate_embedding_model(cls, v: str) -> str:
        """Validate embedding model is supported"""
        valid_models = ["gte-small", "minilm-l6-v2"]
        if v not in valid_models:
            raise ValueError(f"Embedding model must be one of: {', '.join(valid_models)}")
        return v
    
    @field_validator('similarity_algorithm')
    @classmethod
    def validate_similarity_algorithm(cls, v: str) -> str:
        """Validate similarity algorithm is supported"""
        valid_algorithms = ["cosine", "euclidean", "dot_product"]
        if v not in valid_algorithms:
            raise ValueError(f"Similarity algorithm must be one of: {', '.join(valid_algorithms)}")
        return v


class LearningSettingsCreate(LearningSettingsBase):
    """Model for creating learning settings"""
    
    agent_id: UUID = Field(..., description="Agent ID for these settings")


class LearningSettingsUpdate(BaseModel):
    """Model for updating learning settings (all fields optional)"""
    
    auto_approve_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    manual_review_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    consolidation_frequency_hours: Optional[int] = Field(None, ge=1, le=168)
    min_learnings_for_consolidation: Optional[int] = Field(None, ge=1, le=1000)
    max_memory_chunks: Optional[int] = Field(None, ge=100, le=100000)
    memory_importance_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    memory_retention_days: Optional[int] = Field(None, ge=7, le=3650)
    max_behavior_patterns: Optional[int] = Field(None, ge=10, le=10000)
    pattern_min_usage_count: Optional[int] = Field(None, ge=1, le=100)
    pattern_success_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    auto_snapshot_enabled: Optional[bool] = None
    snapshot_frequency_days: Optional[int] = Field(None, ge=1, le=90)
    max_snapshots: Optional[int] = Field(None, ge=5, le=365)
    learn_from_conversations: Optional[bool] = None
    learn_from_documents: Optional[bool] = None
    learn_from_feedback: Optional[bool] = None
    learn_from_patterns: Optional[bool] = None
    embedding_model: Optional[str] = None
    similarity_algorithm: Optional[str] = None
    custom_config: Optional[Dict[str, Any]] = None
    
    @field_validator('embedding_model')
    @classmethod
    def validate_embedding_model(cls, v: Optional[str]) -> Optional[str]:
        """Validate embedding model if provided"""
        if v is not None:
            valid_models = ["gte-small", "minilm-l6-v2"]
            if v not in valid_models:
                raise ValueError(f"Embedding model must be one of: {', '.join(valid_models)}")
        return v
    
    @field_validator('similarity_algorithm')
    @classmethod
    def validate_similarity_algorithm(cls, v: Optional[str]) -> Optional[str]:
        """Validate similarity algorithm if provided"""
        if v is not None:
            valid_algorithms = ["cosine", "euclidean", "dot_product"]
            if v not in valid_algorithms:
                raise ValueError(f"Similarity algorithm must be one of: {', '.join(valid_algorithms)}")
        return v


class LearningSettingsResponse(LearningSettingsBase):
    """Model for learning settings responses"""
    
    id: UUID = Field(..., description="Unique identifier")
    agent_id: UUID = Field(..., description="Agent ID for these settings")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class LearningSettingsPreset(BaseModel):
    """Model for learning settings presets"""
    
    preset_name: str = Field(..., description="Name of the preset")
    description: str = Field(..., description="Description of this preset")
    settings: LearningSettingsBase = Field(..., description="Settings configuration")
    
    class Config:
        from_attributes = True


# Predefined presets
CONSERVATIVE_PRESET = LearningSettingsPreset(
    preset_name="Conservative",
    description="High thresholds, manual review for most learnings, infrequent consolidation",
    settings=LearningSettingsBase(
        auto_approve_threshold=0.95,
        manual_review_threshold=0.8,
        consolidation_frequency_hours=72,
        min_learnings_for_consolidation=50,
        memory_importance_threshold=0.5,
        pattern_success_threshold=0.7
    )
)

BALANCED_PRESET = LearningSettingsPreset(
    preset_name="Balanced",
    description="Moderate thresholds, balanced automation and review, daily consolidation",
    settings=LearningSettingsBase(
        auto_approve_threshold=0.9,
        manual_review_threshold=0.7,
        consolidation_frequency_hours=24,
        min_learnings_for_consolidation=10,
        memory_importance_threshold=0.3,
        pattern_success_threshold=0.6
    )
)

AGGRESSIVE_PRESET = LearningSettingsPreset(
    preset_name="Aggressive",
    description="Low thresholds, high automation, frequent consolidation",
    settings=LearningSettingsBase(
        auto_approve_threshold=0.85,
        manual_review_threshold=0.6,
        consolidation_frequency_hours=12,
        min_learnings_for_consolidation=5,
        memory_importance_threshold=0.2,
        pattern_success_threshold=0.5
    )
)
