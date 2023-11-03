# Generated by Django 4.2.6 on 2023-10-31 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['sort_index'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.CharField(max_length=150, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='delivery_type',
            field=models.CharField(default='pickup', max_length=100, verbose_name='Тип доставки'),
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='store.product'),
        ),
        migrations.AlterModelTable(
            name='product',
            table='Category',
        ),
        migrations.AlterModelTable(
            name='orders',
            table='Orders',
        ),
    ]
