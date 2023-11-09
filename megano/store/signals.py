from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Banners


@receiver(post_save, sender=Banners)
def cache_deleted_banners(**kwargs) -> None:
    """ Удаление кеша баннера при изменении, добавлении модели """
    try:
        cache.delete('banners')
    except AttributeError:
        pass
