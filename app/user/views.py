"""
Views for the user API.
"""
from rest_framework import (
    generics,
    authentication,
    permissions
)
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


# RUAV is provided by django for retrieving and updating objs in db
# get = retrieve, patch = update
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    # authentication
    authentication_classes = [authentication.TokenAuthentication]
    # authorization: must be authenticated -- no other restrictions
    permission_classes = [permissions.IsAuthenticated]

    # override get object - gets object for http request.
    #  just get the user.
    #
    # authed user obj gets assigned to the request object
    #  that's available in view.
    # can use that to return the user obj for the request made
    #  to api
    # steps:
    #  * http get to this endpoint
    #  * gets object to get the user
    #  * retrieves user that was authenticated
    #  * runs it through defined serializer
    #  * returns result to api
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
