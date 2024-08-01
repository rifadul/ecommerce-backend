from rest_framework import serializers
from collections import defaultdict
from categories.models import Category
from .models import Product, ProductVariant, ProductSizeGuide, ProductImage, Size
from categories.serializers import CategorySerializer

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'size']

class SizeQuantitySerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    size_id = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField()
    in_stock = serializers.BooleanField()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), write_only=True, source='size')

    class Meta:
        model = ProductVariant
        fields = ['id', 'quantity', 'color', 'size', 'size_id', 'image', 'in_stock']

class ProductSizeGuideSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), write_only=True, source='size')

    class Meta:
        model = ProductSizeGuide
        fields = ['id', 'size', 'size_id', 'chest', 'length', 'sleeve']

class GroupedColorSerializer(serializers.Serializer):
    color = serializers.CharField()
    image = serializers.ImageField()
    sizes = SizeQuantitySerializer(many=True)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    variants = serializers.SerializerMethodField()
    size_guides = ProductSizeGuideSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'short_description', 'description', 'slug', 'sku', 'category',
            'price', 'discount_price', 'images', 'width',
            'height', 'weight', 'depth', 'variants', 'size_guides'
        ]

    def get_variants(self, obj):
        request = self.context.get('request')
        grouped_colors = defaultdict(lambda: {'color': None, 'image': None, 'sizes': []})
        
        for variant in obj.variants.all():
            color = variant.color
            image_url = request.build_absolute_uri(variant.image.url) if variant.image and request else None
            if grouped_colors[color]['color'] is None:
                grouped_colors[color]['color'] = color
                grouped_colors[color]['image'] = image_url
            grouped_colors[color]['sizes'].append({
                'variant_id': variant.id,
                'size_id': variant.size.id,
                'size': variant.size.size,
                'quantity': variant.quantity,
                'in_stock': variant.in_stock
            })
        
        result = []
        for color, data in grouped_colors.items():
            result.append({
                'color': data['color'],
                'image': data['image'],
                'sizes': data['sizes']
            })
        
        return result

    def validate(self, data):
        if not data.get('variants'):
            raise serializers.ValidationError("Product variants are required.")
        if not data.get('size_guides'):
            raise serializers.ValidationError("Product size guides are required.")
        if not data.get('images'):
            raise serializers.ValidationError("At least one product image is required.")
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
