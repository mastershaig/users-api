from __future__ import absolute_import, unicode_literals
from celery import shared_task
from users.models import Users
from django.core.cache import cache
# Use celery shared_task documentation here
# http://docs.celeryproject.org/en/latest/faq.html


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'default_retry_delay': 5})
def update_user_average():
    """
        Refresh the cached age_sum, and age_count.
        Calculate them again at 00:00 while some users' age can change in a day.
    """
    all_data = Users.objects.all()
    age_sum = 0
    for val in all_data:
        age_sum += val.get_age()
    cache_age_len = len(all_data)
    cache.set('cache_age_len', cache_age_len, 86400)
    cache.set('cache_age_sum', age_sum, 86400)

    return "Celery user average calculation done!"