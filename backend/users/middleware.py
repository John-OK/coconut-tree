import secrets
from django.contrib.sessions.backends.db import SessionStore
from .models import SessionData, AnonymousUserData

def generate_token(length=32):
    return secrets.token_urlsafe(length)

class SessionRestoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('session_token')

        if token:
            try:
                session_data = SessionData.objects.get(token=token)
                request.session = SessionStore(session_data.session_data)
                if hasattr(request, 'user') and request.user.is_authenticated:
                    self.associate_session_data_with_user(request, session_data)
            except SessionData.DoesNotExist:
                token = self.create_new_session(request)
        else:
            token = self.create_new_session(request)

        response = self.get_response(request)
        response.set_cookie('session_token', token, secure=True, httponly=True, max_age=3600)
        return response

    def create_new_session(self, request):
        token = generate_token()
        session_store = SessionStore()
        session_store.create()
        request.session = session_store
        anonymous_user = AnonymousUserData.objects.create(session_key=session_store.session_key)
        SessionData.objects.create(
            token=token,
            session_data=session_store.session_key,
            anonymous_user=anonymous_user
        )
        return token

    def associate_session_data_with_user(self, request, session_data):
        if hasattr(request, 'user') and request.user.is_authenticated:
            session_data.user = request.user
            session_data.anonymous_user = None
            session_data.save()