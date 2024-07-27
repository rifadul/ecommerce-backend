# wishlist/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from common.mixins import SuccessMessageMixin
from .serializers import WishListSerializer
from .models import WishList

class WishlistViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of wishlist.
        This action expects a list of role IDs as query parameters.
        Example request: DELETE /api/wishlist/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        wishlists = WishList.objects.filter(id__in=ids_list)
        count, _ = wishlists.delete()
        
        if count == 0:
            return Response({"message": "No wishlist found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Wishlist deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
