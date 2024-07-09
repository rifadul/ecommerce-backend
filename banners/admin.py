from django.contrib import admin
from django.utils.html import format_html
from .models import Banner

class CustomBannerAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'button_name', 'button_link', 'popup', 'status', 'audience',)
    list_filter = ('status', 'popup', 'audience')  # Add fields to filter by
    search_fields = ('name', 'button_name', 'button_link')  # Add fields to search by

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:45px;" />'.format(obj.image.url))
        return "-"
    
    image_tag.short_description = 'Image'

admin.site.register(Banner, CustomBannerAdmin)
