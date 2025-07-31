import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestProfileApiView:
    def test_get_own_profile(self, api_client, normal_user_profile):
        token = AccessToken.for_user(normal_user_profile.user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:user_profile", kwargs={"pk": normal_user_profile.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
