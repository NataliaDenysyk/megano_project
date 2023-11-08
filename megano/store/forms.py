from django import forms

from authorization.models import Profile
from store.widgets import CustomCheckboxMultiple, CustomRadioSelect


class FilterForm(forms.Form):

    choices = (
        (True, 'Да'),
        (False, 'Нет'),
        (None, 'Не учитывать')
    )
    range = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'range-line',
            'type': 'text',
            'id': 'price',
            'name': 'price',
            'data-type': 'double',
            'data-min': '0',
            'data-max': '1000',
            'data-from': '0',
            'data-to': '27',
        }),
    )
    name = forms.CharField(
        max_length=150,
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input form-input_full',
            'id': 'title',
            'placeholder': 'Название',
            'name': 'title',
        })
    )
    stores = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.filter(role='store'),
        required=False,
        label='',
        widget=CustomCheckboxMultiple(),
    )
    availability = forms.ChoiceField(
        label='Только товары в наличии',
        widget=CustomRadioSelect(),
        choices=choices,
        required=False,
    )
    delivery_free = forms.ChoiceField(
        label='С бесплатной доставкой',
        widget=CustomRadioSelect(),
        choices=choices,
        required=False,
    )
    another_feature = forms.CharField(
        max_length=150,
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input form-input_full',
            'id': 'another_feature',
            'placeholder': 'Поиск по другим характеристикам',
            'name': 'another_feature',
        })
    )

