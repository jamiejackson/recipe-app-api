"""Test for recipe APIS"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(
        user=user,
        **defaults
    )
    return recipe


def create_user(**params):

    return get_user_model().objects.create_user(**params)


class PubliceRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)

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

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        # note that res.data would be a simple python data stucture
        #  represents the json
        res = self.client.get(RECIPES_URL)

        # id, descending
        recipes = Recipe.objects.all().order_by('-id')

        # turn the recipes into a list of simple structures that
        #  matches the stucture of res.data
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com',
            password='password123',
        )
        create_recipe(other_user)
        create_recipe(self.user)

        res = self.client.get(RECIPES_URL)

        # get user 1's recipes from the db
        recipes = Recipe.objects.filter(user=self.user)
        # convert recipes to simple list
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # compare response data to db data for the user
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
            'link': 'https://example.com/yumtown',
            'description': 'Taste-good goo for dinner.'
        }

        res = self.client.post(RECIPES_URL, payload)  # /api/recipes/recipe

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        for k, v in payload.items():
            # use getattr. recipe[k] won't work since this is an obj.
            #  not a dict.
            # https://docs.python.org/3/library/functions.html#getattr
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial updte of a recipe."""
        original_details = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
            'link': 'https://example.com/yumtown',
            'description': 'Taste-good goo for dinner.'
        }
        patch_data = {
            'time_minutes': 35,
        }
        expeted_details = {
            **original_details,
            **patch_data
        }

        recipe = create_recipe(self.user, **original_details)
        recipe_id = recipe.id

        res = self.client.patch(detail_url(recipe_id), patch_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        for k, v in expeted_details.items():
            # use getattr. recipe[k] won't work since this is an obj.
            #  not a dict.
            # https://docs.python.org/3/library/functions.html#getattr
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test full update of recipe."""
        original_details = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
            'link': 'https://example.com/yumtown',
            'description': 'Taste-good goo for dinner.'
        }
        update_details = {
            'title': 'Sample recipe updated',
            'time_minutes': 31,
            'price': Decimal('6.99'),
            'link': 'https://example.com/yumtowne',
            'description': 'Taste-good goo for fifth-meal.'
        }
        recipe = create_recipe(user=self.user, **original_details)

        res = self.client.put(detail_url(recipe.id), update_details)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        for k, v in update_details.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error."""
        another_user=create_user(email='user2@example.com')
        recipe = create_recipe(user=self.user)

        # DRF ignores fields not in the serializer (like user_id),
        # so the PATCH succeeds with 200 OK
        res = self.client.patch(
            detail_url(recipe.id),
            {'user_id': another_user.id},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        recipe = create_recipe(user=self.user)

        res = self.client.delete(detail_url(recipe.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id))
