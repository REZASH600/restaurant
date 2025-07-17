
import pytest
from apps.accounts.api.v1.serializers import UserListSerializer
from django.urls import reverse

@pytest.mark.django_db
class TestUserListSerializer:

    def test_user_list_serializer_contains_expected_fields(self, fake_user, fake_profile,rf):
    
        request = rf.get("/api/accounts/users/")

  
        serializer = UserListSerializer(instance=fake_user, context={"request": request})
        data = serializer.data


        expected_fields = {"id", "username", "phone", "profile"}
        assert expected_fields.issubset(data.keys()), f"Missing fields: {expected_fields - data.keys()}"

        assert data["id"] == fake_user.id
        assert data["username"] == fake_user.username
        assert data["phone"] == fake_user.phone
        expected_profile_url = request.build_absolute_uri(
            reverse("accounts:api_v1:user_profile", kwargs={"pk": fake_profile.pk})
        )
        assert data["profile"] == expected_profile_url
