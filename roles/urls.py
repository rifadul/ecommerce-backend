from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModuleViewSet, PermissionViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'modules', ModuleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('roles/delete-multiple/', RoleViewSet.as_view({'delete': 'delete_multiple'}), name='role-delete-multiple'),
    # http://127.0.0.1:8000/api/roles/delete-multiple/?ids=ef7d579e-dafa-4000-a384-82e3e677fdc1,60b8e54e-a942-43b5-9dfd-9d7e3de6ec8b
]
