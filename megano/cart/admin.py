from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    """
    Регистрация модели корзины в админ панели.
    """
    list_display = ['user', 'products', 'quantity', 'created_at', 'updated_at']
    list_filter = ['created_at', 'products']
    search_fields = ['user', 'products']
    list_editable = ['quantity',]
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        (None, {
            "fields": ('user', 'products', 'quantity'),
        }),
    ]

    def product_name(self, obj: Cart) -> str:
        """
        Возвращает укороченное название товара.
        Если название товара больше 20 символов,
        возвращает строку в виде <название...>.
        """
        if len(obj.products.name) > 20:
            return f"{obj.products.name[:20]}..."
        return f"{obj.products.name}"

    product_name.short_description = 'Товары'




admin.site.register(Cart, CartAdmin)
