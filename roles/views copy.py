from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Module, Permission, Role
from .serializers import ModuleSerializer, PermissionSerializer, RoleSerializer
from common.mixins import SuccessMessageMixin
from rest_framework.decorators import api_view

class ModuleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Module.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class PermissionViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Permission.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

# class RoleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
#     """
#     ViewSet for handling CRUD operations for Role, including bulk deletion.
#     """
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

#     @action(detail=False, methods=['delete'])
#     def delete_multiple(self, request):
#         """
#         Custom action to handle bulk deletion of roles.
#         This action expects a list of role IDs in the request data.
#         Example request data: {"ids": ["uuid1", "uuid2", ...]}
#         """
#         ids = request.data.get('ids', [])
#         roles = Role.objects.filter(id__in=ids)
#         count, _ = roles.delete()
#         return Response({"message": f"Deleted {count} roles."}, status=status.HTTP_204_NO_CONTENT)
    
class RoleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations for Role, including bulk deletion.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    # @action(detail=False, methods=['delete'])
    # def delete_multiple(self, request):
    #     """
    #     Custom action to handle bulk deletion of roles.
    #     This action expects a list of role IDs as query parameters.
    #     Example request: DELETE /api/roles/delete-multiple/?ids=uuid1,uuid2,uuid3
    #     """
    #     print('I am call',self.request.query_params.get('ids'))
    #     ids = request.query_params.get('ids')
    #     print('ids', ids)
    #     if not ids:
    #         return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     ids_list = ids.split(',')
    #     roles = Role.objects.filter(id__in=ids_list)
    #     count, _ = roles.delete()
        
    #     if count == 0:
    #         return Response({"message": "No roles found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
    #     return Response({"message": f"Deleted {count} roles."}, status=status.HTTP_204_NO_CONTENT)

# class RoleViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
#     """
#     ViewSet for handling CRUD operations for Role, including bulk deletion.
#     """
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

#     @action(detail=False, methods=['post'])
#     def delete_multiple(self, request):
#         """
#         Custom action to handle bulk deletion of roles.
#         This action expects a list of role IDs in the request body.
#         Example request data: {"ids": ["uuid1", "uuid2", ...]}
#         """
#         ids = request.data.get('ids', [])
#         if not ids:
#             return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
#         roles = Role.objects.filter(id__in=ids)
#         count, _ = roles.delete()
        
#         if count == 0:
#             return Response({"message": "No roles found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response({"message": f"Deleted {count} roles."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_multiple_roles(request):
    print('I am heer')
    ids = request.query_params.get('ids')
    if not ids:
        return Response({'error': 'No ids provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    id_list = ids.split(',')
    roles_to_delete = Role.objects.filter(id__in=id_list)

    if not roles_to_delete.exists():
        return Response({'error': 'No roles found with the provided ids'}, status=status.HTTP_404_NOT_FOUND)
    
    deleted_count = roles_to_delete.delete()
    return Response({'message': f'{deleted_count[0]} roles deleted successfully'}, status=status.HTTP_200_OK)