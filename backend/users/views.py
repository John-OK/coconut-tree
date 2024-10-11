from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, AnonymousUserData, FormSubmission
from .forms import SignUpForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Transfer anonymous submissions to the new user
            transfer_anonymous_submissions(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home')
    return render(request, 'users/delete_account.html')

def save_form_submission(request, form_data):
    if request.user.is_authenticated:
        FormSubmission.objects.create(user=request.user, form_data=form_data)
    else:
        anonymous_user, _ = AnonymousUserData.objects.get_or_create(session_key=request.session.session_key)
        FormSubmission.objects.create(anonymous_user=anonymous_user, form_data=form_data)

def transfer_anonymous_submissions(request, user):
    if not request.session.session_key:
        return
    
    anonymous_user = AnonymousUserData.objects.filter(session_key=request.session.session_key).first()
    if anonymous_user:
        FormSubmission.objects.filter(anonymous_user=anonymous_user).update(user=user, anonymous_user=None)
        anonymous_user.delete()