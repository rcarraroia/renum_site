"""
Celery Workers - Sprint 07A
Background task processing with Celery + Redis
"""

from .celery_app import celery_app

__all__ = ['celery_app']
