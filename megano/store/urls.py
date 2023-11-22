from django.urls import path

from .views import (
    CatalogListView,
    ProductListView,
    ProductDetailView,
    SettingsView,
    ClearCacheAll,
    ClearCacheBanner,
    ClearCacheCart,
    ClearCacheProductDetail,
    ClearCacheSeller,
    SiteName,
    CacheSetupBannerView,
    CacheSetupCartView,
    CacheSetupProdDetailView,
    CacheSetupSellerView,
)

app_name = 'store'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    path('settings/', SettingsView.as_view(), name='settings'),
    path('clear-all/', ClearCacheAll.as_view(), name='clear_all_cache'),
    path('clear-banner/', ClearCacheBanner.as_view(), name='clear_banner_cache'),
    path('clear-cart/', ClearCacheCart.as_view(), name='clear_cart_cache'),
    path('clear-seller/', ClearCacheSeller.as_view(), name='clear_seller'),
    path('clear-product-detail/', ClearCacheProductDetail.as_view(), name='clear_product_detail'),
    path('site-name/', SiteName.as_view(), name='site_name'),
    path('cache-time-banner/', CacheSetupBannerView.as_view(), name='cache_time_banner'),
    path('cache-time-cart/', CacheSetupCartView.as_view(), name='cache_time_cart'),
    path('cache-time-prod-detail/', CacheSetupProdDetailView.as_view(), name='cache_time_prod_detail'),
    path('cache-time-seller/', CacheSetupSellerView.as_view(), name='cache_time_seller'),
]
