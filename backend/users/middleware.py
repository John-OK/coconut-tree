from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import AppUser, FormSubmission, SessionData, AnonymousUserData
from django.contrib.auth.hashers import make_password

class FormSubmissionView(APIView):
    def post(self, request):
        form_data = request.data
        if request.user.is_authenticated:
            form_submission = FormSubmission.objects.create(user=request.user, form_data=form_data)
        else:
            session_data = SessionData.objects.get(token=request.COOKIES.get('session_token'))
            form_submission = FormSubmission.objects.create(anonymous_user=session_data.anonymous_user, form_data=form_data)
        return Response({'message': 'Form submission saved'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        
        session_data = SessionData.objects.get(token=request.COOKIES.get('session_token'))
        session_data.user = user
        session_data.anonymous_user = None
        session_data.save()
        
        return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if AppUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AppUser.objects.create_user(email=email, password=make_password(password))
        login(request, user)
        
        session_data = SessionData.objects.get(token=request.COOKIES.get('session_token'))
        session_data.user = user
        session_data.anonymous_user = None
        session_data.save()
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)