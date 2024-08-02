from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity', 'total_price')
    readonly_fields = ('total_price',)
    search_fields = ('cart__user__username', 'product_variant__product__name', 'product_variant__color', 'product_variant__size')
    list_filter = ('product_variant__product__name', 'product_variant__color', 'product_variant__size')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'
