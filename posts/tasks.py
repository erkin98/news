from celery import shared_task
from celery.utils.log import get_task_logger
from posts.models import Post

logger = get_task_logger(__name__)


@shared_task(queue="celery", name="reset_votes")
def reset_votes():
    updated_count = Post.objects.update(votes=0)
    logger.info("Votes reset for %s posts", updated_count)
