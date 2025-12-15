"""
ISA (Intelligent System Assistant) Routes
Rotas para interação com o assistente administrativo
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from src.api.middleware.auth_middleware import get_current_user
from src.utils.logger import logger
from src.agents.isa import IsaAgent
from src.services.isa_command_service import IsaCommandService


from src.services.agent_service import get_agent_service
from src.models.agent import AgentRole

router = APIRouter(prefix="/isa", tags=["ISA"])

class IsaChatRequest(BaseModel):
    """Request para chat com ISA"""
    message: str


class IsaChatResponse(BaseModel):
    """Response do chat com ISA"""
    message: str
    command_executed: bool = False
    result: Dict[str, Any] = {}


@router.post("/chat", response_model=IsaChatResponse)
async def chat_with_isa(
    request: IsaChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Envia mensagem para ISA e recebe resposta.
    
    Apenas admins podem usar ISA.
    """
    # Verificar se é admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can use ISA"
        )
    
    try:
        logger.info(f"ISA chat request from admin {current_user.id}: {request.message}")
        
        # Carregar Agente ISA Real do Banco
        agent_service = get_agent_service()
        db_agent = await agent_service.get_system_agent(AgentRole.SYSTEM_SUPERVISOR)
        
        if db_agent:
            logger.info(f"Inicializando ISA Real (ID: {db_agent.id}, Model: {db_agent.model})")
            # Configuração dinâmica carregada do DB
            agent = IsaAgent(
                model=db_agent.model,
                system_prompt=db_agent.system_prompt
            )
        else:
            logger.warning("ISA não encontrada no banco. Usando fallback hardcoded.")
            agent = IsaAgent()

        command_service = IsaCommandService()
        
        # Criar mensagem no formato BaseMessage
        from langchain_core.messages import HumanMessage
        messages = [HumanMessage(content=request.message)]
        
        # Criar contexto
        context = {
            "admin_id": str(current_user.id),
            "is_admin": current_user.role == "admin",
            "user_id": str(current_user.id)
        }
        
        # Invocar agente com mensagem e contexto separados
        result = await agent.invoke(messages, context)
        
        # Extrair resposta e dados
        response_text = result.get("response", "Desculpe, não consegui processar sua solicitação.")
        command_executed = result.get("executed", False)
        command_data = result.get("data", {})
        
        # Salvar comando para auditoria
        try:
            await command_service.log_command(
                admin_id=current_user.id,
                user_message=request.message,
                assistant_response=response_text,
                command_executed=command_executed,
                execution_result=command_data
            )
        except Exception as audit_error:
            logger.warning(f"Failed to save ISA command audit: {audit_error}")
        
        return IsaChatResponse(
            message=response_text,
            command_executed=command_executed,
            result=command_data
        )
        
    except Exception as e:
        logger.error(f"Error in ISA chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ISA error: {str(e)}"
        )


@router.get("/history")
async def get_isa_history(
    current_user: dict = Depends(get_current_user),
    limit: int = 50
):
    """
    Retorna histórico de comandos ISA executados.
    
    Apenas admins podem acessar.
    """
    # Verificar se é admin
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access ISA history"
        )
    
    try:
        from src.config.supabase import supabase_admin
        
        logger.info(f"ISA history request from admin {current_user.get('id')}")
        
        # Buscar comandos do admin atual
        response = supabase_admin.table('isa_commands')\
            .select('*')\
            .eq('admin_id', current_user.get('id'))\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return {
            "commands": response.data or [],
            "total": len(response.data) if response.data else 0
        }
        
    except Exception as e:
        logger.error(f"Error fetching ISA history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching ISA history: {str(e)}"
        )
