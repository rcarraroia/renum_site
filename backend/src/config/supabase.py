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
