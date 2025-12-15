"""
Memory Service - Agent Memory Management
Sprint 10 - SICC Implementation

Service for managing agent adaptive memory with vector similarity search.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from ...config.supabase import supabase_admin
from ...models.sicc.memory import (
    MemoryChunkCreate,
    MemoryChunkUpdate,
    MemoryChunkResponse,
    MemorySearchQuery,
    MemorySearchResult,
    ChunkType
)
from ...utils.logger import logger
from .embedding_service import get_embedding_service


class MemoryService:
    """Service for managing agent memory chunks"""
    
    def __init__(self):
        """Initialize service with Supabase admin client and embedding service"""
        self.supabase = supabase_admin
        self.embedding_service = get_embedding_service()
    
    async def create_memory(self, data: MemoryChunkCreate) -> MemoryChunkResponse:
        """
        Create a new memory chunk.
        
        Args:
            data: MemoryChunkCreate with memory data
        
        Returns:
            MemoryChunkResponse with created memory
        
        Raises:
            Exception: If creation fails
        """
        try:
            logger.info(
                f"Creating memory for agent {data.agent_id}: "
                f"{data.chunk_type} ({len(data.content)} chars)"
            )
            
            # Prepare data for insertion
            memory_data = {
                "agent_id": str(data.agent_id),
                "client_id": str(data.client_id),
                "content": data.content,
                "chunk_type": data.chunk_type.value,
                "embedding": data.embedding,
                "metadata": data.metadata or {},
                "source": data.source,
                "confidence_score": data.confidence_score,
                "version": 1
                # usage_count has default value 0 in database
            }
            
            # Insert into database
            result = self.supabase.table("agent_memory_chunks").insert(memory_data).execute()
            
            if not result.data:
                raise Exception("Failed to create memory chunk")
            
            memory = result.data[0]
            logger.info(f"Successfully created memory {memory['id']}")
            
            return MemoryChunkResponse(**memory)
            
        except Exception as e:
            logger.error(f"Failed to create memory: {e}")
            raise
    
    async def create_memory_from_text(
        self,
        agent_id: UUID,
        client_id: UUID,
        content: str,
        chunk_type: ChunkType,
        metadata: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        confidence: float = 1.0
    ) -> MemoryChunkResponse:
        """
        Create memory chunk from text (generates embedding automatically).
        
        Args:
            agent_id: Agent ID
            client_id: Client ID
            content: Memory content text
            chunk_type: Type of memory chunk
            metadata: Additional metadata
            source: Source of memory
            confidence: Confidence score
                    
        Returns:
            MemoryChunkResponse with created memory
        """
        try:
            logger.info(f"Creating memory from text for agent {agent_id}")
            
            # Generate embedding
            embedding = self.embedding_service.generate_embedding(content)
            
            # Create memory data
            memory_data = MemoryChunkCreate(
                agent_id=agent_id,
                client_id=client_id,
                content=content,
                chunk_type=chunk_type,
                embedding=embedding,
                metadata=metadata or {},
                source=source,
                confidence_score=confidence
            )
            
            return await self.create_memory(memory_data)
            
        except Exception as e:
            logger.error(f"Failed to create memory from text: {e}")
            raise
    
    async def get_memory(self, memory_id: UUID) -> Optional[MemoryChunkResponse]:
        """
        Get memory chunk by ID.
        
        Args:
            memory_id: Memory chunk ID
        
        Returns:
            MemoryChunkResponse or None if not found
        """
        try:
            result = self.supabase.table("agent_memory_chunks").select("*").eq(
                "id", str(memory_id)
            ).execute()
            
            if not result.data:
                return None
            
            return MemoryChunkResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to get memory {memory_id}: {e}")
            raise
    
    async def update_memory(
        self,
        memory_id: UUID,
        data: MemoryChunkUpdate
    ) -> MemoryChunkResponse:
        """
        Update memory chunk.
        
        Args:
            memory_id: Memory chunk ID
            data: MemoryChunkUpdate with update data
        
        Returns:
            MemoryChunkResponse with updated memory
        
        Raises:
            Exception: If update fails
        """
        try:
            logger.info(f"Updating memory {memory_id}")
            
            # Prepare update data (only include non-None fields)
            update_data = {
                k: v for k, v in data.model_dump(exclude_unset=True).items()
                if v is not None
            }
            
            if not update_data:
                raise ValueError("No fields to update")
            
            # Convert enum to value if present
            if "chunk_type" in update_data:
                update_data["chunk_type"] = update_data["chunk_type"].value
            
            # Increment version
            current = await self.get_memory(memory_id)
            if not current:
                raise ValueError(f"Memory {memory_id} not found")
            
            update_data["version"] = current.version + 1
            
            # Update in database
            result = self.supabase.table("agent_memory_chunks").update(
                update_data
            ).eq("id", str(memory_id)).execute()
            
            if not result.data:
                raise Exception("Failed to update memory chunk")
            
            logger.info(f"Successfully updated memory {memory_id}")
            return MemoryChunkResponse(**result.data[0])
            
        except Exception as e:
            logger.error(f"Failed to update memory {memory_id}: {e}")
            raise
    
    async def delete_memory(self, memory_id: UUID) -> bool:
        """
        Delete memory chunk.
        
        Args:
            memory_id: Memory chunk ID
        
        Returns:
            True if deleted successfully
        """
        try:
            logger.info(f"Deleting memory {memory_id}")
            
            result = self.supabase.table("agent_memory_chunks").delete().eq(
                "id", str(memory_id)
            ).execute()
            
            logger.info(f"Successfully deleted memory {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory {memory_id}: {e}")
            raise
    
    async def search_memories(
        self,
        query: MemorySearchQuery
    ) -> List[MemorySearchResult]:
        """
        Search memories using vector similarity.
        
        Args:
            query: MemorySearchQuery with search parameters
        
        Returns:
            List of MemorySearchResult ordered by relevance
        """
        try:
            logger.info(
                f"Searching memories for agent {query.agent_id}: "
                f"'{query.query_text[:50]}...'"
            )
            
            # Generate embedding for query
            query_embedding = self.embedding_service.generate_embedding(query.query_text)
            
            # Build SQL query for vector similarity search
            # Using pgvector's <=> operator for cosine distance
            sql_query = self.supabase.table("agent_memory_chunks").select("*")
            
            # Filter by agent
            sql_query = sql_query.eq("agent_id", str(query.agent_id))
            
            # Filter by memory types if specified
            if query.chunk_types:
                types = [mt.value for mt in query.chunk_types]
                sql_query = sql_query.in_("chunk_type", types)
            
            # Filter by confidence
            if query.min_confidence > 0:
                sql_query = sql_query.gte("confidence_score", query.min_confidence)
            
            # Execute query
            result = sql_query.execute()
            
            if not result.data:
                logger.info("No memories found")
                return []
            
            # Calculate similarity scores and filter
            search_results = []
            
            for memory_data in result.data:
                memory = MemoryChunkResponse(**memory_data)
                
                # Get embedding from database (convert if needed)
                db_embedding = memory_data["embedding"]
                if isinstance(db_embedding, str):
                    # Parse pgvector format: "[0.1, 0.2, ...]"
                    import json
                    db_embedding = json.loads(db_embedding)
                
                # Calculate similarity
                similarity = self.embedding_service.cosine_similarity(
                    query_embedding,
                    db_embedding
                )
                
                # Filter by similarity threshold
                if similarity < query.similarity_threshold:
                    continue
                
                # Calculate relevance score (weighted combination)
                # Normalize usage_count to 0-1 range (assuming max 100 uses)
                normalized_usage = min(memory.usage_count / 100.0, 1.0)
                
                relevance = (
                    similarity * 0.6 +
                    memory.confidence_score * 0.2 +
                    normalized_usage * 0.2
                )
                
                search_results.append(
                    MemorySearchResult(
                        memory=memory,
                        similarity_score=similarity,
                        relevance_score=relevance
                    )
                )
            
            # Sort by relevance score (descending)
            search_results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            # Limit results
            search_results = search_results[:query.limit]
            
            logger.info(f"Found {len(search_results)} relevant memories")
            return search_results
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            raise
    
    async def increment_usage_count(self, memory_id: UUID) -> None:
        """
        Increment access count for memory chunk.
        
        Args:
            memory_id: Memory chunk ID
        """
        try:
            # Get current count
            memory = await self.get_memory(memory_id)
            if not memory:
                return
            
            # Increment count and update last used
            self.supabase.table("agent_memory_chunks").update({
                "usage_count": memory.usage_count + 1,
                "last_used_at": datetime.utcnow().isoformat()
            }).eq("id", str(memory_id)).execute()
            
        except Exception as e:
            logger.warning(f"Failed to increment access count for {memory_id}: {e}")
    
    async def get_agent_memories(
        self,
        agent_id: UUID,
        chunk_type: Optional[ChunkType] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[MemoryChunkResponse]:
        """
        Get all memories for an agent.
        
        Args:
            agent_id: Agent ID
            chunk_type: Optional filter by chunk type
            limit: Maximum number of results
            offset: Offset for pagination
        
        Returns:
            List of MemoryChunkResponse
        """
        try:
            query = self.supabase.table("agent_memory_chunks").select("*").eq(
                "agent_id", str(agent_id)
            )
            
            if chunk_type:
                query = query.eq("chunk_type", chunk_type.value)
            
            query = query.order("created_at", desc=True).range(offset, offset + limit - 1)
            
            result = query.execute()
            
            return [MemoryChunkResponse(**m) for m in result.data]
            
        except Exception as e:
            logger.error(f"Failed to get agent memories: {e}")
            raise
    
    async def get_memory_stats(self, agent_id: UUID) -> Dict[str, Any]:
        """
        Get memory statistics for an agent.
        
        Args:
            agent_id: Agent ID
        
        Returns:
            Dictionary with memory statistics
        """
        try:
            # Get all memories for agent
            result = self.supabase.table("agent_memory_chunks").select(
                "chunk_type, confidence_score, usage_count"
            ).eq("agent_id", str(agent_id)).execute()
            
            if not result.data:
                return {
                    "total_memories": 0,
                    "by_type": {},
                    "avg_confidence": 0.0,
                    "avg_usage": 0.0,
                    "total_accesses": 0
                }
            
            memories = result.data
            
            # Calculate statistics
            by_type = {}
            total_confidence = 0.0
            total_usage = 0.0
            total_accesses = 0
            
            for memory in memories:
                # Count by type
                mem_type = memory["chunk_type"]
                by_type[mem_type] = by_type.get(mem_type, 0) + 1
                
                # Sum metrics
                total_confidence += memory["confidence_score"]
                total_usage += memory["usage_count"]
                total_accesses += memory["usage_count"]
            
            total = len(memories)
            
            return {
                "total_memories": total,
                "by_type": by_type,
                "avg_confidence": total_confidence / total if total > 0 else 0.0,
                "avg_usage": total_usage / total if total > 0 else 0.0,
                "total_accesses": total_accesses
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory stats: {e}")
            raise
