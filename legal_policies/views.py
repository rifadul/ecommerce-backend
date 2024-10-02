# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import PrivacyPolicy, TermsAndConditions
from .serializers import PrivacyPolicySerializer, TermsAndConditionsSerializer

class PrivacyPolicyView(generics.RetrieveAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # Assuming there's only one privacy policy entry
        return PrivacyPolicy.objects.last()

class TermsAndConditionsView(generics.RetrieveAPIView):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # Assuming there's only one terms and conditions entry
        return TermsAndConditions.objects.last()
