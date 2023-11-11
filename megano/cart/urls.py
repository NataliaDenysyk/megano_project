from django.urls import path

from .views import (
    add_product_to_cart,
    CartListView,
    add_product,
    take_product,
    delete_product_from_cart,
    clear_cart
)

app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name='index'),
    path('<slug:slug>/', add_product_to_cart, name='add_product_to_cart'),
    path('add_product/<slug:slug>/', add_product, name='add_product'),
    path('take_product/<slug:slug>/', take_product, name='take_product'),
    path('delete_product/<slug:slug>/', delete_product_from_cart, name='delete_product'),
    path('cart/clear/', clear_cart, name='cart_clear'),
]
