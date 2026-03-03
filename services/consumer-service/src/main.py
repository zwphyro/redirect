from celery import Celery
import clickhouse_connect

from src.settings import settings

app = Celery("ConsumerService", broker=settings.broker_url)

client = clickhouse_connect.get_client(
    host=settings.ch_host,
    port=settings.ch_port,
    database=settings.ch_name,
    username=settings.ch_user,
    password=settings.ch_password,
)

app.autodiscover_tasks(["src.store_redirect.task"])
