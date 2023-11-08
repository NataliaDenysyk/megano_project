from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from services.services import CatalogServices
from store.models import Product


# TODO: дописать отображение найденных после фильтрации товаров
class CatalogView(TemplateView):
    """
    Вьюшка каталога
    """

    template_name = 'store/category_product.html'

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция отображает переданный шаблон

        :param kwargs:
        :return:
        """

        context = super().get_context_data(**kwargs)
        context = CatalogServices()._get_context(context)

        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Функция обрабатывает post-запросы на странице каталога

        :param request: объект запроса
        :param args:
        :param kwargs:
        :return:
        """

        context = CatalogServices()._get_context_from_post(request)

        return self.render_to_response(context)
