from datetime import datetime

from store.configs import settings
from store.forms import SearchForm


def store(request):
    """
    Контекстный процессор позволяет воспользоваться переменными "mount" и "today"
    для вывода даты в шаблонах сайта.
    """
    return {
        'mount': settings,
        'today': datetime.today().strftime("%d-%b-%Y"),
        'form_search': SearchForm(),
    }


def name_shop(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "title_site"
    для вывода названия магазина в "header" любого шаблона сайта
    """

    return {'title_site': settings.get_site_name()}
