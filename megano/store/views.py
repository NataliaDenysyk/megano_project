from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

from store.forms import FilterForm
from store.models import Product
from services.services import CatalogService, ProductService


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
        context['filter'] = FilterForm()
        for i_product in context['products']:
            i_product.price = ProductService(i_product)._get_average_price()

        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Функция обрабатывает post-запросы на странице каталога

        :param request: объект запроса
        """

        self.object_list = self.context_object_name
        context = super().get_context_data(**kwargs)
        context.update(CatalogService(request.POST)._get_context_from_post())

        return self.render_to_response(context)


# TODO добавить кэширование страницы
class ProductDetailView(DetailView):
    """
    Вьюшка детальной страницы товара
    """

    template_name = 'store/product/product-detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция отображает переданный шаблон

        :param kwargs:
        :return:
        """

        context = super().get_context_data(**kwargs)
        context.update(ProductService(context['product'])._get_context())

        return context
