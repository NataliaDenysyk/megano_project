from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """
    name = forms.CharField(
        label='name',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "name",
            'name': "name",
            'type': "text",
            'data-validate': "require"
        })
    )
    e_mail = forms.EmailField(
        label='mail',
        widget=forms.EmailInput(attrs={
            'class': "form-input",
            'id': "mail",
            'name': "mail",
            'type': "email",
            'data-validate': "require",
            'placeholder': "send@test.test"
        }),
        # validators=[
        #     validators.EmailValidator(message='dfghjiklm')
        # ]
    )
    password = forms.CharField(
        label='password',
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': "form-input",
            'id': "password",
            'name': "password",
            'type': "password",
            'placeholder': "Тут можно изменить пароль"
        })
    )
    password_2 = forms.CharField(
        label='passwordReply',
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': "form-input",
            'id': "password",
            'name': "password",
            'type': "password",
            'placeholder': "Введите пароль повторно"
        })
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password_2')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    avatar = forms.ImageField(
        label='avatar',
        required=False,
        widget=forms.FileInput(attrs={
            'class': "Profile-file form-input",
            'id': "avatar",
            'name': "avatar",
            'type': "file",
            'enctype': "multipart/form-data",
            'data-validate': "onlyImgAvatar"
        })
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "phone",
            'name': "phone",
            'type': "text",
            'placeholder': '+7(999)9999999',
            "data-mask": '+7(999)9999999',

        })
    )

    class Meta:
        model = Profile
        fields = ('avatar',)




# class ProfileForm(forms.ModelForm):
#
#     avatar = forms.ImageField(
#         label='avatar',
#         required=False,
#         widget=forms.FileInput(attrs={
#             'class': "Profile-file form-input",
#             'id': "avatar",
#             'name': "avatar",
#             'type': "file",
#             'enctype': "multipart/form-data",
#             'data-validate': "onlyImgAvatar"
#         }))
#
#     name = forms.CharField(
#         label='name',
#         max_length=200,
#         widget=forms.TextInput(attrs={
#             'class': "form-input",
#             'id': "name",
#             'name': "name",
#             'type': "text",
#             'data-validate': "require"
#         })
#     )
#     phone = forms.CharField(
#         label='Телефон',
#         widget=forms.TextInput(attrs={
#             'class': "form-input",
#             'id': "phone",
#             'name': "phone",
#             'type': "text",
#             'placeholder': '+7(999)9999999',
#             "data-mask": '+7(999)9999999',
#
#         }))
#
#     e_mail = forms.EmailField(
#         label='mail',
#         widget=forms.EmailInput(attrs={
#             'class': "form-input",
#             'id': "mail",
#             'name': "mail",
#             'type': "email",
#             'data-validate': "require",
#             'placeholder': "send@test.test"
#         })
#     )
#
#     password = forms.CharField(
#         label='password',
#         min_length=8,
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             'class': "form-input",
#             'id': "password",
#             'name': "password",
#             'type': "password",
#             'placeholder': "Тут можно изменить пароль"
#         })
#     )
#     password_2 = forms.CharField(
#         label='passwordReply',
#         min_length=8,
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             'class': "form-input",
#             'id': "password",
#             'name': "password",
#             'type': "password",
#             'placeholder': "Введите пароль повторно"
#         })
#     )
#
#     class Meta:
#         model = Profile
#         fields = ['avatar', 'name']   #'phone'
#
#
