# coupons/serializers.py
from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'active', 'categories', 'min_purchase_amount', 'max_discount_amount']
