"""
Endpoints de health check
"""
from fastapi import APIRouter
from datetime import datetime
from src.config.supabase import supabase_admin


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/db")
async def database_health():
    """Verifica conexão com Supabase"""
    try:
        # Testar conexão executando query simples
        response = supabase_admin.table("profiles").select("id").limit(1).execute()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
