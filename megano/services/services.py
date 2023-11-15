from typing import List, Dict, Any
from django.db.models import Avg, Count

from django.shortcuts import get_object_or_404

from store.models import Product, Offer, Category, Reviews, Discount, ProductImage

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
            'price_avg': self._get_average_price(),
            'offers': self._get_offers(),
        }

        return context

    def _get_average_price(self) -> float:
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
    def _product_by_category(self, category_slug=None):
        """"
        Функция отбирает продукты по категориям
        """
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(availability=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            sub_categories = category.get_descendants(include_self=True)
            products = products.filter(category__in=sub_categories)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return context

    def _sorting_products(self, request):# -> dict[str, Any]:
        """"
        Функция сортировки товаров по  'Популярности'
        """
        offer = Offer.objects.filter(product__availability=True)
        if request.GET.get('popular'):
            offer = self._sort_by_popularity(request, offer=offer)
            context = {
                'offer': self._sort_by_popularity(request, offer=offer)
            }
        elif request.GET.get('price'):
            context = {
                'offer': self._sort_by_price(request, offer=offer)
            }
        elif request.GET.get('reviews'):
            context = {
                'offer': self._sort_by_reviews(request, offer=offer)
            }
        elif request.GET.get('novetly'):
            context = {
                'offer': self._sort_by_novelty(request, offer=offer)
            }
        else:
            context = {
                'offer': offer
            }

        return context

    def _sort_by_popularity(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.annotate(cnt=Count('order__total', filter='products').order_by('cnt'))
        elif 'down' in request.GET:
            offer = offer.annotate(cnt=Count('order__total', filter='products').order_by('-cnt'))
        else:
            offer = offer

        return offer

    def _sort_by_price(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.order_by('unit_price')
        elif 'down' in request.GET:
            offer = offer.order_by('-unit_price')
        else:
            offer = offer
        return offer

    def _sort_by_reviews(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.annotate(cnt=Count('product__reviews', distinct=True).order_by('cnt'))
        elif 'down' in request.GET:
            offer = offer.annotate(cnt=Count('product__reviews', distinct=True).order_by('-cnt'))
        else:
            offer = offer

        return offer

    def _sort_by_novelty(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.order_by('product__update_at')
        elif 'down' in request.GET:
            offer = offer.order_by('-product__update_at')
        else:
            offer = offer

        return offer


class CatalogService:
    """
    Сервис по работе фильтра
    """

    def _filter_products_by_name(self, queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по имени

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(name__icontains=value)

    def _filter_by_price(self, queryset: Product.objects, name: str, value: str) -> Product.objects:
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

    def _filter_by_availability(self, queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует по доступности продукта

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(availability=value)

    # TODO дописать фильтрацию по доставке
    def _filter_by_delivery(self, queryset: Product.objects, name: str, value: str):
        """
        Функция фильтрует товары по способу доставки

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        pass

    def _filter_by_stores(self, queryset: Product.objects, name: str, value: str) -> Product.objects:
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

    def _filter_by_feature(self, queryset: Product.objects, name: str, value: str) -> Product.objects:
        """
        Функция фильтрует товары по характеристикам

        :param queryset: Product objects
        :param name: имя поля фильтра
        :param value: значения поля
        """

        return queryset.filter(feature__icontains=value)


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
