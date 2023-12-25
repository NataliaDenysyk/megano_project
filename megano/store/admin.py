from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.shortcuts import reverse
from django.utils.html import format_html

from django.core.cache import cache
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

from django.db.models import QuerySet
from django.http import HttpRequest

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
    BannersCategory,
)
from compare.admin import (TVSetCharacteristicInline,
                           HeadphonesCharacteristicInline,
                           PhotoCamCharacteristicInline,
                           KitchenCharacteristicInline,
                           WashMachineCharacteristicInline,
                           NotebookCharacteristicInline,
                           TorchereCharacteristicInline,
                           MicrowaveOvenCharacteristicInline,
                           MobileCharacteristicInline)

from authorization.models import Profile


@admin.action(description='Архивировать')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Разархивировать')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.action(description='Доступен')
def mark_availability(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(availability=True)


@admin.action(description='Не доступен')
def mark_unavailability(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(availability=False)


@admin.action(description="Сбросить кэш списка товаров")
def reset_product_list_cache(self, request, queryset):
    cache.clear()
    self.message_user(request, "кэш списка товаров сброшен.")


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
    save_on_top = True

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
            return mark_safe(f'<img src="{obj.product.preview.url}" alt=""width="60">')
        else:
            return 'not url'

    get_html_images.short_description = "Изображение"


class ProductInline(admin.TabularInline):
    model = Orders.products.through
    extra = 0


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    actions = [
        mark_archived, mark_unarchived
    ]
    inlines = [
        ProductInline,
        CartInline,
    ]
    list_display = ['pk', 'profile_url', 'status', 'total_payment']
    list_display_links = ['pk',]
    ordering = ['pk', 'created_at',]
    search_fields = ['delivery_type', 'created_at']
    readonly_fields = ['created_at',]
    save_on_top = True

    fieldsets = [
        (None, {
            "fields": ('profile', 'total_payment', 'delivery_type',
                       'payment', 'created_at', 'address', 'status', 'status_exception',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
        })
    ]

    def get_queryset(self, request):
        return Orders.objects.select_related('profile').prefetch_related('products')

    def get_actions(self, request):
        """"
        Функкция удаляет 'delete_selected' из actions(действие) в панели администратора
        """
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def profile_url(self, obj: Product) -> str:
        link = reverse('admin:authorization_profile_change', args=(obj.profile.id,))
        return format_html('<a href="{}">{}</a>', link, obj.profile.user.username)

    profile_url.short_description = 'Покупатель'


@admin.register(Category)
class AdminCategory(DjangoMpttAdmin):
    actions = [
        mark_archived, mark_unarchived
    ]
    list_display = ['pk', 'name', 'image', 'parent', 'activity', 'sort_index', 'slug']
    list_display_links = ['pk', 'name']
    ordering = ['pk', 'name', 'activity']
    list_filter = ['activity']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

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

    def get_actions(self, request):
        """"
        Функкция удаляет 'delete_selected' из actions(действие) в панели администратора
        """
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TagInline(admin.TabularInline):
    model = Product.tags.through
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'
    extra = 0


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        is_seller_field = db_field.name == 'seller'

        if is_seller_field:
            kwargs['queryset'] = Profile.objects.filter(role='store')

        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if is_seller_field:
            formfield.label_from_instance = lambda inst: "{}".format(inst.name_store)

        return formfield


class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 0


class DiscountInline(admin.TabularInline):
    model = Product.discount.through
    verbose_name = 'Скидка'
    verbose_name_plural = 'Скидки'
    extra = 0


class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra = 0


class ProductInlineImages(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    actions = [
        mark_availability, mark_unavailability, reset_product_list_cache
    ]
    inlines = [
        OfferInline,
        DiscountInline,
        TagInline,
        OrderInline,
        ProductInlineImages,
        ReviewsInline,
        TVSetCharacteristicInline,
        HeadphonesCharacteristicInline,
        PhotoCamCharacteristicInline,
        KitchenCharacteristicInline,
        WashMachineCharacteristicInline,
        NotebookCharacteristicInline,
        TorchereCharacteristicInline,
        MicrowaveOvenCharacteristicInline,
        MobileCharacteristicInline,
    ]
    list_display = ['pk', 'name', 'category_url', 'description_short', 'limited_edition']
    list_display_links = 'pk', 'name'
    list_filter = ['availability']
    ordering = ['pk', 'availability', 'name', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_time', 'update_time']
    save_on_top = True

    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'category'),
        }),
        ('Главное фото', {
            'fields': ('preview',),
        }),
        ('Другие опции', {
            'fields': ('limited_edition', 'availability', 'slug',),
            "classes": ("collapse",),
        }),
    ]

    def get_queryset(self, request):
        return Product.objects.select_related('category').prefetch_related('discount', 'tags', 'offers')

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

    def category_url(self, obj: Product) -> str:
        link = reverse('admin:store_category_change', args=(obj.category.id,))
        return format_html('<a href="{}">{}</a>', link, obj.category.name)

    description_short.short_description = 'Описание'
    created_time.short_description = 'Создан'
    update_time.short_description = 'Отредактирован'
    category_url.short_description = 'Категория'

    def get_actions(self, request):
        """"
        Функкция удаляет 'delete_selected' из actions(действие) в панели администратора
        """
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['pk', 'seller', 'product_url', 'unit_price', 'amount']
    list_display_links = ['pk', 'seller']
    ordering = ['pk', 'unit_price', 'amount']
    search_fields = ['product', 'seller', 'unit_price', 'amount']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'seller':
            kwargs['queryset'] = Profile.objects.filter(role='store')
        return super(OfferAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def product_url(self, obj: Product) -> str:
        link = reverse('admin:store_product_change', args=(obj.product.id,))
        return format_html('<a href="{}">{}</a>', link, obj.product.name)

    product_url.short_description = 'Товар'


class ProductInline(admin.TabularInline):
    model = Discount.products.through
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'
    extra = 0


@admin.register(Reviews)
class ReviewsProduct(admin.ModelAdmin):
    list_display = 'author', 'created_at', 'comment'

    def comment(self, obj: Reviews):
        return obj.comment_text[:100]


class CategoriesInline(admin.TabularInline):
    model = Discount.categories.through
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    extra = 0


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
        CategoriesInline
    ]
    list_display = ['pk', 'title', 'name', 'get_html_images', 'is_active']
    list_display_links = ['pk', 'name', 'title']
    ordering = ['pk', 'name', 'valid_to', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True

    fieldsets = [
        (None, {
            'fields': ('title', 'slug', 'name', 'image', 'description', 'priority', 'sum_discount', 'sum_cart',
                       'total_products', 'valid_from', 'valid_to', 'is_active'),
        }),
    ]

    def get_queryset(self, request):
        return Discount.objects.prefetch_related('products')

    def get_html_images(self, obj: Discount):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 50х 50.
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" alt=""width="50">')

    get_html_images.short_description = "Изображение"


@admin.register(BannersCategory)
class AdminBannerCategory(admin.ModelAdmin):
    list_display = ['category', 'get_html_images', 'is_active']
    list_display_links = ['category']
    list_filter = ['is_active']

    def get_html_images(self, obj: BannersCategory):
        """
        В панели администратора,
        ссылка на изображение отображается в виде картинки размером 60х 60.
        """
        if obj.preview:
            return mark_safe(f'<img src="{obj.preview.url}" alt=""width="60">')
        else:
            return 'not url'

    get_html_images.short_description = "Изображение"
