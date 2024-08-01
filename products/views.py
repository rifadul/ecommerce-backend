from rest_framework import viewsets, filters, status
from common.mixins import SuccessMessageMixin
from django_filters.rest_framework import DjangoFilterBackend
from products.filters.filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related('variants', 'size_guides', 'images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'sku']

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        products = Product.objects.filter(id__in=ids_list)
        count, _ = products.delete()
        
        if count == 0:
            return Response({"message": "No products found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "products deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
