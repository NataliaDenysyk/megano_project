from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Profile(models.Model):
    """
    Модель профиля всех пользователей
    """

    class Role(models.TextChoices):
        """
        Модель ролей пользователей
        """

        ADMIN = 'admin'
        STORE = 'store'
        BUYER = 'buyer'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    avatar = ProcessedImageField(
        blank=True,
        verbose_name='Фотография товара',
        upload_to='profiles/profile/%y/%m/%d/',
        options={"quality": 80},
        processors=[ResizeToFill(157, 100)],
    )
    name_store = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100)
    viewed_orders = models.ForeignKey('store.Product', blank=True, null=True, on_delete=models.CASCADE)
    role = models.CharField(default=Role.BUYER, choices=Role.choices)

    def __str__(self) -> str:
        return f'{self.user}'

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


class StoreSettings(models.Model):
    """
    Модель настроек магазина
    """

    class Delivery(models.IntegerChoices):
        """
        Модель вариантов доставки
        """

        FREE = 1, 'Обычная доставка'
        EXPRESS = 2, 'Экспресс-доставка'

        __empty__ = 'Выберите доставку'

    class Payment(models.IntegerChoices):
        """
        Модель вариантов оплаты
        """

        OWN_CARD = 1, 'Онлайн картой'
        ANOTHER_CARD = 2, 'Онлайн со случайного счета'

        __empty__ = 'Выберите оплату'

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='store_settings')
    delivery_type = models.IntegerField('Способ доставки', choices=Delivery.choices)
    payment = models.IntegerField('Способ оплаты', choices=Payment.choices)

    def __str__(self) -> str:
        return f"{self.profile.name_store}"

    class Meta:
        db_table = 'StoreSettings'
        ordering = ['id', 'profile']
        verbose_name = 'Настройки магазина'
        verbose_name_plural = 'Настройки магазина'
