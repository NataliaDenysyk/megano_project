from django.urls import path

from store.views import (
    CatalogListView,
)

app_name = 'store'

urlpatterns = [
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    ]

