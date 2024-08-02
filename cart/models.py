from django.db import models
from django.conf import settings
from decimal import Decimal
from common.model import BaseModel
from products.models import ProductVariant
from coupons.models import Coupon

class Cart(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))

    def __str__(self):
        return f"Cart({self.user})"

    def calculate_totals(self):
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.tax = self.subtotal * Decimal('0.1')  # Assuming a tax rate of 10%
        self.shipping = Decimal('10.0')  # Assuming a flat shipping rate
        self.price_before_discount = self.subtotal + self.tax + self.shipping
        if self.coupon and self.coupon.is_valid():
            if self.coupon.discount_type == 'percentage':
                self.discount = self.subtotal * (self.coupon.discount_value / Decimal('100'))
            elif self.coupon.discount_type == 'fixed':
                self.discount = self.coupon.discount_value
            # Apply maximum discount limit
            if self.coupon.max_discount_amount and self.discount > self.coupon.max_discount_amount:
                self.discount = self.coupon.max_discount_amount
        else:
            self.discount = Decimal('0.0')
        self.total = self.price_before_discount - self.discount
        self.save()

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.product_variant.product.name}, color: {self.product_variant.color}, size: {self.product_variant.size}, quantity: {self.quantity}"

    @property
    def total_price(self):
        # Use discount price if available, otherwise use main price
        product_price = self.product_variant.product.discount_price if self.product_variant.product.discount_price else self.product_variant.product.price
        return product_price * self.quantity
