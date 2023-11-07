from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from .cart import Cart
from store.models import Product


def cart_view(request: WSGIRequest) -> HttpResponse:
    """
    Страница отображения всех товаров в корзине

    :param request: запрос
    :return: HttpResponse - страница корзины
    """
    cart = Cart(request)
    return render(request, 'cart/index.html', {'carts': cart})


def add_product_to_cart(request: WSGIRequest, slug: Product) -> HttpResponse:
    """
    Добавление товара в корзину

    :param request: запрос
    :param slug: slug товара
    :return: HttpResponse - текущая страница
    """
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    cart.add_product(product, update=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_product(request: WSGIRequest, slug: Product) -> HttpResponseRedirect:
    """
    Добавить одну единицу товара в корзине

    :param request: запрос
    :param slug: slug товара
    :return: HttpResponse - текущая страница
    """
    cart = Cart(request)
    cart.add(get_object_or_404(Product, slug=slug))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def take_product(request: WSGIRequest, slug: Product) -> HttpResponseRedirect:
    """
    Убрать одну единицу товара в корзине

    :param request: запрос
    :param slug: slug товара
    :return: HttpResponse - текущая страница
    """
    cart = Cart(request)
    cart.take(get_object_or_404(Product, slug=slug))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_product_from_cart(request: WSGIRequest, slug: Product) -> HttpResponseRedirect:
    """
    Удаление продукта из корзины

    :param request: запрос
    :param slug: slug товара
    :return: HttpResponse - текущая страница
    """
    cart = Cart(request)
    cart.remove(get_object_or_404(Product, slug=slug))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_cart(request: WSGIRequest) -> HttpResponseRedirect:
    """
    Очистка корзины от всех продуктов

    :param request: запрос
    :return: HttpResponse - текущая страница
    """
    cart = Cart(request)
    cart.clear()
    return redirect('cart:index')

