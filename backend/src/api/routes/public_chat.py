"""
Public Chat Routes - URLs públicas para sub-agentes
Permite acesso sem autenticação para entrevistas e pesquisas
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, List
from pydantic import BaseModel

from ...services.subagent_service import SubAgentService
from ...services.interview_service import InterviewService
from ...utils.logger import logger


router = APIRouter(tags=["Public Chat"])


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatMessageRequest(BaseModel):
    """Request para enviar mensagem no chat público"""
    message: str
    interview_id: str | None = None
    context: Dict[str, Any] = {}


class ChatMessageResponse(BaseModel):
    """Response com mensagem do agente"""
    message: str
    interview_id: str
    is_complete: bool
    progress: Dict[str, Any]


class AgentInfoResponse(BaseModel):
    """Informações públicas do agente"""
    id: str
    name: str
    description: str
    slug: str
    model: str
    topics: List[str]


# ============================================================================
# Routes
# ============================================================================

@router.get("/chat/{agent_slug}")
def get_agent_info(agent_slug: str):
    """
    Retorna informações públicas do sub-agente.
    
    Usado para renderizar a página de chat pública.
    """
    try:
        service = SubAgentService()
        
        # Buscar agente pelo slug
        agent = service.get_by_slug(agent_slug)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado ou não está público")
        
        if not agent.get("is_public", True):
            raise HTTPException(status_code=403, detail="Este agente não está disponível publicamente")
        
        # Incrementar contador de acessos
        service.increment_access_count(agent["id"])
        
        return AgentInfoResponse(
            id=agent["id"],
            name=agent["name"],
            description=agent.get("description", ""),
            slug=agent["slug"],
            model=agent.get("model", "gpt-4o-mini"),
            topics=agent.get("topics", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/{agent_slug}/message")
async def send_message(agent_slug: str, request: ChatMessageRequest):
    """
    Envia mensagem para o agente e recebe resposta.
    
    Não requer autenticação - acesso público.
    """
    try:
        subagent_service = SubAgentService()
        interview_service = InterviewService()
        
        # Buscar agente
        agent = subagent_service.get_by_slug(agent_slug)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        if not agent.get("is_public", True):
            raise HTTPException(status_code=403, detail="Este agente não está disponível publicamente")
        
        # Criar ou recuperar entrevista
        if request.interview_id:
            interview = interview_service.get_interview(request.interview_id)
            if not interview:
                raise HTTPException(status_code=404, detail="Entrevista não encontrada")
        else:
            # Criar nova entrevista
            interview = interview_service.create_interview(
                subagent_id=agent["id"],
                lead_id=None  # Lead anônimo por enquanto
            )
            request.interview_id = interview["id"]
        
        # Processar mensagem com o agente
        response = await interview_service.process_message_with_agent(
            interview_id=request.interview_id,
            subagent_id=agent["id"],
            user_message=request.message
        )
        
        return ChatMessageResponse(
            message=response["message"],
            interview_id=request.interview_id,
            is_complete=response.get("is_complete", False),
            progress=response.get("progress", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{agent_slug}/interview/{interview_id}")
def get_interview_history(agent_slug: str, interview_id: str):
    """
    Retorna histórico de mensagens de uma entrevista.
    
    Permite que o usuário continue uma conversa anterior.
    """
    try:
        interview_service = InterviewService()
        
        # Buscar entrevista
        interview = interview_service.get_interview(interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Entrevista não encontrada")
        
        # Buscar mensagens
        messages = interview_service.get_messages(interview_id)
        
        return {
            "interview_id": interview_id,
            "status": interview.get("status", "in_progress"),
            "messages": messages,
            "is_complete": interview.get("status") == "completed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting interview history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/public")
def list_public_agents():
    """
    Lista todos os agentes públicos disponíveis.
    
    Útil para criar uma página de "escolha seu agente".
    """
    try:
        service = SubAgentService()
        # TODO: Implementar list_public_agents no service
        agents = []
        
        return {
            "agents": [
                {
                    "id": agent["id"],
                    "name": agent["name"],
                    "description": agent.get("description", ""),
                    "slug": agent["slug"],
                    "public_url": f"/chat/{agent['slug']}",
                    "topics": agent.get("topics", []),
                    "access_count": agent.get("access_count", 0)
                }
                for agent in agents
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing public agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
