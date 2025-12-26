"""
Snapshot Service - Agent Knowledge Snapshot Management
Sprint 10 - SICC Implementation

Service for creating and restoring snapshots of agent knowledge state.
"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, timedelta

from src.utils.supabase_client import get_client
from src.models.sicc.snapshot import (
    SnapshotCreate,
    SnapshotResponse,
    SnapshotType
)
from src.utils.logger import logger


class SnapshotService:
    """Service for managing agent knowledge snapshots"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = get_client()
    
    async def create_snapshot(
        self,
        agent_id: UUID,
        client_id: UUID,
        snapshot_type: SnapshotType = SnapshotType.AUTOMATIC
    ) -> SnapshotResponse:
        """
        Create a snapshot of agent's current knowledge state.
        
        Args:
            agent_id: Agent ID
            client_id: Client ID
            snapshot_type: Type of snapshot (automatic, manual, milestone, pre_rollback)
        
        Returns:
            SnapshotResponse with created snapshot
        
        Raises:
            Exception: If snapshot creation fails
        """
        try:
            logger.info(
                f"Creating {snapshot_type.value} snapshot for agent {agent_id}"
            )
            
            # Get current memory count
            # CORRIGIDO: Usar memory_chunks ao invés de agent_memory_chunks
            memory_result = self.supabase.table("memory_chunks").select(
                "id", count="exact"
            ).eq("agent_id", str(agent_id)).eq("is_active", True).execute()
            
            memory_count = memory_result.count or 0
            
            # Get current pattern count
            # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
            pattern_result = self.supabase.table("behavior_patterns").select(
                "id", count="exact"
            ).eq("agent_id", str(agent_id)).eq("is_active", True).execute()
            
            pattern_count = pattern_result.count or 0
            
            # Get metrics for total interactions and success rate
            # CORRIGIDO: Usar agent_metrics ao invés de agent_performance_metrics
            metrics_result = self.supabase.table("agent_metrics").select(
                "total_interactions, successful_interactions"
            ).eq("agent_id", str(agent_id)).execute()
            
            total_interactions = 0
            successful_interactions = 0
            
            if metrics_result.data:
                for metric in metrics_result.data:
                    total_interactions += metric.get("total_interactions", 0)
                    successful_interactions += metric.get("successful_interactions", 0)
            
            avg_success_rate = (
                successful_interactions / total_interactions 
                if total_interactions > 0 
                else None
            )
            
            # Collect snapshot data (IDs of active memories and patterns)
            snapshot_data = {
                "memories": [],
                "patterns": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Get active memory IDs
            if memory_count > 0:
                # CORRIGIDO: Usar memory_chunks ao invés de agent_memory_chunks
                memories = self.supabase.table("memory_chunks").select(
                    "id, chunk_type, confidence_score, usage_count"
                ).eq("agent_id", str(agent_id)).eq("is_active", True).execute()
                
                snapshot_data["memories"] = [
                    {
                        "id": str(m["id"]),
                        "type": m["chunk_type"],
                        "confidence": m["confidence_score"],
                        "usage": m["usage_count"]
                    }
                    for m in memories.data
                ]
            
            # Get active pattern IDs
            if pattern_count > 0:
                # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
                patterns = self.supabase.table("behavior_patterns").select(
                    "id, pattern_type, success_rate, total_applications"
                ).eq("agent_id", str(agent_id)).eq("is_active", True).execute()
                
                snapshot_data["patterns"] = [
                    {
                        "id": str(p["id"]),
                        "type": p["pattern_type"],
                        "success_rate": p["success_rate"],
                        "applications": p["total_applications"]
                    }
                    for p in patterns.data
                ]
            
            # Create snapshot record
            snapshot_record = {
                "agent_id": str(agent_id),
                "client_id": str(client_id),
                "snapshot_type": snapshot_type.value,
                "memory_count": memory_count,
                "pattern_count": pattern_count,
                "total_interactions": total_interactions,
                "avg_success_rate": avg_success_rate,
                "snapshot_data": snapshot_data
            }
            
            # CORRIGIDO: Usar agent_snapshots ao invés de agent_knowledge_snapshots
            result = self.supabase.table("agent_snapshots").insert(
                snapshot_record
            ).execute()
            
            if not result.data:
                raise Exception("Failed to create snapshot")
            
            snapshot = result.data[0]
            logger.info(
                f"Successfully created snapshot {snapshot['id']}: "
                f"{memory_count} memories, {pattern_count} patterns"
            )
            
            return SnapshotResponse(**snapshot)
            
        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            raise
    
    async def get_snapshot(self, snapshot_id: UUID) -> Optional[SnapshotResponse]:
        """
        Get snapshot by ID.
        
        Args:
            snapshot_id: Snapshot ID
        
        Returns:
            SnapshotResponse or None if not found
        """
        try:
            # CORRIGIDO: Usar agent_snapshots ao invés de agent_knowledge_snapshots
            result = self.supabase.table("agent_snapshots").select("*").eq(
                "id", str(snapshot_id)
            ).execute()
            
            if not result.data:
                return None
            
            return SnapshotResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to get snapshot {snapshot_id}: {e}")
            raise
    
    async def restore_snapshot(
        self,
        snapshot_id: UUID
    ) -> Dict[str, Any]:
        """
        Restore agent knowledge state from snapshot.
        
        This deactivates all memories and patterns created after the snapshot.
        
        Args:
            snapshot_id: Snapshot ID to restore
        
        Returns:
            Dictionary with restoration statistics
        
        Raises:
            Exception: If restoration fails
        """
        try:
            logger.info(f"Restoring snapshot {snapshot_id}")
            
            # Get snapshot
            snapshot = await self.get_snapshot(snapshot_id)
            if not snapshot:
                raise ValueError(f"Snapshot {snapshot_id} not found")
            
            snapshot_time = snapshot.created_at
            agent_id = snapshot.agent_id
            
            # Deactivate memories created after snapshot
            # CORRIGIDO: Usar memory_chunks ao invés de agent_memory_chunks
            memory_update = self.supabase.table("memory_chunks").update({
                "is_active": False
            }).eq("agent_id", str(agent_id)).gt(
                "created_at", snapshot_time.isoformat()
            ).execute()
            
            memories_deactivated = len(memory_update.data) if memory_update.data else 0
            
            # Deactivate patterns created after snapshot
            # CORRIGIDO: Usar behavior_patterns ao invés de agent_behavior_patterns
            pattern_update = self.supabase.table("behavior_patterns").update({
                "is_active": False
            }).eq("agent_id", str(agent_id)).gt(
                "created_at", snapshot_time.isoformat()
            ).execute()
            
            patterns_deactivated = len(pattern_update.data) if pattern_update.data else 0
            
            logger.info(
                f"Snapshot {snapshot_id} restored: "
                f"{memories_deactivated} memories and {patterns_deactivated} patterns deactivated"
            )
            
            return {
                "snapshot_id": str(snapshot_id),
                "snapshot_time": snapshot_time.isoformat(),
                "memories_deactivated": memories_deactivated,
                "patterns_deactivated": patterns_deactivated,
                "current_memory_count": snapshot.memory_count,
                "current_pattern_count": snapshot.pattern_count
            }
            
        except Exception as e:
            logger.error(f"Failed to restore snapshot {snapshot_id}: {e}")
            raise
    
    async def get_agent_snapshots(
        self,
        agent_id: UUID,
        limit: int = 30,
        offset: int = 0
    ) -> List[SnapshotResponse]:
        """
        Get all snapshots for an agent.
        
        Args:
            agent_id: Agent ID
            limit: Maximum number of results
            offset: Offset for pagination
        
        Returns:
            List of SnapshotResponse ordered by creation date (newest first)
        """
        try:
            # CORRIGIDO: Usar agent_snapshots ao invés de agent_knowledge_snapshots
            result = self.supabase.table("agent_snapshots").select("*").eq(
                "agent_id", str(agent_id)
            ).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            return [SnapshotResponse(**s) for s in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get agent snapshots: {e}")
            raise
    
    async def archive_old_snapshots(
        self,
        retention_days: int = 30
    ) -> int:
        """
        Archive snapshots older than retention period.
        
        Args:
            retention_days: Number of days to retain snapshots
        
        Returns:
            Number of snapshots archived
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            
            logger.info(
                f"Archiving snapshots older than {cutoff_date.date()}"
            )
            
            # For now, we just delete old snapshots
            # In production, you might want to move them to cold storage
            # CORRIGIDO: Usar agent_snapshots ao invés de agent_knowledge_snapshots
            result = self.supabase.table("agent_snapshots").delete().lt(
                "created_at", cutoff_date.isoformat()
            ).execute()
            
            archived_count = len(result.data) if result.data else 0
            
            logger.info(f"Archived {archived_count} old snapshots")
            return archived_count
            
        except Exception as e:
            logger.error(f"Failed to archive old snapshots: {e}")
            raise
    
    async def get_snapshot_comparison(
        self,
        snapshot_id_1: UUID,
        snapshot_id_2: UUID
    ) -> Dict[str, Any]:
        """
        Compare two snapshots to see knowledge evolution.
        
        Args:
            snapshot_id_1: First snapshot ID (older)
            snapshot_id_2: Second snapshot ID (newer)
        
        Returns:
            Dictionary with comparison statistics
        """
        try:
            snapshot1 = await self.get_snapshot(snapshot_id_1)
            snapshot2 = await self.get_snapshot(snapshot_id_2)
            
            if not snapshot1 or not snapshot2:
                raise ValueError("One or both snapshots not found")
            
            return {
                "snapshot_1": {
                    "id": str(snapshot1.id),
                    "created_at": snapshot1.created_at.isoformat(),
                    "memory_count": snapshot1.memory_count,
                    "pattern_count": snapshot1.pattern_count,
                    "total_interactions": snapshot1.total_interactions,
                    "avg_success_rate": snapshot1.avg_success_rate
                },
                "snapshot_2": {
                    "id": str(snapshot2.id),
                    "created_at": snapshot2.created_at.isoformat(),
                    "memory_count": snapshot2.memory_count,
                    "pattern_count": snapshot2.pattern_count,
                    "total_interactions": snapshot2.total_interactions,
                    "avg_success_rate": snapshot2.avg_success_rate
                },
                "delta": {
                    "memories_added": snapshot2.memory_count - snapshot1.memory_count,
                    "patterns_added": snapshot2.pattern_count - snapshot1.pattern_count,
                    "interactions_added": snapshot2.total_interactions - snapshot1.total_interactions,
                    "success_rate_change": (
                        snapshot2.avg_success_rate - snapshot1.avg_success_rate
                        if snapshot1.avg_success_rate and snapshot2.avg_success_rate
                        else None
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to compare snapshots: {e}")
            raise
