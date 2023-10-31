from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    """
    Регистрация модели корзины в админ панели.
    """
    list_display = ['user', 'product_name', 'quantity', 'icon_image', 'created_at', 'updated_at']
    list_filter = ['created_at', 'products']
    search_fields = ['user', 'products']
    list_editable = ['quantity',]
    list_per_page = 20

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

    def icon_image(self, obj: Cart) -> str:
        """
        Возвращает ссылку на изображение товара в виде иконки.
        """
        return mark_safe(f"<img src='{obj.products.images.url}' width=50>")

    icon_image.short_description = 'Иконка'


admin.site.register(Cart, CartAdmin)
