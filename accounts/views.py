import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseServerError
from django.shortcuts import redirect, render

from accounts.forms import EditProfileForm, SignupForm

logger = logging.getLogger(__name__)

def handle_form(request, form_class, template_name, success_url, success_message, *,
                instance=None, extra_context=None, commit_callback=None, **form_kwargs):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance, **form_kwargs)
        if form.is_valid():
            try:
                if commit_callback:
                    commit_callback(form)
                else:
                    form.save()
                messages.success(request, success_message)
                return redirect(success_url)
            except ValueError as ve:
                logger.warning(f"Validation error: {ve}")
                messages.error(request, f"Validation error: {ve}")
            except Exception as e:
                logger.exception('Unexpected error during form processing')
                return HttpResponseServerError("An unexpected error occurred.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = form_class(instance=instance, **form_kwargs)

    context = {'form': form}
    if extra_context:
        context.update(extra_context)

    return render(request, template_name, context)



def signup_view(request):
    return handle_form(
        request,
        form_class=SignupForm,
        template_name='accounts/signup.html',
        success_url='profile',
        success_message='Account created successfully!',
    )


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

    def save_form(form):
        form.save(user, profile)

    return handle_form(
        request,
        form_class=EditProfileForm,
        template_name='accounts/edit_profile.html',
        success_url='profile',
        success_message='Profile updated successfully.',
        instance=user,
        form_kwargs={'profile': profile},
        extra_context={'profile': profile},
        commit_callback=save_form
    )
