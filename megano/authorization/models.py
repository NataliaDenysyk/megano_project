from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """"
    Базовый класс модели
    """
    def delete(self, *arg, **kwargs):
        """"
        Функция, меняющая поведение delete на мягкое удаление
        """
        self.archived = False
        self.save()
        return self

    class Meta:
        abstract = True

# TODO добавить связь с заказами


class Profile(BaseModel):
    """
    Модель профиля всех пользователей

    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    sale = models.IntegerField(blank=True, null=True)
    avatar = models.ImageField()
    name_store = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100)
    archived = models.BooleanField(default=True, verbose_name='Архивация')
    viewed_orders = models.ForeignKey('store.Product', blank=True, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        db_table = 'Profiles'
        ordering = ['id', 'user']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        permissions = (
            ('store', 'has offers for sale'),
            ('user', 'all site users'),
            ('buyer', 'only buys goods'),
            ('admin', 'manages the site'),
        )

    def __str__(self) -> str:
        return f"{self.user}"

