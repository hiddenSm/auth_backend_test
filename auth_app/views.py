from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login
from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from .serializers import LoginSerializer, OTPSerializer, OTPVerifySerializer, UserProfileSerializer
from .models import CustomUser, OTPCode, Block


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        phone_number = request.data.get('phone_number')

        # block check
        block = Block.objects.filter(
            Q(ip_address=ip) | Q(phone_number=phone_number),
            blocked_until__gt=timezone.now()
        ).order_by('-blocked_until').first()
        if block:
            return Response({"error": f"phone number {phone_number} is blocked until {block.blocked_until}."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(phone_number=serializer.validated_data['phone_number'])
            login(request, user)
            return Response({"message": f"{phone_number} is logged in."}, status=status.HTTP_200_OK)
        else:
            # failed attempt record and block check
            failed_attempts = Block.objects.filter(
                ip_address=ip, phone_number=phone_number, reason="login_failure"
            ).count()
            if failed_attempts >= 2:
                Block.objects.create(
                    ip_address=ip,
                    phone_number=phone_number,
                    blocked_until=timezone.now() + timedelta(hours=1),
                    reason="login_failure"
                )
                return Response({"error": f"phone number {phone_number} is blocked for 1 hour becouse of 3 failled attemp."}, status=status.HTTP_403_FORBIDDEN)
            Block.objects.create(
                ip_address=ip,
                phone_number=phone_number,
                blocked_until=timezone.now(),
                reason="login_failure"
            )
            return Response({"error": f"Logging in with phone number {phone_number} is failled: wronge phonenuber or password."}, status=status.HTTP_400_BAD_REQUEST)

class OTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        phone_number = request.data.get('phone_number')

        # block check
        block = Block.objects.filter(
            Q(ip_address=ip) | Q(phone_number=phone_number),
            blocked_until__gt=timezone.now()
        ).order_by('-blocked_until').first()
        if block:
            return Response({"error": f"phone number {phone_number} is blocked until {block.blocked_until}."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.create_otp()
            return Response({"message": f"OTP code for phone number {phone_number}: {code}"}, status=status.HTTP_200_OK)
        return Response({"error": f"OTP code request for {phone_number} is failled: {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        phone_number = request.data.get('phone_number')

        # block check
        block = Block.objects.filter(
            Q(ip_address=ip) | Q(phone_number=phone_number),
            blocked_until__gt=timezone.now()
        ).order_by('-blocked_until').first()
        if block:
            return Response({"error": f"phone number {phone_number} is blocked until {block.blocked_until}."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            otp = OTPCode.objects.filter(phone_number=phone_number, code=serializer.validated_data['code']).first()
            if not otp or not otp.is_valid():
                # failed attempt record
                failed_attempts = Block.objects.filter(
                    ip_address=ip, phone_number=phone_number, reason="otp_failure"
                ).count()
                if failed_attempts >= 2:
                    Block.objects.create(
                        ip_address=ip,
                        phone_number=phone_number,
                        blocked_until=timezone.now() + timedelta(hours=1),
                        reason="otp_failure"
                    )
                    return Response({"error": f"phone number {phone_number} is blocked for 1 hour becouse of 3 failled attemp."}, status=status.HTTP_403_FORBIDDEN)
                Block.objects.create(
                    ip_address=ip,
                    phone_number=phone_number,
                    blocked_until=timezone.now(),
                    reason="otp_failure"
                )
                return Response({"error": f"verifying OTP for {phone_number} is failled: invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

            otp.is_used = True
            otp.save()

            # user existence check
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                return Response({"error": f"phone number {phone_number} is registered, please login."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.create_user(
                    username=phone_number,
                    phone_number=phone_number,
                    password=None
                )
                login(request, user)
                return Response({"message": f"verifying OTP for {phone_number} is susuccessful. please complete your profile."}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": f"error in registering{phone_number}. please try again."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # failed attempt record
            failed_attempts = Block.objects.filter(
                ip_address=ip, phone_number=phone_number, reason="otp_failure"
            ).count()
            if failed_attempts >= 2:
                Block.objects.create(
                    ip_address=ip,
                    phone_number=phone_number,
                    blocked_until=timezone.now() + timedelta(hours=1),
                    reason="otp_failure"
                )
                return Response({"error": f"phone number {phone_number} is blocked for 1 hour becouse of 3 failled attemp."}, status=status.HTTP_403_FORBIDDEN)
            Block.objects.create(
                ip_address=ip,
                phone_number=phone_number,
                blocked_until=timezone.now(),
                reason="otp_failure"
            )
            return Response({"error": f"verifying OTP for {phone_number} is failled: invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": f"please enter with {request.data.get('phone_number', 'نامشخص')} first."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{request.user.phone_number} profile is susuccessfully complete."}, status=status.HTTP_200_OK)
        return Response({"error": f"{request.user.phone_number} profile completing is failled  ناموفق بود: {serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
