
import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    """
    API Client
    """
    return APIClient()


@pytest.fixture()
def user(db):
    """
    User
    """
    return User.objects.create_user(
        {
            "email": "k012@gmail.com",
            "password": "ihembosi",
            "first_name": "uche",
            "last_name": "okafor",
            "phone": "08033668887"
        }
    )
