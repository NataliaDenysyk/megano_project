from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'user-input',
            'id': 'name',
            'name': 'name',
            'placeholder': 'Имя',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'user-input',
            'id': 'login',
            'name': 'email',
            'placeholder': 'E-mail',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'user-input',
            'id': 'password',
            'name': 'pass',
            'placeholder': 'Пароль',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'user-input',
            'id': 'login',
            'name': 'email',
            'placeholder': 'E-mail',
        })
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'user-input',
            'id': 'password',
            'name': 'pass',
            'placeholder': '*********',
        })
    )
