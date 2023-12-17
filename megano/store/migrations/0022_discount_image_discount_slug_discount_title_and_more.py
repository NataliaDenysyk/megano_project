# Generated by Django 4.2.6 on 2023-12-17 08:17

from django.db import migrations, models
import imagekit.models.fields
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_product_limited_edition_bannerscategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=store.models.discount_images_directory_path, verbose_name='Изображение скидки'),
        ),
        migrations.AddField(
            model_name='discount',
            name='slug',
            field=models.SlugField(default=10987894657345, max_length=150, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discount',
            name='title',
            field=models.CharField(default='', max_length=70, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='name',
            field=models.CharField(choices=[('DP', 'Скидки на товар'), ('DS', 'Скидки на наборы'), ('DC', 'Скидки на корзину')], default='DP', max_length=2, verbose_name='Тип скидки'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='valid_to',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Действует до'),
        ),
    ]
