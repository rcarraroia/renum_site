"""
Metrics Service - Agent Performance Metrics Management
Sprint 10 - SICC Implementation

Service for recording and aggregating agent performance metrics.
"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, date, timedelta

from ...config.supabase import supabase_admin
from ...models.sicc.metrics import (
    MetricsCreate,
    MetricsUpdate,
    MetricsResponse,
    MetricsPeriod
)
from ...utils.logger import logger


class MetricsService:
    """Service for managing agent performance metrics"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = supabase_admin
    
    async def record_interaction(
        self,
        agent_id: UUID,
        client_id: UUID,
        success: bool,
        response_time_ms: Optional[int] = None,
        satisfaction_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MetricsResponse:
        """
        Record an agent interaction and update daily metrics.
        
        Args:
            agent_id: Agent ID
            client_id: Client ID
            success: Whether interaction was successful
            response_time_ms: Response time in milliseconds
            satisfaction_score: User satisfaction score (0.0-5.0)
            metadata: Additional metadata
        
        Returns:
            MetricsResponse with updated metrics
        """
        try:
            today = date.today()
            
            logger.info(
                f"Recording interaction for agent {agent_id}: "
                f"success={success}, response_time={response_time_ms}ms"
            )
            
            # Get or create today's metrics
            result = self.supabase.table("agent_performance_metrics").select("*").eq(
                "agent_id", str(agent_id)
            ).eq("metric_date", today.isoformat()).execute()
            
            if result.data:
                # Update existing metrics
                current = result.data[0]
                
                new_total = current["total_interactions"] + 1
                new_successful = current["successful_interactions"] + (1 if success else 0)
                
                # Calculate new average response time
                if response_time_ms is not None:
                    current_avg = current.get("avg_response_time_ms")
                    if current_avg is not None:
                        new_avg_response = int(
                            (current_avg * current["total_interactions"] + response_time_ms) / new_total
                        )
                    else:
                        new_avg_response = response_time_ms
                else:
                    new_avg_response = current.get("avg_response_time_ms")
                
                # Calculate new average satisfaction
                if satisfaction_score is not None:
                    current_sat = current.get("user_satisfaction_score")
                    if current_sat is not None:
                        new_avg_satisfaction = (
                            (current_sat * current["total_interactions"] + satisfaction_score) / new_total
                        )
                    else:
                        new_avg_satisfaction = satisfaction_score
                else:
                    new_avg_satisfaction = current.get("user_satisfaction_score")
                
                # Merge metadata
                current_metadata = current.get("metadata", {})
                if metadata:
                    current_metadata.update(metadata)
                
                update_data = {
                    "total_interactions": new_total,
                    "successful_interactions": new_successful,
                    "avg_response_time_ms": new_avg_response,
                    "user_satisfaction_score": new_avg_satisfaction,
                    "metadata": current_metadata
                }
                
                updated = self.supabase.table("agent_performance_metrics").update(
                    update_data
                ).eq("id", current["id"]).execute()
                
                return MetricsResponse(**updated.data[0])
            
            else:
                # Create new metrics for today
                metrics_data = {
                    "agent_id": str(agent_id),
                    "client_id": str(client_id),
                    "metric_date": today.isoformat(),
                    "total_interactions": 1,
                    "successful_interactions": 1 if success else 0,
                    "avg_response_time_ms": response_time_ms,
                    "user_satisfaction_score": satisfaction_score,
                    "metadata": metadata or {}
                }
                
                created = self.supabase.table("agent_performance_metrics").insert(
                    metrics_data
                ).execute()
                
                return MetricsResponse(**created.data[0])
            
        except Exception as e:
            logger.error(f"Failed to record interaction: {e}")
            raise
    
    async def increment_memory_usage(
        self,
        agent_id: UUID,
        count: int = 1
    ) -> None:
        """
        Increment memory chunks used counter for today.
        
        Args:
            agent_id: Agent ID
            count: Number of memories used
        """
        try:
            today = date.today()
            
            result = self.supabase.table("agent_performance_metrics").select("*").eq(
                "agent_id", str(agent_id)
            ).eq("metric_date", today.isoformat()).execute()
            
            if result.data:
                current = result.data[0]
                new_count = current["memory_chunks_used"] + count
                
                self.supabase.table("agent_performance_metrics").update({
                    "memory_chunks_used": new_count
                }).eq("id", current["id"]).execute()
            
        except Exception as e:
            logger.warning(f"Failed to increment memory usage: {e}")
    
    async def increment_pattern_application(
        self,
        agent_id: UUID,
        count: int = 1
    ) -> None:
        """
        Increment patterns applied counter for today.
        
        Args:
            agent_id: Agent ID
            count: Number of patterns applied
        """
        try:
            today = date.today()
            
            result = self.supabase.table("agent_performance_metrics").select("*").eq(
                "agent_id", str(agent_id)
            ).eq("metric_date", today.isoformat()).execute()
            
            if result.data:
                current = result.data[0]
                new_count = current["patterns_applied"] + count
                
                self.supabase.table("agent_performance_metrics").update({
                    "patterns_applied": new_count
                }).eq("id", current["id"]).execute()
            
        except Exception as e:
            logger.warning(f"Failed to increment pattern application: {e}")
    
    async def increment_new_learnings(
        self,
        agent_id: UUID,
        count: int = 1
    ) -> None:
        """
        Increment new learnings counter for today.
        
        Args:
            agent_id: Agent ID
            count: Number of new learnings
        """
        try:
            today = date.today()
            
            result = self.supabase.table("agent_performance_metrics").select("*").eq(
                "agent_id", str(agent_id)
            ).eq("metric_date", today.isoformat()).execute()
            
            if result.data:
                current = result.data[0]
                new_count = current["new_learnings"] + count
                
                self.supabase.table("agent_performance_metrics").update({
                    "new_learnings": new_count
                }).eq("id", current["id"]).execute()
            
        except Exception as e:
            logger.warning(f"Failed to increment new learnings: {e}")
    
    async def get_metrics(
        self,
        agent_id: UUID,
        period: MetricsPeriod = MetricsPeriod.LAST_7_DAYS
    ) -> List[MetricsResponse]:
        """
        Get metrics for an agent for a specific period.
        
        Args:
            agent_id: Agent ID
            period: Time period (last_7_days, last_30_days, last_90_days)
        
        Returns:
            List of MetricsResponse ordered by date (newest first)
        """
        try:
            # Calculate date range
            today = date.today()
            
            if period == MetricsPeriod.LAST_7_DAYS:
                start_date = today - timedelta(days=7)
            elif period == MetricsPeriod.LAST_30_DAYS:
                start_date = today - timedelta(days=30)
            elif period == MetricsPeriod.LAST_90_DAYS:
                start_date = today - timedelta(days=90)
            else:
                start_date = today - timedelta(days=7)
            
            result = self.supabase.table("agent_performance_metrics").select("*").eq(
                "agent_id", str(agent_id)
            ).gte("metric_date", start_date.isoformat()).order(
                "metric_date", desc=True
            ).execute()
            
            return [MetricsResponse(**m) for m in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            raise
    
    async def get_aggregated_metrics(
        self,
        agent_id: UUID,
        period: MetricsPeriod = MetricsPeriod.LAST_30_DAYS
    ) -> Dict[str, Any]:
        """
        Get aggregated metrics for an agent.
        
        Args:
            agent_id: Agent ID
            period: Time period for aggregation
        
        Returns:
            Dictionary with aggregated metrics
        """
        try:
            metrics = await self.get_metrics(agent_id, period)
            
            if not metrics:
                return {
                    "period": period.value,
                    "total_interactions": 0,
                    "successful_interactions": 0,
                    "success_rate": 0.0,
                    "avg_response_time_ms": None,
                    "avg_satisfaction_score": None,
                    "total_memory_usage": 0,
                    "total_patterns_applied": 0,
                    "total_new_learnings": 0
                }
            
            total_interactions = sum(m.total_interactions for m in metrics)
            successful_interactions = sum(m.successful_interactions for m in metrics)
            
            # Calculate averages
            response_times = [
                m.avg_response_time_ms 
                for m in metrics 
                if m.avg_response_time_ms is not None
            ]
            avg_response_time = (
                sum(response_times) / len(response_times) 
                if response_times 
                else None
            )
            
            satisfaction_scores = [
                m.user_satisfaction_score 
                for m in metrics 
                if m.user_satisfaction_score is not None
            ]
            avg_satisfaction = (
                sum(satisfaction_scores) / len(satisfaction_scores) 
                if satisfaction_scores 
                else None
            )
            
            return {
                "period": period.value,
                "days_count": len(metrics),
                "total_interactions": total_interactions,
                "successful_interactions": successful_interactions,
                "success_rate": (
                    successful_interactions / total_interactions 
                    if total_interactions > 0 
                    else 0.0
                ),
                "avg_response_time_ms": int(avg_response_time) if avg_response_time else None,
                "avg_satisfaction_score": round(avg_satisfaction, 2) if avg_satisfaction else None,
                "total_memory_usage": sum(m.memory_chunks_used for m in metrics),
                "total_patterns_applied": sum(m.patterns_applied for m in metrics),
                "total_new_learnings": sum(m.new_learnings for m in metrics)
            }
            
        except Exception as e:
            logger.error(f"Failed to get aggregated metrics: {e}")
            raise
    
    async def calculate_learning_velocity(
        self,
        agent_id: UUID,
        days: int = 30
    ) -> float:
        """
        Calculate learning velocity (new learnings per day).
        
        Args:
            agent_id: Agent ID
            days: Number of days to calculate over
        
        Returns:
            Average new learnings per day
        """
        try:
            start_date = date.today() - timedelta(days=days)
            
            result = self.supabase.table("agent_performance_metrics").select(
                "new_learnings"
            ).eq("agent_id", str(agent_id)).gte(
                "metric_date", start_date.isoformat()
            ).execute()
            
            if not result.data:
                return 0.0
            
            total_learnings = sum(m["new_learnings"] for m in result.data)
            actual_days = len(result.data)
            
            velocity = total_learnings / actual_days if actual_days > 0 else 0.0
            
            logger.info(
                f"Learning velocity for agent {agent_id}: "
                f"{velocity:.2f} learnings/day ({total_learnings} in {actual_days} days)"
            )
            
            return round(velocity, 2)
            
        except Exception as e:
            logger.error(f"Failed to calculate learning velocity: {e}")
            raise
