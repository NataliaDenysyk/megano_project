from django.contrib import admin
from .models import Profile, StoreSettings


class StoreSettingsInline(admin.TabularInline):
    model = StoreSettings
    verbose_name = 'Настройки магазина'
    verbose_name_plural = 'Настройки магазина'

from django.db.models import QuerySet
from django.http import HttpRequest


from django.utils.safestring import mark_safe


@admin.action(description='Archive')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Profile)
class AuthorAdmin(admin.ModelAdmin):
    """
      Регистрация модели профиля в админ панели.
      """
    actions = [
        mark_archived, mark_unarchived
    ]
    list_display = ['pk', 'user', 'get_html_avatar', 'role']
    list_display_links = ['pk', 'user']
    list_filter = ['role']
    prepopulated_fields = {'slug': ('name_store', )}

    def get_inlines(self, request, obj):
        """
        Определяет отображение настроек магазина при выполнении условия
        """

        inlines = super().get_inlines(request, obj)

        if not obj or obj.role != 'buyer':
            inlines += (StoreSettingsInline,)

        return inlines

    def get_html_avatar(self, obj):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 50х 50.
        """
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" alt=""width="50">')

    get_html_avatar.short_description = 'Аватар'

    def get_actions(self, request):
        """"
        Функкция удаляет 'delete_selected' из actions(действие) в панели администратора
        """
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

