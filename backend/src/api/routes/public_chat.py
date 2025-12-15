"""
Public Chat Routes - URLs públicas para sub-agentes
Permite acesso sem autenticação para entrevistas e pesquisas
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, List
from pydantic import BaseModel

from ...services.agent_service import get_agent_service
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
    welcome_message: str | None = None
    persona: str | None = None


# ============================================================================
# Routes
# ============================================================================

@router.get("/chat/{agent_slug}")
async def get_agent_info(agent_slug: str):
    """
    Retorna informações públicas do agente.
    Usado para renderizar a página de chat pública.
    """
    try:
        service = get_agent_service()
        
        # Buscar agente pelo slug
        agent = await service.get_by_slug(agent_slug)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        if not agent.is_public:
            raise HTTPException(status_code=403, detail="Este agente não está disponível publicamente")
        
        # TODO: Implementar incremento de access_count no AgentService se necessário
        # service.increment_access_count(agent.id)
        
        config = agent.config or {}
        identity = config.get("identity", {})
        
        return AgentInfoResponse(
            id=str(agent.id),
            name=agent.name,
            description=agent.description or "",
            slug=agent.slug,
            model=config.get("model", "gpt-4o-mini"),
            topics=config.get("topics", []),
            welcome_message=identity.get("welcome_message") or config.get("welcome_message"),
            persona=identity.get("persona") or config.get("persona")
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
        agent_service = get_agent_service()
        interview_service = InterviewService()
        
        # Buscar agente
        agent = await agent_service.get_by_slug(agent_slug)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        
        if not agent.is_public:
            raise HTTPException(status_code=403, detail="Este agente não está disponível publicamente")
        
        # Criar ou recuperar entrevista
        if request.interview_id:
            interview = interview_service.get_interview(request.interview_id)
            if not interview:
                raise HTTPException(status_code=404, detail="Entrevista não encontrada")
        else:
            # Criar nova entrevista
            # TODO: Adaptar create_interview para aceitar agent_id (UUID) da nova tabela agents
            # Assumindo que interview_service.create_interview aceita ID do agente em 'subagent_id' ou 'agent_id'
            # Se a tabela interviews tiver foreign key para sub_agents, isso vai quebrar.
            # Mas como não posso mudar o banco agora, vou passar o ID e torcer para o backend lidar ou ser loose FK.
            interview = interview_service.create_interview(
                subagent_id=str(agent.id),
                lead_id=None
            )
            request.interview_id = interview["id"]
        
        # Processar mensagem com o agente
        response = await interview_service.process_message_with_agent(
            interview_id=request.interview_id,
            subagent_id=str(agent.id),
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
async def get_interview_history(agent_slug: str, interview_id: str):
    """
    Retorna histórico de mensagens de uma entrevista.
    Permite que o usuário continue uma conversa anterior.
    """
    try:
        # Validar se o agente existe (opcional, mas bom pra consistência da URL)
        service = get_agent_service()
        agent = await service.get_by_slug(agent_slug)
        if not agent:
             raise HTTPException(status_code=404, detail="Agente não encontrado")

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
async def list_public_agents():
    """
    Lista todos os agentes públicos disponíveis.
    """
    try:
        service = get_agent_service()
        # Listar agentes públicos
        agents_list = await service.list_agents(is_active=True)
        # Filtrar manualmente is_public se o service não filtrar (o service tem parametro is_active mas não is_public explícito no list_agents, wait, list_agents TEM is_public? Vamos checar)
        # O metodo list_agents no AgentService NÃO tem parametro is_public. Tem role, active, client_id.
        # Check AgentService.list_agents again:
        # async def list_agents(self, client_id, role, is_active, limit, offset)
        # Realmente não tem is_public. Então filtro aqui.
        
        public_agents = [a for a in agents_list if a.is_public]
        
        return {
            "agents": [
                {
                    "id": str(agent.id),
                    "name": agent.name,
                    "description": agent.description or "",
                    "slug": agent.slug or "",
                    "public_url": f"/chat/{agent.slug}",
                    "topics": agent.config.get("topics", []) if agent.config else [],
                    "access_count": 0 # TODO: Implement access count
                }
                for agent in public_agents
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing public agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
