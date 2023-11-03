from typing import List

from megano.store.models import Product


class GetAdminSettings:
    pass


class AddProductInTrash:
    pass


class AddReview:
    pass


class DiscountProduct:
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
