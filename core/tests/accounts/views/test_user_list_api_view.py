import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestUserListApiView:
    def test_admin_user_can_list_users(self, admin_client):
        url = reverse("accounts:api_v1:user_list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_non_admin_user_cannot_list_users(self, api_client, normal_user):
        token = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:user_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN