from random import choices

from django import template
from django.core.cache import caches

from ..models import Banners

register = template.Library()


@register.inclusion_tag('banner/banner_tpl_main.html')
def banner_main_page() -> dict:
    """
    Caching of random three banners is created.
    """
    banners = caches.get_or_set('banners', choices(Banners.objects.all(), k=3))

    return {'banners': banners}
