"""
Supabase Client Utility
Wrapper para facilitar acesso ao cliente Supabase
"""

from src.config.supabase import supabase_admin


def get_client():
    """
    Retorna instância do cliente Supabase com service_role.
    
    Returns:
        Cliente Supabase configurado
    """
    return supabase_admin
