import stripe
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Order, OrderItem, ShippingMethod, Payment
from .serializers import OrderSerializer, PaymentSerializer, ShippingMethodSerializer
from cart.models import Cart, CartItem
from address.models import Address
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
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

        payment_status = 'unpaid' if payment_method == 'cash_on_delivery' else 'pending'

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
            active=True
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

        if payment_method == 'stripe':
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Order {}'.format(order.id),
                            },
                            'unit_amount': int(order.total * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=settings.STRIPE_SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=settings.STRIPE_CANCEL_URL,
                    metadata={'order_id': str(order.id)}
                )

                Payment.objects.create(
                    order=order,
                    payment_method='stripe',
                    amount=order.total,
                    status='pending',
                    stripe_payment_intent_id=session.payment_intent  # Ensure this is correctly set
                )

                return Response({
                    "message": "Order created successfully.",
                    "data": OrderSerializer(order).data,
                    "payment_url": session.url
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_object()
            if order.user != request.user:
                return Response({"message": "You do not have permission to cancel this order."}, status=status.HTTP_403_FORBIDDEN)
            if order.order_status not in ['processing', 'shipped']:
                return Response({"message": "Order cannot be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
            
            order.order_status = 'cancelled'
            order.active = False
            order.save()
            return Response({"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)
        except NotFound:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def create_payment_intent(self, request, pk=None):
        try:
            order = self.get_object()
            if order.payment_status == 'paid':
                return Response({"message": "Order is already paid."}, status=status.HTTP_400_BAD_REQUEST)
            
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),
                currency='usd',
                metadata={'order_id': order.id}
            )
            
            Payment.objects.create(
                order=order,
                payment_method='stripe',
                amount=order.total,
                status='pending',
                stripe_payment_intent_id=intent['id']
            )

            return Response({
                'client_secret': intent['client_secret'],
                'payment_intent_id': intent['id']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def payment_success(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({"message": "Session ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent_id = session.payment_intent
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            order = payment.order
            serializer = OrderSerializer(order)
            return Response({"success": True, "order": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

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

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def handle_webhook(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            logger.error('Invalid payload')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            logger.error('Invalid signature')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            logger.info('Received checkout.session.completed event')
            session = event['data']['object']
            payment_intent_id = session.get('payment_intent')
            try:
                payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
                payment.status = 'completed'
                payment.save()
                payment.order.payment_status = 'paid'
                payment.order.save()
            except Payment.DoesNotExist:
                logger.error('Payment not found for payment_intent_id: %s', payment_intent_id)

        return Response(status=status.HTTP_200_OK)
