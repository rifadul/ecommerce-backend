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
    ViewSet for handling CRUD operations for Role, including bulk deletion.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [SearchFilter]  # Add search filter
    search_fields = ['name']
    # permission_classes = [IsAuthenticated]