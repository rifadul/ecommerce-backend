from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer
from common.mixins import SuccessMessageMixin
from rest_framework.decorators import action
from rest_framework.response import Response



# Create your views here.

class AddressViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        address = Address.objects.filter(id__in=ids_list)
        count, _ = address.delete()
        
        if count == 0:
            return Response({"message": "No address found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Addresses deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
