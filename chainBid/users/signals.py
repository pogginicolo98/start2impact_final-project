from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile instance associated with the new user instance created.
    """

    if created:
        Profile.objects.create(user=instance)
