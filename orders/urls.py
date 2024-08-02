from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, PaymentViewSet, ShippingMethodViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'shipping-methods', ShippingMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', PaymentViewSet.as_view({'post': 'handle_webhook'}), name='stripe-webhook'),
]
