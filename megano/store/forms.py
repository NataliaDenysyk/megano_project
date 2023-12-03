from django import forms

from store.models import Product


class ReviewsForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, max_length=100)


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
