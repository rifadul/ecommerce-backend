from django.db import models

from common.model import BaseModel
from palooi_project import settings
from products.models import Product

# Create your models here.
class Wishlist(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"Wishlist of {self.user}"
    

class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('wishlist', 'product')

    def __str__(self):
        return f"{self.product.name} in wishlist of {self.wishlist.user}"