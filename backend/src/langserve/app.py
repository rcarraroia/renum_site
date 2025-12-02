"""
LangServe Application
Expõe agentes via API REST com suporte a streaming
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from langserve import add_routes
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.config.settings import settings
from src.utils.logger import logger
from src.agents.mmn_agent_simple import MMNDiscoveryAgent


# Criar app FastAPI separada para LangServe
app = FastAPI(
    title="RENUM LangServe API",
    description="API para exposição de agentes via LangServe com streaming",
    version="1.0.0",
    docs_url="/langserve/docs",
    redoc_url="/langserve/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/langserve/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "langserve",
        "version": "1.0.0"
    }


# Middleware para extrair client_id do token JWT
@app.middleware("http")
async def add_client_context(request: Request, call_next):
    """
    Middleware para adicionar contexto de cliente em todas as requisições.
    Extrai client_id do token JWT e adiciona ao state da request.
    """
    # TODO: Implementar extração de client_id do JWT
    # Por enquanto, usar client_id mock
    request.state.client_id = "default-client"
    
    response = await call_next(request)
    return response


# Inicializar agentes
try:
    # Discovery Agent (MMN)
    discovery_agent = MMNDiscoveryAgent()
    
    # Adicionar rota para Discovery Agent com streaming
    add_routes(
        app,
        discovery_agent.llm,
        path="/agents/discovery",
        enabled_endpoints=["invoke", "stream", "batch"],
    )
    
    logger.info("✅ Discovery Agent registered at /agents/discovery")
    
    # TODO: Adicionar RENUS Agent quando implementado
    # TODO: Adicionar ISA Agent quando implementado
    
except Exception as e:
    logger.error(f"❌ Error initializing LangServe agents: {e}")


@app.get("/agents/list")
async def list_agents():
    """Lista todos os agentes disponíveis via LangServe"""
    return {
        "agents": [
            {
                "name": "Discovery Agent",
                "path": "/agents/discovery",
                "endpoints": {
                    "invoke": "/agents/discovery/invoke",
                    "stream": "/agents/discovery/stream",
                    "batch": "/agents/discovery/batch"
                },
                "description": "Agente para entrevistas com distribuidores MMN"
            }
        ]
    }


logger.info("🚀 LangServe app initialized with streaming support")
