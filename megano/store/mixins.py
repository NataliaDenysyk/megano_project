from django.contrib import admin

from .models import Product


class ChangeListMixin:
    """
    Класс ChangeListMixin миксуется для отображения "sidebar" и навигации в "header" в шаблоне настроек
    """
    def get_change_list_admin(self, **kwargs):
        model = Product
        context = kwargs
        context = dict(list(context.items()) + list(admin.site.each_context(self.request).items()))
        context.update(
            opts=model._meta
        )
        return context
