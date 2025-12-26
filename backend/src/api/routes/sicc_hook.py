"""
SICC Hook API Routes
Sprint SICC Multi-Agente

Endpoints para monitoramento e controle do SICC Hook.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ...services.sicc.sicc_hook import get_sicc_hook
from ...utils.logger import logger

router = APIRouter(prefix="/sicc/hook", tags=["SICC Hook"])


@router.get("/stats")
async def get_hook_stats() -> Dict[str, Any]:
    """
    Retorna estatísticas do SICC Hook.
    
    Returns:
        Dict com enabled, queue_size, processing, batch_size
    """
    try:
        hook = get_sicc_hook()
        return hook.get_stats()
    except Exception as e:
        logger.error(f"Error getting SICC hook stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enable")
async def enable_hook() -> Dict[str, str]:
    """
    Habilita o SICC Hook para monitoramento.
    
    Returns:
        Mensagem de confirmação
    """
    try:
        hook = get_sicc_hook()
        hook.enable()
        return {"status": "enabled", "message": "SICC Hook habilitado com sucesso"}
    except Exception as e:
        logger.error(f"Error enabling SICC hook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/disable")
async def disable_hook() -> Dict[str, str]:
    """
    Desabilita o SICC Hook (útil para manutenção).
    
    Returns:
        Mensagem de confirmação
    """
    try:
        hook = get_sicc_hook()
        hook.disable()
        return {"status": "disabled", "message": "SICC Hook desabilitado com sucesso"}
    except Exception as e:
        logger.error(f"Error disabling SICC hook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flush")
async def flush_queue() -> Dict[str, Any]:
    """
    Força processamento de todas as interações pendentes.
    
    Returns:
        Número de interações processadas
    """
    try:
        hook = get_sicc_hook()
        count = await hook.flush()
        return {
            "status": "flushed",
            "processed": count,
            "message": f"{count} interações processadas"
        }
    except Exception as e:
        logger.error(f"Error flushing SICC hook queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def hook_health() -> Dict[str, Any]:
    """
    Health check do SICC Hook.
    
    Returns:
        Status de saúde do hook
    """
    try:
        hook = get_sicc_hook()
        stats = hook.get_stats()
        
        # Determinar status de saúde
        health = "healthy"
        issues = []
        
        if not stats["enabled"]:
            health = "degraded"
            issues.append("Hook desabilitado")
        
        if stats["queue_size"] > 100:
            health = "degraded"
            issues.append(f"Queue grande: {stats['queue_size']} itens")
        
        return {
            "status": health,
            "enabled": stats["enabled"],
            "queue_size": stats["queue_size"],
            "processing": stats["processing"],
            "issues": issues
        }
    except Exception as e:
        logger.error(f"Error checking SICC hook health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
