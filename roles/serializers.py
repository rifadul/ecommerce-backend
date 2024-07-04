from rest_framework import serializers
from .models import Module, Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','name','codename', 'module']
        # fields = '__all__'

    def validate_name(self,value):
        """
        Check that the permission name is unique.
        """
        print('valaue',value)

        if Permission.objects.filter(name=value).exists():
            raise serializers.ValidationError("A permission with this name already exists.")
        return value
    
    def validate_codename(self,value):
        """
        Check that the permission codename is unique.
        """

        if Permission.objects.filter(codename=value).exists():
            raise serializers.ValidationError("A permission with this codename already exists.")
        return value
        

class ModuleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True, source='permission_set')
    class Meta:
        model = Module
        fields = ['id','name','permissions','created_at','updated_at']
        # fields = '__all__'
    
    def validate_name(self,value):
        """
        Check that the module name is unique.
        """

        if Module.objects.filter(name=value).exists():
            raise serializers.ValidationError("A module with this name already exists.")
        return value
    

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, write_only=True)
    permissions_display = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = ['id','name','permissions','permissions_display','created_at','updated_at']
        # fields = '__all__'


    def validate_name(self,value):
        """
        Check that the role name is unique.
        """

        if Role.objects.filter(name=value).exists():
            raise serializers.ValidationError("A role with this name already exists.")
        return value
    

    def get_permissions_display(self, obj):
        permissions = obj.permissions.all()
        grouped_permissions = {}
        for perm in permissions:
            if perm.module.name not in grouped_permissions:
                grouped_permissions[perm.module.name] = []
            grouped_permissions[perm.module.name].append(perm)
        
        result = []
        for module, perms in grouped_permissions.items():
            result.append({
                'module': module,
                'permissions': PermissionSerializer(perms, many=True).data
            })
        return result