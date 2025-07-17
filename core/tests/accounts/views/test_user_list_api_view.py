import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestUserListApiView:
    def test_super_user_can_list_users(self, auth_client):
        url = reverse("accounts:api_v1:user_list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_non_super_user_cannot_list_users(self, api_client, fake_user):
        token = AccessToken.for_user(fake_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:user_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN