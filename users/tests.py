from datetime import datetime, timedelta, timezone

import jwt
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


def test_token_generation(api_client, user):
    response = api_client.post('https://stratus-nine.vercel.app/auth/login', {
        'email': 'k@gmail.com',
        'password': '1234'
    })

    assert response.status_code == 200

    access_token = response.data['data'].get('accessToken')
    assert isinstance(access_token, str)

    decoded_token = jwt.decode(access_token, options={"verify_signature": False})

    expiration_timestamp = decoded_token['exp']
    expiration_datetime = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)
    expected_expiration_time = datetime.now(tz=timezone.utc) + timedelta(minutes=10)

    assert abs((expiration_datetime - expected_expiration_time).total_seconds()) < 10
    assert decoded_token['userId'] == str(user.userId)
