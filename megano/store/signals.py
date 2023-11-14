from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Banners, Category, Product


@receiver(post_save, sender=Banners)
def cache_deleted_banners(**kwargs) -> None:
    """ Удаление кеша баннера при изменении, добавлении модели """
    try:
        cache.delete('banners')
    except AttributeError:
        pass


@receiver(post_save, sender=Category)
def cache_deleted_category(**kwargs) -> None:
    """ Удаление кеша категорий при изменении, добавлении модели """
    try:
        cache.delete('Category')
    except AttributeError:
        pass


@receiver(post_save, sender=Product)
def cache_deleted_product(**kwargs) -> None:
    """ Удаление кеша продуктов при изменении, добавлении модели """
    try:
        cache.delete('Products')
    except AttributeError:
        pass
