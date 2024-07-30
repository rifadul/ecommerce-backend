from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .models import User
from .serializers import UserCreateSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'forget_password', 'reset_password_with_token']:
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
                'access': str(refresh.access_token)
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
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        user = self.request.user
        current_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'status': 'Password has been set'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forget_password(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a password reset token
            reset_token = get_random_string(20)
            user.reset_token = reset_token
            user.save()
            # print(f'Use the following token to reset your password: {reset_token}')
            send_password_reset_email(user, reset_token)
            
            return Response({'status': 'Check your email for the password reset token'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password_with_token(self, request, *args, **kwargs):
        email = request.data.get('email')
        reset_token = request.data.get('reset_token')
        new_password = request.data.get('new_password')
        user = User.objects.filter(email=email, reset_token=reset_token).first()

        if user:
            user.set_password(new_password)
            user.reset_token = ''  # Clear the reset token after successful password reset
            user.save()
            return Response({'status': 'Password has been reset'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid token or email'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Custom action to handle multiple deletion of roles.
        This action expects a list of role IDs as query parameters.
        Example request: DELETE /api/users/delete-multiple/?ids=uuid1,uuid2,uuid3
        """
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids_list = ids.split(',')
        roles = User.objects.filter(id__in=ids_list)
        count, _ = roles.delete()
        
        if count == 0:
            return Response({"message": "No user found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": f"User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_password_reset_email(user, reset_token):
    send_mail(
        'Password Reset Request',
        f'Use the following token to reset your password: {reset_token}',
        env('EMAIL_HOST_USER'),
        [user.email],
        fail_silently=False,
    )