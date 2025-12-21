"""
Agents API Routes - Sprint 09
API endpoints for managing agents and their sub-agents
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentListItem,
    AgentStats,
    AgentRole
)
from src.models.user import UserProfile
from src.models.sub_agent import (
    SubAgentCreate,
    SubAgentUpdate,
    SubAgentResponse
)
from src.services.agent_service import get_agent_service
from src.services.subagent_service import SubAgentService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/agents", tags=["agents"])


# ============================================================================
# AGENTS CRUD
# ============================================================================

@router.get("/", response_model=List[AgentListItem])
async def list_agents(
    client_id: Optional[UUID] = Query(None, description="Filter by client ID"),
    role: Optional[AgentRole] = Query(None, description="Filter by agent role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    List agents with optional filtering
    """
    agent_service = get_agent_service()
    
    try:
        agents = await agent_service.list_agents(
            client_id=client_id,
            role=role.value if role else None,
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        return agents
    except Exception as e:
        import traceback
        from src.utils.logger import logger
        logger.error(f"Erro na API de agentes: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get agent by ID
    
    Returns agent details
    """
    agent_service = get_agent_service()
    
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )


@router.get("/slug/{slug}", response_model=AgentResponse)
async def get_agent_by_slug(
    slug: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get agent by slug
    
    Returns agent details
    """
    agent_service = get_agent_service()
    
    try:
        agent = await agent_service.get_by_slug(slug)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with slug '{slug}' not found"
            )
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    data: AgentCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new agent
    
    Creates agent with provided data
    """
    agent_service = get_agent_service()
    
    try:
        agent = await agent_service.create_agent(data)
        return agent
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    data: AgentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update agent
    
    Updates agent with provided data
    """
    agent_service = get_agent_service()
    
    try:
        agent = await agent_service.update_agent(agent_id, data)
        return agent
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent: {str(e)}"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete agent
    
    Deletes agent and all associated sub-agents (CASCADE)
    """
    agent_service = get_agent_service()
    
    try:
        await agent_service.delete_agent(agent_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent: {str(e)}"
        )


@router.patch("/{agent_id}/status", response_model=AgentResponse)
async def change_agent_status(
    agent_id: UUID,
    new_status: str = Query(..., description="New status (draft, active, paused, archived)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Change agent status
    
    Updates agent status
    """
    agent_service = get_agent_service()
    
    # Validate status
    valid_statuses = ["draft", "active", "paused", "archived"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    try:
        agent = await agent_service.toggle_status(agent_id, new_status)
        return agent
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change status: {str(e)}"
        )


@router.get("/{agent_id}/stats", response_model=AgentStats)
async def get_agent_stats(
    agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Get agent statistics
    
    Returns usage statistics for agent
    """
    agent_service = get_agent_service()
    
    try:
        stats = await agent_service.get_stats(agent_id)
        return stats
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


# ============================================================================
# SUB-AGENTS NESTED ROUTES
# ============================================================================

@router.get("/{agent_id}/sub-agents", response_model=List[SubAgentResponse])
async def list_agent_subagents(
    agent_id: UUID,
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: dict = Depends(get_current_user)
):
    """
    List sub-agents of an agent
    
    Returns all sub-agents belonging to the specified agent
    """
    agent_service = get_agent_service()
    subagent_service = SubAgentService()
    
    # Verify agent exists
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify agent: {str(e)}"
        )
    
    # List sub-agents
    try:
        # Note: We need to filter by agent_id in the service
        # For now, we'll get all and filter (TODO: optimize in service)
        all_subagents = await subagent_service.list_subagents(
            is_active=is_active,
            limit=limit,
            offset=offset
        )
        
        # Filter by agent_id (this should be done in the service query)
        # TODO: Add agent_id filter to subagent_service.list_subagents()
        filtered = [sa for sa in all_subagents if hasattr(sa, 'agent_id') and str(sa.agent_id) == str(agent_id)]
        
        return filtered
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sub-agents: {str(e)}"
        )


@router.post("/{agent_id}/sub-agents", response_model=SubAgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent_subagent(
    agent_id: UUID,
    data: SubAgentCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create sub-agent for an agent
    
    Creates new sub-agent linked to the specified agent
    """
    agent_service = get_agent_service()
    subagent_service = SubAgentService()
    
    # Verify agent exists
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify agent: {str(e)}"
        )
    
    # Create sub-agent with agent_id
    try:
        # Add agent_id to data
        subagent_data = data.model_dump()
        subagent_data['agent_id'] = str(agent_id)
        
        # Create SubAgentCreate with agent_id
        from pydantic import BaseModel
        
        class SubAgentCreateWithAgent(SubAgentCreate):
            agent_id: Optional[UUID] = None
        
        subagent_create = SubAgentCreateWithAgent(**subagent_data)
        subagent = await subagent_service.create_subagent(subagent_create)
        
        return subagent
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sub-agent: {str(e)}"
        )


@router.put("/{agent_id}/sub-agents/{subagent_id}", response_model=SubAgentResponse)
async def update_agent_subagent(
    agent_id: UUID,
    subagent_id: UUID,
    data: SubAgentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update sub-agent of an agent
    
    Updates sub-agent data
    """
    agent_service = get_agent_service()
    subagent_service = SubAgentService()
    
    # Verify agent exists
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify agent: {str(e)}"
        )
    
    # Verify sub-agent exists and belongs to agent
    try:
        subagent = await subagent_service.get_subagent(subagent_id)
        if not subagent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sub-agent {subagent_id} not found"
            )
        
        # Verify ownership (if agent_id field exists)
        if hasattr(subagent, 'agent_id') and str(subagent.agent_id) != str(agent_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sub-agent {subagent_id} does not belong to agent {agent_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify sub-agent: {str(e)}"
        )
    
    # Update sub-agent
    try:
        updated_subagent = await subagent_service.update_subagent(subagent_id, data)
        return updated_subagent
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update sub-agent: {str(e)}"
        )


@router.delete("/{agent_id}/sub-agents/{subagent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_subagent(
    agent_id: UUID,
    subagent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete sub-agent of an agent
    
    Deletes sub-agent
    """
    agent_service = get_agent_service()
    subagent_service = SubAgentService()
    
    # Verify agent exists
    try:
        agent = await agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify agent: {str(e)}"
        )
    
    # Verify sub-agent exists and belongs to agent
    try:
        subagent = await subagent_service.get_subagent(subagent_id)
        if not subagent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sub-agent {subagent_id} not found"
            )
        
        # Verify ownership (if agent_id field exists)
        if hasattr(subagent, 'agent_id') and str(subagent.agent_id) != str(agent_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sub-agent {subagent_id} does not belong to agent {agent_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify sub-agent: {str(e)}"
        )
    
    # Delete sub-agent
    try:
        await subagent_service.delete_subagent(subagent_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete sub-agent: {str(e)}"
        )


# ============================================================================
# RENUS DASHBOARD (MONITORING)
# ============================================================================

@router.get("/renus/conversations")
async def get_renus_conversations(
    status: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Retorna conversas ativas do RENUS (mock para dashboard)"""
    return []

@router.get("/renus/metrics")
async def get_renus_metrics(
    current_user: dict = Depends(get_current_user)
):
    """Retorna métricas de performance do RENUS (mock para dashboard)"""
    return {
        "active_conversations": 0,
        "total_conversations_today": 0,
        "avg_response_time": 0,
        "satisfaction_rate": 0
    }



