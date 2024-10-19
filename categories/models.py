from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from common.model import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if self.parent:
            ancestor = self.parent
            while ancestor:
                if ancestor == self:
                    raise ValidationError("A category cannot be a subcategory of its own subcategory.")
                ancestor = ancestor.parent

    def get_descendants(self):
        descendants = []
        children = self.subcategories.all()
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_descendants())  # Recursively get all children
        return descendants
    
    def __str__(self):
        return self.name
