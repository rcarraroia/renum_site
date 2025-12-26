"""
FastAPI Main Application - Versão sem Redis para desenvolvimento local
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.settings import settings
from src.api.routes import auth, clients, leads, projects, conversations, agents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    print("🚀 Iniciando RENUM Backend (Modo Local - Sem Redis)")
    print(f"📊 Debug Mode: {settings.DEBUG}")
    print(f"🔗 CORS Origins: {settings.cors_origins_list}")
    yield
    print("🛑 Encerrando RENUM Backend")


# Criar aplicação FastAPI
app = FastAPI(
    title="RENUM Backend API",
    description="Sistema de Agentes de IA para Automação de Negócios",
    version="1.0.0",
    debug=settings.DEBUG,
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

# Registrar routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "RENUM Backend API",
        "version": "1.0.0",
        "status": "running",
        "mode": "local_development",
        "redis": "disabled"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "local_development",
        "redis": "disabled"
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main_no_redis:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )