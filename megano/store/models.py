from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
# TODO models Orders, Product, Discount, Category
# TODO раскомментировать или исправить связи в моделях

class Orders(models.Model):
    pass


def product_media_path(instance: 'Product', filename: str) -> str:
    """
    Функция генерирует путь для сохранения изображений товаров.

    :param instance: Product instance
    :param filename: filename
    :return: string
    """
    return 'products/product_{slug}/{filename}'.format(
        pk=instance.slug,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель товаров магазина

    """

    name = models.CharField('Название товара', default='', max_length=150, null=False, db_index=True)
    slug = models.SlugField(max_length=150, default='')
    # category = models.ForeignKey('store.Category', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField('Описание', default='', null=False, blank=True)
    feature = models.TextField('Характеристика', default='', null=False, blank=True)
    # tags = models.ManyToManyField('store.Tag', related_name='products', verbose_name='Теги')
    images = models.ImageField('Изображение', null=True, upload_to=product_media_path)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    update_at = models.DateTimeField('Отредактирован', auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = 'Products'
        ordering = ['id', 'name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Offer(models.Model):
    """
    Модель предложений продавцов, содержит цену и кол-во предлагаемого товара

    """

    unit_price = models.DecimalField('Цена', default=1, max_digits=8, decimal_places=2)
    amount = models.PositiveIntegerField('Количество')
    # seller = models.ForeignKey('auth.Profile', on_delete=models.CASCADE)
    # product = models.ForeignKey('store.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Price'
        ordering = ['id', 'unit_price']
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Tag(models.Model):
    """
    Модель тегов

    """

    name = models.CharField('Название', default='', max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'Tags'
        ordering = ['id', 'name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Banners(models.Model):
    """

    """
    title = models.CharField(u"Название баннера", max_length=150, db_index=True)
    slug = models.SlugField(u"URL", max_length=150, db_index=True)
    description = models.TextField(u"Описание баннера", blank=True)
    images = models.ImageField(upload_to="img_banner/%y/%m/%d/", verbose_name="Изображение")
    link = models.URLField(max_length=250, blank=True, verbose_name="Ссылка")
    is_active = models.BooleanField(default=False, verbose_name="Модерация")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Отредактирован")

    def __str__(self) -> str:
        return f"{self.title}"

    def get_html_images(self, object):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 60х 60.
        """
        if self.images:
            return mark_safe(f"<img src'{object.images.url}' width=60")
        else:
            return 'not url'

    get_html_images.short_description = "Изображение"
    get_html_images.allow_tags = True

    class Meta:
        db_table = "banners"
        ordering = ["title", ]
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'


