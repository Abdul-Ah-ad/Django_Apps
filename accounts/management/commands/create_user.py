from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Create a new test user'

    def handle(self, *args, **kwargs):
        user, created = CustomUser.objects.get_or_create(email='testuser@example.com')
        if created:
            user.set_password('test123')
            user.save()
            self.stdout.write(self.style.SUCCESS("User created successfully"))
        else:
            self.stdout.write(self.style.WARNING("User already exists"))
