from store.models import Product, Comparison
from typing import List, Dict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from store.forms import FilterForm
from store.models import Product, Comparison, Offer, Category, Reviews, Discount

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


class ProductService:
    """
    Сервис по работе с просмотренными продуктами
    """

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



# class CategoryServices:
    # def _product_by_category(request, category_slug=None):
    #     category = None
    #     categories = Category.objects.all()
    #     products = Product.objects.filter(availability=True)
    #     if category_slug:
    #         category = get_object_or_404(Category, slug=category_slug)
    #         products = products.filter(category=category)
    #     template_name = 'store/category_product.html',
    #     context = {
    #         'category': category,
    #         'categories': categories,
    #         'products': products,
    #     }
    #     return render(request, template_name, context=context)


class CatalogServices:
    """
    Сервис по работе фильтра
    """
    #TODO добавить контекст или удалить и перенести во вьюшку
    def _get_context(self, context):
        context['filter'] = FilterForm()
        return context

    #TODO дописать обработку других post-запросов
    def _get_context_from_post(self, request) -> HttpResponse:
        """
        Функция обрабатывает post-запросы

        :param request:
        :return:
        """

        if 'filter-button' in request.POST:
            filter_data = FilterForm(request.POST)
            if filter_data.is_valid():
                offers, saved_form = self._filter_products(filter_data)
                products_list = self._get_filtered_products(offers)

                context = {
                    'filter': saved_form,
                    'products': products_list,
                }

                return (context)

    # TODO дописать фильтрацию по доставке
    def _filter_products(self, form):
        """
        Функция фильтрует товары по полученным из post-запроса данным

        :param form: объект FilterForm
        :return:
            offers - объекты Offer
            form - фильтр с сохраненными параметрами
        """

        range_list = form.cleaned_data['range'].split(';')
        min_price, max_price = int(range_list[0]), int(range_list[1])

        stores_list = form.cleaned_data['stores']
        availability = form.cleaned_data['availability']
        delivery_free = form.cleaned_data['delivery_free']

        offers = Offer.objects.filter(
            unit_price__range=(min_price, max_price),
            product__name__icontains=form.cleaned_data['name'],
            product__feature__icontains=form.cleaned_data['another_feature'],
        )

        if stores_list:
            offers = offers.filter(seller__in=stores_list)

        if availability:
            offers = offers.filter(product__availability=availability)

        if delivery_free:
            pass

        form.fields['range'].widget.attrs['data-from'] = min_price
        form.fields['range'].widget.attrs['data-to'] = max_price

        return offers, form

    #  TODO Добавить расчет усредненной цены по продавцам, корректное выведение тегов

    def _get_filtered_products(self, offers) -> List[Dict]:
        """
        Функция создает и возвращает список из отфильтрованных товаров

        :param offers:
        :return: products_data - список словарей с данными товаров
        """

        products_data = [
            {
                "preview": i_offer.product.preview,
                "name": i_offer.product.name,
                "price": i_offer.unit_price,
                "category": i_offer.product.category,
            }
            for i_offer in list(offers)
        ]

        return products_data

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

