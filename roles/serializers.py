from rest_framework import serializers
from .models import Module, Permission, Role

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


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