# wishlist/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from common.mixins import SuccessMessageMixin
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer

class WishlistViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistItemSerializer(data=request.data)
        if serializer.is_valid():
            product_variant_id = request.data.get('product_variant_id')
            WishlistItem.objects.create(wishlist=wishlist, product_variant_id=product_variant_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='remove-item')
    def remove_item(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_variant_id = request.data.get('product_variant_id')
        try:
            item = WishlistItem.objects.get(wishlist=wishlist, product_variant_id=product_variant_id)
            item.delete()
            return Response({"message": "Item removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
        except WishlistItem.DoesNotExist:
            return Response({"message": "Item not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)
