import pytest
from tests.menus.factories import ReviewsFactory



@pytest.fixture
def review(normal_user_profile, menu_item_with_relations):
    return ReviewsFactory(
        user_profile=normal_user_profile,
        menu_item=menu_item_with_relations,
        restaurant=menu_item_with_relations.restaurant.first(),
    )
