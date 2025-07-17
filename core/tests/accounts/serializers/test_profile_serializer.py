import pytest
from apps.accounts.api.v1.serializers import ProfileSerializer

@pytest.mark.django_db
class TestProfileSerializer:

    def test_serialize_profile(self, fake_profile):
        serializer = ProfileSerializer(fake_profile)
        data = serializer.data

        for field in ProfileSerializer.Meta.fields:
            assert field in data

    def test_is_email_verified_true(self, fake_profile):
        user = fake_profile.user
        user.email = "test@example.com"
        fake_profile.temporary_email = "test@example.com"
        user.save()
        fake_profile.save()

        serializer = ProfileSerializer(fake_profile)
        assert serializer.data["is_email_verified"] is True

    def test_is_email_verified_false(self, fake_profile):
        user = fake_profile.user
        user.email = "test1@example.com"
        fake_profile.temporary_email = "test2@example.com"
        user.save()
        fake_profile.save()

        serializer = ProfileSerializer(fake_profile)
        assert serializer.data["is_email_verified"] is False
