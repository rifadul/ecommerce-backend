from django.contrib import admin
from django.utils.html import format_html
from .models import Category

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'parent', 'slug', 'description',)
    list_filter = ('name', 'slug',)  # Add fields to filter by
    search_fields = ('name', 'parent__name')
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('parent')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        return "-"

    image_tag.short_description = 'Image'

admin.site.register(Category, CustomCategoryAdmin)
