import pytest
from rest_framework import status
from django.urls import reverse



@pytest.mark.django_db
class TestRegisterUserApiView:
    def test_register_user_successfully(self, api_client):
        url = reverse("accounts:api_v1:user_register")
        data = {
            "username": "newuser",
            "phone": "09120001122",
            "password1": "Test@1234",
            "password2": "Test@1234"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
