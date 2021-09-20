from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile instance associated with the new user instance created.
    """

    if created:
        Profile.objects.create(user=instance)
