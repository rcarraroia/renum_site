"""
SICC Patterns API Routes - Sprint 10
API endpoints for managing behavioral patterns
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.models.sicc.behavior import (
    BehaviorPatternCreate,
    BehaviorPatternUpdate,
    BehaviorPatternResponse,
    PatternType
)
from src.services.sicc.behavior_service import BehaviorService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/sicc/patterns", tags=["sicc-patterns"])


@router.get("/", response_model=List[BehaviorPatternResponse])
async def list_patterns(
    agent_id: UUID = Query(..., description="Agent ID"),
    pattern_type: Optional[PatternType] = Query(None, description="Filter by type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    min_success_rate: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum success rate"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """
    List behavioral patterns for an agent with optional filtering
    
    Returns paginated list of patterns
    """
    behavior_service = BehaviorService()
    
    try:
        patterns = await behavior_service.list_patterns(
            agent_id=agent_id,
            pattern_type=pattern_type,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        
        # Filter by success rate if provided
        if min_success_rate is not None:
            patterns = [
                p for p in patterns
                if p.success_rate and p.success_rate >= min_success_rate
            ]
        
        return patterns
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list patterns: {str(e)}"
        )


@router.get("/{pattern_id}", response_model=BehaviorPatternResponse)
async def get_pattern(
    pattern_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get pattern by ID
    
    Returns pattern details
    """
    behavior_service = BehaviorService()
    
    try:
        pattern = await behavior_service.get_pattern(pattern_id)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pattern {pattern_id} not found"
            )
        return pattern
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pattern: {str(e)}"
        )


@router.post("/", response_model=BehaviorPatternResponse, status_code=status.HTTP_201_CREATED)
async def create_pattern(
    pattern_data: BehaviorPatternCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new behavioral pattern
    
    Used to manually add patterns or by ISA
    """
    behavior_service = BehaviorService()
    
    try:
        pattern = await behavior_service.create_pattern(pattern_data)
        return pattern
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pattern: {str(e)}"
        )


@router.put("/{pattern_id}", response_model=BehaviorPatternResponse)
async def update_pattern(
    pattern_id: UUID,
    pattern_data: BehaviorPatternUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update behavioral pattern
    
    Can modify trigger context, action config, or active status
    """
    behavior_service = BehaviorService()
    
    try:
        pattern = await behavior_service.update_pattern(pattern_id, pattern_data)
        if not pattern:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pattern {pattern_id} not found"
            )
        return pattern
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update pattern: {str(e)}"
        )


@router.delete("/{pattern_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pattern(
    pattern_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete pattern
    
    Soft delete (marks as inactive)
    """
    behavior_service = BehaviorService()
    
    try:
        success = await behavior_service.delete_pattern(pattern_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pattern {pattern_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete pattern: {str(e)}"
        )


@router.post("/{pattern_id}/record-application")
async def record_pattern_application(
    pattern_id: UUID,
    success: bool = Query(..., description="Whether application was successful"),
    current_user: dict = Depends(get_current_user)
):
    """
    Record pattern application result
    
    Updates success rate and application count
    """
    behavior_service = BehaviorService()
    
    try:
        await behavior_service.record_application(pattern_id, success)
        return {"pattern_id": str(pattern_id), "success": success, "recorded": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record application: {str(e)}"
        )


class PatternSearchRequest(BaseModel):
    """Request model for pattern search"""
    agent_id: UUID
    context: Dict[str, Any]
    min_confidence: float = 0.6


@router.post("/search")
async def search_patterns(
    search_request: PatternSearchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for matching patterns
    
    Returns patterns that match given context
    """
    behavior_service = BehaviorService()
    
    try:
        patterns = await behavior_service.find_matching_patterns(
            agent_id=search_request.agent_id,
            context=search_request.context,
            min_confidence=search_request.min_confidence
        )
        return {
            "agent_id": str(search_request.agent_id),
            "matches": len(patterns),
            "patterns": patterns
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search patterns: {str(e)}"
        )


@router.get("/agent/{agent_id}/stats")
async def get_pattern_stats(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get pattern statistics for agent
    
    Returns counts by type, success rates, etc
    """
    behavior_service = BehaviorService()
    
    try:
        # Get all patterns
        patterns = await behavior_service.list_patterns(
            agent_id=agent_id,
            is_active=True,
            limit=1000,
            offset=0
        )
        
        # Calculate stats
        total = len(patterns)
        by_type = {}
        total_applications = 0
        avg_success_rate = 0.0
        
        for pattern in patterns:
            # Count by type
            type_key = pattern.pattern_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            # Sum applications
            total_applications += pattern.application_count
            
            # Sum success rates
            if pattern.success_rate:
                avg_success_rate += pattern.success_rate
        
        if total > 0:
            avg_success_rate /= total
        
        return {
            "agent_id": str(agent_id),
            "total_patterns": total,
            "by_type": by_type,
            "total_applications": total_applications,
            "average_success_rate": avg_success_rate
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pattern stats: {str(e)}"
        )
