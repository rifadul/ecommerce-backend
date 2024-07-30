from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        # name = data.get('name')
        # if Address.objects.filter(user=user, name=name).exists():
        #     raise serializers.ValidationError(f"Address with name '{name}' already exists in your address list.")
        return data       

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data.get('defaultAddress', False):
            Address.objects.filter(user=user, defaultAddress=True).update(defaultAddress=False)
        elif not Address.objects.filter(user=user, defaultAddress=True).exists():
            validated_data['defaultAddress'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if validated_data.get('defaultAddress', False):
            Address.objects.filter(user=user, defaultAddress=True).update(defaultAddress=False)
        updated_instance = super().update(instance, validated_data)
        
        # Ensure at least one default address exists
        if not Address.objects.filter(user=user, defaultAddress=True).exists():
            first_address = Address.objects.filter(user=user).first()
            if first_address:
                first_address.defaultAddress = True
                first_address.save()
                
        return updated_instance
