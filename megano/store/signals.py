from django.core.cache import caches
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Banners


@receiver(post_save, sender=Banners)
def cache_deleted_banners(**kwargs) -> None:
    """
    ПWhen changing the Banners model, caching of random banners is removed.
    """
    caches.delete('banners')
