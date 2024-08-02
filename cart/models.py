from django.db import models
from django.conf import settings
from common.model import BaseModel
from products.models import Product, ProductVariant

class Cart(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart({self.user})"

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
        return self.product_variant.product.price * self.quantity
