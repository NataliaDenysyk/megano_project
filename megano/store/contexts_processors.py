from datetime import datetime

from store.configs import settings


def time_today(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "today"
    для вывода даты в шаблонах сайта.
    """
    return {'today': datetime.today().strftime("%Y-%m-%b ")}


def name_shop(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "title_site"
    для вывода названия магазина в "header" любого шаблона сайта.
    """
    return {'title_site': settings.get_site_name()}


def time_cache_banner(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "cache_banner"
    для использования установки времени кеширования баннера.
    """
    return {'cache_banner': settings.get_cache_banner()}


def time_cache_сart(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "cache_cart"
    для использования установки времени кеширования корзины.
    """
    return {'cache_cart': settings.get_cache_cart()}


def time_cache_prod_detail(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "cache_prod_detail"
    для использования установки времени кеширования детальной информации продукта.
    """
    return {'cache_prod_detail': settings.get_cache_product_detail()}
