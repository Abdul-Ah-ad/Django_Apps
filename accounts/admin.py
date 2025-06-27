from django.contrib import admin
from django.contrib.admin import StackedInline
from .models import Profile, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.crypto import get_random_string

class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'user_code', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'user_code')
    ordering = ('email',)
    readonly_fields = ('user_code',)
    inlines = (ProfileInline,)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_code')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'notes')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_code', 'is_staff', 'is_active')}
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.user_code:
            obj.user_code = get_random_string(8)
        super().save_model(request, obj, form, change)

# Register Profile
try:
    admin.site.register(Profile)
except AlreadyRegistered:
    pass

# Register CustomUser
try:
    admin.site.register(CustomUser, CustomUserAdmin)
except AlreadyRegistered:
    pass
