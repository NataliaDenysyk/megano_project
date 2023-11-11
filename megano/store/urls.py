from django.urls import path

from store.views import (
    CategoryView,
    # sorted_products_popular

)

app_name = 'store'
urlpatterns = [
    path('category/products/', CategoryView.as_view(), name='category_product'),
    # path('category/products/', sorted_products_popular, name='sorted_product'),


    ]

