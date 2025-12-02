"""
Modelos Pydantic para usuário e autenticação
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Schema base de usuário"""
    email: EmailStr


class UserLogin(UserBase):
    """Schema para login"""
    password: str


class UserRegister(UserBase):
    """Schema para registro"""
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserProfile(BaseModel):
    """Schema de perfil de usuário"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "guest"
    avatar_url: Optional[str] = None
    updated_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    """Schema de resposta com token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile


class UserResponse(BaseModel):
    """Schema de resposta genérica de usuário"""
    user: UserProfile
    message: str = "Success"
