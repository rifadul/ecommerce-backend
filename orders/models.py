from django.db import models
from django.conf import settings
from decimal import Decimal
from common.model import BaseModel
from products.models import ProductVariant
from coupons.models import Coupon
from address.models import Address

class ShippingMethod(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='billing_orders')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='shipping_orders')
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2)
    is_coupon_applied = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=[('cash_on_delivery', 'Cash on Delivery'), ('stripe', 'Stripe')])
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    order_status = models.CharField(max_length=50, choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='processing')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order({self.id}, {self.user})"
    
    def save(self, *args, **kwargs):
        if self.order_status == 'delivered' or self.order_status == 'cancelled':
            self.active = False
        super(Order, self).save(*args, **kwargs)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.quantity}"

class Payment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment({self.id}, {self.order})"
