# wishlist/serializers.py
from rest_framework import serializers

from products.models import Product
from .models import WishList
from products.serializers import ProductSerializer

class WishListSerializer(serializers.ModelSerializer):
     product = ProductSerializer(read_only=True)
     product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())

     class Meta:
        model = WishList
        fields = ['id', 'user', 'product', 'product_id', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

     def validate(self, data):
         user = self.context['request'].user
         product = data.get('product')
         if WishList.objects.filter(user=user, product=product).exists():
               raise serializers.ValidationError("This product is already in your wishlist.")
         return data
