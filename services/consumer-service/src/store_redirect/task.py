from celery import shared_task
from celery_batches import Batches


@shared_task(
    base=Batches,
    flush_every=5,
    flush_interval=60,
    name="task.store_redirect",
)
def store_redirects(requests):
    print(*[requset.args for requset in requests], sep="\n")
