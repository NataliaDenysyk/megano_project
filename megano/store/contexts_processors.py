from store.configs import settings


def name_shop(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "title_site"
    для вывода названия магазина в "header" любого шаблона сайта
    """

    return {'title_site': settings.get_site_name()}

