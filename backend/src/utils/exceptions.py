"""
Custom exceptions for RENUM API
"""


class NotFoundError(Exception):
    """Raised when a resource is not found"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class AuthorizationError(Exception):
    """Raised when user is not authorized"""
    pass


class PermissionError(Exception):
    """Raised when user doesn't have permission for an action"""
    pass
