from django.contrib import admin
from .models import Profile, StoreSettings


class StoreSettingsInline(admin.TabularInline):
    model = StoreSettings
    verbose_name = 'Настройки магазина'
    verbose_name_plural = 'Настройки магазина'


@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'role']
    list_display_links = ['pk', 'user']
    list_filter = ['role']

    def get_inlines(self, request, obj):
        """
        Определяет отображение настроек магазина при выполнении условия
        """

        inlines = super().get_inlines(request, obj)

        if not obj or obj.role != 'buyer':
            inlines += (StoreSettingsInline,)

        return inlines
