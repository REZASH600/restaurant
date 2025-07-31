import pytest
from tests.menus.factories import UserFavoriteMenuItemsFactory

@pytest.fixture
def user_favorite_menu_item(normal_user_profile, menu_item_with_relations):
    return UserFavoriteMenuItemsFactory(
        user_profile=normal_user_profile, menu_item=menu_item_with_relations
    )