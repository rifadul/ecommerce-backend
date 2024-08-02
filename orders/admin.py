from django.contrib import admin

from orders.models import ShippingMethod

# Register your models here.
@admin.register(ShippingMethod)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'duration', 'price',)