from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from compare.services import (get_comparison_list,
                              _add_product_to_comparison,
                              get_compare_info)
from store.models import Product


class AddToComparisonView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Создаем уникальный comparison_id
        comparison_id = product.get_comparison_id()
        # сервис по добавлению товара к сравнению
        _add_product_to_comparison(request, comparison_id)

        return HttpResponseRedirect(reverse('store:catalog'))


class ComparisonView(View):
    template_name = 'compare/compare_products.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                # Если пользователь авторизован, используем сессии
                comparison_list = request.session.get('comparison_list', [])
            else:
                # Если пользователь не авторизован, используем куки
                comparison_list = request.COOKIES.get('comparison_list', '').split(',')
            if len(comparison_list) == 0:
                return redirect(reverse_lazy("compare:comparison_none"))
            products = get_comparison_list(comparison_list)
            result = get_compare_info(products)
            return render(request, self.template_name, context={'product_characteristic_list': result})
        except:
            return redirect(reverse_lazy("compare:comparison_error"))


class ComparisonErrorView(TemplateView):
    template_name = 'compare/compare_error.html'

    def get(self, request, *args, **kwargs):
        message = 'Нельзя сравнивать несравнимое. Выберите товары из одной категории. Добавь товары снова'
        if request.user.is_authenticated:
            # Если пользователь авторизован, используем сессии
            comparison_list = request.session.get('comparison_list', [])
        else:
            # Если пользователь не авторизован, используем куки
            comparison_list = request.COOKIES.get('comparison_list', '').split(',')
        comparison_list.clear()
        return render(request, self.template_name, context={'message': message})


class ComparisonNoneView(TemplateView):
    template_name = 'compare/compare_none.html'

    def get(self, request, *args, **kwargs):
        message = 'Тут пока ничего нет. Добавь товары к сравнению'
        return render(request, self.template_name, context={'message': message})
