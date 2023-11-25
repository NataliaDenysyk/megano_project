from .cart import Cart


def cart(request) -> dict:
    """
    Контекстный процессор позволяет воспользоваться переменной "cart" в любом шаблоне сайта
    """
    return {'cart': Cart(request)}
