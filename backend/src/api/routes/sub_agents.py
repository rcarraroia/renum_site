"""
API routes for sub-agents management.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.sub_agent import SubAgentCreate, SubAgentUpdate, SubAgentResponse
from src.services.subagent_service import SubAgentService
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/sub-agents", tags=["sub-agents"])


@router.get("/", response_model=List[SubAgentResponse])
async def list_sub_agents(
    active_only: bool = False,
    agent_type: str = None,
    current_user: dict = Depends(get_current_user)
):
    """List all sub-agents."""
    service = SubAgentService()
    return service.list_sub_agents(active_only=active_only, agent_type=agent_type)


@router.get("/{sub_agent_id}", response_model=SubAgentResponse)
async def get_sub_agent(
    sub_agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Get sub-agent by ID."""
    service = SubAgentService()
    sub_agent = service.get_sub_agent(sub_agent_id)
    if not sub_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-agent not found"
        )
    return sub_agent


@router.post("/", response_model=SubAgentResponse, status_code=status.HTTP_201_CREATED)
async def create_sub_agent(
    sub_agent_data: SubAgentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new sub-agent."""
    # Only admins can create sub-agents
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create sub-agents"
        )
    
    service = SubAgentService()
    return service.create_sub_agent(sub_agent_data)


@router.put("/{sub_agent_id}", response_model=SubAgentResponse)
async def update_sub_agent(
    sub_agent_id: UUID,
    sub_agent_data: SubAgentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update sub-agent."""
    # Only admins can update sub-agents
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update sub-agents"
        )
    
    service = SubAgentService()
    sub_agent = service.update_sub_agent(sub_agent_id, sub_agent_data)
    if not sub_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-agent not found"
        )
    return sub_agent


@router.delete("/{sub_agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sub_agent(
    sub_agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Delete sub-agent."""
    # Only admins can delete sub-agents
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete sub-agents"
        )
    
    service = SubAgentService()
    success = service.delete_sub_agent(sub_agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-agent not found"
        )



@router.patch("/{sub_agent_id}/toggle", response_model=SubAgentResponse)
async def toggle_sub_agent(
    sub_agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Toggle sub-agent active status."""
    # Only admins can toggle sub-agents
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can toggle sub-agents"
        )
    
    service = SubAgentService()
    try:
        return await service.toggle_active(sub_agent_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{sub_agent_id}/stats")
async def get_sub_agent_stats(
    sub_agent_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Get sub-agent usage statistics."""
    service = SubAgentService()
    
    # Verificar se sub-agent existe
    sub_agent = await service.get_subagent(sub_agent_id)
    if not sub_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub-agent not found"
        )
    
    # Buscar estatísticas de uso
    from src.config.supabase import supabase_admin
    
    try:
        # Total de entrevistas
        total_interviews = supabase_admin.table('interviews')\
            .select('id', count='exact')\
            .eq('subagent_id', str(sub_agent_id))\
            .execute()
        
        # Entrevistas completadas
        completed_interviews = supabase_admin.table('interviews')\
            .select('id', count='exact')\
            .eq('subagent_id', str(sub_agent_id))\
            .eq('status', 'completed')\
            .execute()
        
        # Entrevistas em andamento
        in_progress_interviews = supabase_admin.table('interviews')\
            .select('id', count='exact')\
            .eq('subagent_id', str(sub_agent_id))\
            .eq('status', 'in_progress')\
            .execute()
        
        total = total_interviews.count or 0
        completed = completed_interviews.count or 0
        in_progress = in_progress_interviews.count or 0
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            "sub_agent_id": str(sub_agent_id),
            "total_interviews": total,
            "completed_interviews": completed,
            "in_progress_interviews": in_progress,
            "abandoned_interviews": total - completed - in_progress,
            "completion_rate": round(completion_rate, 2),
            "access_count": sub_agent.access_count or 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching stats: {str(e)}"
        )
