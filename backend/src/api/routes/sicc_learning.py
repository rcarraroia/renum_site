"""
SICC Learning API Routes - Sprint 10
API endpoints for managing learning logs and approvals
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.sicc.learning import (
    LearningLogCreate,
    LearningLogResponse,
    LearningStatus,
    LearningStats
)
from src.services.sicc.learning_service import LearningService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/sicc/learnings", tags=["sicc-learning"])


@router.get("/", response_model=List[LearningLogResponse])
async def list_learnings(
    agent_id: UUID = Query(..., description="Agent ID"),
    status_filter: Optional[LearningStatus] = Query(None, description="Filter by status"),
    learning_type: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """
    List learning logs for an agent with optional filtering
    
    Returns paginated list of learnings
    """
    learning_service = LearningService()
    
    try:
        learnings = await learning_service.get_pending_learnings(
            agent_id=agent_id,
            learning_type=learning_type,
            limit=limit,
            offset=offset
        )
        
        # Filter by status if provided
        if status_filter:
            learnings = [l for l in learnings if l.status == status_filter]
        
        return learnings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list learnings: {str(e)}"
        )


@router.get("/{learning_id}", response_model=LearningLogResponse)
async def get_learning(
    learning_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning log by ID
    
    Returns learning details
    """
    learning_service = LearningService()
    
    try:
        # Get from database directly
        from src.utils.supabase_client import get_client
        supabase = get_client()
        
        result = supabase.table("learning_logs").select("*").eq("id", str(learning_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning {learning_id} not found"
            )
        
        return LearningLogResponse(**result.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get learning: {str(e)}"
        )


@router.post("/", response_model=LearningLogResponse, status_code=status.HTTP_201_CREATED)
async def create_learning(
    learning_data: LearningLogCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new learning log
    
    Used by ISA to record detected learnings
    """
    learning_service = LearningService()
    
    try:
        learning = await learning_service.create_learning_log(
            agent_id=learning_data.agent_id,
            client_id=learning_data.client_id,
            learning_type=learning_data.learning_type,
            analysis=learning_data.analysis,
            confidence_score=learning_data.confidence_score,
            source_conversation_ids=learning_data.source_conversation_ids
        )
        return learning
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create learning: {str(e)}"
        )


@router.post("/{learning_id}/approve", response_model=LearningLogResponse)
async def approve_learning(
    learning_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Approve learning log
    
    Consolidates learning into memory or pattern
    """
    learning_service = LearningService()
    
    try:
        # Get profile_id from current_user
        profile_id = UUID(current_user.get("id"))
        
        learning = await learning_service.approve_learning(learning_id, profile_id)
        if not learning:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning {learning_id} not found"
            )
        return learning
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to approve learning: {str(e)}"
        )


@router.post("/{learning_id}/reject", response_model=LearningLogResponse)
async def reject_learning(
    learning_id: UUID,
    reason: Optional[str] = Query(None, description="Reason for rejection"),
    current_user: dict = Depends(get_current_user)
):
    """
    Reject learning log
    
    Marks as rejected with optional reason
    """
    learning_service = LearningService()
    
    try:
        # Get profile_id from current_user
        profile_id = UUID(current_user.get("id"))
        
        learning = await learning_service.reject_learning(learning_id, profile_id, reason)
        if not learning:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Learning {learning_id} not found"
            )
        return learning
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject learning: {str(e)}"
        )


@router.post("/batch/approve")
async def batch_approve_learnings(
    learning_ids: List[UUID],
    current_user: dict = Depends(get_current_user)
):
    """
    Approve multiple learnings in batch
    
    Returns count of approved learnings
    """
    learning_service = LearningService()
    
    try:
        # Get profile_id from current_user
        profile_id = UUID(current_user.get("id"))
        
        count = await learning_service.batch_approve(learning_ids, profile_id)
        return {"approved": count, "total": len(learning_ids)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to batch approve learnings: {str(e)}"
        )


@router.post("/batch/reject")
async def batch_reject_learnings(
    learning_ids: List[UUID],
    reason: Optional[str] = Query(None, description="Reason for rejection"),
    current_user: dict = Depends(get_current_user)
):
    """
    Reject multiple learnings in batch
    
    Returns count of rejected learnings
    """
    learning_service = LearningService()
    
    try:
        # Get profile_id from current_user
        profile_id = UUID(current_user.get("id"))
        
        count = await learning_service.batch_reject(learning_ids, profile_id, reason)
        return {"rejected": count, "total": len(learning_ids)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to batch reject learnings: {str(e)}"
        )


@router.get("/agent/{agent_id}/stats", response_model=LearningStats)
async def get_learning_stats(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning statistics for agent
    
    Returns counts by status, type, etc
    """
    learning_service = LearningService()
    
    try:
        stats = await learning_service.get_learning_stats(agent_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get learning stats: {str(e)}"
        )


@router.post("/agent/{agent_id}/analyze")
async def analyze_conversations(
    agent_id: UUID,
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze"),
    current_user: dict = Depends(get_current_user)
):
    """
    Trigger ISA analysis of recent conversations
    
    Returns count of learnings detected
    """
    learning_service = LearningService()
    
    try:
        learnings = await learning_service.analyze_conversations(agent_id, hours)
        return {"detected": len(learnings), "hours": hours}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze conversations: {str(e)}"
        )
