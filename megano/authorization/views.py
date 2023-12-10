from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Case, When
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, FormView

from django.core.exceptions import ValidationError

from authorization.forms import RegisterForm, LoginForm
from authorization.models import Profile
from services.services import AuthorizationService
from store.configs import settings
from store.models import Offer

from django.core.cache import cache


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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('store:index')

    def form_valid(self, form):
        result = AuthorizationService().register_new_user(self.request, form)

        if result is True:
            return super().form_valid(form)

        context = {
            'error': result,
            'form': form,
        }
        return render(self.request, 'registration/register.html', context=context)

    def form_invalid(self, form):
        context = {
            'form': form,
        }

        if form.errors.get('username'):
            context.update({
                'error': 'Этот username уже используется, выберите другой',
            })
        else:
            context.update({
                'error': form.errors,
            })

        return render(self.request, 'registration/register.html', context=context)


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('store:index')

    def form_valid(self, form):
        result = AuthorizationService().get_login(self.request, form)

        if result is True:
            return super().form_valid(form)

        else:
            context = {
                'form': LoginForm(),
                'error': result,
            }
            return render(self.request, 'registration/login.html', context=context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('store:index')
