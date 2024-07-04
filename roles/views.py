from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Module, Permission, Role
from .serializers import ModuleSerializer, PermissionSerializer, RoleSerializer
from common.mixins import SuccessMessageMixin
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

class ModuleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Module.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name']
    # permission_classes = [IsAuthenticated]

class PermissionViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Permission.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name','codename']
    # permission_classes = [IsAuthenticated]


class RoleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Role, including multiple deletion.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name']
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of roles.
        This action expects a list of role IDs as query parameters.
        Example request: DELETE /api/roles/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        roles = Role.objects.filter(id__in=ids_list)
        count, _ = roles.delete()
        
        if count == 0:
            return Response({"message": "No roles found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Roles deleted successfully"}, status=status.HTTP_204_NO_CONTENT)