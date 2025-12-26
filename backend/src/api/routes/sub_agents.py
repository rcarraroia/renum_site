"""
Task 7: Create sub-agent management APIs
GET /api/agents/{id}/sub-agents - List sub-agents
POST /api/agents/{id}/sub-agents - Create sub-agent  
PUT /api/agents/{id}/sub-agents/{sub_id} - Update sub-agent
DELETE /api/agents/{id}/sub-agents/{sub_id} - Delete sub-agent
POST /api/agents/{id}/sub-agents/{sub_id}/test - Test sub-agent
Requirements: 3.1, 3.2, 3.3, 3.4, 3.5
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import Dict, Any, List
from src.services.agent_service import get_agent_service
from src.services.sub_agent_inheritance_service import get_inheritance_service
from src.models.sub_agent import SubAgentResponse

router = APIRouter(prefix="/api/agents", tags=["sub-agents"])

@router.get("/{agent_id}/sub-agents", response_model=List[SubAgentResponse])
async def list_sub_agents(
    agent_id: UUID,
    agent_service = Depends(get_agent_service)
):
    """List all sub-agents of an agent - TEMPORARY: No auth for testing"""
    """List all sub-agents of an agent"""
    result = agent_service.supabase.table('sub_agents')\
        .select('*')\
        .eq('parent_agent_id', str(agent_id))\
        .execute()
    
    # Mapear dados do banco para o modelo SubAgentResponse
    sub_agents = []
    for data in result.data:
        # Extrair campos do config
        config = data.get('config', {})
        identity = config.get('identity', {})
        
        # Criar objeto compatível com SubAgentResponse
        sub_agent_data = {
            'id': data['id'],
            'agent_id': data.get('parent_agent_id'),
            'name': data['name'],
            'description': identity.get('persona', f"Sub-agente especializado em {data.get('specialization', 'geral')}"),
            'channel': config.get('channel', 'whatsapp'),
            'system_prompt': identity.get('system_prompt', 'Você é um assistente especializado.'),
            'topics': config.get('topics', []),
            'model': config.get('model', 'gpt-4o-mini'),
            'is_active': data.get('is_active', True),
            'fine_tuning_config': config.get('fine_tuning_config'),
            'config_id': None,  # Campo opcional
            'slug': None,  # Campo opcional
            'public_url': None,  # Campo opcional
            'access_count': 0,  # Campo opcional
            'is_public': True,  # Campo opcional
            'knowledge_base': None,  # Campo opcional
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
        
        sub_agents.append(SubAgentResponse(**sub_agent_data))
    
    return sub_agents

@router.post("/{agent_id}/sub-agents")
async def create_sub_agent(
    agent_id: UUID,
    sub_agent_data: Dict[str, Any],
    agent_service = Depends(get_agent_service)
):
    """Create new sub-agent"""
    sub_agent = agent_service.create_sub_agent(
        parent_id=agent_id,
        name=sub_agent_data['name'],
        specialization=sub_agent_data['specialization'],
        inheritance_config=sub_agent_data.get('inheritance_config', {}),
        config=sub_agent_data.get('config', {})
    )
    return sub_agent

@router.put("/{agent_id}/sub-agents/{sub_agent_id}")
async def update_sub_agent(
    agent_id: UUID,
    sub_agent_id: UUID,
    update_data: Dict[str, Any],
    agent_service = Depends(get_agent_service)
):
    """Update sub-agent"""
    result = agent_service.supabase.table('sub_agents')\
        .update(update_data)\
        .eq('id', str(sub_agent_id))\
        .eq('parent_agent_id', str(agent_id))\
        .execute()
    
    return result.data[0]

@router.delete("/{agent_id}/sub-agents/{sub_agent_id}")
async def delete_sub_agent(
    agent_id: UUID,
    sub_agent_id: UUID,
    agent_service = Depends(get_agent_service)
):
    """Delete sub-agent"""
    result = agent_service.supabase.table('sub_agents')\
        .delete()\
        .eq('id', str(sub_agent_id))\
        .eq('parent_agent_id', str(agent_id))\
        .execute()
    
    return {"message": "Sub-agent deleted"}

@router.post("/{agent_id}/sub-agents/{sub_agent_id}/test")
async def test_sub_agent(
    agent_id: UUID,
    sub_agent_id: UUID,
    test_context: Dict[str, Any],
    inheritance_service = Depends(get_inheritance_service)
):
    """Test sub-agent activation and effective configuration"""
    # Get sub-agent
    result = inheritance_service.supabase.table('sub_agents')\
        .select('*')\
        .eq('id', str(sub_agent_id))\
        .single()\
        .execute()
    
    sub_agent = result.data
    
    # Test routing
    should_activate = inheritance_service.evaluate_routing_conditions(
        sub_agent['routing_config'],
        test_context
    )
    
    # Get effective config
    from src.services.agent_service import get_agent_service
    agent_service = get_agent_service()
    parent = agent_service.get_agent(agent_id)
    
    effective_config = inheritance_service.calculate_effective_config(
        parent.config,
        sub_agent['config'],
        sub_agent['inheritance_config']
    )
    
    return {
        "should_activate": should_activate,
        "effective_config": effective_config,
        "test_context": test_context
    }
