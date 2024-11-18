from celery import Celery
import os

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Celery app
app = Celery('healthsphere_backend')

# Celery settings loaded from Django settings
# The 'CELERY' namespace is used to configure Celery settings in Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in all registered Django app configs
app.autodiscover_tasks()

# Custom Celery configuration options
app.conf.update(
    broker_url='redis://localhost:6379/0',  # Redis as the message broker
    result_backend='redis://localhost:6379/0',  # Redis for storing task results
    task_serializer='json',  # Task payload serialization format
    result_serializer='json',  # Result payload serialization format
    accept_content=['json'],  # Allowed content types for task messages
    timezone='UTC',  # Set time zone to UTC for consistent task scheduling
    enable_utc=True,  # Enable UTC for Celery
    task_track_started=True,  # Track task start time for better visibility
    worker_concurrency=4,  # Max number of concurrent worker processes
)

# Optional: Celery beat scheduler for periodic tasks
# You can schedule tasks to run at specific intervals using Celery Beat
app.conf.beat_schedule = {
    'sample-task': {
        'task': 'healthapp.tasks.sample_task',  # Replace with actual task
        'schedule': 3600.0,  # Every hour
    },
}
