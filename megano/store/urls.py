from django.urls import path

from store.views import (
    product_by_category,
)

app_name = 'store'
urlpatterns = [
    path('category/products/', product_by_category, name='category_product'),
    ]
