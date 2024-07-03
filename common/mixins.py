from rest_framework.response import Response
from rest_framework import status

class SuccessMessageMixin:
    """
    Mixin to add dynamic success messages for create, update, delete, and read actions.
    """

    def get_model_name(self):
        return self.get_queryset().model._meta.verbose_name

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        model_name = self.get_model_name()
        return Response(
            {"message": f"{model_name.capitalize()} created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        model_name = self.get_model_name()
        return Response(
            {"message": f"{model_name.capitalize()} updated successfully", "data": serializer.data}
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        model_name = self.get_model_name()
        return Response(
            {"message": f"{model_name.capitalize()} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        model_name = self.get_model_name()
        return Response(
            {"message": f"{model_name.capitalize()} retrieved successfully", "data": serializer.data}
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        model_name = self.get_model_name()
        return Response(
            {"message": f"{model_name.capitalize()} list retrieved successfully", "data": serializer.data}
        )
