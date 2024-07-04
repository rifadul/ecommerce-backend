from rest_framework import serializers
from .models import Module, Permission, Role

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
    
    def validate_name(self,value):
        """
        Check that the module name is unique.
        """

        if Module.objects.filter(name=value).exists():
            raise serializers.ValidationError("A module with this name already exists.")
        return value


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

    def validate_name(self,value):
        """
        Check that the permission name is unique.
        """

        if Permission.objects.filter(name=value).exists():
            raise serializers.ValidationError("A permission with this name already exists.")
        return value


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


    def validate_name(self,value):
        """
        Check that the role name is unique.
        """

        if Role.objects.filter(name=value).exists():
            raise serializers.ValidationError("A role with this name already exists.")
        return value