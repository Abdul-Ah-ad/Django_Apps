import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseServerError
from django.shortcuts import redirect, render

from .forms import EditProfileForm, SignupForm

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
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
            except ValueError as ve:
                logger.warning(f"Validation error during profile update: {ve}")
                messages.error(request, f"Validation error: {ve}")
            except Exception as e:
                logger.exception('Unexpected error during profile update')
                return HttpResponseServerError("An unexpected error occurred.")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=user, profile=profile)

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'profile': profile
    })
