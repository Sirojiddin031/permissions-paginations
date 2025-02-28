from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app_users.views import (
    RegisterAPIView, LoginAPIView, VerifyEmailAPIView,
    TokenBlacklistView, UserProfileAPIView, UpdatePasswordAPIView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('me/', UserProfileAPIView.as_view(), name='me'),
    path('update/password/', UpdatePasswordAPIView.as_view(), name='update_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
