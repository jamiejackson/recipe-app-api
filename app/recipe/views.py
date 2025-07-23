"""
Views for the recipe APIs.
"""

from rest_framework import (
    viewsets,
    mixins,  # things you can add to a view for more functionality
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""

    # since most methods will use the detail serializer
    #  use this one as the default
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    # authentication
    authentication_classes = [TokenAuthentication]
    # authorization
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # method that's called when DRF wants to determine the class
    #  being used for a particular action
    # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    def get_serializer_class(self):
        """Return the serializer class for request."""

        # list uses the less common non-detail one
        if self.action == 'list':
            # the class, not an instance of the serialize.
            #  django will instantiate it.
            return serializers.RecipeSerializer

        # otherwise, use the common one
        return self.serializer_class

    # save & deletion hook docs:
    #  https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself

    # override the way django saves a model in a viewset
    # we pass in the serializer,
    #  which will have already been validated by the viewset
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


# viewset because just CRUD
class TagViewSet(
        # this combination only providees list/GET
        mixins.ListModelMixin,
        viewsets.GenericViewSet,  # allows mixins
):
    """Manage tags in the database."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tags for authenticated user."""
        # without this, it would get all tags
        return self.queryset.filter(user=self.request.user).order_by('-name')
