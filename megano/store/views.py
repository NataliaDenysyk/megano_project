from typing import Dict

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from services.services import CatalogServices
from store.forms import FilterForm


class CatalogView2(View):
    """
    Вьюшка каталога
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Функция ловит get-запрос
        """

        context = {
            'filter': FilterForm(),
        }
        return render(request, 'store/category_product.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Функция ловит post-запросы
        """

        if 'filter-button' in request.POST:
            filter_data = FilterForm(request.POST)
            if filter_data.is_valid():
                offers, saved_form = CatalogFilterServices()._filter_products(filter_data)
                products_list = CatalogFilterServices()._get_filtered_products(offers)

                context = {
                    'filter': saved_form,
                    'products_list': products_list,
                }
                print(products_list)
                return render(request, 'store/category_product.html', context=context)

        else:
            filter_data = FilterForm()

        context = {
            'filter': filter_data,
        }
        return render(request, 'store/category_product.html', context=context)


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
        context['filter'] = FilterForm()

        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Функция обрабатывает post-запросы на странице каталога

        :param request: объект запроса
        :param args:
        :param kwargs:
        :return:
        """

        context = CatalogServices()._get_context(request)

        return self.render_to_response(context)
