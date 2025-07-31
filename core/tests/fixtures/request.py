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
def normal_user_client(normal_user):
    client = APIClient()
    token = AccessToken.for_user(normal_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
    return client

@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    token = AccessToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
    return client

