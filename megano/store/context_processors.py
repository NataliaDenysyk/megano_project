from datetime import datetime

from store.configs import settings


def store(request):
    """
    Контекстный процессор позволяет воспользоваться переменными "mount" и "today"
    для вывода даты в шаблонах сайта.
    """
    return {
        'mount': settings,
        'today': datetime.today().strftime("%d-%b-%Y")
    }
