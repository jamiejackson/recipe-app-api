"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
        ]
        read_only_fields = ['id']


# we'll base this on the base class
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view."""

    # strange to define a class within a class but that's how DRF works.
    class Meta(RecipeSerializer.Meta):
        # just adding an extra field
        fields = RecipeSerializer.Meta.fields + ['description']
