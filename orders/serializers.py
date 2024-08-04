from rest_framework import serializers
from .models import Order, OrderItem, ShippingMethod, Payment
from address.serializers import AddressSerializer
from coupons.serializers import CouponSerializer
from products.serializers import ProductVariantSerializer, ProductSerializer

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'duration', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'product', 'quantity', 'price_at_order_time', 'discount_price_at_order_time', 'total_price']

    def get_product(self, obj):
        return ProductSerializer(obj.product_variant.product).data

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    billing_address = AddressSerializer()
    shipping_address = AddressSerializer()
    shipping_method = ShippingMethodSerializer()
    coupon = CouponSerializer()
    is_coupon_applied = serializers.BooleanField()

    class Meta:
        model = Order
        fields = ['id', 'active', 'billing_address', 'shipping_address', 'shipping_method', 'coupon', 'subtotal', 'tax', 'shipping', 'price_before_discount', 'discount', 'total', 'is_coupon_applied', 'payment_method', 'payment_status', 'order_status', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'amount', 'status', 'stripe_charge_id']
