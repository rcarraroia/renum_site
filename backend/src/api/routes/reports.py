"""
Reports Routes
Sprint 08 - Conexao Backend

API endpoints for reports and analytics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.api.middleware.auth_middleware import get_current_user
from src.services.report_service import ReportService
from src.utils.logger import logger


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/overview")
async def get_overview(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get overview metrics
    
    Returns:
    - totalLeads
    - totalClients
    - totalConversations
    - totalInterviews
    - activeProjects
    - conversionRate
    """
    try:
        service = ReportService()
        
        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "client_id": client_id,
            "project_id": project_id
        }
        
        overview = service.get_overview(filters)
        return overview
        
    except Exception as e:
        logger.error(f"Error getting overview: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get overview: {str(e)}"
        )


@router.get("/agents")
async def get_agent_performance(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    agent_type: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Get agent performance metrics
    
    Returns list of:
    - agentId
    - agentName
    - totalConversations
    - avgResponseTime
    - satisfactionScore
    """
    try:
        service = ReportService()
        
        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "client_id": client_id,
            "agent_type": agent_type
        }
        
        performance = service.get_agent_performance(filters)
        return performance
        
    except Exception as e:
        logger.error(f"Error getting agent performance: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent performance: {str(e)}"
        )


@router.get("/conversions")
async def get_conversion_funnel(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Get conversion funnel data
    
    Returns list of:
    - stage
    - count
    - conversionRate
    """
    try:
        service = ReportService()
        
        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "client_id": client_id,
            "project_id": project_id
        }
        
        funnel = service.get_conversion_funnel(filters)
        return funnel
        
    except Exception as e:
        logger.error(f"Error getting conversion funnel: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversion funnel: {str(e)}"
        )


@router.get("/export")
async def export_data(
    format: str = Query("csv", regex="^(csv|excel)$"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Export report data to CSV or Excel
    
    Returns file download
    """
    try:
        service = ReportService()
        
        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "client_id": client_id
        }
        
        # For now, return a simple message
        # TODO: Implement actual file export
        return {
            "message": f"Export to {format} not yet implemented",
            "filters": filters
        }
        
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export data: {str(e)}"
        )
