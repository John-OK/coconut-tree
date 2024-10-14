import random
import string
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import AppUser, FormSubmission, SessionData, AnonymousUserData
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout

class FormSubmissionView(APIView):
    def post(self, request):
        form_data = request.data
        
        if request.user.is_authenticated:
            # For authenticated users
            form_submission = FormSubmission.objects.create(
                user=request.user,
                form_data=form_data
            )
        else:
            # For unauthenticated users
            session_token = request.COOKIES.get('session_token')
            if session_token:
                try:
                    session_data = SessionData.objects.get(token=session_token)
                    anonymous_user = session_data.anonymous_user
                    if not anonymous_user:
                        anonymous_user = AnonymousUserData.objects.create(session_key=request.session.session_key)
                        session_data.anonymous_user = anonymous_user
                        session_data.save()
                    
                    form_submission = FormSubmission.objects.create(
                        anonymous_user=anonymous_user,
                        form_data=form_data
                    )
                except SessionData.DoesNotExist:
                    return Response({'error': 'Invalid session'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No session found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Form submission saved', 'id': form_submission.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_session(request):
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'email': user.email,
            # Add any other user data you want to send to the frontend
        }
    })

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        
        # Get or create SessionData
        session_token = request.COOKIES.get('session_token')
        created = False
        if session_token:
            session_data, created = SessionData.objects.get_or_create(token=session_token)
        else:
            # If no session token, create a new one
            session_token = generate_token()
            session_data = SessionData.objects.create(token=session_token)
            created = True
        
        # Update session data
        session_data.user = user
        session_data.anonymous_user = None
        session_data.save()
        
        # Transfer any anonymous submissions to the logged-in user
        if not created:
            FormSubmission.objects.filter(anonymous_user__session_key=request.session.session_key).update(user=user, anonymous_user=None)
        
        response = Response({
            'message': 'User logged in successfully',
            'user': {
                'id': user.id,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
        
        # Set the session token cookie
        response.set_cookie('session_token', session_token, httponly=True, secure=True)
        
        return response

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if AppUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new user
        user = AppUser.objects.create_user(email=email, password=password)
        
        # Log the user in
        login(request, user)
        
        # Transfer session data and form submissions
        session_token = request.COOKIES.get('session_token')
        if session_token:
            try:
                session_data = SessionData.objects.get(token=session_token)
                anonymous_user = session_data.anonymous_user
                
                if anonymous_user:
                    # Transfer form submissions
                    FormSubmission.objects.filter(anonymous_user=anonymous_user).update(user=user, anonymous_user=None)
                    
                    # Update session data
                    session_data.user = user
                    session_data.anonymous_user = None
                    session_data.save()
                    
                    # Delete the anonymous user data
                    anonymous_user.delete()
                
            except SessionData.DoesNotExist:
                pass  # No session data to transfer
        
        # Return user data along with the success message
        return Response({
            'message': 'User created successfully and session data transferred',
            'user': {
                'id': user.id,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    def post(self, request):
        auth_logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)