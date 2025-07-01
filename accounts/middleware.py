from django.http import HttpResponseForbidden
from django.utils.timezone import now
 
from django.conf import settings   
from django.shortcuts import redirect

class BlockBannedEmailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned_domains = ['banned.com', 'spam.com']

        if request.user.is_authenticated:
            # ❌ Block inactive users
            if not request.user.is_active:
                return HttpResponseForbidden("Access Denied: Your account is inactive.")

            # ❌ Block users with banned email domains
            email_domain = request.user.email.split('@')[-1]
            if email_domain in banned_domains:
                return HttpResponseForbidden("Access Denied: Your email domain is not allowed.")

        return self.get_response(request)


class LogLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_login = now()
            request.user.save(update_fields=['last_login'])
        return self.get_response(request)


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow unauthenticated access to login, signup, and static/admin pages
        allowed_paths = [
            settings.LOGIN_URL,
            '/accounts/signup/',
            '/admin/',
            '/static/',
        ]
        if not request.user.is_authenticated and not any(request.path.startswith(p) for p in allowed_paths):
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)

