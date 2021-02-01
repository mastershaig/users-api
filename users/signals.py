from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Users
from django.core.cache import cache

"""
Average of user ages (sum of ages and count) are updated each time right after new users are inserted
"""
@receiver(post_save, sender=Users)
def object_post_save_handler(sender, **kwargs):
    user = kwargs.get('instance')
    cache_age_sum = cache.get('cache_age_sum')
    cache_age_len = cache.get('cache_age_len')
    if cache_age_len is not None:
        cache_age_len = cache_age_len + 1
    if cache_age_sum is not None:
        cache_age_sum = cache_age_sum + user.get_age()
    cache.set('cache_age_sum', cache_age_sum, 86400)
    cache.set('cache_age_len', cache_age_len, 86400)
