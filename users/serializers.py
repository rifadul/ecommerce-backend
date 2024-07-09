from rest_framework import serializers

from roles.serializers import RoleSerializer
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'image', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role'],
            image=validated_data.get('image', None),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'image', 'role']
