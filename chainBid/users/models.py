from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Future predisposition for possible extensions of the default user model.
    """


class Profile(models.Model):
    """
    User profile.
    Extension of the CustomUser model.

    * Each user has only one related profile.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    available_balance = models.FloatField(default=0)
    frozen_balance = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['user']

    def __str__(self):
        return self.user.username
