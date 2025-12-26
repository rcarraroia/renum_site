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
from src.utils.logger import logger

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
    memory_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new memory
    
    REGRA: agent_id deve existir e ter client_id associado.
    Memórias só precisam de agent_id (client_id é derivado do agente).
    
    Se agente não tem client_id → ERRO 500 (configuração errada no banco)
    """
    from src.utils.supabase_client import get_client
    import uuid
    
    embedding_service = get_embedding_service()
    
    try:
        # 1. Validar agent_id
        agent_id = memory_data.get('agent_id')
        if not agent_id or agent_id == 'None' or str(agent_id).lower() == 'none':
            raise HTTPException(status_code=400, detail="agent_id é obrigatório")
        
        content = memory_data.get('content')
        if not content or not content.strip():
            raise HTTPException(status_code=400, detail="content é obrigatório")
        
        # 2. Validar formato UUID
        try:
            agent_uuid = UUID(str(agent_id))
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail=f"Formato de agent_id inválido: {agent_id}")
        
        # 3. Buscar agente e validar client_id
        supabase = get_client()
        agent_result = supabase.table("agents").select("id, client_id, name").eq("id", str(agent_uuid)).execute()
        
        if not agent_result.data:
            raise HTTPException(status_code=404, detail=f"Agente {agent_uuid} não encontrado")
        
        agent_data = agent_result.data[0]
        
        # 4. CRÍTICO: Validar que agente tem client_id
        if not agent_data.get("client_id"):
            raise HTTPException(
                status_code=500,
                detail=f"ERRO DE CONFIGURAÇÃO: Agente '{agent_data.get('name', agent_uuid)}' não tem client_id. "
                       f"Todos os agentes devem ter client_id associado. "
                       f"Execute o script SQL: scripts/setup_client_architecture.sql"
            )
        
        # 5. Generate embedding
        try:
            embedding = embedding_service.generate_embedding(content)
        except Exception as e:
            logger.warning(f"Could not generate embedding: {e}")
            embedding = None
        
        # 6. Map chunk_type to valid enum value
        chunk_type = memory_data.get('chunk_type', 'insight')
        valid_types = ['business_term', 'process', 'faq', 'product', 'objection', 'pattern', 'insight', 'general']
        if chunk_type not in valid_types:
            chunk_type = 'insight'  # Default
        
        # 7. Create memory record (SÓ agent_id, NÃO client_id)
        memory_record = {
            'id': str(uuid.uuid4()),
            'agent_id': str(agent_uuid),
            'content': content.strip(),
            'chunk_type': chunk_type,
            'confidence_score': float(memory_data.get('confidence_score', 0.8)),
            'is_active': True,
            'usage_count': 0,
            'metadata': memory_data.get('metadata', {})
        }
        
        # Only add embedding if generated successfully
        if embedding:
            memory_record['embedding'] = embedding
        
        result = supabase.table("memory_chunks").insert(memory_record).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Falha ao criar memória - nenhum dado retornado")
        
        logger.info(f"Memory created for agent {agent_data.get('name')} (client: {agent_data.get('client_id')[:8]}...)")
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao criar memória: {str(e)}"
        )


@router.put("/{memory_id}")
async def update_memory(
    memory_id: UUID,
    memory_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Update memory
    
    Accepts simplified input: content, chunk_type, confidence_score (all optional)
    """
    from src.utils.supabase_client import get_client
    
    embedding_service = get_embedding_service()
    
    try:
        supabase = get_client()
        
        # Build update dict with only provided fields
        update_dict = {}
        
        if 'content' in memory_data and memory_data['content']:
            update_dict['content'] = memory_data['content']
            # Regenerate embedding for new content
            update_dict['embedding'] = embedding_service.generate_embedding(memory_data['content'])
        
        if 'chunk_type' in memory_data:
            valid_types = ['business_term', 'process', 'faq', 'product', 'objection', 'pattern', 'insight']
            chunk_type = memory_data['chunk_type']
            if chunk_type in valid_types:
                update_dict['chunk_type'] = chunk_type
        
        if 'confidence_score' in memory_data:
            update_dict['confidence_score'] = memory_data['confidence_score']
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        # Update in database
        result = supabase.table("memory_chunks").update(update_dict).eq("id", str(memory_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found"
            )
        return result.data[0]
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
