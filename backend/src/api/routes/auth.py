"""
Rotas de autenticação
"""
from fastapi import APIRouter, HTTPException, status, Depends
from src.models.user import (
    UserLogin,
    UserRegister,
    TokenResponse,
    UserProfile,
    UserResponse
)
from src.services.auth_service import auth_service
from src.api.middleware.auth_middleware import get_current_user
from src.utils.exceptions import AuthenticationError, ValidationError
from src.utils.logger import logger


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: UserLogin):
    """
    Endpoint de login
    
    Args:
        credentials: Email e senha do usuário
        
    Returns:
        TokenResponse com access_token e dados do usuário
        
    Raises:
        HTTPException 401: Credenciais inválidas
    """
    try:
        result = await auth_service.login(credentials)
        return TokenResponse(**result)
    except AuthenticationError as e:
        logger.warning(f"Login failed for {credentials.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Endpoint de registro
    
    Args:
        user_data: Dados do novo usuário
        
    Returns:
        TokenResponse com access_token e dados do usuário
        
    Raises:
        HTTPException 400: Email já existe ou dados inválidos
    """
    try:
        result = await auth_service.register(user_data)
        return TokenResponse(**result)
    except ValidationError as e:
        logger.warning(f"Registration failed for {user_data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists or invalid data"
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: UserProfile = Depends(get_current_user)):
    """
    Endpoint de logout (protegido)
    
    Args:
        current_user: Usuário autenticado (via middleware)
        
    Returns:
        Mensagem de sucesso
    """
    try:
        # Token é extraído pelo middleware, mas não precisamos dele aqui
        # O Supabase gerencia a sessão
        await auth_service.logout("")
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def get_me(current_user: UserProfile = Depends(get_current_user)):
    """
    Endpoint para obter dados do usuário atual (protegido)
    
    Args:
        current_user: Usuário autenticado (via middleware)
        
    Returns:
        UserProfile do usuário autenticado
    """
    return current_user


@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_token(current_user: UserProfile = Depends(get_current_user)):
    """
    Endpoint para verificar se token é válido (protegido)
    
    Args:
        current_user: Usuário autenticado (via middleware)
        
    Returns:
        Status de validação do token
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }
