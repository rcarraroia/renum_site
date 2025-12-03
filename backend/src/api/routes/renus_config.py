"""
RENUS Config Routes - Gerenciamento de configurações do agente RENUS
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from ...services.renus_config_service import RenusConfigService
from ...models.renus_config import RenusConfigUpdate, RenusConfigResponse
from ...api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/renus-config", tags=["renus-config"])


@router.get("/", response_model=RenusConfigResponse)
async def get_config(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Busca configuração do RENUS para o cliente atual
    
    Returns:
        Configuração completa do RENUS
    """
    service = RenusConfigService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client_id not found in token"
        )
    
    config = service.get_config(client_id)
    
    if not config:
        # Criar configuração padrão se não existir
        config = service.create_default_config(client_id)
    
    return config


@router.put("/", response_model=RenusConfigResponse)
async def update_config(
    config_data: RenusConfigUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Atualiza configuração completa do RENUS
    
    Args:
        config_data: Dados de configuração a atualizar
        
    Returns:
        Configuração atualizada
    """
    service = RenusConfigService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client_id not found in token"
        )
    
    config = service.update_config(client_id, config_data)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return config


@router.patch("/instructions", response_model=RenusConfigResponse)
async def update_instructions(
    data: Dict[str, str],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Atualiza apenas o system_prompt (instruções) do RENUS
    
    Args:
        data: Dict com chave "system_prompt"
        
    Returns:
        Configuração atualizada
    """
    service = RenusConfigService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client_id not found in token"
        )
    
    if "system_prompt" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="system_prompt is required"
        )
    
    config = service.update_instructions(client_id, data)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return config


@router.patch("/guardrails", response_model=RenusConfigResponse)
async def update_guardrails(
    data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Atualiza apenas os guardrails do RENUS
    
    Args:
        data: Dict com chave "guardrails" (jsonb)
        
    Returns:
        Configuração atualizada
    """
    service = RenusConfigService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client_id not found in token"
        )
    
    if "guardrails" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="guardrails is required"
        )
    
    config = service.update_guardrails(client_id, data)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return config


@router.patch("/advanced", response_model=RenusConfigResponse)
async def update_advanced(
    data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Atualiza configurações avançadas (temperature, max_tokens, etc)
    
    Args:
        data: Dict com campos: temperature, max_tokens, top_p, etc
        
    Returns:
        Configuração atualizada
    """
    service = RenusConfigService()
    client_id = getattr(current_user, "client_id", None)
    
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="client_id not found in token"
        )
    
    config = service.update_advanced(client_id, data)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return config
