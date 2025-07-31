import pytest
from django.db.utils import IntegrityError
from apps.menus.models import UserFavoriteMenuItems


@pytest.mark.django_db
class TestUserFavoriteMenuItemsModel:

    def test_create_favorite(self, normal_user_profile, menu_item_with_relations):
        favorite = UserFavoriteMenuItems.objects.create(
            user_profile=normal_user_profile,
            menu_item=menu_item_with_relations,
        )
        assert favorite.user_profile == normal_user_profile
        assert favorite.menu_item == menu_item_with_relations
        assert favorite.created_at is not None

    def test_unique_together_constraint(self, normal_user_profile, menu_item_with_relations):
        UserFavoriteMenuItems.objects.create(user_profile=normal_user_profile, menu_item=menu_item_with_relations)
        with pytest.raises(IntegrityError):
            UserFavoriteMenuItems.objects.create(user_profile=normal_user_profile, menu_item=menu_item_with_relations)

    def test_str_method(self, normal_user_profile, menu_item_with_relations):
        favorite = UserFavoriteMenuItems.objects.create(user_profile=normal_user_profile, menu_item=menu_item_with_relations)
        expected_str = f"{favorite.user_profile} likes {favorite.menu_item}"
        assert str(favorite) == expected_str
