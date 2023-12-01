from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from services.services import DiscountProduct
from .cart import Cart
from store.models import Product


class CartListView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        discount = DiscountProduct()
        context.update(
            {
                'carts': cart,
                'total_price': discount.get_priority_discount(cart=cart)
            }
        )
        return context


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
