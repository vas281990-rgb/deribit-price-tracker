from celery import Celery
from app.config import settings
 
celery_app = Celery(
    'deribit_tracker',
    # App name used for identification in logs and monitoring tools (e.g., Flower).
    broker=settings.REDIS_URL,
    # Message broker for passing tasks from the producer to workers. 
    # Redis is chosen for its high performance and simplicity.
    backend=settings.REDIS_URL,
    # Result backend to store task execution results (useful for debugging).
    include=['app.tasks.price_tasks'],
    # Modules to import when the Celery worker starts.
)
 
# Periodic task configuration (Celery Beat)
celery_app.conf.beat_schedule = {
    'fetch-prices-every-minute': {
        'task': 'app.tasks.price_tasks.fetch_and_save_prices',
        'schedule': 60.0,
        # Interval in seconds: task runs every minute as per requirements.
    },
}
 
# Use UTC to ensure consistent scheduling across different server environments.
celery_app.conf.timezone = 'UTC'