from celery import shared_task
from celery_batches import Batches

from src.redirect_events.dependencies import build_redirect_event_service
from src.redirect_events.schemas import BaseRedirectEventSchema


redirect_event_service = build_redirect_event_service()


@shared_task(
    base=Batches,
    flush_every=5,
    flush_interval=60,
    name="src.redirect_events.task.store_redirect_events",
)
def store_redirect_events(requests):
    base_redirect_events = [
        BaseRedirectEventSchema.model_validate(request.kwargs) for request in requests
    ]
    redirect_event_service.store_redirect_events(base_redirect_events)
