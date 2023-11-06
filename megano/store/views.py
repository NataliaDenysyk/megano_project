from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from store.forms import FilterForm

from store.models import Category, Product, Offer


# Create your views here.


def product_by_category(request, category_slug=None):
    """"
    Функция получения товаров категорий и подкатегорий
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(availability=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    template_name = 'store/category_product.html',
    context = {
        'category': category,
        'categories': categories,
        'products': products}
    print('context', context)
    return render(request, template_name, context=context)


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
