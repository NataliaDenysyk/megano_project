# Generated by Django 4.2.6 on 2024-01-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0002_electrocharacteristic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='abstractcharacteristicmodel',
            options={'ordering': ['id'], 'verbose_name': 'Абстрактные характеристики', 'verbose_name_plural': 'Абстрактные характеристики'},
        ),
        migrations.AlterModelOptions(
            name='electrocharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики электроники', 'verbose_name_plural': 'Характеристики электроники'},
        ),
        migrations.AlterModelOptions(
            name='headphonescharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики наушников', 'verbose_name_plural': 'Характеристики наушников'},
        ),
        migrations.AlterModelOptions(
            name='kitchencharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики кухонной техники', 'verbose_name_plural': 'Характеристики кухонной техники'},
        ),
        migrations.AlterModelOptions(
            name='microwaveovencharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики микроволновой печи', 'verbose_name_plural': 'Характеристики микроволновых печей'},
        ),
        migrations.AlterModelOptions(
            name='mobilecharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики телефона', 'verbose_name_plural': 'Характеристики телефонов'},
        ),
        migrations.AlterModelOptions(
            name='notebookcharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики ноутбука', 'verbose_name_plural': 'Характеристики ноутбуков'},
        ),
        migrations.AlterModelOptions(
            name='photocamcharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики фотоаппарата', 'verbose_name_plural': 'Характеристики фотоаппаратов'},
        ),
        migrations.AlterModelOptions(
            name='torcherecharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики торшера', 'verbose_name_plural': 'Характеристики торшеров'},
        ),
        migrations.AlterModelOptions(
            name='tvsetcharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики телевизора', 'verbose_name_plural': 'Характеристики телевизоров'},
        ),
        migrations.AlterModelOptions(
            name='washmachinecharacteristic',
            options={'ordering': ['id'], 'verbose_name': 'Характеристики стиральной машины', 'verbose_name_plural': 'Характеристики стиральных машин'},
        ),
        migrations.AddField(
            model_name='abstractcharacteristicmodel',
            name='color_en',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='abstractcharacteristicmodel',
            name='color_ru',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='abstractcharacteristicmodel',
            name='made_in_en',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Сделан в '),
        ),
        migrations.AddField(
            model_name='abstractcharacteristicmodel',
            name='made_in_ru',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Сделан в '),
        ),
        migrations.AddField(
            model_name='electrocharacteristic',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='electrocharacteristic',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='electrocharacteristic',
            name='type_product_en',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип электроники'),
        ),
        migrations.AddField(
            model_name='electrocharacteristic',
            name='type_product_ru',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип электроники'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='bluetooth_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Наличие Bluetooth'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='bluetooth_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Наличие Bluetooth'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='fit_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Как носить'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='fit_ru',
            field=models.CharField(max_length=20, null=True, verbose_name='Как носить'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='hdmi_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='HDMI'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='hdmi_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='HDMI'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='mic_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Микрофон'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='mic_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Микрофон'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='wireless_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Беспроводные'),
        ),
        migrations.AddField(
            model_name='headphonescharacteristic',
            name='wireless_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Беспроводные'),
        ),
        migrations.AddField(
            model_name='kitchencharacteristic',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='kitchencharacteristic',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='kitchencharacteristic',
            name='type_en',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип техники'),
        ),
        migrations.AddField(
            model_name='kitchencharacteristic',
            name='type_ru',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип техники'),
        ),
        migrations.AddField(
            model_name='microwaveovencharacteristic',
            name='grill_en',
            field=models.CharField(default='Информации нет', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='microwaveovencharacteristic',
            name='grill_ru',
            field=models.CharField(default='Информации нет', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='mobilecharacteristic',
            name='phone_type_en',
            field=models.CharField(max_length=20, null=True, verbose_name='Тип мобильного телефона'),
        ),
        migrations.AddField(
            model_name='mobilecharacteristic',
            name='phone_type_ru',
            field=models.CharField(max_length=20, null=True, verbose_name='Тип мобильного телефона'),
        ),
        migrations.AddField(
            model_name='notebookcharacteristic',
            name='laptop_type_en',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип ноутбука'),
        ),
        migrations.AddField(
            model_name='notebookcharacteristic',
            name='laptop_type_ru',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип ноутбука'),
        ),
        migrations.AddField(
            model_name='photocamcharacteristic',
            name='type_en',
            field=models.CharField(default='Информации нет', max_length=30, null=True, verbose_name='Тип фотоаппарата'),
        ),
        migrations.AddField(
            model_name='photocamcharacteristic',
            name='type_ru',
            field=models.CharField(default='Информации нет', max_length=30, null=True, verbose_name='Тип фотоаппарата'),
        ),
        migrations.AddField(
            model_name='torcherecharacteristic',
            name='led_type_en',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип лампочки'),
        ),
        migrations.AddField(
            model_name='torcherecharacteristic',
            name='led_type_ru',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Тип лампочки'),
        ),
        migrations.AddField(
            model_name='torcherecharacteristic',
            name='place_type_en',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Место расположения'),
        ),
        migrations.AddField(
            model_name='torcherecharacteristic',
            name='place_type_ru',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Место расположения'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='country_en',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Страна производитель'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='country_ru',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Страна производитель'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='hdmi_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='HDMI'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='hdmi_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='HDMI'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='name_en',
            field=models.TextField(blank=True, default='TVSet', null=True),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='name_ru',
            field=models.TextField(blank=True, default='TVSet', null=True),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='wi_fi_en',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Наличие Wi-Fi'),
        ),
        migrations.AddField(
            model_name='tvsetcharacteristic',
            name='wi_fi_ru',
            field=models.CharField(default='Нет', max_length=20, null=True, verbose_name='Наличие Wi-Fi'),
        ),
        migrations.AddField(
            model_name='washmachinecharacteristic',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='washmachinecharacteristic',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AddField(
            model_name='washmachinecharacteristic',
            name='type_loading_en',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип загрузки'),
        ),
        migrations.AddField(
            model_name='washmachinecharacteristic',
            name='type_loading_ru',
            field=models.CharField(default='Информации нет', max_length=20, null=True, verbose_name='Тип загрузки'),
        ),
    ]
