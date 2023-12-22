from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from authorization.models import Profile
from .models import Orders, Product


class ReviewsForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, max_length=100)


class OrderCreateForm(forms.ModelForm):
    """
    Класс формы для оформления Заказа.
    """
    name = forms.CharField(
        max_length=100,
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "name",
            'name': "name",
            'type': "text",
            'placeholder': "Иванов Иван Иванович",
        }),
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "phone",
            'name': "phone",
            'type': "text",
            'placeholder': "+79991230000",
        }),
    )
    delivery = forms.ChoiceField(
        choices=Orders.Delivery.choices[1:],
        widget=forms.RadioSelect(attrs={
            'class': "toggle-box",
            'id': "delivery",
            'name': "delivery",
            'type': "radio",
            'checked': "checked"
        }),
    )
    payment = forms.ChoiceField(
        choices=Orders.Payment.choices[1:],
        widget=forms.RadioSelect(attrs={
            'class': "toggle-box",
            'id': "payment",
            'name': "payment",
            'type': "radio",
        }),
    )
    city = forms.CharField(max_length=100, label='Город', help_text='Город проживания')
    address = forms.CharField(max_length=200, label='Адрес', help_text='Адрес доставки')
    email = forms.EmailField(max_length=80, label='Почта', help_text='Почта')

    class Meta:
        model = Profile
        fields = [
            'name', 'phone', 'city', 'address',
            'delivery', 'payment',
        ]


class RegisterForm(UserCreationForm):
    """
    Класс формы для регистрации пользователя
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "phone",
            'name': "phone",
            'type': "text",
            'placeholder': "+79991230000",
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password1', 'password2')


class SearchForm(forms.ModelForm):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'id': 'query',
            'name': 'query',
            'placeholder': 'NVIDIA GeForce RTX 3060',
        })
    )

    class Meta:
        model = Product
        fields = ['name',]


class PaymentForm(forms.Form):
    bill = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input Payment-bill',
            'id': 'numero1',
            'name': 'numero1',
            'type': 'text',
            'placeholder': '9999 9999',
            'data-mask': "9999 9999",
            'data-validate': "require pay",
        })
    )
