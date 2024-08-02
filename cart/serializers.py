from rest_framework import serializers
from categories.serializers import CategorySerializer
from products.models import Product, ProductVariant
from .models import Cart, CartItem
from products.serializers import ProductImageSerializer, ProductVariantSerializer, SizeSerializer

class CartProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'short_description', 'description', 'slug', 'sku', 'category',
            'price', 'discount_price', 'width', 'height', 'weight', 'depth', 'images'
        ]

class CartProductVariantSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    in_stock = serializers.ReadOnlyField()
    size = SizeSerializer()

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'color', 'size', 'image', 'in_stock']

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = CartProductVariantSerializer()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']
