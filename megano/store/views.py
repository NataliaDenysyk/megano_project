from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from store.models import Comparison, Category, Product, Tag, Discount
from django.views.generic import TemplateView

from services.services import CatalogServices


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
