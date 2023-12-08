import json

from django.contrib.contenttypes.fields import GenericRelation
from compare.models import *
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

import compare.models
from authorization.models import Profile
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from store.utils import (
    category_image_directory_path,
    jsonfield_default_description,
    product_images_directory_path
)


class Category(MPTTModel):
    """
    Модель хранения категорий товара
    """

    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT,
                            null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    image = models.ImageField(null=True, blank=True,
                              upload_to=category_image_directory_path,
                              verbose_name='Изображение')
    discount = models.ManyToManyField('Discount', related_name='categories', verbose_name='Скидка')
    slug = models.SlugField()
    activity = models.BooleanField(default=True, verbose_name='Активация')
    sort_index = models.IntegerField(verbose_name='Индекс сортировки')

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product-by-category', args=[str(self.slug)])

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ["sort_index"]
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['name']


class ProductImage(models.Model):
    """
    Модель хранит изображения товаров
    """

    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(
        verbose_name='Фотография товара',
        upload_to=product_images_directory_path,
        options={"quality": 80},
        processors=[ResizeToFill(200, 200)],
    )

    def __str__(self) -> str:
        return f"{self.pk})"

    class Meta:
        db_table = 'Images'
        ordering = ['id', ]
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Offer(models.Model):
    """
    Модель предложений продавцов, содержит цену и кол-во предлагаемого товара
    """

    unit_price = models.DecimalField('Цена', default=0, max_digits=8, decimal_places=2)
    amount = models.PositiveIntegerField('Количество')
    seller = models.ForeignKey(
        'authorization.Profile',
        on_delete=models.CASCADE,
        verbose_name='Продавец',
        related_name='offers'
    )
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='offers'
    )

    def __str__(self) -> str:
        return f"Предложение от {self.seller.name_store}"

    class Meta:
        db_table = 'Offer'
        ordering = ['id', 'unit_price']
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'


class Tag(models.Model):
    """
    Модель тегов
    """

    name = models.CharField('Название', default='', max_length=50, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = 'Tags'
        ordering = ['id', 'name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Banners(models.Model):
    """
    Модель Баннеры
    """
    title = models.CharField(u"Название баннера", max_length=150, db_index=True)
    slug = models.SlugField(u"URL", max_length=150, db_index=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    description = models.TextField(u"Описание баннера", blank=True)
    link = models.URLField(max_length=250, blank=True, verbose_name="Ссылка")
    is_active = models.BooleanField(default=False, verbose_name="Модерация")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Отредактирован")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        db_table = "banners"
        ordering = ["title", ]
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'


class Reviews(models.Model):
    """
    Модель отзывов товара
    """

    comment_text = models.TextField(' Отзыв', default='', null=False, blank=True)
    author = models.ForeignKey('authorization.Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, verbose_name='Товары')

    def __str__(self) -> str:
        return f"{self.comment_text[:25]}"

    class Meta:
        db_table = 'Reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Discount(models.Model):
    """
    Модель скидок

    """

    name = models.CharField('Название', default='', max_length=70, null=False, blank=False)
    description = models.TextField('Описание', default='', null=False, blank=True)
    sum_discount = models.FloatField('Сумма скидки', null=False, blank=False)
    total_products = models.IntegerField('Количество товаров', null=True, blank=True)
    sum_cart = models.FloatField(verbose_name='Сумма корзины', null=True, blank=True)
    priority = models.BooleanField(verbose_name='Приоритет', default=False)
    valid_from = models.DateTimeField('Действует с', null=True, blank=True)
    valid_to = models.DateTimeField('Действует до', blank=False)
    is_active = models.BooleanField('Активно', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        db_table = 'Discounts'
        ordering = ['id', 'name']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Comparison(models.Model):
    pass


class Orders(models.Model):
    """
    Модель хранения заказов
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

    class Status(models.TextChoices):
        PAID = 1, 'Оплачено'
        UNPAID = 2, 'Не оплачено'
        PROCESS = 3, 'Доставляется'

    delivery_type = models.IntegerField(choices=Delivery.choices, verbose_name="Способ доставки")
    payment = models.IntegerField(choices=Payment.choices, verbose_name='Способ оплаты')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    status = models.IntegerField(choices=Status.choices, verbose_name='Статус заказа')
    total_payment = models.IntegerField(verbose_name='Количество')
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f"Order(pk = {self.pk}"

    class Meta:
        db_table = "Orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Product(models.Model):
    """
    Модель товаров магазина

    """

    name = models.CharField('Название товара', default='', max_length=150, null=False, db_index=True)
    slug = models.SlugField(max_length=150, default='')
    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    description = models.JSONField(
        'Описание',
        default=jsonfield_default_description,
    )
    feature = GenericRelation(compare.models.AbstractCharacteristicModel, null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='products', verbose_name='Теги')
    preview = ProcessedImageField(
        verbose_name='Основное фото',
        upload_to="products/product/%y/%m/%d/",
        options={"quality": 80},
        processors=[ResizeToFill(200, 200)],
        blank=True,
        null=True
    )
    availability = models.BooleanField('Доступность', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    update_at = models.DateTimeField('Отредактирован', auto_now=True)
    discount = models.ManyToManyField('Discount', related_name='products', verbose_name='Скидка')
    is_view = models.BooleanField('Просмотрен', default=False)

    def __str__(self) -> str:
        return f"{self.name} (id:{self.pk})"

    def get_comparison_id(self):
        return f"{(self.id)}"

    class Meta:
        db_table = 'Products'
        ordering = ['id', 'name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
