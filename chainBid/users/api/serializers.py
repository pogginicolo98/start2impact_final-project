from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class RequestUserSerializer(serializers.ModelSerializer):
    """
    ModelSerializer to distinguish the user's privileges.
    """

    class Meta:
        model = UserModel
        fields = ['username', 'is_staff', 'slug']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for display user's data.
    """

    auctions_won = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'auctions_won']

    def get_auctions_won(self, instance):
        return instance.auctions.count()
