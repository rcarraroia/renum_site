"""
FastAPI Application - RENUM Backend
Entry point da aplicação
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.api.routes import health, auth
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
