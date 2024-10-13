from django.urls import path
from .views import FormSubmissionView, LoginView, RegisterView

urlpatterns = [
    path('submit-form/', FormSubmissionView.as_view(), name='submit_form'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]