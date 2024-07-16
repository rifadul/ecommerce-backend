# cart/serializers.py
from rest_framework import serializers

from categories.serializers import CategorySerializer
from products.models import Product, ProductVariant
from .models import Cart, CartItem
from products.serializers import ProductImageSerializer, ProductVariantSerializer


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
    product = CartProductSerializer(read_only=True)  # Include the limited product serializer for cart
    in_stock = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'quantity', 'color', 'size', 'image', 'in_stock']

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = CartProductVariantSerializer()  # Use the custom serializer for cart items
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
