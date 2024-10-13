from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Authenticated user data
class AppUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    email = models.EmailField(unique=True)

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
    session_data = models.JSONField()
    token = models.CharField(max_length=255, unique=True)

# Store from submissions and associate it with current user
class FormSubmission(models.Model):
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey('AnonymousUserData', on_delete=models.CASCADE, null=True, blank=True)
    form_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Form submission by {self.user or self.anonymous_user}"



# class TempFormSubmission(models.Model):
#     user = models.ForeignKey('AppUser', on_delete=models.CASCADE, null=True, blank=True)
#     form_data = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

# Store from submissions and associate it with current user
# class FormSubmission(models.Model):
#     session_data = models.ForeignKey('SessionData', on_delete=models.CASCADE, null=True, blank=True)
#     form_data = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Form submission by {self.session_data.user or self.session_data.anonymous_user}"