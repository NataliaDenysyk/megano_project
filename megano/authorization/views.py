from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView

from authorization.forms import ProfileForm
from authorization.models import Profile

from django.http import HttpResponse
from django.urls import reverse_lazy

from store.models import Orders
from services.services import ProfileService


class ProfileDetailView(DetailView):
    queryset = (
        Profile.objects
        .select_related('user')
        .select_related('viewed_orders')
    )

    def get_context_data(self, **kwargs) -> HttpResponse:
        """
        Функция возвращает контекст
        """
        context = super().get_context_data(**kwargs)
        context.update(ProfileService(context['object']).get_context())
        # context.update(ProfileService(context['object']).get_context())

        return context


class ProfileCreateView(CreateView):
    queryset = (
        Profile.objects
        .select_related('user')
        .select_related('viewed_orders')
    )
    # fields = 'user', 'phone', 'e_mail', 'avatar'#, 'password'
    form_class = ProfileForm
    template_name = 'authorization/profile_form.html'
    success_url = reverse_lazy('authorization:profile_details')

    def form_valid(self, form):
        print('form', form)

        response = super().form_valid(form)

        # avatar = form.cleaned_data['avatar']
        # name = form.cleaned_data['name']
        # phone = form.cleaned_data['phone']
        # e_mail = form.cleaned_data['e_mail']
        # password = form.cleaned_data['password']
        # password_2 = form.cleaned_data['password_2']

    def form_invalid(self, form):
        print('qwerty')

        # valid = ProfileService.name_profile(form.cleaned_data['name'])
        # return response
        # # for elem in form.files:
        # #     ProductImage.objects.create(
        # #         product=self.object,
        # #         image=image,
        # #     )
        #
        #
        # if form.is_valid():
        #     # name = form.cleaned_data['name']
        #     # price = form.cleaned_data['price']
        #     # Product.objects.create(**form.cleaned_data)
        #     form.save()
        #     url = reverse('shopapp:orders_list')
        #     return redirect(url)
        # # else:
        # #     form = OrderForm()
        # # context = {
        # #     'form': form,
        # # }
        # return render(request, 'shopapp/create-order.html', context=context)