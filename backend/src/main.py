"""
FastAPI Application - RENUM Backend
Entry point da aplicação
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.api.routes import health, auth, clients, leads, projects, websocket, conversations, messages, interviews, renus_config, tools, sub_agents, public_chat, isa, dashboard
from src.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia eventos de startup e shutdown da aplicação
    """
    # Startup
    logger.info("=" * 50)
    logger.info("🚀 RENUM Backend Starting...")
    logger.info(f"📍 Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"🌐 API Host: {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"🔒 CORS Origins: {settings.cors_origins_list}")
    logger.info("=" * 50)
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("🛑 RENUM Backend Shutting Down...")
    logger.info("=" * 50)


# Inicializar FastAPI
app = FastAPI(
    title="RENUM API",
    description="Backend API para sistema RENUM - Agentes de IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(clients.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(conversations.router, prefix="/api")
app.include_router(messages.router, prefix="/api")
app.include_router(interviews.router, prefix="/api")  # Discovery Agent interviews
app.include_router(renus_config.router, prefix="/api")  # RENUS Configuration
app.include_router(tools.router, prefix="/api")  # Agent Tools
app.include_router(sub_agents.router, prefix="/api")  # Sub-Agents Management
app.include_router(public_chat.router, prefix="/api")  # Public Chat URLs
app.include_router(isa.router, prefix="/api")  # ISA Assistant
app.include_router(dashboard.router, prefix="/api")  # Dashboard Stats
app.include_router(websocket.router)  # WebSocket endpoint


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API
    
    Returns:
        Informações básicas da API
    """
    return {
        "name": "RENUM API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
