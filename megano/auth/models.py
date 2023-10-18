from django.contrib.auth.models import User
from django.db import models

from megano.store.models import Product, Orders


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    sale = models.IntegerField()
    avatar = models.ImageField()
    name_store = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    viewed_orders = models.ForeignKey(Product, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')

    class Meta:
        permissions = (
            ('store', 'user', 'buyer', 'admin'),
        )





