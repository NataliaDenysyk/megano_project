from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from compare.models import (HeadphonesCharacteristic,
                            TVSetCharacteristic,
                            WashMachineCharacteristic,
                            MobileCharacteristic,
                            PhotoCamCharacteristic,
                            NotebookCharacteristic,
                            KitchenCharacteristic,
                            TorchereCharacteristic,
                            ElectroCharacteristic,
                            MicrowaveOvenCharacteristic)

from store.models import Product

"""
Сервис по работе списка сравнений
"""


def _add_product_to_comparison(request: WSGIRequest, comparison_id) -> HttpResponseRedirect:
    """
    Добавить одну единицу товара в корзине

    :param request: запрос
    :param slug: slug товара
    :return: HttpResponse - текущая страница
    """

    if request.user.is_authenticated:
        # Если пользователь авторизован, используем сессии
        comparison_list = request.session.get('comparison_list', [])
    else:
        # Если пользователь не авторизован, используем куки
        comparison_list = request.COOKIES.get('comparison_list', '').split(',')

    # Проверка, чтобы не было больше 4 продуктов для сравнения и не добавлять 1 товар несколько раз
    if len(set(comparison_list)) >= 4:
        comparison_list.pop(0)
        # comparison_list.clear()
    # Проверка, чтобы избежать добавления одного товара несколько раз
    if comparison_id not in comparison_list:
        comparison_list.append(comparison_id)

        if request.user.is_authenticated:
            # Если пользователь авторизован, сохраняем в сессию
            request.session['comparison_list'] = comparison_list
        else:
            # Если пользователь не авторизован, сохраняем в куки
            response = HttpResponseRedirect(reverse('store:catalog'))
            response.set_cookie('comparison_list', ','.join(comparison_list))

            return response


def get_comparison_list(comparison_list):
    products = Product.objects.filter(id__in=comparison_list)
    return products


def get_compare_info(products, prev_prod_category=None) -> dict:
    result = dict()

    for product in products:
        if prev_prod_category == product.category.name or prev_prod_category == None:
            # Получение характеристик из модели в зависимости от категории по id
            id_model_characterisrics = product.feature.values()[0].get('id')
            # Получение общих характеристик в список характеристик
            general_characteristics = get_characteristic_from_common_info(product.feature.values()[0])

            # Добавление характеристик в список характеристик в зависимости от характеристик
            model_info = return_model(product, id_model_characterisrics)

            prev_prod_category = product.category.name
            product_price = product.get_average_price()
            result[product.name] = {
                'product_preview_url': product.preview.url,
                'product_slug': product.slug,
                'product_name': product.name,
                'product_category': product.category.name,
                'characterisctics': general_characteristics,
                'product_characteristic_list': model_info,
                'product_price': product_price,
                'product_offer_id': product.offers.first().id,
            }
        else:
            return redirect(reverse_lazy("compare:comparison_error"))

    return result


def return_model(product, id_model_characteristics) -> dict:
    if product.category.name == 'наушники' or product.category.name == 'Наушники':
        return characteristic_headset(id_model_characteristics)
    if product.category.name == 'Телевизоры' or product.category.name == 'телевизоры':
        return characteristic_tv(id_model_characteristics)
    if product.category.name == 'Мобильные телефоны':
        return characteristic_mobile(id_model_characteristics)
    if product.category.name == 'Стиральные машины':
        return characteristic_wm(id_model_characteristics)
    if product.category.name == 'Фотоаппараты':
        return characteristic_photo(id_model_characteristics)
    if product.category.name == 'Ноутбуки' or product.category.name == 'ноутбуки' or product.category.name == 'ноутбук':
        return characteristic_nb(id_model_characteristics)
    if product.category.name == 'Электроника':
        return characteristic_electro(id_model_characteristics)
    if product.category.name == 'Микроволновые печи':
        return characteristic_mw(id_model_characteristics)
    if product.category.name == 'Кухонная техника':
        return characteristic_kitchen_technik(id_model_characteristics)
    if product.category.name == 'Торшеры':
        return characteristic_torchere(id_model_characteristics)


def characteristic_headset(id_model_characteristics) -> dict:
    model_info = HeadphonesCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Беспроводные': model_info.wireless,
                      'Наличие микрофона': model_info.mic,
                      'Ношение': model_info.fit,
                      'Наличие bluetooth': model_info.bluetooth,
                      'Сомпротивление, Ом': model_info.resistance,
                      'Наличие HDMI': model_info.hdmi,
                      }
    return characteristic


def characteristic_wm(id_model_characteristics) -> dict:
    model_info = WashMachineCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Высота': model_info.height,
                      'Ширина': model_info.width,
                      'Глубина': model_info.depth,
                      'Тип загрузки': model_info.type_loading,
                      'Объём загрузки': model_info.capacity,
                      'Дополнительное описание': model_info.description,
                      }
    return characteristic


def characteristic_mobile(id_model_characteristics) -> dict:
    model_info = MobileCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип мобильного телефона': model_info.phone_type,
                      'Размер экрана в дюймах': model_info.screen_size,
                      'Разрешение экрана': model_info.screen_resolution,
                      'Технология экрана': model_info.screen_technology,
                      'Операционная система': model_info.op_system,
                      }
    return characteristic


def characteristic_tv(id_model_characteristics) -> dict:
    model_info = TVSetCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Название': model_info.name,
                      'Размер экрана': model_info.screen,
                      'Разрешение экрана': model_info.resolution,
                      'Страна производитель': model_info.country,
                      'Частота обновления': model_info.freq,
                      'Наличие Wi - Fi': model_info.wi_fi,
                      'HDMI': model_info.hdmi,
                      'Дополнительное описание': model_info.description,
                      }
    return characteristic


def characteristic_photo(id_model_characteristics) -> dict:
    model_info = PhotoCamCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип фотоаппарата': model_info.type,
                      'Количество мегапикселей': model_info.mp,
                      'ISO максимальная': model_info.max_iso,
                      'ISO минимальная': model_info.min_iso,
                      'Видео разрешение': model_info.video_resolution,
                      }
    return characteristic


def characteristic_nb(id_model_characteristics) -> dict:
    model_info = NotebookCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип ноутбука': model_info.laptop_type,
                      'Размер экрана в дюймах': model_info.screen_size,
                      'Разрешение экрана': model_info.screen_resolution,
                      'Плотность пикселей': model_info.ppi,
                      'Операционная система': model_info.op_system,
                      'Версия операционной системы': model_info.op_version,
                      }
    return characteristic


def characteristic_mw(id_model_characteristics) -> dict:
    model_info = MicrowaveOvenCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Объём загрузки': model_info.capacity,
                      'Мощность Вт': model_info.power,
                      'Гриль': model_info.grill,
                      'Высота, мм': model_info.height,
                      'Ширина, мм': model_info.width,
                      'Глубина, мм': model_info.depth,
                      }
    return characteristic


def characteristic_kitchen_technik(id_model_characteristics) -> dict:
    model_info = KitchenCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип техники': model_info.type,
                      'Дополнительное описание': model_info.description,
                      }
    return characteristic


def characteristic_electro(id_model_characteristics) -> dict:
    model_info = ElectroCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип электроники': model_info.type_product,
                      'Тип питания': model_info.power,
                      'Дополнительное описание': model_info.description,
                      }
    return characteristic


def characteristic_torchere(id_model_characteristics) -> dict:
    model_info = TorchereCharacteristic.objects.get(id=id_model_characteristics)
    characteristic = {'Тип лампочки': model_info.led_type,
                      'Высота': model_info.height,
                      'Место расположения': model_info.place_type,
                      }
    return characteristic


def get_characteristic_from_common_info(data) -> dict:
    characteristic_info = {'Страна производства': data.get('made_in'),
                           'Год производства': data.get('production_year'),
                           'Цвет': data.get('color'),
                           'Вес': data.get('weight'),
                           }
    return characteristic_info
