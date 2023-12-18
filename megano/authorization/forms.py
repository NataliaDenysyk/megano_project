from django import forms
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
    mail = forms.EmailField(
        label='mail',
        widget=forms.EmailInput(attrs={
            'class': "form-input",
            'id': "mail",
            'name': "mail",
            'type': "email",
            'data-validate': "require",
            'placeholder': "send@test.test"
        }),
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
    passwordReply = forms.CharField(
        label='passwordReply',
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': "form-input",
            'id': "passwordReply",
            'name': "passwordReply",
            'type': "password",
            'placeholder': "Введите пароль повторно"
        })
    )

    def clean_mail(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('mail')
        if User.objects.filter(email__iexact=email).exists():
            self.add_error('mail', 'Email адрес должен быть уникальным')
        return email

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'passwordReply')


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

    def clean_avatar(self):
        """"
       Функция, ограничивающая размер загружаемой avatar
       """
        image = self.cleaned_data.get('avatar', False)
        if image:
            if image.size > 2.5 * 1024 * 1024:
                self.add_error('avatar', 'Размер изображения слишком большой ( > 2.5mb )')
            return image
        else:
            self.add_error('avatar', 'Не удалось прочитать загруженное изображение')

    class Meta:
        model = Profile
        fields = ('avatar', 'phone')


class RegisterForm(forms.ModelForm):
    """
    Форма регистрации
    """

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
            'id': 'email',
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
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'user-input',
            'id': 'password2',
            'name': 'pass',
            'placeholder': 'Повтор Пароля',
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.get(username=username):
            raise forms.ValidationError("Такой логин уже существует")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Данный email уже существует.")

    def clean_password2(self):
        passw1 = self.cleaned_data['password']
        passw2 = self.cleaned_data['password2']
        if passw1 != passw2:
            raise forms.ValidationError("Пароли не совпадают")
        if len(passw1) < 6:
            raise forms.ValidationError("Пароль должен содержать не менее 6 символов")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    """
    Форма авторизации
    """

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
