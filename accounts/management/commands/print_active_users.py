from django.core.management.base import BaseCommand
from accounts.models import CustomUser  # Example model

class Command(BaseCommand):
    help = 'List all active users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.filter(is_active=True)
        for user in users:
            self.stdout.write(self.style.SUCCESS(user.email))
