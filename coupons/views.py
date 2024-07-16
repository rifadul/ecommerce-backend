# coupons/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from common.mixins import SuccessMessageMixin
from .models import Coupon
from .serializers import CouponSerializer

class CouponViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(active=True)

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of coupons.
        This action expects a list of coupon IDs as query parameters.
        Example request: DELETE /api/coupons/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        coupons = Coupon.objects.filter(id__in=ids_list)
        count, _ = coupons.delete()
        
        if count == 0:
            return Response({"message": "No coupons found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Coupons deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
