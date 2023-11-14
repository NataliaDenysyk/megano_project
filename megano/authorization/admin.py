from django.contrib import admin
from .models import Profile

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
class AuthorProfile(admin.ModelAdmin):
    """
   Регистрация модели профиля в админ панели.
   """
    actions = [
        mark_archived, mark_unarchived
    ]
    list_display = [
        'pk',
        'user',
        'description',
        'avatar',
        'name_store',
        'address',
        'sale',
        'viewed_orders',
        'archived',
        'role',
    ]
    list_display_links = 'pk', 'user'
    ordering = 'pk', 'user', 'archived', 'name_store'
    list_filter = ['archived']
    search_fields = 'user', 'name_store'
    readonly_fields = ['viewed_orders',]
    fieldsets = [
        (None, {
            'fields': ('role', 'user', 'name_store', 'description', 'avatar', 'address',),
        }),
        ('Additionally', {
            'fields': ('sale',)
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
        })
    ]

    def get_queryset(self, request):
        return Profile.objects.select_related('user', 'viewed_orders')

    def user_verbose(self, obj: Profile) -> str:
        """
        Функция возвращает навание магазина или имя и фамилию польователя, если есть.
        """
        if obj.name_store:
            return obj.name_store
        elif obj.user.first_name and obj.user.last_name:
            return f'{obj.user.first_name}, {obj.user.last_name}'
        elif obj.user.first_name or obj.user.last_name:
            return obj.user.first_name or obj.user.last_name
        else:
            return obj.user.username
    def get_html_images(self, obj):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 60х 60.
        """
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" alt=""width="60">')
        else:
            return 'not url'

    get_html_images.short_description = 'Изображение'

    def get_actions(self, request):
        """"
        Функкция удаляет 'delete_selected' из actions(действие) в панели администратора
        """
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

