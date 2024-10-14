from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

# Custom user manager
class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Authenticated user data
class AppUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AppUserManager()

    def __str__(self):
        return self.email


# Unauthenticated user data including session key
class AnonymousUserData(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_key

class SessionData(models.Model):
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey(AnonymousUserData, on_delete=models.CASCADE, null=True, blank=True)
    session_data = models.CharField(max_length=255)  # Store session key
    token = models.CharField(max_length=255, unique=True)

# Store from submissions and associate it with current user
class FormSubmission(models.Model):
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey('AnonymousUserData', on_delete=models.CASCADE, null=True, blank=True)
    form_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Form submission by {self.user or self.anonymous_user}"