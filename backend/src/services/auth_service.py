"""
Serviço de autenticação usando Supabase Auth
"""
from typing import Optional, Dict, Any
from src.config.supabase import supabase_client, supabase_admin
from src.models.user import UserProfile, UserLogin, UserRegister
from src.utils.exceptions import AuthenticationError, ValidationError
from src.utils.logger import logger


class AuthService:
    """Serviço de autenticação"""
    
    async def login(self, credentials: UserLogin) -> Dict[str, Any]:
        """
        Realiza login do usuário
        
        Args:
            credentials: Email e senha
            
        Returns:
            Dict contendo token e dados do usuário
            
        Raises:
            AuthenticationError: Credenciais inválidas
        """
        try:
            # Login via Supabase Auth
            response = supabase_client.auth.sign_in_with_password({
                "email": credentials.email,
                "password": credentials.password
            })
            
            if not response.user:
                raise AuthenticationError("Invalid credentials")
            
            # Buscar profile do usuário
            profile_response = supabase_admin.table("profiles").select("*").eq(
                "id", response.user.id
            ).single().execute()
            
            profile = profile_response.data
            
            logger.info(f"User logged in: {credentials.email}")
            
            # Construir nome completo
            first_name = profile.get("first_name", "")
            last_name = profile.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip() or "User"
            
            return {
                "access_token": response.session.access_token,
                "token_type": "bearer",
                "expires_in": response.session.expires_in,
                "user": UserProfile(
                    id=response.user.id,
                    email=response.user.email,
                    first_name=first_name,
                    last_name=last_name,
                    name=full_name,  # Campo para frontend
                    role=profile.get("role", "guest"),
                    avatar_url=profile.get("avatar_url"),
                    updated_at=profile.get("updated_at")
                )
            }
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise AuthenticationError("Authentication failed")
    
    async def register(self, user_data: UserRegister) -> Dict[str, Any]:
        """
        Registra novo usuário
        
        Args:
            user_data: Dados do usuário
            
        Returns:
            Dict contendo token e dados do usuário
            
        Raises:
            ValidationError: Email já existe
        """
        try:
            # Criar usuário no Supabase Auth
            response = supabase_client.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name
                    }
                }
            })
            
            if not response.user:
                raise ValidationError("Failed to create user")
            
            logger.info(f"User registered: {user_data.email}")
            
            # Profile é criado automaticamente via trigger no Supabase
            # Buscar profile criado
            profile_response = supabase_admin.table("profiles").select("*").eq(
                "id", response.user.id
            ).single().execute()
            
            profile = profile_response.data
            
            # Construir nome completo
            first_name = profile.get("first_name", "")
            last_name = profile.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip() or "User"
            
            return {
                "access_token": response.session.access_token if response.session else None,
                "token_type": "bearer",
                "expires_in": response.session.expires_in if response.session else 0,
                "user": UserProfile(
                    id=response.user.id,
                    email=response.user.email,
                    first_name=first_name,
                    last_name=last_name,
                    name=full_name,
                    role=profile.get("role", "guest"),
                    avatar_url=profile.get("avatar_url"),
                    updated_at=profile.get("updated_at")
                )
            }
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            raise ValidationError("Registration failed")
    
    async def logout(self, token: str) -> bool:
        """
        Realiza logout do usuário
        
        Args:
            token: JWT token
            
        Returns:
            True se sucesso
        """
        try:
            supabase_client.auth.sign_out()
            logger.info("User logged out")
            return True
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return False
    
    async def get_current_user(self, token: str) -> Optional[UserProfile]:
        """
        Busca usuário atual baseado no token
        
        Args:
            token: JWT token
            
        Returns:
            UserProfile ou None
        """
        try:
            # Validar token e buscar usuário
            user_response = supabase_client.auth.get_user(token)
            
            if not user_response.user:
                return None
            
            # Buscar profile
            profile_response = supabase_admin.table("profiles").select("*").eq(
                "id", user_response.user.id
            ).single().execute()
            
            profile = profile_response.data
            
            # Construir nome completo
            first_name = profile.get("first_name", "")
            last_name = profile.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip() or "User"
            
            return UserProfile(
                id=user_response.user.id,
                email=user_response.user.email,
                first_name=first_name,
                last_name=last_name,
                name=full_name,
                role=profile.get("role", "guest"),
                avatar_url=profile.get("avatar_url"),
                updated_at=profile.get("updated_at")
            )
            
        except Exception as e:
            logger.error(f"Get current user failed: {str(e)}")
            return None


# Instância global do serviço
auth_service = AuthService()
