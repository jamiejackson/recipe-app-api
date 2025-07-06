"""
Views for the user API.
"""
# rest_framework handles a lot of the logic that we need for creating
#  objects in the database
# it does it by providing base classes that we
# can configure in our views which will handle the requests
# in a default/standardized way
# but we can override/modify
from rest_framework import generics

from user.serializers import UserSerializer


# CreateAPIView handles POSTS for creating objects in the db
# so all we need to do is provide the serializer class on the view
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    # djankgo knows which model since that's set in the serializer
    serializer_class = UserSerializer
