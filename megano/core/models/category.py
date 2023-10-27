from django.db import models


def category_image_directory_path(instance: "Category", filename: str) -> str:
    return "category/category_{pk}/image/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Category(models.Model):
    """Модель хранения категорий товара"""
    class Meta:

        ordering = ["sort_index"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100,verbose_name="Название категории")
    image = models.ImageField(upload_to=category_image_directory_path, verbose_name="Изображение")
    parent = models.ForeignKey("self", on_delete=models.CASCADE)
    activity = models.BooleanField(default=True, verbose_name="Активация")
    sort_index = models.IntegerField(max_length=11, verbose_name="Индекс сортировки")


