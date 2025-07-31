# tests/menus/test_serializers/test_user_favorite_menu_item_serializer.py

import pytest
from apps.menus.api.v1.serializers import UserFavoriteMenuItemSerializer
from rest_framework.request import Request


@pytest.mark.django_db
class TestUserFavoriteMenuItemSerializer:

    def test_serialize_user_favorite_menu_item(self, user_favorite_menu_item, rf):
        serializer = UserFavoriteMenuItemSerializer(
            user_favorite_menu_item,
            context={"request": Request(rf.get("/"))},
        )
        data = serializer.data

        assert data["id"] == user_favorite_menu_item.id
        assert "menu_item" in data
        assert "created_at" in data

    def test_create_user_favorite_menu_item(
        self, normal_user_profile, menu_item_with_relations
    ):
        data = {"menu_item": menu_item_with_relations.id}

        serializer = UserFavoriteMenuItemSerializer(
            data=data,
            context={"request": type("Req", (), {"user": normal_user_profile.user})()},
        )
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save()

        assert instance.menu_item == menu_item_with_relations
        assert instance.user_profile == normal_user_profile

    def test_duplicate_favorite_should_fail(
        self, user_favorite_menu_item, normal_user_profile
    ):
        data = {"menu_item": user_favorite_menu_item.menu_item.id}

        serializer = UserFavoriteMenuItemSerializer(
            data=data,
            context={"request": type("Req", (), {"user": normal_user_profile.user})()},
        )

        is_valid = serializer.is_valid()
        if is_valid:
            with pytest.raises(Exception):
                serializer.save()
        else:
            assert (
                "non_field_errors" in serializer.errors
                or "menu_item" in serializer.errors
            )
