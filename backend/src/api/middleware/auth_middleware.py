"""
Middleware de autenticação para validar JWT
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.auth_service import auth_service
from src.models.user import UserProfile
from src.utils.logger import logger


# Security scheme para Swagger
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserProfile:
    """
    Middleware para validar JWT e retornar usuário atual
    
    Args:
        credentials: Credenciais HTTP Bearer
        
    Returns:
        UserProfile do usuário autenticado
        
    Raises:
        HTTPException: Token inválido ou expirado
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    user = await auth_service.get_current_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def require_admin(
    current_user: UserProfile = Depends(get_current_user)
) -> UserProfile:
    """
    Middleware que exige role admin
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        UserProfile do admin autenticado
        
    Raises:
        HTTPException: Não é admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user
