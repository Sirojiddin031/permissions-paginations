from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app_users.utils import generate_verification_code, send_verification_email
from app_users.models import ProfileModel
from app_users.serializers import RegisterSerializer, UserProfileSerializer, UpdatePasswordSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = generate_verification_code()

            profile, created = ProfileModel.objects.get_or_
            create(user=user)
            profile.verification_code = code
            profile.save()

            send_verification_email(user.email, code)
            return Response({"message": "Tasdiqlash kodi yuborildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "Bu endpoint faqat POST usuli bilan ishlaydi."}, status=405)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        user = get_object_or_404(User, email=email)
        profile = user.profile
        if profile.verification_code == code:
            user.is_active = True
            user.save()
            return Response({"message": "Email tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response({"error": "Noto‘g‘ri kod"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data


class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "Eski parol noto‘g‘ri"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password1'])
            user.save()
            return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenBlacklistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout muvaffaqiyatli bajarildi"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Noto‘g‘ri token"}, status=status.HTTP_400_BAD_REQUEST)



class UsersRootAPIView(APIView):
    def get(self, request):
        return Response({"message": "Users API is working!"})
