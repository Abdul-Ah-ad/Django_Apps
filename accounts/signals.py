from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, pre_init, post_init
from django.dispatch import receiver
from .models import CustomUser, Profile

# --- INIT SIGNALS ---
@receiver(pre_init, sender=CustomUser)#decorators
def on_pre_init(sender, *args, **kwargs):
    print(f"[PRE_INIT] About to init {sender.__name__}")

@receiver(post_init, sender=CustomUser)
def on_post_init(sender, instance, **kwargs):
    print(f"[POST_INIT] Initialized {instance}")

# --- SAVE SIGNALS ---
@receiver(pre_save, sender=CustomUser)
def on_pre_save(sender, instance, **kwargs):
    print(f"[PRE_SAVE] About to save {instance.email}")

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Automatically create an empty profile linked to this user
        Profile.objects.create(user=instance)
        print(f"[POST_SAVE] Auto-created profile for {instance.email}")
    else:
        print(f"[POST_SAVE] User updated: {instance.email}")

# --- DELETE SIGNALS ---
@receiver(pre_delete, sender=CustomUser)
def on_pre_delete(sender, instance, **kwargs):
    print(f"[PRE_DELETE] Deleting {instance.email}")

@receiver(post_delete, sender=CustomUser)
def on_post_delete(sender, instance, **kwargs):
    print(f"[POST_DELETE] Deleted {instance.email}")
