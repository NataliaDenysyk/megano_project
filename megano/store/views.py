from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.core.cache import cache

from store.forms import FilterForm
from store.models import Product
from services.services import CatalogService, ProductService, CategoryServices
import re
from typing import Any

from .configs import settings
from .mixins import ChangeListMixin
from .models import Product


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


# Представления для отображения страницы настроек
# в административной панели

class SettingsView(ChangeListMixin, ListView):
    """
    Класс SettingsView отображает страницу с настройками
    """
    model = Product
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))


class ClearCacheAll(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheAll позволяет очистить весь кеш сайта
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.clear()
        messages.success(self.request, 'Кеш полностью очищен.')  # Добавление сообщения для действия
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))

    def dispatch(self, request, *args, **kwargs):
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheBanner(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheBanner позволяет очистить кеш Баннера
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("banners")
        messages.success(self.request, 'Кеш баннера очищен.')
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))

    def dispatch(self, request, *args, **kwargs):
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheCart(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheCart позволяет очистить кеш Корзины
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("cart")
        messages.success(self.request, 'Кеш корзины очищен.')
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))

    def dispatch(self, request, *args, **kwargs):
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheProductDetail(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheProductDetail позволяет очистить кеш детализации продуктов
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("product_detail")
        messages.success(self.request, 'Кеш продукта очищен.')
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))

    def dispatch(self, request, *args, **kwargs):
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class SiteName(ChangeListMixin, TemplateView):
    """
    Класс SiteName позволяет задать новое название интернет магазина
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(
            title="site name",
        )
        return dict(list(context.items()) + list(change_list.items()))

    def post(self, request):
        title_site = request.POST.get('title_site')
        if title_site:
            settings.set_site_name(title_site)
            messages.success(self.request, 'Название магазина успешно изменено')
        else:
            messages.error(self.request, 'Поле не должно быть пустым')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupBannerView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupBannerView позволяет задать или обновить время кеширования Баннера
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(
            title="site name",
        )
        return dict(list(context.items()) + list(change_list.items()))

    def post(self, request):
        cache_time_banner = request.POST.get('cache_time_banner')
        if re.findall(r'[0-9]', cache_time_banner):
            settings.set_cache_banner(cache_time_banner)
            messages.success(self.request, 'Время кеширование Баннера установлено')
        else:
            messages.error(self.request, 'Поле не должно быть пустым и содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupCartView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupCartView позволяет задать или обновить время кеширования Корзины
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(
            title="site name",
        )
        return dict(list(context.items()) + list(change_list.items()))

    def post(self, request):
        cache_time_cart = request.POST.get('cache_time_cart')
        if re.findall(r'[0-9]', cache_time_cart):
            settings.set_cache_cart(cache_time_cart)
            messages.success(self.request, 'Время кеширование Корзины установлено')
        else:
            messages.error(self.request, 'Поле не должно быть пустым и содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupBProdDetailView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupBProdDetailView позволяет задать или обновить время кеширования детальной информации продукта
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(
            title="site name",
        )
        return dict(list(context.items()) + list(change_list.items()))

    def post(self, request):
        cache_time_prod_detail = request.POST.get('cache_time_prod_detail')
        if re.findall(r'[0-9]', cache_time_prod_detail):
            settings.set_cache_product_detail(cache_time_prod_detail)
            messages.success(self.request, 'Время кеширование детализации продукта установлено')
        else:
            messages.error(self.request, 'Поле не должно быть пустым и содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))