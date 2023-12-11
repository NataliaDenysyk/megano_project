from django.urls import path

from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    ProfileOrders,
    SellerDetail
)


app_name = 'authorization'

urlpatterns = [
    path('personal_account/<int:pk>/', ProfileDetailView.as_view(), name='profile_details'),
    path('personal_account/<int:pk>/profile_date_form/', ProfileUpdateView.as_view(), name='profile'),
    path('personal_account/<int:pk>/history_orders/', ProfileOrders.as_view(), name='history_orders'),
    path('seller/<slug:slug>/', SellerDetail.as_view(), name='seller'),
    ]