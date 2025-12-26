"""
SICC Services - Sistema de Inteligência Corporativa Contínua
Sprint 10 - SICC Implementation
Sprint SICC Multi-Agente - Hook universal para todos os agentes

Business logic services for SICC functionality.
"""

from .embedding_service import EmbeddingService, get_embedding_service
from .memory_service import MemoryService
from .behavior_service import BehaviorService
from .snapshot_service import SnapshotService
from .metrics_service import MetricsService
from .learning_service import LearningService
from .agent_orchestrator import AgentOrchestrator, get_agent_orchestrator
from .sicc_hook import SiccHook, get_sicc_hook
from .analyzer_service import SiccAnalyzer

__all__ = [
    "EmbeddingService",
    "get_embedding_service",
    "MemoryService",
    "BehaviorService",
    "SnapshotService",
    "MetricsService",
    "LearningService",
    "AgentOrchestrator",
    "get_agent_orchestrator",
    # SICC Multi-Agente
    "SiccHook",
    "get_sicc_hook",
    "SiccAnalyzer",
]
