from django.urls import path

from .views import (
    SellerDetail,
)

app_name = 'profile'

urlpatterns = [
    path('seller/<slug:slug>/', SellerDetail.as_view(), name='seller'),
]
