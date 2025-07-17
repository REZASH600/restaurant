import pytest
from tests.menus.factories import MenuItemsFactory, MenuItemImagesFactory



@pytest.fixture
def menu_item_with_relations(multiple_categories, multiple_restaurants):
    return MenuItemsFactory(
        category=multiple_categories, restaurant=multiple_restaurants
    )


@pytest.fixture
def menu_item_image():
    return MenuItemImagesFactory()
