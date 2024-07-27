from django.db import models

from common.model import BaseModel
from palooi_project import settings
from products.models import Product

# Create your models here.
class WishList(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='wishlist_product')

    def __str__(self):
        return f"Wishlist of {self.user}"
