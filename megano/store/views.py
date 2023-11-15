from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from django.views.generic import TemplateView

from store.models import Comparison, Category, Product, Tag, Discount
from services.services import CategoryServices


class CategoryView(TemplateView):
    """"
    Класс получения категорий и подкатегорий
    """
    template_name = 'store/category_product.html'

    def get_context_data(self, **kwargs):
        """"
        Функция отображает переданный шаблон
        """
        context = super().get_context_data()
        if self.request.GET.get('category_slug'):
            category_slug = self.request.GET['category_slug']
            context = CategoryServices()._product_by_category(category_slug)

        else:
            context = CategoryServices()._sorting_products(self.request)
        return context
