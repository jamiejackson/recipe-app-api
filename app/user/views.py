"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


# CreateAPIView handles POSTS for creating objects in the db
# so all we need to do is provide the serializer class on the view
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    # django knows which model since that's set in the serializer
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # use custom serializer that we created
    #  becuase ObtainAuthToken uses username/pass instead of email/pass
    serializer_class = AuthTokenSerializer
    # use default renderer classes for ObtainAuthToken view.
    # without it we wouldn't get the browseable api that's used for drf
    # not sure why you don't get it by default.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
