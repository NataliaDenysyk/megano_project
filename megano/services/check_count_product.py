from services.message_toast import ToastMessage
from store.models import Offer, Product


class CheckCountProduct:

    def __init__(self, offer):
        self.offer = Offer.objects.get(id=offer)
        self.message = ToastMessage()

    def checking_product_for_zero(self, quantity) -> bool:
        """
        Проверка товара на отсутствие (кол-во на складе = 0).
        Если товар отсутствует, значение поля "availability" меняется на False.
        """
        if self.offer.amount == 0:
            product = Product.objects.get(id=self.offer.id)
            product.availability = False
            product.save()
            self.message.toast_message('Ошибка', 'Товар отсутствует на складе')
            return False
        else:
            if quantity > self.offer.amount:
                self.message.toast_message('Ошибка', f'Товара  доступно {self.offer.amount}шт.')
                return False
        return True

    def check_more_than_it_is(self, item):
        """
        Проверка товара в корзине на попытку заказать больше,
        чем имеется на складе.
        """
        if item['quantity'] >= self.offer.amount:
            self.message.toast_message('Ошибка', f'Больше {self.offer.amount}шт. нет на складе')
            return False

        return True

    def calculating_amount_of_basket(self, item, offer):
        """
        Вычисление количества товара в корзине из запасов на складе.
        """
        self.offer = offer
        self.offer = Offer.objects.get(id=offer)
        self.offer.amount -= int(item['quantity'])
        self.offer.save()

        self.checking_product_for_zero(item['quantity'])
