"""
Integrations - Sprint 07A
Clients for external services (Uazapi, SMTP, SendGrid, Client Supabase)
"""

from .uazapi_client import UazapiClient
from .smtp_client import SMTPClient
from .sendgrid_client import SendGridClient
from .client_supabase import ClientSupabaseClient

__all__ = [
    'UazapiClient',
    'SMTPClient',
    'SendGridClient',
    'ClientSupabaseClient',
]
