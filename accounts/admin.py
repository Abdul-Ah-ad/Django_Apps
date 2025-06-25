from django.contrib import admin
from .models import Profile
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(Profile)
except AlreadyRegistered:
    pass # guards against the admin double registeration 
