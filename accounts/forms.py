from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class SignupForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta: #rendering these fields
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create associated profile
            Profile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user


class EditProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        # Expect profile instance passed in manually from view
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if profile:
            self.fields['bio'].initial = profile.bio
            self.fields['profile_picture'].initial = profile.profile_picture

    def save(self, user, profile, commit=True):
        user = super().save(commit=False)

        profile.bio = self.cleaned_data['bio']
        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            user.save()
            profile.save()
        return user
