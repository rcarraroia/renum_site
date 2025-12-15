"""
Middleware - Sprint 07A
FastAPI middleware for authentication, logging, etc.
"""

from .auth import get_current_user, require_admin

__all__ = ['get_current_user', 'require_admin']
