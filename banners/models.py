from django.db import models

from common.model import BaseModel

# Create your models here.
class Banner(BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    AUDIENCE_CHOICES = (
        ('customer', 'Customer'),
        ('merchant', 'Merchant')
    )

    name = models.CharField(max_length=100)
    button_name = models.CharField(max_length=50)
    button_link = models.URLField(max_length=200)
    popup = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='customer')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)

    def __str__(self):
        return self.name