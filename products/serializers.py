# products/serializers.py
from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from .models import Product, ProductVariant, ProductSizeGuide, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'quantity', 'color', 'size', 'image','in_stock']

class ProductSizeGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeGuide
        fields = ['id', 'size', 'chest', 'length', 'sleeve']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    variants = ProductVariantSerializer(many=True)
    size_guides = ProductSizeGuideSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'short_description', 'description', 'slug', 'sku', 'category', 
            'price', 'discount_price', 'images', 'width', 
            'height', 'weight', 'depth', 'variants', 'size_guides'
        ]

    def validate(self, data):
        if not data.get('variants'):
            raise serializers.ValidationError("Product variants are required.")
        if not data.get('size_guides'):
            raise serializers.ValidationError("Product size guides are required.")
        return data

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        variants_data = validated_data.pop('variants')
        size_guides_data = validated_data.pop('size_guides')
        images_data = validated_data.pop('images')
        
        category = Category.objects.get(id=category_data['id'])
        product = Product.objects.create(category=category, **validated_data)

        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        
        for size_guide_data in size_guides_data:
            ProductSizeGuide.objects.create(product=product, **size_guide_data)
        
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        return product