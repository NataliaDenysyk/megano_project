from typing import Dict


def category_image_directory_path(instance) -> str:
    """
    Функция coздания пути к картинке категории
    """

    return f'assets/img/icons/departments/{instance.pk}.svg'


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    """
    Функция генерирует путь сохранения изображений с привязкой к id товара

    :param instance: объект ProductImage
    :param filename: имя файла
    :return: str - путь для сохранения
    """

    return f'products/product_{instance.product_id}/{filename}'


def jsonfield_default_description() -> Dict:
    """
    Определяет дефолтное значение поля description,
    где ожидаются данные в виде словаря, в котором:
        'card_text': [] - список строк
        'title': '' - строка
        'text_bottom': '', - строка
        'text_bottom_ul': [] - список строк
    """

    return {
        'card_text': [],
        'title': '',
        'text_bottom': '',
        'text_bottom_ul': [],
    }


def jsonfield_default_feature() -> Dict:
    """
    Определяет дефолтное значение поля feature,
    где ожидаются данные в виде - {key: value}
    """

    return {'': ''}


def discount_images_directory_path(instance: 'Discount', filename: str) -> str:
    """
    Функция генерирует путь сохранения изображений с привязкой к id скидки
    """

    return f'discount/discount{instance.id}/{filename}'
