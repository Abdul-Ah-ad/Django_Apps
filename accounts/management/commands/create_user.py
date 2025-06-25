from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a user with provided email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        self.stdout.write(self.style.SUCCESS(f'Creating user: {email}'))
