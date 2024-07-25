# wishlist/serializers.py
from rest_framework import serializers
from .models import Wishlist, WishlistItem
from products.serializers import ProductVariantSerializer, ProductSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    # product_variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product_variant', write_only=True)

    class Meta:
        model = WishlistItem
        fields = '__all__'
        # fields = ['id', 'product_variant', 'product_variant_id']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'items']
