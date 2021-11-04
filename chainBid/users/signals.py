from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from utils.randomics import generate_random_string

UserModel = get_user_model()


@receiver(pre_save, sender=UserModel)
def set_user_slug(sender, instance, *args, **kwargs):
    """
    Set the user slug when a new user is created.
    """

    if instance and not instance.slug:
        slug = slugify(instance.username)
        random_string = generate_random_string()
        instance.slug = f"{slug}-{random_string}"
