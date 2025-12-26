"""
FastAPI Main - Versão para Desenvolvimento Local
Funciona sem Redis, mas com todas as outras funcionalidades
"""
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

# Imports locais
from src.config.settings import settings
from src.config.supabase import supabase_admin as get_supabase_client
from src.api.routes import auth, clients, leads, projects, conversations, agents

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    
    # Startup
    logger.info("🚀 Iniciando RENUM Backend (Desenvolvimento Local)")
    
    # Testar conexão Supabase
    try:
        supabase = get_supabase_client
        # Teste simples
        result = supabase.table("profiles").select("count", count="exact").execute()
        logger.info(f"✅ Supabase conectado - {result.count} profiles")
    except Exception as e:
        logger.error(f"❌ Erro Supabase: {e}")
        raise HTTPException(status_code=500, detail="Erro de conexão com banco")
    
    # Verificar Redis (opcional em desenvolvimento)
    try:
        import redis
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        logger.info("✅ Redis conectado")
        app.state.redis_available = True
    except Exception as e:
        logger.warning(f"⚠️ Redis não disponível: {e}")
        logger.info("🔄 Continuando sem Redis (modo desenvolvimento)")
        app.state.redis_available = False
    
    yield
    
    # Shutdown
    logger.info("🛑 Encerrando RENUM Backend")

# Criar aplicação FastAPI
app = FastAPI(
    title="RENUM Backend API",
    description="Sistema de Agentes de IA - Desenvolvimento Local",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para verificar Redis
@app.middleware("http")
async def redis_check_middleware(request, call_next):
    """Middleware que adiciona status do Redis no header"""
    response = await call_next(request)
    response.headers["X-Redis-Available"] = str(getattr(app.state, 'redis_available', False))
    return response

# Rotas principais
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clientes"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projetos"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversas"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agentes"])

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "RENUM Backend API - Desenvolvimento Local",
        "version": "1.0.0",
        "status": "running",
        "redis_available": getattr(app.state, 'redis_available', False),
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check completo"""
    health_status = {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "services": {}
    }
    
    # Verificar Supabase
    try:
        supabase = get_supabase_client
        result = supabase.table("profiles").select("count", count="exact").execute()
        health_status["services"]["supabase"] = {
            "status": "connected",
            "profiles_count": result.count
        }
    except Exception as e:
        health_status["services"]["supabase"] = {
            "status": "error",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Verificar Redis
    redis_available = getattr(app.state, 'redis_available', False)
    health_status["services"]["redis"] = {
        "status": "connected" if redis_available else "unavailable",
        "note": "Optional in development" if not redis_available else None
    }
    
    return health_status

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Erro interno do servidor",
            "detail": str(exc) if settings.DEBUG else "Contate o suporte"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "src.main_local:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )