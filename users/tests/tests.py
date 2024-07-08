from datetime import datetime, timedelta, timezone

import jwt
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from organisation.models import Organisation
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
        firstName="Test",
        lastName="User",
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


@pytest.mark.django_db
def test_register_user_with_default_organisation(api_client):
    url = reverse('register')
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'accessToken' in response.data['data']
    assert 'user' in response.data['data']
    assert response.data['data']['user']['firstName'] == 'John'
    assert response.data['data']['user']['lastName'] == 'Doe'
    assert response.data['data']['user']['email'] == 'john.doe@example.com'
    organisation_exists = Organisation.objects.filter(name="John's Organisation").exists()
    assert organisation_exists


@pytest.mark.django_db
def test_register_user_duplicate_email(api_client, user):
    url = reverse('register')
    data = {
        'firstName': 'Test',
        'lastName': 'User',
        'email': 'k@gmail.com',
        'password': '1234'
    }

    response = api_client.post(url, data, format='json')
    assert 'status' in response.data
    assert response.data['status'] == 'Bad request'
    assert 'message' in response.data
    assert response.data['message'] == 'Registration unsuccessful'
    assert 'statusCode' in response.data
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
@pytest.mark.parametrize('data', [
    {'lastName': 'Doe', 'email': 'john.doe@example.com', 'password': 'password123'},  # firstName missing
    {'firstName': 'John', 'email': 'john.doe@example.com', 'password': 'password123'},  # lastName missing
    {'firstName': 'John', 'lastName': 'Doe', 'password': 'password123'},  # email missing
    {'firstName': 'John', 'lastName': 'Doe', 'email': 'john.doe@example.com'},  # password missing
])
def test_register_user_missing_required_fields(api_client, data):
    url = reverse('register')

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_user_login_successful(api_client, user):
    url = reverse('login')
    data = {
        'email': 'k@gmail.com',
        'password': '1234'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'accessToken' in response.data['data']
