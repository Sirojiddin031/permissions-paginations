from django.contrib.auth.models import User
from rest_framework import serializers

from app_users.models import ProfileModel
from app_users.utils import generate_verification_code, send_verification_email


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """Parollarni tekshirish va mavjud foydalanuvchilarni tekshirish"""
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Bu username allaqachon band"})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Bu email allaqachon ishlatilgan"})

        return data

    def create(self, validated_data):
        """Foydalanuvchini yaratish va emailga tasdiqlash kodini yuborish"""
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password1'],
            is_active=False
        )

        verification_code = generate_verification_code()
        profile, created = ProfileModel.objects.get_or_create(user=user)
        profile.verification_code = verification_code
        profile.save()

        send_verification_email(user.email, verification_code)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['avatar', 'bio']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})
        return data
