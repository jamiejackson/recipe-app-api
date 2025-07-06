"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # password=None allows creating users without a password initially,
    # useful for testing or initial setup. It's also how Django's User
    # model is designed, allowing you to create a user without a password
    # and then set it later.
    # extra fields are used to pass additional attributes when creating
    # a user, such as first name, last name, etc. So if you eventually
    # add new fields to your user model, you can still create users with
    # those fields.
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        # set_password encrypts the password using Django's built-in
        # hashing algorithm
        user.set_password(password)
        # even though we just have one database, using self._db is
        # best practice for flexibility in the future
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign custom manager to the User model
    objects = UserManager()

    USERNAME_FIELD = 'email'
