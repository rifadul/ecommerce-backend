from django.contrib import admin
from django.utils.html import format_html
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'first_name', 'last_name', 'email', 'phone_number',  'role', 'is_active', 'is_staff')
    search_fields = ('name',)
    list_filter = ('is_active', 'is_staff', 'role')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        return "-"
    
    image_tag.short_description = 'Image'

admin.site.register(User, CustomUserAdmin)
