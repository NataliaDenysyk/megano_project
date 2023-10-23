from django import template

from megano.store.models import Banners

register = template.Library()


@register.inclusion_tag('banner/banner_tpl_main.html')
def banner_center() -> dict:
    banners = Banners.objects.all()
    return {'banners': banners}
