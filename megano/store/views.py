from django.db.models import Count, Q
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.cache import cache

from store.filters import ProductFilter
from store.models import Product, Orders, Offer
from services.services import ProductService, CategoryServices
import re
from typing import Any

from .configs import settings
from .mixins import ChangeListMixin


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


class ProductListView(ListView):
    """
    Выводит весь список продуктов на главной странице
    """
    model = Product
    template_name = 'base/base.html'
    context_object_name = 'products'


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
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
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
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
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
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
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
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheSeller(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheProductDetail позволяет очистить кеш детализации продуктов
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("seller")
        messages.success(self.request, 'Кеш продавца очищен.')
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class SiteName(ChangeListMixin, TemplateView):
    """
    Класс SiteName позволяет задать новое название интернет магазина
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        title_site = request.POST.get('title_site')
        if title_site:
            settings.set_site_name(title_site)
            messages.success(self.request, 'Название магазина успешно изменено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupBannerView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupBannerView позволяет задать или обновить время кеширования Баннера
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_banner = request.POST.get('cache_time_banner')
        time_banner = re.findall(r'[0-9]+', cache_time_banner)
        if time_banner:
            settings.set_cache_banner(time_banner[0])
            messages.success(self.request, 'Время кеширование Баннера установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupCartView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupCartView позволяет задать или обновить время кеширования Корзины
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_cart = request.POST.get('cache_time_cart')
        time_cart = re.findall(r'[0-9]+', cache_time_cart)
        if time_cart:
            settings.set_cache_cart(time_cart[0])
            messages.success(self.request, 'Время кеширование Корзины установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupProdDetailView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupProdDetailView позволяет задать или обновить время кеширования детальной информации продукта
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_prod_detail = request.POST.get('cache_time_prod_detail')
        time_prod_detail = re.findall(r'[0-9]+', cache_time_prod_detail)
        if time_prod_detail:
            settings.set_cache_product_detail(time_prod_detail[0])
            messages.success(self.request, 'Время кеширование детализации продукта установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupSellerView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupSellerView позволяет задать или обновить время кеширования детальной информации продавца
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_seller = request.POST.get('cache_time_seller')
        time_seller = re.findall(r'[0-9]+', cache_time_seller)
        if time_seller:
            settings.set_cache_seller(time_seller[0])
            messages.success(self.request, 'Время кеширование детализации продавца установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class MainPage(ListView):
    """
    Главная страница
    """

    template_name = 'store/index.html'
    model = Product

    def get_queryset(self):
        """
        Queryset:
            'pk': int,
            'preview': image url,
            'name': str,
            'category__name': str,
            'offer__unit_price': Decimal,
            'count': int
        """
        cache_key = 'product_list_cache'
        popular_products = cache.get(cache_key)

        if popular_products is None:
            popular_products = ProductService(self.model).get_popular_products(quantity=5)
            cache.set(cache_key, popular_products, settings.set_popular_products_cache(1))

        return popular_products
