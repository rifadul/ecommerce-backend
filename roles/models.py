from django.db import models
from common.model import BaseModel

class Module(BaseModel):
    """
    Model representing a module.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Permission(BaseModel):
    """
    Model representing a permission linked to a module.
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.module.name} - {self.name}"

class Role(BaseModel):
    """
    Model representing a role with multiple permissions.
    """
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name
