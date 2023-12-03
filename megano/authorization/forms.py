from django import forms
from django.core import validators

from authorization.models import Profile


class ProfileForm(forms.ModelForm):

    avatar = forms.ImageField(
        label='avatar',
        required=False,
        widget=forms.FileInput(attrs={
            'class': "Profile-file form-input",
            'id': "avatar",
            'name': "avatar",
            'type': "file",
            'data-validate': "onlyImgAvatar"
        }))

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
    # phone = forms.CharField(
    #     label='Телефон',
    #     # max_length=12,
    #     # min_length=12,
    #     widget=forms.TextInput(attrs={
    #         'class': "form-input",
    #         'id': "phone",
    #         'name': "phone",
    #         'type': "text",
    #         'placeholder': "+70000000001"
    #     })
    # )
    # telephone = forms.IntegerField(label='Телефон', max_value=12, min_value=12,
    #                             widget=forms.NumberInput(attrs={'data-mask':'+7__________'}),
    #                             validators=[validators.MinValueValidator(
    #                                 limit_value=12,
    #                                 message='Пожалуйста, проверьте правильность номера и '
    #                                         ' введите номер телефона в соответствии с примером'),
    #                                 validators.MaxValueValidator(
    #                                 limit_value=14,
    #                                 message='Пожалуйста, проверьте правильность номера и'
    #                                         ' введите номер телефона в соответствии с примером')])
    e_mail = forms.EmailField(label='mail',
                              widget=forms.EmailInput(attrs={
                                  'placeholder': 'send@test.test'}),
                              validators=[validators.EmailValidator(
                                  message='Недопустимый адрес электронной почты')])
    password = forms.CharField(
        label='password',
        min_length=8,
        max_length=50,
        widget=forms.TextInput(attrs={
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
        widget=forms.TextInput(attrs={
            'class': "form-input",
            'id': "password",
            'name': "password",
            'type': "password",
            'placeholder': "Введите пароль повторно"
        })
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'name', 'phone']
