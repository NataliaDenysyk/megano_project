from django.urls import path

from .views import (
    SellerDetail,
    RegisterView,
    UserLoginView,
    UserLogoutView,
)

app_name = 'profile'

urlpatterns = [
    path('seller/<slug:slug>/', SellerDetail.as_view(), name='seller'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
