from django import template

from megano.store.models import Banners

from random import choice

register = template.Library()


@register.inclusion_tag('banner/banner_tpl_main.html')
def banner_main_page() -> dict:
    banners = Banners.objects.all()
    if banners.all().count() > 3:
        random_banners = [choice(banners) for _ in range(3)]
        return {'banners': random_banners[0]}

    return {'banners': banners}
