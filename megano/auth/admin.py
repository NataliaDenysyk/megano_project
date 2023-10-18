from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Store, Buyer

admin.site.register(Group)


@admin.register(Store)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class AuthorAdmin(admin.ModelAdmin):
    pass
