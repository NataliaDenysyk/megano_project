from django import template

register = template.Library()


@register.filter(name="split_string")
def split_string(value, separator) -> list:
    """
    Позволяет преобразовать строку в список по символу

    :value: string передаваемая строка.
    :separator: string символ разделитель.
    """
    date = value.split(separator)
    date.append(' '.join(date[1:]))
    del date[1:3]
    return date
