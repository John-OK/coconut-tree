from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    email = models.EmailField(unique=True)