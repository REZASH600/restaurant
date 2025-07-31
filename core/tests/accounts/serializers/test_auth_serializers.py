import pytest
from apps.accounts.api.v1.serializers import (
    ChangePassowrdSerializer,
    VerifyTokenApiSerializer,
    CheckoutSerializer,
)


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_valid_change_password(self, normal_user):
        normal_user.set_password("OldPass123!")
        normal_user.save()

        data = {
            "old_password": "OldPass123!",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
        }
        serializer = ChangePassowrdSerializer(
            data=data, context={"request": type("Req", (), {"user": normal_user})()}
        )
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.check_password(data["password1"])

    def test_wrong_old_password(self, normal_user):
        normal_user.set_password("OldPass123!")
        normal_user.save()

        data = {
            "old_password": "WrongOldPass!",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
        }
        serializer = ChangePassowrdSerializer(
            data=data, context={"request": type("Req", (), {"user": normal_user})()}
        )
        assert not serializer.is_valid()
        assert "old_password" in serializer.errors

    def test_password_mismatch(self, normal_user):
        normal_user.set_password("OldPass123!")
        normal_user.save()

        data = {
            "old_password": "OldPass123!",
            "password1": "NewPass123!",
            "password2": "DifferentPass123!",
        }
        serializer = ChangePassowrdSerializer(
            data=data, context={"request": type("Req", (), {"user": normal_user})()}
        )
        assert not serializer.is_valid()
        assert "password2" in serializer.errors


@pytest.mark.django_db
class TestVerifyTokenApiSerializer:

    def test_valid_token(self):
        data = {"token": "123456"}
        serializer = VerifyTokenApiSerializer(data=data)
        assert serializer.is_valid()

    def test_token_too_long(self):
        data = {"token": "1234567"}
        serializer = VerifyTokenApiSerializer(data=data)
        assert not serializer.is_valid()
        assert "token" in serializer.errors


@pytest.mark.django_db
class TestCheckoutSerializer:

    def test_serialize_checkout(self, default_checkout):
        serializer = CheckoutSerializer(default_checkout)
        data = serializer.data
        for field in CheckoutSerializer.Meta.fields:
            assert field in data

    def test_create_checkout_assigns_user_profile(self, normal_user_profile):
        data = {
            "address": "123 Main St",
            "city": "Tehran",
            "state": "Tehran Province",
            "postal_code": "1234567891",
            "recipient_phone": "09123456789",
            "recipient_name": "John Doe",
            "is_default": True,
        }

        class FakeRequest:
            user = type("User", (), {"profile": normal_user_profile})()

        serializer = CheckoutSerializer(data=data, context={"request": FakeRequest()})
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save()
        assert instance.user_profile == normal_user_profile
        assert instance.address == data["address"]
