"""
Auth Middleware - Sprint 07A
Authentication and authorization middleware for FastAPI
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt

from ..config.settings import settings
from ..config.supabase import supabase_admin
from ..utils.logger import logger

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token
    
    Returns:
        User dict with id, email, role
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        # Get user from database
        result = supabase_admin.table("profiles").select("*").eq("id", user_id).single().execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user = result.data
        
        logger.info(f"[Auth] User authenticated: {user['email']} ({user['role']})")
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[Auth] Error authenticating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


async def require_admin(
    user: dict = Depends(get_current_user)
) -> dict:
    """
    Require user to be admin.
    
    Args:
        user: Current user from get_current_user
    
    Returns:
        User dict if admin
    
    Raises:
        HTTPException: If user is not admin
    """
    if user.get("role") != "admin":
        logger.warning(f"[Auth] Non-admin user attempted admin action: {user['email']}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return user


async def get_current_client_id(
    user: dict = Depends(get_current_user)
) -> str:
    """
    Get client_id for current user.
    
    For admin users, returns None (can access all clients).
    For client users, returns their client_id.
    
    Args:
        user: Current user from get_current_user
    
    Returns:
        Client ID string or None for admins
    """
    if user.get("role") == "admin":
        return None
    
    # Get client_id from clients table
    result = supabase_admin.table("clients").select("id").eq("profile_id", user["id"]).single().execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found for user"
        )
    
    return result.data["id"]
