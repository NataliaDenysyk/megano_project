from django.contrib import admin

from .models import Product
from .configs import settings


class ChangeListMixin:
    """
    Класс ChangeListMixin миксуется для отображения "sidebar" и навигации в "header" в шаблоне настроек
    """
    def get_change_list_admin(self, **kwargs):
        model = Product
        context = kwargs
        context = dict(list(context.items()) + list(admin.site.each_context(self.request).items()))
        context.update(
            opts=model._meta,
            title_site=settings.get_site_name(),
            cache_banner=settings.get_cache_banner(),
            cache_cart=settings.get_cache_cart(),
            cache_prod_detail=settings.get_cache_product_detail(),
            cache_seller=settings.get_cache_seller(),
            cache_catalog=settings.get_cache_catalog()
        )
        return context
