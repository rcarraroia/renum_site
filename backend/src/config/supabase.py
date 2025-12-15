"""
Cliente Supabase
"""
from supabase import create_client, Client
from src.config.settings import settings


# Cliente admin (usa SERVICE_KEY - bypassa RLS)
supabase_admin: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)

# Cliente público (usa ANON_KEY - respeita RLS)
supabase_client: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_ANON_KEY
)


async def cleanup_supabase():
    """
    Fecha conexões HTTP dos clientes Supabase.
    Deve ser chamado no shutdown da aplicação.
    """
    try:
        # Fechar cliente admin
        if hasattr(supabase_admin, 'postgrest') and hasattr(supabase_admin.postgrest, 'session'):
            session = supabase_admin.postgrest.session
            if hasattr(session, 'aclose'):
                await session.aclose()
            elif hasattr(session, 'close'):
                session.close()
        
        # Fechar cliente público
        if hasattr(supabase_client, 'postgrest') and hasattr(supabase_client.postgrest, 'session'):
            session = supabase_client.postgrest.session
            if hasattr(session, 'aclose'):
                await session.aclose()
            elif hasattr(session, 'close'):
                session.close()
                
    except Exception as e:
        # Log mas não falha o shutdown
        print(f"Warning: Error closing Supabase connections: {e}")
