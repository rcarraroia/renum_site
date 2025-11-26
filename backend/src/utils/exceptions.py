"""
Custom exceptions
"""


class AuthenticationError(Exception):
    """Erro de autenticação"""
    pass


class ValidationError(Exception):
    """Erro de validação"""
    pass


class NotFoundError(Exception):
    """Recurso não encontrado"""
    pass


class PermissionError(Exception):
    """Erro de permissão"""
    pass
