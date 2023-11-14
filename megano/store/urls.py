from django.urls import path

from store.views import (
    CatalogListView,
    ProductDetailView
)

app_name = 'store'

urlpatterns = [
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail')
]

