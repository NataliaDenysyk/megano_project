from store.models import Product


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


class Payment:
    pass


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
