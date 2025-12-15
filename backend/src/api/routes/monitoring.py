from fastapi import APIRouter, Depends
from typing import Dict, Any

from src.api.dependencies import get_current_user
from src.services.monitoring_service import get_monitoring_service, MonitoringService

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
async def get_monitoring_stats(
    current_user: dict = Depends(get_current_user),
    service: MonitoringService = Depends(get_monitoring_service)
):
    """
    Get high-level monitoring statistics from LangSmith.
    Requires authentication.
    """
    return await service.get_stats()
