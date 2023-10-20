# Generated by Django 4.2.6 on 2023-10-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название баннера')),
                ('slug', models.SlugField(max_length=150, verbose_name='URL')),
                ('description', models.TextField(blank=True, verbose_name='Описание баннера')),
                ('images', models.ImageField(upload_to='img_banner/%y/%m/%d/', verbose_name='Изображение')),
                ('link', models.URLField(blank=True, max_length=250, verbose_name='Ссылка')),
                ('is_active', models.BooleanField(default=False, verbose_name='Модерация')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Отредактирован')),
            ],
            options={
                'verbose_name': 'баннер',
                'verbose_name_plural': 'баннеры',
                'db_table': 'banners',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
