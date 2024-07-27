# wishlist/admin.py
from django.contrib import admin
from .models import WishList


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user','product')
