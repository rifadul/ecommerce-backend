from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .views import custom_404_view, custom_500_view
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('roles.urls')),
    path('api/', include('users.urls')),
    path('api/', include('banners.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('products.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('coupons.urls')),
    path('api/', include('wishlists.urls')),
    path('api/', include('address.urls')),
    path('api/', include('orders.urls')),
    path('tinymce/', include('tinymce.urls')),
]


# Custom error handlers
handler404 = custom_404_view
handler500 = custom_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)