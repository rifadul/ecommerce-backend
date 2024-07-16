# products/views.py
from rest_framework import viewsets, filters, status
from common.mixins import SuccessMessageMixin
from django_filters.rest_framework import DjangoFilterBackend
from products.filters.filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter  # Use the custom filter set
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'sku']

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of products.
        This action expects a list of Products IDs as query parameters.
        Example request: DELETE /api/products/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        products = Product.objects.filter(id__in=ids_list)
        count, _ = products.delete()
        
        if count == 0:
            return Response({"message": "No products found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"products deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
