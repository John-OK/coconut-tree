from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # 'username' is required here for the admin panel, for deployment
    # it should be removed, leaving an empty list
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Email & Password are required by default.

class AnonymousUserData(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

class FormSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey(AnonymousUserData, on_delete=models.CASCADE, null=True, blank=True)
    form_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


