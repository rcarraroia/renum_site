"""
Celery Application Configuration - Sprint 07A
Configures Celery with Redis broker for async task processing
"""

from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Redis URL from environment
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')

# Create Celery app
celery_app = Celery(
    'renum',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        'src.workers.message_tasks',
        'src.workers.trigger_tasks',
        'src.workers.sicc_tasks',  # SICC Multi-Agente
    ]
)

# Configure Celery
celery_app.conf.update(
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='America/Sao_Paulo',
    enable_utc=True,
    
    # Task execution
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    task_soft_time_limit=240,  # 4 minutes soft limit
    
    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    
    # Worker
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    
    # Beat schedule (for periodic tasks)
    beat_schedule={
        'trigger-scheduler': {
            'task': 'src.workers.trigger_tasks.trigger_scheduler_task',
            'schedule': 60.0,  # Every 60 seconds (1 minute)
        },
        # SICC Multi-Agente Tasks
        'sicc-consolidate-learnings': {
            'task': 'src.workers.sicc_tasks.consolidate_learnings',
            'schedule': 300.0,  # Every 5 minutes
        },
        'sicc-analyze-patterns': {
            'task': 'src.workers.sicc_tasks.analyze_patterns',
            'schedule': 900.0,  # Every 15 minutes
        },
        'sicc-flush-queue': {
            'task': 'src.workers.sicc_tasks.flush_sicc_queue',
            'schedule': 120.0,  # Every 2 minutes
        },
        'sicc-cleanup-weekly': {
            'task': 'src.workers.sicc_tasks.cleanup_old_data',
            'schedule': crontab(hour=3, minute=0, day_of_week=0),  # Sunday 3am
        },
    },
)

# Task routes (optional - for multiple queues)
celery_app.conf.task_routes = {
    'src.workers.message_tasks.*': {'queue': 'messages'},
    'src.workers.trigger_tasks.*': {'queue': 'triggers'},
    'src.workers.sicc_tasks.*': {'queue': 'sicc'},  # SICC queue
}

# Default queue
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_routing_key = 'default'

if __name__ == '__main__':
    celery_app.start()
