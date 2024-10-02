from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from common.mixins import SuccessMessageMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related('parent', 'subcategories')
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        # Get the 'children_of' query parameter from the request
        children_of_slug = request.query_params.get('children_of', None)

        # If 'children_of' is a falsy value, return all categories
        if not children_of_slug:
            # Default behavior to get all categories
            queryset = self.filter_queryset(self.get_queryset())

            # Apply pagination for the default list
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If 'children_of' is provided and valid, get the category by slug
        parent_category = get_object_or_404(Category, slug=children_of_slug)
        # Filter to get all child categories of the parent category
        queryset = parent_category.subcategories.all()

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not applicable, return all child categories
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": f"Child categories of '{parent_category.name}' retrieved successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        categories = Category.objects.filter(id__in=ids_list)
        count, _ = categories.delete()
        
        if count == 0:
            return Response({"message": "No Category found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Categories deleted successfully"}, status=status.HTTP_204_NO_CONTENT)