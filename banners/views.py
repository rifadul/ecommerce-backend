from rest_framework import viewsets,status

from common.mixins import SuccessMessageMixin
from .models import Banner
from .serializers import BannerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class BannerViewSet(SuccessMessageMixin, viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

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
        roles = Banner.objects.filter(id__in=ids_list)
        count, _ = roles.delete()
        
        if count == 0:
            return Response({"message": "No banner found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"Banners deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
