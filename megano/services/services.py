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


class Payment:
    pass


class ProductService:
    """
    Сервис по работе с просмотренными продуктами
    """

    def _get_all_products(self):
        """
        Получить все продукты
        """
        return Product.objects.all()

    def _get_viewed_product_list(self) -> List[str]:
        """
        Получить список просмотренных продуктов
        """
        return list(Product.objects.filter(is_viewed=True))

    def _add_product_to_viewed(self, prod_id):
        """
        Добавить продукт в список просмотренных продуктов
        """
        product = Product.objects.get(id=prod_id)
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

