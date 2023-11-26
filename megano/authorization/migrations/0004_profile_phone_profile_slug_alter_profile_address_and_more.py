# Generated by Django 4.2.6 on 2023-11-26 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_orders_options_remove_product_is_view'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authorization', '0003_remove_profile_sale_alter_profile_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, null=True, unique=True, verbose_name='Teleфон'),
        ),
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default='', max_length=150, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name_store',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя магазина'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('store', 'Store'), ('buyer', 'Buyer')], default='buyer', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='viewed_orders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Связанные заказы'),
        ),
    ]
