from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from store.models import Product


class Cart(models.Model):
    """
    Description of the basket model.

    User    - :model:`User`\n
    Product - :model:`store.Product`
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукты')
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self) -> str:
        """
        Return a string representation of the model.

        :rtype: str
        """
        return f'{self.user.username}: {self.products.name}'

    def get_absolute_url(self) -> str:
        """
        Return the URL to access the detail view of the object.

        :rtype: str
        """
        return reverse('detail', kwargs={'id': self.id})

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
