from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
# TODO models Orders, Product, Discount, Category


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
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100,verbose_name="Название категории")
    image = models.ImageField(upload_to=category_image_directory_path, verbose_name="Изображение")
    parent = models.ForeignKey("self", on_delete=models.CASCADE)
    activity = models.BooleanField(default=True, verbose_name="Активация")
    sort_index = models.IntegerField(max_length=11, verbose_name="Индекс сортировки")

    def __str__(self) -> str:
        return f"{self.name}"


class Orders(models.Model):
    pass


class Product(models.Model):
    pass


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
