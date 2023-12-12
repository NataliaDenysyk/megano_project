from django.urls import path

from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    ProfileOrders,
    SellerDetail,
    ProfileOrderPage,
)


app_name = 'authorization'

urlpatterns = [
    path('personal_account/<slug:slug>/', ProfileDetailView.as_view(), name='profile_details'),
    path('personal_account/<slug:slug>/profile_date_form/', ProfileUpdateView.as_view(), name='profile'),
    path('personal_account/<slug:slug>/history_orders/', ProfileOrders.as_view(), name='history_orders'),
    path('seller/<slug:slug>/', SellerDetail.as_view(), name='seller'),
    path('personal_account/<slug:slug>/history_orders/detailed_order_page/<int:pk>/',
         ProfileOrderPage.as_view(), name='detailed_order'),
    ]