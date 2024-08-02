from rest_framework import serializers
from collections import defaultdict

from categories.serializers import CategorySerializer
from .models import Cart, CartItem
from products.models import Product, ProductVariant
from products.serializers import ProductImageSerializer, SizeSerializer
from coupons.serializers import CouponSerializer

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
    coupon = CouponSerializer()
    is_coupon_applied = serializers.SerializerMethodField()
    price_before_discount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = Cart
        fields = ['id', 'items', 'coupon', 'subtotal', 'tax', 'shipping', 'price_before_discount', 'discount', 'total', 'is_coupon_applied']

    def get_is_coupon_applied(self, obj):
        return obj.coupon is not None
