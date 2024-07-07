import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from organisation.models import Organisation
from users.custom_user_manager import CustomUserManager


class User(AbstractUser):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=120, null=False)
    last_name = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    phone = models.CharField(max_length=15, null=True)
    organisations = models.ManyToManyField(Organisation, related_name='users')
    username = None

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
