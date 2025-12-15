"""
Learning Service - ISA (Inteligência de Supervisão Adaptativa)
Sprint 10 - SICC Implementation - Phase 3

Service for analyzing conversations and extracting learnings with supervised approval.
Implements hybrid approval model: auto-approve high confidence, human review medium confidence.
"""

from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime, timedelta

from ...config.supabase import supabase_admin
from ...models.sicc.learning import (
    LearningLogCreate,
    LearningLogResponse,
    LearningApproval,
    LearningStatus,
    LearningSource,
    LearningStats,
    LearningBatch
)
from ...models.sicc.memory import MemoryChunkCreate, ChunkType
from ...models.sicc.behavior import BehaviorPatternCreate, PatternType
from ...utils.logger import logger
from .memory_service import MemoryService
from .behavior_service import BehaviorService
from .metrics_service import MetricsService


class LearningService:
    """Service for ISA-supervised learning cycle"""
    
    def __init__(self):
        """Initialize service with dependencies"""
        self.supabase = supabase_admin
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        self.metrics_service = MetricsService()
    
    async def analyze_conversations(
        self,
        agent_id: UUID,
        time_window_hours: int = 24,
        min_messages: int = 5
    ) -> Dict[str, Any]:
        """
        Analyze recent conversations to extract potential learnings.
        
        This is the ISA analysis phase - identifies patterns, new terms,
        successful strategies, and areas for improvement.
        
        Args:
            agent_id: Agent ID to analyze
            time_window_hours: Hours to look back (default 24h)
            min_messages: Minimum messages in conversation to analyze
        
        Returns:
            Dictionary with analysis results:
            - conversations_analyzed: int
            - learnings_detected: int
            - high_confidence: int (auto-approved)
            - medium_confidence: int (needs review)
            - low_confidence: int (discarded)
        """
        try:
            logger.info(
                f"ISA analyzing conversations for agent {agent_id} "
                f"(last {time_window_hours}h)"
            )
            
            # Calculate time window
            cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
            
            # Get agent's client_id first
            agent_result = self.supabase.table("agents").select(
                "client_id"
            ).eq("id", str(agent_id)).single().execute()
            
            if not agent_result.data:
                logger.warning(f"Agent {agent_id} not found")
                return {
                    "conversations_analyzed": 0,
                    "learnings_detected": 0,
                    "high_confidence": 0,
                    "medium_confidence": 0,
                    "low_confidence": 0
                }
            
            client_id = agent_result.data["client_id"]
            
            # Get recent conversations for this client
            conversations_result = self.supabase.table("conversations").select(
                "id, status, created_at"
            ).eq("client_id", client_id).gte(
                "created_at", cutoff_time.isoformat()
            ).execute()
            
            if not conversations_result.data:
                logger.info("No recent conversations found")
                return {
                    "conversations_analyzed": 0,
                    "learnings_detected": 0,
                    "high_confidence": 0,
                    "medium_confidence": 0,
                    "low_confidence": 0
                }
            
            conversations = conversations_result.data
            logger.info(f"Found {len(conversations)} recent conversations")
            
            # Analyze each conversation
            total_learnings = 0
            high_confidence_count = 0
            medium_confidence_count = 0
            low_confidence_count = 0
            
            for conversation in conversations:
                # Get messages for this conversation
                messages_result = self.supabase.table("messages").select(
                    "id, role, content, created_at, metadata"
                ).eq("conversation_id", conversation["id"]).order(
                    "created_at", desc=False
                ).execute()
                
                if not messages_result.data or len(messages_result.data) < min_messages:
                    continue
                
                messages = messages_result.data
                
                # Analyze conversation for learnings
                learnings = await self._extract_learnings_from_conversation(
                    agent_id=agent_id,
                    conversation_id=UUID(conversation["id"]),
                    messages=messages
                )
                
                # Process each learning based on confidence
                for learning_data, confidence in learnings:
                    total_learnings += 1
                    
                    # Create learning log
                    learning_log = await self.create_learning_log(
                        agent_id=agent_id,
                        learning_type=learning_data["type"],
                        source_data=learning_data["source_data"],
                        analysis=learning_data["analysis"],
                        confidence=confidence,
                        source=LearningSource.ISA_ANALYSIS,
                        source_id=UUID(conversation["id"])
                    )
                    
                    # Apply hybrid approval model
                    if confidence >= 0.8:
                        # High confidence: auto-approve
                        await self.approve_learning(
                            learning_id=learning_log.id,
                            approved_by=agent_id,  # ISA auto-approval
                            auto_approved=True
                        )
                        high_confidence_count += 1
                        
                    elif confidence >= 0.5:
                        # Medium confidence: needs human review
                        medium_confidence_count += 1
                        
                    else:
                        # Low confidence: discard
                        await self.reject_learning(
                            learning_id=learning_log.id,
                            rejected_by=agent_id,  # ISA auto-rejection
                            reason="Confidence score below threshold (< 0.5)"
                        )
                        low_confidence_count += 1
            
            result = {
                "conversations_analyzed": len(conversations),
                "learnings_detected": total_learnings,
                "high_confidence": high_confidence_count,
                "medium_confidence": medium_confidence_count,
                "low_confidence": low_confidence_count
            }
            
            logger.info(f"ISA analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze conversations: {e}")
            raise
    
    async def _extract_learnings_from_conversation(
        self,
        agent_id: UUID,
        conversation_id: UUID,
        messages: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Extract potential learnings from a conversation.
        
        This is a simplified implementation. In production, this would use
        LangChain/LangGraph with LLM to analyze conversation patterns.
        
        Args:
            agent_id: Agent ID
            conversation_id: Conversation ID
            messages: List of message dictionaries
        
        Returns:
            List of tuples (learning_data, confidence_score)
        """
        learnings = []
        
        # Simple heuristics for learning detection
        # In production, replace with LLM-based analysis
        
        # 1. Detect new business terms (words used frequently by user)
        user_messages = [m for m in messages if m["role"] == "user"]
        if len(user_messages) >= 3:
            # Extract potential business terms
            # (simplified - would use NLP in production)
            all_text = " ".join([m["content"] for m in user_messages])
            words = all_text.lower().split()
            
            # Find words that appear multiple times
            word_freq = {}
            for word in words:
                if len(word) > 5:  # Only longer words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Terms used 3+ times might be important
            for term, freq in word_freq.items():
                if freq >= 3:
                    learning_data = {
                        "type": "memory_added",
                        "source_data": {
                            "conversation_id": str(conversation_id),
                            "content": f"Termo: {term}\nContexto: {all_text[:200]}",
                            "chunk_type": "business_term",
                            "metadata": {
                                "term": term,
                                "frequency": freq
                            }
                        },
                        "analysis": {
                            "detected_pattern": "frequent_term",
                            "occurrences": freq,
                            "recommendation": f"Add '{term}' to business vocabulary"
                        }
                    }
                    # Confidence based on frequency
                    confidence = min(0.5 + (freq * 0.1), 0.9)
                    learnings.append((learning_data, confidence))
        
        # 2. Detect successful response patterns
        # Look for positive user feedback after agent responses
        for i in range(len(messages) - 1):
            if messages[i]["role"] == "assistant":
                next_msg = messages[i + 1]
                if next_msg["role"] == "user":
                    # Check for positive indicators
                    positive_words = ["obrigado", "perfeito", "ótimo", "excelente", "sim"]
                    content_lower = next_msg["content"].lower()
                    
                    if any(word in content_lower for word in positive_words):
                        learning_data = {
                            "type": "pattern_detected",
                            "source_data": {
                                "conversation_id": str(conversation_id),
                                "pattern_type": "response_strategy",
                                "trigger_context": {
                                    "user_sentiment": "positive",
                                    "context": messages[i].get("metadata", {})
                                },
                                "action_config": {
                                    "strategy": "reuse_successful_response",
                                    "template": messages[i]["content"]
                                }
                            },
                            "analysis": {
                                "detected_pattern": "positive_feedback",
                                "strategy": "successful_response",
                                "recommendation": "Reuse this response pattern in similar contexts"
                            }
                        }
                        confidence = 0.7  # Medium-high confidence
                        learnings.append((learning_data, confidence))
        
        # 3. Detect common objections/questions
        question_words = ["como", "quando", "onde", "por que", "quanto"]
        user_questions = []
        
        for msg in user_messages:
            content_lower = msg["content"].lower()
            if any(word in content_lower for word in question_words):
                user_questions.append(msg["content"])
        
        if len(user_questions) >= 2:
            # Multiple questions might indicate FAQ opportunity
            learning_data = {
                "type": "memory_added",
                "source_data": {
                    "conversation_id": str(conversation_id),
                    "content": "\n".join(user_questions),
                    "chunk_type": "faq",
                    "metadata": {
                        "questions_count": len(user_questions)
                    }
                },
                "analysis": {
                    "detected_pattern": "frequent_questions",
                    "recommendation": "Create FAQ entries for these questions"
                }
            }
            confidence = 0.6
            learnings.append((learning_data, confidence))
        
        logger.info(
            f"Extracted {len(learnings)} potential learnings from "
            f"conversation {conversation_id}"
        )
        
        return learnings
    
    async def create_learning_log(
        self,
        agent_id: UUID,
        learning_type: str,
        source_data: Dict[str, Any],
        analysis: Dict[str, Any],
        confidence: float,
        source: LearningSource = LearningSource.ISA_ANALYSIS,
        source_id: Optional[UUID] = None
    ) -> LearningLogResponse:
        """
        Create a new learning log entry.
        
        Args:
            agent_id: Agent ID
            learning_type: Type of learning (business_term, response_strategy, etc)
            source_data: Raw data that triggered the learning
            analysis: ISA analysis results
            confidence: Confidence score (0.0-1.0)
            source: Source of learning
            source_id: ID of source entity (conversation, document, etc)
        
        Returns:
            LearningLogResponse with created log
        """
        try:
            logger.info(
                f"Creating learning log for agent {agent_id}: "
                f"{learning_type} (confidence={confidence:.2f})"
            )
            
            # Get client_id from agent
            agent_result = self.supabase.table("agents").select(
                "client_id"
            ).eq("id", str(agent_id)).single().execute()
            
            if not agent_result.data:
                raise ValueError(f"Agent {agent_id} not found")
            
            client_id = UUID(agent_result.data["client_id"])
            
            # Determine initial status based on confidence
            if confidence >= 0.8:
                status = "pending"  # Will be auto-approved
            elif confidence >= 0.5:
                status = "pending"  # Needs review
            else:
                status = "pending"  # Will be auto-rejected
            
            # Prepare learning log data
            log_data = {
                "agent_id": str(agent_id),
                "client_id": str(client_id),
                "learning_type": learning_type,
                "source_data": source_data,
                "analysis": analysis,
                "action_taken": "created",
                "confidence": confidence,
                "status": status
            }
            
            # Insert into database
            result = self.supabase.table("agent_learning_logs").insert(
                log_data
            ).execute()
            
            if not result.data:
                raise Exception("Failed to create learning log")
            
            log = result.data[0]
            logger.info(f"Successfully created learning log {log['id']}")
            
            return LearningLogResponse(**log)
            
        except Exception as e:
            logger.error(f"Failed to create learning log: {e}")
            raise
    
    async def approve_learning(
        self,
        learning_id: UUID,
        approved_by: UUID,
        auto_approved: bool = False
    ) -> LearningLogResponse:
        """
        Approve a learning log and consolidate into memory/pattern.
        
        Args:
            learning_id: Learning log ID
            approved_by: User/ISA ID approving
            auto_approved: Whether this is auto-approval
        
        Returns:
            LearningLogResponse with updated log
        """
        try:
            logger.info(
                f"Approving learning {learning_id} "
                f"(auto={auto_approved})"
            )
            
            # Get learning log
            log_result = self.supabase.table("agent_learning_logs").select(
                "*"
            ).eq("id", str(learning_id)).single().execute()
            
            if not log_result.data:
                raise ValueError(f"Learning log {learning_id} not found")
            
            log = log_result.data
            
            # Update status
            update_data = {
                "status": "approved",
                "reviewed_by": str(approved_by),
                "reviewed_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table("agent_learning_logs").update(
                update_data
            ).eq("id", str(learning_id)).execute()
            
            if not result.data:
                raise Exception("Failed to approve learning")
            
            # Consolidate learning into memory/pattern
            await self._consolidate_learning(log)
            
            logger.info(f"Successfully approved learning {learning_id}")
            return LearningLogResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to approve learning: {e}")
            raise
    
    async def reject_learning(
        self,
        learning_id: UUID,
        rejected_by: UUID,
        reason: str
    ) -> LearningLogResponse:
        """
        Reject a learning log.
        
        Args:
            learning_id: Learning log ID
            rejected_by: User/ISA ID rejecting
            reason: Rejection reason
        
        Returns:
            LearningLogResponse with updated log
        """
        try:
            logger.info(f"Rejecting learning {learning_id}: {reason}")
            
            # Update status
            update_data = {
                "status": "rejected",
                "reviewed_by": str(rejected_by),
                "reviewed_at": datetime.utcnow().isoformat(),
                "action_taken": f"rejected: {reason}"
            }
            
            result = self.supabase.table("agent_learning_logs").update(
                update_data
            ).eq("id", str(learning_id)).execute()
            
            if not result.data:
                raise Exception("Failed to reject learning")
            
            logger.info(f"Successfully rejected learning {learning_id}")
            return LearningLogResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to reject learning: {e}")
            raise
    
    async def _consolidate_learning(self, log: Dict[str, Any]) -> None:
        """
        Consolidate approved learning into memory chunk or behavior pattern.
        
        Args:
            log: Learning log dictionary
        """
        try:
            agent_id = UUID(log["agent_id"])
            client_id = UUID(log["client_id"])
            learning_type = log["learning_type"]
            source_data = log["source_data"]
            analysis = log["analysis"]
            confidence = log["confidence"]
            
            logger.info(
                f"Consolidating learning {log['id']} into "
                f"{learning_type}"
            )
            
            # Consolidate based on learning type
            if learning_type == "memory_added":
                # Create memory chunk
                content = source_data.get("content", "")
                chunk_type_str = source_data.get("chunk_type", "business_term")
                
                # Map to ChunkType enum
                chunk_type_map = {
                    "business_term": ChunkType.BUSINESS_TERM,
                    "process": ChunkType.PROCESS,
                    "faq": ChunkType.FAQ,
                    "product": ChunkType.PRODUCT,
                    "objection": ChunkType.OBJECTION,
                    "pattern": ChunkType.PATTERN,
                    "insight": ChunkType.INSIGHT
                }
                chunk_type = chunk_type_map.get(chunk_type_str, ChunkType.BUSINESS_TERM)
                
                await self.memory_service.create_memory_from_text(
                    agent_id=agent_id,
                    client_id=client_id,
                    content=content,
                    chunk_type=chunk_type,
                    metadata={
                        **source_data.get("metadata", {}),
                        "learning_log_id": str(log["id"])
                    },
                    source="isa_analysis",
                    confidence=confidence
                )
                
            elif learning_type == "pattern_detected":
                # Create behavior pattern
                trigger_context = source_data.get("trigger_context", {})
                action_config = source_data.get("action_config", {})
                pattern_type_str = source_data.get("pattern_type", "response_strategy")
                
                # Map to PatternType enum
                pattern_type_map = {
                    "response_strategy": PatternType.RESPONSE_STRATEGY,
                    "tone_adjustment": PatternType.TONE_ADJUSTMENT,
                    "flow_optimization": PatternType.FLOW_OPTIMIZATION,
                    "objection_handling": PatternType.OBJECTION_HANDLING
                }
                pattern_type = pattern_type_map.get(pattern_type_str, PatternType.RESPONSE_STRATEGY)
                
                await self.behavior_service.create_pattern(
                    BehaviorPatternCreate(
                        agent_id=agent_id,
                        client_id=client_id,
                        pattern_type=pattern_type,
                        trigger_context=trigger_context,
                        action_config=action_config,
                        success_rate=confidence,
                        total_applications=0
                    )
                )
                
            elif learning_type == "behavior_updated":
                # Update existing behavior pattern
                pattern_id = source_data.get("pattern_id")
                if pattern_id:
                    # Logic to update pattern would go here
                    pass
                
            elif learning_type == "insight_generated":
                # Create insight memory
                insight = source_data.get("insight", "")
                
                await self.memory_service.create_memory_from_text(
                    agent_id=agent_id,
                    client_id=client_id,
                    content=insight,
                    chunk_type=ChunkType.INSIGHT,
                    metadata={
                        "learning_log_id": str(log["id"]),
                        "auto_generated": True
                    },
                    source="isa_analysis",
                    confidence=confidence
                )
            
            # Update learning log to mark as applied
            self.supabase.table("agent_learning_logs").update({
                "status": "applied",
                "action_taken": f"consolidated into {learning_type}"
            }).eq("id", log["id"]).execute()
            
            # Increment metrics
            await self.metrics_service.increment_learnings(
                agent_id=agent_id,
                count=1
            )
            
            logger.info(f"Successfully consolidated learning {log['id']}")
            
        except Exception as e:
            logger.error(f"Failed to consolidate learning: {e}")
            # Don't raise - learning is approved but consolidation failed
            # Can be retried later
    
    async def get_pending_learnings(
        self,
        agent_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[LearningLogResponse]:
        """
        Get pending learnings for review.
        
        Args:
            agent_id: Agent ID
            limit: Maximum results
            offset: Offset for pagination
        
        Returns:
            List of LearningLogResponse
        """
        try:
            result = self.supabase.table("agent_learning_logs").select(
                "*"
            ).eq("agent_id", str(agent_id)).eq(
                "status", "pending"
            ).order("confidence", desc=True).range(
                offset, offset + limit - 1
            ).execute()
            
            return [LearningLogResponse(**log) for log in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get pending learnings: {e}")
            raise
    
    async def get_learning_stats(self, agent_id: UUID) -> Dict[str, Any]:
        """
        Get learning statistics for an agent.
        
        Args:
            agent_id: Agent ID
        
        Returns:
            Dictionary with learning statistics
        """
        try:
            # Get all learnings for agent
            result = self.supabase.table("agent_learning_logs").select(
                "status, confidence, created_at"
            ).eq("agent_id", str(agent_id)).execute()
            
            if not result.data:
                return {
                    "total_learnings": 0,
                    "pending": 0,
                    "approved": 0,
                    "rejected": 0,
                    "applied": 0,
                    "avg_confidence": 0.0,
                    "last_learning_at": None
                }
            
            logs = result.data
            
            # Calculate statistics
            stats = {
                "total_learnings": len(logs),
                "pending": sum(1 for log in logs if log["status"] == "pending"),
                "approved": sum(1 for log in logs if log["status"] == "approved"),
                "rejected": sum(1 for log in logs if log["status"] == "rejected"),
                "applied": sum(1 for log in logs if log["status"] == "applied"),
                "avg_confidence": sum(log["confidence"] for log in logs) / len(logs),
                "last_learning_at": max(log["created_at"] for log in logs)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get learning stats: {e}")
            raise
    
    async def batch_approve_learnings(
        self,
        learning_ids: List[UUID],
        approved_by: UUID
    ) -> Dict[str, Any]:
        """
        Batch approve multiple learnings.
        
        Args:
            learning_ids: List of learning IDs
            approved_by: User ID approving
        
        Returns:
            Dictionary with results
        """
        try:
            logger.info(f"Batch approving {len(learning_ids)} learnings")
            
            approved = 0
            failed = 0
            
            for learning_id in learning_ids:
                try:
                    await self.approve_learning(learning_id, approved_by)
                    approved += 1
                except Exception as e:
                    logger.error(f"Failed to approve {learning_id}: {e}")
                    failed += 1
            
            result = {
                "total": len(learning_ids),
                "approved": approved,
                "failed": failed
            }
            
            logger.info(f"Batch approval complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to batch approve learnings: {e}")
            raise
    
    async def batch_reject_learnings(
        self,
        learning_ids: List[UUID],
        rejected_by: UUID,
        reason: str
    ) -> Dict[str, Any]:
        """
        Batch reject multiple learnings.
        
        Args:
            learning_ids: List of learning IDs
            rejected_by: User ID rejecting
            reason: Rejection reason
        
        Returns:
            Dictionary with results
        """
        try:
            logger.info(f"Batch rejecting {len(learning_ids)} learnings")
            
            rejected = 0
            failed = 0
            
            for learning_id in learning_ids:
                try:
                    await self.reject_learning(learning_id, rejected_by, reason)
                    rejected += 1
                except Exception as e:
                    logger.error(f"Failed to reject {learning_id}: {e}")
                    failed += 1
            
            result = {
                "total": len(learning_ids),
                "rejected": rejected,
                "failed": failed
            }
            
            logger.info(f"Batch rejection complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to batch reject learnings: {e}")
            raise
