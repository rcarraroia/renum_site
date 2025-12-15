"""
Report Service
Sprint 08 - Conexao Backend

Service for generating reports and analytics
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from src.utils.supabase_client import get_client
from src.utils.logger import logger


class ReportService:
    """Service for reports and analytics"""
    
    def __init__(self):
        self.client = get_client()
    
    def get_overview(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get overview metrics
        
        Args:
            filters: Dictionary with optional filters (start_date, end_date, client_id, project_id)
        
        Returns:
            Dictionary with overview metrics
        """
        try:
            # Count leads
            leads_query = self.client.table('leads').select('*', count='exact')
            if filters.get('client_id'):
                leads_query = leads_query.eq('client_id', filters['client_id'])
            total_leads = leads_query.execute().count or 0
            
            # Count clients
            clients_query = self.client.table('clients').select('*', count='exact')
            total_clients = clients_query.execute().count or 0
            
            # Count conversations
            conversations_query = self.client.table('conversations').select('*', count='exact')
            if filters.get('client_id'):
                conversations_query = conversations_query.eq('client_id', filters['client_id'])
            total_conversations = conversations_query.execute().count or 0
            
            # Count interviews
            interviews_query = self.client.table('interviews').select('*', count='exact')
            total_interviews = interviews_query.execute().count or 0
            
            # Count active projects
            projects_query = self.client.table('projects')\
                .select('*', count='exact')\
                .eq('status', 'active')
            if filters.get('client_id'):
                projects_query = projects_query.eq('client_id', filters['client_id'])
            active_projects = projects_query.execute().count or 0
            
            # Calculate conversion rate (completed interviews / total interviews)
            completed_interviews = self.client.table('interviews')\
                .select('*', count='exact')\
                .eq('status', 'completed')\
                .execute().count or 0
            
            conversion_rate = (completed_interviews / total_interviews * 100) if total_interviews > 0 else 0
            
            return {
                "totalLeads": total_leads,
                "totalClients": total_clients,
                "totalConversations": total_conversations,
                "totalInterviews": total_interviews,
                "activeProjects": active_projects,
                "conversionRate": round(conversion_rate, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting overview: {e}")
            raise
    
    def get_agent_performance(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get agent performance metrics
        
        Args:
            filters: Dictionary with optional filters
        
        Returns:
            List of agent performance data
        """
        try:
            # For now, return mock data
            # TODO: Implement real agent performance tracking
            return [
                {
                    "agentId": "agent-1",
                    "agentName": "RENUS Base",
                    "totalConversations": 150,
                    "avgResponseTime": 2.5,
                    "satisfactionScore": 4.5
                },
                {
                    "agentId": "agent-2",
                    "agentName": "RENUS MMN",
                    "totalConversations": 89,
                    "avgResponseTime": 3.1,
                    "satisfactionScore": 4.2
                },
                {
                    "agentId": "agent-3",
                    "agentName": "RENUS Clinica",
                    "totalConversations": 67,
                    "avgResponseTime": 2.8,
                    "satisfactionScore": 4.7
                }
            ]
            
        except Exception as e:
            logger.error(f"Error getting agent performance: {e}")
            raise
    
    def get_conversion_funnel(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get conversion funnel data
        
        Args:
            filters: Dictionary with optional filters
        
        Returns:
            List of funnel stages with counts and conversion rates
        """
        try:
            # Count leads at each stage
            total_leads = self.client.table('leads')\
                .select('*', count='exact')\
                .execute().count or 0
            
            # Total conversations (as proxy for engagement)
            total_conversations = self.client.table('conversations')\
                .select('*', count='exact')\
                .execute().count or 0
            
            # Total interviews
            total_interviews = self.client.table('interviews')\
                .select('*', count='exact')\
                .execute().count or 0
            
            # Completed interviews
            completed_interviews = self.client.table('interviews')\
                .select('*', count='exact')\
                .eq('status', 'completed')\
                .execute().count or 0
            
            # Build funnel
            funnel = [
                {
                    "stage": "Total Leads",
                    "count": total_leads,
                    "conversionRate": 100.0
                },
                {
                    "stage": "Engaged (Conversations)",
                    "count": total_conversations,
                    "conversionRate": round((total_conversations / total_leads * 100) if total_leads > 0 else 0, 2)
                },
                {
                    "stage": "Interviewed",
                    "count": total_interviews,
                    "conversionRate": round((total_interviews / total_leads * 100) if total_leads > 0 else 0, 2)
                },
                {
                    "stage": "Completed",
                    "count": completed_interviews,
                    "conversionRate": round((completed_interviews / total_leads * 100) if total_leads > 0 else 0, 2)
                }
            ]
            
            return funnel
            
        except Exception as e:
            logger.error(f"Error getting conversion funnel: {e}")
            raise
