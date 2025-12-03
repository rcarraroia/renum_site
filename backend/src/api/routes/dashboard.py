"""
Dashboard Routes
Sprint 05 - Completar Menus Sidebar

API endpoints for dashboard statistics and metrics
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.api.middleware.auth_middleware import get_current_user
from src.services.dashboard_service import DashboardService
from src.utils.logger import logger


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get dashboard statistics and metrics
    
    Returns aggregated data for:
    - Total clients, leads, conversations
    - Active and completed interviews
    - Completion rate
    - Recent activities
    """
    try:
        service = DashboardService()
        
        # Get client_id if user is not admin
        client_id = None
        if current_user.role != "admin":
            client_id = getattr(current_user, "client_id", None)
        
        stats = service.get_stats(client_id=client_id)
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get dashboard stats: {str(e)}"
        )
