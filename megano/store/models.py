from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
# TODO models Orders, Product, Discount, Category

class Orders(models.Model):
    pass


class Product(models.Model):
    pass


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
