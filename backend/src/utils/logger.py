"""
Sistema de logging usando loguru
"""
from loguru import logger
import sys
from pathlib import Path


# Criar diretório de logs se não existir
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Remover handler padrão
logger.remove()

# Adicionar handler para console
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Adicionar handler para arquivo
logger.add(
    "logs/renum_{time:YYYY-MM-DD_HH-mm-ss}.log",
    rotation="500 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
    level="DEBUG"
)

def get_logger(name: str = None):
    """
    Retorna uma instância do logger configurado
    """
    if name:
        return logger.bind(name=name)
    return logger
