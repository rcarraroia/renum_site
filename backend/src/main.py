"""
FastAPI Application - RENUM Backend
Entry point da aplicação
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.api.routes import health, auth, clients, leads, projects, websocket, conversations, messages, interviews, renus_config, tools, sub_agents, public_chat, isa, dashboard, reports, integrations, triggers, webhooks, wizard, agents, sicc_memory, sicc_learning, sicc_stats, sicc_patterns, sicc_audio, monitoring, knowledge, auth_google
from src.utils.logger import logger

# Configuração da Aplicação
app = FastAPI(
    title="RENUM API",
    version="1.0.0",
    description="API do Sistema RENUM",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.DEBUG
)

# Middleware CORS
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
app.include_router(knowledge.router, prefix="/api")  # Knowledge Base (RAG)
app.include_router(agents.router, prefix="/api")  # Sprint 09 - Agents Management
app.include_router(sub_agents.router, prefix="/api")  # Sub-Agents Management (legacy)
app.include_router(public_chat.router, prefix="/api")  # Public Chat URLs
app.include_router(isa.router, prefix="/api")  # ISA Assistant
app.include_router(dashboard.router, prefix="/api")  # Dashboard Stats
app.include_router(reports.router, prefix="/api")  # Reports & Analytics
app.include_router(integrations.router, prefix="/api")  # Sprint 07A - Integrations
app.include_router(auth_google.router, prefix="/api")
app.include_router(triggers.router, prefix="/api")  # Sprint 07A - Triggers
app.include_router(webhooks.router)  # Sprint 07A - Webhooks (no prefix)
app.include_router(wizard.router, prefix="/api")  # Sprint 06 - Wizard
app.include_router(sicc_memory.router, prefix="/api")  # Sprint 10 - SICC Memory
app.include_router(sicc_learning.router, prefix="/api")  # Sprint 10 - SICC Learning
app.include_router(sicc_stats.router, prefix="/api")  # Sprint 10 - SICC Stats
app.include_router(sicc_patterns.router, prefix="/api")  # Sprint 10 - SICC Patterns
app.include_router(sicc_audio.router)  # Sprint 10 - SICC Audio Processing
app.include_router(monitoring.router, prefix="/api")  # Monitoring & Observability
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
