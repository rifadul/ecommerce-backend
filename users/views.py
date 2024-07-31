from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .models import User
from .serializers import UserCreateSerializer, UserSerializer, UserImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import environ
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'forget_password', 'reset_password_with_otp']:
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
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user:
            otp = get_random_string(6, allowed_chars='0123456789')
            user.email_otp = otp
            user.save()
            send_mail(
                'Password Reset OTP',
                f'Your OTP for resetting your password is {otp}',
                env('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
            return Response({'status': 'OTP sent to registered email'}, status=status.HTTP_200_OK)

        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password_with_otp(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        user = User.objects.filter(email=email, email_otp=otp).first()

        if user:
            user.set_password(new_password)
            user.email_otp = ''  # Clear the OTP after successful password reset
            user.save()
            return Response({'status': 'Password has been reset'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-multiple')
    def delete_multiple(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({"message": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        ids_list = ids.split(',')
        users = User.objects.filter(id__in=ids_list)
        count, _ = users.delete()

        if count == 0:
            return Response({"message": "No user found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_email(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get('password')
        existing_email = request.data.get('existing_email')
        new_email = request.data.get('new_email')

        if not user.check_password(current_password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.email != existing_email:
            return Response({'error': 'Invalid current email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(new_email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=new_email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_random_string(6, allowed_chars='0123456789')
        user.new_email = new_email
        user.email_otp = otp
        user.save()

        send_mail(
            'Email Change OTP',
            f'Your OTP for changing email to {new_email} is {otp}',
            env('EMAIL_HOST_USER'),
            [new_email],
            fail_silently=False,
        )

        return Response({'status': 'OTP sent to new email'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_phone(self, request, *args, **kwargs):
        user = request.user
        current_password = request.data.get('password')
        existing_phone = request.data.get('existing_phone')
        new_phone = request.data.get('new_phone')

        if not user.check_password(current_password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        if str(user.phone_number) != existing_phone:
            return Response({'error': 'Invalid current phone number'}, status=status.HTTP_400_BAD_REQUEST)

        new_phone_number = to_python(new_phone)
        if not new_phone_number.is_valid():
            return Response({'error': 'Invalid phone number format'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=new_phone).exists():
            return Response({'error': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_random_string(6, allowed_chars='0123456789')
        user.new_phone = new_phone
        user.phone_otp = otp
        user.save()

        send_mail(
            'Phone Number Change OTP',
            f'Your OTP for changing phone number to {new_phone} is {otp}',
            env('EMAIL_HOST_USER'),
            [user.email],
            fail_silently=False,
        )

        return Response({'status': 'OTP sent to registered email'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_otp(self, request, *args, **kwargs):
        user = request.user
        otp_type = request.data.get('otp_type')
        otp = request.data.get('otp')

        if otp_type == 'email':
            if user.email_otp == otp:
                user.email = user.new_email
                user.new_email = ''
                user.email_otp = ''
                user.save()
                return Response({'status': 'Email updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        elif otp_type == 'phone':
            if user.phone_otp == otp:
                user.phone_number = user.new_phone
                user.new_phone = ''
                user.phone_otp = ''
                user.save()
                return Response({'status': 'Phone number updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid OTP type'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def resend_otp(self, request, *args, **kwargs):
        user = request.user
        otp_type = request.data.get('otp_type')

        if otp_type == 'email':
            new_email = user.new_email
            otp = get_random_string(6, allowed_chars='0123456789')
            user.email_otp = otp
            user.save()

            send_mail(
                'Email Change OTP',
                f'Your OTP for changing email to {new_email} is {otp}',
                env('EMAIL_HOST_USER'),
                [new_email],
                fail_silently=False,
            )
            return Response({'status': 'OTP resent to new email'}, status=status.HTTP_200_OK)

        elif otp_type == 'phone':
            new_phone = user.new_phone
            otp = get_random_string(6, allowed_chars='0123456789')
            user.phone_otp = otp
            user.save()

            send_mail(
                'Phone Number Change OTP',
                f'Your OTP for changing phone number to {new_phone} is {otp}',
                env('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False,
            )
            return Response({'status': 'OTP resent to registered email'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Invalid OTP type'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_image(self, request, *args, **kwargs):
        user = request.user
        serializer = UserImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Image updated successfully', 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)