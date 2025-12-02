"""
Configurações do sistema usando Pydantic Settings
Carrega variáveis de ambiente do arquivo .env
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # FastAPI
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # AI / LLM - API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OPENROUTER_API_KEY: str | None = None
    
    # LangSmith - Observability
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "renum-agents"
    LANGSMITH_ENVIRONMENT: str = "development"
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    
    # Agent Configuration - Default Models
    DEFAULT_RENUS_MODEL: str = "gpt-4-turbo-preview"
    DEFAULT_ISA_MODEL: str = "gpt-4o-mini"  # Usando OpenAI para testes
    DEFAULT_DISCOVERY_MODEL: str = "gpt-4o-mini"
    
    # LangServe Configuration
    LANGSERVE_PORT: int = 8001
    LANGSERVE_HOST: str = "0.0.0.0"
    
    # WhatsApp Provider
    WHATSAPP_PROVIDER: str = "none"
    WHATSAPP_API_URL: str | None = None
    WHATSAPP_API_KEY: str | None = None
    
    # Email Provider
    EMAIL_PROVIDER: str = "none"
    EMAIL_API_KEY: str | None = None
    EMAIL_FROM_ADDRESS: str | None = None
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Converte string de CORS_ORIGINS em lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def validate_ai_keys(self) -> None:
        """
        Valida que as chaves de API necessárias estão presentes.
        Falha fast se chaves obrigatórias estiverem faltando.
        
        Raises:
            ValueError: Se alguma chave obrigatória estiver faltando
        """
        missing_keys = []
        
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY == "your-openai-api-key-here":
            missing_keys.append("OPENAI_API_KEY")
        
        if not self.ANTHROPIC_API_KEY or self.ANTHROPIC_API_KEY == "your-anthropic-api-key-here":
            missing_keys.append("ANTHROPIC_API_KEY")
        
        if not self.LANGSMITH_API_KEY or self.LANGSMITH_API_KEY == "your-langsmith-api-key-here":
            missing_keys.append("LANGSMITH_API_KEY")
        
        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}\n"
                f"Please set them in your .env file.\n"
                f"See .env.example for reference."
            )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorar campos extras do .env


# Instância global de settings
settings = Settings()

# Validar chaves de API ao inicializar (fail fast)
try:
    settings.validate_ai_keys()
except ValueError as e:
    # Em desenvolvimento, apenas avisar. Em produção, falhar.
    if settings.DEBUG:
        print(f"⚠️  WARNING: {e}")
        print("⚠️  Sistema iniciará mas funcionalidades de IA não estarão disponíveis.")
    else:
        raise
