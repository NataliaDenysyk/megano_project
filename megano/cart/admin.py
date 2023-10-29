from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    """
    Description of the basket admin model.
    """
    list_display = ['user', 'product_name', 'quantity', 'created_at', 'updated_at']
    list_filter = ['created_at', 'products']
    search_fields = ['user', 'products']
    list_editable = ['quantity',]
    list_per_page = 20

    def product_name(self, obj: Cart) -> str:
        if len(obj.products.name) > 20:
            return f"{obj.products.name[:20]}..."
        return f"{obj.products.name}"

    product_name.short_description = 'Товары'

    # TODO: доработать вывод иконки товаров
    # def icon_image(self, obj):
    #     """
    #     Returns an image as an icon.
    #
    #     :rtype: str
    #     """
    #     print(obj.products.images)
    #     return mark_safe(f"<img src='{obj.products.images.url}' width=50>")
    #
    # icon_image.short_description = 'Иконка'


admin.site.register(Cart, CartAdmin)
