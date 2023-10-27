from django.contrib import admin

from .models import Banners, Product, Discount

# TODO добавить инлайны в товары


class AdminBanner(admin.ModelAdmin):
    list_display = ['title', 'link', 'images', 'is_active', 'update_at']
    list_display_links = ['title']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Banners, AdminBanner)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):

    list_display = 'pk', 'name', 'description_short', 'availability'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name', 'created_at', 'availability'
    search_fields = 'name', 'description'
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'feature'),
        }),
        ('Images', {
            'fields': ('images',),
        }),
        ('Extra options', {
            'fields': ('availability', 'slug'),
        }),
    ]

    def description_short(self, obj: Product) -> str:
        """
        Функция уменьшает длинные описания

        :param obj: Product object
        :return: string
        """

        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'

    description_short.short_description = 'Описание'


@admin.register(Discount)
class AdminProduct(admin.ModelAdmin):
    pass
