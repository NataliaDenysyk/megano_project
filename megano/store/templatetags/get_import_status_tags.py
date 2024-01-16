from celery.result import AsyncResult
from django import template
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_import_status() -> str:
    """
    Получает статус выполнения импорта, если он есть
    """

    task_id = cache.get('task_id')

    if task_id:
        result = AsyncResult(task_id)
        if result.ready():
            if result.successful():
                return 'Выполнен успешно'

            return 'Завершен с ошибкой'

        return 'В процессе выполнения'

    return 'Не было ни одного импорта'
