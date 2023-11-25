from django import forms


class ReviewsForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, max_length=100)
