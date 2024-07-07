import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from organisation.models import Organisation
from users.custom_user_manager import CustomUserManager


class User(AbstractUser):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=120, null=False)
    lastName = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    phone = models.CharField(max_length=15, null=True)
    organisations = models.ManyToManyField(Organisation, related_name='users')

    username = None

    @property
    def first_name(self):
        return self.firstName

    @first_name.setter
    def first_name(self, value):
        self.firstName = value

    @property
    def last_name(self):
        return self.lastName

    @last_name.setter
    def last_name(self, value):
        self.lastName = value

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
