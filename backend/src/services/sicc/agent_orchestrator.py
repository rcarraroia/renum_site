"""
Agent Orchestrator - Renus Integration
Sprint 10 - SICC Implementation - Phase 2 (Task 31)

Service for enriching agent prompts with relevant memories and behavioral patterns.
Integrates SICC with existing Renus service for context-aware responses.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
import tiktoken

from src.utils.logger import logger
from .memory_service import MemoryService
from .behavior_service import BehaviorService
from .embedding_service import get_embedding_service
from src.models.sicc.memory import MemorySearchQuery, ChunkType


class EnrichedPrompt:
    """Container for enriched prompt with memories and patterns"""
    
    def __init__(
        self,
        original_message: str,
        enriched_prompt: str,
        memories_used: List[Dict[str, Any]],
        patterns_applied: List[Dict[str, Any]],
        token_count: int,
        context: Dict[str, Any]
    ):
        self.original_message = original_message
        self.enriched_prompt = enriched_prompt
        self.memories_used = memories_used
        self.patterns_applied = patterns_applied
        self.token_count = token_count
        self.context = context


class AgentOrchestrator:
    """
    Orchestrates agent responses by enriching prompts with SICC knowledge.
    
    This service integrates with Renus to provide context-aware responses
    by adding relevant memories and behavioral patterns to prompts.
    """
    
    MAX_TOKENS = 8000  # Maximum tokens for enriched prompt
    MAX_MEMORIES = 5   # Top N memories to include
    
    def __init__(self):
        """Initialize orchestrator with SICC services"""
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        self.embedding_service = get_embedding_service()
        
        # Initialize tokenizer for token counting
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        except Exception as e:
            logger.warning(f"Failed to load tiktoken, using fallback: {e}")
            self.tokenizer = None
    
    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens
        
        Returns:
            Number of tokens
        """
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4
    
    async def enrich_prompt(
        self,
        agent_id: UUID,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> EnrichedPrompt:
        """
        Enrich prompt with relevant memories and behavioral patterns.
        
        This is the core method that:
        1. Searches for relevant memories using similarity search
        2. Finds applicable behavioral patterns
        3. Constructs enriched prompt with context
        4. Ensures token limit is respected
        
        Args:
            agent_id: Agent ID
            message: User message
            context: Additional context (conversation history, user info, etc)
        
        Returns:
            EnrichedPrompt with enriched content and metadata
        
        Raises:
            Exception: If enrichment fails
        """
        try:
            logger.info(f"Enriching prompt for agent {agent_id}: '{message[:50]}...'")
            
            context = context or {}
            memories_used = []
            patterns_applied = []
            
            # Step 1: Search for relevant memories
            try:
                search_query = MemorySearchQuery(
                    agent_id=agent_id,
                    query_text=message,
                    limit=self.MAX_MEMORIES,
                    similarity_threshold=0.7,  # Only include relevant memories
                    min_confidence=0.5
                )
                
                search_results = await self.memory_service.search_memories(search_query)
                
                if search_results:
                    logger.info(f"Found {len(search_results)} relevant memories")
                    
                    for result in search_results:
                        memory = result.memory
                        memories_used.append({
                            "id": str(memory.id),
                            "type": memory.chunk_type.value,
                            "content": memory.content,
                            "similarity": result.similarity_score,
                            "relevance": result.relevance_score
                        })
                        
                        # Update usage count
                        await self.memory_service.increment_usage_count(memory.id)
                
            except Exception as e:
                logger.warning(f"Memory search failed, continuing without memories: {e}")
            
            # Step 2: Find applicable behavioral patterns
            try:
                # Build context for pattern matching
                pattern_context = {
                    "message_type": context.get("message_type", "text"),
                    "user_sentiment": context.get("sentiment", "neutral"),
                    "conversation_stage": context.get("stage", "ongoing"),
                    **context
                }
                
                patterns = await self.behavior_service.find_matching_patterns(
                    agent_id=agent_id,
                    context=pattern_context,
                    min_confidence=0.6
                )
                
                if patterns:
                    logger.info(f"Found {len(patterns)} applicable patterns")
                    
                    for pattern in patterns[:3]:  # Limit to top 3 patterns
                        patterns_applied.append({
                            "id": str(pattern.id),
                            "type": pattern.pattern_type.value,
                            "trigger": pattern.trigger_context,
                            "action": pattern.action_config,
                            "success_rate": pattern.success_rate
                        })
                
            except Exception as e:
                logger.warning(f"Pattern matching failed, continuing without patterns: {e}")
            
            # Step 3: Construct enriched prompt
            enriched_parts = []
            
            # Add base instruction
            enriched_parts.append("# Context and Knowledge")
            enriched_parts.append("")
            
            # Add memories if found
            if memories_used:
                enriched_parts.append("## Relevant Knowledge:")
                for i, mem in enumerate(memories_used, 1):
                    enriched_parts.append(f"{i}. [{mem['type']}] {mem['content']}")
                enriched_parts.append("")
            
            # Add behavioral patterns if found
            if patterns_applied:
                enriched_parts.append("## Behavioral Guidelines:")
                for i, pattern in enumerate(patterns_applied, 1):
                    action = pattern['action']
                    if 'strategy' in action:
                        enriched_parts.append(f"{i}. Strategy: {action['strategy']}")
                    if 'template' in action:
                        enriched_parts.append(f"   Template: {action['template'][:100]}...")
                enriched_parts.append("")
            
            # Add original message
            enriched_parts.append("## User Message:")
            enriched_parts.append(message)
            enriched_parts.append("")
            
            # Add instruction
            if memories_used or patterns_applied:
                enriched_parts.append("## Instructions:")
                enriched_parts.append(
                    "Use the knowledge and guidelines above to provide a contextual, "
                    "accurate response. Prioritize information from the knowledge base."
                )
            
            enriched_prompt = "\n".join(enriched_parts)
            
            # Step 4: Check token limit
            token_count = self._count_tokens(enriched_prompt)
            
            if token_count > self.MAX_TOKENS:
                logger.warning(
                    f"Enriched prompt exceeds token limit ({token_count} > {self.MAX_TOKENS}), "
                    "truncating memories"
                )
                
                # Truncate memories to fit token limit
                while token_count > self.MAX_TOKENS and memories_used:
                    memories_used.pop()  # Remove least relevant memory
                    
                    # Rebuild prompt
                    enriched_parts = []
                    enriched_parts.append("# Context and Knowledge")
                    enriched_parts.append("")
                    
                    if memories_used:
                        enriched_parts.append("## Relevant Knowledge:")
                        for i, mem in enumerate(memories_used, 1):
                            enriched_parts.append(f"{i}. [{mem['type']}] {mem['content']}")
                        enriched_parts.append("")
                    
                    if patterns_applied:
                        enriched_parts.append("## Behavioral Guidelines:")
                        for i, pattern in enumerate(patterns_applied, 1):
                            action = pattern['action']
                            if 'strategy' in action:
                                enriched_parts.append(f"{i}. Strategy: {action['strategy']}")
                        enriched_parts.append("")
                    
                    enriched_parts.append("## User Message:")
                    enriched_parts.append(message)
                    
                    enriched_prompt = "\n".join(enriched_parts)
                    token_count = self._count_tokens(enriched_prompt)
            
            logger.info(
                f"Prompt enriched: {len(memories_used)} memories, "
                f"{len(patterns_applied)} patterns, {token_count} tokens"
            )
            
            return EnrichedPrompt(
                original_message=message,
                enriched_prompt=enriched_prompt,
                memories_used=memories_used,
                patterns_applied=patterns_applied,
                token_count=token_count,
                context=context
            )
            
        except Exception as e:
            logger.error(f"Failed to enrich prompt: {e}")
            
            # Fallback: return original message
            return EnrichedPrompt(
                original_message=message,
                enriched_prompt=message,
                memories_used=[],
                patterns_applied=[],
                token_count=self._count_tokens(message),
                context=context
            )
    
    async def process_with_memory(
        self,
        agent_id: UUID,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process message with memory enrichment (simplified version).
        
        This method enriches the prompt and returns the enriched content
        ready to be sent to the LLM. The actual LLM call should be done
        by the Renus service.
        
        Args:
            agent_id: Agent ID
            message: User message
            context: Additional context
        
        Returns:
            Dictionary with enriched prompt and metadata
        """
        try:
            # Enrich prompt
            enriched = await self.enrich_prompt(agent_id, message, context)
            
            return {
                "enriched_prompt": enriched.enriched_prompt,
                "original_message": enriched.original_message,
                "memories_count": len(enriched.memories_used),
                "patterns_count": len(enriched.patterns_applied),
                "token_count": enriched.token_count,
                "memories": enriched.memories_used,
                "patterns": enriched.patterns_applied,
                "context": enriched.context
            }
            
        except Exception as e:
            logger.error(f"Failed to process with memory: {e}")
            raise


# Singleton instance
_orchestrator_instance = None


def get_agent_orchestrator() -> AgentOrchestrator:
    """Get singleton instance of AgentOrchestrator"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = AgentOrchestrator()
    return _orchestrator_instance
