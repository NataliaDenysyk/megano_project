# Generated by Django 4.2.6 on 2023-11-10 11:28

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_banners_images_banners_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='images',
            new_name='preview',
        ),
        migrations.AddField(
            model_name='product',
            name='is_view',
            field=models.BooleanField(default=False, verbose_name='Просмотрен'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=store.models.product_images_directory_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
                'db_table': 'Images',
                'ordering': ['id'],
            },
        ),
    ]
