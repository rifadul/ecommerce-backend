from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)

        def validate(self, data):
         user = self.context['request'].user
         name = data.get('name')
         print('Name is ',name)
         if Address.objects.filter(user=user, name=name).exists():
               raise serializers.ValidationError("With name {name} already added in your address list.")
         return data
