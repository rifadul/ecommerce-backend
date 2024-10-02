from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('product_variant', 'quantity', 'get_price_at_order_time', 'get_discount_price_at_order_time', 'total_price')

    def get_price_at_order_time(self, obj):
        return obj.price_at_order_time
    get_price_at_order_time.short_description = 'Price at Order Time'

    def get_discount_price_at_order_time(self, obj):
        return obj.discount_price_at_order_time
    get_discount_price_at_order_time.short_description = 'Discount Price at Order Time'

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    readonly_fields = ('payment_method', 'amount', 'status', 'stripe_charge_id')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_number', 'user', 'billing_address', 'shipping_address', 'shipping_method', 'subtotal', 'tax', 'shipping', 'discount', 'total', 'payment_method', 'payment_status', 'order_status', 'created_at', 'updated_at')
    list_filter = ('payment_status', 'order_status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'billing_address__address_line1', 'shipping_address__address_line1')
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ('subtotal', 'tax', 'shipping', 'discount', 'total', 'price_before_discount', 'is_coupon_applied')

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration', 'price')
    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'status', 'stripe_charge_id', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'created_at', 'updated_at')
    search_fields = ('order__user__username', 'stripe_charge_id')

admin.site.register(OrderItem)  # Register OrderItem for additional configuration if needed
