from __future__ import absolute_import
import os
import logging
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
app = Celery('news')
logger = logging.getLogger("Celery")
app.conf.enable_utc = False
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    "trigger-reset_votes": {
        "task": "posts.tasks.reset_votes",
        "schedule": crontab(hour=0, minute=0)
    }
}
app.conf.update(
    BROKER_URL='redis://redis:6379/0',
    CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
    CELERY_RESULT_BACKEND='redis://redis:6379/1',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Baku'

)
