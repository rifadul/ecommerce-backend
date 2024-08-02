from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', include(router.urls)),
    path('apply-coupon/', CartViewSet.as_view({'post': 'apply_coupon'}), name='apply-coupon'),
    path('my-cart/', CartViewSet.as_view({'get': 'my_cart'}), name='my-cart'),
]
