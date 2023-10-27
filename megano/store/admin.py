from django.contrib import admin

from .models import Banners, Discount


class AdminBanner(admin.ModelAdmin):
    list_display = ['title', 'link', 'images', 'is_active', 'update_at']
    list_display_links = ['title']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Banners, AdminBanner)


@admin.register(Discount)
class AdminProduct(admin.ModelAdmin):
    pass
