"""
Dashboard Service
Sprint 05 - Completar Menus Sidebar

Service for aggregating dashboard statistics and metrics
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.utils.supabase_client import get_client
from src.utils.logger import logger


class DashboardService:
    """Service for dashboard statistics and metrics"""
    
    def __init__(self):
        self.client = get_client()
    
    def get_stats(self, client_id: str = None) -> Dict[str, Any]:
        """
        Get dashboard statistics
        
        Args:
            client_id: Optional client ID for filtering (multi-tenant)
        
        Returns:
            Dictionary with aggregated statistics
        """
        try:
            # Count clients
            clients_query = self.client.table('clients').select('*', count='exact')
            if client_id:
                clients_query = clients_query.eq('id', client_id)
            clients_count = clients_query.execute().count or 0
            
            # Count leads
            leads_query = self.client.table('leads').select('*', count='exact')
            if client_id:
                leads_query = leads_query.eq('client_id', client_id)
            leads_count = leads_query.execute().count or 0
            
            # Count active conversations
            conversations_query = self.client.table('conversations')\
                .select('*', count='exact')\
                .eq('status', 'active')
            if client_id:
                conversations_query = conversations_query.eq('client_id', client_id)
            conversations_count = conversations_query.execute().count or 0
            
            # Count active interviews
            active_interviews_query = self.client.table('interviews')\
                .select('*', count='exact')\
                .eq('status', 'in_progress')
            active_interviews = active_interviews_query.execute().count or 0
            
            # Count completed interviews
            completed_interviews_query = self.client.table('interviews')\
                .select('*', count='exact')\
                .eq('status', 'completed')
            completed_interviews = completed_interviews_query.execute().count or 0
            
            # Calculate completion rate
            total_interviews = active_interviews + completed_interviews
            completion_rate = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
            
            # Get recent activities
            recent_activities = self._get_recent_activities(client_id)
            
            return {
                "total_clients": clients_count,
                "total_leads": leads_count,
                "total_conversations": conversations_count,
                "active_interviews": active_interviews,
                "completed_interviews": completed_interviews,
                "completion_rate": round(completion_rate, 2),
                "recent_activities": recent_activities
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            raise
    
    def _get_recent_activities(self, client_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activities from various tables"""
        activities = []
        
        try:
            # Recent conversations
            conversations_query = self.client.table('conversations')\
                .select('id, created_at, status')\
                .order('created_at', desc=True)\
                .limit(5)
            if client_id:
                conversations_query = conversations_query.eq('client_id', client_id)
            
            conversations = conversations_query.execute().data or []
            
            for conv in conversations:
                activities.append({
                    "type": "conversation",
                    "action": "created",
                    "timestamp": conv["created_at"],
                    "details": f"Conversa {conv['status']}"
                })
            
            # Recent interviews
            interviews = self.client.table('interviews')\
                .select('id, created_at, status')\
                .order('created_at', desc=True)\
                .limit(5)\
                .execute().data or []
            
            for interview in interviews:
                activities.append({
                    "type": "interview",
                    "action": "created",
                    "timestamp": interview["created_at"],
                    "details": f"Entrevista {interview['status']}"
                })
            
            # Sort by timestamp and return top N
            activities.sort(key=lambda x: x["timestamp"], reverse=True)
            return activities[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent activities: {e}")
            return []
