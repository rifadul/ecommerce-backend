# coupons/models.py
from django.db import models
from django.utils import timezone
from categories.models import Category
from common.model import BaseModel

class Coupon(BaseModel):
    CODE_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=CODE_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        return self.code
