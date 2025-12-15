"""
SICC Memory API Routes - Sprint 10
API endpoints for managing agent memories
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.sicc.memory import (
    MemoryChunkCreate,
    MemoryChunkUpdate,
    MemoryChunkResponse,
    MemorySearchQuery,
    MemorySearchResult,
    ChunkType
)
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.embedding_service import get_embedding_service
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/sicc/memories", tags=["sicc-memory"])


@router.get("/", response_model=List[MemoryChunkResponse])
async def list_memories(
    agent_id: UUID = Query(..., description="Agent ID"),
    chunk_type: Optional[ChunkType] = Query(None, description="Filter by type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """
    List memories for an agent with optional filtering
    
    Returns paginated list of memories
    """
    memory_service = MemoryService()
    
    try:
        memories = await memory_service.list_memories(
            agent_id=agent_id,
            chunk_type=chunk_type,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        return memories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list memories: {str(e)}"
        )


@router.get("/{memory_id}", response_model=MemoryChunkResponse)
async def get_memory(
    memory_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get memory by ID
    
    Returns memory details
    """
    memory_service = MemoryService()
    
    try:
        memory = await memory_service.get_memory(memory_id)
        if not memory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found"
            )
        return memory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory: {str(e)}"
        )


@router.post("/", response_model=MemoryChunkResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory_data: MemoryChunkCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new memory
    
    Automatically generates embedding for content
    """
    memory_service = MemoryService()
    embedding_service = get_embedding_service()
    
    try:
        # Generate embedding if not provided
        if not memory_data.embedding:
            memory_data.embedding = embedding_service.generate_embedding(memory_data.content)
        
        memory = await memory_service.create_memory(memory_data)
        return memory
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create memory: {str(e)}"
        )


@router.put("/{memory_id}", response_model=MemoryChunkResponse)
async def update_memory(
    memory_id: UUID,
    memory_data: MemoryChunkUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update memory
    
    Creates new version maintaining history
    """
    memory_service = MemoryService()
    embedding_service = get_embedding_service()
    
    try:
        # Regenerate embedding if content changed
        if memory_data.content:
            memory_data.embedding = embedding_service.generate_embedding(memory_data.content)
        
        memory = await memory_service.update_memory(memory_id, memory_data)
        if not memory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found"
            )
        return memory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update memory: {str(e)}"
        )


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete memory
    
    Soft delete (marks as inactive)
    """
    memory_service = MemoryService()
    
    try:
        success = await memory_service.delete_memory(memory_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete memory: {str(e)}"
        )


@router.post("/search", response_model=List[MemorySearchResult])
async def search_memories(
    search_query: MemorySearchQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Search memories using similarity search
    
    Returns memories ranked by relevance
    """
    memory_service = MemoryService()
    
    try:
        results = await memory_service.search_memories(search_query)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search memories: {str(e)}"
        )


@router.get("/agent/{agent_id}/stats")
async def get_memory_stats(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get memory statistics for agent
    
    Returns counts by type, usage stats, etc
    """
    memory_service = MemoryService()
    
    try:
        stats = await memory_service.get_memory_stats(agent_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory stats: {str(e)}"
        )
