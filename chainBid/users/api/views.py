from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.serializers import UserDisplaySerializer


class CurrentUserAPIView(APIView):
    """
    An APIView that provides 'retrieve()' action.
    Retrieve the username of the current user.

    * Only authenticated user can access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, response):
        serializer = UserDisplaySerializer(response.user)
        return Response(serializer.data)
