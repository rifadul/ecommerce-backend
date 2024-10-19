# coupons/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from cart.models import Cart
from common.mixins import SuccessMessageMixin
from .models import Coupon
from .serializers import CouponSerializer

class CouponViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(active=True)
    
    @action(detail=False, methods=['post'], url_path='apply-coupon', permission_classes=[IsAuthenticated])
    def apply_coupon(self, request):
        cart = Cart.objects.get(user=request.user)
        code = request.data.get('code')
        try:
            coupon = Coupon.objects.get(code=code, active=True)

            # Make sure the coupon is valid before applying it
            if not coupon.is_valid():
                return Response({"message": "Coupon is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

            if cart.coupon is None:
                cart.coupon = coupon
                cart.calculate_totals()
                return Response({"message": "Coupon applied successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "A coupon is already applied to this cart."}, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({"message": "Invalid or inactive coupon code."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-multiple',permission_classes=[IsAuthenticated])
    def delete_multiple(self, request):
        
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        coupons = Coupon.objects.filter(id__in=ids_list)
        count, _ = coupons.delete()
        
        if count == 0:
            return Response({"message": "No coupons found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Coupons deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
