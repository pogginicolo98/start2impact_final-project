from rest_framework import serializers
from users.models import CustomUser


class UserDisplaySerializer(serializers.ModelSerializer):
    """
    ModelSerializer for display user's data.
    """

    class Meta:
        model = CustomUser
        fields = ['username']
