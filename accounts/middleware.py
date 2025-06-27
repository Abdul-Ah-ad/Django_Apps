from django.http import HttpResponseForbidden
from django.utils.timezone import now
    
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
        if not request.user.is_authenticated and not request.path.startswith('/admin/'):
            return redirect('/admin/login/')
        return self.get_response(request)

