from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now


class BlockBannedEmailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned_domains = ['banned.com', 'spam.com']

        if request.user.is_authenticated:
            if not request.user.is_active:
                return HttpResponseForbidden("Access Denied: Your account is inactive.")

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


class CustomAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        allowed_paths = [
            settings.LOGIN_URL,
            '/accounts/signup/',
            '/admin/',
            settings.STATIC_URL,
            settings.MEDIA_URL,
        ]

        if (
            not request.user.is_authenticated
            and not any(request.path.startswith(path) for path in allowed_paths)
        ):
            return redirect(settings.LOGIN_URL)
        
