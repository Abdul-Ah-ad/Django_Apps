import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ---------- Custom User Manager ----------
class CustomUserManager(BaseUserManager): #custom Authentication
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# ---------- Custom User Model ----------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    objects = CustomUserManager() 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No other required fields

    def save(self, *args, **kwargs):
        # Remove punctuation from username, first_name, last_name
        remove_punct = lambda s: ''.join(ch for ch in s if ch not in string.punctuation) if s else s

        self.username = remove_punct(self.username)
        self.first_name = remove_punct(self.first_name)
        self.last_name = remove_punct(self.last_name)
        
        # Force email lowercase 
        if self.email:
            self.email = self.email.lower()

        super().save(*args, **kwargs) 

    
    def __str__(self):
        return self.email

# ---------- Profile Model ----------
class Profile(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
