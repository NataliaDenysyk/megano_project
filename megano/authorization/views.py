from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from django.db.models import Count, Case, When
from django.views.generic import DetailView, TemplateView

from authorization.mixins import MenuMixin
from authorization.models import Profile
from store.configs import settings
from store.models import Offer

from django.core.cache import cache

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from authorization.forms import ProfileForm
from authorization.models import Profile

from django.http import HttpResponse
from django.urls import reverse_lazy

from store.models import Orders
from services.services import ProfileService, ProfileCreateService


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


# class AccountView(TemplateView, MenuMixin):
#     model = Profile
#     template_name = 'auth/account/account.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(
#             self.get_menu()
#         )
#
#         return context
#
# class ProfileView(TemplateView, MenuMixin):
#     model = Profile
#     template_name = 'auth/account/profile.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(
#             self.get_menu()
#         )
#
#         return context
#
# class HistoryOrderView(TemplateView, MenuMixin):
#     model = Profile
#     template_name = 'auth/account/historyorder.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(
#             self.get_menu()
#         )
#
#         return context

# class HistoryProductsView(TemplateView, MenuMixin):
#     model = Profile
#     template_name = 'auth/account/historyview.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(
#             self.get_menu()
#         )
#
#         return context


class ProfileDetailView(MenuMixin, DetailView):
    queryset = (
        Profile.objects
        .select_related('user')
        .select_related('viewed_orders')
    )
    template_name = 'authorization/profile_detail.html'

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция возвращает контекст
        """
        context = super().get_context_data(**kwargs)
        context.update(ProfileService(context['object']).get_context())
        context.update(
            {'menu': self.get_menu()}
        )
        context.update(ProfileService(context['object']).get_context())

        return context


class ProfileUpdateView(MenuMixin, UpdateView):
    queryset = (
        Profile.objects
        .select_related('user')
        .select_related('viewed_orders')
    )
    form_class = ProfileForm
    # template_name = 'authorization/profile_update_form.html'
    template_name_suffix = "_update_form"

    def get_success_url(self,):
        return reverse(
            'authorization:profile_details',
            kwargs={'pk': self.request.user.id},
        )

    # @login_required
    def form_valid(self, form):
        customer = Profile.objects.get(user=self.request.user)
        ProfileCreateService().get_form_valid(form, customer)
        # HttpResponseRedirect(self.get_success_url)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'menu': self.get_menu()}
        )
        print('context', context)
        return context
