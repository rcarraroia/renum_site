#!/usr/bin/env python3
"""
Servidor mínimo para testar módulo SICC
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn

# Imports mínimos necessários
from src.utils.supabase_client import get_client
from src.utils.logger import logger

app = FastAPI(title="SICC Test Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://localhost:8082"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    """Handle CORS preflight requests"""
    return {"status": "ok"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "service": "sicc-test"}

@app.post("/auth/login")
async def login(credentials: Dict[str, str]):
    """Login simples para testes"""
    email = credentials.get("email")
    password = credentials.get("password")
    
    # Validação simples para testes
    if email == "rcarraro2015@gmail.com" and password == "M&151173c@":
        return {
            "access_token": "test-token-123",
            "token_type": "bearer",
            "user": {"email": email, "role": "admin"}
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

def get_current_user():
    """Mock user para testes"""
    return {"id": "test-user", "email": "rcarraro2015@gmail.com", "role": "admin"}

@app.get("/api/sicc/settings/{agent_id}")
async def get_sicc_settings(agent_id: str, current_user: dict = Depends(get_current_user)):
    """Get SICC settings for an agent"""
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
        
        return settings
    
    except Exception as e:
        logger.error(f"Error getting SICC settings for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/")
async def list_agents(
    role: str = None,
    is_system: bool = None,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Lista agentes (mock com dados reais do Supabase)"""
    try:
        supabase = get_client()
        
        # Build query
        query = supabase.table("agents").select("*")
        
        # Apply filters
        if role:
            if role == "system_orchestrator":
                query = query.eq("is_system", True)
            else:
                query = query.eq("role", role)
        
        if is_system is not None:
            query = query.eq("is_system", is_system)
        
        # Apply limit
        query = query.limit(limit)
        
        # Execute
        result = query.execute()
        
        return result.data
        
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        # Return mock data if database fails
        return [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "RENUS Base",
                "description": "Agente base do sistema",
                "is_system": True,
                "role": "assistant",
                "status": "active",
                "created_at": "2025-12-21T20:00:00Z"
            }
        ]

@app.get("/api/agents")
async def list_agents_alt(
    role: str = None,
    is_system: bool = None,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Lista agentes - rota alternativa"""
    return await list_agents(role, is_system, limit, current_user)

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    """Estatísticas do dashboard"""
    try:
        supabase = get_client()
        
        # Get real counts from database
        agents_result = supabase.table("agents").select("id", count="exact").execute()
        clients_result = supabase.table("clients").select("id", count="exact").execute()
        leads_result = supabase.table("leads").select("id", count="exact").execute()
        conversations_result = supabase.table("conversations").select("id", count="exact").execute()
        
        return {
            "agents_count": agents_result.count or 0,
            "clients_count": clients_result.count or 0,
            "leads_count": leads_result.count or 0,
            "conversations_count": conversations_result.count or 0,
            "active_conversations": 0,
            "messages_today": 0,
            "success_rate": 0.0
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {str(e)}")
        return {
            "agents_count": 2,
            "clients_count": 3,
            "leads_count": 1,
            "conversations_count": 1,
            "active_conversations": 0,
            "messages_today": 0,
            "success_rate": 0.0
        }

@app.get("/api/clients")
async def list_clients(
    page: int = 1,
    limit: int = 10,
    status: str = None,
    current_user: dict = Depends(get_current_user)
):
    """Lista clientes"""
    try:
        supabase = get_client()
        
        # Build query
        query = supabase.table("clients").select("*")
        
        # Apply filters
        if status:
            query = query.eq("status", status)
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.range(offset, offset + limit - 1)
        
        # Execute
        result = query.execute()
        
        return result.data
        
    except Exception as e:
        logger.error(f"Error listing clients: {str(e)}")
        return []

@app.get("/api/leads")
async def list_leads(
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Lista leads"""
    try:
        supabase = get_client()
        
        # Build query
        query = supabase.table("leads").select("*").limit(limit)
        
        # Execute
        result = query.execute()
        
        return result.data
        
    except Exception as e:
        logger.error(f"Error listing leads: {str(e)}")
        return []

@app.get("/api/projects")
async def list_projects(
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Lista projetos"""
    try:
        supabase = get_client()
        
        # Build query
        query = supabase.table("projects").select("*").limit(limit)
        
        # Execute
        result = query.execute()
        
        return result.data
        
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        return []

@app.get("/api/chat/renus")
async def get_renus_welcome(current_user: dict = Depends(get_current_user)):
    """Mensagem de boas-vindas do RENUS"""
    return {
        "message": "Olá! Eu sou o RENUS, seu assistente inteligente. Como posso ajudá-lo hoje?",
        "status": "ready"
    }

@app.put("/api/sicc/settings/{agent_id}")
async def update_sicc_settings(
    agent_id: str, 
    settings: Dict[str, Any], 
    current_user: dict = Depends(get_current_user)
):
    """Update SICC settings for an agent"""
    try:
        supabase = get_client()
        
        # Remove legacy fields that don't exist in database
        db_settings = {k: v for k, v in settings.items() 
                      if k not in ['enabled', 'evolution_rate', 'confidence_threshold', 'learning_active']}
        
        # Map legacy fields to database fields
        if 'confidence_threshold' in settings:
            db_settings['auto_approve_threshold'] = settings['confidence_threshold']
        
        # Update settings in database
        result = supabase.table("sicc_settings")\
            .update(db_settings)\
            .eq("agent_id", agent_id)\
            .execute()
        
        if not result.data:
            # If no existing settings, create new ones
            db_settings['agent_id'] = agent_id
            result = supabase.table("sicc_settings")\
                .insert(db_settings)\
                .execute()
        
        logger.info(f"Updated SICC settings for agent {agent_id}")
        return {"success": True, "message": "Settings updated successfully"}
    
    except Exception as e:
        logger.error(f"Error updating SICC settings for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")