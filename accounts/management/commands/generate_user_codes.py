from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate user_code for users without one'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.filter(user_code__isnull=True)
        for user in users:
            user.user_code = get_random_string(8)
            user.save()
        self.stdout.write(self.style.SUCCESS('User codes generated.'))
