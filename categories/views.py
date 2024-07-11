from rest_framework import viewsets, status
from common.mixins import SuccessMessageMixin
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(SuccessMessageMixin,viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('parent', 'subcategories')
    serializer_class = CategorySerializer

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of Category.
        This action expects a list of role IDs as query parameters.
        Example request: DELETE /api/category/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        categories = Category.objects.filter(id__in=ids_list)
        count, _ = categories.delete()
        
        if count == 0:
            return Response({"message": "No Category found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Categories deleted successfully"}, status=status.HTTP_204_NO_CONTENT)