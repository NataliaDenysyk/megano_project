from django.contrib import admin

from .models import (
    Banners,
    Product,
    Discount,
    Offer,
    Orders,
    Category,
)


class AdminBanner(admin.ModelAdmin):
    list_display = ['title', 'link', 'images', 'is_active', 'update_at']
    list_display_links = ['title']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Banners, AdminBanner)


class ProductInline(admin.TabularInline):
    model = Orders.products.through


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'delivery_type', 'address', 'created_at'
    list_display_links = 'pk', 'delivery_type'
    ordering = 'pk', 'created_at', 'address'
    search_fields = 'delivery_type', 'address', 'created_at'


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = 'pk', 'name', 'image', 'parent', 'activity'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name', 'activity'
    list_filter = ['activity']
    search_fields = ['name']


class TagInline(admin.TabularInline):
    model = Product.tags.through
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class OfferInline(admin.TabularInline):
    model = Offer


class DiscountInline(admin.TabularInline):
    model = Product.discount.through
    verbose_name = 'Скидка'
    verbose_name_plural = 'Скидки'


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    inlines = [
        OfferInline,
        DiscountInline,
        TagInline,
    ]
    list_display = 'pk', 'name', 'category', 'description_short', 'created_time', 'update_time', 'availability'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name', 'created_at'
    search_fields = 'name', 'description'
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_time', 'update_time')

    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'feature'),
        }),
        ('Images', {
            'fields': ('images',),
        }),
        ('Reviews', {
            'fields': ('reviews',),
        }),
        ('Extra options', {
            'fields': ('availability', 'slug', 'category'),
        }),
    ]

    def get_queryset(self, request):
        return Product.objects.select_related('category').prefetch_related('discount', 'tags', 'offer_set')

    def description_short(self, obj: Product) -> str:
        """
        Функция уменьшает длинные описания

        :param obj: Product object
        :return: string
        """

        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'

    def created_time(self, obj: Product):
        return obj.created_at.strftime("%d %B %Y")

    def update_time(self, obj: Product):
        return obj.update_at.strftime("%d %B %Y")

    description_short.short_description = 'Описание'
    created_time.short_description = 'Создан'
    update_time.short_description = 'Отредактирован'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = 'pk', 'product', 'seller_verbose', 'unit_price', 'amount'
    list_display_links = 'pk', 'product'
    ordering = 'pk', 'unit_price', 'amount'
    search_fields = 'product', 'seller_verbose', 'unit_price', 'amount'

    def get_queryset(self, request):
        return Offer.objects.select_related('seller', 'product')

    def seller_verbose(self, obj: Offer) -> str:
        return obj.seller.name_store

    seller_verbose.short_description = 'Продавец'


class ProductInline(admin.TabularInline):
    model = Discount.products.through
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'


@admin.register(Reviews)
class ReviewsProduct(admin.ModelAdmin):
    list_display = 'comment_text', 'created_at', 'author'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'name', 'description', 'sum_discount', 'valid_from', 'valid_to', 'is_active'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name', 'valid_to', 'is_active'
    search_fields = 'name', 'description'

    def get_queryset(self, request):
        return Discount.objects.prefetch_related('products')
