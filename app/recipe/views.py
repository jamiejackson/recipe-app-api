"""
Views for the recipe APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
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
