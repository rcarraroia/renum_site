from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.api.dependencies import get_current_user

router = APIRouter()

@router.get("/commands")
async def list_sicc_commands(limit: int = 50, current_user: dict = Depends(get_current_user)):
    """Lista comandos SICC (mock)"""
    return []

@router.get("/status")
async def get_sicc_status(current_user: dict = Depends(get_current_user)):
    """Status global do SICC (mock)"""
    return {
        "agents_monitored": 0,
        "commands_today": 0,
        "error_rate": 0,
        "sicc_active": True
    }

@router.get("/settings/{agent_id}")
async def get_sicc_settings(agent_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get SICC settings for an agent.
    Endpoint placeholder to prevent 404 in frontend.
    """
    return {
        "agent_id": agent_id,
        "enabled": True,
        "evolution_rate": 1.0,
        "confidence_threshold": 0.8,
        "learning_active": True,
        "memory_retention_days": 30
    }
