from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.exceptions import ObjectDoesNotExist
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class BaseModel(models.Model):
    """"
    Базовый класс модели
    """
    def delete(self, *arg, **kwargs):
        """"
        Функция, меняющая поведение delete на мягкое удаление
        """
        self.archived = True
        self.save()
        return self

    class Meta:
        abstract = True


def profile_images_directory_path(instance: 'Profile', filename: str) -> str:
    """
    Функция генерирует путь сохранения изображений с привязкой к id товара

    :param instance: объект ProductImage
    :param filename: имя файла
    :return: str - путь для сохранения
    """

    return f'profiles/profile_{instance.id}/{filename}'


class Profile(BaseModel):
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

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    slug = models.SlugField('Слаг', max_length=150, default='')
    phone = models.CharField('Teleфон', null=True, blank=True, unique=True)
    description = models.CharField('Описание', max_length=100)
    avatar = ProcessedImageField(
        blank=True,
        verbose_name='Фотография профиля',
        upload_to=profile_images_directory_path,
        options={"quality": 80},
        processors=[ResizeToFit(157, 100)],
        null=True
    )
    archived = models.BooleanField(default=False, verbose_name='Архивация')
    name_store = models.CharField('Имя магазина', max_length=50, blank=True, null=True)
    address = models.CharField('Адрес', max_length=100)
    viewed_orders = models.ForeignKey(
        'store.Product',
        verbose_name='Связанные заказы',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    role = models.CharField('Роль', default=Role.BUYER, choices=Role.choices)

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
