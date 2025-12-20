"""
Marketplace API Routes
Endpoints para marketplace de templates
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models.agent import AgentListItem, AgentResponse
from src.models.user import UserProfile
from src.services.agent_service import get_agent_service
from src.api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


@router.get("/templates", response_model=List[AgentListItem])
async def list_marketplace_templates(
    niche: Optional[str] = Query(None, description="Filter by niche"),
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Lista templates disponíveis no marketplace
    Filtra automaticamente pela categoria do cliente (B2B/B2C)
    """
    agent_service = get_agent_service()
    
    try:
        # Buscar informações do cliente
        client_response = agent_service.supabase.table('clients')\
            .select('*')\
            .eq('id', str(current_user.client_id))\
            .single()\
            .execute()
        
        if not client_response.data:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client = client_response.data
        
        # Detectar categoria automaticamente
        # Se tem document (CNPJ/CPF) com 14 dígitos = B2B, senão B2C
        category = "b2b" if client.get("document") and len(client["document"]) >= 14 else "b2c"
        
        # Buscar templates
        query = agent_service.supabase.table('agents')\
            .select('*')\
            .eq('is_template', True)\
            .eq('marketplace_visible', True)
        
        if category:
            query = query.eq('category', category)
        
        if niche:
            query = query.ilike('niche', f'%{niche}%')
        
        result = query.order('created_at', desc=True).execute()
        
        return [agent_service._parse_agent_list_item(item) for item in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list templates: {str(e)}"
        )


@router.post("/templates/{template_id}/clone", response_model=AgentResponse)
async def clone_template(
    template_id: UUID,
    custom_name: Optional[str] = None,
    current_user: UserProfile = Depends(get_current_user)
):
    """
    Clona um template para o cliente atual
    """
    agent_service = get_agent_service()
    
    try:
        # Buscar template
        template_response = agent_service.supabase.table('agents')\
            .select('*')\
            .eq('id', str(template_id))\
            .single()\
            .execute()
        
        if not template_response.data:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template = template_response.data
        
        if not template.get('is_template'):
            raise HTTPException(status_code=400, detail="Agent is not a template")
        
        # Buscar cliente
        client_response = agent_service.supabase.table('clients')\
            .select('*')\
            .eq('id', str(current_user.client_id))\
            .single()\
            .execute()
        
        if not client_response.data:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client = client_response.data
        
        # Criar novo agente clonado
        from uuid import uuid4
        from datetime import datetime
        
        new_agent_id = uuid4()
        now = datetime.utcnow()
        
        new_agent_data = {
            **template,
            'id': str(new_agent_id),
            'client_id': str(current_user.client_id),
            'parent_id': str(template_id),
            'is_template': False,
            'marketplace_visible': False,
            'name': custom_name or f"{template['name']} - {client['company_name']}",
            'slug': f"{template.get('slug', 'agent')}-{new_agent_id.hex[:8]}",
            'status': 'active',
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        
        result = agent_service.supabase.table('agents').insert(new_agent_data).execute()
        
        if not result.data:
            raise Exception("Failed to clone template")
        
        return agent_service._parse_agent_response(result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clone template: {str(e)}"
        )
