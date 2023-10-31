from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from store.models import Comparison


# Create your views here.

class ComparisonListView(ListView):
    """
    Отображает список товаров, добавленных к сравнению

    """

    template_name = ''
    context_object_name = 'comparisons'
    paginate_by = 3

    def get_queryset(self):
        """
        Отбирает объекты в зависимости от текущего пользователя

        :return: queryset
        """

        return Comparison.objects.filter(user=self.request.user)


def add_product_to_comparison(request):
    """
    Добавляет товар в список сравнения

    :param request: объект запроса
    """
    Comparison.objects.create()


def get_amount_from_comparison(request) -> int:
    """
    Получение количества товаров в списке сравнения текущего пользователя

    :param request: объект запроса
    :return: int
    """
    amount_products = Comparison.objects.filter(user=request.user).count()
    return amount_products


class ComparisonDeleteView(DeleteView):
    """
    Удаление одного товара из сравнения

    """

    model = Comparison
    success_url = reverse_lazy('')
