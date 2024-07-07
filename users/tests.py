
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
        email="k@gmail.com",
        password="1234",
        first_name="Test",
        last_name="User",
        phone="08033668887"
    )
