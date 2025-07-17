import pytest
from tests.menus.factories import ReviewsFactory
from tests.menus.fixtures.menu import menu_item_with_relations


@pytest.fixture
def review(fake_profile, menu_item_with_relations):
    return ReviewsFactory(
        user_profile=fake_profile,
        menu_item=menu_item_with_relations,
        restaurant=menu_item_with_relations.restaurant.first(),
    )
