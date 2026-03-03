from celery import Celery
from celery_batches import Batches
import clickhouse_connect

from src.schemas.redirect_data import RedirectDataSchema
from src.settings import settings

app = Celery("ConsumerService", broker=settings.broker_url)

client = clickhouse_connect.get_client(
    host=settings.ch_host,
    port=settings.ch_port,
    database=settings.ch_name,
    username=settings.ch_user,
    password=settings.ch_password,
)


@app.task(
    base=Batches,
    flush_every=5,
    flush_interval=60,
    name="task.store_redirect",
)
def store_redirects(requests):
    print(
        *[RedirectDataSchema.model_validate(req.args[0]) for req in requests], sep="\n"
    )
