# Generated by Django 4.2.6 on 2023-11-05 19:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_alter_profile_sale_alter_profile_viewed_orders'),
        ('store', '0011_reviews_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['sort_index'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.TextField(max_length=150, null=True, verbose_name='Адрес'),
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
        migrations.AddField(
            model_name='orders',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authorization.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Оплачен'),
        ),
        migrations.AddField(
            model_name='orders',
            name='total',
            field=models.IntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=store.models.category_image_directory_path, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='store.category', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='reviews',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.reviews', verbose_name='Отзывы'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'slug')},
        ),
        migrations.AlterModelTable(
            name='category',
            table='Category',
        ),
        migrations.AlterModelTable(
            name='orders',
            table='Orders',
        ),
    ]
