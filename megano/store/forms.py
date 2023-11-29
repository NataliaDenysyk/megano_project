from django import forms

from .models import Orders


class ReviewsForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, max_length=100)


class OrderCreateForm(forms.Form):
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
    city = forms.CharField(max_length=100, label='Город', help_text='Город проживания')
    address = forms.CharField(max_length=200, label='Адрес', help_text='Адрес доставки')

    class Meta:
        model = Orders
        fields = ['name', 'phone', 'city', 'address']


class ReviewsForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, max_length=100)
