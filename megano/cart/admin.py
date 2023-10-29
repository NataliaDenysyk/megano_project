from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    """
    Description of the basket admin model.
    """
    list_display = ('user', 'products', 'quantity', 'icon_image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'products')
    search_fields = ('user__username', 'products__title')
    list_editable = ('quantity',)
    list_per_page = 15
    # prepopulated_fields = {'slug': ('products',)}
    # TODO После добавления модели продуктов раскомментировать

    # TODO После добавления модели продуктов отредактировать поле с изображением (photo or image)
    def icon_image(self, request) -> str:
        """
        Returns an image as an icon.

        :rtype: str
        """
        return mark_safe(f'<img src="{request.product.get(id=request.id).image.url}" width="40"/>')

    icon_image.short_description = 'Иконка'


admin.site.register(Cart, CartAdmin)
