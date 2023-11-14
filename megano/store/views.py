from urllib import request

from typing import Any
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import SiteNameForm
from .mixins import ChangeListMixin
from .models import Product
from .configs import settings


from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from services.services import CatalogServices


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

        return self.render_to_response(context)



from typing import Any
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import SiteNameForm
from .mixins import ChangeListMixin
from .models import Product
from .configs import settings


class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/product_list.html'


# Представления для страницы настроек в админ панели

class SettingsView(ChangeListMixin, generic.ListView):
    """
    Класс SettingsView отображает страницу с настройками
    """
    model = Product
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        change_list = self.get_change_list_admin(title="Settings")
        return dict(list(context.items()) + list(change_list.items()))


class ClearCacheAll(ChangeListMixin, generic.TemplateView):
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


class ClearCacheBanner(ChangeListMixin, generic.TemplateView):
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


class ClearCacheCart(ChangeListMixin, generic.TemplateView):
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


class SiteName(ChangeListMixin, generic.TemplateView):
    """
    Класс SiteName позволяет задать новое название интернет магазина
    """
    template_name = 'admin/settings.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        messages.success(self.request, 'Название магазина успешно изменено')
        change_list = self.get_change_list_admin(
            title="site name",
            form=SiteNameForm()
        )
        return dict(list(context.items()) + list(change_list.items()))

    # TODO: написать проверку формы для Названия магазина, на сайте в настройках админки.
    #  ==> Стилизовать страницу настроек

    def dispatch(self, request, *args, **kwargs):
        if cache:
            super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("store:settings"))


# TODO: функция заглушка для объявления названия магазина (времянка)
def site_name(request):
    if request.method == 'POST':
        form = SiteNameForm(request.POST)
        if form.is_valid():
            settings.set_site_name(form.cleaned_data['title_site'])
        else:
            form = SiteNameForm()
    return render(
        request, 'admin/settings.html', {'form': form}
    )
