"""
URL Mappings for he user API.
"""
from django.urls import path

from user import views


# e.g., used for reverse mapping in test_user_api.py
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
