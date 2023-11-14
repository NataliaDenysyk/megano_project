from datetime import datetime

from store.configs import settings


def name_shop(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "title_site"
    для вывода названия магазина в "header" любого шаблона сайта
    """
    return {'title_site': settings.get_site_name()}


def time_cache_banner(request) -> dict:
    """

    :param request:
    :return:
    """
    return {'cache_banner': settings.get_cache_banner()}


def time_cache_сart(request) -> dict:
    """

    :param request:
    :return:
    """
    return {'cache_cart': settings.get_cache_cart()}


def time_cache_prod_detail(request) -> dict:
    """

    :param request:
    :return:
    """
    return {'cache_prod_detail': settings.get_cache_product_detail()}
