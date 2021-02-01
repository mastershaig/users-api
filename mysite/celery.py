from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
import logging
from django.conf import settings
from celery.schedules import crontab

logger = logging.getLogger("Celery")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if settings.PROD:
    app.conf.update(
        BROKER_URL='redis://:{password}@redis:6379/0'.format(password=os.environ.get('REDIS_PASSWORD')),
        CELERY_RESULT_BACKEND='redis://:{password}@redis:6379/1'.format(password=os.environ.get('REDIS_PASSWORD')),
        CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
    )
else:
    app.conf.update(
        BROKER_URL='redis://:dKqs72RhtaPPYyfN@redis:6379/0',
        CELERY_RESULT_BACKEND='redis://:dKqs72RhtaPPYyfN@redis:6379/1',
        CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
    )
#
app.conf.beat_schedule = {
    'update_user_age_average_daily': {
        'task': 'users.tasks.update_user_average',
        'schedule': crontab(minute="00", hour="00", day_of_month="*", month_of_year="*", day_of_week="*"),
    },
}
app.conf.timezone = 'Europe/Berlin'
