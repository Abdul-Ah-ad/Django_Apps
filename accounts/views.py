from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, EditProfileForm #created by me
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages  
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    try:
        if request.method == 'POST':
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully!")  #  Added success message
                return redirect('profile')
            else:
                messages.error(request, "Please fix the errors below.")  #  Inform user if form invalid
        else:
            form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Signup error: {e}")
        return redirect('signup')


def login_view(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Invalid logincredentials.")  #  Inform user if form invalid
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Login error: {e}")
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required#protected 
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': getattr(request.user, 'profile', None),
    })

@login_required
def edit_profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user, profile=profile)
        if form.is_valid():
            try:
                form.save(user, profile)
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            except Exception as e:
                logger.exception("Error during profile update")
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=user, profile=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile': profile
    })