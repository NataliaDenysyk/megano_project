from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from store.models import Product
from services.services import CatalogServices


class CatalogListView(ListView):
    """
    Вьюшка каталога
    """
    template_name = 'store/catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 8

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
        self.object_list = self.context_object_name

        return self.render_to_response(context)
