from django.urls import path
from .views import LoginView, RegisterView, LogoutView, check_session, FormSubmissionView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/check-session/', check_session, name='check_session'),
    path('api/submit-form/', FormSubmissionView.as_view(), name='submit_form'),
]