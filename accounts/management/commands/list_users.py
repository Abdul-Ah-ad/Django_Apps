from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'List all users and their codes'

    def handle(self, *args, **kwargs):
        for user in CustomUser.objects.all():
            self.stdout.write(f'{user.email} - {user.user_code}')
