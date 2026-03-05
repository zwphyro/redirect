from celery import Celery
from src.settings import settings

app = Celery("ConsumerService", broker=settings.broker_url)

app.autodiscover_tasks(["src.store_redirect.task"])
