from celery.utils.log import get_task_logger
from news.celery import app
from celery import shared_task
from posts.models import Post

logger = get_task_logger(__name__)


@shared_task(queue="celery", name="reset_votes")
@app.task
def reset_votes():
    posts = Post.objects.all()
    for post in posts:
        post.votes = 0
        post.save()
    logger.info("Votes resetting")
