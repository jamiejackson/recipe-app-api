"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

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
        """Update and return user."""
        # you get a create for free but that wouldn't, say,
        #  hash the password. so we want to use our own.
        return get_user_model().objects.create_user(**validated_data)

    # override update method on user serializer
    #  (the model that the serializer represents)
    # instance is the model instance to be updated
    def update(self, instance, validated_data):
        """Update a user"""
        password = validated_data.pop('password', None)
        # here we just use the base model's serializer for, say
        #  email and name
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        # this masks the password field
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # called at validation stage by view (affter serializer)
    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            # request is required. not sure why.
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            # standard way to raise auth problem with serializers
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
