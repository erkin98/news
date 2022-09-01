from __future__ import absolute_import
import os
import logging
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from pathlib import Path
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
app = Celery("news")
logger = logging.getLogger("Celery")
app.conf.enable_utc = False
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


app.conf.beat_schedule = {
    "trigger-reset_votes": {
        "task": "posts.tasks.reset_votes",
        "schedule": crontab(hour=0, minute=0),
    }
}
app.conf.update(
    BROKER_URL=str(os.getenv('BROKER_URL')),
    CELERYBEAT_SCHEDULER=str(os.getenv('CELERYBEAT_SCHEDULER')),
    CELERY_RESULT_BACKEND=str(os.getenv('CELERY_RESULT_BACKEND')),
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=[
        "json",
    ],
    CELERY_TASK_SERIALIZER="json",
    CELERY_RESULT_SERIALIZER="json",
    CELERY_TIMEZONE="Asia/Baku",
)
