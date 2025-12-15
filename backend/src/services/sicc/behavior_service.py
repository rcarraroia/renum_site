"""
Behavior Service - Agent Behavior Pattern Management
Sprint 10 - SICC Implementation

Service for managing and evolving agent behavioral patterns.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

from ...config.supabase import supabase_admin
from ...models.sicc.behavior import (
    BehaviorPatternCreate,
    BehaviorPatternUpdate,
    BehaviorPatternResponse,
    BehaviorPatternStats,
    PatternType
)
from ...utils.logger import logger


class BehaviorService:
    """Service for managing agent behavior patterns"""
    
    def __init__(self):
        """Initialize service with Supabase admin client"""
        self.supabase = supabase_admin
    
    async def create_pattern(self, data: BehaviorPatternCreate) -> BehaviorPatternResponse:
        """
        Create a new behavior pattern.
        
        Args:
            data: BehaviorPatternCreate with pattern data
        
        Returns:
            BehaviorPatternResponse with created pattern
        
        Raises:
            Exception: If creation fails
        """
        try:
            logger.info(
                f"Creating behavior pattern for agent {data.agent_id}: "
                f"{data.pattern_type} - {data.pattern_type}"
            )
            
            # Prepare data for insertion
            pattern_data = {
                "agent_id": str(data.agent_id),
                "client_id": str(data.client_id),
                "pattern_type": data.pattern_type.value,
                "trigger_context": data.trigger_context,
                "action_config": data.action_config,
                "success_rate": data.success_rate,
                "total_applications": data.total_applications,
                "successful_applications": int(data.success_rate * data.total_applications),
                "is_active": data.is_active
            }
            
            # Insert into database
            result = self.supabase.table("agent_behavior_patterns").insert(
                pattern_data
            ).execute()
            
            if not result.data:
                raise Exception("Failed to create behavior pattern")
            
            pattern = result.data[0]
            logger.info(f"Successfully created pattern {pattern['id']}")
            
            return BehaviorPatternResponse(**pattern)
            
        except Exception as e:
            logger.error(f"Failed to create behavior pattern: {e}")
            raise
    
    async def get_pattern(self, pattern_id: UUID) -> Optional[BehaviorPatternResponse]:
        """
        Get behavior pattern by ID.
        
        Args:
            pattern_id: Pattern ID
        
        Returns:
            BehaviorPatternResponse or None if not found
        """
        try:
            result = self.supabase.table("agent_behavior_patterns").select("*").eq(
                "id", str(pattern_id)
            ).execute()
            
            if not result.data:
                return None
            
            return BehaviorPatternResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to get pattern {pattern_id}: {e}")
            raise
    
    async def update_pattern(
        self,
        pattern_id: UUID,
        data: BehaviorPatternUpdate
    ) -> BehaviorPatternResponse:
        """
        Update behavior pattern.
        
        Args:
            pattern_id: Pattern ID
            data: BehaviorPatternUpdate with update data
        
        Returns:
            BehaviorPatternResponse with updated pattern
        
        Raises:
            Exception: If update fails
        """
        try:
            logger.info(f"Updating behavior pattern {pattern_id}")
            
            # Prepare update data (only include non-None fields)
            update_data = {
                k: v for k, v in data.model_dump(exclude_unset=True).items()
                if v is not None
            }
            
            if not update_data:
                raise ValueError("No fields to update")
            
            # Get current pattern for validation
            current = await self.get_pattern(pattern_id)
            if not current:
                raise ValueError(f"Pattern {pattern_id} not found")
            
            # Update in database
            result = self.supabase.table("agent_behavior_patterns").update(
                update_data
            ).eq("id", str(pattern_id)).execute()
            
            if not result.data:
                raise Exception("Failed to update behavior pattern")
            
            logger.info(f"Successfully updated pattern {pattern_id}")
            return BehaviorPatternResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to update pattern {pattern_id}: {e}")
            raise
    
    async def delete_pattern(self, pattern_id: UUID) -> bool:
        """
        Delete behavior pattern.
        
        Args:
            pattern_id: Pattern ID
        
        Returns:
            True if deleted successfully
        """
        try:
            logger.info(f"Deleting behavior pattern {pattern_id}")
            
            result = self.supabase.table("agent_behavior_patterns").delete().eq(
                "id", str(pattern_id)
            ).execute()
            
            logger.info(f"Successfully deleted pattern {pattern_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete pattern {pattern_id}: {e}")
            raise
    
    async def get_agent_patterns(
        self,
        agent_id: UUID,
        pattern_type: Optional[PatternType] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[BehaviorPatternResponse]:
        """
        Get all patterns for an agent.
        
        Args:
            agent_id: Agent ID
            pattern_type: Optional filter by pattern type
            is_active: Optional filter by active status
            limit: Maximum number of results
            offset: Offset for pagination
        
        Returns:
            List of BehaviorPatternResponse
        """
        try:
            query = self.supabase.table("agent_behavior_patterns").select("*").eq(
                "agent_id", str(agent_id)
            )
            
            if pattern_type:
                query = query.eq("pattern_type", pattern_type.value)
            
            if is_active is not None:
                query = query.eq("is_active", is_active)
            
            query = query.order("success_rate", desc=True).range(
                offset, offset + limit - 1
            )
            
            result = query.execute()
            
            return [BehaviorPatternResponse(**p) for p in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get agent patterns: {e}")
            raise
    
    async def record_pattern_usage(
        self,
        pattern_id: UUID,
        success: bool
    ) -> BehaviorPatternResponse:
        """
        Record usage of a behavior pattern and update success rate.
        
        Args:
            pattern_id: Pattern ID
            success: Whether the pattern usage was successful
        
        Returns:
            BehaviorPatternResponse with updated pattern
        """
        try:
            logger.info(f"Recording pattern usage: {pattern_id} (success={success})")
            
            # Get current pattern
            pattern = await self.get_pattern(pattern_id)
            if not pattern:
                raise ValueError(f"Pattern {pattern_id} not found")
            
            # Calculate new success rate
            total_uses = pattern.total_applications + 1
            successful_uses = int(pattern.success_rate * pattern.total_applications)
            
            if success:
                successful_uses += 1
            
            new_success_rate = successful_uses / total_uses if total_uses > 0 else 0.0
            
            # Update pattern
            update_data = {
                "total_applications": total_uses,
                "successful_applications": successful_uses,
                "success_rate": new_success_rate,
                "last_applied_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("agent_behavior_patterns").update(
                update_data
            ).eq("id", str(pattern_id)).execute()
            
            if not result.data:
                raise Exception("Failed to update pattern usage")
            
            logger.info(
                f"Updated pattern {pattern_id}: "
                f"uses={total_uses}, success_rate={new_success_rate:.2f}"
            )
            
            return BehaviorPatternResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to record pattern usage: {e}")
            raise
    
    async def get_pattern_stats(self, pattern_id: UUID) -> BehaviorPatternStats:
        """
        Get statistics for a behavior pattern.
        
        Args:
            pattern_id: Pattern ID
        
        Returns:
            BehaviorPatternStats with pattern statistics
        """
        try:
            pattern = await self.get_pattern(pattern_id)
            if not pattern:
                raise ValueError(f"Pattern {pattern_id} not found")
            
            # Calculate statistics
            total_uses = pattern.total_applications
            successful_uses = int(pattern.success_rate * total_uses)
            failed_uses = total_uses - successful_uses
            
            # Get usage in last 7 days (would need additional tracking table)
            # For now, approximate based on last_used_at
            last_7_days_uses = 0
            if pattern.last_used_at:
                days_since_use = (datetime.utcnow() - pattern.last_used_at).days
                if days_since_use <= 7:
                    # Rough estimate
                    last_7_days_uses = max(1, total_uses // 10)
            
            # Determine trend (would need historical data)
            trend = "stable"
            if pattern.success_rate > 0.7:
                trend = "increasing"
            elif pattern.success_rate < 0.4:
                trend = "decreasing"
            
            return BehaviorPatternStats(
                pattern_id=pattern.id,
                total_uses=total_uses,
                successful_applications=successful_uses,
                failed_uses=failed_uses,
                success_rate=pattern.success_rate,
                avg_last_7_days_uses=last_7_days_uses,
                trend=trend
            )
            
        except Exception as e:
            logger.error(f"Failed to get pattern stats: {e}")
            raise
    
    async def find_matching_patterns(
        self,
        agent_id: UUID,
        context: Dict[str, Any],
        min_confidence: float = 0.5
    ) -> List[BehaviorPatternResponse]:
        """
        Find behavior patterns that match given context.
        
        Args:
            agent_id: Agent ID
            context: Context to match against trigger conditions
            min_confidence: Minimum confidence threshold
        
        Returns:
            List of matching BehaviorPatternResponse ordered by relevance
        """
        try:
            logger.info(f"Finding matching patterns for agent {agent_id}")
            
            # Get all active patterns for agent
            patterns = await self.get_agent_patterns(
                agent_id=agent_id,
                is_active=True
            )
            
            # Filter by success rate (use as confidence proxy)
            patterns = [p for p in patterns if p.success_rate >= min_confidence]
            
            # Match patterns against context
            # This is a simplified matching - in production would use more sophisticated logic
            matching_patterns = []
            
            for pattern in patterns:
                # Check if trigger conditions match context
                match_score = self._calculate_match_score(
                    pattern.trigger_context,
                    context
                )
                
                if match_score > 0:
                    # Add pattern with match score for sorting
                    pattern_dict = pattern.model_dump()
                    pattern_dict["match_score"] = match_score
                    matching_patterns.append(pattern_dict)
            
            # Sort by match score * success rate
            matching_patterns.sort(
                key=lambda p: (
                    p["match_score"] *
                    p["success_rate"]
                ),
                reverse=True
            )
            
            # Convert back to response models
            result = [
                BehaviorPatternResponse(**{k: v for k, v in p.items() if k != "match_score"})
                for p in matching_patterns
            ]
            
            logger.info(f"Found {len(result)} matching patterns")
            return result
            
        except Exception as e:
            logger.error(f"Failed to find matching patterns: {e}")
            raise
    
    def _calculate_match_score(
        self,
        trigger_conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Calculate how well trigger conditions match context.
        
        Args:
            trigger_conditions: Pattern trigger conditions
            context: Current context
        
        Returns:
            Match score between 0 and 1
        """
        if not trigger_conditions:
            return 0.0
        
        matches = 0
        total = len(trigger_conditions)
        
        for key, expected_value in trigger_conditions.items():
            if key in context:
                actual_value = context[key]
                
                # Simple equality check (could be more sophisticated)
                if actual_value == expected_value:
                    matches += 1
                elif isinstance(expected_value, (list, tuple)):
                    if actual_value in expected_value:
                        matches += 1
        
        return matches / total if total > 0 else 0.0
    
    async def deactivate_low_performing_patterns(
        self,
        agent_id: UUID,
        min_usage: int = 10,
        min_success_rate: float = 0.3
    ) -> int:
        """
        Deactivate patterns with low performance.
        
        Args:
            agent_id: Agent ID
            min_usage: Minimum usage count before considering deactivation
            min_success_rate: Minimum success rate to keep active
        
        Returns:
            Number of patterns deactivated
        """
        try:
            logger.info(f"Checking for low-performing patterns for agent {agent_id}")
            
            # Get all active patterns
            patterns = await self.get_agent_patterns(
                agent_id=agent_id,
                is_active=True
            )
            
            deactivated = 0
            
            for pattern in patterns:
                # Only consider patterns with enough usage
                if pattern.total_applications >= min_usage:
                    # Deactivate if success rate is too low
                    if pattern.success_rate < min_success_rate:
                        await self.update_pattern(
                            pattern.id,
                            BehaviorPatternUpdate(is_active=False)
                        )
                        deactivated += 1
                        logger.info(
                            f"Deactivated pattern {pattern.id}: "
                            f"success_rate={pattern.success_rate:.2f}"
                        )
            
            logger.info(f"Deactivated {deactivated} low-performing patterns")
            return deactivated
            
        except Exception as e:
            logger.error(f"Failed to deactivate low-performing patterns: {e}")
            raise
