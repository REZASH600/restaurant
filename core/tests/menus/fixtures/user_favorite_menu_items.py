import pytest
from tests.menus.factories import UserFavoriteMenuItemsFactory

@pytest.fixture
def user_favorite_menu_item(fake_profile, menu_item_with_relations):
    return UserFavoriteMenuItemsFactory(
        user_profile=fake_profile, menu_item=menu_item_with_relations
    )