# Generated by Django 4.2.6 on 2023-10-24 17:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, default=1, max_digits=8, verbose_name='Цена')),
                ('amount', models.PositiveIntegerField(verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
                'db_table': 'Price',
                'ordering': ['id', 'unit_price'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'Tags',
                'ordering': ['id', 'name'],
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['id', 'name'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AddField(
            model_name='product',
            name='availability',
            field=models.BooleanField(default=True, verbose_name='Доступность'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='feature',
            field=models.TextField(blank=True, default='', verbose_name='Характеристика'),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to="products/product/%y/%m/%d/", verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=150, verbose_name='Название товара'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='product',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Отредактирован'),
        ),
        migrations.AlterModelTable(
            name='product',
            table='Products',
        ),
    ]
