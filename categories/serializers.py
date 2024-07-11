from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'subcategories', 'image']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

    def validate(self, data):
        parent = data.get('parent')
        if self.instance and parent:
            ancestor = parent
            while ancestor:
                if ancestor == self.instance:
                    raise serializers.ValidationError("A category cannot be a subcategory of its own subcategory.")
                ancestor = ancestor.parent
        return data
