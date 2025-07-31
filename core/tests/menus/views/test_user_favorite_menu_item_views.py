import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from apps.menus import models


@pytest.mark.django_db
class TestUserFavoriteMenuItemViews:

    def test_user_can_list_own_favorites(self, api_client, user_favorite_menu_item):
        user = user_favorite_menu_item.user_profile.user
        token = AccessToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")

        url = reverse("menus:api_v1:user_favorite_menuitem_list_create")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)
        assert (
            response.data["results"][0]["menu_item"]
            == user_favorite_menu_item.menu_item.id
        )

    def test_user_can_create_favorite(
        self, api_client, fake_profile, menu_item_with_relations
    ):
        user = fake_profile.user
        token = AccessToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")

        url = reverse("menus:api_v1:user_favorite_menuitem_list_create")
        payload = {"menu_item": menu_item_with_relations.id}
        response = api_client.post(url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert models.UserFavoriteMenuItems.objects.filter(
            user_profile=fake_profile, menu_item=menu_item_with_relations
        ).exists()

    def test_user_can_delete_own_favorite(self, api_client, user_favorite_menu_item):
        user = user_favorite_menu_item.user_profile.user
        token = AccessToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")

        url = reverse(
            "menus:api_v1:favorite_menuitem_delete", args=[user_favorite_menu_item.id]
        )
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not models.UserFavoriteMenuItems.objects.filter(
            id=user_favorite_menu_item.id
        ).exists()
