from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse

from django.views.generic import ListView, DetailView, UpdateView

from django.core.cache import cache

from django.db.models import Count, Case, When

from .mixins import MenuMixin

from store.configs import settings
from store.models import Offer, Orders

from services.services import ProfileService, ProfileUpdate

from .forms import UserUpdateForm, ProfileUpdateForm

from .models import Profile



class SellerDetail(DetailView):
    model = Profile
    template_name = 'auth/about-seller.html'
    context_object_name = 'seller'

    def get_object(self, *args, **kwargs) -> Profile.objects:
        slug = self.kwargs.get('slug')
        instance = Profile.objects.get(slug=slug)
        profile = cache.get_or_set(f'profile-{slug}', instance, settings.get_cache_seller())

        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['top_offers'] = Offer.objects.filter(
            seller=context.get('object')
        ).annotate(
            count=Count(Case(
                When(product__orders__status=True, then=1),
            ))
        ).order_by('-count')[:10]

        return context


class ProfileOrders(ListView, MenuMixin):
    """
    Представление для просмотра заказов профиля
    """
    model = Profile
    template_name = 'authorization/history_orders.html'

    def get_context_data(self, **kwargs):
        """
        Функция возвращает контекст
        """
        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.filter(profile=self.request.user.id).order_by('created_at')[:20]
        context.update(
            self.get_menu(id='3'),
        )
        return context


class ProfileDetailView(MenuMixin, DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    template_name = 'authorization/profile_detail.html'

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция возвращает контекст
        """
        profile = Profile.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context.update(ProfileService(profile).get_context())
        context.update(
            self.get_menu(id='1')
        )
        context['title'] = f'Страница пользователя: {self.request.user.username}'
        return context


class ProfileUpdateView(MenuMixin, UpdateView):
    """
   Представление для редактирования профиля
   """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'authorization/profile_update_form.html'

    def get_success_url(self):
        return reverse(
            'authorization:profile',
            kwargs={'pk': self.request.user.id},
        )

    def form_valid(self, form):
        """"
        Функция обрабатывает валидную форму
        """
        context = self.get_context_data()
        profile = Profile.objects.get(user=self.request.user)
        response = ProfileUpdate(profile).update_profile(
            request=self.request, form=form, context=context)
        if response is not None:
            return response

        messages.success(self.request, 'Профиль успешно сохранен ')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        """"
        Функция обрабатывает невалидную форму
        """
        context = self.get_context_data()
        context.update(
            {'error': "Некорректный ввод данных. Попробуйте еще раз."}
        )

        return render(self.request, 'authorization/profile_update_form.html', context=context)

    def get_context_data(self, **kwargs):
        """
        Функция возвращает контекст
        """
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context.update(
            self.get_menu(id='2'),
        )
        context['title'] = f'Редактирование страницы пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)

        return context


