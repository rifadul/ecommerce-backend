# products/serializers.py
from rest_framework import serializers
from collections import defaultdict

from categories.models import Category
from .models import Product, ProductVariant, ProductSizeGuide, ProductImage, Size
from categories.serializers import CategorySerializer

# Serializer for Size model
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size']

# Serializer for color, quantity, image, and in_stock details, including variant_id
class ColorQuantitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    variant_id = serializers.CharField()
    color = serializers.CharField()
    quantity = serializers.IntegerField()
    image = serializers.ImageField()
    in_stock = serializers.BooleanField()

# Serializer for ProductImage model
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

# Serializer for ProductVariant model
class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)  # Serialize size details
    size_id = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), write_only=True, source='size')

    class Meta:
        model = ProductVariant
        fields = ['id', 'quantity', 'color', 'size', 'size_id', 'image', 'in_stock']

        # Serializer for ProductSizeGuide model
class ProductSizeGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeGuide
        fields = ['id', 'size', 'chest', 'length', 'sleeve']

# Serializer for grouped size details
class GroupedSizeSerializer(serializers.Serializer):
    size = SizeSerializer()  # Serialize size details
    colors = ColorQuantitySerializer(many=True)  # Serialize list of colors with quantity, image, and in_stock

# Main Product serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Serialize category details
    variants = serializers.SerializerMethodField()  # Custom method to group variants
    size_guides = ProductSizeGuideSerializer(many=True)  # Serialize size guides
    images = ProductImageSerializer(many=True)  # Serialize product images

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'short_description', 'description', 'slug', 'sku', 'category', 
            'price', 'discount_price', 'images', 'width', 
            'height', 'weight', 'depth', 'variants', 'size_guides'
        ]

    # Custom method to group variants by size and color
    def get_variants(self, obj):
        grouped_sizes = defaultdict(lambda: {'size': None, 'colors': []})

        # Group variants by size and color
        for variant in obj.variants.all():
            size_id = variant.size.id
            if grouped_sizes[size_id]['size'] is None:
                grouped_sizes[size_id]['size'] = SizeSerializer(variant.size).data

            # Append color, quantity, image, in_stock details, and variant_id
            grouped_sizes[size_id]['colors'].append({
                'id': variant.id,
                'variant_id': variant.id,  # Include variant_id here
                'color': variant.color,
                'quantity': variant.quantity,
                'image': variant.image.url,
                'in_stock': variant.in_stock
            })

        # Prepare the result list
        result = []
        for size_id, data in grouped_sizes.items():
            result.append({
                'size': data['size'],
                'colors': data['colors']
            })

        return result

    # Validate that variants and size guides are provided
    def validate(self, data):
        if not data.get('variants'):
            raise serializers.ValidationError("Product variants are required.")
        if not data.get('size_guides'):
            raise serializers.ValidationError("Product size guides are required.")
        if not data.get('images'):
            raise serializers.ValidationError("At least one product image is required.")
        return data


    # Create method to handle nested data
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


