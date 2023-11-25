from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Banners, Product


@receiver(post_save, sender=Banners)
def cache_deleted_banners(**kwargs) -> None:
    """ Удаление кеша баннера при изменении, добавлении модели """
    try:
        cache.delete('banners')
    except AttributeError:
        pass


@receiver(post_save, sender=Product)
def reset_product_list_cache(sender, instance, **kwargs):
    cache_key = 'product_list_cache'
    cache.delete(cache_key)


@receiver(post_save, sender=Product)
def cache_deleted_product(**kwargs) -> None:
    """ Удаление кеша товара и списка товаров при изменении, добавлении модели """
    try:
        slug = kwargs['instance'].slug
        cache.delete(f'product-{slug}')
        cache.delete('products')

    except AttributeError:
        pass

