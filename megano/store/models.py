from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
# TODO models Orders, Product, Discount, Category
# TODO раскомментировать или исправить связи в моделях


def category_image_directory_path(instance: "Category", filename: str) -> str:
    """
    Функция coздания пути к картинке категории
    """
    return "category/category_{pk}/image/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Category(models.Model):
    """
    Модель хранения категорий товара
    """
    class Meta:

        ordering = ["sort_index"]
        db_table = 'Category'
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=100,verbose_name="Название категории")
    image = models.ImageField(upload_to=category_image_directory_path, verbose_name="Изображение")
    parent = models.ForeignKey("self", on_delete=models.CASCADE)
    activity = models.BooleanField(default=True, verbose_name="Активация")
    sort_index = models.IntegerField(verbose_name="Индекс сортировки")

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    """
    Модель товаров магазина

    """

    name = models.CharField('Название товара', default='', max_length=150, null=False, db_index=True)
    slug = models.SlugField(max_length=150, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField('Описание', default='', null=False, blank=True)
    feature = models.TextField('Характеристика', default='', null=False, blank=True)
    tags = models.ManyToManyField('Tag', related_name='products', verbose_name='Теги')
    images = models.ImageField(
        'Изображение', upload_to="products/product/%y/%m/%d/", blank=True, null=True
    )
    availability = models.BooleanField('Доступность', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    update_at = models.DateTimeField('Отредактирован', auto_now=True)
    discount = models.ManyToManyField('Discount', related_name='products', verbose_name='Скидка')

    def __str__(self) -> str:
        return f"{self.name} (id:{self.pk})"

    class Meta:
        db_table = 'Products'
        ordering = ['id', 'name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Offer(models.Model):
    """
    Модель предложений продавцов, содержит цену и кол-во предлагаемого товара

    """

    unit_price = models.DecimalField('Цена', default=0, max_digits=8, decimal_places=2)
    amount = models.PositiveIntegerField('Количество')
    seller = models.ForeignKey('authorization.Profile', on_delete=models.CASCADE, verbose_name='Продавец')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        db_table = 'Offer'
        ordering = ['id', 'unit_price']
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self) -> str:
        return f"Предложение от {self.seller.name_store}"


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

    def __str__(self) -> str:
        return f"{self.name}"


class Banners(models.Model):
    """
    The model displays banners for products.
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


class Discount(models.Model):
    """
    Модель скидок

    """

    name = models.CharField('Название', default='', max_length=70, null=False, blank=False)
    description = models.TextField('Описание', default='', null=False, blank=True)
    sum_discount = models.FloatField('Сумма скидки', null=False, blank=False)
    total_products = models.IntegerField('Количество товаров', null=True, blank=True)
    valid_from = models.DateTimeField('Действует с', null=True, blank=True)
    valid_to = models.DateTimeField('Действует до', blank=False)
    is_active = models.BooleanField('Активно', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        db_table = 'Discounts'
        ordering = ['id', 'name']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self) -> str:
        return f'{self.name}'


class Comparison(models.Model):
    pass


class Orders(models.Model):
    """
    Модель хранения заказов
    """

    class Meta:
        db_table = "Orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    delivery_type = models.CharField(
        max_length=100,
        blank=False,
        default='pickup',
        verbose_name="Тип доставки")
    address = models.CharField(max_length=150, null=True, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f"Order(pk = {self.pk}"

