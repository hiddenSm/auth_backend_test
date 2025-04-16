from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.phone_number


class OTPCode(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300 and not self.is_used

    def __str__(self):
        return f"{self.phone_number} - {self.code}"


class Block(models.Model):
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    blocked_until = models.DateTimeField()
    reason = models.CharField(max_length=100)

    def is_blocked(self):
        return self.blocked_until > timezone.now()

    def __str__(self):
        return f"{self.ip_address or self.phone_number} - Blocked until {self.blocked_until}"