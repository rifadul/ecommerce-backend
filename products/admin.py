# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import  Product, ProductVariant, ProductSizeGuide, ProductImage
from .forms import ProductAdminForm, ProductVariantInlineForm, ProductSizeGuideInlineForm

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    form = ProductVariantInlineForm

class ProductSizeGuideInline(admin.TabularInline):
    model = ProductSizeGuide
    extra = 1
    form = ProductSizeGuideInlineForm

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)  # Add image_preview to readonly_fields
    fields = ('image', 'image_preview')  # Ensure image_preview is displayed with image field

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 150px; height: auto;" />'.format(obj.image.url))
        return "No image available"
    
    image_preview.short_description = 'Image Preview'



class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ( 'image_tag', 'name', 'category', 'price', 'discount_price', 'sku',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_description', 'description', 'slug', 'sku',)
        }),
        ('Categories', {
            'fields': ('category',)
        }),
        ('Pricing Information', {
            'fields': ('price', 'discount_price')
        }),
        ('Product Dimensions', {
            'fields': ('width', 'height', 'weight', 'depth')
        }),
    )
    inlines = [ProductVariantInline, ProductSizeGuideInline, ProductImageInline]

    def image_tag(self, obj):
        if obj.images.first():
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.images.first().image.url))
        return "-"
    
    image_tag.short_description = 'Image'

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
