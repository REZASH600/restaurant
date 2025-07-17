import pytest
from apps.accounts.api.v1.serializers import RegisterUserSerializer

@pytest.mark.django_db
class TestRegisterUserSerializer:

    def test_valid_data_creates_user(self):
        valid_data = {
            "username": "user1",
            "phone": "09123456789",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        serializer = RegisterUserSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.username == valid_data["username"]
        assert user.phone == valid_data["phone"]

        assert user.check_password(valid_data["password1"])

    def test_password_mismatch(self):
        data = {
            "username": "user2",
            "phone": "09123456789",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass122!",
        }
        serializer = RegisterUserSerializer(data=data)
        assert not serializer.is_valid()
        assert "password2" in serializer.errors

    def test_password_validation(self):
        data = {
            "username": "user3",
            "phone": "09123456789",
            "password1": "123",
            "password2": "123",
        }
        serializer = RegisterUserSerializer(data=data)
        assert not serializer.is_valid()
        assert "password1" in serializer.errors