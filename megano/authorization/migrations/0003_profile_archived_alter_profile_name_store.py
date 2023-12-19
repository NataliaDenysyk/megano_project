# Generated by Django 4.2.6 on 2023-11-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_alter_profile_sale_alter_profile_viewed_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='archived',
            field=models.BooleanField(default=True, verbose_name='Архивация'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name_store',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
