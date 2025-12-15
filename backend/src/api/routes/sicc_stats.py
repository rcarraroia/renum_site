"""
SICC Stats API Routes - Sprint 10
API endpoints for statistics and metrics
"""

from typing import Optional
from uuid import UUID
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.sicc.metrics import MetricsPeriod, MetricsResponse
from src.services.sicc.metrics_service import MetricsService
from src.services.sicc.snapshot_service import SnapshotService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/sicc/stats", tags=["sicc-stats"])


@router.get("/agent/{agent_id}/metrics")
async def get_agent_metrics(
    agent_id: UUID,
    period: MetricsPeriod = Query(MetricsPeriod.LAST_7_DAYS, description="Time period"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get metrics for agent
    
    Returns time-series metrics for specified period
    """
    metrics_service = MetricsService()
    
    try:
        metrics = await metrics_service.get_metrics(agent_id, period)
        return {"agent_id": str(agent_id), "period": period.value, "metrics": metrics}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )


@router.get("/agent/{agent_id}/aggregated")
async def get_aggregated_metrics(
    agent_id: UUID,
    period: MetricsPeriod = Query(MetricsPeriod.LAST_30_DAYS, description="Time period"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get aggregated metrics for agent
    
    Returns summary statistics for specified period
    """
    metrics_service = MetricsService()
    
    try:
        aggregated = await metrics_service.get_aggregated_metrics(agent_id, period)
        return aggregated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get aggregated metrics: {str(e)}"
        )


@router.get("/agent/{agent_id}/learning-velocity")
async def get_learning_velocity(
    agent_id: UUID,
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning velocity for agent
    
    Returns learnings per day over specified period
    """
    metrics_service = MetricsService()
    
    try:
        velocity = await metrics_service.calculate_learning_velocity(agent_id, days)
        return {
            "agent_id": str(agent_id),
            "days": days,
            "velocity": velocity,
            "unit": "learnings/day"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate learning velocity: {str(e)}"
        )


@router.get("/agent/{agent_id}/evolution")
async def get_agent_evolution(
    agent_id: UUID,
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get agent evolution over time
    
    Returns timeline of memories, patterns, and learnings
    """
    metrics_service = MetricsService()
    snapshot_service = SnapshotService()
    
    try:
        # Get metrics for period
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get snapshots
        snapshots = await snapshot_service.get_agent_snapshots(agent_id, limit=days)
        
        # Get aggregated metrics
        aggregated = await metrics_service.get_aggregated_metrics(
            agent_id,
            MetricsPeriod.LAST_30_DAYS if days <= 30 else MetricsPeriod.LAST_90_DAYS
        )
        
        # Get learning velocity
        velocity = await metrics_service.calculate_learning_velocity(agent_id, days)
        
        return {
            "agent_id": str(agent_id),
            "period": {"start": str(start_date), "end": str(end_date), "days": days},
            "snapshots": [
                {
                    "date": str(s.created_at.date()),
                    "memories_count": s.memories_count,
                    "patterns_count": s.patterns_count,
                    "total_interactions": s.total_interactions,
                    "success_rate": s.success_rate
                }
                for s in snapshots
            ],
            "aggregated": aggregated,
            "learning_velocity": velocity
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent evolution: {str(e)}"
        )


@router.get("/agent/{agent_id}/top-memories")
async def get_top_memories(
    agent_id: UUID,
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get top memories by usage
    
    Returns most frequently used memories
    """
    from src.services.sicc.memory_service import MemoryService
    memory_service = MemoryService()
    
    try:
        # Get all memories for agent
        memories = await memory_service.list_memories(
            agent_id=agent_id,
            is_active=True,
            limit=100,
            offset=0
        )
        
        # Sort by usage_count
        sorted_memories = sorted(
            memories,
            key=lambda m: m.usage_count,
            reverse=True
        )[:limit]
        
        return {
            "agent_id": str(agent_id),
            "top_memories": [
                {
                    "id": str(m.id),
                    "type": m.chunk_type.value,
                    "content": m.content[:100] + "..." if len(m.content) > 100 else m.content,
                    "usage_count": m.usage_count,
                    "confidence": m.confidence,
                    "last_used_at": str(m.last_used_at) if m.last_used_at else None
                }
                for m in sorted_memories
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get top memories: {str(e)}"
        )


@router.get("/agent/{agent_id}/active-patterns")
async def get_active_patterns(
    agent_id: UUID,
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get active behavioral patterns
    
    Returns patterns with success rates
    """
    from src.services.sicc.behavior_service import BehaviorService
    behavior_service = BehaviorService()
    
    try:
        # Get all patterns for agent
        patterns = await behavior_service.list_patterns(
            agent_id=agent_id,
            is_active=True,
            limit=100,
            offset=0
        )
        
        # Sort by success_rate
        sorted_patterns = sorted(
            patterns,
            key=lambda p: p.success_rate if p.success_rate else 0,
            reverse=True
        )[:limit]
        
        return {
            "agent_id": str(agent_id),
            "active_patterns": [
                {
                    "id": str(p.id),
                    "type": p.pattern_type.value,
                    "trigger_context": p.trigger_context,
                    "success_rate": p.success_rate,
                    "application_count": p.application_count,
                    "confidence": p.confidence
                }
                for p in sorted_patterns
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active patterns: {str(e)}"
        )


@router.get("/agent/{agent_id}/dashboard")
async def get_dashboard_stats(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get comprehensive dashboard statistics
    
    Returns all key metrics for agent overview
    """
    metrics_service = MetricsService()
    
    try:
        from src.services.sicc.memory_service import MemoryService
        from src.services.sicc.behavior_service import BehaviorService
        from src.services.sicc.learning_service import LearningService
        
        memory_service = MemoryService()
        behavior_service = BehaviorService()
        learning_service = LearningService()
        
        # Get counts
        memory_stats = await memory_service.get_memory_stats(agent_id)
        learning_stats = await learning_service.get_learning_stats(agent_id)
        
        # Get aggregated metrics
        aggregated = await metrics_service.get_aggregated_metrics(
            agent_id,
            MetricsPeriod.LAST_30_DAYS
        )
        
        # Get learning velocity
        velocity = await metrics_service.calculate_learning_velocity(agent_id, 30)
        
        return {
            "agent_id": str(agent_id),
            "memories": memory_stats,
            "learnings": learning_stats,
            "performance": aggregated,
            "learning_velocity": velocity
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard stats: {str(e)}"
        )
