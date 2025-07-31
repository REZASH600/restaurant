import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache



@pytest.mark.django_db
class TestChangePasswordApiView:
    def test_change_password_valid(self, api_client, normal_user):
        normal_user.set_password("old_pass123")
        normal_user.save()

        token = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")

        url = reverse("accounts:api_v1:change_password")
        data = {
            "old_password": "old_pass123",
            "password1": "Newpass@123",
            "password2": "Newpass@123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestSendEmailApiView:
    def test_send_email_token(self, api_client, normal_user, normal_user_profile):
        normal_user_profile.temporary_email = "test@example.com"
        normal_user_profile.save()

        token = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:send_email")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestVerifyEmailApiView:
    def test_verify_email_token_valid(self, api_client, normal_user, normal_user_profile):
        token = "123456"
        normal_user_profile.temporary_email = "test@example.com"
        normal_user_profile.save()

        cache_key = f"verify_email:{normal_user.id}"
        cache.set(cache_key, token)

        jwt = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(jwt)}")

        url = reverse("accounts:api_v1:verify_email")
        response = api_client.post(url, {"token": token})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestSendPhoneOtpApiView:
    def test_send_phone_otp(self, api_client, normal_user):
        normal_user.is_phone_verified = False
        normal_user.save()
        token = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:send_phone_otp")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestVerifyPhoneOtpApiView:
    def test_verify_phone_otp_valid(self, api_client, normal_user):
        token_value = "654321"
        cache.set(f"verify_phone:{normal_user.id}", token_value)

        jwt = AccessToken.for_user(normal_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(jwt)}")
        url = reverse("accounts:api_v1:verify_phone_otp")
        response = api_client.post(url, {"token": token_value})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCheckoutApiViews:
    def test_list_checkouts(self, api_client, normal_user_profile):
        token = AccessToken.for_user(normal_user_profile.user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:checkout_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_checkout(self, api_client, normal_user_profile):
        token = AccessToken.for_user(normal_user_profile.user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:checkout_create")
        data = {
            "address": "Test st",
            "city": "Tehran",
            "state": "Tehran",
            "postal_code": "1234567890",
            "recipient_name": "Ali",
            "recipient_phone": "09120001122",
            "is_default": False,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_checkout(self, api_client, default_checkout):
        token = AccessToken.for_user(default_checkout.user_profile.user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        url = reverse("accounts:api_v1:checkout_update", args=[default_checkout.id])
        data = {"city": "Mashhad"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
