from django.db import migrations


def set_notes_for_existing_users(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'CustomUser')
    for user in CustomUser.objects.all():
        if not user.notes:
            user.notes = "Auto note for existing user"
            user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts',  '0002_customuser_notes'),
    ]

    operations = [
    ]

