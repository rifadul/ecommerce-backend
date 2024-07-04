from django.contrib import admin
from .models import Module, Permission, Role

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Admin view for managing Module instances.
    """
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin view for managing Permission instances.
    """
    list_display = ('name', 'codename', 'module', 'created_at', 'updated_at')
    search_fields = ('name', 'codename')
    list_filter = ('module',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin view for managing Role instances.
    """
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
