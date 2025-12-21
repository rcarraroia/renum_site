"""
Task 5: Implement configuration API endpoints
GET /api/agents/{id}/config - Get full configuration
PUT /api/agents/{id}/config/{tab} - Update specific tab
POST /api/agents/{id}/config/validate - Validate configuration
GET /api/agents/{id}/config/export - Export configuration
Requirements: 2.1, 2.2, 2.3, 2.4, 2.5
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import Dict, Any, Literal
from src.services.agent_service import get_agent_service

router = APIRouter(prefix="/api/agents", tags=["configuration"])

TabName = Literal[
    'instructions', 'intelligence', 'tools', 'integrations',
    'knowledge', 'triggers', 'guardrails', 'sub_agents', 'advanced'
]

@router.get("/{agent_id}/config")
async def get_agent_config(
    agent_id: UUID,
    agent_service = Depends(get_agent_service)
):
    """Get full agent configuration (all 9 tabs)"""
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": str(agent_id),
        "config": agent.config
    }

@router.get("/{agent_id}/config/{tab}")
async def get_config_tab(
    agent_id: UUID,
    tab: TabName,
    agent_service = Depends(get_agent_service)
):
    """Get specific configuration tab"""
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if tab not in agent.config:
        return {
            "agent_id": str(agent_id),
            "tab": tab,
            "config": {}
        }
    
    return {
        "agent_id": str(agent_id),
        "tab": tab,
        "config": agent.config[tab]
    }

@router.put("/{agent_id}/config/{tab}")
async def update_config_tab(
    agent_id: UUID,
    tab: TabName,
    config_data: Dict[str, Any],
    agent_service = Depends(get_agent_service)
):
    """Update specific configuration tab"""
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get current config
    current_config = agent.config.copy()
    
    # Update specific tab
    current_config[tab] = config_data
    
    # Update agent
    from src.models.agent import AgentUpdate
    updated_agent = agent_service.update_agent(
        agent_id,
        AgentUpdate(config=current_config)
    )
    
    return {
        "agent_id": str(agent_id),
        "tab": tab,
        "config": updated_agent.config[tab],
        "message": f"Tab '{tab}' updated successfully"
    }

@router.post("/{agent_id}/config/validate")
async def validate_config(
    agent_id: UUID,
    config_data: Dict[str, Any],
    agent_service = Depends(get_agent_service)
):
    """Validate configuration structure and values"""
    errors = []
    
    # Validate 9-category structure
    required_categories = [
        'instructions', 'intelligence', 'tools', 'integrations',
        'knowledge', 'triggers', 'guardrails', 'sub_agents', 'advanced'
    ]
    
    for category in required_categories:
        if category not in config_data:
            errors.append(f"Missing category: {category}")
    
    # Validate instructions
    if 'instructions' in config_data:
        instructions = config_data['instructions']
        if not instructions.get('system_prompt'):
            errors.append("instructions.system_prompt is required")
    
    # Validate intelligence
    if 'intelligence' in config_data:
        intelligence = config_data['intelligence']
        if 'temperature' in intelligence:
            temp = intelligence['temperature']
            if not (0 <= temp <= 1):
                errors.append("intelligence.temperature must be between 0 and 1")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

@router.get("/{agent_id}/config/export")
async def export_config(
    agent_id: UUID,
    format: Literal['json', 'yaml'] = 'json',
    agent_service = Depends(get_agent_service)
):
    """Export agent configuration"""
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    export_data = {
        "agent_id": str(agent.id),
        "name": agent.name,
        "description": agent.description,
        "type": {
            "is_template": agent.is_template,
            "is_system": agent.is_system,
            "category": agent.category,
            "niche": agent.niche
        },
        "config": agent.config,
        "exported_at": agent.updated_at.isoformat()
    }
    
    if format == 'yaml':
        import yaml
        return yaml.dump(export_data, default_flow_style=False)
    
    return export_data
