from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from store.forms import FilterForm
from store.models import Product, Offer


# TODO: дописать отображение найденных после фильтрации товаров


def catalog(request: HttpRequest) -> HttpResponse:
    """
    Вьюшка отображает страницу каталога

    :param request:
    :return:
    """

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            filter_offers = filter_products(form)

            products_data = [
                {
                    "images": i_offer.product.images,
                    "name": i_offer.product.name,
                    "price": i_offer.unit_price,
                    "tags": i_offer.product.tags,
                }
                for i_offer in list(filter_offers)
            ]
            context = {
                'products_data': products_data,
                'form': form,
            }
            return render(request, 'store/catalog.html', context=context)

    else:
        form = FilterForm()

    context = {
        'form': form,
    }

    return render(request, 'store/catalog.html', context=context)


# TODO дописать фильтрацию по доставке
def filter_products(form):
    """
    Функция отбирает подходящие товары по полученным из post-запроса данным

    :param form: объект FilterForm
    :return: product_list - список объектов Product
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

    return offers
