"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
        ]
        read_only_fields = ['id']

    # by default, nested serializers are read-only
    def create(self, validated_data):
        """Create a recipe."""
        # if we passed tags directly into the Recipe model
        #  it won't work. it expects tags to be assigned
        #  as a related field.
        # `[]` returns empty list instead of KeyError
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        # because this is a serializer and not a view, we need
        #  to get the user from the request context, which the
        #  view passes the serializer.
        auth_user = self.context['request'].user
        for tag in tags:
            # get_or_create gets val if exists, otherwise, creates
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # could also do name=tag['name'], but this is more future-proof
                #  if tag model grows
                **tag,
            )
            recipe.tags.add(tag_obj)
        return recipe


# we'll base this on the base class
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view."""

    # strange to define a class within a class but that's how DRF works.
    class Meta(RecipeSerializer.Meta):
        # just adding an extra field
        fields = RecipeSerializer.Meta.fields + ['description']
