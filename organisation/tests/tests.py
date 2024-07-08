import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from organisation.models import Organisation
from users.authentication import refresh_token
from users.models import User


@pytest.fixture
def api_client():
    """
    API Client
    """
    return APIClient()


@pytest.fixture
def setup_data():
    """
    Setting Up Data
    """
    user1 = User.objects.create_user(
        email="k@gmail.com",
        password="1234",
        firstName="Test",
        lastName="User",
        phone="08033668887"
    )
    user2 = User.objects.create_user(
        email="k1@gmail.com",
        password="1234",
        firstName="Test",
        lastName="User",
        phone="08033668887"
    )
    user3 = User.objects.create_user(
        email="k2@gmail.com",
        password="1234",
        firstName="Test",
        lastName="User",
        phone="08033668887"
    )

    org1 = Organisation.objects.create(name='Org1', description='Organization 1')
    org2 = Organisation.objects.create(name='Org2', description='Organization 2')
    org3 = Organisation.objects.create(name='Org3', description='Organization 3')

    user1.organisations.add(org1)
    user2.organisations.add(org2)
    user3.organisations.add(org3)

    return {
        'user1': user1,
        'user2': user2,
        'user3': user3,
        'org1': org1,
        'org2': org2,
        'org3': org3,
    }


@pytest.mark.django_db
class TestOrganisationAccess:

    def test_user_can_access_own_organisation(self, setup_data, api_client):
        user1 = setup_data['user1']
        org1 = setup_data['org1']

        token = refresh_token(user1).access_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        url = reverse('organisation', kwargs={'pk': org1.orgId})
        response = api_client.get(url)

        assert response.status_code == 200
        print(response.data)
        assert response.data['data']['name'] == 'Org1'
        assert response.data['data']['description'] == 'Organization 1'

    def test_user_cannot_access_other_organisations(self, setup_data, api_client):
        user1 = setup_data['user1']
        org2 = setup_data['org2']

        api_client.force_authenticate(user=user1)

        url = reverse('organisation', kwargs={'pk': org2.orgId})
        response = api_client.get(url)

        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
