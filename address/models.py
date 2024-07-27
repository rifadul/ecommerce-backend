from django.db import models

from common.model import BaseModel
from palooi_project import settings

# Create your models here.
class Address(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    defaultAddress = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.defaultAddress:
            Address.objects.filter(user=self.user, defaultAddress=True).update(defaultAddress=False)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Address of {self.name}"
    
