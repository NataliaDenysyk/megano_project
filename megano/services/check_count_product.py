from store.models import Offer


class CheckCountProduct:

    def __init__(self, offer):
        self.offer = Offer.objects.get(id=offer)

    def checking_product_for_zero(self) -> bool:
        """
        Проверка товара на отсутствие (кол-во на складе = 0).
        Если товар отсутствует, значение поля "availability" меняется на False.
        """
        if self.offer.amount == 0:
            self.offer.product.availability = False
            self.offer.save()
            # TODO: добавить сообщение, что товар отсутствует на складе
            return False

        return True

    def check_more_than_it_is(self, item):
        """
        Проверка товара в корзине на попытку заказать больше,
        чем имеется на складе.
        """
        if item['quantity'] > self.offer.amount:
            # TODO: добавить сообщение, что заказанного товара больше чем на складе
            return item['quantity']

        return True

    @staticmethod
    def calculating_amount_of_basket(item, offer):
        """
        Вычисление количества товара в корзине из запасов на складе.
        """
        _offer = Offer.objects.get(id=offer)
        _offer.amount -= int(item['quantity'])
        _offer.save()
