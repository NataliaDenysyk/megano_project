from django.urls import path

from store.views import (
    CatalogView,
)

app_name = 'store'
urlpatterns = [
    path('category/products/', CatalogView.as_view(), name='category_product'),
]
