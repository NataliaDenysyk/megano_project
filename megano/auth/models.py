from django.contrib.auth.models import User
from django.db import models

from megano.store.models import Product, Orders


class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    sale = models.IntegerField()
    avatar_store = models.ImageField()
    name_store = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='user')

    class Meta:
        permissions = (
            ('store'),
        )


class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    cart = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_orders = models.ForeignKey(Product, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')

    class Meta:
        permissions = (
            ('buyer'),
        )


class Bio(models.Model):
    fullname = models.CharField(max_length=50)
    phone = models.IntegerField()
    avatar = models.ImageField()
