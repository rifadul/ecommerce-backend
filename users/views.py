from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .models import User
from .serializers import UserCreateSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import random
import string
from django.core.mail import send_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'reset_password']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        password = request.data.get('password')
        new_password = request.data.get('new_password')

        if not user.check_password(password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'status': 'password set'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a temporary password or reset link
            temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.set_password(temporary_password)
            user.save()
            
            # Send the temporary password to the user's email
            send_mail(
                'Password Reset Request',
                f'Your temporary password is {temporary_password}',
                'rifadul1618@gmail.com',
                [user.email],
                fail_silently=False,
            )
            
            return Response({'status': 'Check your email for the temporary password'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
