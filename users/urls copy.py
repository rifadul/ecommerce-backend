from django.urls import path, include
from .views import RegisterView, LoginView, ChangePasswordView, ResetPasswordView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users/', UserListView)
router.register(r'register/', RegisterView)
router.register(r'login/', LoginView)
router.register(r'change-password/', ChangePasswordView)
router.register(r'reset-password/', ResetPasswordView)
router.register(r'token/', TokenObtainPairView)
router.register(r'token/refresh/', TokenRefreshView)


urlpatterns = [
    path('', include(router.urls)),
]


# urlpatterns = [
#     path('users/', UserListView.as_view(), name='user-list'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('change-password/', ChangePasswordView.as_view(), name='change_password'),
#     path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
