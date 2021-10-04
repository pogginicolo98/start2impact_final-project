from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    """
    ModelSerializer for display user's data.
    """

    class Meta:
        model = UserModel
        fields = ['username', 'is_staff']
