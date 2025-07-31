
import pytest
from apps.accounts.api.v1.serializers import UserListSerializer
from django.urls import reverse

@pytest.mark.django_db
class TestUserListSerializer:

    def test_user_list_serializer_contains_expected_fields(self, normal_user, normal_user_profile,rf):
    
        request = rf.get("/api/accounts/users/")

  
        serializer = UserListSerializer(instance=normal_user, context={"request": request})
        data = serializer.data


        expected_fields = {"id", "username", "phone", "profile"}
        assert expected_fields.issubset(data.keys()), f"Missing fields: {expected_fields - data.keys()}"

        assert data["id"] == normal_user.id
        assert data["username"] == normal_user.username
        assert data["phone"] == normal_user.phone
        expected_profile_url = request.build_absolute_uri(
            reverse("accounts:api_v1:user_profile", kwargs={"pk": normal_user_profile.pk})
        )
        assert data["profile"] == expected_profile_url
