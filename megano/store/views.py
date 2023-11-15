from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

from store.filters import ProductFilter
from store.models import Product
from services.services import ProductService


class CatalogListView(ListView):
    """
    Вьюшка каталога
    """

    template_name = 'store/catalog/catalog.html'
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self) -> Product.objects:
        """
        Функция возвращает отфильтрованные продукты

        :return queryset Product objects
        """

        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция возвращает контекст

        """

        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset.form

        for i_product in context['products']:
            i_product.price = ProductService(i_product)._get_average_price()

        return context


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
        Функция возвращает контекст

        """

        context = super().get_context_data(**kwargs)
        context.update(ProductService(context['product'])._get_context())

        return context
