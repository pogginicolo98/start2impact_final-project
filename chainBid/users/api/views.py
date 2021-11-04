from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from users.api.serializers import RequestUserSerializer, UserProfileSerializer

UserModel = get_user_model()


class RequestUserAPIView(RetrieveAPIView):
    """
    An APIView that provides 'retrieve()' action.
    Retrieve the username of the current user.

    * Only authenticated user can access this endpoint.
    """

    serializer_class = RequestUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        serializer = self.serializer_class(self.request.user)
        return serializer.data


class UserProfileAPIView(RetrieveAPIView):
    """
    An APIView that provides 'retrieve()' action.
    Retrieve the profile information of a specific user.

    * Only authenticated user can access this endpoint.
    """

    queryset = UserModel.objects.all()
    lookup_field = "slug"
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
