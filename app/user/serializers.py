"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        # notice that, say, `is_staff` isn't in here, since it should
        #  only be set via the admin. (a user shouldn't be able to set it.)
        fields = ['email', 'password', 'name']
        # extra metadata
        #  user can set password but can't read it.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # this is called *after* teh serializer validates the data
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # you get a create for free but that wouldn't, say,
        #  hash the password. so we want to user our own.
        return get_user_model().objects.create_user(**validated_data)
