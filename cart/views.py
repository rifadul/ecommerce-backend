from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductVariant
from coupons.models import Coupon

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.calculate_totals()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.calculate_totals()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_variant_id = request.data.get('product_variant')
        quantity = request.data.get('quantity', 1)

        try:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"message": "Product variant not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the cart item already exists
        existing_cart_item = CartItem.objects.filter(cart=cart, product_variant=product_variant).first()
        if existing_cart_item:
            return Response(
                {"message": f"Product '{product_variant.product.name}' already exists in the cart."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if product_variant.quantity < int(quantity):
            return Response(
                {"message": f"Product '{product_variant.product.name}' does not have {quantity} units in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = CartItem.objects.create(cart=cart, product_variant=product_variant, quantity=int(quantity))
        cart_item.save()
        cart.calculate_totals()

        serializer = self.get_serializer(cart_item)
        return Response({"message": "Product added to cart successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, id=kwargs['pk'])
        except CartItem.DoesNotExist:
            return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity', None)
        if quantity is None:
            raise ValidationError({"message": "A valid integer greater than 0 is required."})

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError({"message": "A valid integer greater than 0 is required."})

        if cart_item.product_variant.quantity < quantity:
            return Response(
                {"message": f"Product '{cart_item.product_variant.product.name}' does not have {quantity} units in stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()
        cart.calculate_totals()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, id=kwargs['pk'])
        except CartItem.DoesNotExist:
            return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        # Check if the cart has any items left
        if not CartItem.objects.filter(cart=cart).exists():
            cart.delete()
            return Response({"message": "Cart and its items deleted."}, status=status.HTTP_204_NO_CONTENT)

        cart.calculate_totals()
        return Response({"message": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
