from celery import Celery

from src.config import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"]
)

celery.conf.broker_connection_retry_on_startup = True  
