"""
URL Mappings for the recipe app.
"""
from django.urls import (
    path,
    # include urls by their url names
    include,
)

# this can create routes for all options available for view
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
# register recipes name to the viewset:
#  creates api endpoing at api/recipes
#  autognerated urls based on functionality of viewset
#  1.e. create, read, update, delete
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

# used by reverse lookup of urls
app_name = 'recipe'

urlpatterns = [
    # include url patterns created by the router
    path('', include(router.urls)),
]
