from langsmith import Client
from datetime import datetime, timedelta
from typing import Dict, Any, List
from ..config.settings import settings
from ..utils.logger import logger

class MonitoringService:
    """Service to interact with LangSmith API for monitoring and observability."""
    
    def __init__(self):
        try:
            self.client = Client(api_key=settings.LANGSMITH_API_KEY)
            self.project_name = settings.LANGSMITH_PROJECT
            self.is_active = True
        except Exception as e:
            logger.error(f"Failed to initialize LangSmith client: {e}")
            self.is_active = False

    async def get_stats(self) -> Dict[str, Any]:
        """
        Fetches high-level statistics for the project from LangSmith.
        Returns total runs, error rate, and recent runs.
        """
        if not self.is_active:
            return {"status": "disabled", "message": "LangSmith client not initialized"}

        try:
            # List recent runs to calculate stats
            # Note: list_runs returns an iterator. We fetch last 100 for a quick snapshot.
            runs = list(self.client.list_runs(
                project_name=self.project_name, 
                execution_order=1, # Descending
                limit=100
            ))
            
            total_runs = len(runs)
            error_runs = len([r for r in runs if r.error])
            
            # Simple stats based on the last 100 runs
            # Ideally we would use client.read_project(project_name=...) for aggregate stats if available
            
            recent_display = []
            for r in runs[:10]: # Top 10 most recent
                latency = 0.0
                if r.end_time and r.start_time:
                    latency = (r.end_time - r.start_time).total_seconds()
                
                recent_display.append({
                    "id": str(r.id),
                    "name": r.name,
                    "status": "error" if r.error else "success",
                    "error": str(r.error) if r.error else None,
                    "tokens": r.total_tokens if hasattr(r, 'total_tokens') else 0,
                    "latency": round(latency, 2),
                    "timestamp": r.start_time.isoformat() if r.start_time else None
                })

            return {
                "status": "active",
                "project": self.project_name,
                "stats_window": "Last 100 runs",
                "total_runs_in_window": total_runs,
                "error_count": error_runs,
                "error_rate": round((error_runs / total_runs * 100), 2) if total_runs > 0 else 0,
                "success_rate": round(((total_runs - error_runs) / total_runs * 100), 2) if total_runs > 0 else 100,
                "recent_runs": recent_display
            }
            
        except Exception as e:
            logger.error(f"Error fetching LangSmith stats: {e}")
            return {"status": "error", "message": str(e)}

_monitoring_service = None

def get_monitoring_service() -> MonitoringService:
    global _monitoring_service
    if not _monitoring_service:
        _monitoring_service = MonitoringService()
    return _monitoring_service
