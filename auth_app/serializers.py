from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
import random, string

from .models import CustomUser, OTPCode


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        user = authenticate(username=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("شماره موبایل یا رمز عبور اشتباه است.")
        return data

class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("این شماره قبلاً ثبت شده است. لطفاً وارد شوید.")
        return value

    def create_otp(self):
        phone_number = self.validated_data['phone_number']
        code = ''.join(random.choices(string.digits, k=6))
        OTPCode.objects.create(phone_number=phone_number, code=code)
        return code

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        code = data.get('code')

        otp = OTPCode.objects.filter(phone_number=phone_number, code=code).first()
        if not otp or not otp.is_valid():
            raise serializers.ValidationError("کد نامعتبر یا منقضی شده است.")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance