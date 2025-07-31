import pytest
from apps.accounts.api.v1.serializers import ProfileSerializer

@pytest.mark.django_db
class TestProfileSerializer:

    def test_serialize_profile(self, normal_user_profile):
        serializer = ProfileSerializer(normal_user_profile)
        data = serializer.data

        for field in ProfileSerializer.Meta.fields:
            assert field in data

    def test_is_email_verified_true(self, normal_user_profile):
        user = normal_user_profile.user
        user.email = "test@example.com"
        normal_user_profile.temporary_email = "test@example.com"
        user.save()
        normal_user_profile.save()

        serializer = ProfileSerializer(normal_user_profile)
        assert serializer.data["is_email_verified"] is True

    def test_is_email_verified_false(self, normal_user_profile):
        user = normal_user_profile.user
        user.email = "test1@example.com"
        normal_user_profile.temporary_email = "test2@example.com"
        user.save()
        normal_user_profile.save()

        serializer = ProfileSerializer(normal_user_profile)
        assert serializer.data["is_email_verified"] is False
