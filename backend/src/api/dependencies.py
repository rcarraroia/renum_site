"""
API Dependencies
Provides common dependencies for FastAPI routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from src.config.settings import settings
from src.utils.logger import logger

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Get current authenticated user from JWT token.
    Supports both:
    - User tokens (with 'sub' field) - from Supabase Auth
    - API tokens (with 'role' field) - anon/service_role keys
    """
    try:
        token = credentials.credentials
        
        # Decode with SUPABASE_JWT_SECRET
        payload = jwt.decode(
            token, 
            settings.SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            options={"verify_aud": False}  # Supabase tokens may not have aud
        )
        
        # Check for user token (has 'sub')
        user_id = payload.get("sub")
        if user_id:
            return {
                "id": user_id, 
                "email": payload.get("email"),
                "role": payload.get("role", "authenticated")
            }
        
        # Check for API token (has 'role' like 'anon' or 'service_role')
        role = payload.get("role")
        if role in ["anon", "service_role"]:
            return {
                "id": f"api_{role}",
                "email": None,
                "role": role
            }
        
        # No valid identifier found
        logger.warning(f"JWT token missing 'sub' or valid 'role': {payload.keys()}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    """
    Get current user if authenticated, None otherwise
    """
    if not credentials:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None