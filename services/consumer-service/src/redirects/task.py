from celery import shared_task
from celery_batches import Batches

from src.redirects.dependencies import build_redirect_service
from src.redirects.schemas import BaseRedirectSchema


redirect_service = build_redirect_service()


@shared_task(
    base=Batches,
    flush_every=5,
    flush_interval=60,
    name="src.redirects.task.store_redirects",
)
def store_redirects(requests):
    base_redirects = [
        BaseRedirectSchema.model_validate(request.kwargs) for request in requests
    ]
    redirect_service.store_redirects(base_redirects)
