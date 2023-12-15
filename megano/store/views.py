from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.cache import cache

from .configs import settings
from .forms import ReviewsForm, SearchForm, OrderCreateForm, RegisterForm
from .filters import ProductFilter
from .mixins import ChangeListMixin
from authorization.models import Profile
from cart.cart import Cart
from cart.models import Cart as Basket
from .models import Product, Orders, Offer, BannersCategory
from services.services import (
    ProductService,
    CatalogService,
    CategoryServices,
    GetParamService,
    ProductsViewService,
    ReviewsProduct,
    MainService,
)

import re
from typing import Any


class CatalogListView(ListView):
    """
    Вьюшка каталога
    """

    template_name = 'store/catalog/catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self) -> Product.objects:
        """
        Функция возвращает отфильтрованные продукты по категории, тегу, фильтру или сортировке
        """

        queryset = super().get_queryset()
        queryset = cache.get_or_set('products', queryset, settings.get_cache_catalog())

        if self.request.resolver_match.captured_kwargs.get('slug'):
            queryset = CategoryServices.product_by_category(
                self.request.resolver_match.captured_kwargs['slug']
            )

        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        self.filterset = CatalogService().catalog_processing(self.request, self.filterset)

        return self.filterset.qs

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция возвращает контекст
        """

        form_search = SearchForm(self.request.GET or None)
        context = super().get_context_data(**kwargs)

        context['form_search'] = form_search
        context['filter'] = self.filterset.form
        context['tags'] = CatalogService.get_popular_tags()

        for product in context['products']:
            product.price = ProductService(product).get_average_price()

        context['full_path'] = GetParamService(self.request.get_full_path()).remove_param('sorting').get_url()

        return context


class ProductDetailView(DetailView):
    """
    Вьюшка детальной страницы товара
    """

    template_name = 'store/product/product-detail.html'
    model = Product
    context_object_name = 'product'

    def get_object(self, *args, **kwargs) -> Product.objects:
        slug = self.kwargs.get('slug')
        instance = Product.objects.get(slug=slug)
        product = cache.get_or_set(f'product-{slug}', instance, settings.get_cache_product_detail())

        ProductsViewService(self.request).add_product_to_viewed(product.id)

        return product

    def get_context_data(self, **kwargs) -> HttpResponse:
        form_search = SearchForm(self.request.GET or None)
        context = super().get_context_data(**kwargs)

        context['form_search'] = form_search
        context['num_reviews'] = ReviewsProduct.get_number_of_reviews_for_product(self.object)
        context['reviews_num3'], context['reviews_all'] = ReviewsProduct.get_list_of_product_reviews(self.object)
        context['form'] = ReviewsForm()
        context.update(ProductService(context['product']).get_context())

        return context

    def post(self, request, *args, **kwargs):
        form = ReviewsForm(request.POST)
        if form.is_valid():
            ReviewsProduct.add_review_to_product(request, form, self.kwargs['slug'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
    Класс ClearCacheAll позволяет очистить весь кэш сайта
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.clear()
        messages.success(self.request, 'кэш полностью очищен.')  # Добавление сообщения для действия
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheBanner(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheBanner позволяет очистить кэш Баннера
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("banners")
        messages.success(self.request, 'кэш баннера очищен.')
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheCart(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheCart позволяет очистить кэш Корзины
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("cart")
        messages.success(self.request, 'кэш корзины очищен.')
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheProductDetail(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheProductDetail позволяет очистить кэш детализации продуктов
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("product_detail")
        messages.success(self.request, 'кэш продукта очищен.')
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheSeller(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheProductDetail позволяет очистить кэш детализации продуктов
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("seller")
        messages.success(self.request, 'кэш продавца очищен.')
        return context

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


class ClearCacheCatalog(ChangeListMixin, TemplateView):
    """
    Класс ClearCacheCatalog позволяет очистить кэш детализации продуктов
    """

    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cache.delete("catalog")
        messages.success(self.request, 'кэш каталога очищен.')
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
    Класс CacheSetupBannerView позволяет задать или обновить время кэширования Баннера
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_banner = request.POST.get('cache_time_banner')
        time_banner = re.findall(r'[0-9]+', cache_time_banner)
        if time_banner:
            settings.set_cache_banner(time_banner[0])
            messages.success(self.request, 'Время кэширование Баннера установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupCartView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupCartView позволяет задать или обновить время кэширования Корзины
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_cart = request.POST.get('cache_time_cart')
        time_cart = re.findall(r'[0-9]+', cache_time_cart)
        if time_cart:
            settings.set_cache_cart(time_cart[0])
            messages.success(self.request, 'Время кэширование Корзины установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupProdDetailView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupProdDetailView позволяет задать или обновить время кэширования детальной информации продукта
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_prod_detail = request.POST.get('cache_time_prod_detail')
        time_prod_detail = re.findall(r'[0-9]+', cache_time_prod_detail)
        if time_prod_detail:
            settings.set_cache_product_detail(time_prod_detail[0])
            messages.success(self.request, 'Время кэширование детализации продукта установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupSellerView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupSellerView позволяет задать или обновить время кэширования детальной информации продавца
    """
    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_seller = request.POST.get('cache_time_seller')
        time_seller = re.findall(r'[0-9]+', cache_time_seller)
        if time_seller:
            settings.set_cache_seller(time_seller[0])
            messages.success(self.request, 'Время кэширование детализации продавца установлено')
        else:
            messages.warning(self.request, 'Поле не должно быть пустым или содержать только цифры')
        return HttpResponseRedirect(reverse_lazy('store:settings'))


class CacheSetupCatalogView(ChangeListMixin, TemplateView):
    """
    Класс CacheSetupCatalogView позволяет задать или обновить время кэширования каталога
    """

    template_name = 'admin/settings.html'

    def post(self, request) -> HttpResponse:
        cache_time_catalog = request.POST.get('cache_time_catalog')
        time_catalog = re.findall(r'[0-9]+', cache_time_catalog)
        if time_catalog:
            settings.set_cache_catalog(time_catalog[0])
            messages.success(self.request, 'Время кэширование детализации продавца установлено')
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

        if len(popular_products) == 0:
            popular_products = ProductService(self.model).get_popular_products(quantity=8)
            cache.set(cache_key, popular_products, settings.set_popular_products_cache(1))

        return popular_products

    def get_context_data(self, **kwargs):
        form_search = SearchForm(self.request.GET or None)
        context = super().get_context_data(**kwargs)

        context['form_search'] = form_search
        context['banners_category'] = BannersCategory.objects.all()[:3]
        context['limited_deals'] = MainService.get_limited_deals()
        context['hot_offers'] = Product.objects.all().filter(discount__is_active=True).distinct('pk')[:9]
        context['limited_edition'] = Product.objects.filter(limited_edition=True).distinct('pk')[:16]

        return context


class OrderRegisterView(CreateView):
    """
    Класс регистрации пользователя.
    После регистрации пользователь авторизуется.
    """
    template_name = 'store/order/order_register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        phone = form.cleaned_data.get('phone')
        Profile.objects.create(
            user=user,
            slug='slug',
            phone=phone,
            description='description',
            address='address',
        )
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(reverse_lazy("store:order_create", kwargs={'pk': user.pk}))


class OrderView(UpdateView):
    """
    Класс позволяет оформить заказ для пользователя и очистить корзину из сессии.
    Перед оформлением заказа товар проверяется:
    1. Проверка на отсутствие товара.
    2. Проверка на кол-во заказанного товара больше, чем доступно в магазине.
    """
    model = User
    template_name = 'store/order/order_create.html'
    form_class = OrderCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'form': self.get_data
            }
        )
        return context

    def get_data(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        address = profile.address.split(' ')
        data = {
            'name': user.first_name + ' ' + user.last_name,
            'email': user.email,
            'phone': profile.phone,
            'city': address[0],
            'address': ' '.join(address[1:])
        }
        form = OrderCreateForm(data)
        return form

    def form_valid(self, form):
        cart = Cart(self.request)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        full_name = form.cleaned_data['name'].split(' ')
        delivery = form.cleaned_data['delivery']
        payment = form.cleaned_data['payment']
        user.email = form.cleaned_data['email']
        user.first_name = full_name[0]
        user.last_name = full_name[1]
        user.save()

        profile.phone = form.cleaned_data['phone']
        profile.address = f"{form.cleaned_data['city']} {form.cleaned_data['address']}"
        profile.save()

        order = Orders.objects.create(
            delivery_type=delivery,
            payment=payment,
            profile=profile,
            total_payment=sum([item['total_price'] for item in cart]),
            status=3,
        )
        order.save()

        for item in cart:
            order.products.add(item['product'])
            Basket.objects.create(
                order=order,
                products=item['product'],
                quantity=item['quantity'],
            )
            # product = Product.objects.get(slug=item['product'].slug)
            # TODO: added function for checking counter products

            quantity = Offer.objects.get(product=item['product'].id)
            quantity.amount -= int(item['quantity'])
            quantity.save()

        cart.clear()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('store:order_confirm', kwargs={'pk': self.kwargs['pk']})


class OrderConfirmView(TemplateView):
    """
    Подтверждение заказа и переход на страницу оплаты
    """
    model = Orders
    template_name = 'store/order/order_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'order': Orders.objects.select_related('profile').last(),
            }
        )
        return context

    def get_success_url(self):
        return reverse_lazy('store:order_confirm', kwargs={'pk': self.request.user.id})
