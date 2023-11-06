from typing import List

from store.models import Product, Comparison


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

    def _add_product_to_viewed(self) -> Bool:
        pass

    def _remove_product_from_viewed(self) -> Bool:
        pass

    def _is_product_in_viewed_list(self) -> Bool:
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
