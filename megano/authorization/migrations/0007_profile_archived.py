# Generated by Django 4.2.6 on 2023-12-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0006_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Архивация'),
        ),
    ]
