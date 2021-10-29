from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Future predisposition for possible extensions of the default user model.
    """

    slug = models.SlugField(max_length=255, unique=True)
