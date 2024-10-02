from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from common.mixins import SuccessMessageMixin
from django_filters.rest_framework import DjangoFilterBackend
from products.filters.filters import ProductFilter
from utils.utils import ColorUtils
from .models import Product, ProductVariant
from .serializers import ProductReviewSerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Min, Max, Avg

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
    
    @action(detail=False, methods=['post'], url_path='add-review', permission_classes=[IsAuthenticated])
    def add_review(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Copy request data to avoid modifying the original request
        review_data = request.data.copy()
        serializer = ProductReviewSerializer(data=review_data, context={'request': request})
        
        if serializer.is_valid():
            try:
                serializer.save(user=request.user, product=product)
                return Response(
                    {
                        "message": "Review added successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {
                        "message": "You have already added a review for this product."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='colors')
    def get_all_colors(self, request):
        """
        Custom action to get all unique colors used in product variants.
        Example request: GET /api/products/colors/
        """
        unique_colors = ProductVariant.objects.values_list('color', flat=True).distinct()

        # Create a list of color data with both the color code and name
        color_data = []
        for color_code in unique_colors:
            color_name = ColorUtils.get_color_name_from_hex(color_code)  # Use the utility function
            color_data.append({
                "code": color_code,
                "name": color_name
            })

        return Response(color_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='price-stats')
    def get_price_stats(self, request):
        """
        Custom action to get minimum, maximum, and average price of all products.
        Example request: GET /api/products/price-stats/
        """
        stats = Product.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
        
        # Handle case where no products exist in the database
        stats = {
            'min_price': stats['min_price'] if stats['min_price'] is not None else 0,
            'max_price': stats['max_price'] if stats['max_price'] is not None else 0,
            'avg_price': stats['avg_price'] if stats['avg_price'] is not None else 0
        }

        return Response(stats, status=status.HTTP_200_OK)
