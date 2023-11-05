from django.urls import path

from .views import catalog

app_name = 'store'

urlpatterns = [
    path('catalog/', catalog, name='catalog'),
]
