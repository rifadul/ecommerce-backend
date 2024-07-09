from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.forms import ImageField
from phonenumber_field.modelfields import PhoneNumberField

from common.model import BaseModel
from roles.models import Role

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)  # Replace 'Role' with your actual role model name
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return self.email
