from typing import List, Dict
from urllib.parse import urlparse, parse_qs, urlencode

from django.db.models import Avg, Count, When, Case

from django.shortcuts import get_object_or_404

from store.models import Product, Offer, Category, Reviews, Discount, ProductImage, Tag

from cart.models import Cart


class GetAdminSettings:
    pass


class AddProductInTrash:
    pass


class AddReview:
    pass


class DiscountProduct:
    """
    Сервис получения скидок на товары и группы товаров
    """

    def _get_all_discounts(self):
        pass

    def _get_priority_discount(self):
        pass

    def _calculate_price_with_discount(self, price) -> float:
        pass


class PaymentService:
    """
    Сервис оплаты
    """

    def _get_payment_status(self, order) -> str:
        if order.is_paid == True:
            return 'Оплаченый заказ'
        else:
            return 'Заказ не оплачен'

    def _pay_order(self, order) -> str:
        order.is_paid = True
        order.save()
        return 'Оплачено'


# TODO Добавить расчет цены с учетом скидки
# TODO Добавить отображение отзывов на страницу товара
class ProductService:
    """
    Сервис по работе с продуктами

    """

    def __init__(self, product: Product):
        self._product = product

    def _get_all_products(self):
        """
        Получить все продукты
        """
        return Product.objects.all()

    def _get_viewed_product_list(self):
        """
        Получить список просмотренных продуктов
        """
        return self._get_all_products().filter(is_viewed=True)

    def _add_product_to_viewed(self, prod_slug):
        """
        Добавить продукт в список просмотренных продуктов
        """
        product = Product.objects.get(slug=prod_slug)
        product.is_viewed = True
        product.save()

    def _remove_product_from_viewed(self, prod_id):
        """
        Удалить продукт из списка просмотренных продуктов
        """
        product = Product.objects.get(id=prod_id)
        product.is_viewed = False
        product.save()

    def _is_product_in_viewed_list(self, prod_id):
        """
        Проверить есть ли продукт в списке просмотренных продуктов
        """
        if prod_id in self._get_viewed_product_list():
            return True
        else:
            return False

    def _count_viewed_product(self) -> int:
        """
        Получить количество просмотренных продуктов
        """
        return int(len(self._get_viewed_product_list()))

    def _get_context(self) -> Dict:
        """
        Функция собирает контекст для рендера шаблона

        :param product: объект Product
        :return: context - контекст для рендера шаблона
        """

        context = {
            'feature': self._get_features(),
            'description': self._get_description(),
            'images': self._get_images(),
            'price_avg': self.get_average_price(),
            'offers': self._get_offers(),
        }

        return context

    def get_average_price(self) -> float:
        """
        Функция возвращает среднюю цену товара по всем продавцам
        """

        return round(
            Offer.objects.filter(
                product=self._product,
            ).aggregate(
                Avg('unit_price')
            ).get('unit_price__avg')
        )

    def _get_features(self) -> Dict:
        """
        Приводит строку характеристик в формат словаря

        :param product:
        :return: dict - словарь характеристик и их описаний
        """

        new_feature = dict()
        try:
            features_list = self._product.feature.split('\r\n')
            for feature in features_list:
                key, value = feature.split('-')
                new_feature[key] = value
        except Exception as error:
            return {}

        return new_feature

    def _get_description(self) -> Dict:
        """
        Приводит строку описания в формат словаря
        """

        description_data = {}

        try:
            description_list = self._product.description.split('\r\n\r\n')
            if description_list[0]:
                description_data['title'] = description_list[0]
            if description_list[1]:
                description_data['description'] = description_list[1]
            if description_list[2]:
                description_data['cart_text'] = description_list[2].split('\r\n')
            if description_list[3]:
                description_data['description_ul'] = description_list[3].split('\r\n')

            return description_data

        except Exception as error:
            return description_data

    def _get_images(self) -> ProductImage.objects:
        """
        Функция возвращает все изображения товара
        """

        return ProductImage.objects.filter(product=self._product)

    def _get_offers(self):
        """
        Функция возвращает всех продавцов товара
        """

        return Offer.objects.filter(product=self._product)

    def get_popular_products(self, quantity):
        popular_products = self._product.objects.filter(orders__status=True). \
                               values('pk', 'preview', 'name', 'category__name', 'offer__unit_price'). \
                               annotate(count=Count('pk')).order_by('-count')[:quantity]
        print(popular_products)
        return popular_products


class ComparisonServices:
    """
    Сервис по работе списка сравнений
    """

    def _add_product_to_comparison(self):
        pass

    def _get_comparison_list(self):
        pass

    def _get_amount_from_comparison(self) -> int:
        pass

    def _delete_product_from_comparison(self):
        pass


class CategoryServices:
    """
    Сервис по работе категорий
    """

    @staticmethod
    def product_by_category(category_slug=None) -> Product.objects:
        """
        Функция отбирает продукты по категориям
        """

        products = Product.objects.filter(availability=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            sub_categories = category.get_descendants(include_self=True)
            products = products.filter(category__in=sub_categories)

        return products


class CatalogService:
    """
    Сервис по работе фильтра
    """

    def catalog_processing(self, request, filterset):
        """
        Функция сортирует переданные товары и фильтрует по тегу

        :param request: объект запроса
        :param filterset: объект ProductFilter
        :return: объект ProductFilter после сортировки
        """

        if 'tag' in set(request.GET.keys()):
            filterset.queryset = self._filter_by_tags(
                filterset.queryset,
                request.GET.get('tag')
            )

        if 'sorting' in set(request.GET.keys()):
            filterset.queryset = self._sorting_products(
                request.GET.get('sorting'),
                filterset.queryset
            )

        return filterset

    @staticmethod
    def filter_products_by_name(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по имени

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(name__icontains=value)

    @staticmethod
    def filter_by_price(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по цене

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        range_list = value.split(';')
        min_price, max_price = int(range_list[0]), int(range_list[1])
        offers = Offer.objects.filter(
            unit_price__range=(min_price, max_price),
        )

        return queryset.filter(id__in=offers.values_list('product_id', flat=True))

    @staticmethod
    def filter_by_availability(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует по доступности продукта

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(availability=value)

    @staticmethod
    def filter_by_delivery(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по способу доставки

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        delivery_type = 1

        if value == 'False':
            delivery_type = 2

        return queryset.filter(offer__seller__store_settings__delivery_type=delivery_type)

    @staticmethod
    def filter_by_stores(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по продавцу

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        if value:
            offers = Offer.objects.filter(seller__in=value)

            return queryset.filter(id__in=offers.values_list('product_id', flat=True))

        return queryset

    @staticmethod
    def filter_by_feature(queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по характеристикам

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(feature__icontains=value)

    @staticmethod
    def _filter_by_tags(queryset: Product.objects, value: str) -> Product.objects:
        """
        Функция фильтрует товары по переданному тегу

        :param queryset: Product objects
        :param value: имя тега
        """

        return queryset.filter(tags__name=value)

    @staticmethod
    def get_popular_tags():
        """
        Функция отбирает популярные теги по частоте купленных товаров
        """

        tags = Tag.objects.annotate(
            count=Count(Case(
                When(products__orders__status=True, then=1),
            ))
        ).order_by('-count')

        return tags

    def _sorting_products(self, sorting: str, queryset: Product.objects) -> Product.objects:
        """
        Функция отвечает за выбор метода сортировки

        :param sorting: параметр сортировки
        """

        if 'popular' in sorting:
            queryset = self._sort_by_popularity(sorting, products=queryset)

        elif 'price' in sorting:
            queryset = self._sort_by_price(sorting, products=queryset)

        elif 'reviews' in sorting:
            queryset = self._sort_by_reviews(sorting, products=queryset)

        elif 'novelty' in sorting:
            queryset = self._sort_by_novelty(sorting, products=queryset)

        return queryset

    @staticmethod
    def _sort_by_popularity(sorting: str, products: Product.objects) -> Product.objects:
        """
        Функция сортирует продукты по популярности

        :param sorting: параметр сортировки
        """

        ordering = 'count'

        if 'down' in sorting:
            ordering = '-count'

        products = products.annotate(
            count=Count(Case(
                When(orders__status=True, then=1),
            ))
        ).order_by(ordering)

        return products

    @staticmethod
    def _sort_by_price(sorting: str, products: Product.objects) -> Product.objects:
        """
        Функция сортирует продукты по средней цене

        :param sorting: параметр сортировки
        """

        ordering = 'avg'

        if 'down' in sorting:
            ordering = '-avg'

        products = products.annotate(
            avg=Avg('offer__unit_price')
        ).order_by(ordering)

        return products

    @staticmethod
    def _sort_by_reviews(sorting: str, products: Product.objects) -> Product.objects:
        """
        Функция сортирует продукты по количеству отзывов

        :param sorting: параметр сортировки
        """

        ordering = 'count'

        if 'down' in sorting:
            ordering = '-count'

        products = products.annotate(
            count=Count('reviews')
        ).order_by(ordering)

        return products

    @staticmethod
    def _sort_by_novelty(sorting: str, products: Product.objects) -> Product.objects:
        """
        Функция сортирует продукты по дате обновления

        :param sorting: параметр сортировки
        """

        update = 'update_at'

        if 'down' in sorting:
            update = '-update_at'

        products = products.order_by(update)

        return products


class ReviewsProduct:
    """
    Сервис для добавления отзыва к товару
    """

    def _add_review_to_product(self, reviews: Reviews, product: Product) -> None:
        # добавить отзыв к товару
        pass

    def _get_list_of_product_reviews(self, product: Product) -> List:
        # получить список отзывов к товару
        pass

    def _get_discount_on_cart(self, cart: Cart) -> Discount:
        # получить скидку на корзину
        pass

    def _get_number_of_reviews_for_product(self, product: Product) -> int:
        # получить количество отзывов для товара
        pass


class GetParamService:
    """
    Сервис, позволяющий добавлять или удалять get параметры из url
    """

    def __init__(self, url):
        self._parsed_url = urlparse(url)
        self._query = parse_qs(self._parsed_url.query, keep_blank_values=True)

    def get_url(self) -> str:
        """
        Возвращает новый url
        """

        return self._parsed_url._replace(query=urlencode(self._query, True)).geturl()

    def remove_param(self, param_name: str) -> 'GetParamService':
        """
        Удаляет get параметр из url
        """

        self._query.pop(param_name, None)
        return self

    def add_param(self, param_name: str, param_value: str) -> 'GetParamService':
        """
        Добавляет get параметр в url
        """

        self._query[param_name] = param_value
        return self
