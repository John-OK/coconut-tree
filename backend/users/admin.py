from django.contrib import admin
from .models import CustomUser, AnonymousUserData, FormSubmission

admin.site.register(CustomUser)
admin.site.register(AnonymousUserData)
admin.site.register(FormSubmission)