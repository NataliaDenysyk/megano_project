from megano.celery import app
from services.services import PaymentService


@app.task
def pay_order(order_id: int, card: str):
    """
    Таск на оплату
    """

    PaymentService(order_id, card).get_payment()
