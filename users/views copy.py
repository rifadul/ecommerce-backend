from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from common.mixins import SuccessMessageMixin
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(SuccessMessageMixin,generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(SuccessMessageMixin,generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        user = User.objects.filter(email=email_or_phone).first() or User.objects.filter(phone_number=email_or_phone).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ChangePasswordView(SuccessMessageMixin,generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if not user.check_password(password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'status': 'password set'}, status=status.HTTP_200_OK)

class ResetPasswordView(SuccessMessageMixin,generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Implement email sending logic with reset link or OTP
            return Response({'status': 'Check your email for reset instructions'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
