"""
SICC Models - Sistema de Inteligência Corporativa Contínua
Sprint 10 - SICC Implementation

Pydantic models for SICC (Continuous Corporate Intelligence System).
"""

from .memory import (
    MemoryChunkBase,
    MemoryChunkCreate,
    MemoryChunkUpdate,
    MemoryChunkResponse,
    MemorySearchQuery,
    MemorySearchResult,
    ChunkType
)

from .behavior import (
    BehaviorPatternBase,
    BehaviorPatternCreate,
    BehaviorPatternUpdate,
    BehaviorPatternResponse,
    BehaviorPatternStats,
    PatternType
)

from .learning import (
    LearningLogBase,
    LearningLogCreate,
    LearningLogResponse,
    LearningStatus,
    LearningSource
)

from .snapshot import (
    KnowledgeSnapshotBase,
    KnowledgeSnapshotCreate,
    KnowledgeSnapshotResponse
)

from .metrics import (
    PerformanceMetricBase,
    PerformanceMetricCreate,
    PerformanceMetricResponse,
    MetricType
)

from .settings import (
    LearningSettingsBase,
    LearningSettingsCreate,
    LearningSettingsUpdate,
    LearningSettingsResponse
)

__all__ = [
    # Memory
    "MemoryChunkBase",
    "MemoryChunkCreate",
    "MemoryChunkUpdate",
    "MemoryChunkResponse",
    "MemorySearchQuery",
    "MemorySearchResult",
    
    # Behavior
    "BehaviorPatternBase",
    "BehaviorPatternCreate",
    "BehaviorPatternUpdate",
    "BehaviorPatternResponse",
    "PatternType",
    
    # Learning
    "LearningLogBase",
    "LearningLogCreate",
    "LearningLogResponse",
    "LearningStatus",
    "LearningSource",
    
    # Snapshot
    "KnowledgeSnapshotBase",
    "KnowledgeSnapshotCreate",
    "KnowledgeSnapshotResponse",
    
    # Metrics
    "PerformanceMetricBase",
    "PerformanceMetricCreate",
    "PerformanceMetricResponse",
    "MetricType",
    
    # Settings
    "LearningSettingsBase",
    "LearningSettingsCreate",
    "LearningSettingsUpdate",
    "LearningSettingsResponse",
]
