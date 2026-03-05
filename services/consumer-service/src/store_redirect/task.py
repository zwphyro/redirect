from celery import shared_task
from celery_batches import Batches

from src.store_redirect.schemas import BaseRedirectSchema


@shared_task(
    base=Batches,
    flush_every=5,
    flush_interval=60,
    name="task.store_redirect",
)
def store_redirects(requests):
    print(
        *[BaseRedirectSchema.model_validate(requset.kwargs) for requset in requests],
        sep="\n",
    )
