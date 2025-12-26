from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.api.dependencies import get_current_user
from src.utils.supabase_client import get_client
from src.utils.logger import logger

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
    """
    try:
        supabase = get_client()
        
        # Get settings from database
        result = supabase.table("sicc_settings")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .execute()
        
        if not result.data:
            # Return default settings if not found
            logger.info(f"No SICC settings found for agent {agent_id}, returning defaults")
            return {
                "agent_id": agent_id,
                "enabled": True,
                "evolution_rate": 1.0,
                "confidence_threshold": 0.8,
                "learning_active": True,
                "memory_retention_days": 30,
                "auto_approve_threshold": 0.9,
                "manual_review_threshold": 0.7,
                "consolidation_frequency_hours": 24,
                "min_learnings_for_consolidation": 10,
                "max_memory_chunks": 10000,
                "memory_importance_threshold": 0.3,
                "memory_retention_days": 365,
                "max_behavior_patterns": 1000,
                "pattern_min_usage_count": 5,
                "pattern_success_threshold": 0.6,
                "auto_snapshot_enabled": True,
                "snapshot_frequency_days": 7,
                "max_snapshots": 52,
                "learn_from_conversations": True,
                "learn_from_documents": True,
                "learn_from_feedback": True,
                "learn_from_patterns": True,
                "embedding_model": "gte-small",
                "similarity_algorithm": "cosine",
                "custom_config": {}
            }
        
        settings = result.data[0]
        logger.info(f"Retrieved SICC settings for agent {agent_id}")
        
        # Add legacy fields for frontend compatibility
        settings["enabled"] = True
        settings["evolution_rate"] = 1.0
        settings["confidence_threshold"] = settings.get("auto_approve_threshold", 0.8)
        settings["learning_active"] = True
        
        # Bug #4 - Corrigido: Calcular auto_approval_enabled baseado no threshold
        threshold = settings.get("auto_approve_threshold", 0.8)
        settings["auto_approval_enabled"] = threshold < 1.0
        
        return settings
    
    except Exception as e:
        logger.error(f"Error getting SICC settings for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings/{agent_id}")
async def update_sicc_settings(
    agent_id: str, 
    settings: Dict[str, Any], 
    current_user: dict = Depends(get_current_user)
):
    """
    Update SICC settings for an agent.
    """
    try:
        supabase = get_client()
        
        # Remove legacy fields that don't exist in database
        db_settings = {k: v for k, v in settings.items() 
                      if k not in ['enabled', 'evolution_rate', 'confidence_threshold', 'learning_active']}
        
        # Map legacy fields to database fields
        if 'confidence_threshold' in settings:
            db_settings['auto_approve_threshold'] = settings['confidence_threshold']
        
        # Bug #4 - Corrigido: Mapear auto_approval_enabled para auto_approve_threshold
        if 'auto_approval_enabled' in settings:
            if settings['auto_approval_enabled']:
                # Se habilitado, usar o threshold fornecido ou default 0.8
                db_settings['auto_approve_threshold'] = settings.get('auto_approval_threshold', 0.8)
            else:
                # Se desabilitado, setar threshold para 1.0 (nunca auto-aprova)
                db_settings['auto_approve_threshold'] = 1.0
        
        logger.info(f"Updating SICC settings for agent {agent_id}: {db_settings}")
        
        # Check if settings exist
        existing = supabase.table("sicc_settings")\
            .select("id")\
            .eq("agent_id", agent_id)\
            .execute()
        
        if existing.data:
            # Update existing settings
            result = supabase.table("sicc_settings")\
                .update(db_settings)\
                .eq("agent_id", agent_id)\
                .execute()
        else:
            # Create new settings
            db_settings['agent_id'] = agent_id
            result = supabase.table("sicc_settings")\
                .insert(db_settings)\
                .execute()
        
        logger.info(f"Updated SICC settings for agent {agent_id}")
        return {"success": True, "message": "Settings updated successfully"}
    
    except Exception as e:
        logger.error(f"Error updating SICC settings for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
