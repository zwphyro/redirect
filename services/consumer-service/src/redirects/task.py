from celery import shared_task
from celery_batches import Batches

from src.redirects.dependencies import RedirectServiceMixin
from src.redirects.schemas import BaseRedirectSchema


class StoreRedirectsTask(RedirectServiceMixin, Batches): ...


@shared_task(
    bind=True,
    base=StoreRedirectsTask,
    flush_every=5,
    flush_interval=60,
    name="src.redirects.task.store_redirects",
)
def store_redirects(self, requests):
    self.service.store_redirects(
        [BaseRedirectSchema.model_validate(requset.kwargs) for requset in requests]
    )
