from django.contrib import admin
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

from cart.models import Cart
from .models import (
    Banners,
    Product,
    Discount,
    Offer,
    Orders,
    Category,
    Reviews,
    Tag,
    ProductImage,
)


class CartInline(admin.TabularInline):
    model = Cart
    extra = 0


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(Banners)
class AdminBanner(admin.ModelAdmin):
    list_display = ['title', 'link', 'get_html_images', 'is_active', 'update_at']
    list_display_links = ['title']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (None, {
            "fields": ('title', 'link', 'slug', 'product', 'description'),
        }),
        ("Extra options", {
            "fields": ("is_active",),
            "classes": ("collapse",),
        })
    ]

    def get_html_images(self, obj: Banners):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 60х 60.
        """
        if obj.product:
            return mark_safe(f'<img src="{obj.product.images.first().image.url}" alt=""width="60">')
        else:
            return 'not url'

    get_html_images.short_description = "Изображение"


class ProductInline(admin.TabularInline):
    model = Orders.products.through


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    inlines = [
        ProductInline,
        CartInline,
    ]
    list_display = 'pk', 'delivery_type', 'address', 'created_at', 'profile', 'total',
    list_display_links = 'pk', 'delivery_type'
    ordering = 'pk', 'created_at', 'address'
    search_fields = 'delivery_type', 'address', 'created_at'

    fieldsets = [
        (None, {
            "fields": ('profile', 'delivery_type', 'address', 'products', 'total'),
        }),
        ('Extra options', {
            'fields': ('status',),
            'classes': ('collapse',),
        })
    ]

    def get_queryset(self, request):
        return Orders.objects.select_related('profile').prefetch_related('products')


@admin.register(Category)
class AdminCategory(DjangoMpttAdmin):
    list_display = 'pk', 'name', 'image', 'parent', 'activity', 'sort_index', 'slug'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name', 'activity'
    list_filter = ['activity']
    search_fields = ['name']
    repopulated_fields = {'slug': ('name',)}

    fieldsets = [
        (None, {
            "fields": ('name', 'parent', 'sort_index', 'slug'),
        }),
        ("Extra options", {
            "fields": ("activity",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'activity' is for soft delete",
        })
    ]


class TagInline(admin.TabularInline):
    model = Product.tags.through
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


class OfferInline(admin.TabularInline):
    model = Offer


class ReviewsInline(admin.TabularInline):
    model = Reviews


class DiscountInline(admin.TabularInline):
    model = Product.discount.through
    verbose_name = 'Скидка'
    verbose_name_plural = 'Скидки'


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInlineImages(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    inlines = [
        OfferInline,
        DiscountInline,
        TagInline,
        OrderInline,
        ProductInlineImages,
        ReviewsInline,
    ]
    list_display = 'pk', 'name', 'category', 'description_short', 'created_time', 'update_time', 'availability'
    list_display_links = 'pk', 'name'
    list_filter = ['availability']
    ordering = 'pk', 'name', 'created_at'
    search_fields = 'name', 'description'
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_time', 'update_time')

    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'feature'),
        }),
        ('Главное фото', {
            'fields': ('preview',),
        }),
        ('Другие опции', {
            'fields': ('availability', 'slug', 'category'),
            "classes": ("collapse",),
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
    list_display = 'author', 'created_at', 'comment'

    def comment(self, obj: Reviews):
        return obj.comment_text[:100]


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


