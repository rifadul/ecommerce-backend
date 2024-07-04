from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Module, Permission, Role
from .serializers import ModuleSerializer, PermissionSerializer, RoleSerializer
from common.mixins import SuccessMessageMixin
from rest_framework.filters import SearchFilter

class ModuleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Module.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name']

class PermissionViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Permission.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # permission_classes = [IsAuthenticated]


class RoleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Role, including bulk deletion.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name']
    # permission_classes = [IsAuthenticated]