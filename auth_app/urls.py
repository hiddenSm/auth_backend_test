from django.urls import path
from .views import LoginView, OTPRequestView, OTPVerifyView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('otp/request/', OTPRequestView.as_view(), name='otp_request'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]