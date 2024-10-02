# urls.py
from django.urls import path
from .views import PrivacyPolicyView, TermsAndConditionsView

urlpatterns = [
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),
]
