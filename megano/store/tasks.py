from megano.celery import app
from services.services import PaymentService


@app.task
def pay_order(order_id, card):
    PaymentService(order_id, card).get_payment_status()
