import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

@pytest.fixture
def rf():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(super_user):
    client = APIClient()
    token = AccessToken.for_user(super_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
    return client