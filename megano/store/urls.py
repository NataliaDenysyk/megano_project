from django.urls import path

from store.views import (
    CatalogView, ProductListView, SettingsView, ClearCacheAll, ClearCacheCart, ClearCacheBanner, site_name,
)

app_name = 'store'
urlpatterns = [
    path('category/products/', CatalogView.as_view(), name='category_product'),
    path('', ProductListView.as_view(), name='index'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('clear-all/', ClearCacheAll.as_view(), name='clear_all_cache'),
    path('clear-banner/', ClearCacheBanner.as_view(), name='clear_banner_cache'),
    path('clear-cart/', ClearCacheCart.as_view(), name='clear_cart_cache'),
    path('site-name/', site_name, name='site_name'),
]
