from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .models import Order, OrderItem, ShippingMethod, Payment
from .serializers import OrderSerializer, PaymentSerializer, ShippingMethodSerializer
from cart.models import Cart, CartItem
from address.models import Address

class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer()
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        shipping_address_id = request.data.get('shipping_address')
        billing_address_id = request.data.get('billing_address')
        shipping_method_id = request.data.get('shipping_method')
        payment_method = request.data.get('payment_method')

        try:
            shipping_address = Address.objects.get(id=shipping_address_id)
            billing_address = Address.objects.get(id=billing_address_id)
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id)
        except Address.DoesNotExist:
            return Response({"message": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
        except ShippingMethod.DoesNotExist:
            return Response({"message": "Shipping method not found."}, status=status.HTTP_404_NOT_FOUND)

        # Determine payment status based on payment method
        payment_status = 'unpaid' if payment_method == 'cash_on_delivery' else 'paid'

        order = Order.objects.create(
            user=user,
            billing_address=billing_address,
            shipping_address=shipping_address,
            shipping_method=shipping_method,
            coupon=cart.coupon,
            subtotal=cart.subtotal,
            tax=cart.tax,
            shipping=shipping_method.price,
            discount=cart.discount,
            total=cart.total,
            price_before_discount=cart.price_before_discount,
            is_coupon_applied=cart.coupon is not None,
            payment_method=payment_method,
            payment_status=payment_status,
            active=True  # Set active to True when the order is created
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                price_at_order_time=item.product_variant.product.price,
                discount_price_at_order_time=item.product_variant.product.discount_price,
                total_price=item.total_price
            )

        cart.items.all().delete()
        cart.delete()

        serializer = self.get_serializer(order)
        return Response({"message": "Order created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            order.delete()
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_orders(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = self.get_serializer(orders, many=True)
        return Response({"message": "Orders retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.order_status not in ['processing', 'shipped']:
                return Response({"message": "Order cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
            
            order.order_status = 'cancelled'
            order.active = False
            order.save()
            return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order')
        payment_method = request.data.get('payment_method')
        amount = request.data.get('amount')
        stripe_charge_id = request.data.get('stripe_charge_id', None)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=amount,
            status='completed' if payment_method == 'stripe' else 'pending',
            stripe_charge_id=stripe_charge_id
        )

        if payment_method == 'stripe':
            order.payment_status = 'paid'
            order.save()

        serializer = self.get_serializer(payment)
        return Response({"message": "Payment created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
