"""Tests for tag APIs."""

"""Test for recipe APIS"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import (
    TagSerializer
)

TAGS_URL = reverse('recipe:tag-list')

# def detail_url(tag_id):
#     """Create and return a recipe detail URL."""
#     return reverse('recipe:tag-detail', args=[tag_id])

# from recipe.serializers import (
#     RecipeSerializer,
#     RecipeDetailSerializer,
# )

def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    get_user_model().objects.create(
        email=email,
        password=password,
    )


class PublicTagAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Rest authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.all().order_by('-name')
        # many=True because we're going to be getting multiple
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        Tag.objects.create(user=other_user, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

        # get user 1's tags from the db
        tags = Tag.objects.filter(user=self.user)
        # convert tags to simple list
        serializer = TagSerializer(recipes, many=True)
        # compare response data to db data for the user
        self.assertEqual(res.data, serializer.data)
