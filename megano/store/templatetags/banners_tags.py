from django import template
from django.http import HttpResponse
from django.core.cache import cache

from random import choices

from ..models import Banners

register = template.Library()


@register.inclusion_tag('banner/banner_tpl_main.html')
def banner_main_page() -> dict:
    """
    Caching of random three banners is created.
    """
    try:
        banners = cache.get_or_set('banners', choices(Banners.objects.all(), k=3))
        return {'banners': banners}
    except Exception as err:
        HttpResponse('Not Banners', err)  # TODO заменить заглушку на файл с логами

