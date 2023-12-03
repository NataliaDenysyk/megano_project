from django.urls import path

from .views import (
    ProfileDetailView,
    ProfileUpdateView,
)


app_name = 'authorization'

urlpatterns = [
    path('personal_account/<int:pk>/', ProfileDetailView.as_view(), name='profile_details'),
    path('personal_account/<int:pk>/profile_date_form/', ProfileUpdateView.as_view(), name='profile'),
    ]