from typing import List

from django.shortcuts import get_object_or_404

from store.models import Product, Comparison, Offer, Category


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

    def _get_all_discounts(self) -> List:
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

    def _pay_order(self, order) -> bool:
        order.is_paid = True
        order.save()
        return 'Оплачено'


class ProductViewed:
    """
    Сервис по работе с просмотренными продуктами
    """

    def _add_product_to_viewed(self) -> bool:
        pass

    def _remove_product_from_viewed(self) -> bool:
        pass

    def _is_product_in_viewed_list(self) -> bool:
        pass

    def _get_viewed_product_list(self) -> List[str]:
        pass

    def _count_viewed_product(self) -> int:
        pass


class ComparisonViewed:
    """
    Сервис по работе списка сравнений
    """

    def _add_product_to_comparison(self) -> bool:
        pass

    def _get_comparison_list(self) -> List[str]:
        pass

    def _get_amount_from_comparison(self) -> int:
        pass

    def _delete_product_from_comparison(self) -> bool:
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


class CatalogFilterServices:
    """
    Сервис по работе фильтра
    """

    # TODO дописать фильтрацию по доставке
    @classmethod
    def _filter_products(cls, form):
        """
        Функция фильтрует товары по полученным из post-запроса данным

        :param form: объект FilterForm
        :return: products_data - список объектов Product
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
    @classmethod
    def _get_filtered_products(cls, offers) -> List:
        """
        Функция создает и возвращает список из отфильтрованных товаров

        :param offers:
        :return: products_data - список товаров
        """

        products_data = [
            {
                "images": i_offer.product.images,
                "name": i_offer.product.name,
                "price": i_offer.unit_price,
                "tags": i_offer.product.tags,
            }
            for i_offer in list(offers)
        ]

        return products_data

