from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AbstractCharacteristicModel(models.Model):
    """
    Общая модель характеристик
    """

    made_in = models.CharField(max_length=30, verbose_name='Сделан в ', null=True, blank=True)
    production_year = models.IntegerField(verbose_name='В каком году произведен', null=True, blank=True)
    color = models.CharField(max_length=15, verbose_name='Цвет', null=True, blank=True)
    weight = models.CharField(verbose_name='Вес', null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class TVSetCharacteristic(AbstractCharacteristicModel):
    """
    Характеристики Телевизора
    """

    name = models.TextField(default='TVSet', null=True, blank=True)
    screen = models.CharField(null=True, blank=True, max_length=10, verbose_name='Размер экрана')
    resolution = models.CharField(null=True, blank=True, max_length=10, verbose_name='Разрешение экрана')
    country = models.CharField(null=True, blank=True, max_length=25, verbose_name='Страна производитель')
    freq = models.IntegerField(null=True, blank=True, verbose_name='Частота обновления')
    wi_fi = models.CharField(max_length=20, verbose_name='Наличие Wi-Fi', default='Нет')
    hdmi = models.CharField(max_length=20, verbose_name='HDMI', default='Нет')
    description = models.TextField(verbose_name='Дополнительное описание')


class HeadphonesCharacteristic(AbstractCharacteristicModel):
    """
    Характеристики Наушников
    """

    wireless = models.CharField(max_length=20, verbose_name='Беспроводные', default='Нет')
    mic = models.CharField(max_length=20, verbose_name='Микрофон', default='Нет')
    fit = models.CharField(max_length=20, verbose_name='Как носить')
    bluetooth = models.CharField(max_length=20, verbose_name='Наличие Bluetooth', default='Нет')
    resistance = models.IntegerField(verbose_name='Сопротивление (Ом)', null=True, blank=True)
    hdmi = models.CharField(max_length=20, verbose_name='HDMI', default='Нет')
    description = models.TextField(null=True, blank=True, verbose_name='Дополнительное описание')


class WashMachineCharacteristic(AbstractCharacteristicModel):
    """
    Характеристики Стиральной машины
    """

    height = models.IntegerField(null=True, blank=True, verbose_name='Высота')
    width = models.IntegerField(null=True, blank=True, verbose_name='Ширина')
    depth = models.IntegerField(null=True, blank=True, verbose_name='Глубина')
    type_loading = models.CharField(max_length=20, verbose_name='Тип загрузки', default='Информации нет')
    capacity = models.IntegerField(null=True, blank=True, verbose_name='Объём загрузки')
    description = models.TextField(null=True, blank=True, verbose_name='Дополнительное описание')


class MobileCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик мобильного телефона
    """

    phone_type = models.CharField(max_length=20, verbose_name='Тип мобильного телефона')
    screen_size = models.IntegerField(null=True, blank=True, verbose_name='Размер экрана в дюймах')
    screen_resolution = models.CharField(null=True, blank=True, verbose_name='Разрешение экрана')
    screen_technology = models.CharField(max_length=10, verbose_name='Технология экрана', null=True, blank=True)
    op_system = models.CharField(max_length=20, verbose_name='Операционная система', default='Информации нет')


class PhotoCamCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик фотоаппарата
    """

    type = models.CharField(max_length=30, verbose_name='Тип фотоаппарата', default='Информации нет')
    mp = models.IntegerField(verbose_name='Количество мегапикселей', null=True, blank=True)
    max_iso = models.IntegerField(verbose_name='ISO максимальная', null=True, blank=True)
    min_iso = models.IntegerField(verbose_name='ISO минимальная', null=True, blank=True)
    video_resolution = models.IntegerField(verbose_name='Видео разрешение', null=True, blank=True)


class MicrowaveOvenCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик микроволновки
    """

    capacity = models.IntegerField(null=True, blank=True, verbose_name='Объём загрузки')
    power = models.IntegerField(null=True, blank=True, verbose_name='Мощность Вт')
    grill = models.CharField(max_length=30, default='Информации нет')
    height = models.IntegerField(null=True, blank=True, verbose_name='Высота')
    width = models.IntegerField(null=True, blank=True, verbose_name='Ширина')
    depth = models.IntegerField(null=True, blank=True, verbose_name='Глубина')


class KitchenCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик кухонного электронного прибора
    """

    type = models.CharField(max_length=20, blank=True, verbose_name='Тип техники')
    description = models.TextField(null=True, blank=True, verbose_name='Дополнительное описание')


class TorchereCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик торшера
    """

    led_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='Тип лампочки')
    place_type = models.CharField(max_length=30, null=True, blank=True, verbose_name='Место расположения')
    height = models.IntegerField(null=True, blank=True, verbose_name='Высота')


class NotebookCharacteristic(AbstractCharacteristicModel):
    """
    Модель характеристик ноутбука
    """

    laptop_type = models.CharField(max_length=20, default='Информации нет', verbose_name='Тип ноутбука')
    screen_size = models.IntegerField(null=True, blank=True, verbose_name='Размер экрана в дюймах')
    screen_resolution = models.CharField(null=True, blank=True, verbose_name='Разрешение экрана')
    ppi = models.IntegerField(null=True, blank=True, verbose_name='Плотность пикселей')
    op_system = models.CharField(max_length=20, verbose_name='Операционная система', default='Информации нет')
    op_version = models.CharField(null=True, blank=True, max_length=15, verbose_name='Версия операционной системы')


class ElectroCharacteristic(AbstractCharacteristicModel):
    """
    Characteristic model
    """

    type_product = models.CharField(max_length=20, default='Информации нет', verbose_name='Тип электроники')
    power = models.CharField(max_length=30, null=True, blank=True, verbose_name='Тип питания')
    description = models.TextField(null=True, blank=True, verbose_name='Дополнительное описание')
