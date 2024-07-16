# products/models.py
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from categories.models import Category
from common.model import BaseModel
from tinymce.models import HTMLField
from PIL import Image, UnidentifiedImageError
from colorfield.fields import ColorField  # Import ColorField



def validate_image(image):
    valid_image_formats = ['JPEG', 'JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'WEBP',]
    try:
        img = Image.open(image)
        img_format = img.format.upper()
        if img_format not in valid_image_formats:
            raise ValidationError(f"Unsupported image format: {img_format}. Supported formats: {', '.join(valid_image_formats)}")
    except UnidentifiedImageError:
        raise ValidationError("Invalid image file")

class Size(BaseModel):  # Add Size model
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size



class Product(BaseModel):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    description = HTMLField()  # Use HTMLField for rich text description
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def in_stock(self):
        return any(variant.quantity > 0 for variant in self.variants.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    quantity = models.PositiveIntegerField(default=0)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='variants')  # ForeignKey to Size model
    color = ColorField(default='#FFFFFF')  # Use ColorField for color
    # color = models.CharField(max_length=50)
    # size = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/variants/', validators=[validate_image],help_text="Supported formats: JPEG, JPG, PNG, GIF, BMP, TIFF, WEBP")
    in_stock = models.BooleanField(default=True, editable=False)  # Automatically managed field

    def save(self, *args, **kwargs):
        # Automatically set in_stock based on quantity
        self.in_stock = self.quantity > 0
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"

class ProductSizeGuide(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_guides')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='size_guides')
    # size = models.CharField(max_length=50)
    chest = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    sleeve = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.size}"

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/', validators=[validate_image], help_text="Supported formats: JPEG, JPG, PNG, GIF, BMP, TIFF, WEBP")

    def __str__(self):
        return f"Image for {self.product.name}"