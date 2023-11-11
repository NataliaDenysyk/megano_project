from store.models import Product, Comparison
from typing import List, Dict, Any

from django.db.models import Count

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from store.forms import FilterForm
from store.models import Product, Comparison, Offer, Category, Reviews, Discount

from cart.models import Cart


class CategoryServices:
    """
    Сервис по работе категорий
    """
    def _product_by_category(self, category_slug=None):
        """"
        Функция отбирает продукты по категориям
        """
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(availability=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            sub_categories = category.get_descendants(include_self=True)
            products = products.filter(category__in=sub_categories)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return context

    def _sorting_products(self, request):# -> dict[str, Any]:
        """"
        Функция сортировки товаров по  'Популярности'
        """
        offer = Offer.objects.filter(product__availability=True)
        if request.GET.get('popular'):
            print('offer', request.GET.get('popular'))
            offer = self._sort_by_popularity(request, offer=offer)
            context = {
                'offer': self._sort_by_popularity(request, offer=offer)
            }
        elif request.GET.get('price'):
            context = {
                'offer': self._sort_by_price(request, offer=offer)
            }
        elif request.GET.get('reviews'):
            context = {
                'offer': self._sort_by_reviews(request, offer=offer)
            }
        elif request.GET.get('novetly'):
            context = {
                'offer': self._sort_by_novelty(request, offer=offer)
            }
        else:
            context = {
                'offer': offer
            }

        print('runpy', context)
        return context

    def _sort_by_popularity(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.annotate(cnt=Count('order__total', filter='products').order_by('cnt'))
        elif 'down' in request.GET:
            offer = offer.annotate(cnt=Count('order__total', filter='products').order_by('-cnt'))
        else:
            offer = offer

        return offer

    def _sort_by_price(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.order_by('unit_price')
        elif 'down' in request.GET:
            offer = offer.order_by('-unit_price')
        else:
            offer = offer
        print('asdfghjkloiuytredcvbhn')
        return offer

    def _sort_by_reviews(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.annotate(cnt=Count('product__reviews', distinct=True).order_by('cnt'))
        elif 'down' in request.GET:
            offer = offer.annotate(cnt=Count('product__reviews', distinct=True).order_by('-cnt'))
        else:
            offer = offer

        return offer

    def _sort_by_novelty(self, request, offer) -> Any:
        if 'up' in request.GET:
            offer = offer.order_by('product__update_at')
        elif 'down' in request.GET:
            offer = offer.order_by('-product__update_at')
        else:
            offer = offer

        return offer
